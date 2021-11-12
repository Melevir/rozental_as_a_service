from __future__ import annotations

import collections
import functools
import logging
import math
import multiprocessing
import os
import sys

from tabulate import tabulate
from sentry_sdk import init as init_sentry


from rozental_as_a_service.args_utils import parse_args, prepare_arguments
from rozental_as_a_service.common_types import TypoInfo
from rozental_as_a_service.config import DEFAULT_WORDS_CHUNK_SIZE, SENTRY_ENABLED, SENTRY_URL
from rozental_as_a_service.db_utils import load_obscene_words
from rozental_as_a_service.extractors_utils import extract_words
from rozental_as_a_service.list_utils import chunks, flat
from rozental_as_a_service.logging_urils import set_logging_level
from rozental_as_a_service.obscene_utils import (
    fetch_obscene_words_base_if_necessary,
)
from rozental_as_a_service.typos_backends import (
    process_with_vocabulary, YaSpellerBackend, AutocorrectCheckerBackend,
)
from rozental_as_a_service.files_utils import get_all_filepathes_recursively, get_content_from_file
from rozental_as_a_service.strings_extractors import (
    extract_from_python_src, extract_from_markdown, extract_from_html,
    extract_from_js,
    extract_from_po,
)

if False:  # TYPE_CHECKING
    from typing import List, Callable, DefaultDict, Tuple

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
logging.getLogger('urllib3').setLevel(logging.INFO)
log = logging.getLogger(__name__)


if SENTRY_ENABLED:
    init_sentry(SENTRY_URL)


def extract_all_constants_from_path(
    path: str,
    exclude: List[str],
    process_dots: bool,
    processes_amount: int,
    verbosity: int = 0,
) -> List[str]:
    extractors = [
        (extract_from_python_src, ['py', 'pyi']),
        (extract_from_markdown, ['md']),
        (extract_from_html, ['html']),
        (extract_from_js, ['js', 'ts', 'tsx']),
        (extract_from_po, ['po']),
    ]

    extension_to_extractor_mapping: DefaultDict[str, List[Callable]] = collections.defaultdict(list)
    for extractor, extensions in extractors:
        for extension in extensions:
            extension_to_extractor_mapping[extension].append(extractor)

    string_constants: List[str] = []

    for extension, extension_extractors in extension_to_extractor_mapping.items():
        all_files = (
            get_all_filepathes_recursively(path, exclude, extension)
            if os.path.isdir(path)
            else [path] if path.endswith(extension) else []
        )
        if not process_dots:
            all_files = [f for f in all_files if '/.' not in f and not f.startswith('.')]
        if not all_files:
            continue
        chunk_size = math.ceil(len(all_files) / processes_amount)
        new_strings = multiprocessing.Pool(processes_amount).map(
            functools.partial(
                extract_all_constants_from_files,
                extractors=extension_extractors,
                verbosity=verbosity,
            ),
            chunks(all_files, chunk_size),
        )
        string_constants += flat(new_strings)
    return list(set(string_constants))


def extract_all_constants_from_files(
    files_pathes: List[str],
    extractors: List[Callable],
    verbosity: int = 0,
) -> List[str]:
    log = logging.getLogger()
    log.addHandler(logging.StreamHandler(sys.stdout))
    set_logging_level(verbosity, log)

    string_constants: List[str] = []
    for filepath in files_pathes:
        for extractor_callable in extractors:
            log.debug(f'Start reading {filepath}...')
            raw_content = get_content_from_file(filepath, guess_encoding=False)
            if raw_content is None:
                raw_content = get_content_from_file(filepath, guess_encoding=True)
            if raw_content is None:
                return []
            log.debug(f'Start processing {filepath}...')
            string_constants += extractor_callable(raw_content)
    return extract_words(list(set(string_constants)))


def fetch_typos_info(string_constants: List[str], backends: List[Callable[[List[str]], Tuple]]) -> List[TypoInfo]:
    typos_info: List[TypoInfo] = []

    for words_chunk in chunks(string_constants, DEFAULT_WORDS_CHUNK_SIZE):
        for words_processor in backends:
            log.debug(f'Using processor {words_processor} for words {words_chunk}')
            _, sure_with_typo_info, unknown = words_processor(words_chunk)
            typos_info += sure_with_typo_info
            # переопределяем переменную цикла так, чтобы следующему процессору доставались
            # только слова, по которым не известно, ок ли они
            words_chunk = unknown

    return typos_info


def reorder_vocabulary(vocabulary_path: str) -> None:
    with open(vocabulary_path, 'r') as file_handler:
        raw_lines = file_handler.readlines()
    sections: List[List[str]] = []
    current_section: List[str] = []
    for line in raw_lines:
        processed_line = line.strip()
        if not processed_line:
            continue
        if processed_line.startswith('#') and current_section:
            sections.append(current_section)
            current_section = []
        current_section.append(processed_line)
    if current_section:
        sections.append(current_section)
    sorted_sections: List[List[str]] = []
    for section_num, section in enumerate(sections, 1):
        sorted_sections.append(
            [f'{r}\n' for r in section if r.startswith('#')]
            + sorted(f'{r}\n' for r in section if not r.startswith('#'))
            + (['\n'] if section_num < len(sections) else []),
        )

    with open(vocabulary_path, 'w') as file_handler:
        file_handler.writelines(flat(sorted_sections))


def main() -> None:
    script_arguments = parse_args()
    arguments = prepare_arguments(script_arguments)

    set_logging_level(arguments['verbosity'], log)

    log.debug(f'Starting with following parameters: {arguments}')

    unique_words = extract_all_constants_from_path(
        arguments['path'],
        arguments['exclude'],
        arguments['process_dots'],
        arguments['processes_amount'],
        arguments['verbosity'],
    )

    available_backends: List[Tuple[str, Callable]] = [
        ('vocabulary', functools.partial(process_with_vocabulary, vocabulary_path=arguments['vocabulary_path'])),
        ('yaspeller', YaSpellerBackend(db_path=arguments['db_path'])),
        ('autocorrect', AutocorrectCheckerBackend()),
    ]
    available_backend_names = [available_backend[0] for available_backend in available_backends]
    for backend_name in arguments['backends']:
        if backend_name not in available_backend_names:
            raise Exception(f'Неизвестный бекенд {backend_name}')

    backends: List[Callable] = [
        backend
        for backend_name, backend in available_backends
        if backend_name in arguments['backends']
    ]

    typos_info = fetch_typos_info(unique_words, backends)
    found_obscene_words = None
    if arguments['ban_obscene_words']:
        fetch_obscene_words_base_if_necessary(arguments['db_path'])
        obscene_words = load_obscene_words(arguments['db_path'])
        found_obscene_words = list(set(unique_words).intersection(obscene_words))

    if arguments['reorder_vocabulary'] and os.path.exists(arguments['vocabulary_path']):
        reorder_vocabulary(arguments['vocabulary_path'])

    if typos_info:
        table = [(t['original'], ', '.join(t['possible_options'])) for t in typos_info]
        print(tabulate(table, headers=('Найденное слово', 'Возможные исправления')))  # noqa

        if found_obscene_words:
            print(f'\n\nНайдены слова ненормативной лексики: {", ".join(found_obscene_words)}')  # noqa
        if not arguments['exit_zero']:
            exit(1)


if __name__ == '__main__':
    main()

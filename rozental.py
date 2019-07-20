import argparse
import os
import re
from typing import List

from tabulate import tabulate

from rozental_as_a_service.ast_utils import extract_all_constants_from_path
from rozental_as_a_service.common_types import TypoInfo, BackendsConfig
from rozental_as_a_service.config import (
    DEFAULT_WORDS_CHUNK_SIZE, DEFAULT_VOCABULARY_FILENAME, DEFAULT_SQLITE_DB_FILENAME,
)
from rozental_as_a_service.list_utils import chunks
from rozental_as_a_service.typos_backends import (
    process_with_vocabulary, process_with_ya_speller,
    process_with_db_with_cache,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=str)
    parser.add_argument('--vocabulary_path', default=None)
    parser.add_argument('--db_path', default=None)
    return parser.parse_args()


def fetch_typos_info(string_constants: List[str], vocabulary_path: str, db_path: str) -> List[TypoInfo]:
    typos_info: List[TypoInfo] = []

    backends = [
        process_with_vocabulary,
        process_with_db_with_cache,
        process_with_ya_speller,
    ]
    backend_config: BackendsConfig = {
        'vocabulary_path': vocabulary_path,
        'db_path': db_path,
        'speller_chunk_size': DEFAULT_WORDS_CHUNK_SIZE,
    }
    for words_chunk in chunks(string_constants, backend_config['speller_chunk_size']):
        for words_processor in backends:
            sure_correct, sure_with_typo_info, unknown = words_processor(words_chunk, backend_config)
            typos_info += sure_with_typo_info
            # переопределяем переменную цикла так, чтобы следующему процессору доставались
            # только слова, по которым не известно, ок ли они
            words_chunk = unknown

    return typos_info


def extract_words(raw_constants: List[str], min_word_length: int = 3, only_russian: bool = True) -> List[str]:
    processed_words: List[str] = []
    for constant in string_constants:
        processed_words += list({
            w.strip().lower() for w in re.findall(r'\w+', constant)
            if len(w.strip()) >= min_word_length
        })
    processed_words = list(set(processed_words))
    if only_russian:
        processed_words = [w for w in processed_words if re.match(r'[а-я]+', w)]
    return processed_words


if __name__ == '__main__':
    arguments = parse_args()
    vocabulary_path = arguments.vocabulary_path or os.path.join(arguments.path, DEFAULT_VOCABULARY_FILENAME)
    db_path = arguments.db_path or os.path.join(arguments.path, DEFAULT_SQLITE_DB_FILENAME)
    string_constants = extract_all_constants_from_path(arguments.path)
    unique_words = extract_words(string_constants)
    typos_info = fetch_typos_info(unique_words, vocabulary_path, db_path)

    table = [t.values() for t in typos_info]
    print(tabulate(table))  # noqa
    if typos_info:
        exit(1)

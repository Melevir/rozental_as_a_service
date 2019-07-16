import argparse
import ast
import math
import re
from typing import List

import requests
from mypy_extensions import TypedDict
from tabulate import tabulate


class TypoInfo(TypedDict):
    original: str
    possible_options: List[str]


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=str)
    return parser.parse_args()


def get_all_filepathes_recursively(path: str, extension: str) -> List[str]:
    from pathlib import Path

    pathlist = Path(path).glob(f'**/*.{extension}')
    return [str(p) for p in pathlist]


def extract_all_constants_from_ast(ast_tree: ast.AST) -> List[str]:
    return list({n.s for n in ast.walk(ast_tree) if isinstance(n, ast.Str)})


def extract_all_constants_from_path(path: str) -> List[str]:
    string_constants: List[str] = []
    for filepath in get_all_filepathes_recursively(path, 'py'):
        with open(filepath, 'r') as file_handler:
            raw_content = file_handler.read()
        ast_tree = ast.parse(raw_content)
        string_constants += extract_all_constants_from_ast(ast_tree)
    return list(set(string_constants))


def fetch_typos_info(string_constants: List[str], chunk_size: int = 100) -> List[TypoInfo]:
    typos_info: List[TypoInfo] = []
    chunks_amount = math.ceil(len(string_constants) / chunk_size)
    for chunk_num, words_chunk in enumerate(chunks(string_constants, chunk_size)):
        print(f'Processing chunk {chunk_num} of {chunks_amount}...')
        speller_result = requests.get(
            'https://speller.yandex.net/services/spellservice.json/checkTexts',
            params={'lang': 'ru', 'text': words_chunk},
        ).json()
        if speller_result:
            for word_info, word in zip(speller_result, words_chunk):
                if word_info and word_info[0]['s']:
                    typos_info.append({
                        'original': word,
                        'possible_options': word_info[0]['s'],
                    })
    return typos_info


def extract_words(raw_constants: List[str], min_word_length: int = 3, only_russian: bool = True) -> List[str]:
    processed_words = []
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
    string_constants = extract_all_constants_from_path(arguments.path)
    unique_words = extract_words(string_constants)
    typos_info = fetch_typos_info(unique_words)

    table = [t.values() for t in typos_info]
    print(tabulate(table))

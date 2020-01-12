import json
import os
import sqlite3
from typing import List, Mapping, Any, Tuple, Optional, Dict, Set

from rozental_as_a_service.config import OBSCENE_BASE_TABLE_NAME
from rozental_as_a_service.list_utils import flat


def save_ya_speller_results_to_db(
        speller_result: List[List[Mapping[str, Any]]],
        words: List[str],
        db_path: str,
) -> None:
    if not os.path.exists(db_path):
        create_db(db_path)
    connection = sqlite3.connect(db_path)
    existing_words = get_existing_words_in_db(words, connection)

    new_results = [(w, r[0] if r else None) for w, r in zip(words, speller_result) if w not in existing_words]
    insert_db_words_info(new_results, connection)


def get_ya_speller_cache_from_db(
    words: List[str],
    db_path: str,
) -> Dict[str, Optional[List[str]]]:
    if not os.path.exists(db_path):
        return {}
    connection = sqlite3.connect(db_path)
    return fetch_words_info_from_db(words, connection)


def create_db(db_path: str) -> None:
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE words (word text, ya_speller_hints_json text)')
    cursor.execute(f'CREATE TABLE {OBSCENE_BASE_TABLE_NAME} (word text)')
    connection.commit()


def get_existing_words_in_db(words: List[str], connection: sqlite3.Connection) -> List[str]:
    cursor = connection.cursor()
    raw_result = cursor.execute(
        'SELECT word FROM words WHERE word IN ({0})'.format(','.join('?' * len(words))),
        words,
    ).fetchall()
    return [r[0] for r in raw_result]


def fetch_words_info_from_db(words: List[str], connection: sqlite3.Connection) -> Dict[str, Optional[List[str]]]:
    cursor = connection.cursor()
    raw_result = cursor.execute(
        'SELECT word, ya_speller_hints_json FROM words WHERE word IN ({0})'.format(','.join('?' * len(words))),
        words,
    ).fetchall()
    return {r: json.loads(info) for r, info in raw_result}


def insert_db_words_info(data: List[Tuple[str, Optional[Mapping]]], connection: sqlite3.Connection) -> None:
    cursor = connection.cursor()
    cursor.executemany(
        'INSERT INTO words (word, ya_speller_hints_json) VALUES (?, ?)',
        [(d[0], json.dumps(d[1]['s'] if d[1] else None)) for d in data],  # type: ignore
    )
    connection.commit()


def is_table_exists(db_path: str, table_name: str) -> bool:
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    raw_result = cursor.execute(
        f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';",
    ).fetchall()
    return bool(raw_result)


def is_obscene_table_has_data(db_path: str) -> bool:
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    raw_result = cursor.execute(
        f'SELECT count(*) FROM {OBSCENE_BASE_TABLE_NAME}',
    ).fetchall()
    return bool(raw_result[0][0])


def create_obscene_base_table(db_path: str) -> None:
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute(f'CREATE TABLE {OBSCENE_BASE_TABLE_NAME} (word text)')
    connection.commit()


def save_obscene_words_to_db(db_path: str, obscene_words: List[str]) -> None:
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.executemany(
        f'INSERT INTO {OBSCENE_BASE_TABLE_NAME} (word) VALUES (?)',
        [[w] for w in obscene_words],
    )
    connection.commit()


def load_obscene_words(db_path: str) -> Set[str]:
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    return set(flat(cursor.execute(
        f'SELECT word FROM {OBSCENE_BASE_TABLE_NAME}',
    ).fetchall()))

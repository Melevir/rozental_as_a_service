import os

from typing import List

import requests

from rozental_as_a_service.config import OBSCENE_BASE_TABLE_NAME, OBSCENE_CORPUS_HTTP_PATH
from rozental_as_a_service.db_utils import (
    is_table_exists, is_obscene_table_has_data, create_db, create_obscene_base_table,
    save_obscene_words_to_db)


def fetch_obscene_words_base_if_necessary(db_path: str) -> None:
    if (
        os.path.exists(db_path)
        and is_table_exists(db_path, OBSCENE_BASE_TABLE_NAME)
        and is_obscene_table_has_data(db_path)
    ):
        return None
    if not os.path.exists(db_path):
        create_db(db_path)
    if not is_table_exists(db_path, OBSCENE_BASE_TABLE_NAME):
        create_obscene_base_table(db_path)
    obscene_words = fetch_obscene_words_from_github()
    save_obscene_words_to_db(db_path, obscene_words)


def fetch_obscene_words_from_github() -> List[str]:
    response = requests.get(OBSCENE_CORPUS_HTTP_PATH)
    return list({w.lower().strip() for w in response.text.strip().split('\n')})

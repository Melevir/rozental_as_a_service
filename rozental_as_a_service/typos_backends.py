import os
from typing import List, Tuple, Optional

import json
import pathlib
import tarfile
from contextlib import closing
from requests import Response, get
from autocorrect import Speller
from sentry_sdk import capture_exception

from rozental_as_a_service.common_types import TypoInfo
from rozental_as_a_service.config import YA_SPELLER_REQUEST_TIMEOUTS, YA_SPELLER_RETRIES_COUNT
from rozental_as_a_service.db_utils import save_ya_speller_results_to_db, get_ya_speller_cache_from_db


PATH = os.path.abspath(os.path.dirname(__file__))


def process_with_vocabulary(
        words: List[str],
        vocabulary_path: Optional[str],
) -> Tuple[List[str], List[TypoInfo], List[str]]:
    if vocabulary_path is None or not os.path.exists(vocabulary_path):
        return [], [], words
    with open(vocabulary_path, encoding='utf8') as file_handler:
        raw_vocabulary = file_handler.readlines()
    vocabulary = {w.strip().lower() for w in raw_vocabulary if not w.strip().startswith('#')}
    correct_words = {w for w in words if w in vocabulary}
    return list(correct_words), [], [w for w in words if w not in correct_words]


class YaSpellerBackend:
    def __init__(self, db_path: Optional[str]):
        self.db_path = db_path

    def __call__(self, words: List[str]) -> Tuple[List[str], List[TypoInfo], List[str]]:
        sure_correct_words, incorrect_typos_info, unknown = self._process_with_db_cache(
            words,
        )
        (
            sure_correct_words_from_ya,
            incorrect_typos_info_from_ya,
            unknown,
        ) = self._process_with_ya_speller(unknown)
        return (
            sure_correct_words + sure_correct_words_from_ya,
            incorrect_typos_info + incorrect_typos_info_from_ya,
            unknown,
        )

    def _process_with_db_cache(
        self,
        words: List[str],
    ) -> Tuple[List[str], List[TypoInfo], List[str]]:
        if self.db_path is None:
            return [], [], words
        words_cache = get_ya_speller_cache_from_db(words, self.db_path)
        sure_correct_words: List[str] = []
        incorrect_typos_info: List[TypoInfo] = []
        for word in words:
            if word not in words_cache:
                continue
            cached_value = words_cache[word]
            if cached_value is None:
                sure_correct_words.append(word)
            else:
                incorrect_typos_info.append(
                    {
                        'original': word,
                        'possible_options': cached_value,
                    },
                )
        known_words = set(
            sure_correct_words + [t['original'] for t in incorrect_typos_info],
        )
        return sure_correct_words, incorrect_typos_info, list(set(words) - known_words)

    def _process_with_ya_speller(
        self,
        words: List[str],
    ) -> Tuple[List[str], List[TypoInfo], List[str]]:
        if not words:
            return [], [], words
        for _ in range(YA_SPELLER_RETRIES_COUNT):
            try:
                response = get(
                    'https://speller.yandex.net/services/spellservice.json/checkTexts',
                    params={'text': words},
                    timeout=YA_SPELLER_REQUEST_TIMEOUTS,
                )
            except TimeoutError as e:
                capture_exception(e)
            else:
                break

        return ([], *_process_ya_speller_response(response, words, self.db_path))


def _process_ya_speller_response(
    response: Response,
    words: List[str],
    db_path: Optional[str],
) -> Tuple[List[TypoInfo], List[str]]:
    typos_info: List[TypoInfo] = []
    speller_result = response.json()
    if speller_result:
        for word_info in speller_result:
            if word_info and word_info[0]['s']:
                typos_info.append({
                    'original': word_info[0]['word'],
                    'possible_options': word_info[0]['s'],
                })
        if db_path is not None:
            save_ya_speller_results_to_db(speller_result, words, db_path)
    typo_words = {t['original'] for t in typos_info}
    return typos_info, [w for w in words if w not in typo_words]


class AutocorrectCheckerBackend:
    def __init__(self) -> None:
        archive_path = pathlib.Path(PATH, 'data', 'ru.tar.gz')
        with closing(tarfile.open(archive_path, 'r:gz')) as tarf, closing(tarf.extractfile('word_count.json')) as file:
            nlp_data = json.load(file)  # type: ignore
        self.checker = Speller('ru', fast=True, nlp_data=nlp_data)

    def __call__(self, words: List[str]) -> Tuple[List[str], List[TypoInfo], List[str]]:
        incorrect_typos_info: List[TypoInfo] = []
        known: List[str] = []
        unknown: List[str] = []
        for word in words:
            if self.checker.existing([word]):
                known.append(word)
                continue
            candidates = [
                candidate[1] for candidate in sorted(
                    self.checker.get_candidates(word), key=lambda item: item[0],
                )
            ]
            if word == candidates[0]:
                known.append(word)
                continue
            incorrect_typos_info.append(
                {
                    'original': word,
                    'possible_options': candidates,
                },
            )
        return known, incorrect_typos_info, unknown

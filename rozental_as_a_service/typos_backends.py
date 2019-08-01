import os
from typing import List, Tuple

import requests

from rozental_as_a_service.common_types import TypoInfo, BackendsConfig
from rozental_as_a_service.db_utils import save_ya_speller_results_to_db, get_ya_speller_cache_from_db


def process_with_vocabulary(
        words: List[str],
        config: BackendsConfig,
) -> Tuple[List[str], List[TypoInfo], List[str]]:
    if config['vocabulary_path'] is None or not os.path.exists(config['vocabulary_path']):
        return [], [], words
    with open(config['vocabulary_path']) as file_handler:
        raw_vocabulary = file_handler.readlines()
    vocabulary = {w.strip().lower() for w in raw_vocabulary if not w.strip().startswith('#')}
    correct_words = {w for w in words if w in vocabulary}
    return list(correct_words), [], [w for w in words if w not in correct_words]


def process_with_db_with_cache(
        words: List[str],
        config: BackendsConfig,
) -> Tuple[List[str], List[TypoInfo], List[str]]:
    if config['db_path'] is None:
        return [], [], words
    words_cache = get_ya_speller_cache_from_db(words, config['db_path'])
    sure_correct_words: List[str] = []
    incorrect_typos_info: List[TypoInfo] = []
    for word in words:
        if word not in words_cache:
            continue
        cached_value = words_cache[word]
        if cached_value is None:
            sure_correct_words.append(word)
        else:
            incorrect_typos_info.append({
                'original': word,
                'possible_options': cached_value,
            })
    known_words = set(sure_correct_words + [t['original'] for t in incorrect_typos_info])
    return sure_correct_words, incorrect_typos_info, list(set(words) - known_words)


def process_with_ya_speller(
        words: List[str],
        config: BackendsConfig,
) -> Tuple[List[str], List[TypoInfo], List[str]]:
    if not words:
        return [], [], words
    typos_info: List[TypoInfo] = []
    response = requests.get(
        'https://speller.yandex.net/services/spellservice.json/checkTexts',
        params={'text': words},
    )
    speller_result = response.json()
    if speller_result:
        for word_info in speller_result:
            if word_info and word_info[0]['s']:
                typos_info.append({
                    'original': word_info[0]['word'],
                    'possible_options': word_info[0]['s'],
                })
        if config['db_path'] is not None:
            save_ya_speller_results_to_db(speller_result, words, config['db_path'])
    typo_words = {t['original'] for t in typos_info}
    return [], typos_info, [w for w in words if w not in typo_words]

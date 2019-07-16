import os
from typing import List, Tuple

import requests

from rozental_as_a_service.common_types import TypoInfo, BackendsConfig


def process_with_vocabulary(
        words: List[str],
        config: BackendsConfig,
) -> Tuple[List[str], List[TypoInfo], List[str]]:
    if not os.path.exists(config['vocabulary_path']):
        return [], [], words
    with open(config['vocabulary_path']) as file_handler:
        raw_vocabulary = file_handler.readlines()
    vocabulary = {w.strip().lower() for w in raw_vocabulary if not w.strip().startswith('#')}
    correct_words = {w for w in words if w in vocabulary}
    return list(correct_words), [], [w for w in words if w not in correct_words]


def process_with_ya_speller(
        words: List[str],
        config: BackendsConfig,
) -> Tuple[List[str], List[TypoInfo], List[str]]:
    typos_info: List[TypoInfo] = []
    speller_result = requests.get(
        'https://speller.yandex.net/services/spellservice.json/checkTexts',
        params={'lang': 'ru', 'text': words},
    ).json()
    if speller_result:
        for word_info, word in zip(speller_result, words):
            if word_info and word_info[0]['s']:
                typos_info.append({
                    'original': word,
                    'possible_options': word_info[0]['s'],
                })
    typo_words = {t['original'] for t in typos_info}
    return [], typos_info, [w for w in words if w not in typo_words]

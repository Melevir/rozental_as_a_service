import re
from typing import List, Tuple

from rozental_as_a_service.text_utils import split_camel_case_words, is_camel_case_word


def extract_words(
    raw_constants: List[str],
    min_word_length: int = 3,
    only_russian: bool = True,
    strip_urls: bool = True,
) -> List[str]:
    common_replacements = [
        # remove diacritic symbols manually
        ('\u0306', ''),
        ('\u0301', ''),
        ('\u0300', ''),
    ]
    url_regexp = r'(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)'
    processed_words: List[str] = []
    raw_camelcase_words: List[str] = []
    for constant in raw_constants:
        if strip_urls:
            constant = re.sub(url_regexp, ' ', constant)

        for replace_from, replace_to in common_replacements:
            constant = constant.replace(replace_from, replace_to)

        new_processed_words, new_camelcase_words = process_raw_constant(constant, min_word_length)
        processed_words += new_processed_words
        raw_camelcase_words += new_camelcase_words
    processed_words += process_camelcased_words(raw_camelcase_words)

    processed_words = list(set(processed_words))

    word_regexp = r'[а-яё-]+' if only_russian else r'[а-яёa-z-]+'
    filtered_words = []
    for word in processed_words:
        match = re.match(word_regexp, word)
        if match:
            word = match.group()
            if 'а-я' not in word and 'a-z' not in word:  # most likely regexp
                filtered_words.append(word)
    processed_words = filtered_words
    return processed_words


def process_raw_constant(constant: str, min_word_length: int) -> Tuple[List[str], List[str]]:
    processed_words: List[str] = []
    raw_camelcase_words: List[str] = []
    for raw_word in re.findall(r'[\w-]+', constant):
        word = raw_word.strip()
        if (
            len(word) >= min_word_length
            and not (word.startswith('-') or word.endswith('-'))
        ):
            if is_camel_case_word(word):
                raw_camelcase_words.append(word)
            else:
                processed_words.append(word.lower())
    return processed_words, raw_camelcase_words


def process_camelcased_words(raw_camelcase_words: List[str]) -> List[str]:
    processed_words: List[str] = []
    for camel_case_words in raw_camelcase_words:
        splitted_words = split_camel_case_words(camel_case_words)
        if splitted_words:
            processed_words += splitted_words
    return processed_words

import re

from typing import List


def is_camel_case_word(word: str) -> bool:
    uppercase_letters_amount = re.subn(r'[A-Z]', '', word)[1]
    lowercase_letters_amount = re.subn(r'[a-z]', '', word)[1]
    return bool(
        (lowercase_letters_amount and uppercase_letters_amount >= 2)
        or re.findall(r'[a-z][A-Z]', word),
    )


def split_camel_case_words(camel_cased_word: str) -> List[str]:
    words_start_indexes = [m.start(0) for m in re.finditer(r'[A-Z]', camel_cased_word)]
    if words_start_indexes[0] > 0:
        words_start_indexes.insert(0, 0)
    if words_start_indexes[-1] < len(camel_cased_word):
        words_start_indexes.append(len(camel_cased_word))
    words = []
    for word_start_index, word_end_index in zip(words_start_indexes, words_start_indexes[1:]):
        words.append(camel_cased_word[word_start_index:word_end_index].lower())
    return words

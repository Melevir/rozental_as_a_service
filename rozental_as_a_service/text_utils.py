import re


def is_long_camel_case_word(word: str, max_words_length: int = 2) -> bool:
    uppercase_letters_amount = re.subn(r'[A-Z]', '', word)[1]
    lowercase_letters_amount = re.subn(r'[a-z]', '', word)[1]
    return bool(lowercase_letters_amount and uppercase_letters_amount >= max_words_length)

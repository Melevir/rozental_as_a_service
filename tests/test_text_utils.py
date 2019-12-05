from rozental_as_a_service.text_utils import is_camel_case_word, split_camel_case_words


def test_is_camel_case_word():
    assert is_camel_case_word('Notcamelcase') is False
    assert is_camel_case_word('IsCamelCase') is True


def test_split_camel_case_words():
    assert split_camel_case_words('ReturnNormalWorlds') == ['return', 'normal', 'worlds']

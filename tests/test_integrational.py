from rozental_as_a_service.rozental import extract_all_constants_from_path, extract_words, fetch_typos_info


def test_finds_correct_py_files_typos():
    string_constants = extract_all_constants_from_path('tests/test_files/', [])
    unique_words = extract_words(string_constants)
    typos_info = fetch_typos_info(unique_words, None, None)
    expected_typos = ['бджета', 'ркеламную', 'содание']
    assert sorted(t['original'] for t in typos_info) == expected_typos

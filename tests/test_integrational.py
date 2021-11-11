import pytest

from rozental_as_a_service.rozental import extract_all_constants_from_path, fetch_typos_info


@pytest.mark.parametrize('vocabulary_path, expected_typos', [
    (None, ['бджета', 'ркеламную', 'содание', 'созадет']),
    ('tests/test_files/.vocabulary', ['бджета', 'содание', 'созадет']),
])
def test_finds_correct_py_files_typos(vocabulary_path, expected_typos):
    unique_words = extract_all_constants_from_path('tests/test_files/', [], process_dots=False, processes_amount=2)
    typos_info = fetch_typos_info(unique_words, vocabulary_path, None)
    assert sorted(t['original'] for t in typos_info) == expected_typos

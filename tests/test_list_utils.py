import pytest

from rozental_as_a_service.list_utils import chunks, flat


@pytest.mark.parametrize('test_value,expected_result', [
    (([1, 2, 3], 2), [[1, 2], [3]]),
    (([], 2), []),
    ((range(3), 2), [range(2), range(2, 3)]),
])
def test_calculate_age_works_fine(test_value, expected_result):
    assert list(chunks(*test_value)) == expected_result


def test_flat():
    assert flat([[1, 2], [3, 4], [5, 6]]) == list(range(1, 7))
    assert flat([['a', 'b'], ['c', 'd']]) == ['a', 'b', 'c', 'd']

from unittest.mock import patch

from rozental_as_a_service.args_utils import parse_args


def test_parse_args(randomized_fake_argv):
    with patch('sys.argv', randomized_fake_argv):
        args = parse_args()
    assert args  # we trust that ArgumentParser is tested

import pytest
from unittest.mock import patch

from conftest import get_temp_file_path
from rozental_as_a_service.files_utils import get_config_path


@pytest.mark.parametrize(
    'custom_path_provided, custom_path_exists, custom_path_matches, '
    'default_path_provided, default_path_exists, default_path_matches',
    [
        (
            False, False, False,
            False, False, False,
        ),
        (
            True, False, False,
            True, False, False,
        ),
        (
            True, True, True,
            False, False, False,
        ),
        (
            True, True, True,
            True, True, False,
        ),
        (
            True, False, False,
            True, True, True,
        ),
    ],
)
def test_get_config_path(
    custom_path_provided, custom_path_exists, custom_path_matches,
    default_path_provided, default_path_exists, default_path_matches,
    fake_custom_path_config_file, fake_base_directory,
    fake_default_config_name,
):
    custom_path = get_temp_file_path(
        remove_file=not custom_path_exists,
        return_empty=not custom_path_provided,
        temp_file=fake_custom_path_config_file,
    )
    base_path = get_temp_file_path(
        remove_file=not default_path_exists,
        return_empty=not default_path_provided,
        temp_file=fake_base_directory,
    )

    with patch('rozental_as_a_service.files_utils.DEFAULT_CONFIG_FILENAME', fake_default_config_name):
        result_path = get_config_path(base_path, custom_path)

    assert (result_path is None) == (custom_path_matches is False and default_path_matches is False)
    assert (result_path == custom_path) == (custom_path_matches is True)
    if result_path and base_path:
        assert (result_path.startswith(base_path)) == (default_path_matches is True)

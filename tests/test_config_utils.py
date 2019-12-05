from unittest.mock import patch

from rozental_as_a_service.config_utils import get_params_from_config


def test_get_params_from_config(fake_section_name, fake_config_params, fake_config_file):
    with patch('rozental_as_a_service.config_utils.CONFIG_SECTION_NAME', fake_section_name):
        params = get_params_from_config(fake_config_file)
    assert params == fake_config_params


def test_get_params_from_config_empty_section(fake_section_name, fake_config_params, fake_config_file):
    different_section_name = f'{fake_section_name}_diff'
    with patch('rozental_as_a_service.config_utils.CONFIG_SECTION_NAME', different_section_name):
        params = get_params_from_config(fake_config_file)
    assert params == {}

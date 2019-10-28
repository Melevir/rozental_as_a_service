import pytest
from faker import Faker

fake = Faker()


@pytest.fixture
def fake_default_config_name():
    return fake.word()


@pytest.fixture
def fake_custom_path_config_file(fake_default_config_name, tmpdir):
    config = tmpdir.mkdir('fake_custom_config_path').join(fake_default_config_name)
    config.write(fake.word())
    return config


@pytest.fixture
def fake_base_directory(fake_default_config_name, tmpdir):
    base_directory = tmpdir.mkdir('fake_base_directory')
    config = base_directory.join(fake_default_config_name)
    config.write(fake.word())
    return base_directory


def get_temp_file_path(remove_file, return_empty, temp_file):
    if return_empty:
        return ''
    if remove_file:
        temp_file.remove()
    return str(temp_file)

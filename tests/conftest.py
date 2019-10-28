import random

import pytest
from faker import Faker

fake = Faker()


@pytest.fixture
def fake_default_config_name():
    return fake.word()

@pytest.fixture
def fake_section_name():
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


@pytest.fixture
def fake_config_params():
    return {
        'processes': fake.pyint(),
        'exclude': [fake.uri_path(), fake.uri_path()],
        'exit_zero': random.choice([True, False]),
        'reorder_vocabulary': random.choice([True, False]),
        'process_dots': random.choice([True, False]),
        'verbosity': fake.pyint(),
    }


@pytest.fixture
def fake_config_file(fake_section_name, fake_config_params, tmpdir):
    lines = [f'[{fake_section_name}]']

    for name, value in fake_config_params.items():
        if isinstance(value, list):
            value = ','.join(value)
        lines.append(f'{name} = {value}')
    file_contents = '\n'.join(lines)

    config_file = tmpdir.join('config')
    config_file.write(file_contents)
    return str(config_file)


@pytest.fixture
def randomized_fake_argv():
    argv = ['command_name']  # cli command name is always the first argument
    argv.append(fake.uri_path())  # path, required argument

    string_arguments = {
        '--config': fake.uri_path(),
        '--exclude': ','.join([fake.uri_path()]),
        '--db_path': fake.uri_path(),
        '--processes': str(fake.pyint()),
    }
    for name, value in string_arguments.items():
        argv.append(name)
        argv.append(value)

    boolean_arguments = {
        '--exit_zero': random.choice([True, False]),
        '--reorder_vocabulary': random.choice([True, False]),
        '--process_dots': random.choice([True, False]),
        '--verbose': random.choice([True, False]),
    }
    for name, is_true in boolean_arguments.items():
        if is_true:
            argv.append(name)

    return argv

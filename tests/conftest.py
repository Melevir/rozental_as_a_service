import random

import pytest
from faker import Faker

fake = Faker()


@pytest.fixture
def fake_section_name():
    return fake.word()


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

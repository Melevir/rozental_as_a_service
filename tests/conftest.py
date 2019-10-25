import random

import pytest
from faker import Faker

fake = Faker()


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

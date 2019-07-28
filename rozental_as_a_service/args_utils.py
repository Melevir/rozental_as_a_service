import argparse
import multiprocessing
import os
from typing import Any, Mapping

from rozental_as_a_service.common_types import RozentalOptions
from rozental_as_a_service.config import DEFAULT_SQLITE_DB_FILENAME, DEFAULT_VOCABULARY_FILENAME
from rozental_as_a_service.config_utils import get_params_from_config
from rozental_as_a_service.files_utils import get_config_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=str)
    parser.add_argument('--config', metavar='config_path')
    parser.add_argument('--vocabulary_path')
    parser.add_argument('--exclude', default='')
    parser.add_argument('--db_path')
    parser.add_argument('--exit_zero', action='store_true')
    parser.add_argument('--processes', type=int, default=None)
    parser.add_argument('-v', action='count', default=0)

    return parser.parse_args()


def prepare_arguments(argparse_args: argparse.Namespace) -> RozentalOptions:
    config_path = get_config_path(argparse_args.path, argparse_args.config)
    config: Mapping[str, Any] = {}
    if config_path:
        config = get_params_from_config(config_path)

    processes_amount = argparse_args.processes or config.get('processes') or multiprocessing.cpu_count()
    vocabulary_path = (
        argparse_args.vocabulary_path
        or config.get('vocabulary_path')
        or os.path.join(argparse_args.path, DEFAULT_VOCABULARY_FILENAME)
    )
    db_path = (
        argparse_args.db_path
        or config.get('db_path')
        or os.path.join(argparse_args.path, DEFAULT_SQLITE_DB_FILENAME)
    )
    exclude = argparse_args.exclude.split(',') if argparse_args.exclude else config.get('exclude', [])
    exit_zero = argparse_args.exit_zero or config.get('exit_zero') or False
    verbosity = argparse_args.v or config.get('v') or 0

    return {
        'path': argparse_args.path,
        'vocabulary_path': vocabulary_path,
        'exclude': exclude,
        'db_path': db_path,
        'exit_zero': exit_zero,
        'processes_amount': processes_amount,
        'verbosity': verbosity,
    }

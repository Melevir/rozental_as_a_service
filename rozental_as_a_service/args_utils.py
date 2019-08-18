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
    parser.add_argument('--reorder_vocabulary', action='store_true', help='reorder vocabulary in alphabetical order')
    parser.add_argument('--process_dots', action='store_true', help='process dot-files and dot-directories')
    parser.add_argument('--processes', type=int, default=None)
    parser.add_argument('-v', action='count', default=0)

    return parser.parse_args()


def prepare_arguments(argparse_args: argparse.Namespace) -> RozentalOptions:
    config_path = get_config_path(argparse_args.path, argparse_args.config)
    config: Mapping[str, Any] = {}
    if config_path:
        config = get_params_from_config(config_path)

    default_processors_amount = multiprocessing.cpu_count() if os.path.isdir(argparse_args.path) else 1
    processes_amount = argparse_args.processes or config.get('processes') or default_processors_amount
    if not os.path.exists(argparse_args.path):
        base_path = '.'
    else:
        base_path = (
            argparse_args.path
            if os.path.isdir(argparse_args.path)
            else os.path.dirname(os.path.abspath(argparse_args.path))
        )
    vocabulary_path = (
        argparse_args.vocabulary_path
        or config.get('vocabulary_path')
        or os.path.join(base_path, DEFAULT_VOCABULARY_FILENAME)
    )
    db_path = (
        argparse_args.db_path
        or config.get('db_path')
        or os.path.join(base_path, DEFAULT_SQLITE_DB_FILENAME)
    )
    exclude = argparse_args.exclude.split(',') if argparse_args.exclude else config.get('exclude', [])
    exit_zero = argparse_args.exit_zero or config.get('exit_zero') or False
    verbosity = argparse_args.v or config.get('v') or 0
    process_dots = argparse_args.process_dots or config.get('process_dots') or False
    reorder_vocabulary = argparse_args.reorder_vocabulary or config.get('reorder_vocabulary') or False

    return {
        'path': argparse_args.path,
        'vocabulary_path': vocabulary_path,
        'exclude': exclude,
        'db_path': db_path,
        'exit_zero': exit_zero,
        'reorder_vocabulary': reorder_vocabulary,
        'process_dots': process_dots,
        'processes_amount': processes_amount,
        'verbosity': verbosity,
    }

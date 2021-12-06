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
    parser.add_argument(
        'path',
        type=str,
        help='Путь до файла, который надо проверить.')
    parser.add_argument(
        '--config', '-c',
        metavar='config_path',
        help='Путь до файла с конфигурациями.')
    parser.add_argument(
        '--vocabulary_path', '-vp',
        help='Путь до файла словаря.')
    parser.add_argument(
        '--exclude', '-e',
        default='',
        help='Список файлов/каталогов, которые следует исключить из проверки.')
    parser.add_argument(
        '--db_path', '-db',
        help='Путь до sqlite базы с кешем. По умолчанию: .rozental.sqlite в корне проекта.')
    parser.add_argument(
        '--exit_zero', '-z',
        action='store_true',
        help='В любом случае завершать процесс без ошибки. Прим.: если вы не хотите ломать билд при наличии опечаток.')
    parser.add_argument(
        '--reorder_vocabulary', '-rv',
        action='store_true',
        help='Отсортировать словарь в алфавитном порядке.')
    parser.add_argument(
        '--process_dots', '-pd',
        action='store_true',
        help='Проверять файлы и директории, название которых начинается с точки. По-умолчанию они пропускаются.')
    parser.add_argument(
        '--processes', '-p',
        type=int, default=None,
        help='Количество процессов, которые будут использоваться для извлечения строк.')
    parser.add_argument(
        '-v', '--verbose',
        action='count', default=0,
        help='Более многословный режим.')
    parser.add_argument(
        '--ban_obscene_words', '-obs',
        action='store_true',
        help='Считать вхождения мата за ошибки.')
    parser.add_argument(
        '--backends', '-b',
        default='vocabulary,yaspeller',
        help='Список бэкендов, которые использовать для проверки, '
             'через запятую, доступные бэкенды: vocabulary, yaspeller, autocorrect.',
    )

    return parser.parse_args()


def prepare_arguments(argparse_args: argparse.Namespace) -> RozentalOptions:
    config_path = get_config_path(argparse_args.path, argparse_args.config)
    config: Mapping[str, Any] = {}
    if config_path:
        config = get_params_from_config(config_path)

    default_processors_amount = multiprocessing.cpu_count() if os.path.isdir(argparse_args.path) else 1
    processes_amount = argparse_args.processes or config.get('processes') or default_processors_amount
    base_path = (
        argparse_args.path
        if os.path.isdir(argparse_args.path)
        else os.path.dirname(os.path.abspath(argparse_args.path))
    ) if os.path.exists(argparse_args.path) else '.'
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
    verbosity = argparse_args.verbose or config.get('verbosity') or 0
    process_dots = argparse_args.process_dots or config.get('process_dots') or False
    reorder_vocabulary = argparse_args.reorder_vocabulary or config.get('reorder_vocabulary') or False
    ban_obscene_words = argparse_args.ban_obscene_words or config.get('ban_obscene_words') or False
    backends = argparse_args.backends.split(',')

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
        'ban_obscene_words': ban_obscene_words,
        'backends': backends,
    }

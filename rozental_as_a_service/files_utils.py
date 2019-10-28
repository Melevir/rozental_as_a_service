import os
from typing import List, Optional
from pathlib import Path

from chardet import detect

from rozental_as_a_service.config import DEFAULT_CONFIG_FILENAME


def is_path_in_exclude_list(path: str, exclude: List[str]) -> bool:
    return any(e in path for e in exclude)


def get_all_filepathes_recursively(path: str, exclude: List[str], extension: str) -> List[str]:
    pathlist = Path(path).glob(f'**/*.{extension}')
    return [
        str(p) for p in pathlist
        if not is_path_in_exclude_list(str(p), exclude)
        and not os.path.isdir(str(p))
    ]


def get_content_from_file(filepath: str, guess_encoding: bool) -> Optional[str]:
    if guess_encoding:
        with open(filepath, 'rb') as file_handler:
            binary_content = file_handler.read()
        encoding = detect(binary_content)['encoding']
        with open(filepath, 'r', encoding=encoding) as file_handler:
            return file_handler.read()
    else:
        try:
            with open(filepath, 'r') as file_handler:
                return file_handler.read()
        except UnicodeDecodeError:
            return None


def get_config_path(base_path: str, config_path: str = None) -> Optional[str]:
    if config_path and os.path.exists(config_path):
        return config_path
    default_config_path = os.path.join(base_path, DEFAULT_CONFIG_FILENAME)
    if os.path.exists(default_config_path):
        return default_config_path

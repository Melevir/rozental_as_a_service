from typing import List
from pathlib import Path


def is_path_in_exclude_list(path: str, exclude: List[str]) -> bool:
    return any(e in path for e in exclude)


def get_all_filepathes_recursively(path: str, exclude: List[str], extension: str) -> List[str]:
    pathlist = Path(path).glob(f'**/*.{extension}')
    return [str(p) for p in pathlist if not is_path_in_exclude_list(str(p), exclude)]

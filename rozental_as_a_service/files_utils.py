from typing import List


def get_all_filepathes_recursively(path: str, extension: str) -> List[str]:
    from pathlib import Path

    pathlist = Path(path).glob(f'**/*.{extension}')
    return [str(p) for p in pathlist]

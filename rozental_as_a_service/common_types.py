from mypy_extensions import TypedDict
from typing import List


class TypoInfo(TypedDict):
    original: str
    possible_options: List[str]


class BackendsConfig(TypedDict):
    vocabulary_path: str
    speller_chunk_size: int
    db_path: str

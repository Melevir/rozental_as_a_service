from mypy_extensions import TypedDict
from typing import List, Optional


class TypoInfo(TypedDict):
    original: str
    possible_options: List[str]


class BackendsConfig(TypedDict):
    speller_chunk_size: int
    vocabulary_path: Optional[str]
    db_path: Optional[str]


class RozentalOptions(TypedDict):
    path: str
    vocabulary_path: str
    exclude: List[str]
    db_path: str
    exit_zero: bool
    process_dots: bool
    processes_amount: int
    verbosity: int

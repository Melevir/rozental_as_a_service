from mypy_extensions import TypedDict
from typing import List, Mapping, Any


class TypoInfo(TypedDict):
    original: str
    possible_options: List[str]


class RozentalOptions(TypedDict):
    path: str
    vocabulary_path: str
    exclude: List[str]
    db_path: str
    exit_zero: bool
    reorder_vocabulary: bool
    process_dots: bool
    processes_amount: int
    verbosity: int
    ban_obscene_words: bool
    backends: List[str]


GoogleDocumentContent = Mapping[str, Any]

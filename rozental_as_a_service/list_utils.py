from typing import List, Generator


def chunks(some_list: List, chunk_size: int) -> Generator:
    for chunk_num in range(0, len(some_list), chunk_size):
        yield some_list[chunk_num:chunk_num + chunk_size]


def flat(some_list: List[List]) -> List:
    return [item for sublist in some_list for item in sublist]

import ast

from typing import List

from rozental_as_a_service.files_utils import get_all_filepathes_recursively


def extract_all_constants_from_ast(ast_tree: ast.AST) -> List[str]:
    return list({n.s for n in ast.walk(ast_tree) if isinstance(n, ast.Str)})


def extract_all_constants_from_path(path: str) -> List[str]:
    string_constants: List[str] = []
    for filepath in get_all_filepathes_recursively(path, 'py'):
        with open(filepath, 'r') as file_handler:
            raw_content = file_handler.read()
        ast_tree = ast.parse(raw_content)
        string_constants += extract_all_constants_from_ast(ast_tree)
    return list(set(string_constants))

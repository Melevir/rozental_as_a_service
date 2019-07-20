import ast

from typing import List


def extract_all_constants_from_ast(ast_tree: ast.AST) -> List[str]:
    return list({n.s for n in ast.walk(ast_tree) if isinstance(n, ast.Str)})

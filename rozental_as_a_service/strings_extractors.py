import ast
import re

from typing import List

from bs4 import BeautifulSoup
from markdown import markdown

from rozental_as_a_service.ast_utils import extract_all_constants_from_ast


def extract_from_python_src(raw_content: str) -> List[str]:
    try:
        ast_tree = ast.parse(raw_content)
    except SyntaxError:
        return []
    return extract_all_constants_from_ast(ast_tree)


def extract_from_html(raw_content: str) -> List[str]:
    return BeautifulSoup(raw_content, 'html.parser').find_all(text=True)


def extract_from_markdown(raw_content: str) -> List[str]:
    html = markdown(raw_content)
    html = re.sub(r'<pre>(.*?)</pre>', ' ', html)
    html = re.sub(r'<code>(.*?)</code>', ' ', html)
    return extract_from_html(html)

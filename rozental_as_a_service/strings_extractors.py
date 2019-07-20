import ast
import re

from typing import List

from bs4 import BeautifulSoup
from markdown import markdown

from rozental_as_a_service.ast_utils import extract_all_constants_from_ast


def extract_from_python_src(raw_content: str) -> List[str]:
    ast_tree = ast.parse(raw_content)
    return extract_all_constants_from_ast(ast_tree)


def extract_from_markdown(raw_content: str) -> List[str]:
    html = markdown(raw_content)
    html = re.sub(r'<pre>(.*?)</pre>', ' ', html)
    html = re.sub(r'<code>(.*?)</code >', ' ', html)
    return BeautifulSoup(html, 'html.parser').find_all(text=True)

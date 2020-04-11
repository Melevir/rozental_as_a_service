import ast
import io
import re

from typing import List
import tokenize

from bs4 import BeautifulSoup
from markdown import markdown
from esprima import tokenize as esprima_tokenize, Error

from rozental_as_a_service.ast_utils import extract_all_constants_from_ast


def extract_from_python_src(raw_content: str) -> List[str]:
    return list(set(
        _extract_from_python_ast(raw_content)
        + _extract_from_python_code_comments(raw_content),
    ))


def extract_from_html(raw_content: str) -> List[str]:
    return [n.strip() for n in BeautifulSoup(raw_content, 'html.parser').find_all(text=True) if n.strip()]


def extract_from_markdown(raw_content: str) -> List[str]:
    html = markdown(raw_content)
    html = re.sub(r'<pre>(.*?)</pre>', ' ', html)
    html = re.sub(r'<code>(.*?)</code>', ' ', html)
    html = re.sub(r'<strong>(.*?)</strong>', r'\1', html)
    html = re.sub(r'\n', ' ', html)
    return extract_from_html(html)


def extract_from_js(raw_content: str) -> List[str]:
    try:
        tokens = esprima_tokenize(raw_content)
    except Error:
        return []
    return list({t.value for t in tokens if t.type == 'String'})


def extract_from_po(raw_content: str) -> List[str]:
    text_regexp = r'(msgid|msgstr) "(.+)"'
    extracted_text: List[str] = []
    for line in raw_content.split('\n'):
        match = re.match(text_regexp, line)
        if match:
            extracted_text.append(match.groups()[1])
    return extracted_text


def _extract_from_python_ast(raw_content: str) -> List[str]:
    try:
        ast_tree = ast.parse(raw_content)
    except SyntaxError:
        return []
    return extract_all_constants_from_ast(ast_tree)


def _extract_from_python_code_comments(raw_content: str) -> List[str]:
    string_constants = []
    for line in tokenize.generate_tokens(io.StringIO(raw_content).readline):
        if line.type == tokenize.COMMENT:
            string_constants.append(line.string)
    return string_constants

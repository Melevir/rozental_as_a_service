import os

import rozental_as_a_service.strings_extractors as extr


def _load_src_file(filename):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    td_dir = os.path.join(cur_dir, 'test_files', 'src_for_strings_extractors')
    with open(os.path.join(td_dir, filename), encoding='utf8') as f:
        return f.read()


def test_extract_from_python_src():
    src = _load_src_file('src_python')
    actual_res = sorted(extr.extract_from_python_src(src))
    assert actual_res == [
        '\n    1\n    2\n    3\n    ',
        '# принт',
        'Show {0}',
        'p1',
        'val',
        'Дока',
        'вал2',
        'коммент',
        'п2',
    ]


def test_extract_from_html_src():
    src = _load_src_file('src_html')
    actual_res = sorted(extr.extract_from_html(src))
    assert actual_res == [
        '\n',
        '\n',
        '\n',
        '\n',
        '\n',
        '\n',
        '\n',
        ' <title>Title</title> ',
        ' Здесь <span>1</span> <br/>2 ',
        'Title',
    ]


def test_extract_from_markdown_src():
    src = _load_src_file('src_markdown')
    actual_res = extr.extract_from_markdown(src)
    assert actual_res == [
        ' <title>Title</title> ',
        ' ',
        'Title',
        ' Здесь <span>1</span> <br/>2 ',
        '              strong 55 77',
    ]


def test_extract_from_js():
    src = _load_src_file('src_js')
    actual_res = sorted(extr.extract_from_js(src))
    assert actual_res == [
        '" secs."',
        '"."',
        '"123"',
        "'getSecs()'",
    ]


def test_extract_from_po():
    src = _load_src_file('src_po')
    actual_res = sorted(extr.extract_from_po(src))
    assert actual_res == ['AD', 'Андорра']

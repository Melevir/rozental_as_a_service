import os

import rozental_as_a_service.strings_extractors as extr


def _load_src_file(filename):
    td_dir = os.path.join(os.getcwd(), 'test_files', 'src_for_strings_extractors')
    with open(os.path.join(td_dir, filename), encoding='utf8') as f:
        return f.read()


def test_extract_from_python_src():
    src = _load_src_file('src_python')
    actual_res = extr.extract_from_python_src(src)
    expected_res = [
        'Show {0}',
        'p1',
        '# принт',
        'коммент',
        'вал2',
        '\n    1\n    2\n    3\n    ',
        'п2',
        'val',
        'Дока',
    ]
    for item in expected_res:
        assert item in actual_res


def test_extract_from_html_src():
    src = _load_src_file('src_html')
    actual_res = extr.extract_from_html(src)
    expected_res = [
        ' <title>Title</title> ',
        'Title',
        ' Здесь <span>1</span> <br/>2 ',
        '\n',
    ]
    for item in expected_res:
        assert item in actual_res


def test_extract_from_markdown_src():
    src = _load_src_file('src_markdown')
    actual_res = extr.extract_from_markdown(src)
    expected_res = [
        ' <title>Title</title> ',
        'Title',
        ' Здесь <span>1</span> <br/>2 ',
        '\n',
        'strong 55 77',
    ]
    for item in expected_res:
        assert item in actual_res


def test_extract_from_js():
    src = _load_src_file('src_js')
    actual_res = extr.extract_from_js(src)
    expected_res = [
        "'getSecs()'",
        '" secs."',
        '"."',
        '"123"',
    ]
    for item in expected_res:
        assert item in actual_res


def test_extract_from_po():
    src = _load_src_file('src_po')
    actual_res = extr.extract_from_markdown(src)
    expected_res = [
        'Translators:',
        '\n',
        'msgid ""\nmsgstr ""',
        '"Project-Id-Version: aimeos-core\\n"\nReport-Msgid-Bugs-To: \\n',
        'msgid "AD"\nmsgstr "Андорра"',
    ]
    for item in expected_res:
        assert item in actual_res

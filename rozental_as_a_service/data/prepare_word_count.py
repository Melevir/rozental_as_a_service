"""
Копипаста autocorrect.word_count

Отличия:
    - захардкожен русский язык
    - в word_regex добавлен дефис, чтобы добавлялись слова вида "кто-то"
    - выкидываются слова с threshold < 10
"""
from typing import Optional
import sys
import json
import re
from collections import Counter, OrderedDict


def get_words(filename: str, encd: str):
    word_regex = r'[АаБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯя-]+'
    capitalized_regex = r'(\.|^|<|"|\'|\(|\[|\{)\s*' + word_regex
    with open(filename, encoding=encd) as file:
        for line in file:
            line = re.sub(capitalized_regex, '', line)
            yield from re.findall(word_regex, line)


def count_words(src_filename: str, encd: Optional[str] = None, out_filename: str = 'word_count.json') -> None:
    words = get_words(src_filename, encd)
    counts = Counter(words)
    # make output file human readable
    counts_list = list(counts.items())
    counts_list.sort(key=lambda i: i[1], reverse=True)
    counts_list = (item for item in counts_list if item[1] > 10)
    counts_ord_dict = OrderedDict(counts_list)
    with open(out_filename, 'w') as outfile:
        json.dump(counts_ord_dict, outfile, indent=4)


if __name__ == '__main__':
    src_filename = sys.argv[1]
    count_words(src_filename)

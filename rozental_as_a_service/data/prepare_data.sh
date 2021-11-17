#! bash
set -ex

wget https://dumps.wikimedia.org/ruwiki/latest/ruwiki-latest-pages-articles.xml.bz2
bzip2 -d ruwiki-latest-pages-articles.xml.bzc2
python rozental_as_a_service/data/prepare_word_count.py ruwiki-latest-pages-articles.xml
tar -zcvf rozental_as_a_service/data/ru.tar.gz word_count.json
mv word_count.json rozental_as_a_service/data/word_count.json

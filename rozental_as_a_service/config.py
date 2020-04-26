import os


DEFAULT_WORDS_CHUNK_SIZE = 30
DEFAULT_VOCABULARY_FILENAME = '.vocabulary'
DEFAULT_SQLITE_DB_FILENAME = '.rozental.sqlite'
DEFAULT_CONFIG_FILENAME = 'setup.cfg'
CONFIG_SECTION_NAME = 'rozental'
GOOGLE_DOC_URL_REGEXP = r'https://docs.google.com/document/d/([a-zA-Z0-9_-]+)/.+'
YA_SPELLER_REQUEST_TIMEOUTS = (.5, .7)  # (connect timeout, read timeout)
YA_SPELLER_RETRIES_COUNT = 5
OBSCENE_BASE_TABLE_NAME = 'obscene_words'
OBSCENE_CORPUS_HTTP_PATH = 'https://raw.githubusercontent.com/odaykhovskaya/obscene_words_ru/master/obscene_corpus.txt'
SENTRY_ENABLED = os.environ.get('ROZENTAL_SENTRY_ENABLED', None) == 'True'
SENTRY_URL = 'https://9315f394f1c74f03a3882a61e8a4a4aa@o383595.ingest.sentry.io/5213839'  # open rozental errors storage

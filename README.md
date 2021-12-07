# Rozental As A Service

[![Build Status](https://travis-ci.org/Melevir/rozental_as_a_service.svg?branch=master)](https://travis-ci.org/Melevir/rozental_as_a_service)
[![Maintainability](https://api.codeclimate.com/v1/badges/716840a3b7d5fa62b273/maintainability)](https://codeclimate.com/github/Melevir/rozental_as_a_service/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/716840a3b7d5fa62b273/test_coverage)](https://codeclimate.com/github/Melevir/rozental_as_a_service/test_coverage)
[![PyPI version](https://badge.fury.io/py/rozental-as-a-service.svg)](https://badge.fury.io/py/rozental-as-a-service)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/rozental-as-a-service)

Библиотека для поиска опечаток в строковых константах в исходном коде.
Скажем нет опечаткам в докстрингах и пользовательских сообщениях.


![Говорите и пишите по-русски правильно](https://raw.githubusercontent.com/Melevir/rozental_as_a_service/master/docs_img/rozental_book.jpg)

**ВНИМАНИЕ**: Это проект находится в стадии "почти никем не используется в бою и
поддерживается очень эпизодически". Используйте на свой страх и риск.

Фамилия Розенталя на английском пишется так: Rosenthal,
но эта библиотека называется `rozental`. Это не безграмотность, это метаирония. :)


## Принцип работы
Розенталь парсит исходный код в указанной директории,
извлекает из него строковые константы, отфильтровывает из них русские слова
и проверяет их правильность с помощью [Яндекс.Спеллера](https://yandex.ru/dev/speller/).
Чтобы не тратить много времени на общение с внешним сервисом, Розенталь
кэширует результат работы Я.Спеллера в локальной sqlite базе данных.

Также Розенталь поддерживает `.vocabulary`-файл: текстовый файл с
перечислением точно верных слов. Это нужно для слов, специфичных для проекта
и для слов, которые Я.Спеллер считает некорректными, хотя с ними всё ок.


## Установка

    pip install rozental_as_a_service

Для этого вам понадобится Python 3.7+.


## Пример

    def start_ad_company(company: Company) -> bool:
        if company.owner.total_budget < company.budget:
            company.owner.send_message('Для содание рекламной компании недостаточно бджета')
            return False
        ...

Использование:

    $ rozental test.py
    Найденное слово    Возможные исправления
    -----------------  ---------------------------
    бджета             бюджета, джетта, буджета
    содание            создание, задание, создания

Аргументы:

- `--vocabulary_path`, `-vp` – путь до файла словаря. По-умолчанию Розенталь ищет файл `.vocabulary` в директории для проверки.
- `--db_path`, `-db` – путь до sqlite-базы данных с кэшем для Розенталя. По-умолчанию создаётся `.rozental.sqlite` в директории для проверки.
- `--exclude`, `-e` – список каталогов, в которых не нужно проверять файлы. Например, `tests/,cache/,lib/,dist/`.
- `--exit_zero`, `-ez` – в любом случае завершать процесс без ошибки. Пригодится, если вы не хотите ломать билд при наличии опечаток (полезно при внедрении).
- `--process_dots`, `-pd` – проверять файлы и директории, название которых начинается с точки. По-умолчанию они пропускаются.
- `--processes`, `-p` – количество процессов, которые будут использоваться для извлечения строк. По-умолчанию используется доступное количество процессоров.
- `--ban_obscene_words`, `-obs` – считать вхождения мата за ошибки.
- `--backends`, `-b` – Список бэкендов, которые использовать для проверки, через запятую, доступные бэкенды: vocabulary, yaspeller, autocorrect..
- `--verbose`, `-v`  – более многословный режим.

Эти же опции можно указать в `.cfg`-файле (секция `rozental`), путь до которого указать с помощью
`--config`, `-c` (по-умолчанию Розенталь ищет `setup.cfg` в пути для проверки).


## Какие файлы умеет смотреть Розенталь

- `.py`, `.pyi`;
- `.po`;
- `.md`;
- `.html`;
- `.js`, `.tsx`.


## Как использовать

1. Разово запустить на существующей кодовой базе и исправить некоторые опечатки.
2. Заполнить `.vocabulary`-файл, исправить все существующие опечатки
 и поставить проверку Розенталя в билд: если кто-то опечатается, билд сломается.


# Contributing

Да, пожалуйста!

Мы соблюдаем [правила поведения Django](https://www.djangoproject.com/conduct/)
и [стайлгайд BestDoctor](https://github.com/best-doctor/guides/blob/master/guides/python_styleguide.md).

Если хотите принять участие в разработке – напишите Илье (https://t.me/melevir),
он всё расскажет. Я пишу о себе в третьем лице, ну отлично.

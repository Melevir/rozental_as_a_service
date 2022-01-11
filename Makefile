test:
	python -m pytest

coverage:
	python -m pytest --cov=rozental_as_a_service --cov-report=xml

types:
	mypy rozental_as_a_service

style:
	flake8 rozental_as_a_service

spelling:
	rozental .

check:
	make style
	make types
	make spelling
	make test

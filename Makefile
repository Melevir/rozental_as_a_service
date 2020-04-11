style:
	flake8 .

check:
	make style
	mypy .
	python -m pytest --cov=rozental_as_a_service --cov-report=xml
	rozental .

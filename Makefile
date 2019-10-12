check:
	flake8 .
	mypy .
	python -m pytest --cov=rozental_as_a_service --cov-report=xml
	rozental .
	pytest .

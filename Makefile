cov:
	pytest --cov-report term-missing --cov-branch --cov=tagfiles tests/

lint:
	black -S -t py37 -l 79 tagfiles tests
	isort -rc .
	flake8

tests:
	pytest tests/
	black -S -t py37 -l 79 --check tagfiles tests
	isort -rc -c .
	flake8

.PHONY: cov lint tests

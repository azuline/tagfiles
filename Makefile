cov:
	pytest --cov-report term-missing --cov-branch --cov=tagfiles tests/

lint:
	yapf --in-place --parallel --recursive .
	isort -rc .
	flake8

tests:
	pytest tests/
	yapf --parallel --diff --recursive .
	isort -rc -c .
	flake8

.PHONY: cov lint tests

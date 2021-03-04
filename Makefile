lint:
	black .
	isort .
	flake8

test:
	pytest --cov-report term-missing --cov-branch --cov=. tests/
	black --check .
	isort -c .
	flake8

.PHONY: lint test

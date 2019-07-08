cov:
	poetry run pytest --cov-report term-missing --cov-branch --cov=tagfiles tests/
lint:
	poetry run yapf --in-place --parallel --recursive .
	poetry run isort -rc .
	poetry run flake8
test:
	poetry run pytest tests/
	poetry run yapf --parallel --diff --recursive .
	poetry run isort -rc -c .
	poetry run flake8

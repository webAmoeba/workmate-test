install:
	uv sync

build:
	uv build

i:
	uv tool install .

uninstall:
	uv tool uninstall workmate-test
	uv clean

re: uninstall i

#_______________________________________________________________________________Test run

# 

#_______________________________________________________________________________Lint

lint:
	uv run ruff check .

fix:
	uv run ruff check --fix

#_______________________________________________________________________________Tests

test:
	uv run pytest

test-vv:
	uv run pytest -vv

check: test lint
# Update version ONLY here
VERSION := 1.11.1
SHELL := /bin/bash
# Makefile for project
VENV := .venv/bin/activate
UNAME_S := $(shell uname -s)

# ----------------------------------------------------------------------------
# Documentation
# ----------------------------------------------------------------------------

build-docs:
	uv run sphinx-build -n -b text docs builddocs
	uv run sphinx-build -n -a -b html docs builddocs
	cd builddocs && zip -r ../builddocs.zip . -x ".*" && cd ..

rebuild-docs:
	uv run sphinx-apidoc . --full -o docs -H 'ska' -A 'Artur Barseghyan <artur.barseghyan@gmail.com>' -f -d 20
	cp docs/conf.py.distrib docs/conf.py
	cp docs/index.rst.distrib docs/index.rst

build-docs-epub:
	$(MAKE) -C docs/ epub

build-docs-pdf:
	$(MAKE) -C docs/ latexpdf

auto-build-docs:
	uv run sphinx-autobuild docs docs/_build/html --port 5001

serve-docs:
	uv run python -m http.server 5001 --directory builddocs/

# ----------------------------------------------------------------------------
# Pre-commit
# ----------------------------------------------------------------------------

pre-commit-install:
	pre-commit install

pre-commit: pre-commit-install
	pre-commit run --all-files

# ----------------------------------------------------------------------------
# Linting
# ----------------------------------------------------------------------------

doc8:
	uv run doc8

ruff:
	uv run ruff check .

mypy:
	uv run mypy src/ska/

# ----------------------------------------------------------------------------
# Installation
# ----------------------------------------------------------------------------

create-venv:
	uv venv

install: create-venv
	uv sync --all-extras
	mkdir -p examples/logs examples/db examples/static examples/tmp examples/media examples/media/foo-images examples/media/static

# ----------------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------------

test: clean
	uv run pytest -vrx -s

test-all: test django-test

django-test:
	source $(VENV) && cd examples/django/ && pytest

test-ci: clean
	uv run pytest -vrx -s

# ----------------------------------------------------------------------------
# Development
# ----------------------------------------------------------------------------

clean:
	find . -type f -name "*.pyc" -exec rm -f {} \;
	find . -type f -name "builddocs.zip" -exec rm -f {} \;
	find . -type f -name "*.py,cover" -exec rm -f {} \;
	find . -type f -name "*.orig" -exec rm -f {} \;
	find . -type f -name "*.coverage" -exec rm -f {} \;
	find . -type f -name "*.db" -exec rm -f {} \;
	find . -type d -name "__pycache__" -exec rm -rf {} \; -prune
	find . -type f -name "*.log.*" -exec rm -rf {} \;
	rm -rf build/
	rm -rf dist/
	rm -rf .cache/
	rm -rf htmlcov/
	rm -rf builddocs/
	rm -rf testdocs/
	rm -rf .coverage
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	rm -rf dist/
	rm -rf src/ska.egg-info/
	rm -rf examples/logs/

shell:
	source $(VENV) && ipython

compile-requirements:
	source $(VENV) && uv pip compile pyproject.toml examples/requirements/common.in --all-extras -o examples/requirements/common.txt
	source $(VENV) && uv pip compile pyproject.toml examples/requirements/debug.in --all-extras -o examples/requirements/debug.txt
	source $(VENV) && uv pip compile pyproject.toml examples/requirements/deployment.in --all-extras -o examples/requirements/deployment.txt
	source $(VENV) && uv pip compile pyproject.toml examples/requirements/dev.in --all-extras -o examples/requirements/dev.txt
	source $(VENV) && uv pip compile pyproject.toml examples/requirements/django_4_2.in --all-extras -o examples/requirements/django_4_2.txt
	source $(VENV) && uv pip compile pyproject.toml examples/requirements/django_5_1.in --all-extras -o examples/requirements/django_5_1.txt
	source $(VENV) && uv pip compile pyproject.toml examples/requirements/django_5_2.in --all-extras -o examples/requirements/django_5_2.txt
	source $(VENV) && uv pip compile pyproject.toml examples/requirements/docs.in --all-extras -o examples/requirements/docs.txt
	source $(VENV) && uv pip compile pyproject.toml examples/requirements/documentation.in --all-extras -o examples/requirements/documentation.txt
	source $(VENV) && uv pip compile pyproject.toml examples/requirements/style_checkers.in --all-extras -o examples/requirements/style_checkers.txt
	source $(VENV) && uv pip compile pyproject.toml examples/requirements/test.in --all-extras -o examples/requirements/test.txt
	source $(VENV) && uv pip compile pyproject.toml examples/requirements/testing.in --all-extras -o examples/requirements/testing.txt

compile-requirements-upgrade:
	source $(VENV) && uv pip compile pyproject.toml examples/requirements/common.in --all-extras -o examples/requirements/common.txt --upgrade
	source $(VENV) && uv pip compile pyproject.toml examples/requirements/debug.in --all-extras -o examples/requirements/debug.txt --upgrade
	source $(VENV) && uv pip compile pyproject.toml examples/requirements/deployment.in --all-extras -o examples/requirements/deployment.txt --upgrade
	source $(VENV) && uv pip compile pyproject.toml examples/requirements/dev.in --all-extras -o examples/requirements/dev.txt --upgrade
	source $(VENV) && uv pip compile pyproject.toml examples/requirements/django_4_2.in --all-extras -o examples/requirements/django_4_2.txt --upgrade
	source $(VENV) && uv pip compile pyproject.toml examples/requirements/django_5_1.in --all-extras -o examples/requirements/django_5_1.txt --upgrade
	source $(VENV) && uv pip compile pyproject.toml examples/requirements/django_5_2.in --all-extras -o examples/requirements/django_5_2.txt --upgrade
	source $(VENV) && uv pip compile pyproject.toml examples/requirements/docs.in --all-extras -o examples/requirements/docs.txt --upgrade
	source $(VENV) && uv pip compile pyproject.toml examples/requirements/documentation.in --all-extras -o examples/requirements/documentation.txt --upgrade
	source $(VENV) && uv pip compile pyproject.toml examples/requirements/style_checkers.in --all-extras -o examples/requirements/style_checkers.txt --upgrade
	source $(VENV) && uv pip compile pyproject.toml examples/requirements/test.in --all-extras -o examples/requirements/test.txt --upgrade
	source $(VENV) && uv pip compile pyproject.toml examples/requirements/testing.in --all-extras -o examples/requirements/testing.txt --upgrade

update-version:
	@echo "Updating version in pyproject.toml and src/ska/__init__.py"
	@if [ "$(UNAME_S)" = "Darwin" ]; then \
		gsed -i 's/version = "[0-9.]\+"/version = "$(VERSION)"/' pyproject.toml; \
		gsed -i 's/__version__ = "[0-9.]\+"/__version__ = "$(VERSION)"/' src/ska/__init__.py; \
	else \
		sed -i 's/version = "[0-9.]\+"/version = "$(VERSION)"/' pyproject.toml; \
		sed -i 's/__version__ = "[0-9.]\+"/__version__ = "$(VERSION)"/' src/ska/__init__.py; \
	fi

make-pypi-long-description:
	uv run python setup.py --long-description | rst2html.py > builddocs/pypi.html
	uv run python setup.py --long-description | rst2html.py | cat

# ----------------------------------------------------------------------------
# Django
# ----------------------------------------------------------------------------

django-shell:
	uv run python examples/simple/manage.py shell

django-make-messages:
	source $(VENV) && cd src/ska/contrib/django/ska/ \
		&& django-admin.py makemessages -l hy \
		django-admin.py makemessages -l nl \
		django-admin.py makemessages -l ru

django-runserver:
	uv run python examples/simple/manage.py runserver 0.0.0.0:8000 --traceback -v 3

django-make-migrations:
	uv run python examples/simple/manage.py makemigrations

django-apply-migrations:
	uv run python examples/simple/manage.py migrate

# ----------------------------------------------------------------------------
# Security
# ----------------------------------------------------------------------------

create-secrets:
	uv run detect-secrets scan > .secrets.baseline

detect-secrets:
	uv run detect-secrets scan --baseline .secrets.baseline

# ----------------------------------------------------------------------------
# Release
# ----------------------------------------------------------------------------

build:
	uv run python -m build .

check-build:
	uv run twine check dist/*

check-manifest:
	uv run check-manifest

release:
	uv run twine upload dist/* --verbose

test-release:
	uv run twine upload --repository testpypi dist/*

# ----------------------------------------------------------------------------
# Docker
# ----------------------------------------------------------------------------

docker-build:
	docker compose build

# List all available environments in the Docker container
docker-list-envs: docker-build
	docker compose run --rm tox -l

docker-test: docker-build
	docker compose run --rm tox

# Usage: make docker-test-env ENV=py312-django52
docker-test-env: docker-build
	@if [ -z "$(ENV)" ]; then \
		echo "Usage: make docker-test-env ENV=py312-django52"; \
		exit 1; \
	fi
	docker compose run --rm tox -e $(ENV)

docker-shell: docker-build
	docker compose run --rm --entrypoint bash tox

# Usage: make shell-env ENV=py312
docker-shell-env: build
	@if [ -z "$(ENV)" ]; then \
		echo "Usage: make docker-shell-env ENV=py312"; \
		exit 1; \
	fi
	docker compose run --rm --entrypoint bash tox -e $(ENV)

# ----------------------------------------------------------------------------
# Other
# ----------------------------------------------------------------------------

%:
	@:

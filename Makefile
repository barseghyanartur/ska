# Update version ONLY here
VERSION := 1.11
SHELL := /bin/bash
# Makefile for project
VENV := ~/.virtualenvs/ska/bin/activate
UNAME_S := $(shell uname -s)

# Build documentation using Sphinx and zip it
build_docs:
	source $(VENV) && sphinx-build -n -b text docs builddocs
	source $(VENV) && sphinx-build -n -a -b html docs builddocs
	cd builddocs && zip -r ../builddocs.zip . -x ".*" && cd ..

rebuild_docs:
	source $(VENV) && sphinx-apidoc . --full -o docs -H 'ska' -A 'Artur Barseghyan <artur.barseghyan@gmail.com>' -f -d 20
	cp docs/conf.py.distrib docs/conf.py
	cp docs/index.rst.distrib docs/index.rst

build_docs_epub:
	$(MAKE) -C docs/ epub

build_docs_pdf:
	$(MAKE) -C docs/ latexpdf

auto_build_docs:
	source $(VENV) && sphinx-autobuild docs docs/_build/html

pre-commit:
	pre-commit run --all-files

doc8:
	source $(VENV) && doc8

# Run ruff on the codebase
ruff:
	source $(VENV) && ruff check .

# Serve the built docs on port 5001
serve_docs:
	source $(VENV) && cd builddocs && python -m http.server 5001

# Install the project
install:
	source $(VENV) && pip install -e .[all]
	mkdir -p examples/logs examples/db examples/static examples/tmp examples/media examples/media/foo-images examples/media/static

test: clean
	source $(VENV) && pytest -vrx -s

test-all: test \
django-test

django-test:
	source $(VENV) && cd examples/django/ && pytest

shell:
	source $(VENV) && ipython

django-shell:
	source $(VENV) && python examples/simple/manage.py shell

django-make-messages:
	source $(VENV) && cd src/ska/contrib/django/ska/ \
		&& django-admin.py makemessages -l hy \
		django-admin.py makemessages -l nl \
		django-admin.py makemessages -l ru

django-runserver:
	source $(VENV) && python examples/simple/manage.py runserver 0.0.0.0:8000 --traceback -v 3

django-make-migrations:
	source $(VENV) && python examples/simple/manage.py makemigrations

django-apply-migrations:
	source $(VENV) && python examples/simple/manage.py migrate

create-secrets:
	source $(VENV) && detect-secrets scan > .secrets.baseline

detect-secrets:
	source $(VENV) && detect-secrets scan --baseline .secrets.baseline

# Clean up generated files
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

compile-requirements:
	source $(VENV) && uv pip compile --all-extras -o docs/requirements.txt pyproject.toml

compile-requirements-upgrade:
	source $(VENV) && uv pip compile --all-extras -o docs/requirements.txt pyproject.toml --upgrade

update-version:
	@echo "Updating version in pyproject.toml and src/ska/__init__.py"
	@if [ "$(UNAME_S)" = "Darwin" ]; then \
		gsed -i 's/version = "[0-9.]\+"/version = "$(VERSION)"/' pyproject.toml; \
		gsed -i 's/__version__ = "[0-9.]\+"/__version__ = "$(VERSION)"/' src/ska/__init__.py; \
	else \
		sed -i 's/version = "[0-9.]\+"/version = "$(VERSION)"/' pyproject.toml; \
		sed -i 's/__version__ = "[0-9.]\+"/__version__ = "$(VERSION)"/' src/ska/__init__.py; \
	fi

build:
	source $(VENV) && python -m build .

check-build:
	source $(VENV) && twine check dist/*

check-manifest:
	source $(VENV) && check-manifest

release:
	source $(VENV) && twine upload dist/* --verbose

test-release:
	source $(VENV) && twine upload --repository testpypi dist/*

mypy:
	source $(VENV) && mypy src/ska/

%:
	@:

---
name: dev-setup
description: Environment setup, dependency installation, and recovery steps.
---

# dev-setup

## Environment creation

### Primary method (uv)

```sh
make install
```

This creates a virtual environment (`.venv`) and installs all dependencies via `uv sync --all-extras`. Directories needed by tests are also created.

### Manual method

```sh
uv venv
uv sync --all-extras
mkdir -p examples/logs examples/db examples/static examples/tmp examples/media examples/media/foo-images examples/media/static
```

### Docker method (recommended for test isolation)

```sh
make docker-build
make docker-shell
```

Or for a specific environment:

```sh
make docker-shell-env ENV=py312-django52
```

## Dependency installation

### Core + all extras

```sh
make install
```

### Specific tool groups (from pyproject.toml)

| Group | Contents |
|---|---|
| `dev` | detect-secrets, doc8, ipython, mypy, pydoclint, ruff, uv |
| `test` | fake.py, pytest, pytest-codeblock, pytest-django, mock, beautifulsoup4, soupsieve, coverage |
| `docs` | sphinx, sphinx-autobuild, sphinx-rtd-theme, sphinx-no-pragma, sphinx-llms-txt-link, sphinx-source-tree |
| `django` | django-nine>=0.2.4 |

Install a specific extra:

```sh
uv sync --extra dev --extra test
```

## Common environment failures

### Missing directories (test errors about missing paths)

```sh
mkdir -p examples/logs examples/db examples/static examples/tmp examples/media examples/media/foo-images examples/media/static
```

### Stale compiled artifacts

```sh
make clean
make install
```

### Tox environment not found

```sh
docker compose run --rm tox -l
```

### Dependency resolution issues

```sh
uv sync --refresh
```

### Pre-commit hooks not installed

```sh
pre-commit install
```

## Verified working tool versions

All dependencies are pinned via `uv.lock`. The lock file is the authoritative source of installed versions.

## What this skill does NOT cover

- Coding rules (see `coding-standards`)
- Lint/test loops (see `dev-workflow`)
- PR review logic (see `pr-review`)

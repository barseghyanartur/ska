# AGENTS.md — ska

## Project overview

**ska** is a Python package for signing and validating data (dictionaries, strings, URLs) using symmetric-key algorithm encryption (HMAC with SHA-1, SHA-224, SHA-256, SHA-384, SHA-512). It provides password-less authentication for Django applications and URL signing for query string authentication.

**Repository**: <https://github.com/barseghyanartur/ska>
**Maintainer**: Artur Barseghyan <artur.barseghyan@gmail.com>
**License**: GPL-2.0-only OR LGPL-2.1-or-later

## Architecture invariants

- **Zero external dependencies for core module** — `src/ska/__init__.py`, signatures, shortcuts, and utilities must use only the Python standard library.
- **Django integration is optional** — lives in `ska.contrib.django` and may have third-party dependencies.
- **All signatures use HMAC-SHA1 or stronger** — MD5 is supported only for legacy compatibility.
- **Python 3.10+ required** for core; Django integration requires Django 4.2+.

## Repository layout (authoritative)

```text
src/ska/               — Package source (root of setuptools package-dir)
  __init__.py           — Public API exports
  base.py               — Abstract base classes
  signatures/           — HMAC signature implementations
  shortcuts.py          — Convenience functions
  utils.py              — RequestHelper and utilities
  defaults.py           — Default configuration values
  exceptions.py         — Exception classes
  error_codes.py        — Error code constants
  contrib/django/        — Django integration (optional)
  tests/                — Core package tests
src/ska.egg-info/       — Setuptools metadata (generated)
examples/              — Example applications and requirements
docs/                  — Sphinx documentation
tests/                 — Django integration tests (at project root)
conftest.py            — Shared pytest fixtures
pyproject.toml         — Project configuration (build-system, tools, deps)
Makefile               — Task runner (install, test, lint, docs, release)
tox.ini                — Test environments (py310-313 × django42/51/52)
docker-compose.yml     — Docker-based test environment
```

## Hard constraints

- **Never target `main` branch directly** — all PRs target `dev`.
- **Do not add external dependencies to the core package** — zero-deps invariant must hold.
- **Do not weaken default security** — e.g., do not use MD5 as the default algorithm.
- **Do not expose secret keys in logs or error messages.**
- **All tests must pass in Docker** before merge — `make docker-test` is the source of truth.
- **PRs must include tests** for any new behavior.

## Known intentional behaviors — do not change

1. Default signature lifetime is 10 minutes (600 seconds). Defined in `ska.defaults.SIGNATURE_LIFETIME`.
2. Default URL suffix is `?`. Defined in `ska.defaults.DEFAULT_URL_SUFFIX`.
3. Default param names (`signature`, `auth_user`, `valid_until`) are defined in `ska.defaults`.
4. Multiple secret keys (providers) are supported in Django integration via `SKA_PROVIDERS` setting.
5. Django authentication backends fall back to default callbacks when provider-specific callbacks are not defined.
6. Generated signatures are inter-compatible between Python, NodeJS (skajs), and PHP (skaphp) implementations.
7. The `ska-sign-url` CLI command is exported via `ska.generate_signed_url:main`.

## Configuration authority

- **pyproject.toml** — Python package metadata, tool configs (ruff, black, isort, mypy, pytest, coverage), dependency groups.
- **Makefile** — Task runner (install, test, lint, build, release, docker).
- **tox.ini** — Test matrix specification (Python 3.10–3.13 × Django 4.2/5.1/5.2).
- **docker-compose.yml** — Docker-based test environment.
- **.github/workflows/test.yml** — CI pipeline (runs tox on push/PR).
- **conftest.py** — pytest fixtures shared across all test paths.
- **ska/defaults.py** — Default values for signature parameters.
- **ska/contrib/django/ska/settings.py** (Django integration) — Django-specific settings (SKA_SECRET_KEY, SKA_PROVIDERS, etc.).

## Agent obligations

1. **Before implementing any change**, verify it does not violate the hard constraints (zero deps, no main-branch PRs, no security weakening).
2. **When fixing a bug**, write a regression test that reproduces the bug before implementing the fix.
3. **When adding a feature**, identify the correct module (core signatures → `signatures/`, shortcuts → `shortcuts.py`, Django integration → `contrib/django/`), implement, add tests, and update `README.rst` if the public API changes.
4. **When updating documentation**, ensure code examples match the actual API (see `.agents/skills/update-documentation/SKILL.md`).
5. **Before opening a PR**, run `make docker-test` to verify all tests pass in the containerized environment.
6. **Linting**: run `make ruff` and `make mypy` locally; CI catches failures.
7. **Definition of Done**: lint → fix → test, with retries and explicit stop conditions (see `.agents/skills/dev-workflow/SKILL.md`).

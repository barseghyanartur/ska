---
name: pr-review
description: Deterministic pull-request review behavior and checklist.
---

# pr-review

## Scope

This skill defines the review checklist for any pull request opened against `ska`. It applies to all contributors, including AI agents.

## Pre-review prerequisites

Before starting the checklist, verify:
- The PR targets the `dev` branch (never `main`)
- CI is green (all tox environments passed on the PR branch)

If either is missing, stop and report the issue immediately.

## Review checklist

### 1. Hard constraints — must pass

- [ ] **Zero new external dependencies in core** — Check `pyproject.toml` and `requirements` for any new imports not in stdlib.
- [ ] **No weakening of security defaults** — No introduction of MD5 as default, no reduction of HMAC key requirements.
- [ ] **No secret key exposure** — Search for `secret_key`, `SKA_SECRET_KEY` in any new `logging` call, `raise` message, or string formatting.
- [ ] **Test coverage exists for new behavior** — New functions/classes must have corresponding tests in `src/ska/tests/` or `tests/`.
- [ ] **No modification of conftest.py** — Fixtures are fixed; test logic must adapt to existing fixtures.

### 2. Correctness

- [ ] New public API functions have type annotations on all parameters and return type.
- [ ] New public API functions are exported from `__init__.py` and listed in `__all__`.
- [ ] Exception handling chains exceptions with `from ...` syntax.
- [ ] No `eval()` or `exec()` with user-supplied input.
- [ ] Django integration changes include migrations if database schema changed.

### 3. Code quality

- [ ] `make ruff` passes with no errors.
- [ ] `make mypy` passes with no errors.
- [ ] Line length does not exceed 80 characters (verified by ruff).
- [ ] Imports are sorted per `isort` / `black` profile.

### 4. Documentation

- [ ] If public API changed, `README.rst` is updated with correct examples.
- [ ] If new feature added, relevant docs page in `docs/` is updated.
- [ ] No placeholder or pseudo-code examples in documentation.
- [ ] Codeblock tests in `.rst` files pass (run `pytest --rootdir=. --ignore=src --ignore=examples *.rst`).

### 5. Configuration and release

- [ ] If version was changed, `make update-version VERSION=x.y.z` was used (not manual edit).
- [ ] `AGENTS.md` is updated if architecture invariants changed.
- [ ] No generated artifacts committed (`build/`, `dist/`, `htmlcov/`, `.egg-info/`).

### 6. Tests

- [ ] `make docker-test` passes (full suite in Docker container).
- [ ] No tests skipped via `pytest.skip` or `-k` filtering in the final run.
- [ ] Coverage regression: if coverage dropped, new tests are required before merge.

## Reporting

After completing the checklist, report:

1. **Summary**: one paragraph describing what the PR does.
2. **Status**: `approved` or `changes requested`.
3. **Blocking issues**: list each failing item from the checklist with file:line reference.
4. **Non-blocking suggestions**: list optional improvements (style nits, minor refactors).

## What this skill does NOT cover

- Implementation guidance (that is the developer's responsibility)
- Development workflow details (see `dev-workflow`)
- Environment setup (see `dev-setup`)

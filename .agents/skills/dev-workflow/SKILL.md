---
name: dev-workflow
description: Definition of Done, lint → fix → test sequence, retries, stop conditions.
---

# dev-workflow

## Definition of Done

A change is complete when:

1. All linting passes (`make pre-commit`)
2. All tests pass (`make docker-test`)
3. No new warnings introduced (ruff, mypy)
4. New behavior has test coverage
5. Documentation is updated if public API changed
6. `AGENTS.md` is updated if architecture invariants are affected

## Mandatory sequence

```text
lint → fix → test
```

Repeat until both lint and tests pass, or a stop condition is reached.

### Step 1 — Lint

Run both linters:

```sh
make ruff
make mypy
```

Collect all lint errors before proceeding to fix.

### Step 2 — Fix

Fix all lint errors reported by `ruff` and `mypy`. Apply fixes in this order:
1. Ruff auto-fixes (import sorting, formatting)
2. Manual fixes for remaining ruff errors
3. Type annotation fixes for mypy errors

### Step 3 — Test

Run the full test suite:

```sh
make docker-test
```

Or for a specific environment:

```sh
make docker-test-env ENV=py312-django52
```

### Step 4 — Repeat

If either lint or tests fail after fixes, return to Step 1.

## Retry logic

Maximum 3 cycles of `lint → fix → test`.

If after 3 cycles lint passes but tests still fail, stop and report:
- Which test(s) failed
- Last error message
- The failing test file(s) and line number(s)

## Stop conditions

Stop immediately and report if any of these occur:

1. **Test data directory missing** — Tests reference `examples/` subdirectories that must exist. Create them with `mkdir -p examples/logs examples/db examples/static examples/tmp examples/media examples/media/foo-images examples/media/static`.
2. **Import errors** — The package fails to import. Do not continue; fix the import error first.
3. **Security invariant violation** — Code introduces a new external dependency in core, weakens HMAC defaults, or exposes a secret key. Reject immediately.
4. **Django migration required but not provided** — If a Django integration change requires a database migration, the PR must include it.
5. **Coverage regression** — New code reduces overall coverage below the current threshold.

## Forbidden actions

- **Do not skip tests** — `pytest -k` to select specific tests is permitted only for fast iteration; the final run must be full suite.
- **Do not use `--no-cov`** to hide coverage regressions.
- **Do not modify conftest.py to make tests pass** — fixtures are fixed; tests must be fixed instead.
- **Do not push to `main`** — all PRs target `dev`.
- **Do not commit generated artifacts** — `build/`, `dist/`, `htmlcov/`, `.egg-info/` are generated and must not be committed.
- **Do not change version manually** — use `make update-version VERSION=x.y.z`; never manually edit `pyproject.toml` version or `src/ska/__init__.__version__`.

## What this skill does NOT cover

- Environment setup (see `dev-setup`)
- Code style rules (see `coding-standards`)
- PR review checklist (see `pr-review`)

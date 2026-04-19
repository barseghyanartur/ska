---
name: coding-standards
description: Style rules, typing rules, naming conventions, logging, error-handling philosophy.
---

# coding-standards

## Formatting and style

- **Line length**: 80 characters (enforced by `ruff` and `black` in pyproject.toml).
- **Target Python version**: 3.9 minimum. Type annotations must be compatible.
- **Import sorting**: `isort` with `profile = "black"`. `ska` is a known first-party module. Run `make ruff` to check.
- **Auto-formatting**: `ruff` auto-fixes formatting and import sorting. Do not manually reformat what ruff fixes.

## Module header

Every non-test Python module must have:

```python
__all__ = [...]       # Exported public symbols
__author__ = "..."
__copyright__ = "..."
__license__ = "GPL-2.0-only OR LGPL-2.1-or-later"
```

## Naming conventions

- **Classes**: `CamelCase` (e.g., `HMACSHA256Signature`)
- **Functions and variables**: `snake_case` (e.g., `sign_url`, `valid_until`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `DEFAULT_SIGNATURE_PARAM`)
- **Private module-level names**: `_prefixed` (single underscore prefix; do not use `__dunder__` unless required)
- **Test functions**: `test_<subject>_<scenario>` (e.g., `test_signature_generate_signature_part_2`)
- **Test files**: `test_<module>.py` (e.g., `test_signatures.py`)

## Type annotations

- All public functions **must** have type annotations on parameters and return value.
- Use `typing` module for complex types (Optional, Union, etc.).
- Generic types: prefer `list[str]` over `List[str]`, `dict[str, int]` over `Dict[str, int]`.
- Do not use `Any` unless unavoidable; document why it is needed.

## Exception handling

- **Always chain exceptions**: `raise NewException(...) from original_exception`.
- **Do not catch Exception** unless absolutely necessary; catch specific subclasses.
- **Do not expose secret keys in exception messages or logs**.
- All custom exceptions inherit from `Exception`.

## Logging conventions

- Use standard library `logging` module.
- Logger name: `__name__` module path.
- Do not use f-strings in log messages; use `%s`-style formatting.
- Do not log secret keys, auth tokens, or signature data.
- Allowed log levels: DEBUG (parameter names/values at entry), INFO (major events), WARNING (recoverable issues), ERROR (failures).

## Allowed / prohibited

### Allowed

- Adding new HMAC variants (e.g., HMAC-SHA3) as new signature classes
- New Django authentication backends
- Integration with other frameworks (Flask, FastAPI) as optional modules
- CLI tools for signing/validating

### Prohibited

- Adding external dependencies to the core `ska` package
- Weakening default security (MD5 as default, lower HMAC key length, etc.)
- Exposing secret keys in logs or error messages
- Using `eval()` or `exec()` with user-supplied input
- Hardcoding credentials or tokens

## How rules are enforced

| Tool | Rule set | Config location |
| --- | --- | --- |
| ruff | B, C4, E, F, G, I, ISC, INP, N, PERF, Q, SIM | pyproject.toml `[tool.ruff]` |
| mypy | strict (check_untyped_defs, warn_unused_ignores, etc.) | pyproject.toml `[tool.mypy]` |
| black | line-length 80, target py39 | pyproject.toml `[tool.black]` |
| isort | profile=black | pyproject.toml `[tool.isort]` |

## What this skill does NOT cover

- Commands to run tools (use `make ruff`, `make mypy`, `make docker-test`)
- Procedural workflows (use `dev-workflow`)
- PR review logic (use `pr-review`)

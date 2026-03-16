# AGENTS.md — ska

**Package version**: See pyproject.toml
**Repository**: https://github.com/barseghyanartur/ska
**Maintainer**: Artur Barseghyan <artur.barseghyan@gmail.com>

This file is for AI agents and developers using AI assistants to work on or with
ska. It covers two distinct roles: **using** the package in application code,
and **developing/extending** the package itself.

---

## 1. Project Mission (Never Deviate)

> Sign and validate data (dictionaries, strings, URLs) using symmetric-key
> algorithm encryption (HMAC with SHA-1, SHA-224, SHA-256, SHA-384, SHA-512).
> Useful for password-less authentication in Django applications.

- Secure by default - all signatures use HMAC-SHA1 or stronger.
- Zero external dependencies (stdlib only for core).
- Support for custom hash algorithms.
- Django integration for password-less login.
- URL signing for query string authentication.

---

## 2. Using ska in Application Code

### Signing a dictionary

```python
from ska import sign_url, validate_signed_request_data, extract_signed_request_data

# Sign a dictionary
secret_key = "my-secret-key"
data = {"user_id": 123, "role": "admin"}
signed_data = sign_url(data, secret_key=secret_key)
# Returns: {"user_id": 123, "role": "admin", "signature": "...", "valid_until": "..."}

# Validate signed data
is_valid, data, errors = validate_signed_request_data(signed_data, secret_key)
```

### Signing a URL

```python
from ska import sign_url

secret_key = "my-secret-key"
url = "https://example.com/api/resource"
signed_url = sign_url(url, secret_key=secret_key)
# Returns: "https://example.com/api/resource?signature=...&valid_until=..."
```

### Django password-less login

```python
# In settings.py
INSTALLED_APPS = [
    # ...
    'ska.contrib.django.ska',
]

# In URLs
from ska.contrib.django.ska.urls import urlpatterns as ska_urls
urlpatterns = [
    # ...
    path('ska/', include(ska_urls)),
]

# Login with ska token
# POST to /ska/login/?next=/dashboard/ with ska token in headers or params
```

### Exception handling

All ska exceptions inherit from `Exception`:

```python
from ska import validate_signed_request_data
from ska.signatures import SignatureError

try:
    is_valid, data, errors = validate_signed_request_data(signed_data, secret_key)
    if not is_valid:
        print(f"Validation errors: {errors}")
except SignatureError as e:
    print(f"Signature error: {e}")
```

---

## 3. Architecture

### Core modules

| File | Purpose |
| --- | --- |
| `src/ska/__init__.py` | Public API exports |
| `src/ska/base.py` | Abstract base classes (`AbstractSignature`, `SignatureValidationResult`) |
| `src/ska/signatures.py` | HMAC signature implementations (SHA1, SHA224, SHA256, SHA384, SHA512) |
| `src/ska/shortcuts.py` | Convenience functions (`sign_url`, `validate_signed_request_data`, etc.) |
| `src/ska/utils.py` | Utility classes (`RequestHelper`) |
| `src/ska/defaults.py` | Default configuration values |
| `src/ska/contrib/django/` | Django integration |

### Django integration

| File | Purpose |
| --- | --- |
| `src/ska/contrib/django/ska/views.py` | Login views |
| `src/ska/contrib/django/ska/views/constance_views.py` | Constance-based login views |
| `src/ska/contrib/django/ska/backends.py` | Authentication backends |
| `src/ska/contrib/django/ska/middleware.py` | Request signing middleware |

---

## 4. Security Principles

**1. Use strong hash algorithms.**
Default to HMAC-SHA256 or stronger. MD5 and SHA1 are supported for legacy compatibility but should not be used for new implementations.

**2. Keep secrets safe.**
Never log or expose secret keys. Store them securely (e.g., environment variables, Django settings).

**3. Validate signatures before processing.**
Always validate signed data before performing any action based on it.

**4. Set appropriate validity windows.**
Use `valid_until` to limit the time window for signature validity.

---

## 5. Agent Workflow: Adding Features or Fixing Bugs

When asked to add a feature or fix a bug, follow these steps in order:

1. **Check the mission** — Does the change preserve zero deps for core, secure defaults?
2. **Identify the correct module** — Is it core signatures, shortcuts, or Django integration?
3. **For bug fixes: write the regression fixture first** — Add a test that reproduces the bug.
4. **Implement the change** in the correct module.
5. **Add/update exceptions** if needed.
6. **Export** new public symbols from `__init__.py` and `__all__`.
7. **Write tests** in `src/ska/tests/`.
8. **Update `README.rst`** if the API changed.

### Acceptable new features

- Additional hash algorithm support (if secure).
- New Django authentication backends.
- Integration with other frameworks (Flask, FastAPI).
- CLI tools for signing/validating.

### Forbidden

- Adding external dependencies to the core package.
- Weakening default security (e.g., using MD5 by default).
- Exposing secret keys in logs or error messages.

---

## 6. Testing Rules

### All tests must run inside Docker

```sh
make docker-test                            # full test suite
make docker-test-env ENV=py312-django52     # single Python version test suite
make docker-shell                           # interactive shell
make docker-shell-env ENV=py312-django52    # single Python version shell
```

Do not run `pytest` directly on the host machine unless you understand the security implications.

### Test layout

```
src/ska/tests/
    conftest.py          — shared fixtures
    test_signatures.py   — signature implementations
    test_shortcuts.py    — shortcut functions
    test_utils.py        — utility functions
    test_django/         — Django integration tests
    tests/               — additional Django tests (if any)
```

### Running tests locally (not recommended for security tests)

```sh
make test              # core tests
make test-all          # core + Django tests
```

### Required assertions for validation tests

```python
# Test that valid signature passes
is_valid, data, errors = validate_signed_request_data(signed_data, secret_key)
assert is_valid is True
assert data["user_id"] == 123

# Test that tampered data fails
tampered_data = signed_data.copy()
tampered_data["user_id"] = 999
is_valid, data, errors = validate_signed_request_data(tampered_data, secret_key)
assert is_valid is False
assert "signature" in str(errors).lower()
```

---

## 7. Coding Conventions

### Formatting

- Line length: **88 characters** (ruff).
- Import sorting: `isort`; `ska` is `known-first-party`.
- Target: `py39`. Run `make ruff` to check.

### Ruff rules in effect

`B`, `C4`, `E`, `F`, `G`, `I`, `ISC`, `INP`, `N`, `PERF`, `Q`, `SIM`.

Explicitly ignored rules should be documented in `pyproject.toml`.

### Style

- Every non-test module must have `__all__`, `__author__`, `__copyright__`, `__license__` at module level.
- Always chain exceptions: `raise X(...) from exc`.
- Type annotations on all public functions.

### Pull requests

Target the `dev` branch only. Never open a PR directly to `main`.

---

## 8. Makefile Targets

Run `make` to see all available targets. Key targets:

| Target | Description |
| --- | --- |
| `make install` | Install dependencies |
| `make docker-test` | Run all tests in Docker |
| `make docker-test-env ENV=py312-django52` | Test spec Python/Django version |
| `make docker-shell` | Interactive shell in Docker |
| `make ruff` | Run ruff linter |
| `make mypy` | Run mypy type checker |
| `make build` | Build package for release |

---

## 9. Prompt Templates

**Explaining usage to a user:**
> You are an expert in Python cryptography. Explain how to use ska for signing
> HTTP requests. Include URL signing, dictionary signing, and Django integration.
> Emphasize secure defaults and proper validation.

**Implementing a new feature:**
> Extend ska with [feature]. Follow the AGENTS.md agent workflow: identify
> the correct module, implement, add tests, update README. Preserve zero
> external dependencies for core and secure defaults.

**Fixing a bug:**
> Reproduce [bug] with a new test. The test must fail before the fix. Then
> fix in the correct module. Add tests asserting correct behavior and that
> legitimate inputs still work.

**Reviewing a change:**
> Review this ska change against AGENTS.md: Does it preserve zero deps?
> Does it maintain secure defaults? Are new features tested?

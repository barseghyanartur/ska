---
name: update-documentation
description: Documentation policy, precision scope, agent-based sync process, and validation.
---

# update-documentation

## 1. Operation mode

- **Pure agent-based synchronization** — No scripts are used. Agents read code, identify misalignments, and edit documentation directly.
- **Docs are updated to match code** — Code is never changed to match documentation.

## 2. Ground truth and authority hierarchy

1. **Code is ground truth** — for API, CLI, defaults, exceptions, configuration behavior.
2. **AGENTS.md and SKILL.md are policy** — must match reality; when they diverge from code, treat code as correct and fix the policy files.
3. **README.rst and docs/ are derived** — must match code and policy; when they diverge, update them to match.
4. **Explicit exclusions**: Auto-generated or vendored documentation (e.g., `docs/_build/`, `docs/.doctrees/`, Sphinx-apidoc output) is not modified by this skill.

## 3. Agent-based sync process

### Step 1 — Extract ground truth from code

Extract from the source:
- Public API surface: `__all__` and exported names in `__init__.py`
- Function signatures (parameters, types, defaults)
- CLI commands and arguments (from `generate_signed_url.py`)
- Default values (from `defaults.py`)
- Exception classes and error codes
- Environment variables and Django settings
- Public constants

### Step 2 — Scan documentation files

Scan these files for correctness and completeness:

| File | Purpose | When to update |
| --- | --- | --- |
| `README.rst` | User-facing usage docs, examples | API changes, new features |
| `AGENTS.md` | Architecture invariants, agent obligations | Architecture changes |
| `.agents/skills/*/SKILL.md` | Agent procedures and policies | Policy changes |
| `CONTRIBUTING.rst` | Contributor guidelines | Process changes |
| `SECURITY.md` / `SECURITY.rst` | Security contact/process | Only if contact info changes |
| `docs/` | Sphinx reference docs | API additions, removed features |

### Step 3 — Identify misalignments

Check for:
- Missing items: a function exists in code but is not documented
- Outdated references: documentation mentions a default or param that differs from code
- Broken paths: file paths referenced in docs no longer exist
- Stale examples: code in `.rst` code blocks differs from actual API behavior
- Wrong signatures: parameter names, types, or defaults in docs differ from code
- Missing examples: new public API has no usage example

### Step 4 — Auto-fix documentation safely

Fix only:

- **Tables**: add missing rows, update column values to match code
- **Examples**: fix parameter names, return values, import statements to match actual code
- **References**: fix file paths, function names, variable names
- **Sections**: add missing sections when a new feature is documented in code but not in docs
- **Defaults**: correct `valid_until`, `lifetime`, param names to match `ska/defaults.py`

Do **not** fix by changing code to match docs. Do **not** invent behavior. If documentation describes behavior that does not exist in code, remove or mark the documentation as stale rather than implementing the described behavior.

### Step 5 — Report changes

Report:
- Files changed (absolute paths)
- What changed in each file (specific line ranges or sections)
- What could not be fixed and why (e.g., feature described in docs has no code implementation)
- Any policy files (AGENTS.md, SKILL.md) that were updated

## 4. Documentation files overview and targeting rules

### README.rst

- **Audience**: End users integrating ska into their applications.
- **Responsibility**: Usage examples for core API, Django integration, CLI.
- **When to update**: Any change to public API (new function, changed signature, new default).
- **Rules**: Examples must be runnable. Do not include pseudo-code. Use actual import paths (`from ska import sign_url`).

### AGENTS.md

- **Audience**: AI agents and developers working on the codebase.
- **Responsibility**: Architecture invariants, hard constraints, known behaviors.
- **When to update**: Any change to repository layout, hard constraints, agent obligations.
- **Rules**: Do not reference SKILL.md files from AGENTS.md. Do not include procedural steps.

### .agents/skills/*/SKILL.md

- **Audience**: AI agents performing specific tasks.
- **Responsibility**: Procedures for dev-setup, dev-workflow, coding-standards, pr-review, update-documentation.
- **When to update**: Any change to developer processes, tool configurations, or workflow definitions.
- **Rules**: Each skill has a single responsibility. Do not merge procedural logic.

### CONTRIBUTING.rst

- **Audience**: Human contributors.
- **Responsibility**: Contributor guidelines, PR process, testing instructions.
- **When to update**: Process changes (testing, linting, PR submission).

### docs/

- **Audience**: API reference consumers.
- **Responsibility**: Full technical reference (Sphinx).
- **When to update**: New features, removed features, changed behavior.
- **Rules**: Do not modify auto-generated files (conf.py, apidoc output). Do not add pseudo-code examples.

## 5. Feature-specific documentation checklist

### Adding an exception

1. Add to `src/ska/exceptions.py` with docstring.
2. Export from `src/ska/__init__.py`.
3. Add to `__all__` in the module.
4. Document in `README.rst` under the relevant section if it is a public-facing exception.
5. Add a usage example in `README.rst` showing when the exception is raised.

### Adding CLI commands/options

1. Implement in `src/ska/generate_signed_url.py`.
2. Document arguments in `README.rst` under "Command line usage".
3. Update the CLI example block with new arguments.
4. Verify the CLI help text matches documentation (`ska-sign-url --help`).

### Adding/changing public API

1. Add function with type annotations and docstring.
2. Export from `src/ska/__init__.py`.
3. Add to `__all__`.
4. Add usage example in `README.rst`.
5. If the function has configurable defaults, verify `defaults.py` reflects the actual defaults.

### Changing defaults/limits

1. Update the default value in `src/ska/defaults.py`.
2. Find all references to that default in `README.rst` and update them.
3. If a default affects Django settings, update `src/ska/contrib/django/ska/settings.py` and `README.rst`.
4. Ensure all example code using that default is consistent.

## 6. Code example rules (documentation-as-tests)

- Codeblock tests are run via `pytest-codeblock` against `README.rst` and other `.rst` files.
- Named code blocks (`:name:` directive) are treated as test targets.
- **Naming convention for codeblock tests**: Use descriptive names matching the test pattern (e.g., `test_signing_urls`, `test_signing_dicts`).
- When editing examples, preserve the `.name:` and `.continue:` directives so tests chain correctly.
- Do not introduce pseudo-code examples where runnable examples are expected.
- If an example cannot be made runnable (e.g., framework-specific), mark it clearly but do not include invalid code.

## 7. Validation checklist (before reporting completion)

- [ ] README.rst examples match actual API (imports, function calls, return values)
- [ ] AGENTS.md matches architecture (modules listed exist, constraints reflect reality)
- [ ] SKILL.md descriptions remain accurate (procedures still work with current tool versions)
- [ ] Cross-references and file paths are valid (no broken `:doc:` or `:ref:` roles)
- [ ] No generated docs were modified (check `docs/_build/`, `htmlcov/`)
- [ ] `conftest.py` fixtures referenced in docs exist and are correct
- [ ] CLI help text (`ska-sign-url --help`) matches README.rst documentation

## 8. What NOT to do

- Do not modify source code to match documentation.
- Do not weaken policy encoded in SKILL.md or AGENTS.md.
- Do not silently delete content; preserve intent while correcting facts.
- Do not reformat docs unnecessarily; minimize diffs.
- Do not add new external dependencies to core to "make docs work".
- Do not modify `conftest.py` to fix test failures.
- Do not change version manually (use `make update-version`).

## Output

The output of this skill is a set of documentation edits plus a clear change report:
- Files changed (paths)
- What changed (deltas)
- What could not be fixed and why

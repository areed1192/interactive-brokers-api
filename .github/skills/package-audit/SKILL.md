---
name: package-audit
description: >
  Perform a comprehensive audit of a Python package and produce a phased improvement plan
  saved to IMPROVEMENT.md. Use this skill whenever someone asks to review a Python package,
  audit a codebase, plan improvements, modernize a project, assess package quality, or
  produce an improvement roadmap. Trigger on phrases like "review this package", "audit
  my project", "what should I improve", "create an improvement plan", "make this package
  better", "is this project production-ready", "what's wrong with my package", or any
  request that involves evaluating a Python package holistically. This skill only PLANS —
  it does not implement changes.
---

# Package Audit

This skill audits a Python package across eight dimensions, identifies issues, and
produces a prioritized, phased improvement plan saved to `IMPROVEMENT.md`. It does
not implement any changes — the output is a plan that the user can review and execute
in subsequent sessions.

## Before you start

Read the best-practices reference file:

```
cat references/best-practices.md
```

Use the checklist in that file as your scanning rubric.

## Critical rule

**This skill only produces a plan. Do not implement any changes.** Every finding
goes into `IMPROVEMENT.md` as an unchecked action item. The user will execute
those items later, possibly using other specialized skills.

## Workflow

### Step 1 — Classify the project

Before auditing, determine what kind of project this is. The project type shapes
which audit dimensions apply and how the phased plan is organized.

Look at `pyproject.toml`, `setup.py`, the directory structure, and the README to
classify into one of:

- **Library** — distributed on PyPI, has a public API, users import it.
  Example signals: `[project]` table, `name` on PyPI, `from mypkg import ...` in examples.
- **CLI tool** — primary interface is command-line. Example signals:
  `[project.scripts]` entry points, `argparse`/`click`/`typer` in the code,
  README shows shell commands.
- **Web service** — long-running server. Example signals: Flask/FastAPI/Django
  imports, `uvicorn`/`gunicorn` in dependencies, Dockerfile, API routes.
- **Internal application** — not distributed, used internally. Example signals:
  no PyPI publishing, no classifiers, may have deployment configs instead.
- **Data/ML project** — notebooks and pipelines. Example signals: `.ipynb` files,
  `pandas`/`numpy`/`scikit-learn` in deps, `data/` or `models/` directories.

Note the classification at the top of the audit. Skip or adjust dimensions that
don't apply (e.g., a CLI tool doesn't need a "convenience API" phase; an internal
application doesn't need PyPI classifiers).

### Step 2 — Discovery

Systematically examine the project across these eight dimensions. Take notes as
you go — you'll use them in Step 3.

1. **Project structure**
   - List top-level directories and their purposes
   - Identify the layout (`src/` vs flat)
   - Check for `__init__.py` completeness
   - Note any files that shouldn't be tracked (`.pyc`, `__pycache__`, `.DS_Store`,
     `*.egg-info`)

2. **Packaging & metadata**
   - Is there a `pyproject.toml`? If only `setup.py`, that's a finding.
   - Does `[project]` include: `name`, `version`, `description`, `readme`,
     `requires-python`, `license`, `authors`, `classifiers`, `dependencies`,
     `[project.urls]`?
   - Build backend: Hatchling, Setuptools, Poetry, PDM, Flit?
   - Are optional dependencies grouped (`[project.optional-dependencies]`)?
   - Are classifiers valid PyPI trove classifiers?

3. **Public API**
   - What does the package's `__init__.py` export?
   - Map every public class and function (names not starting with `_`)
   - Are there type hints on public signatures?
   - Is the API consistent in naming (snake_case functions, PascalCase classes)?

4. **Test coverage**
   - Is there a `tests/` directory?
   - Which modules have no test file?
   - If possible, run `pytest --cov=<package> --cov-report=term-missing`
   - Note the overall coverage percentage and uncovered modules

5. **Documentation**
   - Does the README exist and cover: what it does, install, quick-start, link to full docs?
   - Are there docstrings on public functions/classes?
   - Is there a `CHANGELOG.md`?
   - Are there example files or usage notebooks?
   - Is there an API reference (Sphinx, MkDocs)?

6. **CI/CD**
   - Is there a `.github/workflows/` directory (or GitLab/Bitbucket equivalent)?
   - Are tests run automatically on push/PR?
   - Is there linting in CI?
   - Is there a release workflow (PyPI publishing on tag)?
   - Is Dependabot/Renovate configured?

7. **Security** (run these checks if possible)
   - Run `bandit -r <package>/ -q` and note findings
   - Run `pip-audit` or check for known vulnerable dependencies
   - Grep for obvious issues: hardcoded passwords/tokens, `eval()`, `exec()`,
     `shell=True` in subprocess, `pickle.load` on untrusted data,
     unsafe XML parsing (`xml.etree` instead of `defusedxml`)
   - Check for missing input validation on public API methods

8. **Code quality**
   - Are type hints used consistently?
   - Is `from __future__ import annotations` used (for 3.9 support)?
   - Is logging used instead of `print()`?
   - Are custom exceptions defined, or does everything use built-ins?
   - Is there dead code (unused imports, unreachable branches)?
   - Naming consistency (PEP 8)

### Step 3 — Write IMPROVEMENT.md

Save the audit and plan to `IMPROVEMENT.md` in the project root, following
this exact template:

```markdown
# Improvement Plan

**Project type:** <Library / CLI tool / Web service / Internal app / Data/ML>
**Audit date:** <YYYY-MM-DD>
**Audited against:** [Keep a Changelog 1.1.0, Semantic Versioning 2.0.0,
PEP 621, pytest, bandit]

## Audit Summary

### Strengths

- What the project does well. Keep doing these.
- Be specific — "uses modern pyproject.toml with complete metadata" not "good packaging".

### Critical Issues

Security vulnerabilities, broken functionality, missing input validation, hardcoded
credentials. Each issue must cite the file and line number where applicable.

### Code Quality Issues

Inconsistent patterns, missing type hints, poor error handling, dead code.

### Missing Infrastructure

No tests, no CI, no linting, no changelog, outdated packaging.

### Feature Gaps

<Only if Step 1 classified this as a Library. Skip for other project types.>
Features missing compared to similar packages users would expect.

### Developer Experience Gaps

Poor README, no examples, verbose boilerplate, missing convenience features.

---

## Improvement Phases

### Phase 1: Foundation & Safety

Security fixes, input validation, exception handling, packaging modernization,
CI pipeline, basic test coverage.

- [ ] **P0 · S** — Add input validation to `parser.parse_url()` (`src/pkg/parser.py:42`)
      to reject URLs with `file://` scheme
- [ ] **P0 · M** — Replace `xml.etree.ElementTree` with `defusedxml` for untrusted XML
      parsing (`src/pkg/xml_reader.py`)
- [ ] **P1 · M** — Modernize packaging: migrate `setup.py` to `pyproject.toml` with
      full `[project]` metadata
- [ ] **P1 · L** — Add GitHub Actions workflow: lint + test on push/PR

### Phase 2: Code Quality & Reliability

Type hints, consistent error handling, custom exceptions, logging, docstrings.

- [ ] **P1 · M** — Add type hints to all public functions in `src/pkg/api.py`
- [ ] **P1 · S** — Replace `print()` statements with `logging` (`src/pkg/cli.py:15-28`)
- [ ] **P2 · M** — Define custom exception hierarchy (`PkgError`, `PkgValidationError`,
      `PkgConnectionError`)

### Phase 3: Developer Experience

<Skip for internal applications. Adapt heavily for CLI tools and web services —
these care more about user-facing docs than API ergonomics.>

README rewrite, examples, convenience API, sample files.

- [ ] **P1 · L** — Rewrite README with install/quick-start/example sections
- [ ] **P2 · M** — Add `examples/` directory with runnable usage scripts

### Phase 4: Ecosystem & Growth

<Only for libraries with a public user base. Skip for internal apps and new
projects that haven't hit 1.0 yet.>

Optional integrations, serialization helpers, async support, caching.

- [ ] **P2 · L** — Add optional pandas integration via `[project.optional-dependencies]`
- [ ] **P2 · L** — Provide async client under `pkg.aio` module

---

## Progress

| Phase   | Status      | Items Done | Items Total |
| ------- | ----------- | ---------- | ----------- |
| Phase 1 | Not started | 0          | N           |
| Phase 2 | Not started | 0          | N           |
| Phase 3 | Not started | 0          | N           |
| Phase 4 | Not started | 0          | N           |
```

### Step 4 — Item format rules

Every action item follows this exact format:

```
- [ ] **<Priority> · <Size>** — <Specific action with file path and/or line numbers>
```

**Priority:**

- **P0** — Critical. Security, data loss risk, broken functionality, legal/licensing.
- **P1** — High value. Major quality, reliability, or usability improvement.
- **P2** — Nice to have. Polish, optional features, minor DX improvements.

**Size:**

- **S** — Small. Less than 1 hour of focused work.
- **M** — Medium. 1–3 hours.
- **L** — Large. 3+ hours, may span a full day.

**Specificity rules:**

- Reference actual file paths: `src/pkg/parser.py:42` not "the parser"
- Name the actual thing to change: "add `timeout` parameter to `fetch()`"
  not "improve the fetch method"
- Each item must be independently actionable — someone reading just that line
  should know what to do
- Split compound items: "add type hints AND tests" becomes two items

### Step 5 — Feature gap research (optional, libraries only)

If the project is a **library** and the user asked about feature gaps or
ecosystem fit, search PyPI and GitHub for 2–3 similar packages. Compare:

- What capabilities do competitors offer that this package lacks?
- What conventions are standard in the space?

Include findings under "Feature Gaps" with source citations.

For non-library projects, skip this step — it doesn't apply to CLI tools,
internal apps, or web services in the same way.

### Step 6 — Present

After writing `IMPROVEMENT.md`, present a summary to the user:

- Total item count and breakdown by priority
- The top 3 most critical items
- Which phases are most/least populated

Let the user know they can execute items in future sessions. If the project
needs logging improvements, changelog work, or test coverage work specifically,
mention the specialized skills that handle those (`python-logging-reviewer`,
`changelog-review`, `test-coverage-review`).

## Constraints

- **Plan only, never implement.** Do not modify any code. Do not create tests.
  Do not rewrite the README. The only file this skill writes is `IMPROVEMENT.md`.
- **Be specific.** Vague items ("improve security") are useless. Every item
  must name the file, the method, and the change.
- **Prioritize ruthlessly.** A plan with 200 items is a plan no one will execute.
  Target 15–40 items total. If you find more issues, prioritize the critical
  ones and note "…and others" in the audit summary.
- **Don't recommend changes that don't serve real users.** Adding async support
  to a synchronous CLI tool with no demand for it is not helpful. Weigh every
  recommendation against whether a real user would benefit.
- **Adapt phases to project type.** Don't force library-specific phases onto
  a CLI tool or internal application.
- **Respect existing choices.** If the project deliberately uses `setup.py` for
  reasons visible in comments or commit history, note the modernization option
  but don't treat it as critical.

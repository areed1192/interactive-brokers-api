# Python Package Audit Reference

This file is the scanning rubric for the package-audit skill. Each dimension below
lists what to check for, what good looks like, and common findings with their
typical priority.

## Source abbreviations

| Tag           | Source                                                        |
|---------------|---------------------------------------------------------------|
| [PYPA]        | Python Packaging User Guide (packaging.python.org)            |
| [PEP621]      | PEP 621 — Storing project metadata in pyproject.toml          |
| [PEP517]      | PEP 517 — A build-system independent format                   |
| [PEP518]      | PEP 518 — Specifying minimum build system requirements        |
| [PEP639]      | PEP 639 — Improving License Clarity with Better Package Metadata |
| [PEP8]        | PEP 8 — Style Guide for Python Code                          |
| [PEP561]      | PEP 561 — Distributing and Packaging Type Information         |
| [BANDIT]      | Bandit security linter (bandit.readthedocs.io)               |
| [KACL]        | Keep a Changelog 1.1.0                                       |
| [SEMVER]      | Semantic Versioning 2.0.0                                    |
| [SRE]         | Google SRE Book — Monitoring Distributed Systems             |

---

## Dimension 1: Project Structure

### What to check
- Layout: `src/` layout vs flat layout
- Presence of `__init__.py` files
- Directory naming follows PEP 8 (lowercase, underscores)
- Files that shouldn't be tracked in git

### What good looks like
```
project/
├── pyproject.toml
├── README.md
├── LICENSE
├── CHANGELOG.md
├── .gitignore
├── .github/workflows/
├── src/
│   └── mypackage/
│       ├── __init__.py
│       ├── py.typed             # If type hints are shipped
│       └── ...
└── tests/
    ├── conftest.py
    └── test_*.py
```

The `src/` layout is recommended for new projects because it prevents
accidental imports from the source tree during testing — tests run against
the installed package.

**Source:** [PYPA]

### Common findings
| Finding                                          | Priority |
|--------------------------------------------------|----------|
| No `.gitignore` or missing `__pycache__`, `*.egg-info` entries | P1 · S |
| Tracked `.pyc`, `__pycache__`, or `.DS_Store` files | P2 · S |
| Flat layout with package name matching common imports (collision risk) | P2 · M |
| Missing `__init__.py` in subpackages             | P1 · S |
| Package directory name uses hyphens or mixed case | P1 · S |

---

## Dimension 2: Packaging & Metadata

### What to check
- Presence of `pyproject.toml`
- Whether `setup.py` is legacy-only or doing non-declarative work
- Completeness of `[project]` metadata
- Build backend choice
- Valid PyPI trove classifiers
- License declaration
- Optional dependency groups
- Project URLs

### What good looks like
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "mypackage"
version = "1.2.0"
description = "A short one-line description."
readme = "README.md"
requires-python = ">=3.9"
license = "MIT"
license-files = ["LICEN[CS]E*"]
authors = [{name = "Your Name", email = "you@example.com"}]
keywords = ["relevant", "search", "terms"]
classifiers = [
  "Development Status :: 4 - Beta",
  "Intended Audience :: Developers",
  "Programming Language :: Python :: 3",
  "Programming Language :: Python :: 3.9",
  "Programming Language :: Python :: 3.10",
  "Programming Language :: Python :: 3.11",
  "Programming Language :: Python :: 3.12",
  "Operating System :: OS Independent",
]
dependencies = [
  "requests>=2.28",
]

[project.optional-dependencies]
dev = ["pytest>=7", "ruff", "mypy"]
docs = ["sphinx", "furo"]

[project.urls]
Homepage = "https://github.com/user/mypackage"
Documentation = "https://mypackage.readthedocs.io"
Repository = "https://github.com/user/mypackage"
Issues = "https://github.com/user/mypackage/issues"
Changelog = "https://github.com/user/mypackage/blob/main/CHANGELOG.md"
```

**Source:** [PYPA], [PEP621], [PEP639]

### Common findings
| Finding                                          | Priority |
|--------------------------------------------------|----------|
| `setup.py` only, no `pyproject.toml`             | P1 · M   |
| `[project]` missing `description`, `readme`, or `requires-python` | P1 · S |
| No `classifiers` (hurts PyPI discoverability)   | P1 · S   |
| Using deprecated `License ::` classifier instead of SPDX `license` key | P2 · S |
| No `[project.urls]` (no links on PyPI)          | P1 · S   |
| No `[project.optional-dependencies]` for dev/docs extras | P2 · S |
| `requires-python` missing or too permissive (e.g., `>=2.7`) | P1 · S |
| Classifiers include a Python version not tested in CI | P2 · S |
| Dependencies unpinned (no lower bound)           | P2 · S   |

---

## Dimension 3: Public API

### What to check
- What does `__init__.py` export via `__all__` or re-exports?
- Map of public classes, functions, methods (names not starting with `_`)
- Type hints on public signatures
- Naming consistency: `snake_case` for functions/methods, `PascalCase` for classes, `UPPER_CASE` for constants
- Deprecation warnings on changed/removed APIs

### What good looks like
- `__all__` explicitly lists public names
- Every public function has type hints on parameters and return
- Public classes have `__repr__` / `__str__` defined where useful
- Deprecated APIs use `warnings.warn(..., DeprecationWarning)`

**Source:** [PEP8], [PEP561]

### Common findings
| Finding                                          | Priority |
|--------------------------------------------------|----------|
| No `__all__` in `__init__.py` (everything is implicitly public) | P2 · S |
| Public functions without type hints              | P1 · M   |
| Inconsistent naming across modules               | P2 · M   |
| Same functionality exposed under multiple names  | P2 · S   |
| No `py.typed` marker despite shipping type hints | P1 · S   |
| Removed public APIs with no deprecation path     | P0 · M   |

---

## Dimension 4: Test Coverage

### What to check
- Presence of `tests/` directory
- Which source modules have no corresponding test file
- Test framework in use (pytest, unittest)
- Coverage percentage if measurable
- Whether tests run offline (no live network/API calls)

### Running coverage
```bash
pytest tests/ --cov=<package> --cov-report=term-missing --tb=short -q
```

### Common findings
| Finding                                          | Priority |
|--------------------------------------------------|----------|
| No tests at all                                  | P0 · L   |
| Tests make live API calls                        | P0 · M   |
| Public modules with no test file                 | P1 · M   |
| Test coverage under 50%                          | P1 · L   |
| Tests depend on execution order                  | P1 · M   |
| Mixing unittest and pytest styles without reason | P2 · M   |

For detailed test-quality findings, defer to the `test-coverage-review` skill
instead of duplicating that work here.

---

## Dimension 5: Documentation

### What to check
- README covers: what, install, quick-start, link to full docs
- CHANGELOG.md exists and follows Keep a Changelog
- Docstrings on public classes and functions
- Example files or notebooks
- API reference (Sphinx, MkDocs) if the library is published
- CONTRIBUTING.md if the project accepts contributions

### README checklist
A good README has, in this order:
1. Project name and one-line description
2. Badges (tests, PyPI version, license, Python versions)
3. Installation instructions
4. Quick-start: a single runnable example that demonstrates the core value
5. Feature list or use cases
6. Link to full documentation
7. Contributing instructions (or link to CONTRIBUTING.md)
8. License

**Source:** [KACL], [PYPA]

### Common findings
| Finding                                          | Priority |
|--------------------------------------------------|----------|
| No README, or README is just the project name    | P0 · M   |
| README missing install instructions              | P1 · S   |
| README missing runnable quick-start example      | P1 · M   |
| No CHANGELOG.md                                  | P1 · S   |
| CHANGELOG doesn't follow Keep a Changelog        | P2 · M   |
| Public functions with no docstrings              | P1 · M   |
| No `examples/` directory                         | P2 · M   |
| No API documentation site (libraries)            | P2 · L   |
| No LICENSE file despite `license = "MIT"` in pyproject.toml | P0 · S |

For CHANGELOG-specific findings, defer to the `changelog-review` skill.

---

## Dimension 6: CI/CD

### What to check
- Presence of `.github/workflows/` (or equivalent for GitLab, Bitbucket)
- Tests run on push and pull request
- Linting runs in CI
- Matrix across Python versions declared in classifiers
- Release/publish workflow on tag push
- Dependabot/Renovate for dependency updates

### What good looks like
A library project should have at minimum:
- **`.github/workflows/test.yml`** — runs on every push and PR, tests across
  all supported Python versions, runs linter and type checker
- **`.github/workflows/publish.yml`** — triggered by version tags, builds
  wheel + sdist, publishes to PyPI using Trusted Publishers (OIDC)
- **`.github/dependabot.yml`** — weekly or monthly dependency updates

**Source:** [PYPA]

### Common findings
| Finding                                          | Priority |
|--------------------------------------------------|----------|
| No CI workflow                                   | P1 · L   |
| Tests only run on one Python version             | P1 · M   |
| No linting in CI                                 | P1 · S   |
| Classifiers claim Python 3.12 support but CI doesn't test it | P1 · S |
| Manual PyPI publishing (no release workflow)     | P2 · M   |
| PyPI publishing uses long-lived API token instead of OIDC | P1 · M |
| No Dependabot/Renovate                           | P2 · S   |

---

## Dimension 7: Security

### What to check
Run automated scans first:
```bash
# Static analysis for security issues in code
bandit -r <package>/ -q

# Dependency vulnerability check
pip-audit

# Or with safety (alternative)
safety check
```

Then manually grep for patterns bandit might miss:
- Hardcoded secrets: `password =`, `api_key =`, `token =`, `secret =`
- Dangerous functions: `eval(`, `exec(`, `__import__(`
- Command injection: `subprocess.*shell=True`, `os.system(`
- Unsafe XML: `xml.etree`, `xml.sax` (should be `defusedxml`)
- Unsafe deserialization: `pickle.load(`, `pickle.loads(` on untrusted data
- Path traversal: user input passed to `open()`, `Path()` without validation
- SSRF: user-supplied URLs in `requests.get()`, `urllib.request.urlopen()`
  without scheme allow-listing

### What good looks like
- Bandit scan produces no high/medium severity findings (or they're all
  justified with `# nosec` comments explaining why)
- All user input to public methods is validated
- XML parsing uses `defusedxml`
- Subprocess calls use argument lists, never `shell=True`
- Secrets come from environment variables, never hardcoded
- URLs are allow-listed by scheme (https only) before fetching

**Source:** [BANDIT]

### Common findings
| Finding                                          | Priority |
|--------------------------------------------------|----------|
| Hardcoded API keys, tokens, or passwords in source | P0 · S |
| `subprocess.*shell=True` with user input         | P0 · S   |
| `eval()` or `exec()` on user input               | P0 · S   |
| `xml.etree` used on untrusted input              | P0 · M   |
| `pickle.load` on untrusted data                  | P0 · S   |
| User-supplied URLs fetched without scheme validation | P0 · M |
| No input validation on public API methods        | P1 · M   |
| Dependencies with known CVEs (pip-audit)         | P0 · S   |
| No `bandit` or `pip-audit` in CI                 | P1 · S   |

---

## Dimension 8: Code Quality

### What to check
- Type hints on public functions (run `mypy --strict <package>` if possible)
- `from __future__ import annotations` for forward references / PEP 604 union syntax on Python < 3.10
- Logging vs. `print()`
- Custom exception hierarchy vs. built-in exceptions everywhere
- Dead code (run `vulture` or check for unused imports, unreachable code)
- Consistent naming per PEP 8
- Docstring style consistency (Google / NumPy / reST — pick one)

### What good looks like
- All public signatures have types
- Module-level `logger = logging.getLogger(__name__)` and `logger.info(...)` usage
- A package-level exception base class with specific subclasses
- No `print()` calls in library code (CLI tools are an exception for user-facing output)
- Consistent docstring format across the codebase

**Source:** [PEP8], [SRE]

### Common findings
| Finding                                          | Priority |
|--------------------------------------------------|----------|
| `print()` used for diagnostics in library code   | P1 · S   |
| No type hints on public functions                | P1 · M   |
| All errors use built-in `Exception` or `ValueError` | P2 · M |
| Bare `except:` blocks                            | P1 · S   |
| Unused imports across multiple files             | P2 · S   |
| Inconsistent docstring styles                    | P2 · M   |
| Configuration done in module-level `basicConfig()` (library code) | P1 · S |
| No `__repr__` on dataclass-like classes          | P2 · S   |

For detailed logging findings, defer to `python-logging-reviewer`.

---

## How to use this reference

1. Walk each dimension in order.
2. For each finding, note the file/line and map it to a priority and size from
   this document's tables.
3. Group findings into the four phases in `IMPROVEMENT.md` based on the
   phase descriptions:
   - **Phase 1** — All P0 findings + packaging/CI foundations
   - **Phase 2** — Code quality findings that improve reliability
   - **Phase 3** — Developer experience findings (README, examples, API polish)
   - **Phase 4** — Growth features (integrations, async, caching) — libraries only

4. If a finding falls under a specialized skill (logging, changelog, tests),
   the action item can say "see python-logging-reviewer skill" rather than
   duplicating those skills' audit logic.

## Project type adjustments

Not every dimension applies equally to every project type:

| Dimension           | Library | CLI | Web service | Internal | Data/ML |
|---------------------|---------|-----|-------------|----------|---------|
| Project structure   | ✅      | ✅  | ✅          | ✅       | ✅      |
| Packaging/metadata  | ✅      | ✅  | ⚠️          | ⚠️       | ⚠️      |
| Public API          | ✅      | ⚠️  | ⚠️          | ❌       | ⚠️      |
| Test coverage       | ✅      | ✅  | ✅          | ✅       | ⚠️      |
| Documentation       | ✅      | ✅  | ⚠️          | ⚠️       | ✅      |
| CI/CD               | ✅      | ✅  | ✅          | ⚠️       | ⚠️      |
| Security            | ✅      | ✅  | ✅          | ✅       | ✅      |
| Code quality        | ✅      | ✅  | ✅          | ✅       | ✅      |

Legend: ✅ fully applicable · ⚠️ applies with adjustments · ❌ skip

**Internal applications** skip "public API" since there are no external users
importing it. "Packaging" becomes about deployment config rather than PyPI metadata.

**Web services** care about deployment, containerization, and runtime observability
more than PyPI metadata. Consider adding Dockerfile review and health check
endpoints to the audit.

**Data/ML projects** often have looser testing (notebooks aren't easily tested).
Focus on reproducibility (locked dependencies, random seeds) and data pipeline
documentation instead.

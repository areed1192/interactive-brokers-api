# Changelog & Versioning Best Practices Reference

This file is the authoritative checklist for the changelog-review skill.
Every audit finding must trace back to a practice listed here.

## Source abbreviations

| Tag        | Source                                                                   |
|------------|--------------------------------------------------------------------------|
| [KACL]     | Keep a Changelog 1.1.0 (keepachangelog.com/en/1.1.0)                    |
| [SEMVER]   | Semantic Versioning 2.0.0 (semver.org)                                  |
| [PEP440]   | PEP 440 — Version Identification and Dependency Specification           |
| [PEP621]   | PEP 621 — Storing project metadata in pyproject.toml                    |
| [GNU-STD]  | GNU Coding Standards — Style of Change Logs                             |

---

## 1. Keep a Changelog Format

### 1.1 File naming and location
The changelog file should be named `CHANGELOG.md` and live in the project root.
Alternative names (`HISTORY.md`, `NEWS.md`, `CHANGES.md`) are acceptable but
`CHANGELOG.md` is the most widely recognized and discoverable.

**Source:** [KACL] — "Call it `CHANGELOG.md`"

### 1.2 File header
The file should begin with:
```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
```

The header tells readers and tools which format and versioning scheme to expect.

**Source:** [KACL] — Guiding Principles: "Mention whether you follow Semantic Versioning"

### 1.3 The Unreleased section
An `## [Unreleased]` section must exist at the top of the changelog (below the
header). All work-in-progress entries go here until a release is cut.

**Why it matters:** It serves two purposes — users can see what's coming in the
next release, and at release time you simply rename the section to a version number
rather than assembling entries retroactively.

**Anti-patterns to flag:**
- No `[Unreleased]` section exists
- Entries are added directly under version numbers that haven't been released yet
- Multiple `[Unreleased]` sections

**Source:** [KACL] — "Keep an `Unreleased` section at the top to track upcoming changes"

### 1.4 Change type headings
Entries must be grouped under one of these six headings, in this canonical order:

| Heading        | Use for                                           |
|----------------|---------------------------------------------------|
| `### Added`    | New features                                      |
| `### Changed`  | Changes in existing functionality                 |
| `### Deprecated` | Soon-to-be removed features                     |
| `### Removed`  | Now removed features                              |
| `### Fixed`    | Bug fixes                                         |
| `### Security` | Vulnerability fixes                               |

**Anti-patterns to flag:**
- Non-standard headings: `### Improvements`, `### Misc`, `### Other`,
  `### Enhancements`, `### Updates`, `### Bugfixes` (should be `Fixed`)
- Missing heading level (using `## Fixed` instead of `### Fixed`)
- Entries placed directly under the version heading without a type heading
- Empty headings with no entries beneath them (remove these to reduce noise)

**Source:** [KACL] — "Types of changes"

### 1.5 Version headings
Released versions must use the format:
```
## [x.y.z] - YYYY-MM-DD
```

- The version number is in square brackets.
- A single hyphen separates the version from the date.
- The date is always ISO 8601 format (`YYYY-MM-DD`).

**Anti-patterns to flag:**
- Missing date: `## [1.2.0]`
- Regional date format: `## [1.2.0] - 04/19/2026` or `## [1.2.0] - 19 April 2026`
- Missing brackets: `## 1.2.0 - 2026-04-19`
- Version prefix: `## [v1.2.0]` (the `v` prefix belongs on git tags, not in
  the changelog — though this is a stylistic choice some projects make deliberately)

**Source:** [KACL] — "Confusing Dates" section, ISO 8601 recommendation

### 1.6 Reverse chronological order
The most recent version must appear first (directly below `[Unreleased]`).
Older versions follow in descending order.

**Source:** [KACL] — Guiding Principles: "The latest version comes first"

### 1.7 Comparison links
The bottom of the file should contain link definitions for every version,
pointing to the repository's diff between tags:

```markdown
[unreleased]: https://github.com/user/repo/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/user/repo/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/user/repo/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/user/repo/releases/tag/v1.0.0
```

**Why it matters:** These make the bracketed version numbers clickable in
rendered markdown, letting users jump directly to the full diff on GitHub/GitLab.

**Anti-patterns to flag:**
- No comparison links at all
- Links that don't match the versions in the changelog
- Broken or outdated URLs
- Missing `[unreleased]` comparison link

**Source:** [KACL] — Guiding Principles: "Versions and sections should be linkable"

### 1.8 Yanked releases
If a release was pulled due to a serious bug or security issue, it must be
marked with `[YANKED]`:
```
## [0.5.0] - 2026-03-01 [YANKED]
```

Yanked releases should still appear in the changelog — do not silently remove them.

**Source:** [KACL] — "What about yanked releases?"

---

## 2. Entry Quality

### 2.1 Write for humans, not machines
Changelog entries are for end users, contributors, and maintainers. They should
describe *what changed* and *why it matters*, not *how it was implemented*.

**Good entries:**
```markdown
- **edgar/models.py**: `Fact` and `Facts` XBRL dataclass models.
  - `Facts.get(taxonomy, concept, unit=None)` returns a flat `list[Fact]` sorted by end date.
  - `Fact` wraps a single data point with `value`, `end`, `form`, `filed` properties.
```

**Bad entries (flag these):**
```markdown
- Fixed bug                         # No context
- Updated code                     # Meaningless
- Merge pull request #42            # Commit log noise
- Refactored internals              # Not user-visible (skip entirely)
- misc changes and improvements     # Vague
```

**Source:** [KACL] — "Changelogs are for humans, not machines"

### 2.2 Commit log dumps
Using raw `git log` output as a changelog is explicitly called out as bad practice.
Commit messages serve a different purpose (documenting steps in source evolution)
than changelog entries (documenting notable differences between releases).

**Anti-patterns to flag:**
- Entries that look like commit messages (present tense, no context)
- Entries containing commit hashes
- Entries that are clearly auto-generated without editing

**Source:** [KACL] — "Don't let your friends dump git logs into changelogs"

### 2.3 One logical change per entry
Each bullet should describe one coherent change. Do not combine unrelated
changes into a single entry.

**Bad:**
```markdown
- Added user authentication and fixed the database migration bug.
```

**Good:**
```markdown
### Added
- **auth/login.py**: User authentication with JWT tokens.

### Fixed
- **db/migrations.py**: Database migration crash on empty tables.
```

### 2.4 Include test and sample files
When new test files or sample/fixture files are added, they deserve their own
entry under `### Added`. Include the test count when practical.

```markdown
- **tests/test_xbrl_facts.py**: 39 unit tests for XBRL Facts models and integration.
- **samples/10-K_2024.xml**: Sample SEC 10-K filing for integration tests.
```

### 2.5 Bold file paths
Prefix each entry with the bolded file or module path to quickly identify
where a change lives:
```markdown
- **edgar/models.py**: Description of the change.
```

This convention is especially valuable in projects with many modules, as it
lets readers scan for changes in their area of interest.

### 2.6 Deprecation warnings
When deprecating functionality, the changelog entry should explain:
- What is deprecated
- What replaces it (if anything)
- When it will be removed (version or timeline)

```markdown
### Deprecated
- **utils/old_parser.py**: `parse_legacy()` is deprecated in favor of
  `parse_v2()`. Will be removed in v3.0.0.
```

**Source:** [KACL] — Deprecated type; [SEMVER] — "Deprecating existing
functionality is a normal part of software development"

---

## 3. Semantic Versioning

### 3.1 Version format
Versions follow the `MAJOR.MINOR.PATCH` format where all three are
non-negative integers with no leading zeros.

- **MAJOR** — incremented for backward-incompatible API changes.
- **MINOR** — incremented for backward-compatible new functionality.
  Resets PATCH to 0.
- **PATCH** — incremented for backward-compatible bug fixes.

**Source:** [SEMVER] — §2, §6, §7, §8

### 3.2 Breaking changes require a MAJOR bump
Any removal of public API, rename of a public function/class/module,
change in return type, change in required parameters, or behavioral change
that existing callers would not expect constitutes a breaking change and
requires a MAJOR version increment.

**Anti-patterns to flag:**
- A `### Removed` entry in a MINOR or PATCH release
- A `### Changed` entry describing a breaking behavioral change in a MINOR release
- Removal of a function/class with no MAJOR bump

**Source:** [SEMVER] — "Backward incompatible API changes increment the major version"

### 3.3 New features require at least a MINOR bump
Adding new public functions, classes, methods, parameters, or modules
is a MINOR change (not a PATCH).

**Anti-patterns to flag:**
- `### Added` entries in a PATCH release

**Source:** [SEMVER] — "Backward compatible API additions/changes increment the minor version"

### 3.4 Pre-release and initial development
- **0.y.z** versions are for initial development. Anything may change at any time.
  The public API should not be considered stable.
- Pre-release versions append a hyphen and identifiers: `1.0.0-alpha.1`,
  `1.0.0-beta.2`, `1.0.0-rc.1`.
- Pre-release versions have lower precedence than the associated normal version.

**Source:** [SEMVER] — §4, §9, §11

### 3.5 Immutability of released versions
Once a versioned package has been released, the contents of that version
must NOT be modified. Any modifications must be released as a new version.
This applies to both the code and the changelog entry.

**Anti-patterns to flag:**
- Edits to changelog entries under released version headings
- Re-tagging an existing version with different code

**Source:** [SEMVER] — §3: "Once a versioned package has been released, the
contents of that version MUST NOT be modified"

---

## 4. Python-Specific Versioning

### 4.1 Version in pyproject.toml
Modern Python projects store their version in `pyproject.toml` under
`[project].version`. This must be a PEP 440-compliant string.

```toml
[project]
name = "my-package"
version = "1.2.0"
```

Some projects use dynamic versioning where the version is computed by the
build backend from git tags or a `__version__` variable.

**Anti-patterns to flag:**
- Version in `pyproject.toml` doesn't match the latest released version
  in `CHANGELOG.md`
- Version string uses a `v` prefix (PEP 440 does not allow this)
- Version exists in multiple places with conflicting values

**Source:** [PEP621], [PEP440]

### 4.2 PEP 440 vs SemVer differences
PEP 440 and SemVer are mostly compatible but have differences:

| Concept            | SemVer              | PEP 440               |
|--------------------|---------------------|------------------------|
| Pre-release        | `1.0.0-alpha.1`     | `1.0.0a1`              |
| Post-release       | Not supported       | `1.0.0.post1`          |
| Dev release        | Not supported       | `1.0.0.dev1`           |
| Local version      | Build metadata `+`  | `1.0.0+local1`         |

When the changelog uses SemVer notation and the project uses PEP 440 in
`pyproject.toml`, the skill should note the difference but not flag it as
an error — this is standard practice in the Python ecosystem.

**Source:** [PEP440], [SEMVER]

### 4.3 Single source of truth for version
The version should be defined in exactly one place and derived everywhere else.
Common patterns:

1. **pyproject.toml only** — Version in `[project].version`, read at build time.
2. **`__init__.py`** — `__version__ = "1.2.0"` in the package's `__init__.py`,
   with `pyproject.toml` using dynamic versioning to read from it.
3. **Git tags** — Build backend (e.g., `setuptools-scm`, `hatch-vcs`) derives
   the version from git tags.

**Anti-patterns to flag:**
- Version hardcoded in multiple files with no automation to keep them in sync
- `__version__` in `__init__.py` disagrees with `pyproject.toml`
- Changelog shows version `1.3.0` but `pyproject.toml` still says `1.2.0`

**Source:** [PEP621]

---

## 5. Release Checklist

When preparing a release, verify all of the following:

### 5.1 Changelog completeness
- [ ] All user-visible changes since the last release have entries
- [ ] Entries are under the correct type headings
- [ ] Each entry is clear and descriptive
- [ ] Test files and sample files have their own entries where appropriate
- [ ] No entries are in the wrong section (e.g., bug fix under `Added`)

### 5.2 Version consistency
- [ ] `## [Unreleased]` has been replaced with `## [x.y.z] - YYYY-MM-DD`
- [ ] A new empty `## [Unreleased]` section has been added above
- [ ] The version bump matches the severity of changes (see §3.1–3.3)
- [ ] `pyproject.toml` version matches the new version
- [ ] `__version__` (if it exists) matches the new version
- [ ] Comparison links at the bottom of the file are updated

### 5.3 Format compliance
- [ ] Date is in ISO 8601 format (`YYYY-MM-DD`)
- [ ] Version is in brackets: `## [x.y.z]`
- [ ] No empty type headings remain
- [ ] Reverse chronological order is maintained
- [ ] Previously released sections are unmodified

---

## 6. What Does NOT Need a Changelog Entry

These changes are not user-visible and should be omitted:

- Internal refactors with no API or behavior change
- Comment-only or docstring-only changes (unless they fix user-facing docs)
- CI/CD configuration changes (`Makefile`, `.github/workflows/`, `tox.ini`)
  unless they affect how users install or use the project
- Developer tooling (`.pre-commit-config.yaml`, linter configs)
- Dependency version pin updates (unless fixing a user-facing bug)
- Merge commits, branch maintenance
- Whitespace or formatting-only changes

**Source:** [KACL] — "Inconsistent Changes": important changes must be noted,
but trivial internal changes create noise.

---

## 7. Patterns to Scan For

### Structural issues (always flag)
```
### Improvements         # Non-standard heading
### Bug Fixes            # Should be "Fixed"
### Bugfixes             # Should be "Fixed"
### Enhancements         # Should be "Added" or "Changed"
### Misc                 # Non-standard
### Other                # Non-standard
### Updates              # Non-standard
## v1.2.0               # Missing brackets and/or date
## [1.2.0]              # Missing date
## [1.2.0] 2026-04-19   # Missing hyphen separator
```

### Entry quality issues (flag with context)
```
- Fixed bug              # Too vague
- Updated code           # Meaningless
- Merge pull request     # Commit log noise
- Various improvements   # Vague
- Minor changes          # Vague
- Bumped version         # Meta, not user-visible
```

### Version consistency checks
```
pyproject.toml version != latest changelog version    # Mismatch
__version__ != pyproject.toml version                 # Mismatch
### Added entry in a PATCH release                    # Wrong bump type
### Removed entry in a MINOR release                  # Should be MAJOR
```

### Good patterns (note approvingly)
```
## [Unreleased]                                        # Correct section
## [1.2.0] - 2026-04-19                               # Correct format
### Added / Changed / Fixed / Removed / Deprecated / Security  # Standard types
- **path/to/file.py**: Clear description.              # Good entry format
[unreleased]: https://github.com/...compare/v1.2.0...HEAD  # Comparison link
```

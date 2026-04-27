---
name: changelog-review
description: >
  Audit, enforce, and maintain changelogs in Python projects. Use this skill whenever someone
  asks to review a changelog, add a changelog entry, check if a changelog is up to date,
  fix changelog formatting, create a CHANGELOG.md from scratch, prepare a release, or
  ensure changelog compliance with Keep a Changelog. Trigger on phrases like "update the
  changelog", "add a changelog entry", "review my changelog", "is my changelog correct",
  "prepare for release", "bump the version", "what changed since last release", or any
  request involving CHANGELOG.md, release notes, or version management in a Python project.
  Also trigger when someone finishes a code change and needs to document it, or when they
  ask about semantic versioning.
---

# Changelog Review

This skill audits, creates, and maintains changelogs in Python projects following
the Keep a Changelog 1.1.0 format and Semantic Versioning 2.0.0.

## Before you start

Read the best-practices reference file to ground your review:

```
cat references/best-practices.md
```

Use the rules and source citations in that file as your authoritative checklist.

## Modes of operation

This skill operates in one of four modes depending on what the user needs.
Determine the mode from their request, then follow the corresponding workflow.

---

### Mode 1 — Audit an existing changelog

Use when the user says things like "review my changelog", "is my changelog correct",
or "check my CHANGELOG.md".

**Step 1: Read the changelog**

Open `CHANGELOG.md` (or `HISTORY.md`, `NEWS.md` — check all common names).
If no changelog exists, switch to Mode 3 (Create from scratch).

**Step 2: Check structure against Keep a Changelog 1.1.0**

Verify each of the following. For every violation, note the line number,
what's wrong, and cite the source from `references/best-practices.md`:

1. **Header** — File starts with `# Changelog` and optionally a description
   mentioning Keep a Changelog and Semantic Versioning.
2. **Unreleased section** — An `## [Unreleased]` section exists at the top.
3. **Change type headings** — Entries use only the six allowed types:
   `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`.
   Flag any non-standard headings (e.g., `### Improvements`, `### Misc`).
4. **Version format** — Released sections use `## [x.y.z] - YYYY-MM-DD`
   with ISO 8601 dates. Flag ambiguous date formats like `04/19/2026`.
5. **Reverse chronological order** — Newest version appears first.
6. **Comparison links** — Bottom of file has `[unreleased]` and version
   comparison links pointing to the repository's diff URLs.
7. **No empty sections** — Flag `### Added` headings with no entries beneath them.
8. **Entry quality** — Each entry should describe a user-visible change,
   not a commit message. Flag entries like "fixed bug" (no context) or
   entries that are clearly copy-pasted commit messages.
9. **Yanked releases** — If any release was yanked, it should be marked
   with `[YANKED]` after the date.

**Step 3: Cross-check with project metadata**

- Compare the latest released version in the changelog against
  `version` in `pyproject.toml` (or `setup.py`, `setup.cfg`).
  Flag mismatches.
- If there are commits or code changes since the last release tag
  that are not reflected in `## [Unreleased]`, note them.

**Step 4: Produce the audit report**

Output a markdown table:

| Line | Issue | Severity | Source |
|------|-------|----------|--------|
| 12   | Non-standard heading `### Improvements` | error | [KACL] §Types |
| 45   | Date format `04/19/2026` should be `2026-04-19` | warning | [KACL] §Dates |

Severity levels:
- **error** — Violates Keep a Changelog spec or Semantic Versioning.
- **warning** — Deviates from best practice but not spec-breaking.
- **info** — Suggestion for improvement.

---

### Mode 2 — Add a changelog entry

Use when the user says things like "update the changelog", "add this to the
changelog", or has just finished a code change.

**Step 1: Identify what changed**

Ask or infer from context:
- Which files were added, changed, or fixed?
- Is this a new feature (Added), a behavior change (Changed), a bug fix (Fixed),
  a removal (Removed), a deprecation (Deprecated), or a security fix (Security)?
- Are there new test files? New sample/fixture files?

**Step 2: Write the entries**

Follow this format for each entry:

```markdown
- **<file or module>**: Brief description of the user-visible change.
  - Sub-bullet for important details (methods, properties, behavior).
  - Another sub-bullet if needed.
```

Rules for writing entries:
- **Bold the file path** — `**path/to/file.py**:` prefix identifies where
  the change lives.
- **One entry per logical change** — do not combine unrelated changes.
- **Include test files** — new test files get their own `Added` entry with
  the test count (e.g., "12 unit tests for…").
- **Include sample/fixture files** — new or updated data files get their own entry.
- **Use the right section** — new features → Added, behavior changes → Changed,
  bug fixes → Fixed, removals → Removed, deprecations → Deprecated,
  vulnerability fixes → Security.

**Step 3: Insert into the changelog**

Add the entries under the appropriate `### <Type>` heading within
`## [Unreleased]`. If the heading doesn't exist yet, create it in the
canonical order: Added, Changed, Deprecated, Removed, Fixed, Security.

Never modify entries under a released version section.

---

### Mode 3 — Create a changelog from scratch

Use when no `CHANGELOG.md` exists, or when the user asks to "create a changelog"
or "initialize a changelog".

**Step 1: Determine project state**

- Check `pyproject.toml` (or `setup.py`) for the current version.
- Check git tags for previous releases.
- Check git log for notable changes.

**Step 2: Generate the file**

Start with this template:

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

```

If the project already has released versions (from git tags), add sections
for those versions with entries derived from commit messages between tags.
Clean up commit messages into proper changelog entries — do not dump raw
commit logs.

Add comparison links at the bottom of the file.

**Step 3: Present and confirm**

Show the generated changelog to the user for review before writing it to disk.

---

### Mode 4 — Prepare a release

Use when the user says "prepare a release", "bump the version", "release v1.2.0",
or "cut a release".

**Step 1: Determine the version bump**

Review the entries in `## [Unreleased]` and recommend a version bump
based on Semantic Versioning:

- **MAJOR** — if any entry describes a breaking API change, backward-incompatible
  change, or removal of public functionality.
- **MINOR** — if entries describe new features, additions, or non-breaking
  changes to existing functionality.
- **PATCH** — if entries describe only bug fixes, security patches, or
  documentation corrections with no API impact.

Present the recommendation and let the user confirm or override.

**Step 2: Update the changelog**

1. Replace `## [Unreleased]` with `## [x.y.z] - YYYY-MM-DD` using today's
   date in ISO 8601 format.
2. Add a new empty `## [Unreleased]` section above the new release.
3. Add/update the comparison link at the bottom of the file.

**Step 3: Update project metadata**

Update the `version` field in `pyproject.toml` (or `setup.py`, `setup.cfg`)
to match the new version. If the project uses a `__version__` variable in
`__init__.py`, update that too.

**Step 4: Present changes**

Show before/after diffs for:
- `CHANGELOG.md`
- `pyproject.toml` (or equivalent)
- Any `__version__` file

Wait for user approval before writing.

---

## What does NOT need a changelog entry

Not every change is user-visible. Skip changelog entries for:

- Internal refactors with no API or behavior change
- Comment-only or docstring-only changes
- CI/CD configuration changes (unless they affect users)
- Developer tooling changes (linter config, pre-commit hooks)
- Dependency version pin updates (unless they fix a user-facing bug)

If unsure, ask the user.

## Constraints

- **Never edit released sections.** Once a version is published, its changelog
  entries are immutable. If a correction is needed, add a note in the next release.
- **Always use ISO 8601 dates** — `YYYY-MM-DD`, never regional formats.
- **Changelogs are for humans, not machines.** Write clear, concise descriptions
  of what changed and why it matters. Do not paste commit hashes, PR numbers
  without context, or raw diff output.
- **One logical change per entry.** Do not combine "added feature X and fixed
  bug Y" in a single bullet.
- **Follow the project's existing conventions.** If the project already uses
  a specific entry format (e.g., bold file paths, module prefixes), match it.
  Only suggest format changes during an audit (Mode 1).

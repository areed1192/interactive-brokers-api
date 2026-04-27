---
name: python-logging-reviewer
description: >
  Audit, plan, and fix logging in any Python project. Use this skill whenever someone asks to
  review, audit, improve, fix, or standardize logging in a Python codebase. Trigger on phrases
  like "check my logging", "improve observability", "standardize log output", "add structured
  logging", "review my logging setup", "fix my logs", "logging best practices", or any request
  that involves evaluating or improving how a Python project logs. Also trigger when someone
  mentions replacing print() with proper logging, adding correlation IDs, or making logs
  machine-readable. Even if the user just says "my logs are a mess" or "I can't debug production",
  this skill applies.
---

# Python Logging Reviewer

This skill audits a Python project's logging implementation against industry best practices,
produces a prioritized improvement plan, and implements approved changes.

## Before you start

Read the best-practices reference file to ground your audit:

```
cat references/best-practices.md
```

Use the practices and source citations in that file as your authoritative checklist.
Do not invent rules — every finding you report should trace back to a named source
in the reference file.

## Workflow

Follow these four steps in order. Present the output of each step to the user and
wait for approval before moving to the next.

### Step 1 — Audit the codebase

Scan every Python file in the project. For each file, record:

1. **Logger instantiation** — How loggers are created. Flag any use of the root logger,
   hardcoded logger names, or `basicConfig()` called outside the entry point.
2. **Log levels** — Which levels are used and whether they match their semantic meaning.
   Flag DEBUG used for operational messages, WARNING used for expected behavior, etc.
3. **Format and structure** — Whether output is plain text or structured (JSON). Note the
   formatter class, fields included, and timestamp format.
4. **Exception handling** — Look for `except` blocks. Flag bare `except: pass`, exception
   handlers that log only the message string without `exc_info=True`, and duplicate
   exception logging across call layers.
5. **Lazy formatting** — Flag f-strings, `.format()`, or string concatenation inside log
   calls. These evaluate eagerly even when the log level is disabled.
6. **Missing logging** — Identify code paths with no logging: API/HTTP endpoints,
   database operations, retry loops, background tasks, signal handlers, and startup/shutdown.
7. **Output destination** — Flag hardcoded file paths in handlers. Note whether the project
   writes to stdout or manages its own log files.
8. **Security** — Flag any log call that could emit secrets, tokens, passwords, API keys,
   or PII. Look for logging of full request/response objects, auth headers, and
   database query parameters containing user data.
9. **Library vs. application** — If the project is a library (or contains library modules),
   check that those modules use `NullHandler` and do not call `basicConfig()`.
10. **Observability readiness** — Note whether logs include correlation/request IDs, whether
    OpenTelemetry is present, and whether log attribute names follow OTel semantic conventions.

Produce a markdown table summarizing all findings. Group by file, and include the line number,
the issue category (from the list above), a one-line description, and a severity tag:
**critical**, **recommended**, or **nice-to-have**.

Severity guidelines:
- **Critical** — Security risks (PII/secrets in logs), swallowed exceptions, missing
  error-path logging, root logger misuse in production code.
- **Recommended** — Eager formatting, inconsistent log levels, plain-text format in
  production, missing correlation IDs, hardcoded file destinations.
- **Nice-to-have** — Timestamp format improvements, OTel semantic convention alignment,
  adding DEBUG-level tracing to internal utilities.

### Step 2 — Recommendations with sources

For each finding from Step 1, recommend a concrete fix. Every recommendation must cite
the specific best practice it's based on. Use the source abbreviations defined in
`references/best-practices.md`:

- **[PY-HOWTO]** — Python logging HOWTO
- **[PY-COOKBOOK]** — Python Logging Cookbook
- **[PY-STDLIB]** — Python `logging` module docs
- **[12FACTOR]** — 12-Factor App, Factor XI (Logs)
- **[OTEL]** — OpenTelemetry Semantic Conventions
- **[SRE-BOOK]** — Google SRE Book, Ch. 6 (Monitoring Distributed Systems)
- **[SRE-WORKBOOK]** — Google SRE Workbook, Ch. 4 (Monitoring)
- **[REAL-PYTHON]** — Real Python logging best practices
- **[HITCHHIKER]** — The Hitchhiker's Guide to Python — Logging

Format each recommendation as:

```
### [severity] File: path/to/file.py, line N
**Finding:** <what's wrong>
**Fix:** <what to do>
**Source:** [SOURCE-TAG] — <one-sentence explanation of the cited practice>
```

### Step 3 — Implementation plan

Group the recommendations into logical PR-sized batches. A good grouping:

- **PR 1: Standardize logger initialization** — Switch all modules to
  `logging.getLogger(__name__)`, remove root logger usage, add `NullHandler` to
  library `__init__.py` files.
- **PR 2: Fix exception logging** — Add `exc_info=True` or switch to
  `logger.exception()` in all except blocks, remove bare `except: pass`.
- **PR 3: Add structured formatting** — Introduce a JSON formatter, configure it
  centrally, standardize timestamp to ISO 8601.
- **PR 4: Secure log output** — Add scrubbing filters for sensitive fields, remove
  logging of full request/auth objects.
- **PR 5: Fill logging gaps** — Add logging to unlogged code paths (API boundaries,
  retry loops, startup/shutdown).
- **PR 6: Observability alignment** — Add correlation IDs, align attribute names
  with OTel semantic conventions, integrate trace context if OTel is present.

Not every PR group will apply to every project. Skip groups that have no findings.
Add groups if the project has issues not covered above.

For each PR, list:
1. The files to change
2. A one-line summary of each change
3. The severity of the most critical finding in that PR
4. Estimated diff size (small / medium / large)

Present the plan and wait for user approval before implementing.

### Step 4 — Implement

After the user approves (they may approve all PRs or select specific ones), implement
the changes one PR-group at a time.

For each change:
- Show a before/after diff
- Explain in one sentence why the change matters
- Ensure the change does not alter application logic — only logging

After implementing each PR group, pause and let the user review before continuing.

## Constraints

These rules are non-negotiable:

- **Prefer stdlib `logging`** unless the project already uses `structlog`, `loguru`,
  or another library. Do not introduce a new logging library without asking.
- **Never change application logic.** Only add, fix, or restructure logging code.
- **Preserve existing log levels** unless the audit found a clear semantic mismatch.
- **Never log secrets, tokens, passwords, or PII.** If existing code does this,
  flag it as critical and fix it.
- **Do not remove existing log calls** unless they are duplicates or security risks.
  The goal is to improve coverage, not reduce it.

## Output format

- The audit report (Step 1) is a markdown table.
- The recommendations (Step 2) are structured markdown entries with source citations.
- The implementation plan (Step 3) is a numbered list grouped by PR.
- The implementation (Step 4) produces diffs with inline explanations.

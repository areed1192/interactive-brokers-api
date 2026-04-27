# Linting

All Python files must pass lint checks before work is considered complete.

## Tooling

This project uses **Ruff** for linting and import sorting. Project-level Ruff config lives in `pyproject.toml` under `[tool.ruff]` and `[tool.ruff.lint]` sections.

### Project-level config (`pyproject.toml`)

- **Max line length**: 120 characters
- **Target version**: `py310`
- **Selected rules**: `E` (pycodestyle errors), `F` (pyflakes), `W` (pycodestyle warnings), `I` (isort), `UP` (pyupgrade), `B` (bugbear), `SIM` (simplify)
- **Ignored rules**: `E501` (line too long — handled by formatter)

Do **not** modify the project-level config without good reason.

## Per-File Suppression

Use `# noqa: <CODE>` inline comments sparingly. The only accepted pattern:

| Suppress             | Where                                       | Why                                                       |
| -------------------- | ------------------------------------------- | --------------------------------------------------------- |
| `# noqa: E402`       | Test files with `sys.path` manipulation     | Imports must come after path setup for optional deps      |

Do **not** add blanket `# noqa` comments. Fix the underlying issue instead.

## Type Checking

This project uses **mypy** for type checking. Config lives in `pyproject.toml` under `[tool.mypy]`.

- `strict = false` — enabling incrementally
- `warn_return_any = true`, `warn_unused_configs = true`
- `ignore_missing_imports = true`
- Disabled error codes: `assignment`, `return-value`, `no-any-return`, `arg-type`, `union-attr` (legacy code — re-enable as types are fixed)

## Common Rules to Watch For

### Unused imports

- Remove any import that is not used in the file.
- `TYPE_CHECKING` imports are fine — they're used for type hints only.

### Line length

- Target **120 characters** per line (matching `line-length` in `pyproject.toml`). Break long strings, dict literals, and function signatures across multiple lines.

### Import ordering

- Ruff's `I` rule enforces isort-compatible ordering: standard library first, then third-party, then local `ibc.*` imports.
- Separate groups with a blank line.

```python
import logging
import time
from collections import deque

import requests
from urllib3.util.retry import Retry

from edgar.exceptions import EdgarRequestError
from edgar.parser import EdgarParser
```

### Type hints

- Use `from __future__ import annotations` at the top of modules that use `X | Y` union syntax.
- Use `TYPE_CHECKING` guard for imports only needed for type hints to avoid circular imports.

```python
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from edgar.session import EdgarSession
```

### f-string formatting

- Prefer f-strings over `.format()` or `%` formatting.
- Use `!r` for values that should show their repr: `f"Got: {value!r}"`.

## Validation Workflow

After completing any code change:

1. Check for lint errors in modified files using the editor's problem panel.
2. Fix all errors and warnings before committing.
3. If a new per-file disable is genuinely needed, document why in a comment.

## Files That Must Be Lint-Clean

- All files under `edgar/` (source code)
- All files under `tests/` (test code)
- Sample files under `samples/` are best-effort but should still be clean.

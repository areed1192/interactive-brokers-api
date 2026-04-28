# Contributing

Thanks for your interest in contributing to `ibc-api`! This guide covers
everything you need to get started.

## Requirements

- Python 3.10+
- Git

## Setup

```bash
# Clone the repository
git clone git@github.com:areed1192/interactive-brokers-api.git
cd interactive-brokers-api

# Install in editable mode with all dev dependencies
pip install -e ".[dev,async,docs]"
```

## Running Tests

```bash
python -m pytest tests/ --tb=short -q
```

All tests must pass before submitting a pull request.

## Linting

```bash
ruff check .
```

Line length is set to 120 characters.

## Building Documentation

```bash
mkdocs build --strict
mkdocs serve  # Preview at http://127.0.0.1:8000
```

## Project Structure

```
ibc/
├── client.py              # Main client entry point
├── session.py             # Synchronous HTTP session with retry/rate limiting
├── async_session.py       # Async HTTP session (httpx)
├── websocket.py           # WebSocket streaming client
├── models.py              # Typed dataclass response/request models
├── exceptions.py          # Custom exception hierarchy
├── rest/                  # REST service classes (one per API domain)
└── utils/                 # Auth, gateway, enums
samples/                   # Runnable usage examples
tests/                     # Unit tests (pytest)
docs/                      # MkDocs documentation source
```

## Contribution Guidelines

1. **Branch from `master`** — create a feature branch for your work.
2. **One logical change per PR** — don't combine unrelated changes.
3. **Add tests** — new features need unit tests in `tests/`.
4. **Add a sample** — user-facing features need an example in `samples/`.
5. **Update the changelog** — add entries under `## [Unreleased]` in `CHANGELOG.md`.
6. **Follow existing conventions** — match the style of surrounding code.

## Code Style

- Type hints on all public method signatures.
- `from __future__ import annotations` at the top of every module.
- Docstrings follow Google style.
- No `print()` in library code — use `logging.getLogger(__name__)`.
- Input validation at public API boundaries using `IBCValidationError`.

## Models

When adding a new API endpoint that returns structured data:

- Add a frozen dataclass to `ibc/models.py` with a `from_dict()` classmethod.
- For request bodies, add a `to_dict()` method.
- Return the model from the REST service method instead of a raw dict.

## Commit Signing

This project requires signed commits. Configure GPG signing:

```bash
git config commit.gpgsign true
git config user.signingkey YOUR_KEY_ID
```

## Questions?

Open an issue on [GitHub](https://github.com/areed1192/interactive-brokers-api/issues).

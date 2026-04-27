# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added

- **ibc/session.py**: Retry with exponential backoff on HTTP 429 responses using `tenacity`.
  - Configurable `max_retries`, `backoff_min`, `backoff_max` parameters on `InteractiveBrokersSession`.
- **ibc/session.py**: Token-bucket rate limiter (`TokenBucket`) to prevent API throttling.
  - Configurable `rate_limit` parameter (requests per second, default 10).
- **ibc/exceptions.py**: `IBCRateLimitError` exception for HTTP 429 responses.
- **ibc/models.py**: 20 typed response dataclasses generated from the IB API Swagger spec.
  - `AuthStatus`, `Account`, `Contract`, `SecdefInfo`, `Order`, `OrderStatus`, `OrderRequest`, `ModifyOrder`, `Trade`, `HistoryBar`, `HistoryData`, `MarketData`, `Position`, `Ledger`, `AlertCondition`, `AlertResponse`, `ScannerFilter`, `ScannerParams`, `ScannerContract`, `ScannerResult`, `Summary`, `Transaction`, `Transactions`, `SystemError`.
  - All models are frozen dataclasses with `from_dict()` class methods and sensible defaults.
  - Request models (`OrderRequest`, `ModifyOrder`, `ScannerParams`) include `to_dict()` for API serialization.
- **ibc/async_session.py**: Async REST session using `httpx` with retry on 429.
  - `AsyncInteractiveBrokersSession` with `async make_request()`, context manager support.
- **ibc/websocket.py**: WebSocket streaming client for real-time market data.
  - `IBWebSocketClient` with subscribe/unsubscribe for market data, orders, and account summary.
  - Async context manager and async iteration over incoming messages.
- **pyproject.toml**: Added `tenacity>=8.2` to core dependencies.
- **pyproject.toml**: Added `async` optional dependency group (`httpx>=0.27`, `websockets>=12.0`).
- **pyproject.toml**: Added `pytest-asyncio>=0.23` to dev dependencies.
- **tests/test_models.py**: 52 unit tests for all response model dataclasses.
- **tests/test_async_session.py**: 11 unit tests for async session.
- **tests/test_websocket.py**: 16 unit tests for WebSocket client.
- **tests/test_session.py**: 6 additional tests for retry/backoff and rate limiting.
- **samples/use_models.py**: New sample demonstrating typed model access for contracts, market data, historical bars, `OrderRequest.to_dict()`, `ScannerParams.to_dict()`, and portfolio positions/ledger.
- **.github/workflows/docs.yml**: GitHub Actions workflow to build and deploy MkDocs documentation to GitHub Pages on push to master.
- **docs/api/models.md**: API reference page for all response and request models.

- **README.md**: Complete rewrite with badges (Python versions, PyPI, license), Features table listing all 14 services, proper pip install instructions, and a concise quick-start example.
- **docs/**: MkDocs-based API reference documentation auto-generated from docstrings.
  - `mkdocs.yml` configuration with Material theme and `mkdocstrings[python]`.
  - 15 API reference pages (one per service) plus Getting Started guide.
- **pyproject.toml**: Added `docs` optional dependency group (`mkdocs`, `mkdocs-material`, `mkdocstrings[python]`).

### Changed

- **ibc/rest/orders.py**: `orders()` now returns `list[Order]` instead of a raw dict.
- **ibc/rest/accounts.py**: `accounts()` now returns `list[Account]` instead of a raw dict. Handles both dict and string account entries.
- **ibc/utils/auth.py**: `is_authenticated()`, `tickle()`, and `login()` now return `AuthStatus` model instead of raw dicts. `check_auth()` uses `AuthStatus.authenticated` internally.
- **ibc/__init__.py**: Added `__version__` via `importlib.metadata.version("ibc-api")`.
- **README.md**: Updated quick-start import to use `from ibc import InteractiveBrokersClient`.

### Added

- **samples/use_async_orders.py**: New sample demonstrating placing and monitoring an order using sync REST and async WebSocket together.

### Changed

- **ibc/rest/market_data.py**: `snapshot()`, `market_history()`, `market_history_beta()`, and `snapshot_beta()` now return typed models (`list[MarketData]`, `HistoryData`).
- **ibc/rest/orders.py**: `order_status()` now returns an `OrderStatus` model instead of a raw dict.
- **ibc/rest/alert.py**: `available_alerts()` now returns `list[AlertResponse]` and `alert_details()` returns `AlertResponse`.
- **ibc/rest/contract.py**: `contract_info()` now returns a `Contract` model and `secdef_info()` returns `list[SecdefInfo]`.
- **ibc/rest/portfolio.py**: `account_ledger()` now returns `dict[str, Ledger]` and `portfolio_positions()` returns `list[Position]`.
- **ibc/rest/portfolio_analysis.py**: `transactions_history()` now returns a `Transactions` model.
- **ibc/rest/scanner.py**: `run_scanner()` now returns a `ScannerResult` model.
- **ibc/rest/trades.py**: `trades()` now returns `list[Trade]`.
- **docs/index.md**: Quick start updated to demonstrate typed model access.
- **docs/getting-started.md**: Making Requests section rewritten to show typed responses and `OrderRequest.to_dict()`.
- **mkdocs.yml**: Added Models page to the navigation.
- **samples/*.py**: Polished all 14 sample files to follow project conventions.
  - Added module-level docstrings.
  - Added `# ---` section dividers between logical blocks.
  - Added inline `# Output: ...` comments showing expected response shapes.
  - Simplified boilerplate (removed redundant comments, used `wait_for_login()`).

### Fixed

- **README.md**: Fixed typo "plesfe" → correct link text, removed reference to nonexistent `requirements.txt`.
- **tests/test_market_data.py**: Fixed `test_converts_enum_bar` using wrong keyword `bar` instead of `market_bar` for `market_history_beta()`.
- **tests/test_alerts.py**: Updated assertions to verify `AlertResponse` model instances.
- **tests/test_contracts.py**: Updated assertions to verify `Contract` and `SecdefInfo` model instances.
- **tests/test_orders.py**: Updated assertions to verify `OrderStatus` model instance.
- **tests/test_market_data.py**: Updated assertions to verify `MarketData` and `HistoryData` model instances.

## [0.1.0] - 2026-04-27

### Added

- **ibc/utils/auth.py**: `tickle()` method — POST `/api/tickle` to keep the session alive.
  - `logout()` method — POST `/api/logout` to terminate the authenticated session.
- **ibc/rest/contract.py**: 8 new endpoint methods for expanded contract discovery.
  - `search_stocks(symbols)` — GET `/api/trsrv/stocks`.
  - `trading_schedule(asset_class, symbol, exchange)` — GET `/api/trsrv/secdef/schedule`.
  - `secdef_strikes(contract_id, sectype, month, exchange)` — GET `/api/iserver/secdef/strikes`.
  - `secdef_info(contract_id, sectype, month, exchange, strike, right)` — GET `/api/iserver/secdef/info`.
  - `contract_algos(contract_id, algos, add_description, add_params)` — GET `/api/iserver/contract/{conid}/algos`.
  - `contract_rules(contract_id, is_buy)` — POST `/api/iserver/contract/rules`.
  - `contract_info_and_rules(contract_id, is_buy)` — GET `/api/iserver/contract/{conid}/info-and-rules`.
  - `currency_pairs(currency)` — GET `/api/iserver/currency/pairs`.
- **ibc/rest/alert.py**: 4 new endpoint methods for alert management.
  - `create_or_modify_alert(account_id, alert)` — POST `/api/iserver/account/{account_id}/alert`.
  - `activate_alert(account_id, alert_id, activate)` — POST `/api/iserver/account/{account_id}/alert/activate`.
  - `delete_alert(account_id, alert_id)` — DELETE `/api/iserver/account/{account_id}/alert/{alert_id}`.
  - `alert_details(alert_id)` — GET `/api/iserver/account/alert/{alert_id}`.
- **ibc/rest/orders.py**: 3 new endpoint methods for order operations.
  - `order_status(order_id)` — GET `/api/iserver/account/order/status/{order_id}`.
  - `place_orders_for_fa_group(fa_group, orders)` — POST `/api/iserver/account/orders/{fa_group}`.
  - `place_whatif_orders(account_id, orders)` — POST `/api/iserver/account/{account_id}/orders/whatif`.
- **ibc/rest/market_data.py**: 5 new endpoint methods for market data operations.
  - `unsubscribe(contract_id)` — GET `/api/iserver/marketdata/{conid}/unsubscribe`.
  - `unsubscribe_all()` — GET `/api/iserver/marketdata/unsubscribeall`.
  - `market_history_beta(contract_id, period, bar, outside_regular_trading_hours)` — GET `/api/hmds/history`.
  - `snapshot_beta(contract_ids, fields)` — GET `/api/md/snapshot`.
  - `scanner_beta(scanner)` — POST `/api/hmds/scanner`.
- **ibc/rest/portfolio.py**: `subaccounts2(page)` method — GET `/api/portfolio/subaccounts2`.
- **ibc/rest/fyi.py**: New FYI notifications service with 12 endpoint methods.
  - `unread_number()`, `settings()`, `toggle_setting(typecode, enabled)`, `disclaimer(typecode)`, `accept_disclaimer(typecode)`, `delivery_options()`, `toggle_email_delivery(enabled)`, `toggle_device_delivery(device_id, enabled)`, `delete_device(device_id)`, `notifications(max_count, include_read)`, `more_notifications(notification_id)`, `mark_notification_read(notification_id)`.
- **ibc/client.py**: `fyi` property returning the `FYI` service instance.
- **tests/test_contracts.py**: 24 unit tests for all contract service methods.
- **tests/test_alerts.py**: 12 unit tests for all alert service methods.
- **tests/test_fyi.py**: 24 unit tests for all FYI service methods.
- **tests/test_auth.py**: 10 unit tests for authentication service methods.
- **tests/test_orders.py**: 6 new unit tests for order_status, place_orders_for_fa_group, place_whatif_orders.
- **tests/test_market_data.py**: 10 new unit tests for unsubscribe, unsubscribe_all, market_history_beta, snapshot_beta, scanner_beta.
- **tests/test_portfolio.py**: 2 new unit tests for subaccounts2.
- **samples/use_contracts.py**: Examples for search_stocks, trading_schedule, secdef_strikes, secdef_info, contract_algos, contract_rules, contract_info_and_rules, currency_pairs.
- **samples/use_alerts.py**: Examples for create_or_modify_alert, activate_alert, alert_details, delete_alert.
- **samples/use_orders.py**: Examples for order_status, place_orders_for_fa_group, place_whatif_orders.
- **samples/use_market_data.py**: Examples for unsubscribe, unsubscribe_all, market_history_beta, snapshot_beta, scanner_beta.
- **samples/use_fyi.py**: New sample file demonstrating the FYI notifications service.

### Fixed

- **tests/test_market_data.py**: Fixed `test_converts_enum_bar_to_value` using wrong keyword argument `bar` instead of `market_bar`.


  - `IBCError` base exception for all IB API client errors.
  - `IBCRequestError` with `status_code`, `url`, `method`, and `response_body` attributes.
  - `IBCAuthenticationError` for gateway and login failures.
  - `IBCValidationError` for input validation failures.
- **ibc/__init__.py**: Package init with explicit `__all__` exports for `InteractiveBrokersClient`, `InteractiveBrokersSession`, and all exception classes.
- **ibc/rest/__init__.py**: Subpackage init with `__all__` exporting all 12 REST service classes.
- **ibc/utils/__init__.py**: Subpackage init with `__all__` exporting auth, gateway, and enum modules.
- **ibc/py.typed**: PEP 561 marker file for type information distribution.
- **ibc/utils/auth.py**: `wait_for_login(timeout=300, poll_interval=3)` method that polls the gateway for authentication with configurable timeout, replacing manual busy-wait loops in callers.
- **ibc/utils/auth.py**: `_is_already_running_unix()` method using `pgrep` for Linux/macOS gateway process detection.
- **tests/conftest.py**: Shared pytest fixtures (`mock_client`, `mock_session`) for offline testing without live credentials or gateway download.
- **tests/test_client.py**: 18 unit tests for `InteractiveBrokersClient` initialization and service properties.
- **tests/test_session.py**: 16 unit tests for `InteractiveBrokersSession` URL building, headers, and request handling.
  - Added 3 new tests: `__repr__`, empty-body success response, invalid method validation, and case-insensitive method dispatch (19 total).
- **tests/test_accounts.py**: 4 unit tests for `Accounts` service methods.
- **tests/test_orders.py**: 10 unit tests for `Orders` service methods including place, modify, and cancel flows.
- **tests/test_market_data.py**: 13 unit tests for `MarketData` service methods.
- **tests/test_portfolio.py**: 18 unit tests for `Portfolio` service methods.
- **tests/test_gateway.py**: 21 unit tests for `ClientPortalGateway` covering download, zip validation, extraction, path traversal rejection, and setup orchestration.
- **pyproject.toml**: PEP 621 project metadata replacing legacy `setup.py`. Includes `requires-python >= 3.10`, Python 3.10–3.13 classifiers, unpinned `requests>=2.33.1` and `fake-useragent>=2.2.0`, and dev extras with `pytest>=7` and `pylint`.
- **.github/dependabot.yml**: Weekly automated dependency updates for pip.
- **README.md**: SSL Certificates section explaining self-signed certs, `verify_ssl=False` default, and steps for custom certificate configuration.

### Changed

- **ibc/utils/gateway.py**: Rewrote `ClientPortalGateway` for resilience and security.
  - Added zip path traversal validation (`_validate_zip_entries`) to prevent zip-slip attacks.
  - Fixed extraction path to use `self._gateway_folder` instead of a hardcoded relative string.
  - Added `timeout=60` and `raise_for_status()` to the download request.
  - Wrapped download and zip parsing errors in `IBCError` with descriptive messages.
  - Replaced folder-existence check with marker-file check (`bin/run.bat` or `bin/run.sh`) to detect incomplete installs.
  - Made download URL configurable via `download_url` parameter.
  - Added `__repr__` for debugging.
  - Removed unused `textwrap` import.
- **ibc/utils/auth.py**: Rewrote authentication and gateway management for cross-platform support and robustness.
  - `login()` now checks if already authenticated before restarting the gateway, attempts reauthentication, and falls back to browser login.
  - `_startup_gateway()` uses `client.client_portal._gateway_folder` instead of hardcoded relative path; supports Linux/macOS via `bash bin/run.sh`.
  - `_is_already_running()` delegates to platform-specific methods; handles empty output, subprocess timeouts, and `OSError`.
  - `close_gateway()` raises `IBCAuthenticationError` when no PID is available; uses `kill` on Linux/macOS.
  - `check_auth()` uses `response.get("authenticated")` instead of `response["authenticated"] == True`.
  - Replaced broad `except Exception` with `except (IBCRequestError, requests.RequestException)`.
  - Added explicit `check=False` to all `subprocess.run` calls.
  - Removed unused `_use_selenium` parameter from `login()`.
  - Removed unused `check` parameter from `is_authenticated()`.
  - Removed unused `requests` import (replaced with targeted `IBCRequestError` import).
  - Added `_GATEWAY_LOGIN_URL` constant to replace scattered URL strings.
  - Added `update_server_account()` input validation via `IBCValidationError`.
- **ibc/session.py**: Rewrote session to use persistent `requests.Session` for connection pooling and cookie handling.
  - Replaced standalone `requests.get/post/delete` calls with `session.request(method=...)`, eliminating the if/elif dispatch chain.
  - Removed dead code: second `elif` branch (`len(content) > 0 and response.ok`) was unreachable (identical condition to first `if`).
  - Removed fragile `/api/iserver/account` special-case that silently returned errors as JSON instead of raising `IBCRequestError`.
  - Moved `UserAgent().edge` generation from per-request `build_headers()` to `__init__`, eliminating repeated `fake_useragent` calls.
  - Removed `build_headers()` method — headers now live on the persistent session.
  - Added HTTP method validation against a `_VALID_METHODS` set with a clear `ValueError`.
  - Method parameter is now case-insensitive.
  - Narrowed `except Exception` in JSON parsing to `except (ValueError, requests.JSONDecodeError)`.
  - Made SSL verification configurable via `verify_ssl` parameter (default `False` for localhost gateway).
  - Replaced `logging.basicConfig()` with `logger = logging.getLogger(__name__)` — libraries must not configure the root logger.
  - Demoted response body logging from `info` to `debug`.
  - Added `__repr__` for debugging.
- **ibc/client.py**: Improved client initialization and API consistency.
  - `session` is now a `@property` instead of a method, matching all other service accessors.
  - Added `__repr__` for debugging.
- **ibc/rest/data.py**: Fixed copy-paste bug where `news_sources()` hit `/api/iserver/news/top` instead of the correct endpoint.
- **ibc/rest/portfolio_analysis.py**: Fixed copy-paste bug where `transactions_history()` posted to `/api/pa/summary` instead of `/api/pa/transactions`.
- **ibc/rest/orders.py**: Fixed copy-paste bug where `modify_order()` ignored the `order_id` parameter in the endpoint URL.
- **ibc/rest/contract.py**: Fixed type hint bug where `search_symbol(name: str = False)` had a `bool` default with `str` annotation.
- **ibc/rest/*.py**: Added `from __future__ import annotations`, `TYPE_CHECKING` guard for `InteractiveBrokersClient`, `__repr__`, and input validation (`_validate_id`) across all 12 REST service classes.
- **ibc/rest/market_data.py**: Removed `__init__()` side-effect that called the accounts endpoint on instantiation.
- **ibc/rest/pnl.py**: Removed duplicate `pnl_server_account()` — consolidated into `Accounts` service only.
- **samples/*.py**: Replaced manual `while not authenticated` busy-wait loops with `auth_service.wait_for_login()` across all 9 sample files.
- **.github/workflows/python-package.yml**: Updated to `actions/checkout@v4` and `actions/setup-python@v5`, Python 3.10–3.13 matrix, fixed test filename typo.
- **.github/workflows/python-publish.yml**: Updated actions and switched to OIDC Trusted Publishers.

### Removed

- **ibc/session.py**: Removed `build_headers()` method — headers are now set once on the persistent session.
- **ibc/rest/market_data.py**: Removed `print()` statement from library code.
- **ibc/utils/auth.py**: Removed `print()` statements from library code.
- **ibc/utils/gateway.py**: Removed `print()` statements and unused `textwrap` import from library code.

# Python Logging Best Practices Reference

This file is the authoritative checklist for the python-logging-reviewer skill.
Every audit finding must trace back to a practice listed here. Each practice includes
a source tag used for citations in the recommendation output.

## Source abbreviations

| Tag             | Source                                                            |
|-----------------|-------------------------------------------------------------------|
| [PY-HOWTO]      | Python docs — Logging HOWTO (docs.python.org/3/howto/logging)     |
| [PY-COOKBOOK]    | Python docs — Logging Cookbook (docs.python.org/3/howto/logging-cookbook) |
| [PY-STDLIB]     | Python docs — `logging` module reference                          |
| [12FACTOR]      | The Twelve-Factor App — Factor XI: Logs (12factor.net/logs)       |
| [OTEL]          | OpenTelemetry Semantic Conventions (opentelemetry.io/docs/specs/semconv) |
| [SRE-BOOK]      | Google SRE Book, Ch. 6: Monitoring Distributed Systems            |
| [SRE-WORKBOOK]  | Google SRE Workbook, Ch. 4: Monitoring                            |
| [REAL-PYTHON]   | Real Python — logging best practices (realpython.com/ref/best-practices/logging) |
| [HITCHHIKER]    | The Hitchhiker's Guide to Python — Logging (docs.python-guide.org/writing/logging) |

---

## 1. Logger Instantiation

### 1.1 Use `__name__` for all loggers
Create one logger per module with `logging.getLogger(__name__)`. This produces a
hierarchy that mirrors the package structure, avoids name collisions, and lets you
configure logging per-module or per-package.

**Why it matters:** Using hardcoded names or the root logger makes it impossible to
selectively enable/disable logging for specific parts of the application.

**Anti-patterns to flag:**
- `logging.getLogger()` with no argument (returns root logger)
- `logging.getLogger("my_app")` with a hardcoded string instead of `__name__`
- `logging.info(...)` / `logging.debug(...)` (module-level functions use the root logger)

**Source:** [PY-HOWTO], [REAL-PYTHON], [HITCHHIKER]

### 1.2 Configure logging once at the entry point
Call `basicConfig()`, `dictConfig()`, or `fileConfig()` exactly once in the
`if __name__ == "__main__"` block, a CLI entry point, or a dedicated config module.
Never configure logging inside imported modules.

**Why it matters:** Multiple `basicConfig()` calls are silently ignored after the first,
leading to confusion. Configuration in imported modules creates unpredictable side effects
that depend on import order.

**Anti-patterns to flag:**
- `basicConfig()` called in a library module or utility file
- Multiple `basicConfig()` calls across the codebase
- Logging configuration scattered across many files
- Handler creation inside class `__init__` methods

**Source:** [PY-HOWTO], [REAL-PYTHON]

### 1.3 Libraries must use NullHandler only
If the project is a library (or contains reusable modules), the library's `__init__.py`
should contain only:
```python
import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())
```
Libraries must never call `basicConfig()`, attach file/stream handlers, or set log levels.
The consuming application decides how logs are handled.

**Why it matters:** A library that configures logging forces its opinions on every
application that imports it, potentially conflicting with the application's own config.

**Source:** [PY-HOWTO], [HITCHHIKER], [REAL-PYTHON]

---

## 2. Log Levels

### 2.1 Use levels according to their semantic meaning
- **DEBUG** — Detailed diagnostic information useful only during active debugging.
  Should be disabled in production.
- **INFO** — Confirmation that things are working as expected. Routine operational events.
- **WARNING** — Something unexpected happened, or a potential problem is approaching
  (e.g., disk space low), but the application is still functioning.
- **ERROR** — A specific operation failed. The application could not perform a function.
- **CRITICAL** — A serious error indicating the application itself may be unable to
  continue running.

**Anti-patterns to flag:**
- Using WARNING for expected code paths (e.g., cache misses)
- Using ERROR for validation failures that are normal user input
- Using INFO for detailed diagnostic data that should be DEBUG
- Using CRITICAL for recoverable errors

**Source:** [PY-HOWTO], [REAL-PYTHON]

### 2.2 Do not define custom log levels
Python's five built-in levels cover virtually all use cases. Custom levels create conflicts
when multiple libraries define overlapping numeric values, and they confuse log aggregation
tools that expect the standard set.

**Source:** [PY-HOWTO]

### 2.3 Support environment-driven level configuration
Log level should be configurable via environment variable or config file, not hardcoded.
Use DEBUG in development and INFO or higher in production. This aligns with the
12-Factor App principle that configuration belongs in the environment.

**Source:** [12FACTOR], [SRE-WORKBOOK]

---

## 3. Log Format and Structure

### 3.1 Use structured logging (JSON) in production
Plain-text logs are difficult to parse, query, and aggregate at scale. Structured JSON
logs make every field independently queryable by log aggregation tools (ELK, Datadog,
Splunk, etc.).

**Minimum fields for a structured log record:**
- `timestamp` (ISO 8601 format, e.g., `2026-04-19T14:30:00.123Z`)
- `level` (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `logger` (the logger name, typically the module path)
- `message` (the human-readable log message)
- `module`, `function`, `line` (code location)

**Implementation options:**
- Custom `logging.Formatter` subclass that outputs JSON
- `python-json-logger` library
- `structlog` (if the project already uses it or is adopting it)

**Anti-patterns to flag:**
- Plain-text formatters in production configuration
- Inconsistent format strings across different handlers
- Missing timestamps or non-ISO timestamp formats

**Source:** [SRE-WORKBOOK], [OTEL], [12FACTOR]

### 3.2 Include contextual fields
Log records should include enough context to trace an event back to its origin:
- **Correlation/request ID** — A unique ID that follows a request across all log entries
  it generates. Essential for debugging in multi-threaded or async applications.
- **User/session identifiers** — When appropriate and not a PII risk.
- **Operation identifiers** — Task IDs, job names, transaction IDs.

Use Python's `extra` parameter, `LoggerAdapter`, or `structlog`'s context binding
to attach these fields without polluting log call sites.

**Source:** [PY-COOKBOOK], [OTEL], [SRE-WORKBOOK]

### 3.3 Use consistent field names across services
If the project contains multiple services, use the same field names for the same concepts.
OpenTelemetry semantic conventions provide a ready-made vocabulary:
- `service.name`, `service.version`
- `deployment.environment`
- `trace_id`, `span_id`

**Source:** [OTEL]

---

## 4. Exception Logging

### 4.1 Always log exceptions with tracebacks
Inside `except` blocks, use `logger.exception("message")` (which automatically attaches
`exc_info=True`) or explicitly pass `exc_info=True` to the log call. The traceback is
essential for diagnosing the root cause.

**Anti-patterns to flag:**
- `logger.error(str(e))` — Loses the traceback and exception type.
- `logger.error(f"Failed: {e}")` — Same problem plus eager formatting.
- `except Exception: pass` — Swallows the exception entirely with no record.
- `except Exception as e: print(e)` — Uses print instead of logging.

**Source:** [PY-HOWTO], [REAL-PYTHON]

### 4.2 Log exceptions at the right layer
Log an exception once at the layer that handles it, not at every layer it passes through.
If a function re-raises an exception, it should not also log it — that creates duplicate
noise. The handler (the `except` block that actually recovers or terminates) is the
right place to log.

**Source:** [PY-COOKBOOK]

---

## 5. Lazy Formatting

### 5.1 Use %-style formatting in log calls
```python
# CORRECT — lazy evaluation, string is only built if level is enabled
logger.info("User %s performed action %s", user_id, action)

# WRONG — f-string always evaluates, even if INFO is disabled
logger.info(f"User {user_id} performed action {action}")

# WRONG — concatenation always evaluates
logger.info("User " + str(user_id) + " performed action " + action)

# WRONG — .format() always evaluates
logger.info("User {} performed action {}".format(user_id, action))
```

**Why it matters:** In high-throughput code paths, eager string construction for
disabled log levels wastes CPU. The %-style defers formatting to the logging framework,
which skips it entirely if the level is not active.

**Source:** [PY-HOWTO], [REAL-PYTHON]

---

## 6. Output Destination

### 6.1 Log to stdout, not files
Applications should write logs to stdout (or stderr for errors) and let the execution
environment (Docker, Kubernetes, systemd, a log router like Fluentd) handle collection,
routing, and storage.

**Why it matters:** Hardcoded file paths couple the application to its deployment
environment. In containerized or cloud-native deployments, the filesystem is ephemeral
and logs written to files may be lost. Writing to stdout is simpler, more portable,
and compatible with every log aggregation system.

**Anti-patterns to flag:**
- `FileHandler` or `RotatingFileHandler` in production config
- Hardcoded paths like `/var/log/app.log`
- Application code that manages log rotation

**Exception:** `RotatingFileHandler` is acceptable in development-only config or in
scripts that explicitly need local log files. The skill should note the context before
flagging.

**Source:** [12FACTOR]

### 6.2 Do not buffer or batch logs internally
Applications should not accumulate logs in memory and periodically flush them to a
database or external service. This creates coupling, adds failure modes, and risks
data loss if the application crashes before flushing.

**Source:** [12FACTOR]

---

## 7. Security

### 7.1 Never log secrets, tokens, passwords, or PII
Log calls must not include:
- Passwords or password hashes
- API keys, tokens, or secrets
- Credit card numbers or SSNs
- Email addresses, phone numbers, or other PII (unless explicitly required and scrubbed
  in the logging pipeline)
- Full HTTP request/response bodies that may contain auth headers
- Database query parameters that contain user data

**Implementation strategies:**
- Avoid logging entire objects — log only specific, safe fields.
- Implement a custom `logging.Filter` that scrubs or masks known sensitive field names
  (e.g., `password`, `token`, `authorization`, `secret`, `ssn`, `credit_card`).
- Use structured logging with a field allow-list rather than a block-list.
- In OpenTelemetry pipelines, add a log processor to scrub sensitive attributes before export.

**Source:** [SRE-BOOK], [OTEL], [12FACTOR]

### 7.2 Sanitize database queries in logs
If logging SQL queries, strip or parameterize values. Log the query template
(`SELECT * FROM users WHERE id = ?`) rather than the filled query
(`SELECT * FROM users WHERE id = 12345`).

**Source:** [OTEL]

---

## 8. Performance

### 8.1 Do not log in tight loops
Logging inside a loop that executes thousands or millions of times per second can
bottleneck the application on I/O. If loop-level visibility is needed, log a summary
after the loop completes, or use sampling.

**Source:** [PY-COOKBOOK], [SRE-WORKBOOK]

### 8.2 Use QueueHandler for async or high-throughput applications
`QueueHandler` moves log I/O off the hot path by writing log records to an in-memory
queue. A `QueueListener` in a background thread drains the queue and forwards records
to the actual handlers. This prevents logging from blocking request processing.

**Source:** [PY-COOKBOOK]

### 8.3 Do not create handlers inside loops or functions
Creating a new `FileHandler` or `StreamHandler` on every function call or loop iteration
leaks memory and produces duplicate log output. Handlers should be created once during
configuration.

**Source:** [PY-STDLIB]

---

## 9. Observability and Monitoring

### 9.1 Align with the Four Golden Signals
Google's SRE book identifies four signals essential for monitoring any service:
latency, traffic, errors, and saturation. Logging should support all four:
- **Latency** — Log request duration at INFO level for completed requests.
- **Traffic** — Log request counts or use metrics; don't use log lines as a substitute
  for counters.
- **Errors** — Log all errors with tracebacks, error codes, and context.
- **Saturation** — Log resource warnings (queue depth, connection pool exhaustion,
  memory pressure) at WARNING level.

**Source:** [SRE-BOOK]

### 9.2 Use OpenTelemetry semantic conventions for attribute names
When adding structured fields to logs, prefer OTel's standard attribute names:
- `service.name`, `service.version`, `deployment.environment`
- `http.method`, `http.route`, `http.status_code`
- `db.system`, `db.name`, `db.operation`
- `exception.type`, `exception.message`, `exception.stacktrace`

This ensures logs can be correlated with traces and metrics in any OTel-compatible
backend without custom mapping.

**Source:** [OTEL]

### 9.3 Inject trace context into logs
If the project uses OpenTelemetry (or any distributed tracing system), configure the
logging integration to automatically inject `trace_id` and `span_id` into every log
record. This enables one-click correlation between a log entry and the distributed
trace that produced it.

**Source:** [OTEL], [SRE-WORKBOOK]

### 9.4 Prefer metrics over log-line counting
Do not use log lines as a substitute for metrics. Counting log lines for rates and
volumes is expensive, fragile, and scales poorly. Use a proper metrics system
(Prometheus, OpenTelemetry Metrics, StatsD) for quantitative signals. Logs are for
context and narrative; metrics are for numbers.

**Source:** [SRE-BOOK], [SRE-WORKBOOK]

---

## 10. Code Patterns to Scan For

This section provides grep-able patterns the skill should use during the audit.

### Definite anti-patterns (always flag)
```
logging.info(          # Root logger usage (module-level functions)
logging.debug(
logging.warning(
logging.error(
logging.critical(
except:                # Bare except (no exception type)
except Exception: pass # Swallowed exception (when combined with no logging)
except.*pass           # Swallowed exception variant
f".*logger            # f-string in log call
.format(.*logger      # .format() in log call
password              # Potential secret in log message (inspect context)
token                 # Potential secret in log message (inspect context)
secret                # Potential secret in log message (inspect context)
api_key               # Potential secret in log message (inspect context)
```

### Patterns that need context (flag only if misused)
```
basicConfig(           # Fine in entry point, bad in library modules
FileHandler(           # Fine in dev config, bad in production config
print(                 # Fine in CLI output, bad as a substitute for logging
```

### Patterns that indicate good practice (note approvingly)
```
getLogger(__name__)    # Correct logger instantiation
NullHandler()          # Correct library pattern
exc_info=True          # Correct exception logging
logger.exception(      # Correct exception logging
dictConfig(            # Centralized configuration
QueueHandler(          # Performance-conscious logging
```

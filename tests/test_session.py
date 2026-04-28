"""Tests for the InteractiveBrokersSession."""

from unittest.mock import MagicMock, patch

import pytest
import requests

from ibc.exceptions import IBCAuthenticationError, IBCRateLimitError, IBCRequestError
from ibc.session import InteractiveBrokersSession, TokenBucket

# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------

SAMPLE_RESPONSE_JSON = {"status": "ok", "data": [1, 2, 3]}

SAMPLE_ERROR_RESPONSE_JSON = {
    "error": "Bad Request",
    "statusCode": 400,
}


# ---------------------------------------------------------------------------
# InteractiveBrokersSession init tests
# ---------------------------------------------------------------------------


class TestInteractiveBrokersSessionInit:
    """Tests for InteractiveBrokersSession initialization."""

    def test_stores_client_reference(self, mock_session, mock_client):
        """Verify the session stores a reference to the client."""
        assert mock_session.client is mock_client

    def test_default_verify_ssl_is_false(self, mock_session):
        """Verify SSL verification defaults to False."""
        assert mock_session.verify_ssl is False

    def test_verify_ssl_can_be_enabled(self, mock_client):
        """Verify SSL verification can be set to True."""
        with patch("ibc.session.UserAgent"):
            session = InteractiveBrokersSession(ib_client=mock_client, verify_ssl=True)
        assert session.verify_ssl is True

    def test_default_resource_url(self, mock_session):
        """Verify the default resource URL points to localhost."""
        assert mock_session.resource_url == "https://localhost:5000/v1"

    def test_creates_requests_session(self, mock_session):
        """Verify a persistent requests.Session is created."""
        assert isinstance(mock_session._session, requests.Session)

    def test_session_verify_matches_verify_ssl(self, mock_session):
        """Verify the internal session's verify flag matches verify_ssl."""
        assert mock_session._session.verify is False

    def test_repr(self, mock_session):
        """Verify __repr__ output."""
        result = repr(mock_session)
        assert "InteractiveBrokersSession" in result
        assert "localhost:5000" in result


# ---------------------------------------------------------------------------
# build_url tests
# ---------------------------------------------------------------------------


class TestBuildUrl:
    """Tests for the build_url method."""

    def test_builds_full_url(self, mock_session):
        """Verify build_url concatenates base URL and endpoint."""
        url = mock_session.build_url("/api/iserver/accounts")
        assert url == "https://localhost:5000/v1/api/iserver/accounts"

    def test_builds_url_with_empty_endpoint(self, mock_session):
        """Verify build_url works with an empty endpoint."""
        url = mock_session.build_url("")
        assert url == "https://localhost:5000/v1"


# ---------------------------------------------------------------------------
# make_request tests
# ---------------------------------------------------------------------------


class TestMakeRequest:
    """Tests for the make_request method."""

    def _mock_response(self, status_code=200, json_data=None, content=b"data", ok=True):
        """Helper to create a mock response object."""
        mock_resp = MagicMock(spec=requests.Response)
        mock_resp.status_code = status_code
        mock_resp.ok = ok
        mock_resp.content = content
        mock_resp.text = str(json_data) if json_data else ""
        mock_resp.json.return_value = json_data or {}
        mock_resp.url = "https://localhost:5000/v1/test"
        mock_resp.request = MagicMock()
        mock_resp.request.headers = {"Content-Type": "application/json"}
        mock_resp.request.method = "GET"
        return mock_resp

    def test_get_request_returns_json(self, mock_session):
        """Verify GET request returns parsed JSON on success."""
        mock_session._session.request = MagicMock(return_value=self._mock_response(json_data=SAMPLE_RESPONSE_JSON))

        result = mock_session.make_request(method="get", endpoint="/api/test")

        assert result == SAMPLE_RESPONSE_JSON

    def test_post_request_sends_json_payload(self, mock_session):
        """Verify POST request forwards json_payload correctly."""
        mock_session._session.request = MagicMock(return_value=self._mock_response(json_data=SAMPLE_RESPONSE_JSON))
        payload = {"key": "value"}

        mock_session.make_request(method="post", endpoint="/api/test", json_payload=payload)

        _, kwargs = mock_session._session.request.call_args
        assert kwargs["json"] == payload

    def test_delete_request_calls_correct_method(self, mock_session):
        """Verify DELETE request uses the delete method."""
        mock_session._session.request = MagicMock(return_value=self._mock_response(json_data={}))

        mock_session.make_request(method="delete", endpoint="/api/test")

        _, kwargs = mock_session._session.request.call_args
        assert kwargs["method"] == "delete"

    def test_passes_verify_ssl_to_session(self, mock_session):
        """Verify the verify_ssl flag is set on the internal session."""
        assert mock_session._session.verify is False

    def test_error_response_raises_ibc_request_error(self, mock_session):
        """Verify non-ok responses raise IBCRequestError."""
        mock_session._session.request = MagicMock(
            return_value=self._mock_response(
                status_code=400,
                ok=False,
                json_data=SAMPLE_ERROR_RESPONSE_JSON,
            )
        )

        with pytest.raises(IBCRequestError):
            mock_session.make_request(method="get", endpoint="/api/test")

    def test_error_response_with_empty_content(self, mock_session):
        """Verify error handling works when response body is empty."""
        mock_session._session.request = MagicMock(
            return_value=self._mock_response(
                status_code=500,
                ok=False,
                content=b"",
            )
        )

        with pytest.raises(IBCRequestError):
            mock_session.make_request(method="get", endpoint="/api/test")

    def test_error_with_non_json_body_falls_back_to_text(self, mock_session):
        """Verify non-JSON error response falls back to text content."""
        mock_resp = self._mock_response(status_code=500, ok=False, content=b"Server Error")
        mock_resp.json.side_effect = ValueError("No JSON")
        mock_resp.text = "Server Error"
        mock_session._session.request = MagicMock(return_value=mock_resp)

        with pytest.raises(IBCRequestError):
            mock_session.make_request(method="get", endpoint="/api/test")

    def test_ok_response_with_empty_content(self, mock_session):
        """Verify ok response with empty body returns success message."""
        mock_session._session.request = MagicMock(
            return_value=self._mock_response(status_code=200, ok=True, content=b"")
        )

        result = mock_session.make_request(method="get", endpoint="/api/test")

        assert result["message"] == "response successful"
        assert result["status_code"] == 200

    def test_invalid_method_raises_value_error(self, mock_session):
        """Verify unsupported HTTP method raises ValueError."""
        with pytest.raises(ValueError, match="Unsupported HTTP method"):
            mock_session.make_request(method="OPTIONS", endpoint="/api/test")

    def test_method_is_case_insensitive(self, mock_session):
        """Verify method is lowercased before dispatch."""
        mock_session._session.request = MagicMock(return_value=self._mock_response(json_data=SAMPLE_RESPONSE_JSON))

        result = mock_session.make_request(method="GET", endpoint="/api/test")

        assert result == SAMPLE_RESPONSE_JSON


# ---------------------------------------------------------------------------
# Retry / Rate Limit tests
# ---------------------------------------------------------------------------


class TestRetryBehavior:
    """Tests for retry and rate-limit behavior in make_request."""

    def _mock_response(self, status_code=200, json_data=None, content=b"data", ok=True):
        """Helper to create a mock response object."""
        mock_resp = MagicMock(spec=requests.Response)
        mock_resp.status_code = status_code
        mock_resp.ok = ok
        mock_resp.content = content
        mock_resp.text = str(json_data) if json_data else ""
        mock_resp.json.return_value = json_data or {}
        mock_resp.url = "https://localhost:5000/v1/test"
        mock_resp.request = MagicMock()
        mock_resp.request.headers = {"Content-Type": "application/json"}
        mock_resp.request.method = "GET"
        return mock_resp

    def test_retries_on_429_then_succeeds(self, mock_session):
        """Verify request retries on 429 and succeeds on subsequent attempt."""
        rate_limit_resp = self._mock_response(status_code=429, ok=False)
        success_resp = self._mock_response(json_data=SAMPLE_RESPONSE_JSON)

        mock_session._session.request = MagicMock(side_effect=[rate_limit_resp, success_resp])

        result = mock_session.make_request(method="get", endpoint="/api/test")

        assert result == SAMPLE_RESPONSE_JSON
        assert mock_session._session.request.call_count == 2

    def test_raises_rate_limit_error_after_max_retries(self, mock_client):
        """Verify IBCRateLimitError is raised after exhausting retries."""
        with patch("ibc.session.UserAgent") as mock_ua:
            mock_ua.return_value.edge = "MockUserAgent/1.0"
            session = InteractiveBrokersSession(
                ib_client=mock_client, max_retries=2, backoff_min=0.01, backoff_max=0.02
            )

        rate_limit_resp = MagicMock(spec=requests.Response)
        rate_limit_resp.status_code = 429
        rate_limit_resp.ok = False
        rate_limit_resp.content = b""
        rate_limit_resp.url = "https://localhost:5000/v1/test"
        rate_limit_resp.request = MagicMock()
        rate_limit_resp.request.method = "GET"

        session._session.request = MagicMock(return_value=rate_limit_resp)

        with pytest.raises(IBCRateLimitError):
            session.make_request(method="get", endpoint="/api/test")

    def test_non_429_error_not_retried(self, mock_session):
        """Verify non-429 errors are raised immediately without retry."""
        error_resp = self._mock_response(status_code=500, ok=False, json_data={"error": "fail"})

        mock_session._session.request = MagicMock(return_value=error_resp)

        with pytest.raises(IBCRequestError):
            mock_session.make_request(method="get", endpoint="/api/test")

        assert mock_session._session.request.call_count == 1

    def test_custom_retry_settings(self, mock_client):
        """Verify custom max_retries and backoff settings are stored."""
        with patch("ibc.session.UserAgent") as mock_ua:
            mock_ua.return_value.edge = "MockUserAgent/1.0"
            session = InteractiveBrokersSession(ib_client=mock_client, max_retries=5, backoff_min=2.0, backoff_max=30.0)
        assert session.max_retries == 5
        assert session.backoff_min == 2.0
        assert session.backoff_max == 30.0


# ---------------------------------------------------------------------------
# TokenBucket tests
# ---------------------------------------------------------------------------


class TestTokenBucket:
    """Tests for the TokenBucket rate limiter."""

    def test_acquire_does_not_block_under_capacity(self):
        """Verify acquire returns immediately when tokens are available."""
        bucket = TokenBucket(rate=100.0)
        # Should not block
        bucket.acquire()
        bucket.acquire()
        bucket.acquire()

    def test_rate_property(self):
        """Verify the rate is stored correctly."""
        bucket = TokenBucket(rate=5.0, capacity=10.0)
        assert bucket._rate == 5.0
        assert bucket._capacity == 10.0


# ---------------------------------------------------------------------------
# Connection health monitoring tests
# ---------------------------------------------------------------------------


class TestConnectionHealthMonitoring:
    """Tests for gateway connection error handling."""

    def test_connection_error_raises_authentication_error(self, mock_session):
        """Verify ConnectionError is wrapped in IBCAuthenticationError."""
        mock_session._session.request = MagicMock(side_effect=requests.ConnectionError("Connection refused"))

        with pytest.raises(IBCAuthenticationError, match="Unable to connect"):
            mock_session.make_request(method="get", endpoint="/api/test")

    def test_connection_error_message_includes_url(self, mock_session):
        """Verify the error message includes the target URL."""
        mock_session._session.request = MagicMock(side_effect=requests.ConnectionError("Connection refused"))

        with pytest.raises(IBCAuthenticationError, match="localhost:5000"):
            mock_session.make_request(method="get", endpoint="/api/test")

    def test_connection_error_preserves_original_exception(self, mock_session):
        """Verify the original ConnectionError is chained as __cause__."""
        original = requests.ConnectionError("Connection refused")
        mock_session._session.request = MagicMock(side_effect=original)

        with pytest.raises(IBCAuthenticationError) as exc_info:
            mock_session.make_request(method="get", endpoint="/api/test")

        assert exc_info.value.__cause__ is original


# ---------------------------------------------------------------------------
# Timeout tests
# ---------------------------------------------------------------------------


class TestTimeout:
    """Tests for the timeout parameter."""

    def _mock_response(self, status_code=200, json_data=None, content=b"data", ok=True):
        """Helper to create a mock response object."""
        mock_resp = MagicMock(spec=requests.Response)
        mock_resp.status_code = status_code
        mock_resp.ok = ok
        mock_resp.content = content
        mock_resp.text = str(json_data) if json_data else ""
        mock_resp.json.return_value = json_data or {}
        mock_resp.url = "https://localhost:5000/v1/test"
        mock_resp.request = MagicMock()
        mock_resp.request.headers = {"Content-Type": "application/json"}
        mock_resp.request.method = "GET"
        return mock_resp

    def test_default_timeout_is_30(self, mock_session):
        """Verify the default timeout is 30 seconds."""
        assert mock_session.timeout == 30

    def test_custom_timeout_stored(self, mock_client):
        """Verify a custom timeout is stored on the session."""
        with patch("ibc.session.UserAgent") as mock_ua:
            mock_ua.return_value.edge = "MockUserAgent/1.0"
            session = InteractiveBrokersSession(ib_client=mock_client, timeout=60)
        assert session.timeout == 60

    def test_zero_timeout_disables_timeout(self, mock_client):
        """Verify timeout=0 sets timeout to None (no timeout)."""
        with patch("ibc.session.UserAgent") as mock_ua:
            mock_ua.return_value.edge = "MockUserAgent/1.0"
            session = InteractiveBrokersSession(ib_client=mock_client, timeout=0)
        assert session.timeout is None

    def test_timeout_passed_to_request(self, mock_session):
        """Verify the session-level timeout is passed to requests."""
        mock_session._session.request = MagicMock(return_value=self._mock_response(json_data={"status": "ok"}))

        mock_session.make_request(method="get", endpoint="/api/test")

        _, kwargs = mock_session._session.request.call_args
        assert kwargs["timeout"] == 30

    def test_per_request_timeout_overrides_session(self, mock_session):
        """Verify per-request timeout overrides the session default."""
        mock_session._session.request = MagicMock(return_value=self._mock_response(json_data={"status": "ok"}))

        mock_session.make_request(method="get", endpoint="/api/test", timeout=5)

        _, kwargs = mock_session._session.request.call_args
        assert kwargs["timeout"] == 5


# ---------------------------------------------------------------------------
# health_check tests
# ---------------------------------------------------------------------------


class TestHealthCheck:
    """Tests for the health_check method."""

    def test_returns_true_on_success(self, mock_session):
        """Verify health_check returns True when gateway responds."""
        mock_resp = MagicMock(spec=requests.Response)
        mock_resp.status_code = 200
        mock_resp.ok = True
        mock_resp.content = b'{"session": "active"}'
        mock_resp.text = '{"session": "active"}'
        mock_resp.json.return_value = {"session": "active"}
        mock_session._session.request = MagicMock(return_value=mock_resp)

        assert mock_session.health_check() is True

    def test_returns_false_on_connection_error(self, mock_session):
        """Verify health_check returns False when gateway is unreachable."""
        mock_session._session.request = MagicMock(side_effect=requests.ConnectionError("Connection refused"))

        assert mock_session.health_check() is False

    def test_returns_false_on_request_error(self, mock_session):
        """Verify health_check returns False on a non-ok response."""
        mock_resp = MagicMock(spec=requests.Response)
        mock_resp.status_code = 500
        mock_resp.ok = False
        mock_resp.content = b""
        mock_resp.text = ""
        mock_resp.url = "https://localhost:5000/v1/api/tickle"
        mock_resp.request = MagicMock()
        mock_resp.request.headers = {"Content-Type": "application/json"}
        mock_resp.request.method = "GET"
        mock_session._session.request = MagicMock(return_value=mock_resp)

        assert mock_session.health_check() is False

    def test_calls_tickle_endpoint(self, mock_session):
        """Verify health_check calls the /api/tickle endpoint."""
        mock_resp = MagicMock(spec=requests.Response)
        mock_resp.status_code = 200
        mock_resp.ok = True
        mock_resp.content = b'{"session": "active"}'
        mock_resp.text = '{"session": "active"}'
        mock_resp.json.return_value = {"session": "active"}
        mock_session._session.request = MagicMock(return_value=mock_resp)

        mock_session.health_check()

        _, kwargs = mock_session._session.request.call_args
        assert kwargs["url"] == "https://localhost:5000/v1/api/tickle"


# ---------------------------------------------------------------------------
# Request/response timing logging tests
# ---------------------------------------------------------------------------


class TestTimingLogging:
    """Tests for request/response timing at DEBUG level."""

    def _mock_response(self, status_code=200, json_data=None, content=b"data", ok=True):
        """Helper to create a mock response object."""
        mock_resp = MagicMock(spec=requests.Response)
        mock_resp.status_code = status_code
        mock_resp.ok = ok
        mock_resp.content = content
        mock_resp.text = str(json_data) if json_data else ""
        mock_resp.json.return_value = json_data or {}
        mock_resp.url = "https://localhost:5000/v1/test"
        mock_resp.request = MagicMock()
        mock_resp.request.headers = {"Content-Type": "application/json"}
        mock_resp.request.method = "GET"
        return mock_resp

    def test_debug_log_includes_elapsed_ms(self, mock_session, caplog):
        """Verify DEBUG log includes elapsed time in milliseconds."""
        mock_session._session.request = MagicMock(return_value=self._mock_response(json_data={"status": "ok"}))

        import logging

        with caplog.at_level(logging.DEBUG, logger="ibc.session"):
            mock_session.make_request(method="get", endpoint="/api/test")

        debug_messages = [r.message for r in caplog.records if r.levelno == logging.DEBUG]
        assert any("completed in" in msg and "ms" in msg for msg in debug_messages)


# ---------------------------------------------------------------------------
# IBCRequestError.__repr__ test
# ---------------------------------------------------------------------------


class TestIBCRequestErrorRepr:
    """Tests for the IBCRequestError repr output."""

    def test_repr_format(self):
        """Verify __repr__ includes status_code, method, and url."""
        err = IBCRequestError(status_code=404, method="GET", url="https://example.com/api")
        result = repr(err)
        assert "IBCRequestError(" in result
        assert "status_code=404" in result
        assert "method='GET'" in result
        assert "url='https://example.com/api'" in result

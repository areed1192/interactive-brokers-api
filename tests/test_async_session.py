"""Tests for the async session (httpx-based)."""

# pylint: disable=redefined-outer-name
# pylint: disable=import-outside-toplevel
# pylint: disable=protected-access

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

pytest.importorskip("httpx", reason="httpx not installed (install with: pip install ibc-api[async])")

from ibc.exceptions import IBCRateLimitError, IBCRequestError #pylint: disable=wrong-import-position
from ibc.async_session import AsyncInteractiveBrokersSession #pylint: disable=wrong-import-position


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def mock_client():
    """Create a mock InteractiveBrokersClient."""
    client = MagicMock()
    client.account_number = "U1234567"
    return client


@pytest.fixture
def async_session(mock_client):
    """Create an AsyncInteractiveBrokersSession with mocked httpx client."""
    session = AsyncInteractiveBrokersSession(ib_client=mock_client)
    session._client = MagicMock()
    return session


# ---------------------------------------------------------------------------
# AsyncInteractiveBrokersSession tests
# ---------------------------------------------------------------------------


class TestAsyncSessionInit:
    """Tests for AsyncInteractiveBrokersSession initialization."""

    def test_stores_client_reference(self, async_session, mock_client):
        """Verify the async session stores a reference to the client."""
        assert async_session.client is mock_client

    def test_default_resource_url(self, async_session):
        """Verify the default resource URL."""
        assert async_session.resource_url == "https://localhost:5000/v1"

    def test_repr(self, async_session):
        """Verify __repr__ output."""
        result = repr(async_session)
        assert "AsyncInteractiveBrokersSession" in result
        assert "localhost:5000" in result

    def test_build_url(self, async_session):
        """Verify build_url concatenates correctly."""
        url = async_session.build_url("/api/iserver/accounts")
        assert url == "https://localhost:5000/v1/api/iserver/accounts"


class TestAsyncMakeRequest:
    """Tests for async make_request."""

    @pytest.mark.asyncio
    async def test_successful_request(self, async_session):
        """Verify successful request returns parsed JSON."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.is_success = True
        mock_response.content = b'{"status": "ok"}'
        mock_response.json.return_value = {"status": "ok"}

        async_session._client.request = AsyncMock(return_value=mock_response)

        result = await async_session.make_request(method="get", endpoint="/api/test")
        assert result == {"status": "ok"}

    @pytest.mark.asyncio
    async def test_empty_content_returns_success_message(self, async_session):
        """Verify empty content returns success dict."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.is_success = True
        mock_response.content = b""

        async_session._client.request = AsyncMock(return_value=mock_response)

        result = await async_session.make_request(method="get", endpoint="/api/test")
        assert result["message"] == "response successful"

    @pytest.mark.asyncio
    async def test_invalid_method_raises_value_error(self, async_session):
        """Verify unsupported HTTP method raises ValueError."""
        with pytest.raises(ValueError, match="Unsupported HTTP method"):
            await async_session.make_request(method="OPTIONS", endpoint="/api/test")

    @pytest.mark.asyncio
    async def test_error_response_raises_request_error(self, async_session):
        """Verify non-ok responses raise IBCRequestError."""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.is_success = False
        mock_response.content = b'{"error": "fail"}'
        mock_response.json.return_value = {"error": "fail"}
        mock_response.text = '{"error": "fail"}'
        mock_response.url = "https://localhost:5000/v1/test"

        async_session._client.request = AsyncMock(return_value=mock_response)

        with pytest.raises(IBCRequestError):
            await async_session.make_request(method="get", endpoint="/api/test")

    @pytest.mark.asyncio
    async def test_429_retries_then_succeeds(self, async_session):
        """Verify 429 triggers retry and succeeds on second attempt."""
        rate_limit_resp = MagicMock()
        rate_limit_resp.status_code = 429
        rate_limit_resp.is_success = False
        rate_limit_resp.url = "https://localhost:5000/v1/test"

        success_resp = MagicMock()
        success_resp.status_code = 200
        success_resp.is_success = True
        success_resp.content = b'{"data": 1}'
        success_resp.json.return_value = {"data": 1}

        async_session._client.request = AsyncMock(side_effect=[rate_limit_resp, success_resp])

        with patch("asyncio.sleep", new_callable=AsyncMock):
            result = await async_session.make_request(method="get", endpoint="/api/test")

        assert result == {"data": 1}

    @pytest.mark.asyncio
    async def test_429_exhausts_retries_raises_rate_limit_error(self, async_session):
        """Verify IBCRateLimitError after max retries on 429."""
        rate_limit_resp = MagicMock()
        rate_limit_resp.status_code = 429
        rate_limit_resp.is_success = False
        rate_limit_resp.url = "https://localhost:5000/v1/test"

        async_session._client.request = AsyncMock(return_value=rate_limit_resp)

        with patch("asyncio.sleep", new_callable=AsyncMock):
            with pytest.raises(IBCRateLimitError):
                await async_session.make_request(method="get", endpoint="/api/test")

    @pytest.mark.asyncio
    async def test_close(self, async_session):
        """Verify close calls aclose on the httpx client."""
        async_session._client.aclose = AsyncMock()
        await async_session.close()
        async_session._client.aclose.assert_called_once()

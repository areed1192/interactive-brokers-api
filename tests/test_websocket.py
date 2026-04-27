"""Tests for the WebSocket streaming client."""


from unittest.mock import AsyncMock, MagicMock, patch

import pytest

pytest.importorskip("websockets", reason="websockets not installed (install with: pip install ibc-api[async])")

from ibc.websocket import DEFAULT_WS_URL, IBWebSocketClient  # noqa: E402

# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------


class AsyncIteratorMock:
    """Helper to make a list behave as an async iterator."""

    def __init__(self, items):
        self._items = iter(items)

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            return next(self._items)
        except StopIteration:
            raise StopAsyncIteration from None


# ---------------------------------------------------------------------------
# IBWebSocketClient tests
# ---------------------------------------------------------------------------


class TestIBWebSocketClientInit:
    """Tests for IBWebSocketClient initialization."""

    def test_default_url(self):
        """Verify default WebSocket URL."""
        ws = IBWebSocketClient()
        assert ws._url == DEFAULT_WS_URL

    def test_custom_url(self):
        """Verify custom URL is stored."""
        ws = IBWebSocketClient(url="wss://custom:5000/ws")
        assert ws._url == "wss://custom:5000/ws"

    def test_not_connected_by_default(self):
        """Verify client is not connected initially."""
        ws = IBWebSocketClient()
        assert ws.connected is False

    def test_repr(self):
        """Verify __repr__ output."""
        ws = IBWebSocketClient()
        result = repr(ws)
        assert "IBWebSocketClient" in result
        assert "connected=False" in result


class TestIBWebSocketClientSend:
    """Tests for send and subscribe methods."""

    @pytest.mark.asyncio
    async def test_send_raises_if_not_connected(self):
        """Verify send raises RuntimeError if not connected."""
        ws = IBWebSocketClient()
        with pytest.raises(RuntimeError, match="not connected"):
            await ws.send("test")

    @pytest.mark.asyncio
    async def test_send_calls_ws_send(self):
        """Verify send delegates to the underlying websocket."""
        ws = IBWebSocketClient()
        ws._ws = AsyncMock()
        ws._connected = True

        await ws.send("test message")
        ws._ws.send.assert_called_once_with("test message")

    @pytest.mark.asyncio
    async def test_subscribe_market_data(self):
        """Verify subscribe_market_data sends correct format."""
        ws = IBWebSocketClient()
        ws._ws = AsyncMock()
        ws._connected = True

        await ws.subscribe_market_data(conids=[265598, 756733])

        assert ws._ws.send.call_count == 2
        calls = [c.args[0] for c in ws._ws.send.call_args_list]
        assert "smd+265598+" in calls[0]
        assert "smd+756733+" in calls[1]

    @pytest.mark.asyncio
    async def test_subscribe_market_data_with_fields(self):
        """Verify subscribe sends field list when provided."""
        ws = IBWebSocketClient()
        ws._ws = AsyncMock()
        ws._connected = True

        await ws.subscribe_market_data(conids=[265598], fields=["31", "84"])

        sent = ws._ws.send.call_args[0][0]
        assert '"fields": ["31", "84"]' in sent

    @pytest.mark.asyncio
    async def test_unsubscribe_market_data(self):
        """Verify unsubscribe sends correct format."""
        ws = IBWebSocketClient()
        ws._ws = AsyncMock()
        ws._connected = True

        await ws.unsubscribe_market_data(conids=[265598])

        ws._ws.send.assert_called_once_with("umd+265598+{}")

    @pytest.mark.asyncio
    async def test_subscribe_order_updates(self):
        """Verify subscribe_order_updates sends correct message."""
        ws = IBWebSocketClient()
        ws._ws = AsyncMock()
        ws._connected = True

        await ws.subscribe_order_updates()
        ws._ws.send.assert_called_once_with("sor+{}")

    @pytest.mark.asyncio
    async def test_unsubscribe_order_updates(self):
        """Verify unsubscribe_order_updates sends correct message."""
        ws = IBWebSocketClient()
        ws._ws = AsyncMock()
        ws._connected = True

        await ws.unsubscribe_order_updates()
        ws._ws.send.assert_called_once_with("uor+{}")

    @pytest.mark.asyncio
    async def test_subscribe_account_summary(self):
        """Verify subscribe_account_summary sends correct message."""
        ws = IBWebSocketClient()
        ws._ws = AsyncMock()
        ws._connected = True

        await ws.subscribe_account_summary()
        ws._ws.send.assert_called_once_with("sbd+{}")


class TestIBWebSocketClientConnect:
    """Tests for connect and close."""

    @pytest.mark.asyncio
    async def test_connect_sets_connected(self):
        """Verify connect sets connected flag."""
        ws = IBWebSocketClient()

        with patch("websockets.connect", new_callable=AsyncMock) as mock_connect:
            mock_connect.return_value = AsyncMock()
            await ws.connect()

        assert ws.connected is True

    @pytest.mark.asyncio
    async def test_close_sets_disconnected(self):
        """Verify close unsets connected flag."""
        ws = IBWebSocketClient()
        ws._ws = AsyncMock()
        ws._connected = True

        await ws.close()
        assert ws.connected is False

    @pytest.mark.asyncio
    async def test_context_manager(self):
        """Verify async context manager connects and disconnects."""
        with patch("websockets.connect", new_callable=AsyncMock) as mock_connect:
            mock_ws = AsyncMock()
            mock_connect.return_value = mock_ws

            async with IBWebSocketClient() as ws:
                assert ws.connected is True

            mock_ws.close.assert_called_once()


class TestIBWebSocketClientIteration:
    """Tests for async iteration."""

    @pytest.mark.asyncio
    async def test_aiter_raises_if_not_connected(self):
        """Verify iteration raises RuntimeError if not connected."""
        ws = IBWebSocketClient()
        with pytest.raises(RuntimeError, match="not connected"):
            async for _ in ws:
                pass

    @pytest.mark.asyncio
    async def test_aiter_yields_parsed_json(self):
        """Verify async iteration parses JSON messages."""
        ws = IBWebSocketClient()
        ws._connected = True

        messages = ['{"conid": 265598, "31": "150.5"}', '{"conid": 756733, "31": "50.0"}']
        ws._ws = AsyncIteratorMock(messages)

        received = []
        async for msg in ws:
            received.append(msg)

        assert len(received) == 2
        assert received[0]["conid"] == 265598
        assert received[1]["31"] == "50.0"

    @pytest.mark.asyncio
    async def test_aiter_skips_non_json(self):
        """Verify non-JSON messages are skipped."""
        ws = IBWebSocketClient()
        ws._connected = True

        messages = ["not json", '{"valid": true}']
        ws._ws = AsyncIteratorMock(messages)

        received = []
        async for msg in ws:
            received.append(msg)

        assert len(received) == 1
        assert received[0] == {"valid": True}

    @pytest.mark.asyncio
    async def test_on_message_callback(self):
        """Verify on_message callback is invoked for each message."""
        callback = MagicMock()
        ws = IBWebSocketClient(on_message=callback)
        ws._connected = True

        messages = ['{"data": 1}', '{"data": 2}']
        ws._ws = AsyncIteratorMock(messages)

        async for _ in ws:
            pass

        assert callback.call_count == 2

"""WebSocket streaming client for real-time Interactive Brokers market data."""


from __future__ import annotations

import json
import logging
from collections.abc import AsyncIterator, Callable
from typing import Any

logger = logging.getLogger(__name__)

# IB WebSocket endpoint (Client Portal Gateway)
DEFAULT_WS_URL = "wss://localhost:5000/v1/api/ws"


class IBWebSocketClient:
    """WebSocket client for streaming real-time data from IB Client Portal Gateway.

    ### Overview
    ----
    Connects to the IB Client Portal WebSocket endpoint and provides
    async iteration over incoming messages. Supports subscribing to
    market data, order updates, and account notifications.

    ### Usage
    ----
        >>> async with IBWebSocketClient() as ws:
        ...     await ws.subscribe_market_data(conids=[265598])
        ...     async for message in ws:
        ...         print(message)
    """

    def __init__(
        self,
        url: str = DEFAULT_WS_URL,
        verify_ssl: bool = False,
        on_message: Callable[[dict], None] | None = None,
    ) -> None:
        """Initialize the WebSocket client.

        ### Parameters
        ----
        url : str (optional)
            WebSocket URL. Defaults to the IB Client Portal Gateway WS endpoint.

        verify_ssl : bool (optional, Default=False)
            Whether to verify SSL certificates.

        on_message : Callable (optional)
            Optional callback invoked for each received message.
        """
        self._url = url
        self._verify_ssl = verify_ssl
        self._on_message = on_message
        self._ws: Any = None
        self._connected = False

    def __repr__(self) -> str:
        return f"IBWebSocketClient(url={self._url!r}, connected={self._connected})"

    @property
    def connected(self) -> bool:
        """Whether the WebSocket connection is currently active."""
        return self._connected

    async def connect(self) -> None:
        """Establish the WebSocket connection."""
        import ssl

        import websockets

        ssl_context: ssl.SSLContext | None = None
        if not self._verify_ssl:
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE

        self._ws = await websockets.connect(self._url, ssl=ssl_context)
        self._connected = True
        logger.info("WebSocket connected to %s", self._url)

    async def close(self) -> None:
        """Close the WebSocket connection."""
        if self._ws:
            await self._ws.close()
            self._connected = False
            logger.info("WebSocket disconnected")

    async def __aenter__(self) -> IBWebSocketClient:
        await self.connect()
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.close()

    async def send(self, message: str) -> None:
        """Send a raw message over the WebSocket.

        ### Parameters
        ----
        message : str
            The message string to send.
        """
        if not self._ws:
            raise RuntimeError("WebSocket is not connected. Call connect() first.")
        await self._ws.send(message)
        logger.debug("Sent: %s", message)

    async def subscribe_market_data(self, conids: list[int], fields: list[str] | None = None) -> None:
        """Subscribe to real-time market data for the given contract IDs.

        ### Parameters
        ----
        conids : list[int]
            List of contract IDs to subscribe to.

        fields : list[str] (optional)
            List of field IDs to subscribe to (e.g. ["31", "84", "86"]).
            If not provided, subscribes to all available fields.
        """
        for conid in conids:
            payload = f"smd+{conid}+"
            if fields:
                payload += json.dumps({"fields": fields})
            else:
                payload += "{}"
            await self.send(payload)

    async def unsubscribe_market_data(self, conids: list[int]) -> None:
        """Unsubscribe from market data for the given contract IDs.

        ### Parameters
        ----
        conids : list[int]
            List of contract IDs to unsubscribe from.
        """
        for conid in conids:
            await self.send(f"umd+{conid}+{{}}")

    async def subscribe_order_updates(self) -> None:
        """Subscribe to real-time order status updates."""
        await self.send("sor+{}")

    async def unsubscribe_order_updates(self) -> None:
        """Unsubscribe from order status updates."""
        await self.send("uor+{}")

    async def subscribe_account_summary(self) -> None:
        """Subscribe to account summary/PnL updates."""
        await self.send("sbd+{}")

    async def __aiter__(self) -> AsyncIterator[dict]:
        """Async iterate over incoming WebSocket messages.

        ### Yields
        ----
        dict:
            Parsed JSON messages from the IB WebSocket.
        """
        if not self._ws:
            raise RuntimeError("WebSocket is not connected. Call connect() first.")

        async for raw_message in self._ws:
            try:
                message = json.loads(raw_message)
            except (json.JSONDecodeError, TypeError):
                logger.warning("Non-JSON message received: %s", raw_message)
                continue

            logger.debug("Received: %s", message)

            if self._on_message:
                self._on_message(message)

            yield message

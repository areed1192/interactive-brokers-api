"""Example usage of the WebSocket streaming client for real-time market data."""

import asyncio
from pprint import pprint
from ibc.websocket import IBWebSocketClient


async def main():
    """Demonstrate WebSocket streaming from IB Client Portal Gateway."""

    # -----------------------------------------------------------------------
    # Connect using a context manager and subscribe to market data.
    # -----------------------------------------------------------------------

    async with IBWebSocketClient() as ws:

        # Subscribe to real-time quotes for AAPL (265598) and MSFT (272093).
        await ws.subscribe_market_data(
            conids=[265598, 272093],
            fields=["31", "84", "86"]  # Last price, Bid, Ask
        )
        print("Subscribed to market data for AAPL and MSFT")

        # -------------------------------------------------------------------
        # Subscribe to order status updates.
        # -------------------------------------------------------------------

        await ws.subscribe_order_updates()
        print("Subscribed to order updates")

        # -------------------------------------------------------------------
        # Subscribe to account summary / PnL updates.
        # -------------------------------------------------------------------

        await ws.subscribe_account_summary()
        print("Subscribed to account summary")

        # -------------------------------------------------------------------
        # Iterate over incoming messages (async for loop).
        # -------------------------------------------------------------------

        count = 0
        async for message in ws:
            pprint(message)
            # Output: {'conid': 265598, '31': '192.53', '84': '192.50', '86': '192.55'}
            count += 1
            if count >= 10:
                break  # Stop after 10 messages for demo purposes.

        # -------------------------------------------------------------------
        # Unsubscribe before disconnecting.
        # -------------------------------------------------------------------

        await ws.unsubscribe_market_data(conids=[265598, 272093])
        await ws.unsubscribe_order_updates()
        print("Unsubscribed and disconnecting")


async def with_callback():
    """Demonstrate the on_message callback pattern."""

    def handle_message(msg: dict) -> None:
        """Process each incoming WebSocket message."""
        topic = msg.get("topic", "unknown")
        print(f"[{topic}] {msg}")

    # -----------------------------------------------------------------------
    # Provide a callback that fires for each message.
    # -----------------------------------------------------------------------

    async with IBWebSocketClient(on_message=handle_message) as ws:
        await ws.subscribe_market_data(conids=[265598])

        count = 0
        async for _ in ws:
            count += 1
            if count >= 5:
                break


if __name__ == '__main__':
    print("--- Streaming market data ---")
    asyncio.run(main())

    print("\n--- Callback pattern ---")
    asyncio.run(with_callback())

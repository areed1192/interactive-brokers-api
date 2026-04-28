"""Example usage of placing an order and monitoring updates via async session and WebSocket."""

import asyncio
from configparser import ConfigParser

from ibc.client import InteractiveBrokersClient
from ibc.websocket import IBWebSocketClient

config = ConfigParser()
config.read("config/config.ini")

account_number = config.get("interactive_brokers_paper", "paper_account")

# Initialize the client and authenticate (sync — opens browser for gateway login).
ibc_client = InteractiveBrokersClient(
    account_number=account_number,
)
ibc_client.authentication.wait_for_login()


async def place_and_monitor() -> None:
    """Place a limit order and stream order updates via WebSocket."""

    # -------------------------------------------------------------------
    # Place a limit order using the sync orders service.
    # -------------------------------------------------------------------

    order_template = {
        "conid": 265598,
        "secType": "265598:STK",
        "cOID": "async-limit-buy-1",
        "orderType": "LMT",
        "price": 150.00,
        "side": "BUY",
        "quantity": 1,
        "tif": "DAY",
    }

    response = ibc_client.orders.place_order(
        account_id=ibc_client.account_number,
        order=order_template,
    )
    print("Order placed:", response)
    # Output: [{'id': 'abc123', 'message': ['...confirm...']}]

    # Handle order confirmation reply if needed.
    if isinstance(response, list) and response and "id" in response[0]:
        reply = ibc_client.orders.reply(
            reply_id=response[0]["id"],
            message={"confirmed": True},
        )
        print("Order confirmed:", reply)
        # Output: [{'order_id': '1915650541', 'order_status': 'Submitted'}]

    # -------------------------------------------------------------------
    # Stream real-time order updates via WebSocket.
    # -------------------------------------------------------------------

    print("\nListening for order updates (Ctrl+C to stop)...")

    async with IBWebSocketClient() as ws:
        await ws.subscribe_order_updates()

        async for message in ws:
            # Order update messages have a "topic" starting with "sor"
            topic = message.get("topic", "")
            if topic.startswith("sor"):
                print("Order update:", message)
            else:
                print("Message:", message)


if __name__ == "__main__":
    asyncio.run(place_and_monitor())

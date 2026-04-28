"""Example usage of the Orders service."""

from configparser import ConfigParser
from pprint import pprint

from ibc.client import InteractiveBrokersClient

config = ConfigParser()
config.read('config/config.ini')

account_number = config.get('interactive_brokers_paper', 'paper_account')

ibc_client = InteractiveBrokersClient(
    account_number=account_number,
)
ibc_client.authentication.wait_for_login()

orders_service = ibc_client.orders

# ---------------------------------------------------------------------------
# List all current orders.
# ---------------------------------------------------------------------------

pprint(orders_service.orders())
# Output: {'orders': [{'orderId': 123, 'status': 'Submitted', ...}]}

# ---------------------------------------------------------------------------
# Place a limit order (may require confirmation via reply).
# ---------------------------------------------------------------------------

order_template = {
    "conid": 265598,
    "secType": "265598:STK",
    "cOID": "limit-buy-order-v1",
    "orderType": "LMT",
    "price": 150.00,
    "side": "BUY",
    "quantity": 1,
    "tif": "DAY",
}

response = orders_service.place_order(
    account_id=ibc_client.account_number,
    order=order_template
)
pprint(response)
# Output: [{'id': 'abc123', 'message': ['...confirm...']}]

# Handle order confirmation reply if needed.
if isinstance(response, list) and response and 'id' in response[0]:
    pprint(
        orders_service.reply(
            reply_id=response[0]['id'],
            message={"confirmed": True}
        )
    )
    # Output: [{'order_id': '1915650541', 'order_status': 'Submitted'}]

# ---------------------------------------------------------------------------
# Place a bracket order (parent + child orders).
# ---------------------------------------------------------------------------

bracket = {
    "orders": [
        {
            "conid": 265598,
            "secType": "265598:STK",
            "cOID": "bracket-parent",
            "orderType": "LMT",
            "side": "BUY",
            "price": 150.00,
            "quantity": 1,
            "tif": "DAY",
        },
        {
            "conid": 265598,
            "secType": "265598:STK",
            "parentId": "bracket-parent",
            "orderType": "LMT",
            "side": "SELL",
            "price": 160.00,
            "quantity": 1,
            "tif": "GTC",
        },
    ]
}

pprint(
    orders_service.place_bracket_order(
        account_id=ibc_client.account_number,
        orders=bracket
    )
)
# Output: [{'order_id': '...', 'order_status': 'PreSubmitted'}]

# ---------------------------------------------------------------------------
# Modify an existing order.
# ---------------------------------------------------------------------------

pprint(
    orders_service.modify_order(
        account_id=ibc_client.account_number,
        order_id='1915650541',
        order={
            "conid": 265598,
            "orderType": "LMT",
            "price": 155.00,
            "side": "BUY",
            "quantity": 1,
            "tif": "DAY",
        }
    )
)
# Output: [{'order_id': '1915650541', 'order_status': 'Submitted'}]

# ---------------------------------------------------------------------------
# Delete (cancel) an order.
# ---------------------------------------------------------------------------

pprint(
    orders_service.delete_order(
        account_id=ibc_client.account_number,
        order_id='1915650541'
    )
)
# Output: {'msg': 'Request was submitted', 'order_id': 1915650541, ...}

# ---------------------------------------------------------------------------
# Get the status of an order.
# ---------------------------------------------------------------------------

pprint(orders_service.order_status(order_id='1915650541'))
# Output: {'orderId': 1915650541, 'status': 'Cancelled', ...}

# ---------------------------------------------------------------------------
# Place a what-if order (cost preview without execution).
# ---------------------------------------------------------------------------

pprint(
    orders_service.place_whatif_order(
        account_id=ibc_client.account_number,
        order=order_template
    )
)
# Output: {'amount': {'total': '150.00', 'commission': '1.00', ...}}

# ---------------------------------------------------------------------------
# Place what-if orders (multiple).
# ---------------------------------------------------------------------------

pprint(
    orders_service.place_whatif_orders(
        account_id=ibc_client.account_number,
        orders=[order_template]
    )
)
# Output: {'amount': {'total': '150.00', 'commission': '1.00', ...}}

# ---------------------------------------------------------------------------
# Place orders for a Financial Advisor group.
# ---------------------------------------------------------------------------

pprint(
    orders_service.place_orders_for_fa_group(
        fa_group='MyGroup',
        orders=[order_template]
    )
)
# Output: [{'order_id': '...', 'order_status': 'Submitted'}]

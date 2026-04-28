"""Orders-related end-points for the Interactive Brokers API."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ibc.models import Order, OrderStatus
from ibc.session import InteractiveBrokersSession
from ibc.utils.validation import validate_id

if TYPE_CHECKING:
    from ibc.client import InteractiveBrokersClient


class Orders:
    """Client for managing orders via the Interactive Brokers API."""

    def __init__(self, ib_client: InteractiveBrokersClient, ib_session: InteractiveBrokersSession) -> None:
        """Initializes the `Orders` client.

        ### Parameters
        ----
        ib_client : InteractiveBrokersClient
            The `InteractiveBrokersClient` Python Client.

        ib_session : InteractiveBrokersSession
            The IB session handler.
        """

        self.client = ib_client
        self.session = ib_session

    def __repr__(self) -> str:
        return "Orders()"

    def orders(self) -> list[Order]:
        """The end-point is meant to be used in polling mode, e.g. requesting
        every x seconds.

        ### Overview
        ----
        The response will contain two objects, one is notification,
        the other is orders. Orders is the list of orders (cancelled,
        filled, submitted) with activity in the current day. Notifications
        contains information about execute orders as they happen, see
        status field.

        ### Returns
        ----
        list[Order]:
            A list of ``Order`` model instances parsed from the response.

        ### Usage
        ----
            >>> orders_services = ibc_client.orders
            >>> orders_services.orders()
        """

        content = self.session.make_request(method="get", endpoint="/api/iserver/account/orders")

        raw_orders = content.get("orders", []) if isinstance(content, dict) else []
        return [Order.from_dict(o) for o in raw_orders]

    def place_order(self, account_id: str, order: dict) -> dict:
        """Places an order.

        ### Overview
        ----
        Please note here, sometimes this end-point alone can’t make sure
        you submit the order successfully, you could receive some questions
        in the response, you have to to answer them in order to submit the order
        successfully. You can use `/iserver/reply/{replyid}` end-point to answer
        questions.

        ### Parameters
        ----
        account_id : str
            The account you want the order placed on.

        order : dict
            The order payload.

        ### Returns
        ----
        dict:
            A `Reply` resource or a `Order` resource.

        ### Usage
        ----
            >>> orders_services = ibc_client.orders
            >>> orders_services.place_order(
                account_id=ibc_client.account_number,
                order={
                    "conid": 251962528,
                    "secType": "362673777:STK",
                    "cOID": "limit-buy-order-1",
                    "orderType": "LMT",
                    "price": 5.00,
                    "side": "BUY",
                    "quantity": 1,
                    "tif": "DAY"
                }
            )
        """

        validate_id(account_id, "account_id")

        content = self.session.make_request(
            method="post",
            endpoint=f"/api/iserver/account/{account_id}/order",
            json_payload=order,
        )

        return content

    def place_bracket_order(self, account_id: str, orders: dict) -> dict:
        """Places multiple orders at once.

        ### Parameters
        ----
        account_id : str
            The account you want the orders placed on.

        orders : dict
            The orders payload.

        ### Returns
        ----
        dict:
            A `Reply` resource or a `Order` resource.

        ### Usage
        ----
            >>> orders_services = ibc_client.orders
            >>> orders_services.place_bracket_order(
                account_id=ibc_client.account_number,
                order={
                    "orders": [
                        {
                            "conid": 251962528,
                            "secType": "362673777:FUT",
                            "cOID": "buy-1",
                            "orderType": "LMT",
                            "side": "BUY",
                            "price": 9.00,
                            "quantity": 1,
                            "tif": "DAY"
                        },
                        {
                            "conid": 251962528,
                            "secType": "362673777:STK",
                            # This MUST match the `cOID` of the first order.
                            "parentId": "buy-1",
                            "orderType": "LMT",
                            "side": "BUY",
                            "price": 7.00,
                            "quantity": 2,
                            "tif": "DAY"
                        }
                    ]
                }
            )
        """

        validate_id(account_id, "account_id")

        content = self.session.make_request(
            method="post",
            endpoint=f"/api/iserver/account/{account_id}/orders",
            json_payload=orders,
        )

        return content

    def modify_order(self, account_id: str, order_id: str, order: dict) -> dict:
        """Modifies an open order.

        ### Overview
        ----
        The `/iserver/accounts` endpoint must first be called.

        ### Parameters
        ----
        account_id : str
            The account which has the order you want to be
            modified.

        order_id : str
            The id of the order you want to be modified.

        order : dict
            The new order payload.

        ### Returns
        ----
        dict:
            A `Reply` resource or a `Order` resource.

        ### Usage
        ----
            >>> orders_services = ibc_client.orders
            >>> orders_services.modify_order(
                account_id=ibc_client.account_number,
                order_id='1915650539',
                order={
                    "conid": 251962528,
                    "secType": "362673777:STK",
                    "cOID": "limit-buy-order-1",
                    "orderType": "LMT",
                    "price": 5.00,
                    "side": "BUY",
                    "quantity": 1,
                    "tif": "DAY"
                }
            )
        """

        validate_id(account_id, "account_id")
        validate_id(order_id, "order_id")

        content = self.session.make_request(
            method="post",
            endpoint=f"/api/iserver/account/{account_id}/order/{order_id}",
            json_payload=order,
        )

        return content

    def delete_order(self, account_id: str, order_id: str) -> list | dict:
        """Deletes an order.

        ### Parameters
        ----
        account_id : str
            The account that contains the order you want to
            delete.

        order_id : str
            The id of the order you want to delete.

        ### Returns
        ----
        Union[list, dict]:
            A `OrderResponse` resource or a collection of them.

        ### Usage
        ----
            >>> orders_services = ibc_client.orders
            >>> orders_services.delete_order(
                account_id=ibc_client.account_number,
                order_id=
            )
        """

        validate_id(account_id, "account_id")
        validate_id(order_id, "order_id")

        content = self.session.make_request(
            method="delete",
            endpoint=f"/api/iserver/account/{account_id}/order/{order_id}",
        )

        return content

    def place_whatif_order(self, account_id: str, order: dict) -> dict:
        """This end-point allows you to preview order without actually
        submitting the order and you can get commission information in
        the response.

        ### Parameters
        ----
        account_id : str
            The account you want the order placed on.

        order : dict
            The order payload.

        ### Returns
        ----
        dict:
            A `OrderCommission` resource.

        ### Usage
        ----
            >>> orders_services = ibc_client.orders
            >>> orders_services.place_whatif_order(
                account_id=ibc_client.account_number,
                order={
                    "conid": 251962528,
                    "secType": "362673777:STK",
                    "cOID": "limit-buy-order-1",
                    "orderType": "LMT",
                    "price": 5.00,
                    "side": "BUY",
                    "quantity": 1,
                    "tif": "DAY"
                }
            )
        """

        validate_id(account_id, "account_id")

        content = self.session.make_request(
            method="post",
            endpoint=f"/api/iserver/account/{account_id}/order/whatif",
            json_payload=order,
        )

        return content

    def reply(self, reply_id: str, message: dict) -> list | dict:
        """Reply to questions when placing orders and submit orders.

        ### Parameters
        ----
        reply_id : str
            The `ID` from the response of `Place Order` end-point

        message : dict
            The answer to question.

        ### Returns
        ----
        Union[list, dict]:
            A list when the order is submitted, a dictionary
            with an error message if not confirmed.

        ### Usage
        ----
            >>> orders_services = ibc_client.orders
            >>> orders_services.reply(
                reply_id='5050c104-1276-4483-8be8-ca598e698766',
                message={
                    "confirmed": True
                }
            )
        """

        validate_id(reply_id, "reply_id")

        content = self.session.make_request(
            method="post",
            endpoint=f"/api/iserver/reply/{reply_id}",
            json_payload=message,
        )

        return content

    def order_status(self, order_id: str) -> OrderStatus:
        """Returns the status of a single order.

        ### Parameters
        ----
        order_id : str
            The order ID to query.

        ### Returns
        ----
        OrderStatus:
            An order status resource.

        ### Usage
        ----
            >>> orders_services = ibc_client.orders
            >>> orders_services.order_status(order_id='1915650539')
        """

        validate_id(order_id, "order_id")

        content = self.session.make_request(method="get", endpoint=f"/api/iserver/account/order/status/{order_id}")

        return OrderStatus.from_dict(content)

    def place_orders_for_fa_group(self, fa_group: str, orders: dict) -> dict:
        """Places orders for a Financial Advisor (FA) group.

        ### Parameters
        ----
        fa_group : str
            The FA group name.

        orders : dict
            The orders payload.

        ### Returns
        ----
        dict:
            A ``Reply`` resource or an ``Order`` resource.

        ### Usage
        ----
            >>> orders_services = ibc_client.orders
            >>> orders_services.place_orders_for_fa_group(
                fa_group='MyGroup',
                orders={
                    "orders": [
                        {
                            "conid": 265598,
                            "orderType": "LMT",
                            "side": "BUY",
                            "price": 150.00,
                            "quantity": 10,
                            "tif": "DAY"
                        }
                    ]
                }
            )
        """

        validate_id(fa_group, "fa_group")

        content = self.session.make_request(
            method="post",
            endpoint=f"/api/iserver/account/orders/{fa_group}",
            json_payload=orders,
        )

        return content

    def place_whatif_orders(self, account_id: str, orders: dict) -> dict:
        """Preview multiple orders without submitting and get commission info.

        ### Parameters
        ----
        account_id : str
            The account to preview orders for.

        orders : dict
            The orders payload.

        ### Returns
        ----
        dict:
            A ``WhatIfOrder`` resource with commission and margin info.

        ### Usage
        ----
            >>> orders_services = ibc_client.orders
            >>> orders_services.place_whatif_orders(
                account_id=ibc_client.account_number,
                orders={
                    "orders": [
                        {
                            "conid": 265598,
                            "orderType": "LMT",
                            "side": "BUY",
                            "price": 150.00,
                            "quantity": 10,
                            "tif": "DAY"
                        }
                    ]
                }
            )
        """

        validate_id(account_id, "account_id")

        content = self.session.make_request(
            method="post",
            endpoint=f"/api/iserver/account/{account_id}/orders/whatif",
            json_payload=orders,
        )

        return content

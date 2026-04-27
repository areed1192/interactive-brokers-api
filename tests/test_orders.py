"""Tests for the Orders service."""


from unittest.mock import MagicMock

import pytest

from ibc.rest.orders import Orders
from ibc.models import Order, OrderStatus


# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------

SAMPLE_ORDERS_RESPONSE = {
    "orders": [
        {
            "acct": "U1234567",
            "orderId": 1915650539,
            "status": "Submitted",
            "conid": 265598,
            "side": "BUY",
            "orderType": "LMT",
            "price": 150.00,
            "quantity": 10,
        }
    ],
    "snapshot": True,
}

SAMPLE_PLACE_ORDER_RESPONSE = [
    {
        "id": "5050c104-1276-4483-8be8-ca598e698766",
        "message": ["Are you sure you want to submit this order?"],
    }
]

SAMPLE_ORDER_PAYLOAD = {
    "conid": 265598,
    "secType": "265598:STK",
    "cOID": "limit-buy-order-1",
    "orderType": "LMT",
    "price": 150.00,
    "side": "BUY",
    "quantity": 10,
    "tif": "DAY",
}

SAMPLE_BRACKET_PAYLOAD = {
    "orders": [
        {
            "conid": 265598,
            "secType": "265598:STK",
            "cOID": "buy-1",
            "orderType": "LMT",
            "side": "BUY",
            "price": 150.00,
            "quantity": 10,
            "tif": "DAY",
        },
        {
            "conid": 265598,
            "secType": "265598:STK",
            "parentId": "buy-1",
            "orderType": "STP",
            "side": "SELL",
            "price": 140.00,
            "quantity": 10,
            "tif": "GTC",
        },
    ]
}

SAMPLE_REPLY_RESPONSE = [{"order_id": "1915650539", "order_status": "Submitted"}]

ACCOUNT_ID = "U1234567"
ORDER_ID = "1915650539"


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def orders_service(mock_session, mock_client):
    """Create an Orders service with mocked session."""
    return Orders(ib_client=mock_client, ib_session=mock_session)


# ---------------------------------------------------------------------------
# Orders.orders tests
# ---------------------------------------------------------------------------


class TestOrdersList:
    """Tests for the Orders.orders method."""

    def test_returns_list_of_order_models(self, orders_service, mock_session):
        """Verify orders() returns a list of Order model instances."""
        mock_session.make_request = MagicMock(return_value=SAMPLE_ORDERS_RESPONSE)

        result = orders_service.orders()

        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], Order)
        assert result[0].acct == "U1234567"
        assert result[0].status == "Submitted"
        assert result[0].conid == 265598

    def test_returns_empty_list_for_empty_response(self, orders_service, mock_session):
        """Verify orders() returns empty list when no orders key."""
        mock_session.make_request = MagicMock(return_value={})

        result = orders_service.orders()

        assert result == []

    def test_calls_correct_endpoint(self, orders_service, mock_session):
        """Verify orders() calls the correct API endpoint."""
        mock_session.make_request = MagicMock(return_value={})

        orders_service.orders()

        mock_session.make_request.assert_called_once_with(
            method="get",
            endpoint="/api/iserver/account/orders",
        )


# ---------------------------------------------------------------------------
# Orders.place_order tests
# ---------------------------------------------------------------------------


class TestPlaceOrder:
    """Tests for the Orders.place_order method."""

    def test_returns_place_order_response(self, orders_service, mock_session):
        """Verify place_order() returns the parsed JSON response."""
        mock_session.make_request = MagicMock(return_value=SAMPLE_PLACE_ORDER_RESPONSE)

        result = orders_service.place_order(
            account_id=ACCOUNT_ID, order=SAMPLE_ORDER_PAYLOAD
        )

        assert result == SAMPLE_PLACE_ORDER_RESPONSE

    def test_calls_correct_endpoint_with_account_id(self, orders_service, mock_session):
        """Verify place_order() includes account_id in the endpoint."""
        mock_session.make_request = MagicMock(return_value={})

        orders_service.place_order(account_id=ACCOUNT_ID, order=SAMPLE_ORDER_PAYLOAD)

        mock_session.make_request.assert_called_once_with(
            method="post",
            endpoint=f"/api/iserver/account/{ACCOUNT_ID}/order",
            json_payload=SAMPLE_ORDER_PAYLOAD,
        )


# ---------------------------------------------------------------------------
# Orders.place_bracket_order tests
# ---------------------------------------------------------------------------


class TestPlaceBracketOrder:
    """Tests for the Orders.place_bracket_order method."""

    def test_calls_correct_endpoint(self, orders_service, mock_session):
        """Verify place_bracket_order() uses /orders (plural) endpoint."""
        mock_session.make_request = MagicMock(return_value={})

        orders_service.place_bracket_order(
            account_id=ACCOUNT_ID, orders=SAMPLE_BRACKET_PAYLOAD
        )

        mock_session.make_request.assert_called_once_with(
            method="post",
            endpoint=f"/api/iserver/account/{ACCOUNT_ID}/orders",
            json_payload=SAMPLE_BRACKET_PAYLOAD,
        )


# ---------------------------------------------------------------------------
# Orders.modify_order tests
# ---------------------------------------------------------------------------


class TestModifyOrder:
    """Tests for the Orders.modify_order method."""

    def test_calls_correct_endpoint_with_order_id(self, orders_service, mock_session):
        """Verify modify_order() includes both account_id and order_id."""
        mock_session.make_request = MagicMock(return_value={})

        orders_service.modify_order(
            account_id=ACCOUNT_ID,
            order_id=ORDER_ID,
            order=SAMPLE_ORDER_PAYLOAD,
        )

        mock_session.make_request.assert_called_once_with(
            method="post",
            endpoint=f"/api/iserver/account/{ACCOUNT_ID}/order/{ORDER_ID}",
            json_payload=SAMPLE_ORDER_PAYLOAD,
        )


# ---------------------------------------------------------------------------
# Orders.delete_order tests
# ---------------------------------------------------------------------------


class TestDeleteOrder:
    """Tests for the Orders.delete_order method."""

    def test_calls_delete_method(self, orders_service, mock_session):
        """Verify delete_order() uses the DELETE HTTP method."""
        mock_session.make_request = MagicMock(return_value={})

        orders_service.delete_order(account_id=ACCOUNT_ID, order_id=ORDER_ID)

        mock_session.make_request.assert_called_once_with(
            method="delete",
            endpoint=f"/api/iserver/account/{ACCOUNT_ID}/order/{ORDER_ID}",
        )


# ---------------------------------------------------------------------------
# Orders.place_whatif_order tests
# ---------------------------------------------------------------------------


class TestPlaceWhatifOrder:
    """Tests for the Orders.place_whatif_order method."""

    def test_calls_correct_whatif_endpoint(self, orders_service, mock_session):
        """Verify place_whatif_order() uses the /whatif endpoint."""
        mock_session.make_request = MagicMock(return_value={})

        orders_service.place_whatif_order(
            account_id=ACCOUNT_ID, order=SAMPLE_ORDER_PAYLOAD
        )

        mock_session.make_request.assert_called_once_with(
            method="post",
            endpoint=f"/api/iserver/account/{ACCOUNT_ID}/order/whatif",
            json_payload=SAMPLE_ORDER_PAYLOAD,
        )


# ---------------------------------------------------------------------------
# Orders.reply tests
# ---------------------------------------------------------------------------


class TestReply:
    """Tests for the Orders.reply method."""

    def test_returns_reply_response(self, orders_service, mock_session):
        """Verify reply() returns the parsed JSON response."""
        mock_session.make_request = MagicMock(return_value=SAMPLE_REPLY_RESPONSE)
        reply_id = "5050c104-1276-4483-8be8-ca598e698766"
        message = {"confirmed": True}

        result = orders_service.reply(reply_id=reply_id, message=message)

        assert result == SAMPLE_REPLY_RESPONSE

    def test_calls_correct_endpoint_with_reply_id(self, orders_service, mock_session):
        """Verify reply() includes reply_id in the endpoint."""
        mock_session.make_request = MagicMock(return_value={})
        reply_id = "5050c104-1276-4483-8be8-ca598e698766"
        message = {"confirmed": True}

        orders_service.reply(reply_id=reply_id, message=message)

        mock_session.make_request.assert_called_once_with(
            method="post",
            endpoint=f"/api/iserver/reply/{reply_id}",
            json_payload=message,
        )


# ---------------------------------------------------------------------------
# Orders.order_status tests
# ---------------------------------------------------------------------------


SAMPLE_ORDER_STATUS = {
    "sub_type": None,
    "request_id": "1",
    "order_id": 1915650539,
    "conid": 265598,
    "symbol": "AAPL",
    "side": "BUY",
    "order_type": "LMT",
    "status": "Submitted",
}


class TestOrderStatus:
    """Tests for the Orders.order_status method."""

    def test_returns_order_status(self, orders_service, mock_session):
        """Verify order_status() returns an OrderStatus model."""
        mock_session.make_request = MagicMock(return_value=SAMPLE_ORDER_STATUS)

        result = orders_service.order_status(order_id=ORDER_ID)

        assert isinstance(result, OrderStatus)
        assert result.order_id == 1915650539
        assert result.symbol == "AAPL"
        assert result.side == "BUY"

    def test_calls_correct_endpoint(self, orders_service, mock_session):
        """Verify order_status() GETs the correct endpoint."""
        mock_session.make_request = MagicMock(return_value={})

        orders_service.order_status(order_id=ORDER_ID)

        mock_session.make_request.assert_called_once_with(
            method="get",
            endpoint=f"/api/iserver/account/order/status/{ORDER_ID}",
        )

    def test_validates_empty_order_id(self, orders_service):
        """Verify order_status() raises IBCValidationError for empty order_id."""
        from ibc.exceptions import IBCValidationError
        with pytest.raises(IBCValidationError):
            orders_service.order_status(order_id='')


# ---------------------------------------------------------------------------
# Orders.place_orders_for_fa_group tests
# ---------------------------------------------------------------------------


class TestPlaceOrdersForFAGroup:
    """Tests for the Orders.place_orders_for_fa_group method."""

    def test_calls_correct_endpoint(self, orders_service, mock_session):
        """Verify place_orders_for_fa_group() POSTs to the correct endpoint."""
        mock_session.make_request = MagicMock(return_value={})

        orders_service.place_orders_for_fa_group(
            fa_group='MyGroup', orders=SAMPLE_BRACKET_PAYLOAD
        )

        mock_session.make_request.assert_called_once_with(
            method="post",
            endpoint="/api/iserver/account/orders/MyGroup",
            json_payload=SAMPLE_BRACKET_PAYLOAD,
        )

    def test_validates_empty_fa_group(self, orders_service):
        """Verify place_orders_for_fa_group() raises IBCValidationError for empty group."""
        from ibc.exceptions import IBCValidationError
        with pytest.raises(IBCValidationError):
            orders_service.place_orders_for_fa_group(fa_group='', orders={})


# ---------------------------------------------------------------------------
# Orders.place_whatif_orders tests
# ---------------------------------------------------------------------------


class TestPlaceWhatifOrders:
    """Tests for the Orders.place_whatif_orders method."""

    def test_calls_correct_endpoint(self, orders_service, mock_session):
        """Verify place_whatif_orders() POSTs to the plural /orders/whatif endpoint."""
        mock_session.make_request = MagicMock(return_value={})

        orders_service.place_whatif_orders(
            account_id=ACCOUNT_ID, orders=SAMPLE_BRACKET_PAYLOAD
        )

        mock_session.make_request.assert_called_once_with(
            method="post",
            endpoint=f"/api/iserver/account/{ACCOUNT_ID}/orders/whatif",
            json_payload=SAMPLE_BRACKET_PAYLOAD,
        )

    def test_validates_empty_account_id(self, orders_service):
        """Verify place_whatif_orders() raises IBCValidationError for empty account_id."""
        from ibc.exceptions import IBCValidationError
        with pytest.raises(IBCValidationError):
            orders_service.place_whatif_orders(account_id='', orders={})

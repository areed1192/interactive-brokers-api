"""Tests for the Trades service."""


from unittest.mock import MagicMock

import pytest

from ibc.models import Trade
from ibc.rest.trades import Trades


# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------

SAMPLE_TRADES = [
    {
        "execution_id": "exec1",
        "symbol": "AAPL",
        "side": "BUY",
        "size": 100.0,
        "price": 150.0,
        "account": "U1234567",
        "conid": 265598,
        "order_ref": "order1",
        "exchange": "SMART",
    },
    {
        "execution_id": "exec2",
        "symbol": "MSFT",
        "side": "SELL",
        "size": 50.0,
        "price": 350.0,
        "account": "U1234567",
        "conid": 272093,
        "order_ref": "order2",
        "exchange": "SMART",
    },
]


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def trades_service(mock_session, mock_client):
    """Create a Trades service with mocked session."""
    return Trades(ib_client=mock_client, ib_session=mock_session)


# ---------------------------------------------------------------------------
# Trades.get_trades tests
# ---------------------------------------------------------------------------


class TestGetTrades:
    """Tests for the Trades.get_trades method."""

    def test_returns_trade_models(self, trades_service, mock_session):
        """Verify get_trades() returns a list of Trade models."""
        mock_session.make_request = MagicMock(return_value=SAMPLE_TRADES)

        result = trades_service.get_trades()

        assert len(result) == 2
        assert all(isinstance(t, Trade) for t in result)
        assert result[0].execution_id == "exec1"
        assert result[0].symbol == "AAPL"
        assert result[1].symbol == "MSFT"

    def test_calls_correct_endpoint(self, trades_service, mock_session):
        """Verify get_trades() calls the correct API endpoint."""
        mock_session.make_request = MagicMock(return_value=[])

        trades_service.get_trades()

        mock_session.make_request.assert_called_once_with(
            method="get",
            endpoint="/api/iserver/account/trades",
        )

    def test_returns_empty_list_for_no_trades(self, trades_service, mock_session):
        """Verify get_trades() returns empty list when no trades exist."""
        mock_session.make_request = MagicMock(return_value=[])

        result = trades_service.get_trades()

        assert result == []

    def test_repr(self, trades_service):
        """Verify the service repr."""
        assert repr(trades_service) == "Trades()"

"""Tests for the MarketData service."""


from enum import Enum
from unittest.mock import MagicMock

import pytest

from ibc.exceptions import IBCValidationError
from ibc.models import HistoryData, MarketData as MarketDataModel
from ibc.rest.market_data import MarketData


# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------

SAMPLE_SNAPSHOT_RESPONSE = [
    {
        "conid": 265598,
        "31": "150.25",
        "84": "150.10",
        "86": "150.30",
    }
]

SAMPLE_HISTORY_RESPONSE = {
    "symbol": "AAPL",
    "data": [
        {"t": 1609459200000, "o": 133.52, "c": 132.69, "h": 134.74, "l": 131.72, "v": 143301887},
    ],
    "timePeriod": "1d",
}


class MockField(Enum):
    """Mock enum for MarketDataFields."""
    LAST_PRICE = "31"
    BID_PRICE = "84"
    ASK_PRICE = "86"


class MockBar(Enum):
    """Mock enum for bar size."""
    ONE_HOUR = "1h"


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def market_data_service(mock_session, mock_client):
    """Create a MarketData service with mocked session and accounts."""
    mock_client.accounts = MagicMock()
    mock_client.accounts._has_portfolio_been_called = True
    return MarketData(ib_client=mock_client, ib_session=mock_session)


# ---------------------------------------------------------------------------
# MarketData.__init__ tests
# ---------------------------------------------------------------------------


class TestMarketDataInit:
    """Tests for MarketData initialization."""

    def test_init_sets_client_and_session(self, mock_session, mock_client):
        """Verify __init__ stores client and session references."""
        md = MarketData(ib_client=mock_client, ib_session=mock_session)

        assert md.client is mock_client
        assert md.session is mock_session


# ---------------------------------------------------------------------------
# MarketData.snapshot tests
# ---------------------------------------------------------------------------


class TestSnapshot:
    """Tests for the MarketData.snapshot method."""

    def test_returns_snapshot_response(self, market_data_service, mock_session):
        """Verify snapshot() returns a list of MarketData models."""
        mock_session.make_request = MagicMock(return_value=SAMPLE_SNAPSHOT_RESPONSE)

        result = market_data_service.snapshot(contract_ids=["265598"])

        assert len(result) == 1
        assert isinstance(result[0], MarketDataModel)
        assert result[0].conid == 265598
        assert result[0].last_price == "150.25"

    def test_calls_correct_endpoint(self, market_data_service, mock_session):
        """Verify snapshot() calls the correct API endpoint."""
        mock_session.make_request = MagicMock(return_value={})

        market_data_service.snapshot(contract_ids=["265598"])

        mock_session.make_request.assert_called_once_with(
            method="get",
            endpoint="/api/iserver/marketdata/snapshot",
            params={
                "conids": "265598",
                "since": None,
                "fields": None,
            },
        )

    def test_joins_multiple_contract_ids(self, market_data_service, mock_session):
        """Verify snapshot() joins multiple contract IDs with commas."""
        mock_session.make_request = MagicMock(return_value={})

        market_data_service.snapshot(contract_ids=["265598", "8314"])

        _, kwargs = mock_session.make_request.call_args
        assert kwargs["params"]["conids"] == "265598,8314"

    def test_converts_enum_fields_to_values(self, market_data_service, mock_session):
        """Verify snapshot() converts Enum field values to their string values."""
        mock_session.make_request = MagicMock(return_value={})

        market_data_service.snapshot(
            contract_ids=["265598"],
            fields=[MockField.LAST_PRICE, MockField.BID_PRICE],
        )

        _, kwargs = mock_session.make_request.call_args
        assert kwargs["params"]["fields"] == "31,84"

    def test_passes_string_fields_directly(self, market_data_service, mock_session):
        """Verify snapshot() passes string field values directly."""
        mock_session.make_request = MagicMock(return_value={})

        market_data_service.snapshot(
            contract_ids=["265598"],
            fields=["31", "84"],
        )

        _, kwargs = mock_session.make_request.call_args
        assert kwargs["params"]["fields"] == "31,84"

    def test_passes_since_parameter(self, market_data_service, mock_session):
        """Verify snapshot() passes the since parameter."""
        mock_session.make_request = MagicMock(return_value={})

        market_data_service.snapshot(contract_ids=["265598"], since=1609459200)

        _, kwargs = mock_session.make_request.call_args
        assert kwargs["params"]["since"] == 1609459200


# ---------------------------------------------------------------------------
# MarketData.market_history tests
# ---------------------------------------------------------------------------


class TestMarketHistory:
    """Tests for the MarketData.market_history method."""

    def test_returns_history_response(self, market_data_service, mock_session):
        """Verify market_history() returns a HistoryData model."""
        mock_session.make_request = MagicMock(return_value=SAMPLE_HISTORY_RESPONSE)

        result = market_data_service.market_history(
            contract_id="265598", period="1d"
        )

        assert isinstance(result, HistoryData)
        assert result.symbol == "AAPL"
        assert result.time_period == "1d"
        assert len(result.data) == 1
        assert result.data[0].open == 133.52

    def test_calls_correct_endpoint(self, market_data_service, mock_session):
        """Verify market_history() calls the correct API endpoint."""
        mock_session.make_request = MagicMock(return_value={})

        market_data_service.market_history(contract_id="265598", period="1d")

        mock_session.make_request.assert_called_once_with(
            method="get",
            endpoint="/api/iserver/marketdata/history",
            params={
                "conid": "265598",
                "period": "1d",
                "bar": None,
                "exchange": None,
                "outsideRth": True,
            },
        )

    def test_converts_enum_bar_to_value(self, market_data_service, mock_session):
        """Verify market_history() converts Enum bar to its string value."""
        mock_session.make_request = MagicMock(return_value={})

        market_data_service.market_history(
            contract_id="265598", period="1d", market_bar=MockBar.ONE_HOUR
        )

        _, kwargs = mock_session.make_request.call_args
        assert kwargs["params"]["bar"] == "1h"

    def test_passes_exchange_parameter(self, market_data_service, mock_session):
        """Verify market_history() passes the exchange parameter."""
        mock_session.make_request = MagicMock(return_value={})

        market_data_service.market_history(
            contract_id="265598", period="1d", exchange="NASDAQ"
        )

        _, kwargs = mock_session.make_request.call_args
        assert kwargs["params"]["exchange"] == "NASDAQ"

    def test_outside_rth_defaults_to_true(self, market_data_service, mock_session):
        """Verify outside_regular_trading_hours defaults to True."""
        mock_session.make_request = MagicMock(return_value={})

        market_data_service.market_history(contract_id="265598", period="1d")

        _, kwargs = mock_session.make_request.call_args
        assert kwargs["params"]["outsideRth"] is True

    def test_outside_rth_can_be_disabled(self, market_data_service, mock_session):
        """Verify outside_regular_trading_hours can be set to False."""
        mock_session.make_request = MagicMock(return_value={})

        market_data_service.market_history(
            contract_id="265598",
            period="1d",
            outside_regular_trading_hours=False,
        )

        _, kwargs = mock_session.make_request.call_args
        assert kwargs["params"]["outsideRth"] is False


# ---------------------------------------------------------------------------
# MarketData.unsubscribe tests
# ---------------------------------------------------------------------------


class TestUnsubscribe:
    """Tests for the MarketData.unsubscribe method."""

    def test_calls_correct_endpoint(self, market_data_service, mock_session):
        """Verify unsubscribe() calls the correct endpoint."""
        mock_session.make_request = MagicMock(return_value={"confirmed": True})

        result = market_data_service.unsubscribe(contract_id="265598")

        assert result == {"confirmed": True}
        mock_session.make_request.assert_called_once_with(
            method="get",
            endpoint="/api/iserver/marketdata/265598/unsubscribe",
        )

    def test_validates_empty_contract_id(self, market_data_service):
        """Verify unsubscribe() raises IBCValidationError for empty ID."""
        with pytest.raises(IBCValidationError):
            market_data_service.unsubscribe(contract_id='')


# ---------------------------------------------------------------------------
# MarketData.unsubscribe_all tests
# ---------------------------------------------------------------------------


class TestUnsubscribeAll:
    """Tests for the MarketData.unsubscribe_all method."""

    def test_calls_correct_endpoint(self, market_data_service, mock_session):
        """Verify unsubscribe_all() calls the correct endpoint."""
        mock_session.make_request = MagicMock(return_value={"confirmed": True})

        result = market_data_service.unsubscribe_all()

        assert result == {"confirmed": True}
        mock_session.make_request.assert_called_once_with(
            method="get",
            endpoint="/api/iserver/marketdata/unsubscribeall",
        )


# ---------------------------------------------------------------------------
# MarketData.market_history_beta tests
# ---------------------------------------------------------------------------


class TestMarketHistoryBeta:
    """Tests for the MarketData.market_history_beta method."""

    def test_calls_correct_endpoint(self, market_data_service, mock_session):
        """Verify market_history_beta() calls the /hmds/history endpoint."""
        mock_session.make_request = MagicMock(return_value=SAMPLE_HISTORY_RESPONSE)

        result = market_data_service.market_history_beta(
            contract_id="265598", period="1d"
        )

        assert isinstance(result, HistoryData)
        assert result.symbol == "AAPL"
        mock_session.make_request.assert_called_once_with(
            method="get",
            endpoint="/api/hmds/history",
            params={
                "conid": "265598",
                "period": "1d",
                "bar": None,
                "outsideRth": True,
            },
        )

    def test_converts_enum_bar(self, market_data_service, mock_session):
        """Verify market_history_beta() converts Enum bar value."""
        mock_session.make_request = MagicMock(return_value={})

        market_data_service.market_history_beta(
            contract_id="265598", period="1d", market_bar=MockBar.ONE_HOUR
        )

        _, kwargs = mock_session.make_request.call_args
        assert kwargs["params"]["bar"] == "1h"


# ---------------------------------------------------------------------------
# MarketData.snapshot_beta tests
# ---------------------------------------------------------------------------


class TestSnapshotBeta:
    """Tests for the MarketData.snapshot_beta method."""

    def test_calls_correct_endpoint(self, market_data_service, mock_session):
        """Verify snapshot_beta() calls the /md/snapshot endpoint."""
        mock_session.make_request = MagicMock(return_value=SAMPLE_SNAPSHOT_RESPONSE)

        result = market_data_service.snapshot_beta(contract_ids=["265598"])

        assert len(result) == 1
        assert isinstance(result[0], MarketDataModel)
        assert result[0].conid == 265598
        mock_session.make_request.assert_called_once_with(
            method="get",
            endpoint="/api/md/snapshot",
            params={"conids": "265598", "fields": None},
        )

    def test_converts_enum_fields(self, market_data_service, mock_session):
        """Verify snapshot_beta() converts Enum fields."""
        mock_session.make_request = MagicMock(return_value=[])

        market_data_service.snapshot_beta(
            contract_ids=["265598"],
            fields=[MockField.LAST_PRICE, MockField.BID_PRICE],
        )

        _, kwargs = mock_session.make_request.call_args
        assert kwargs["params"]["fields"] == "31,84"


# ---------------------------------------------------------------------------
# MarketData.scanner_beta tests
# ---------------------------------------------------------------------------


SAMPLE_SCANNER_PAYLOAD = {
    "instrument": "STK",
    "type": "TOP_PERC_GAIN",
    "location": "STK.US.MAJOR",
    "size": "25",
}


class TestScannerBeta:
    """Tests for the MarketData.scanner_beta method."""

    def test_calls_correct_endpoint(self, market_data_service, mock_session):
        """Verify scanner_beta() POSTs to the /hmds/scanner endpoint."""
        mock_session.make_request = MagicMock(return_value=[])

        market_data_service.scanner_beta(scanner=SAMPLE_SCANNER_PAYLOAD)

        mock_session.make_request.assert_called_once_with(
            method="post",
            endpoint="/api/hmds/scanner",
            json_payload=SAMPLE_SCANNER_PAYLOAD,
        )

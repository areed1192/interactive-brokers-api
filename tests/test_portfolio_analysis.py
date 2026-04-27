"""Tests for the PortfolioAnalysis service."""


from unittest.mock import MagicMock

import pytest

from ibc.exceptions import IBCValidationError
from ibc.models import Transactions
from ibc.rest.portfolio_analysis import PortfolioAnalysis


# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------

SAMPLE_PERFORMANCE = {
    "currencyType": "base",
    "nav": {"data": [{"baseCurrency": "USD"}]},
}

SAMPLE_SUMMARY = {
    "total": {"chg": 1000.0, "endVal": 50000.0},
}

SAMPLE_TRANSACTIONS = {
    "id": "txn-batch-1",
    "currency": "USD",
    "transactions": [
        {
            "acctid": "U1234567",
            "conid": 265598,
            "cur": "USD",
            "fxRate": 1.0,
            "desc": "AAPL",
            "type": "BUY",
            "qty": 10.0,
            "pr": 150.0,
            "amt": -1500.0,
            "date": "20240101",
        }
    ],
}

ACCOUNT_IDS = ["U1234567"]


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def pa_service(mock_session, mock_client):
    """Create a PortfolioAnalysis service with mocked session."""
    return PortfolioAnalysis(ib_client=mock_client, ib_session=mock_session)


# ---------------------------------------------------------------------------
# PortfolioAnalysis.account_performance tests
# ---------------------------------------------------------------------------


class TestAccountPerformance:
    """Tests for the PortfolioAnalysis.account_performance method."""

    def test_returns_performance(self, pa_service, mock_session):
        """Verify account_performance() returns the response."""
        mock_session.make_request = MagicMock(return_value=SAMPLE_PERFORMANCE)

        result = pa_service.account_performance(
            account_ids=ACCOUNT_IDS, frequency="D"
        )

        assert result == SAMPLE_PERFORMANCE

    def test_calls_correct_endpoint(self, pa_service, mock_session):
        """Verify account_performance() calls the correct API endpoint."""
        mock_session.make_request = MagicMock(return_value={})

        pa_service.account_performance(account_ids=ACCOUNT_IDS, frequency="M")

        mock_session.make_request.assert_called_once_with(
            method="post",
            endpoint="/api/pa/performance",
            json_payload={"acctIds": ACCOUNT_IDS, "freq": "M"},
        )

    def test_validates_empty_account_ids(self, pa_service):
        """Verify account_performance() raises IBCValidationError for empty list."""
        with pytest.raises(IBCValidationError):
            pa_service.account_performance(account_ids=[], frequency="D")

    def test_validates_none_account_ids(self, pa_service):
        """Verify account_performance() raises IBCValidationError for None."""
        with pytest.raises(IBCValidationError):
            pa_service.account_performance(account_ids=None, frequency="D")

    def test_accepts_enum_frequency(self, pa_service, mock_session):
        """Verify account_performance() converts Enum frequency to value."""
        from enum import Enum

        class Freq(Enum):
            """Frequency Enum for testing."""

            DAILY = "D"

        mock_session.make_request = MagicMock(return_value={})

        pa_service.account_performance(account_ids=ACCOUNT_IDS, frequency=Freq.DAILY)

        mock_session.make_request.assert_called_once_with(
            method="post",
            endpoint="/api/pa/performance",
            json_payload={"acctIds": ACCOUNT_IDS, "freq": "D"},
        )


# ---------------------------------------------------------------------------
# PortfolioAnalysis.account_summary tests
# ---------------------------------------------------------------------------


class TestAccountSummary:
    """Tests for the PortfolioAnalysis.account_summary method."""

    def test_returns_summary(self, pa_service, mock_session):
        """Verify account_summary() returns the response."""
        mock_session.make_request = MagicMock(return_value=SAMPLE_SUMMARY)

        result = pa_service.account_summary(account_ids=ACCOUNT_IDS)

        assert result == SAMPLE_SUMMARY

    def test_calls_correct_endpoint(self, pa_service, mock_session):
        """Verify account_summary() calls the correct API endpoint."""
        mock_session.make_request = MagicMock(return_value={})

        pa_service.account_summary(account_ids=ACCOUNT_IDS)

        mock_session.make_request.assert_called_once_with(
            method="post",
            endpoint="/api/pa/summary",
            json_payload={"acctIds": ACCOUNT_IDS},
        )

    def test_validates_empty_account_ids(self, pa_service):
        """Verify account_summary() raises IBCValidationError for empty list."""
        with pytest.raises(IBCValidationError):
            pa_service.account_summary(account_ids=[])

    def test_validates_none_account_ids(self, pa_service):
        """Verify account_summary() raises IBCValidationError for None."""
        with pytest.raises(IBCValidationError):
            pa_service.account_summary(account_ids=None)


# ---------------------------------------------------------------------------
# PortfolioAnalysis.transactions_history tests
# ---------------------------------------------------------------------------


class TestTransactionsHistory:
    """Tests for the PortfolioAnalysis.transactions_history method."""

    def test_returns_transactions_model(self, pa_service, mock_session):
        """Verify transactions_history() returns a Transactions model."""
        mock_session.make_request = MagicMock(return_value=SAMPLE_TRANSACTIONS)

        result = pa_service.transactions_history(
            account_ids=ACCOUNT_IDS, contract_ids=["265598"]
        )

        assert isinstance(result, Transactions)
        assert result.id == "txn-batch-1"
        assert result.currency == "USD"

    def test_calls_correct_endpoint(self, pa_service, mock_session):
        """Verify transactions_history() calls the correct API endpoint."""
        mock_session.make_request = MagicMock(return_value=SAMPLE_TRANSACTIONS)

        pa_service.transactions_history(
            account_ids=ACCOUNT_IDS,
            contract_ids=["265598"],
            currency="EUR",
            days=30,
        )

        mock_session.make_request.assert_called_once_with(
            method="post",
            endpoint="/api/pa/transactions",
            json_payload={
                "acctIds": ACCOUNT_IDS,
                "conids": ["265598"],
                "currency": "EUR",
                "days": 30,
            },
        )

    def test_default_currency_and_days(self, pa_service, mock_session):
        """Verify transactions_history() uses default currency and days."""
        mock_session.make_request = MagicMock(return_value=SAMPLE_TRANSACTIONS)

        pa_service.transactions_history(account_ids=ACCOUNT_IDS)

        call_kwargs = mock_session.make_request.call_args
        payload = call_kwargs[1]["json_payload"] if call_kwargs[1] else call_kwargs.kwargs["json_payload"]
        assert payload["currency"] == "USD"
        assert payload["days"] == 90

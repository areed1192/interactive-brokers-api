"""Tests for the Accounts service."""


from unittest.mock import MagicMock

import pytest

from ibc.models import Account
from ibc.rest.accounts import Accounts

# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------

SAMPLE_ACCOUNTS_RESPONSE = {
    "accounts": ["U1234567"],
    "aliases": {"U1234567": "Paper Account"},
    "selectedAccount": "U1234567",
}

SAMPLE_ACCOUNTS_DICT_RESPONSE = {
    "accounts": [
        {
            "id": "U1234567",
            "accountId": "U1234567",
            "accountTitle": "Paper Account",
            "displayName": "Paper Trading",
            "currency": "USD",
            "type": "INDIVIDUAL",
        }
    ],
}

SAMPLE_PNL_RESPONSE = {
    "upnl": {
        "U1234567": {
            "rowType": 1,
            "dpl": 100.50,
            "nl": 50000.00,
            "upl": 200.75,
            "el": 49800.00,
            "mv": 50200.75,
        }
    }
}


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def accounts_service(mock_session, mock_client):
    """Create an Accounts service with mocked session."""
    return Accounts(ib_client=mock_client, ib_session=mock_session)


# ---------------------------------------------------------------------------
# Accounts.accounts tests
# ---------------------------------------------------------------------------


class TestAccountsAccounts:
    """Tests for the Accounts.accounts method."""

    def test_returns_account_models_from_dicts(self, accounts_service, mock_session):
        """Verify accounts() returns Account models when response has dict entries."""
        mock_session.make_request = MagicMock(return_value=SAMPLE_ACCOUNTS_DICT_RESPONSE)

        result = accounts_service.accounts()

        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], Account)
        assert result[0].account_id == "U1234567"
        assert result[0].account_title == "Paper Account"
        assert result[0].currency == "USD"

    def test_returns_account_models_from_strings(self, accounts_service, mock_session):
        """Verify accounts() handles string account IDs in the response."""
        mock_session.make_request = MagicMock(return_value=SAMPLE_ACCOUNTS_RESPONSE)

        result = accounts_service.accounts()

        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], Account)
        assert result[0].id == "U1234567"

    def test_returns_empty_list_for_empty_response(self, accounts_service, mock_session):
        """Verify accounts() returns empty list when no accounts key."""
        mock_session.make_request = MagicMock(return_value={})

        result = accounts_service.accounts()

        assert result == []

    def test_calls_correct_endpoint(self, accounts_service, mock_session):
        """Verify accounts() calls the correct API endpoint."""
        mock_session.make_request = MagicMock(return_value={})

        accounts_service.accounts()

        mock_session.make_request.assert_called_once_with(
            method="get",
            endpoint="/api/iserver/accounts",
        )


# ---------------------------------------------------------------------------
# Accounts.pnl_server_account tests
# ---------------------------------------------------------------------------


class TestAccountsPnlServerAccount:
    """Tests for the Accounts.pnl_server_account method."""

    def test_returns_pnl_response(self, accounts_service, mock_session):
        """Verify pnl_server_account() returns the parsed JSON response."""
        mock_session.make_request = MagicMock(return_value=SAMPLE_PNL_RESPONSE)

        result = accounts_service.pnl_server_account()

        assert result == SAMPLE_PNL_RESPONSE

    def test_calls_correct_endpoint(self, accounts_service, mock_session):
        """Verify pnl_server_account() calls the correct API endpoint."""
        mock_session.make_request = MagicMock(return_value={})

        accounts_service.pnl_server_account()

        mock_session.make_request.assert_called_once_with(
            method="get",
            endpoint="/api/iserver/account/pnl/partitioned",
        )

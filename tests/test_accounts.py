"""Tests for the Accounts service."""


from unittest.mock import MagicMock

import pytest

from ibc.rest.accounts import Accounts


# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------

SAMPLE_ACCOUNTS_RESPONSE = {
    "accounts": ["U1234567"],
    "aliases": {"U1234567": "Paper Account"},
    "selectedAccount": "U1234567",
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

    def test_returns_accounts_response(self, accounts_service, mock_session):
        """Verify accounts() returns the parsed JSON response."""
        mock_session.make_request = MagicMock(return_value=SAMPLE_ACCOUNTS_RESPONSE)

        result = accounts_service.accounts()

        assert result == SAMPLE_ACCOUNTS_RESPONSE

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

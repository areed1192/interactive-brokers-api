"""Tests for the PnL service."""


from unittest.mock import MagicMock

import pytest

from ibc.rest.pnl import PnL

# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------

SAMPLE_PNL = {
    "upnl": {"U1234567": {"dpl": 500.0, "nl": 10000.0, "upl": 200.0}},
}


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def pnl_service(mock_session, mock_client):
    """Create a PnL service with mocked session."""
    return PnL(ib_client=mock_client, ib_session=mock_session)


# ---------------------------------------------------------------------------
# PnL.pnl_server_account tests
# ---------------------------------------------------------------------------


class TestPnlServerAccount:
    """Tests for the PnL.pnl_server_account method."""

    def test_delegates_to_accounts_service(self, pnl_service, mock_client):
        """Verify pnl_server_account() delegates to accounts.pnl_server_account()."""
        mock_client.accounts.pnl_server_account = MagicMock(return_value=SAMPLE_PNL)

        result = pnl_service.pnl_server_account()

        assert result == SAMPLE_PNL
        mock_client.accounts.pnl_server_account.assert_called_once()

    def test_repr(self, pnl_service):
        """Verify the service repr."""
        assert repr(pnl_service) == "PnL()"

"""Tests for the PortfolioAccounts service."""


from unittest.mock import MagicMock

import pytest

from ibc.rest.portfolio import PortfolioAccounts

# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------

SAMPLE_ACCOUNTS_RESPONSE = [
    {
        "id": "U1234567",
        "accountId": "U1234567",
        "accountTitle": "Paper Account",
        "type": "INDIVIDUAL",
    }
]

SAMPLE_SUBACCOUNTS_RESPONSE = [
    {"acctId": "U1234567", "desc": "Sub Account 1"}
]

SAMPLE_METADATA_RESPONSE = {
    "id": "U1234567",
    "accountTitle": "Paper Account",
    "currency": "USD",
}

SAMPLE_SUMMARY_RESPONSE = {
    "totalcashvalue": {"amount": 50000.00, "currency": "USD"},
    "netliquidation": {"amount": 100000.00, "currency": "USD"},
}

SAMPLE_LEDGER_RESPONSE = {
    "USD": {"cashbalance": 50000.00, "settledcash": 49000.00}
}

SAMPLE_ALLOCATION_RESPONSE = {
    "assetClass": {"long": {"STK": 80.0, "BOND": 20.0}}
}

SAMPLE_POSITIONS_RESPONSE = [
    {
        "acctId": "U1234567",
        "conid": 265598,
        "contractDesc": "AAPL",
        "position": 100,
        "mktPrice": 150.25,
    }
]

ACCOUNT_ID = "U1234567"
CONTRACT_ID = "265598"


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def portfolio_service(mock_session, mock_client):
    """Create a PortfolioAccounts service with mocked session."""
    return PortfolioAccounts(ib_client=mock_client, ib_session=mock_session)


# ---------------------------------------------------------------------------
# PortfolioAccounts.accounts tests
# ---------------------------------------------------------------------------


class TestPortfolioAccounts:
    """Tests for the PortfolioAccounts.accounts method."""

    def test_returns_accounts_response(self, portfolio_service, mock_session):
        """Verify accounts() returns the parsed JSON response."""
        mock_session.make_request = MagicMock(return_value=SAMPLE_ACCOUNTS_RESPONSE)

        result = portfolio_service.accounts()

        assert result == SAMPLE_ACCOUNTS_RESPONSE

    def test_calls_correct_endpoint(self, portfolio_service, mock_session):
        """Verify accounts() calls the correct API endpoint."""
        mock_session.make_request = MagicMock(return_value=[])

        portfolio_service.accounts()

        mock_session.make_request.assert_called_once_with(
            method="get",
            endpoint="/api/portfolio/accounts",
        )

    def test_sets_portfolio_called_flag(self, portfolio_service, mock_session):
        """Verify accounts() sets _has_portfolio_been_called to True."""
        mock_session.make_request = MagicMock(return_value=[])

        portfolio_service.accounts()

        assert portfolio_service._has_portfolio_been_called is True


# ---------------------------------------------------------------------------
# PortfolioAccounts.subaccounts tests
# ---------------------------------------------------------------------------


class TestPortfolioSubaccounts:
    """Tests for the PortfolioAccounts.subaccounts method."""

    def test_returns_subaccounts_response(self, portfolio_service, mock_session):
        """Verify subaccounts() returns the parsed JSON response."""
        mock_session.make_request = MagicMock(return_value=SAMPLE_SUBACCOUNTS_RESPONSE)

        result = portfolio_service.subaccounts()

        assert result == SAMPLE_SUBACCOUNTS_RESPONSE

    def test_calls_correct_endpoint(self, portfolio_service, mock_session):
        """Verify subaccounts() calls the correct API endpoint."""
        mock_session.make_request = MagicMock(return_value=[])

        portfolio_service.subaccounts()

        mock_session.make_request.assert_called_once_with(
            method="get",
            endpoint="/api/portfolio/subaccounts",
        )

    def test_sets_sub_portfolio_called_flag(self, portfolio_service, mock_session):
        """Verify subaccounts() sets _has_sub_portfolio_been_called to True."""
        mock_session.make_request = MagicMock(return_value=[])

        portfolio_service.subaccounts()

        assert portfolio_service._has_sub_portfolio_been_called is True


# ---------------------------------------------------------------------------
# PortfolioAccounts.account_metadata tests
# ---------------------------------------------------------------------------


class TestAccountMetadata:
    """Tests for the PortfolioAccounts.account_metadata method."""

    def test_returns_metadata_response(self, portfolio_service, mock_session):
        """Verify account_metadata() returns the parsed JSON response."""
        mock_session.make_request = MagicMock(return_value=SAMPLE_METADATA_RESPONSE)

        portfolio_service._has_portfolio_been_called = True
        portfolio_service._has_sub_portfolio_been_called = True
        result = portfolio_service.account_metadata(account_id=ACCOUNT_ID)

        assert result == SAMPLE_METADATA_RESPONSE

    def test_calls_correct_endpoint(self, portfolio_service, mock_session):
        """Verify account_metadata() calls the correct API endpoint."""
        mock_session.make_request = MagicMock(return_value={})

        portfolio_service._has_portfolio_been_called = True
        portfolio_service._has_sub_portfolio_been_called = True
        portfolio_service.account_metadata(account_id=ACCOUNT_ID)

        mock_session.make_request.assert_called_once_with(
            method="get",
            endpoint=f"/api/portfolio/{ACCOUNT_ID}/meta",
        )

    def test_auto_calls_accounts_if_not_called(self, portfolio_service, mock_session):
        """Verify account_metadata() auto-calls accounts() and subaccounts() if needed."""
        responses = iter([[], [], SAMPLE_METADATA_RESPONSE])
        mock_session.make_request = MagicMock(side_effect=lambda **kw: next(responses))

        result = portfolio_service.account_metadata(account_id=ACCOUNT_ID)

        assert mock_session.make_request.call_count == 3
        assert result == SAMPLE_METADATA_RESPONSE


# ---------------------------------------------------------------------------
# PortfolioAccounts.account_summary tests
# ---------------------------------------------------------------------------


class TestAccountSummary:
    """Tests for the PortfolioAccounts.account_summary method."""

    def test_calls_correct_endpoint(self, portfolio_service, mock_session):
        """Verify account_summary() calls the correct API endpoint."""
        mock_session.make_request = MagicMock(return_value={})

        portfolio_service._has_portfolio_been_called = True
        portfolio_service._has_sub_portfolio_been_called = True
        portfolio_service.account_summary(account_id=ACCOUNT_ID)

        mock_session.make_request.assert_called_once_with(
            method="get",
            endpoint=f"/api/portfolio/{ACCOUNT_ID}/summary",
        )


# ---------------------------------------------------------------------------
# PortfolioAccounts.account_ledger tests
# ---------------------------------------------------------------------------


class TestAccountLedger:
    """Tests for the PortfolioAccounts.account_ledger method."""

    def test_calls_correct_endpoint(self, portfolio_service, mock_session):
        """Verify account_ledger() calls the correct API endpoint."""
        mock_session.make_request = MagicMock(return_value={})

        portfolio_service._has_portfolio_been_called = True
        portfolio_service._has_sub_portfolio_been_called = True
        portfolio_service.account_ledger(account_id=ACCOUNT_ID)

        mock_session.make_request.assert_called_once_with(
            method="get",
            endpoint=f"/api/portfolio/{ACCOUNT_ID}/ledger",
        )


# ---------------------------------------------------------------------------
# PortfolioAccounts.account_allocation tests
# ---------------------------------------------------------------------------


class TestAccountAllocation:
    """Tests for the PortfolioAccounts.account_allocation method."""

    def test_calls_correct_endpoint(self, portfolio_service, mock_session):
        """Verify account_allocation() calls the correct API endpoint."""
        mock_session.make_request = MagicMock(return_value={})

        portfolio_service._has_portfolio_been_called = True
        portfolio_service._has_sub_portfolio_been_called = True
        portfolio_service.account_allocation(account_id=ACCOUNT_ID)

        mock_session.make_request.assert_called_once_with(
            method="get",
            endpoint=f"/api/portfolio/{ACCOUNT_ID}/allocation",
        )


# ---------------------------------------------------------------------------
# PortfolioAccounts.portfolio_allocation tests
# ---------------------------------------------------------------------------


class TestPortfolioAllocation:
    """Tests for the PortfolioAccounts.portfolio_allocation method."""

    def test_calls_correct_endpoint_with_post(self, portfolio_service, mock_session):
        """Verify portfolio_allocation() uses POST with account IDs payload."""
        mock_session.make_request = MagicMock(return_value={})

        portfolio_service._has_portfolio_been_called = True
        portfolio_service._has_sub_portfolio_been_called = True
        portfolio_service.portfolio_allocation(account_ids=[ACCOUNT_ID])

        mock_session.make_request.assert_called_once_with(
            method="post",
            endpoint="/api/portfolio/allocation",
            json_payload={"acctIds": [ACCOUNT_ID]},
        )


# ---------------------------------------------------------------------------
# PortfolioAccounts.portfolio_positions tests
# ---------------------------------------------------------------------------


class TestPortfolioPositions:
    """Tests for the PortfolioAccounts.portfolio_positions method."""

    def test_calls_correct_endpoint_with_page(self, portfolio_service, mock_session):
        """Verify portfolio_positions() includes page_id in the endpoint."""
        mock_session.make_request = MagicMock(return_value=[])

        portfolio_service._has_portfolio_been_called = True
        portfolio_service._has_sub_portfolio_been_called = True
        portfolio_service.portfolio_positions(account_id=ACCOUNT_ID, page_id=2)

        mock_session.make_request.assert_called_once_with(
            method="get",
            endpoint=f"/api/portfolio/{ACCOUNT_ID}/positions/2",
            params={"sort": None, "direction": None, "period": None},
        )

    def test_defaults_to_page_zero(self, portfolio_service, mock_session):
        """Verify portfolio_positions() defaults to page 0."""
        mock_session.make_request = MagicMock(return_value=[])

        portfolio_service._has_portfolio_been_called = True
        portfolio_service._has_sub_portfolio_been_called = True
        portfolio_service.portfolio_positions(account_id=ACCOUNT_ID)

        _, kwargs = mock_session.make_request.call_args
        assert "/positions/0" in kwargs["endpoint"]


# ---------------------------------------------------------------------------
# PortfolioAccounts.position_by_contract_id tests
# ---------------------------------------------------------------------------


class TestPositionByContractId:
    """Tests for the PortfolioAccounts.position_by_contract_id method."""

    def test_calls_correct_endpoint(self, portfolio_service, mock_session):
        """Verify position_by_contract_id() includes contract_id in the endpoint."""
        mock_session.make_request = MagicMock(return_value={})

        portfolio_service._has_portfolio_been_called = True
        portfolio_service._has_sub_portfolio_been_called = True
        portfolio_service.position_by_contract_id(
            account_id=ACCOUNT_ID, contract_id=CONTRACT_ID
        )

        mock_session.make_request.assert_called_once_with(
            method="get",
            endpoint=f"/api/portfolio/{ACCOUNT_ID}/position/{CONTRACT_ID}",
        )


# ---------------------------------------------------------------------------
# PortfolioAccounts.positions_by_contract_id tests
# ---------------------------------------------------------------------------


class TestPositionsByContractId:
    """Tests for the PortfolioAccounts.positions_by_contract_id method."""

    def test_calls_correct_endpoint(self, portfolio_service, mock_session):
        """Verify positions_by_contract_id() uses the multi-account endpoint."""
        mock_session.make_request = MagicMock(return_value={})

        portfolio_service._has_portfolio_been_called = True
        portfolio_service._has_sub_portfolio_been_called = True
        portfolio_service.positions_by_contract_id(contract_id=CONTRACT_ID)

        mock_session.make_request.assert_called_once_with(
            method="get",
            endpoint=f"/api/portfolio/positions/{CONTRACT_ID}",
        )


# ---------------------------------------------------------------------------
# PortfolioAccounts.invalidate_positions_cache tests
# ---------------------------------------------------------------------------


class TestInvalidatePositionsCache:
    """Tests for the PortfolioAccounts.invalidate_positions_cache method."""

    def test_calls_correct_endpoint_with_post(self, portfolio_service, mock_session):
        """Verify invalidate_positions_cache() uses POST method."""
        mock_session.make_request = MagicMock(return_value=None)

        portfolio_service.invalidate_positions_cache(account_id=ACCOUNT_ID)

        mock_session.make_request.assert_called_once_with(
            method="post",
            endpoint=f"/api/portfolio/{ACCOUNT_ID}/positions/invalidate",
        )


# ---------------------------------------------------------------------------
# PortfolioAccounts.subaccounts2 tests
# ---------------------------------------------------------------------------


SAMPLE_SUBACCOUNTS2_RESPONSE = {
    "metadata": {"total": 150, "pageSize": 20, "pageNum": 0},
    "subaccounts": [{"acctId": "U1234567", "desc": "Sub Account 1"}],
}


class TestSubaccounts2:
    """Tests for the PortfolioAccounts.subaccounts2 method."""

    def test_returns_paginated_response(self, portfolio_service, mock_session):
        """Verify subaccounts2() returns the parsed JSON response."""
        mock_session.make_request = MagicMock(return_value=SAMPLE_SUBACCOUNTS2_RESPONSE)

        result = portfolio_service.subaccounts2(page=0)

        assert result == SAMPLE_SUBACCOUNTS2_RESPONSE

    def test_calls_correct_endpoint_with_page(self, portfolio_service, mock_session):
        """Verify subaccounts2() calls the correct endpoint with page param."""
        mock_session.make_request = MagicMock(return_value={})

        portfolio_service.subaccounts2(page=2)

        mock_session.make_request.assert_called_once_with(
            method="get",
            endpoint="/api/portfolio/subaccounts2",
            params={"page": "2"},
        )

    def test_sets_sub_portfolio_called_flag(self, portfolio_service, mock_session):
        """Verify subaccounts2() sets _has_sub_portfolio_been_called to True."""
        mock_session.make_request = MagicMock(return_value={})

        portfolio_service.subaccounts2()

        assert portfolio_service._has_sub_portfolio_been_called is True

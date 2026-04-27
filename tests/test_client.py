"""Tests for the InteractiveBrokersClient."""


from unittest.mock import patch

import pytest

from ibc.client import InteractiveBrokersClient
from ibc.rest.accounts import Accounts
from ibc.rest.alert import Alerts
from ibc.rest.contract import Contracts
from ibc.rest.customer import Customer
from ibc.rest.data import Data
from ibc.rest.market_data import MarketData
from ibc.rest.orders import Orders
from ibc.rest.pnl import PnL
from ibc.rest.portfolio import PortfolioAccounts
from ibc.rest.portfolio_analysis import PortfolioAnalysis
from ibc.rest.scanner import Scanners
from ibc.rest.trades import Trades
from ibc.session import InteractiveBrokersSession
from ibc.utils.auth import InteractiveBrokersAuthentication
from ibc.utils.gateway import ClientPortalGateway

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

@pytest.fixture
def ibc_client():
    """Create an InteractiveBrokersClient with mocked gateway setup."""
    with patch.object(ClientPortalGateway, "setup"):
        client = InteractiveBrokersClient(
            account_number="U1234567",
            password="test_password",
        )
    return client


# ---------------------------------------------------------------------------
# InteractiveBrokersClient tests
# ---------------------------------------------------------------------------


class TestInteractiveBrokersClientInit:
    """Tests for InteractiveBrokersClient initialization."""

    def test_creates_instance_of_client(self, ibc_client):
        """Verify the client is an InteractiveBrokersClient instance."""
        assert isinstance(ibc_client, InteractiveBrokersClient)

    def test_stores_account_number(self, ibc_client):
        """Verify account number is stored correctly."""
        assert ibc_client.account_number == "U1234567"

    def test_creates_session(self, ibc_client):
        """Verify session is created as InteractiveBrokersSession."""
        assert isinstance(ibc_client._session, InteractiveBrokersSession)

    def test_creates_auth_service(self, ibc_client):
        """Verify authentication service is created."""
        assert isinstance(ibc_client.authentication, InteractiveBrokersAuthentication)

    def test_creates_gateway(self, ibc_client):
        """Verify client portal gateway is created."""
        assert isinstance(ibc_client.client_portal, ClientPortalGateway)


# ---------------------------------------------------------------------------
# Service property tests
# ---------------------------------------------------------------------------


class TestInteractiveBrokersClientServices:
    """Tests for InteractiveBrokersClient service properties."""

    def test_accounts_returns_accounts_instance(self, ibc_client):
        """Verify accounts property returns an Accounts instance."""
        assert isinstance(ibc_client.accounts, Accounts)

    def test_alerts_returns_alerts_instance(self, ibc_client):
        """Verify alerts property returns an Alerts instance."""
        assert isinstance(ibc_client.alerts, Alerts)

    def test_contracts_returns_contracts_instance(self, ibc_client):
        """Verify contracts property returns a Contracts instance."""
        assert isinstance(ibc_client.contracts, Contracts)

    def test_customers_returns_customer_instance(self, ibc_client):
        """Verify customers property returns a Customer instance."""
        assert isinstance(ibc_client.customers, Customer)

    def test_data_services_returns_data_instance(self, ibc_client):
        """Verify data_services property returns a Data instance."""
        assert isinstance(ibc_client.data_services, Data)

    def test_market_data_returns_market_data_instance(self, ibc_client):
        """Verify market_data property returns a MarketData instance."""
        with patch.object(Accounts, "accounts", return_value={}):
            assert isinstance(ibc_client.market_data, MarketData)

    def test_orders_returns_orders_instance(self, ibc_client):
        """Verify orders property returns an Orders instance."""
        assert isinstance(ibc_client.orders, Orders)

    def test_pnl_returns_pnl_instance(self, ibc_client):
        """Verify pnl property returns a PnL instance."""
        assert isinstance(ibc_client.pnl, PnL)

    def test_portfolio_accounts_returns_instance(self, ibc_client):
        """Verify portfolio_accounts property returns a PortfolioAccounts instance."""
        assert isinstance(ibc_client.portfolio_accounts, PortfolioAccounts)

    def test_portfolio_analysis_returns_instance(self, ibc_client):
        """Verify portfolio_analysis property returns a PortfolioAnalysis instance."""
        assert isinstance(ibc_client.portfolio_analysis, PortfolioAnalysis)

    def test_scanners_returns_scanners_instance(self, ibc_client):
        """Verify scanners property returns a Scanners instance."""
        assert isinstance(ibc_client.scanners, Scanners)

    def test_trades_returns_trades_instance(self, ibc_client):
        """Verify trades property returns a Trades instance."""
        assert isinstance(ibc_client.trades, Trades)

    def test_session_returns_session_instance(self, ibc_client):
        """Verify session method returns the InteractiveBrokersSession."""
        assert isinstance(ibc_client.session, InteractiveBrokersSession)

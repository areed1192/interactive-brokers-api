"""Client class for the Interactive Brokers API."""

from __future__ import annotations

import functools

from ibc.rest.accounts import Accounts
from ibc.rest.alert import Alerts
from ibc.rest.contract import Contracts
from ibc.rest.customer import Customer
from ibc.rest.data import Data
from ibc.rest.fyi import FYI
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


class InteractiveBrokersClient:
    """Python client for the Interactive Brokers API."""

    def __init__(
        self,
        account_number: str,
        verify_ssl: bool | str = False,
    ) -> None:
        """Initializes the `InteractiveBrokersClient` object.

        ### Parameters
        ----
        account_number (str):
            The User's account number they wish to use during the
            session. Can be either their paper trading account or
            their regular account.

        verify_ssl : bool | str (optional, Default=False)
            Whether to verify SSL certificates. Pass ``True`` to verify
            using the default CA bundle, or a string path to a custom
            CA certificate file or directory. Defaults to ``False``
            because the IB Client Portal Gateway uses a self-signed
            certificate on localhost.

        ### Usage
        ----
            >>> ibc_client = InteractiveBrokersClient(
                account_number=account_number,
            )
        """

        self._account_number = account_number

        # Initialize the services that need to start up together.
        self._session = InteractiveBrokersSession(ib_client=self, verify_ssl=verify_ssl)
        self._auth_service = InteractiveBrokersAuthentication(ib_client=self, ib_session=self._session)

        # Client portal stuff.
        self._client_portal = ClientPortalGateway()
        self._client_portal.setup()

    def __repr__(self) -> str:
        return f"InteractiveBrokersClient(account_number={self._account_number!r})"

    @property
    def account_number(self) -> str:
        """The User's Interactive Brokers Account Number.

        ### Returns
        ----
        str:
            The account number.

        ### Usage
        ----
            >>> ibc_client = InteractiveBrokersClient(
                account_number=account_number,
            )
            >>> ibc_client.account_number
        """

        return self._account_number

    @property
    def client_portal(self) -> ClientPortalGateway:
        """Initializes the `ClientPortalGateway` object.

        ### Returns
        ----
        `ClientPortalGateway`:
            The Interactive Brokers Client Portal Gateway, which is used
            to download the required files needed to access the API.

        ### Usage
        ----
            >>> ibc_client = InteractiveBrokersClient(
                account_number=account_number,
            )
            >>> ibc_client.authentication.login()
            >>> ibc_client_portal = ibc_client.client_portal
        """

        return self._client_portal

    @property
    def session(self) -> InteractiveBrokersSession:
        """Initializes the `InteractiveBrokersSession` object.

        ### Returns
        ----
        `InteractiveBrokersSession`:
            Handles all the requests made during your session with
            the Interactive Brokers API.

        ### Usage
        ----
            >>> ibc_client = InteractiveBrokersClient(
                account_number=account_number,
            )
            >>> ibc_client.authentication.login()
            >>> ibc_session = ibc_client.session
        """

        return self._session

    @property
    def authentication(self) -> InteractiveBrokersAuthentication:
        """Initializes the `InteractiveBrokersAuthentication` object.

        ### Returns
        ----
        `InteractiveBrokersAuthentication`:
            Handles authenticating the User so that they can make
            requests to the Interactive Brokers API.

        ### Usage
        ----
            >>> ibc_client = InteractiveBrokersClient(
                account_number=account_number,
            )
            >>> ibc_client.authentication.login()
            >>> authentication_service = ibc_client.authentication
        """

        return self._auth_service

    @functools.cached_property
    def customers(self) -> Customer:
        """The :class:`Customer` service for customer information."""

        return Customer(ib_client=self, ib_session=self._session)

    @functools.cached_property
    def portfolio_analysis(self) -> PortfolioAnalysis:
        """The :class:`PortfolioAnalysis` service for portfolio analytics."""

        return PortfolioAnalysis(ib_client=self, ib_session=self._session)

    @functools.cached_property
    def accounts(self) -> Accounts:
        """The :class:`Accounts` service for managing IB accounts."""

        return Accounts(ib_client=self, ib_session=self._session)

    @functools.cached_property
    def market_data(self) -> MarketData:
        """The :class:`MarketData` service for quotes and historical prices."""

        return MarketData(ib_client=self, ib_session=self._session)

    @functools.cached_property
    def pnl(self) -> PnL:
        """The :class:`PnL` service for account PnL information."""

        return PnL(ib_client=self, ib_session=self._session)

    @functools.cached_property
    def alerts(self) -> Alerts:
        """The :class:`Alerts` service for managing alerts."""

        return Alerts(ib_client=self, ib_session=self._session)

    @functools.cached_property
    def contracts(self) -> Contracts:
        """The :class:`Contracts` service for contract information."""

        return Contracts(ib_client=self, ib_session=self._session)

    @functools.cached_property
    def scanners(self) -> Scanners:
        """The :class:`Scanners` service for market scanners."""

        return Scanners(ib_client=self, ib_session=self._session)

    @functools.cached_property
    def trades(self) -> Trades:
        """The :class:`Trades` service for querying active trades."""

        return Trades(ib_client=self, ib_session=self._session)

    @functools.cached_property
    def portfolio_accounts(self) -> PortfolioAccounts:
        """The :class:`PortfolioAccounts` service for portfolio data."""

        return PortfolioAccounts(ib_client=self, ib_session=self._session)

    @functools.cached_property
    def orders(self) -> Orders:
        """The :class:`Orders` service for order management."""

        return Orders(ib_client=self, ib_session=self._session)

    @functools.cached_property
    def data_services(self) -> Data:
        """The :class:`Data` service for instrument data."""

        return Data(ib_client=self, ib_session=self._session)

    @functools.cached_property
    def fyi(self) -> FYI:
        """The :class:`FYI` service for notifications and disclaimers."""

        return FYI(ib_client=self, ib_session=self._session)

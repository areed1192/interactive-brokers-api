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
        password: str,
        verify_ssl: bool | str = False,
    ) -> None:
        """Initializes the `InteractiveBrokersClient` object.

        ### Parameters
        ----
        account_number (str):
            The User's account number they wish to use during the
            session. Can be either their paper trading account or
            their regular account.

        password (str):
            The password associated with the account they've chosen.

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
                password=account_password
            )
        """

        self._account_number = account_number
        self._password = password

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
                password=account_password
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
                password=account_password
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
                password=account_password
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
                password=account_password
            )
            >>> ibc_client.authentication.login()
            >>> authentication_service = ibc_client.authentication
        """

        return self._auth_service

    @functools.cached_property
    def customers(self) -> Customer:
        """Initializes the `Customer` object.

        ### Returns
        ----
        `Customer`:
            Used to grab customer information.

        ### Usage
        ----
            >>> ibc_client = InteractiveBrokersClient(
                account_number=account_number,
                password=account_password
            )
            >>> ibc_client.authentication.login()
            >>> customer_service = ibc_client.customers
        """

        return Customer(ib_client=self, ib_session=self._session)

    @functools.cached_property
    def portfolio_analysis(self) -> PortfolioAnalysis:
        """Initializes the `PortfolioAnalysis` object.

        ### Returns
        ----
        `PortfolioAnalysis`:
            Used to interact with the Portfolio Analysis
            service.

        ### Usage
        ----
            >>> ibc_client = InteractiveBrokersClient(
                account_number=account_number,
                password=account_password
            )
            >>> ibc_client.authentication.login()
            >>> portfolio_analysis_service = ibc_client.portfolio_analysis
        """

        return PortfolioAnalysis(ib_client=self, ib_session=self._session)

    @functools.cached_property
    def accounts(self) -> Accounts:
        """Initializes the `Accounts` object.

        ### Returns
        ----
        `Accounts`:
            Used to interact with the Accounts
            service.

        ### Usage
        ----
            >>> ibc_client = InteractiveBrokersClient(
                account_number=account_number,
                password=account_password
            )
            >>> ibc_client.authentication.login()
            >>> accounts_services = ibc_client.accounts
        """

        return Accounts(ib_client=self, ib_session=self._session)

    @functools.cached_property
    def market_data(self) -> MarketData:
        """Initializes the `MarketData` object.

        ### Returns
        ----
        `MarketData`:
            Used to market quotes and historical prices.

        ### Usage
        ----
            >>> ibc_client = InteractiveBrokersClient(
                account_number=account_number,
                password=account_password
            )
            >>> ibc_client.authentication.login()
            >>> market_data_services = ibc_client.market_data
        """

        return MarketData(ib_client=self, ib_session=self._session)

    @functools.cached_property
    def pnl(self) -> PnL:
        """Initializes the `PnL` object.

        ### Returns
        ----
        `PnL`:
            Used to grab Account PNL information.

        ### Usage
        ----
            >>> ibc_client = InteractiveBrokersClient(
                account_number=account_number,
                password=account_password
            )
            >>> ibc_client.authentication.login()
            >>> pnl_services = ibc_client.pnl
        """

        return PnL(ib_client=self, ib_session=self._session)

    @functools.cached_property
    def alerts(self) -> Alerts:
        """Initializes the `Alerts` object.

        ### Returns
        ----
        `Alerts`:
            Used to grab, update, and delete Alerts
            associated with your account.

        ### Usage
        ----
            >>> ibc_client = InteractiveBrokersClient(
                account_number=account_number,
                password=account_password
            )
            >>> ibc_client.authentication.login()
            >>> alerts_services = ibc_client.alerts
        """

        return Alerts(ib_client=self, ib_session=self._session)

    @functools.cached_property
    def contracts(self) -> Contracts:
        """Initializes the `Contracts` object.

        ### Returns
        ----
        `Contracts`:
            Used to search for contract information.

        ### Usage
        ----
            >>> ibc_client = InteractiveBrokersClient(
                account_number=account_number,
                password=account_password
            )
            >>> ibc_client.authentication.login()
            >>> contracts_services = ibc_client.contracts
        """

        return Contracts(ib_client=self, ib_session=self._session)

    @functools.cached_property
    def scanners(self) -> Scanners:
        """Initializes the `Scanners` object.

        ### Returns
        ----
        `Scanners`:
            Used to create market scanners that can
            be used to filter instruments.

        ### Usage
        ----
            >>> ibc_client = InteractiveBrokersClient(
                account_number=account_number,
                password=account_password
            )
            >>> ibc_client.authentication.login()
            >>> scanners_services = ibc_client.scanners
        """

        return Scanners(ib_client=self, ib_session=self._session)

    @functools.cached_property
    def trades(self) -> Trades:
        """Initializes the `Trades` object.

        ### Returns
        ----
        `Trades`:
            Used to query active trades on your
            account.

        ### Usage
        ----
            >>> ibc_client = InteractiveBrokersClient(
                account_number=account_number,
                password=account_password
            )
            >>> ibc_client.authentication.login()
            >>> trades_services = ibc_client.trades
        """

        return Trades(ib_client=self, ib_session=self._session)

    @functools.cached_property
    def portfolio_accounts(self) -> PortfolioAccounts:
        """Initializes the `PortfolioAccounts` object.

        ### Returns
        ----
        `PortfolioAccounts`:
            Used to query portfolio account information
            including ledger data, allocation, and positions.

        ### Usage
        ----
            >>> ibc_client = InteractiveBrokersClient(
                account_number=account_number,
                password=account_password
            )
            >>> ibc_client.authentication.login()
            >>> portfolio_accounts_service = ibc_client.portfolio_accounts
        """

        return PortfolioAccounts(ib_client=self, ib_session=self._session)

    @functools.cached_property
    def orders(self) -> Orders:
        """Initializes the `Orders` object.

        ### Returns
        ----
        `Orders`:
            Used to query, create, update, and delete
            orders with Interactive Brokers.

        ### Usage
        ----
            >>> ibc_client = InteractiveBrokersClient(
                account_number=account_number,
                password=account_password
            )
            >>> ibc_client.authentication.login()
            >>> orders_service = ibc_client.orders
        """

        return Orders(ib_client=self, ib_session=self._session)

    @functools.cached_property
    def data_services(self) -> Data:
        """Initializes the `Data` object.

        ### Returns
        ----
        `Data`:
            Used to query different kinds of data
            for instruments.

        ### Usage
        ----
            >>> ibc_client = InteractiveBrokersClient(
                account_number=account_number,
                password=account_password
            )
            >>> ibc_client.authentication.login()
            >>> data_service = ibc_client.data_services
        """

        return Data(ib_client=self, ib_session=self._session)

    @functools.cached_property
    def fyi(self) -> FYI:
        """Initializes the `FYI` object.

        ### Returns
        ----
        `FYI`:
            Used to manage FYI notifications, delivery
            options, and disclaimer settings.

        ### Usage
        ----
            >>> ibc_client = InteractiveBrokersClient(
                account_number=account_number,
                password=account_password
            )
            >>> ibc_client.authentication.login()
            >>> fyi_service = ibc_client.fyi
        """

        return FYI(ib_client=self, ib_session=self._session)

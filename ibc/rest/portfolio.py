"""Portfolio and accounts-related end-points for the Interactive Brokers API."""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, Any

from ibc.exceptions import IBCValidationError
from ibc.models import Ledger, Position
from ibc.session import InteractiveBrokersSession

if TYPE_CHECKING:
    from ibc.client import InteractiveBrokersClient


class PortfolioAccounts:
    """Client for managing portfolio and account-related operations via the Interactive Brokers API."""

    def __init__(self, ib_client: InteractiveBrokersClient, ib_session: InteractiveBrokersSession) -> None:
        """Initializes the `PortfolioAccounts` client.

        ### Parameters
        ----
        ib_client : InteractiveBrokersClient
            The `InteractiveBrokersClient` Python Client.

        ib_session : InteractiveBrokersSession
            The IB session handler.
        """

        self.client = ib_client
        self.session = ib_session
        self._has_portfolio_been_called = False
        self._has_sub_portfolio_been_called = False

    def __repr__(self) -> str:
        return "PortfolioAccounts()"

    @staticmethod
    def _validate_id(value: str, name: str) -> None:
        """Validate that an ID parameter is a non-empty string."""
        if not value or not isinstance(value, str) or not value.strip():
            raise IBCValidationError(f"{name} must be a non-empty string, got {value!r}")

    def accounts(self) -> list[dict]:
        """Returns the portfolio accounts

        ### Overview
        ----
        In non-tiered account structures, returns a list of accounts
        for which the user can view position and account information.
        This endpoint must be called prior to calling other /portfolio
        endpoints for those accounts. For querying a list of accounts
        which the user can trade, see /iserver/accounts. For a list
        of subaccounts in tiered account structures (e.g. financial
        advisor or ibroker accounts) see /portfolio/subaccounts.

        ### Returns
        ----
        list[dict]:
            A collection of ``PortfolioAccount`` resources.

        ### Usage
        ----
            >>> portfolio_accounts_service = ibc_client.portfolio_accounts
            >>> portfolio_accounts_services.accounts()
        """

        content = self.session.make_request(method="get", endpoint="/api/portfolio/accounts")

        self._has_portfolio_been_called = True

        return content

    def subaccounts(self) -> list[dict]:
        """Returns the portfolio subaccounts

        ### Overview
        ----
        Used in tiered account structures (such as financial advisor
        and ibroker accounts) to return a list of sub-accounts for
        which the user can view position and account-related information.
        This endpoint must be called prior to calling other /portfolio
        endpoints for those subaccounts. To query a list of accounts
        the user can trade, see /iserver/accounts.

        ### Returns
        ----
        list[dict]:
            A collection of ``PortfolioSubAccount`` resources.

        ### Usage
        ----
            >>> portfolio_accounts_service = ibc_client.portfolio_accounts
            >>> portfolio_accounts_services.subaccounts()
        """

        content = self.session.make_request(method="get", endpoint="/api/portfolio/subaccounts")

        self._has_sub_portfolio_been_called = True

        return content

    def subaccounts2(self, page: int = 0) -> dict[str, Any]:
        """Returns a list of sub-accounts for large account structures.

        ### Overview
        ----
        Used in tiered account structures (such as financial advisor
        and ibroker accounts) with many sub-accounts. Supports pagination.
        Use this endpoint instead of ``/portfolio/subaccounts`` when
        dealing with more than 100 sub-accounts.

        ### Parameters
        ----
        page : int (optional, Default=0)
            The page number (zero-indexed).

        ### Returns
        ----
        dict:
            A paginated collection of ``PortfolioSubAccount`` resources.

        ### Usage
        ----
            >>> portfolio_accounts_service = ibc_client.portfolio_accounts
            >>> portfolio_accounts_service.subaccounts2(page=0)
        """

        params = {"page": str(page)}

        content = self.session.make_request(method="get", endpoint="/api/portfolio/subaccounts2", params=params)

        self._has_sub_portfolio_been_called = True

        return content

    def account_metadata(self, account_id: str) -> dict[str, Any]:
        """Account information related to account Id.

        ### Overview
        ---
        /portfolio/accounts or /portfolio/subaccounts
        must be called prior to this endpoint.

        ### Returns
        ----
        dict:
            A `AccountInfo` resource.

        ### Usage
        ----
            >>> portfolio_accounts_service = ibc_client.portfolio_accounts
            >>> portfolio_accounts_services.account_metadata(
                account_id=ibc_client.account_number
            )
        """

        self._validate_id(account_id, "account_id")

        if not self._has_portfolio_been_called:
            self.accounts()

        if not self._has_sub_portfolio_been_called:
            self.subaccounts()

        content = self.session.make_request(method="get", endpoint=f"/api/portfolio/{account_id}/meta")

        return content

    def account_summary(self, account_id: str) -> dict[str, Any]:
        """Returns information about margin, cash balances
        and other information related to specified account.

        ### Overview
        ----
        `/portfolio/accounts` or `/portfolio/subaccounts`
        must be called prior to this endpoint.

        ### Returns
        ----
        dict:
            A `AccountSummary` resource.

        ### Usage
        ----
            >>> portfolio_accounts_service = ibc_client.portfolio_accounts
            >>> portfolio_accounts_services.account_summary(
                account_id=ibc_client.account_number
            )
        """

        self._validate_id(account_id, "account_id")

        if not self._has_portfolio_been_called:
            self.accounts()

        if not self._has_sub_portfolio_been_called:
            self.subaccounts()

        content = self.session.make_request(method="get", endpoint=f"/api/portfolio/{account_id}/summary")

        return content

    def account_ledger(self, account_id: str) -> dict[str, Ledger]:
        """Information regarding settled cash, cash balances,
        etc. in the account’s base currency and any other cash
        balances hold in other currencies.

        ### Overview
        ---
        `/portfolio/accounts` or `/portfolio/subaccounts`
        must be called prior to this endpoint. The list of
        supported currencies is available at:
        https://www.interactivebrokers.com/en/index.php?f=3185

        ### Returns
        ----
        dict[str, Ledger]:
            A `Ledger` resource keyed by currency.

        ### Usage
        ----
            >>> portfolio_accounts_service = ibc_client.portfolio_accounts
            >>> portfolio_accounts_services.account_ledger(
                account_id=ibc_client.account_number
            )
        """

        self._validate_id(account_id, "account_id")

        if not self._has_portfolio_been_called:
            self.accounts()

        if not self._has_sub_portfolio_been_called:
            self.subaccounts()

        content = self.session.make_request(method="get", endpoint=f"/api/portfolio/{account_id}/ledger")

        return {key: Ledger.from_dict(val) for key, val in content.items()}

    def account_allocation(self, account_id: str) -> dict[str, Any]:
        """Information about the account’s portfolio
        by Asset Class, Industry and Category.

        ### Overview
        ---
        /portfolio/accounts or /portfolio/subaccounts
        must be called prior to this endpoint. The list of
        supported currencies is available at:
        https://www.interactivebrokers.com/en/index.php?f=3185

        ### Returns
        ----
        dict:
            A `AccountAllocation` resource.

        ### Usage
        ----
            >>> portfolio_accounts_service = ibc_client.portfolio_accounts
            >>> portfolio_accounts_services.account_allocation(
                account_id=ibc_client.account_number
            )
        """

        self._validate_id(account_id, "account_id")

        if not self._has_portfolio_been_called:
            self.accounts()

        if not self._has_sub_portfolio_been_called:
            self.subaccounts()

        content = self.session.make_request(method="get", endpoint=f"/api/portfolio/{account_id}/allocation")

        return content

    def portfolio_allocation(self, account_ids: list[str]) -> dict[str, Any]:
        """Similar to /portfolio/{accountId}/allocation but
        returns a consolidated view of of all the accounts
        returned by /portfolio/accounts

        ### Overview
        ---
        /portfolio/accounts or /portfolio/subaccounts
        must be called prior to this endpoint.

        ### Parameters
        ----
        account_ids : List[str]
            A list of accounts that you want to be consolidated
            into the view.

        ### Returns
        ----
        dict:
            A consolidated `AccountAllocation` resource.

        ### Usage
        ----
            >>> portfolio_accounts_service = ibc_client.portfolio_accounts
            >>> portfolio_accounts_services.portfolio_allocation(
                account_ids=[ibc_client.account_number]
            )
        """

        if not self._has_portfolio_been_called:
            self.accounts()

        if not self._has_sub_portfolio_been_called:
            self.subaccounts()

        payload = {"acctIds": account_ids}

        content = self.session.make_request(method="post", endpoint="/api/portfolio/allocation", json_payload=payload)

        return content

    def portfolio_positions(
        self,
        account_id: str,
        page_id: int = 0,
        sort: str | Enum = None,
        direction: str | Enum = None,
        period: str = None,
    ) -> list[Position]:
        """Returns a list of positions for the given account.
        The endpoint supports paging, page’s default size is
        30 positions.

        ### Overview
        ---
        /portfolio/accounts or /portfolio/subaccounts
        must be called prior to this endpoint.

        ### Parameters
        ----
        account_id : str
            The account you want to query for positions.

        page_id : int (optional, Default=0)
            The page you want to query.

        sort : Union[str, Enum] (optional, Default=None)
            The field on which to sort the data on.

        direction : Union[str, Enum] (optional, Default=None)
            The order of the sort, `a` means ascending and
            `d` means descending

        period : str (optional, Default=None)
            The period for pnl column, can be 1D, 7D, 1M...

        ### Returns
        ----
        dict:
            A collection of `PortfolioPosition` resources.

        ### Usage
        ----
            >>> portfolio_accounts_service = ibc_client.portfolio_accounts
            >>> portfolio_accounts_services.portfolio_positions(
                    account_id=ibc_client.account_number,
                    page_id=0,
                    sort=SortFields.BaseUnrealizedPnl,
                    direction=SortDirection.Descending
                )
        """

        self._validate_id(account_id, "account_id")

        if not self._has_portfolio_been_called:
            self.accounts()

        if not self._has_sub_portfolio_been_called:
            self.subaccounts()

        if isinstance(sort, Enum):
            sort = sort.value

        if isinstance(direction, Enum):
            direction = direction.value

        params = {"sort": sort, "direction": direction, "period": period}

        content = self.session.make_request(
            method="get", endpoint=f"/api/portfolio/{account_id}/positions/{page_id}", params=params
        )

        return [Position.from_dict(item) for item in content]

    def position_by_contract_id(self, account_id: str, contract_id: str) -> dict[str, Any]:
        """Returns a list of all positions matching the conid. For portfolio models the
        conid could be in more than one model, returning an array with the name of
        model it belongs to.

        ### Overview
        ---
        /portfolio/accounts or /portfolio/subaccounts
        must be called prior to this endpoint.

        ### Parameters
        ----
        account_id : str
            The account you want to query for positions.

        contract_id : str
            The contract ID you want to query.

        ### Returns
        ----
        dict:
            A collection of `PortfolioPosition` resources.

        ### Usage
        ----
            >>> portfolio_accounts_service = ibc_client.portfolio_accounts
            >>> portfolio_accounts_services.position_by_contract_id(
                account_id=ibc_client.account_number,
                contract_id='251962528'
            )
        """

        self._validate_id(account_id, "account_id")
        self._validate_id(contract_id, "contract_id")

        if not self._has_portfolio_been_called:
            self.accounts()

        if not self._has_sub_portfolio_been_called:
            self.subaccounts()

        content = self.session.make_request(
            method="get", endpoint=f"/api/portfolio/{account_id}/position/{contract_id}"
        )

        return content

    def positions_by_contract_id(self, contract_id: str) -> dict[str, Any]:
        """Returns an object of all positions matching the conid for all
        the selected accounts. For portfolio models the conid could be in
        more than one model, returning an array with the name of the model
        it belongs to.

        ### Overview
        ---
        /portfolio/accounts or /portfolio/subaccounts
        must be called prior to this endpoint.

        ### Parameters
        ----
        contract_id : str
            The contract ID you want to query.

        ### Returns
        ----
        dict:
            A collection of `PortfolioPosition` resources.

        ### Usage
        ----
            >>> portfolio_accounts_service = ibc_client.portfolio_accounts
            >>> portfolio_accounts_services.positions_by_contract_id(
                contract_id='251962528'
            )
        """

        self._validate_id(contract_id, "contract_id")

        if not self._has_portfolio_been_called:
            self.accounts()

        if not self._has_sub_portfolio_been_called:
            self.subaccounts()

        content = self.session.make_request(method="get", endpoint=f"/api/portfolio/positions/{contract_id}")

        return content

    def invalidate_positions_cache(self, account_id: str) -> dict | None:
        """Invalidates the backend cache of the Portfolio.

        ### Parameters
        ----
        account_id : str
            The account you want to query for positions.

        ### Returns
        ----
        Union[dict, None]:
            Nothing is returned if successful.

        ### Usage
        ----
            >>> portfolio_accounts_service = ibc_client.portfolio_accounts
            >>> portfolio_accounts_services.invalidate_positions_cache()
        """

        self._validate_id(account_id, "account_id")

        content = self.session.make_request(method="post", endpoint=f"/api/portfolio/{account_id}/positions/invalidate")

        return content

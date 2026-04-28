"""Module for managing accounts via the Interactive Brokers API."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ibc.models import Account
from ibc.session import InteractiveBrokersSession

if TYPE_CHECKING:
    from ibc.client import InteractiveBrokersClient


class Accounts:
    """Client for managing accounts via the Interactive Brokers API."""

    def __init__(self, ib_client: InteractiveBrokersClient, ib_session: InteractiveBrokersSession) -> None:
        """Initializes the `Accounts` client.

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
        return "Accounts()"

    def accounts(self) -> list[Account]:
        """Returns the Users Accounts.

        ### Overview
        ----
        Returns a list of accounts the user has trading access to,
        their respective aliases and the currently selected account.
        Note this endpoint must be called before modifying an order
        or querying open orders.

        ### Returns
        ----
        list[Account]:
            A list of ``Account`` model instances parsed from the response.

        ### Usage
        ----
            >>> accounts_services = ibc_client.accounts
            >>> accounts_services.accounts()
        """

        content = self.session.make_request(method="get", endpoint="/api/iserver/accounts")

        raw_accounts = content.get("accounts", []) if isinstance(content, dict) else []
        return [Account.from_dict(a) if isinstance(a, dict) else Account(id=str(a)) for a in raw_accounts]

    def pnl_server_account(self) -> dict[str, Any]:
        """Returns an object containing PnL for the selected account
        and its models (if any).

        ### Returns
        ----
        dict:
            An `AccountPnL` resource.

        ### Usage
        ----
            >>> accounts_services = ibc_client.accounts
            >>> accounts_services.pnl_server_account()
        """

        content = self.session.make_request(method="get", endpoint="/api/iserver/account/pnl/partitioned")

        return content

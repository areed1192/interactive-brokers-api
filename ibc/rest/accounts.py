from __future__ import annotations

from typing import TYPE_CHECKING

from ibc.session import InteractiveBrokersSession

if TYPE_CHECKING:
    from ibc.client import InteractiveBrokersClient


class Accounts():

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

    def accounts(self) -> dict:
        """Returns the Users Accounts.

        ### Overview
        ----
        Returns a list of accounts the user has trading access to,
        their respective aliases and the currently selected account.
        Note this endpoint must be called before modifying an order
        or querying open orders.

        ### Returns
        ----
        dict: 
            A collection of `Account` resources.
        
        ### Usage
        ----
            >>> accounts_services = ibc_client.accounts
            >>> accounts_services.accounts()
        """

        content = self.session.make_request(
            method='get',
            endpoint='/api/iserver/accounts'
        )

        return content

    def pnl_server_account(self) -> dict:
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

        content = self.session.make_request(
            method='get',
            endpoint='/api/iserver/account/pnl/partitioned'
        )

        return content

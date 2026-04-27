"""Module for managing PnL via the Interactive Brokers API."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ibc.exceptions import IBCValidationError
from ibc.session import InteractiveBrokersSession

if TYPE_CHECKING:
    from ibc.client import InteractiveBrokersClient


class PnL:
    """Client for managing PnL via the Interactive Brokers API."""

    def __init__(
        self, ib_client: InteractiveBrokersClient, ib_session: InteractiveBrokersSession
    ) -> None:
        """Initializes the `PnL` client.

        ### Parameters
        ----
        ib_client : InteractiveBrokersClient
            The `InteractiveBrokersClient` Python Client.

        ib_session : InteractiveBrokersSession
            The IB session handler.
        """

        self.client = ib_client
        self.session = ib_session

    def __repr__(self) -> str:
        return "PnL()"

    @staticmethod
    def _validate_id(value: str, name: str) -> None:
        """Validate that an ID parameter is a non-empty string."""
        if not value or not isinstance(value, str) or not value.strip():
            raise IBCValidationError(
                f"{name} must be a non-empty string, got {value!r}"
            )

    def pnl_server_account(self) -> dict:
        """Returns an object containing PnL for the selected account
        and its models (if any).

        ### Overview
        ----
        Delegates to `Accounts.pnl_server_account()` for a single
        source of truth.

        ### Returns
        ----
        dict:
            An `AccountPnL` resource.
        """

        return self.client.accounts.pnl_server_account()

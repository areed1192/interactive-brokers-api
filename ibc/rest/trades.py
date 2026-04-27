"""Trades-related end-points for the Interactive Brokers API."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ibc.exceptions import IBCValidationError
from ibc.models import Trade
from ibc.session import InteractiveBrokersSession

if TYPE_CHECKING:
    from ibc.client import InteractiveBrokersClient


class Trades:
    """Client for managing trades via the Interactive Brokers API."""

    def __init__(
        self, ib_client: InteractiveBrokersClient, ib_session: InteractiveBrokersSession
    ) -> None:
        """Initializes the `Trades` client.

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
        return "Trades()"

    @staticmethod
    def _validate_id(value: str, name: str) -> None:
        """Validate that an ID parameter is a non-empty string."""
        if not value or not isinstance(value, str) or not value.strip():
            raise IBCValidationError(
                f"{name} must be a non-empty string, got {value!r}"
            )

    def get_trades(self) -> list[Trade]:
        """Returns a list of trades for the currently selected
        account for current day and six previous days.

        ### Returns
        ----
        list[Trade]:
            A collection of `Trade` resources.

        ### Usage
        ----
            >>> trades_service = ibc_client.trades
            >>> trades_service.get_trades()
        """

        content = self.session.make_request(
            method="get", endpoint="/api/iserver/account/trades"
        )

        return [Trade.from_dict(item) for item in content]

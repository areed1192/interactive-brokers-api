"""Portfolio analysis-related end-points for the Interactive Brokers API."""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, List, Union

from ibc.models import Transactions
from ibc.session import InteractiveBrokersSession

if TYPE_CHECKING:
    from ibc.client import InteractiveBrokersClient


class PortfolioAnalysis:
    """Client for managing portfolio analysis via the Interactive Brokers API."""

    def __init__(
        self, ib_client: InteractiveBrokersClient, ib_session: InteractiveBrokersSession
    ) -> None:
        """Initializes the `PortfolioAnalysis` client.

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
        return "PortfolioAnalysis()"

    def account_performance(
        self, account_ids: List[str], frequency: Union[str, Enum]
    ) -> dict:
        """Returns the performance (MTM) for the given accounts, if more than one account
        is passed, the result is consolidated.

        ### Parameters
        ----
        account_ids : List[str]
            A list of account Numbers.

        frequency : Union[str, Enum]
            Frequency of cumulative performance data
            points: 'D'aily, 'M'onthly,'Q'uarterly. Can
            be one of 3 possible values: "D" "M" "Q".

        ### Returns
        ----
            dict: A performance resource.
        """

        # Grab the Order Status.
        if isinstance(frequency, Enum):
            frequency = frequency.value

        payload = {"acctIds": account_ids, "freq": frequency}

        content = self.session.make_request(
            method="post", endpoint="/api/pa/performance", json_payload=payload
        )

        return content

    def account_summary(self, account_ids: List[str]) -> dict:
        """Returns a summary of all account balances for the given accounts,
        if more than one account is passed, the result is consolidated.

        ### Parameters
        ----
        account_ids : List[str]
            A list of account Numbers.

        ### Returns
        ----
            dict: A performance resource.
        """

        payload = {"acctIds": account_ids}

        content = self.session.make_request(
            method="post", endpoint="/api/pa/summary", json_payload=payload
        )

        return content

    def transactions_history(
        self,
        account_ids: List[str] = None,
        contract_ids: List[str] = None,
        currency: str = "USD",
        days: int = 90,
    ) -> Transactions:
        """Transaction history for a given number of conids and accounts. Types of transactions
        include dividend payments, buy and sell transactions, transfers.

        ### Parameters
        ----
        account_ids : List[str]
            A list of account Numbers.

        contract_ids : List[str]
            A list contract IDs.

        currency : str (optional, Default='USD')
            The currency for which to return values.

        days : int (optional, Default=90)
            The number of days to return.

        ### Returns
        ----
        dict :
            A collection of `Transactions` resource.
        """

        payload = {
            "acctIds": account_ids,
            "conids": contract_ids,
            "currency": currency,
            "days": days,
        }

        content = self.session.make_request(
            method="post", endpoint="/api/pa/transactions", json_payload=payload
        )

        return Transactions.from_dict(content)

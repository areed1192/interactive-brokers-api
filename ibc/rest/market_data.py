"""Market data-related end-points for the Interactive Brokers API."""

from __future__ import annotations

import logging
from enum import Enum
from typing import TYPE_CHECKING

from ibc.exceptions import IBCValidationError
from ibc.models import HistoryData
from ibc.models import MarketData as MarketDataModel
from ibc.session import InteractiveBrokersSession

if TYPE_CHECKING:
    from ibc.client import InteractiveBrokersClient

logger = logging.getLogger(__name__)


class MarketData:
    """Client for interacting with the Market Data endpoints of the Interactive Brokers API."""

    def __init__(
        self, ib_client: InteractiveBrokersClient, ib_session: InteractiveBrokersSession
    ) -> None:
        """Initializes the `MarketData` client.

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
        return "MarketData()"

    def snapshot(
        self,
        contract_ids: list[str],
        since: int = None,
        fields: str | Enum = None,
    ) -> list[MarketDataModel]:
        """Get Market Data for the given conid(s).

        ### Overview
        ----
        The end-point will return by default bid, ask,  last, change, change pct, close,
        listing exchange. The endpoint /iserver/accounts should be called prior to
        /iserver/marketdata/snapshot. To receive all available fields the /snapshot
        endpoint will need to be called several times.

        ### Parameters
        ----
        contract_ids : List[str]
            A list of contract Ids.

        frequency : Union[str, Enum]
            Frequency of cumulative performance data
            points: 'D'aily, 'M'onthly,'Q'uarterly. Can
            be one of 3 possible values: "D" "M" "Q".

        ### Returns
        ----
            list[MarketData]: A collection of `MarketData` resources.

        ### Usage
        ----
            >>> market_data_services = ibc_client.market_data
            >>> market_data_services.snapshot(contract_ids=['265598'])
        """

        new_fields = []

        if fields:
            # Check for Enums.
            for field in fields:

                if isinstance(field, Enum):
                    field = field.value
                new_fields.append(field)

            fields = ",".join(new_fields)
        else:
            fields = None

        # Define the payload.
        params = {"conids": ",".join(contract_ids), "since": since, "fields": fields}

        content = self.session.make_request(
            method="get", endpoint="/api/iserver/marketdata/snapshot", params=params
        )

        return [MarketDataModel.from_dict(item) for item in content]

    def market_history(
        self,
        contract_id: str,
        period: str,
        market_bar: str | Enum = None,
        exchange: str = None,
        outside_regular_trading_hours: bool = True,
    ) -> HistoryData:
        """Get historical market Data for given conid, length of data
        is controlled by 'period' and 'bar'.

        ### Parameters
        ----
        contract_id : str
            A contract Id.

        period : str
            Available time period: {1-30}min, {1-8}h,
            {1-1000}d, {1-792}w, {1-182}m, {1-15}y

        bar : Union[str, Enum] (optional, Default=None):
            The bar type you want the data in.

        exchange : str (optional, Default=None):
            Exchange of the conid.

        outside_regular_trading_hours : bool (optional, Default=True)
            For contracts that support it, will determine if historical
            data includes outside of regular trading hours.

        ### Returns
        ----
            dict: A collection `Bar` resources.

        ### Usage
        ----
            >>> market_data_services = ibc_client.market_data
            >>> market_data_services.snapshot(contract_ids=['265598'])
        """

        if isinstance(market_bar, Enum):
            market_bar = market_bar.value

        payload = {
            "conid": contract_id,
            "period": period,
            "bar": market_bar,
            "exchange": exchange,
            "outsideRth": outside_regular_trading_hours,
        }

        content = self.session.make_request(
            method="get", endpoint="/api/iserver/marketdata/history", params=payload
        )

        return HistoryData.from_dict(content)

    def unsubscribe(self, contract_id: str) -> dict:
        """Cancel market data subscription for the given contract.

        ### Parameters
        ----
        contract_id : str
            The contract ID to unsubscribe from.

        ### Returns
        ----
        dict:
            An unsubscribe confirmation resource.

        ### Usage
        ----
            >>> market_data_services = ibc_client.market_data
            >>> market_data_services.unsubscribe(contract_id='265598')
        """

        if (
            not contract_id
            or not isinstance(contract_id, str)
            or not contract_id.strip()
        ):
            raise IBCValidationError(
                f"contract_id must be a non-empty string, got {contract_id!r}"
            )

        content = self.session.make_request(
            method="get", endpoint=f"/api/iserver/marketdata/{contract_id}/unsubscribe"
        )

        return content

    def unsubscribe_all(self) -> dict:
        """Cancel all market data subscriptions.

        ### Returns
        ----
        dict:
            An unsubscribe confirmation resource.

        ### Usage
        ----
            >>> market_data_services = ibc_client.market_data
            >>> market_data_services.unsubscribe_all()
        """

        content = self.session.make_request(
            method="get", endpoint="/api/iserver/marketdata/unsubscribeall"
        )

        return content

    def market_history_beta(
        self,
        contract_id: str,
        period: str,
        market_bar: str | Enum = None,
        outside_regular_trading_hours: bool = True,
    ) -> HistoryData:
        """Get historical market data using the beta HMDS endpoint.

        ### Parameters
        ----
        contract_id : str
            A contract ID.

        period : str
            Available time period (e.g. ``1d``, ``1w``, ``1m``).

        market_bar : Union[str, Enum] (optional, Default=None)
            The bar size.

        outside_regular_trading_hours : bool (optional, Default=True)
            Whether to include outside regular trading hours data.

        ### Returns
        ----
        dict:
            A collection of ``Bar`` resources.

        ### Usage
        ----
            >>> market_data_services = ibc_client.market_data
            >>> market_data_services.market_history_beta(
                contract_id='265598',
                period='1d',
                bar='1min'
            )
        """

        if isinstance(market_bar, Enum):
            market_bar = market_bar.value

        params = {
            "conid": contract_id,
            "period": period,
            "bar": market_bar,
            "outsideRth": outside_regular_trading_hours,
        }

        content = self.session.make_request(
            method="get", endpoint="/api/hmds/history", params=params
        )

        return HistoryData.from_dict(content)

    def snapshot_beta(
        self, contract_ids: list[str], fields: str | Enum = None
    ) -> list[MarketDataModel]:
        """Get market data snapshot using the beta endpoint.

        ### Parameters
        ----
        contract_ids : List[str]
            A list of contract IDs.

        fields : Union[str, Enum] (optional, Default=None)
            Fields to return.

        ### Returns
        ----
        dict:
            A ``MarketSnapshot`` resource.

        ### Usage
        ----
            >>> market_data_services = ibc_client.market_data
            >>> market_data_services.snapshot_beta(contract_ids=['265598'])
        """

        new_fields = []

        if fields:
            for field in fields:
                if isinstance(field, Enum):
                    field = field.value
                new_fields.append(field)
            fields = ",".join(new_fields)
        else:
            fields = None

        params = {"conids": ",".join(contract_ids), "fields": fields}

        content = self.session.make_request(
            method="get", endpoint="/api/md/snapshot", params=params
        )

        return [MarketDataModel.from_dict(item) for item in content]

    def scanner_beta(self, scanner: dict) -> dict:
        """Run a market scanner using the beta HMDS endpoint.

        ### Parameters
        ----
        scanner : dict
            A scanner definition payload.

        ### Returns
        ----
        dict:
            A collection of contract resources matching the scanner criteria.

        ### Usage
        ----
            >>> market_data_services = ibc_client.market_data
            >>> market_data_services.scanner_beta(
                scanner={
                    "instrument": "STK",
                    "type": "TOP_PERC_GAIN",
                    "location": "STK.US.MAJOR",
                    "size": "25"
                }
            )
        """

        content = self.session.make_request(
            method="post", endpoint="/api/hmds/scanner", json_payload=scanner
        )

        return content

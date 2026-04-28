"""Contracts-related end-points for the Interactive Brokers API."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ibc.models import Contract, SecdefInfo
from ibc.session import InteractiveBrokersSession
from ibc.utils.validation import validate_id

if TYPE_CHECKING:
    from ibc.client import InteractiveBrokersClient


class Contracts:
    """Client for managing contract-related operations via the Interactive Brokers API."""

    def __init__(self, ib_client: InteractiveBrokersClient, ib_session: InteractiveBrokersSession) -> None:
        """Initializes the `Contracts` client.

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
        return "Contracts()"

    def contract_info(self, contract_id: str) -> Contract:
        """Get contract details, you can use this to prefill your
        order before you submit an order.

        ### Parameters
        ----
        contract_id : str
            The contract ID you want details for.

        ### Returns
        ----
        Contract:
            A `Contract` resource.

        ### Usage
        ----
            >>> contracts_service = ibc_client.contracts
            >>> contracts_service.contract_info(
                contract_id='265598'
            )
        """

        validate_id(contract_id, "contract_id")

        content = self.session.make_request(method="get", endpoint=f"/api/iserver/contract/{contract_id}/info")

        return Contract.from_dict(content)

    def search_futures(self, symbols: list[str]) -> dict:
        """Returns a list of non-expired future contracts
        for given symbol(s).

        ### Parameters
        ----
        symbols : str
            List of case-sensitive symbols separated by comma

        ### Returns
        ----
        list:
            A collection of `Futures` resource.

        ### Usage
        ----
            >>> contracts_service = ibc_client.contracts
            >>> contracts_service.search_futures(
                symbols=['CL', 'ES']
            )
        """

        content = self.session.make_request(
            method="get",
            endpoint="/api/trsrv/futures",
            params={"symbols": ",".join(symbols)},
        )

        return content

    def search_symbol(self, symbol: str, name: bool = False, security_type: str = None) -> list:
        """Search by symbol or name.

        ### Parameters
        ----
        symbol : str
            The symbol to be searched.

        name : bool (optional, Default=False)
            Set to `True` if searching by name, `False` if searching
            by symbol.

        security_type : str (optional, default=True)
            The security type of the symbol.

        ### Returns
        ----
        list:
            A collection of `Contract` resources.

        ### Usage
        ----
            >>> contracts_service = ibc_client.contracts
            >>> contracts_service.search_symbol(
                symbol='AAPL',
                name='Apple'
            )
        """

        payload = {"symbol": symbol, "name": name, "secType": security_type}

        content = self.session.make_request(method="post", endpoint="/api/iserver/secdef/search", json_payload=payload)

        return content

    def search_multiple_contracts(self, contract_ids: list[int]) -> list:
        """Returns a list of security definitions for the given conids.

        ### Parameters
        ----
        contract_ids : List[str]
            A list of Contract IDs.

        ### Returns
        ----
        list:
            A collection of `Contract` resources.

        ### Usage
        ----
            >>> contracts_service = ibc_client.contracts
            >>> contracts_service.search_multiple_contracts(
                contract_ids=['265598']
            )
        """

        payload = {"conids": contract_ids}

        content = self.session.make_request(method="post", endpoint="/api/trsrv/secdef", json_payload=payload)

        return content

    def search_stocks(self, symbols: list[str]) -> dict:
        """Returns a list of stock contracts for the given symbol(s).

        ### Parameters
        ----
        symbols : List[str]
            List of case-sensitive symbols separated by comma.

        ### Returns
        ----
        dict:
            A collection of stock contract resources.

        ### Usage
        ----
            >>> contracts_service = ibc_client.contracts
            >>> contracts_service.search_stocks(
                symbols=['AAPL', 'MSFT']
            )
        """

        content = self.session.make_request(
            method="get",
            endpoint="/api/trsrv/stocks",
            params={"symbols": ",".join(symbols)},
        )

        return content

    def trading_schedule(self, asset_class: str, symbol: str, exchange: str = None) -> dict:
        """Returns the trading schedule for the given symbol.

        ### Parameters
        ----
        asset_class : str
            The asset class of the instrument (e.g. ``STK``, ``OPT``, ``FUT``).

        symbol : str
            The symbol to query.

        exchange : str (optional, Default=None)
            The exchange to query. If not provided, returns all exchanges.

        ### Returns
        ----
        dict:
            A trading schedule resource.

        ### Usage
        ----
            >>> contracts_service = ibc_client.contracts
            >>> contracts_service.trading_schedule(
                asset_class='STK',
                symbol='AAPL'
            )
        """

        params = {"assetClass": asset_class, "symbol": symbol, "exchange": exchange}

        content = self.session.make_request(method="get", endpoint="/api/trsrv/secdef/schedule", params=params)

        return content

    def secdef_strikes(self, contract_id: str, sectype: str, month: str, exchange: str = None) -> dict:
        """Returns available strikes for an option or warrant contract.

        ### Parameters
        ----
        contract_id : str
            The underlying contract ID.

        sectype : str
            The security type (e.g. ``OPT``, ``WAR``).

        month : str
            The expiry month in ``YYYYMM`` format.

        exchange : str (optional, Default=None)
            The exchange to filter by.

        ### Returns
        ----
        dict:
            A collection of available strikes.

        ### Usage
        ----
            >>> contracts_service = ibc_client.contracts
            >>> contracts_service.secdef_strikes(
                contract_id='265598',
                sectype='OPT',
                month='202501'
            )
        """

        validate_id(contract_id, "contract_id")

        params = {
            "conid": contract_id,
            "sectype": sectype,
            "month": month,
            "exchange": exchange,
        }

        content = self.session.make_request(method="get", endpoint="/api/iserver/secdef/strikes", params=params)

        return content

    def secdef_info(
        self,
        contract_id: str,
        sectype: str,
        month: str = None,
        exchange: str = None,
        strike: str = None,
        right: str = None,
    ) -> list[SecdefInfo]:
        """Returns detailed security definition information.

        ### Parameters
        ----
        contract_id : str
            The underlying contract ID.

        sectype : str
            The security type (e.g. ``OPT``, ``FUT``, ``WAR``).

        month : str (optional, Default=None)
            The expiry month in ``YYYYMM`` format.

        exchange : str (optional, Default=None)
            The exchange to filter by.

        strike : str (optional, Default=None)
            The strike price.

        right : str (optional, Default=None)
            The right side (``C`` for call, ``P`` for put).

        ### Returns
        ----
        list[SecdefInfo]:
            A collection of security definition resources.

        ### Usage
        ----
            >>> contracts_service = ibc_client.contracts
            >>> contracts_service.secdef_info(
                contract_id='265598',
                sectype='OPT',
                month='202501',
                strike='150',
                right='C'
            )
        """

        validate_id(contract_id, "contract_id")

        params = {
            "conid": contract_id,
            "sectype": sectype,
            "month": month,
            "exchange": exchange,
            "strike": strike,
            "right": right,
        }

        content = self.session.make_request(method="get", endpoint="/api/iserver/secdef/info", params=params)

        return [SecdefInfo.from_dict(item) for item in content]

    def contract_algos(
        self,
        contract_id: str,
        algos: str = None,
        add_description: str = None,
        add_params: str = None,
    ) -> list:
        """Returns the IB algorithm parameters for a given contract.

        ### Parameters
        ----
        contract_id : str
            The contract ID.

        algos : str (optional, Default=None)
            List of algo ids delimited by semicolon to filter.

        add_description : str (optional, Default=None)
            Whether to add algo description (``1`` for yes).

        add_params : str (optional, Default=None)
            Whether to add algo parameters (``1`` for yes).

        ### Returns
        ----
        list:
            A collection of algorithm parameter resources.

        ### Usage
        ----
            >>> contracts_service = ibc_client.contracts
            >>> contracts_service.contract_algos(
                contract_id='265598'
            )
        """

        validate_id(contract_id, "contract_id")

        params = {
            "algos": algos,
            "addDescription": add_description,
            "addParams": add_params,
        }

        content = self.session.make_request(
            method="get",
            endpoint=f"/api/iserver/contract/{contract_id}/algos",
            params=params,
        )

        return content

    def contract_rules(self, contract_id: str, is_buy: bool = True) -> dict:
        """Returns trading rules for a specific contract.

        ### Parameters
        ----
        contract_id : str
            The contract ID.

        is_buy : bool (optional, Default=True)
            Whether the rules are for a buy (``True``) or sell (``False``).

        ### Returns
        ----
        dict:
            A contract rules resource with order types, TIF types, etc.

        ### Usage
        ----
            >>> contracts_service = ibc_client.contracts
            >>> contracts_service.contract_rules(
                contract_id='265598',
                is_buy=True
            )
        """

        validate_id(contract_id, "contract_id")

        payload = {"conid": int(contract_id), "isBuy": is_buy}

        content = self.session.make_request(method="post", endpoint="/api/iserver/contract/rules", json_payload=payload)

        return content

    def contract_info_and_rules(self, contract_id: str, is_buy: bool = True) -> dict:
        """Returns both contract info and trading rules in a single call.

        ### Parameters
        ----
        contract_id : str
            The contract ID.

        is_buy : bool (optional, Default=True)
            Whether the rules are for a buy (``True``) or sell (``False``).

        ### Returns
        ----
        dict:
            A combined contract info and rules resource.

        ### Usage
        ----
            >>> contracts_service = ibc_client.contracts
            >>> contracts_service.contract_info_and_rules(
                contract_id='265598',
                is_buy=True
            )
        """

        validate_id(contract_id, "contract_id")

        params = {"isBuy": is_buy}

        content = self.session.make_request(
            method="get",
            endpoint=f"/api/iserver/contract/{contract_id}/info-and-rules",
            params=params,
        )

        return content

    def currency_pairs(self, currency: str) -> dict:
        """Returns available currency pairs for trading.

        ### Parameters
        ----
        currency : str
            The base currency (e.g. ``USD``).

        ### Returns
        ----
        dict:
            A collection of available currency pairs.

        ### Usage
        ----
            >>> contracts_service = ibc_client.contracts
            >>> contracts_service.currency_pairs(currency='USD')
        """

        params = {"currency": currency}

        content = self.session.make_request(method="get", endpoint="/api/iserver/currency/pairs", params=params)

        return content

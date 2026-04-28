"""Scanners-related end-points for the Interactive Brokers API."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ibc.exceptions import IBCValidationError
from ibc.models import ScannerResult
from ibc.session import InteractiveBrokersSession

if TYPE_CHECKING:
    from ibc.client import InteractiveBrokersClient


class Scanners:
    """Client for managing scanners via the Interactive Brokers API."""

    def __init__(self, ib_client: InteractiveBrokersClient, ib_session: InteractiveBrokersSession) -> None:
        """Initializes the `Scanners` client.

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
        return "Scanners()"

    def scanners(self) -> dict:
        """Returns an object contains four lists contain all parameters
        for scanners.

        ### Returns
        ----
        dict:
            A collection of `Scanner` resources.

        ### Usage
        ----
            >>> scanners_service = ibc_client.scanners
            >>> scanners_service.scanners()
        """

        content = self.session.make_request(method="get", endpoint="/api/iserver/scanner/params")

        return content

    def run_scanner(self, scanner: dict) -> ScannerResult:
        """Runs scanner to get a list of contracts.

        ### Parameters
        ----
        scanner : dict
            A scanner definition that you want to run.

        ### Returns
        ----
        dict:
            A collection of `contract` resources.

        ### Usage
        ----
            >>> scanners_service = ibc_client.scanners
            >>> scanners_service.run_scanner(
                scanner={
                    "instrument": "STK",
                    "type": "NOT_YET_TRADED_TODAY",
                    "filter": [
                        {
                            "code": "priceAbove",
                            "value": 50
                        },
                        {
                            "code": "priceBelow",
                            "value": 70
                        },
                        {
                            "code": "volumeAbove",
                            "value": None
                        },
                        {
                            "code": "volumeBelow",
                            "value": None
                        }
                    ],
                    "location": "STK.US.MAJOR",
                    "size": "25"
                }
            )
        """

        if not scanner or not isinstance(scanner, dict):
            raise IBCValidationError(f"scanner must be a non-empty dict, got {type(scanner).__name__}")

        content = self.session.make_request(method="post", endpoint="/api/iserver/scanner/run", json_payload=scanner)

        return ScannerResult.from_dict(content)

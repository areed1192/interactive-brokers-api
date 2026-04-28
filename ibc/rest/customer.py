"""Customer-related end-points for the Interactive Brokers API."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ibc.session import InteractiveBrokersSession

if TYPE_CHECKING:
    from ibc.client import InteractiveBrokersClient


class Customer:
    """Client for managing customer-related operations via the Interactive Brokers API."""

    def __init__(self, ib_client: InteractiveBrokersClient, ib_session: InteractiveBrokersSession) -> None:
        """Initializes the `InteractiveBrokersCustomer` client.

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
        return "Customer()"

    def customer_info(self) -> dict[str, Any]:
        """Returns Applicant Id with all owner related entities.

        ### Returns
        ----
        dict:
            A customer resource object.

        ### Usage
        ----
            >>> customers_service = ibc_client.customers
            >>> customers_service.customer_info()
        """

        content = self.session.make_request(method="get", endpoint="/api/ibcust/entity/info")

        return content

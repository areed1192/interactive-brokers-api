"""Customer-related end-points for the Interactive Brokers API."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ibc.exceptions import IBCValidationError
from ibc.session import InteractiveBrokersSession

if TYPE_CHECKING:
    from ibc.client import InteractiveBrokersClient


class Customer:
    """Client for managing customer-related operations via the Interactive Brokers API."""

    def __init__(
        self, ib_client: InteractiveBrokersClient, ib_session: InteractiveBrokersSession
    ) -> None:
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

    @staticmethod
    def _validate_id(value: str, name: str) -> None:
        """Validate that an ID parameter is a non-empty string."""
        if not value or not isinstance(value, str) or not value.strip():
            raise IBCValidationError(
                f"{name} must be a non-empty string, got {value!r}"
            )

    def customer_info(self) -> dict:
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

        content = self.session.make_request(
            method="get", endpoint="/api/ibcust/entity/info"
        )

        return content

"""Tests for the Customer service."""


from unittest.mock import MagicMock

import pytest

from ibc.rest.customer import Customer

# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------

SAMPLE_CUSTOMER_INFO = {
    "applicantId": 12345,
    "entities": [
        {
            "entityId": 1,
            "entityType": "Individual",
            "name": "John Doe",
        }
    ],
}


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def customer_service(mock_session, mock_client):
    """Create a Customer service with mocked session."""
    return Customer(ib_client=mock_client, ib_session=mock_session)


# ---------------------------------------------------------------------------
# Customer.customer_info tests
# ---------------------------------------------------------------------------


class TestCustomerInfo:
    """Tests for the Customer.customer_info method."""

    def test_returns_customer_info(self, customer_service, mock_session):
        """Verify customer_info() returns the response."""
        mock_session.make_request = MagicMock(return_value=SAMPLE_CUSTOMER_INFO)

        result = customer_service.customer_info()

        assert result == SAMPLE_CUSTOMER_INFO
        assert result["applicantId"] == 12345

    def test_calls_correct_endpoint(self, customer_service, mock_session):
        """Verify customer_info() calls the correct API endpoint."""
        mock_session.make_request = MagicMock(return_value={})

        customer_service.customer_info()

        mock_session.make_request.assert_called_once_with(
            method="get",
            endpoint="/api/ibcust/entity/info",
        )

    def test_repr(self, customer_service):
        """Verify the service repr."""
        assert repr(customer_service) == "Customer()"

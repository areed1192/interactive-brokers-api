"""Shared fixtures for Interactive Brokers API tests."""

# pylint: disable=redefined-outer-name

from unittest.mock import patch, MagicMock

import pytest

from ibc.session import InteractiveBrokersSession


# ---------------------------------------------------------------------------
# Mock client fixture
# ---------------------------------------------------------------------------

@pytest.fixture
def mock_client():
    """Create a mock InteractiveBrokersClient without triggering gateway download."""
    client = MagicMock()
    client.account_number = "U1234567"
    client._account_number = "U1234567" #pylint: disable=protected-access
    client._password = "test_password" #pylint: disable=protected-access
    return client


# ---------------------------------------------------------------------------
# Mock session fixture
# ---------------------------------------------------------------------------

@pytest.fixture
def mock_session(mock_client):
    """Create an InteractiveBrokersSession with mocked dependencies."""
    with patch("ibc.session.UserAgent") as mock_ua:
        mock_ua.return_value.edge = "MockUserAgent/1.0"
        session = InteractiveBrokersSession(ib_client=mock_client)
    return session

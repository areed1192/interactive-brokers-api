"""Tests for the InteractiveBrokersAuthentication service."""

# pylint: disable=redefined-outer-name
# pylint: disable=protected-access

from unittest.mock import MagicMock

import pytest

from ibc.utils.auth import InteractiveBrokersAuthentication


# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------

SAMPLE_TICKLE_RESPONSE = {
    "session": "abc123",
    "ssoExpires": 86400,
    "collission": False,
    "iserver": {"authStatus": {"authenticated": True, "competing": False}},
}

SAMPLE_LOGOUT_RESPONSE = {"confirmed": True}

SAMPLE_AUTH_STATUS = {"authenticated": True, "competing": False, "connected": True}

SAMPLE_SSO_VALIDATE = {
    "LOGIN_TYPE": 2,
    "USER_NAME": "testuser",
    "RESULT": True,
}

SAMPLE_REAUTH_RESPONSE = {"message": "triggered"}


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def auth_service(mock_session, mock_client):
    """Create an InteractiveBrokersAuthentication service with mocked session."""
    mock_client.client_portal = MagicMock()
    mock_client.client_portal._gateway_folder = "/tmp/gateway"
    mock_client.client_portal._is_gateway_installed.return_value = True
    service = InteractiveBrokersAuthentication(ib_client=mock_client, ib_session=mock_session)
    return service


# ---------------------------------------------------------------------------
# InteractiveBrokersAuthentication.tickle tests
# ---------------------------------------------------------------------------


class TestTickle:
    """Tests for the InteractiveBrokersAuthentication.tickle method."""

    def test_returns_tickle_response(self, auth_service, mock_session):
        """Verify tickle() returns the parsed JSON response."""
        mock_session.make_request = MagicMock(return_value=SAMPLE_TICKLE_RESPONSE)

        result = auth_service.tickle()

        assert result == SAMPLE_TICKLE_RESPONSE

    def test_calls_correct_endpoint(self, auth_service, mock_session):
        """Verify tickle() POSTs to the /tickle endpoint."""
        mock_session.make_request = MagicMock(return_value={})

        auth_service.tickle()

        mock_session.make_request.assert_called_once_with(
            method="post", endpoint="/api/tickle"
        )


# ---------------------------------------------------------------------------
# InteractiveBrokersAuthentication.logout tests
# ---------------------------------------------------------------------------


class TestLogout:
    """Tests for the InteractiveBrokersAuthentication.logout method."""

    def test_returns_logout_response(self, auth_service, mock_session):
        """Verify logout() returns the parsed JSON response."""
        mock_session.make_request = MagicMock(return_value=SAMPLE_LOGOUT_RESPONSE)

        result = auth_service.logout()

        assert result == SAMPLE_LOGOUT_RESPONSE

    def test_calls_correct_endpoint(self, auth_service, mock_session):
        """Verify logout() POSTs to the /logout endpoint."""
        mock_session.make_request = MagicMock(return_value={})

        auth_service.logout()

        mock_session.make_request.assert_called_once_with(
            method="post", endpoint="/api/logout"
        )

    def test_sets_authenticated_to_false(self, auth_service, mock_session):
        """Verify logout() sets authenticated flag to False."""
        auth_service.authenticated = True
        mock_session.make_request = MagicMock(return_value={})

        auth_service.logout()

        assert auth_service.authenticated is False


# ---------------------------------------------------------------------------
# InteractiveBrokersAuthentication.is_authenticated tests
# ---------------------------------------------------------------------------


class TestIsAuthenticated:
    """Tests for the InteractiveBrokersAuthentication.is_authenticated method."""

    def test_returns_auth_status(self, auth_service, mock_session):
        """Verify is_authenticated() returns the parsed JSON response."""
        mock_session.make_request = MagicMock(return_value=SAMPLE_AUTH_STATUS)

        result = auth_service.is_authenticated()

        assert result == SAMPLE_AUTH_STATUS

    def test_calls_correct_endpoint(self, auth_service, mock_session):
        """Verify is_authenticated() POSTs to the correct endpoint."""
        mock_session.make_request = MagicMock(return_value={})

        auth_service.is_authenticated()

        mock_session.make_request.assert_called_once_with(
            method="post", endpoint="/api/iserver/auth/status"
        )


# ---------------------------------------------------------------------------
# InteractiveBrokersAuthentication.sso_validate tests
# ---------------------------------------------------------------------------


class TestSsoValidate:
    """Tests for the InteractiveBrokersAuthentication.sso_validate method."""

    def test_returns_validate_response(self, auth_service, mock_session):
        """Verify sso_validate() returns the parsed JSON response."""
        mock_session.make_request = MagicMock(return_value=SAMPLE_SSO_VALIDATE)

        result = auth_service.sso_validate()

        assert result == SAMPLE_SSO_VALIDATE

    def test_calls_correct_endpoint(self, auth_service, mock_session):
        """Verify sso_validate() POSTs to the correct endpoint."""
        mock_session.make_request = MagicMock(return_value={})

        auth_service.sso_validate()

        mock_session.make_request.assert_called_once_with(
            method="post", endpoint="/api/sso/validate"
        )


# ---------------------------------------------------------------------------
# InteractiveBrokersAuthentication.reauthenticate tests
# ---------------------------------------------------------------------------


class TestReauthenticate:
    """Tests for the InteractiveBrokersAuthentication.reauthenticate method."""

    def test_returns_reauth_response(self, auth_service, mock_session):
        """Verify reauthenticate() returns the parsed JSON response."""
        mock_session.make_request = MagicMock(return_value=SAMPLE_REAUTH_RESPONSE)

        result = auth_service.reauthenticate()

        assert result == SAMPLE_REAUTH_RESPONSE

    def test_calls_correct_endpoint(self, auth_service, mock_session):
        """Verify reauthenticate() POSTs to the correct endpoint."""
        mock_session.make_request = MagicMock(return_value={})

        auth_service.reauthenticate()

        mock_session.make_request.assert_called_once_with(
            method="post", endpoint="/api/iserver/reauthenticate"
        )

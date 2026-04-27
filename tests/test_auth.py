"""Tests for the InteractiveBrokersAuthentication service."""

# pylint: disable=redefined-outer-name
# pylint: disable=protected-access

from unittest.mock import MagicMock, patch

import pytest

from ibc.exceptions import IBCAuthenticationError, IBCRequestError, IBCValidationError
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

SAMPLE_AUTH_STATUS_NOT_AUTHENTICATED = {"authenticated": False, "competing": False, "connected": False}

SAMPLE_SERVER_ACCOUNT = {"set": True, "acctId": "U1234567"}


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


# ---------------------------------------------------------------------------
# InteractiveBrokersAuthentication.update_server_account tests
# ---------------------------------------------------------------------------


class TestUpdateServerAccount:
    """Tests for the InteractiveBrokersAuthentication.update_server_account method."""

    def test_returns_response(self, auth_service, mock_session):
        """Verify update_server_account() returns the server account response."""
        mock_session.make_request = MagicMock(return_value=SAMPLE_SERVER_ACCOUNT)

        result = auth_service.update_server_account(account_id="U1234567")

        assert result == SAMPLE_SERVER_ACCOUNT

    def test_calls_correct_endpoint(self, auth_service, mock_session):
        """Verify update_server_account() POSTs to the correct endpoint."""
        mock_session.make_request = MagicMock(return_value={})

        auth_service.update_server_account(account_id="U1234567")

        mock_session.make_request.assert_called_once_with(
            method="post",
            endpoint="/api/iserver/account",
            json_payload={"acctId": "U1234567"},
        )

    def test_validates_empty_account_id(self, auth_service):
        """Verify update_server_account() raises IBCValidationError for empty ID."""
        with pytest.raises(IBCValidationError):
            auth_service.update_server_account(account_id="")

    def test_validates_none_account_id(self, auth_service):
        """Verify update_server_account() raises IBCValidationError for None."""
        with pytest.raises(IBCValidationError):
            auth_service.update_server_account(account_id=None)

    def test_validates_whitespace_account_id(self, auth_service):
        """Verify update_server_account() raises IBCValidationError for whitespace."""
        with pytest.raises(IBCValidationError):
            auth_service.update_server_account(account_id="   ")


# ---------------------------------------------------------------------------
# InteractiveBrokersAuthentication.check_auth tests
# ---------------------------------------------------------------------------


class TestCheckAuth:
    """Tests for the InteractiveBrokersAuthentication.check_auth method."""

    def test_sets_authenticated_true(self, auth_service, mock_session):
        """Verify check_auth() sets authenticated flag when session is valid."""
        mock_session.make_request = MagicMock(return_value=SAMPLE_AUTH_STATUS)

        auth_service.check_auth()

        assert auth_service.authenticated is True

    def test_does_not_set_when_not_authenticated(self, auth_service, mock_session):
        """Verify check_auth() does not set flag when session is not authenticated."""
        mock_session.make_request = MagicMock(
            return_value=SAMPLE_AUTH_STATUS_NOT_AUTHENTICATED
        )
        auth_service.authenticated = False

        auth_service.check_auth()

        assert auth_service.authenticated is False

    def test_silently_returns_on_request_error(self, auth_service, mock_session):
        """Verify check_auth() silently returns on IBCRequestError."""
        mock_session.make_request = MagicMock(side_effect=IBCRequestError("fail"))
        auth_service.authenticated = False

        auth_service.check_auth()

        assert auth_service.authenticated is False


# ---------------------------------------------------------------------------
# InteractiveBrokersAuthentication.login tests
# ---------------------------------------------------------------------------


class TestLogin:
    """Tests for the InteractiveBrokersAuthentication.login method."""

    @patch("ibc.utils.auth.webbrowser.open")
    def test_login_already_authenticated(self, mock_wb, auth_service, mock_session):
        """Verify login() returns immediately if already authenticated."""
        auth_service._is_already_running = MagicMock(
            return_value={"is_running": True, "data": []}
        )
        mock_session.make_request = MagicMock(return_value=SAMPLE_AUTH_STATUS)

        result = auth_service.login()

        assert result["authenticated"] is True
        assert auth_service.authenticated is True
        mock_wb.assert_not_called()

    @patch("ibc.utils.auth.webbrowser.open")
    def test_login_reauthenticates(self, mock_wb, auth_service, mock_session):
        """Verify login() attempts reauthentication when gateway running but not authed."""
        auth_service._is_already_running = MagicMock(
            return_value={"is_running": True, "data": []}
        )
        mock_session.make_request = MagicMock(
            side_effect=[
                SAMPLE_AUTH_STATUS_NOT_AUTHENTICATED,
                SAMPLE_REAUTH_RESPONSE,
                SAMPLE_AUTH_STATUS,
            ]
        )

        result = auth_service.login()

        assert result["authenticated"] is True
        assert auth_service.authenticated is True

    @patch("ibc.utils.auth.webbrowser.open")
    def test_login_opens_browser_on_reauth_failure(self, mock_wb, auth_service, mock_session):
        """Verify login() opens browser when reauthentication fails."""
        auth_service._is_already_running = MagicMock(
            return_value={"is_running": True, "data": []}
        )
        mock_session.make_request = MagicMock(
            side_effect=[
                SAMPLE_AUTH_STATUS_NOT_AUTHENTICATED,
                SAMPLE_REAUTH_RESPONSE,
                SAMPLE_AUTH_STATUS_NOT_AUTHENTICATED,
            ]
        )

        auth_service.login()

        mock_wb.assert_called_once()

    @patch("ibc.utils.auth.webbrowser.open")
    @patch("ibc.utils.auth.subprocess.Popen")
    def test_login_starts_gateway_when_not_running(self, mock_popen, mock_wb, auth_service):
        """Verify login() starts the gateway when it's not running."""
        auth_service._is_already_running = MagicMock(
            return_value={"is_running": False, "data": []}
        )
        mock_popen.return_value.pid = 12345

        result = auth_service.login()

        assert result == {"authenticated": False}
        mock_wb.assert_called_once()


# ---------------------------------------------------------------------------
# InteractiveBrokersAuthentication.wait_for_login tests
# ---------------------------------------------------------------------------


class TestWaitForLogin:
    """Tests for the InteractiveBrokersAuthentication.wait_for_login method."""

    def test_returns_true_when_already_authenticated(self, auth_service, mock_session):
        """Verify wait_for_login() returns True immediately if already authed."""
        auth_service._is_already_running = MagicMock(
            return_value={"is_running": True, "data": []}
        )
        mock_session.make_request = MagicMock(return_value=SAMPLE_AUTH_STATUS)

        result = auth_service.wait_for_login(timeout=5)

        assert result is True

    @patch("ibc.utils.auth.time.sleep")
    @patch("ibc.utils.auth.time.monotonic")
    def test_raises_on_timeout(self, mock_monotonic, mock_sleep, auth_service, mock_session):
        """Verify wait_for_login() raises IBCAuthenticationError on timeout."""
        auth_service._is_already_running = MagicMock(
            return_value={"is_running": True, "data": []}
        )
        mock_session.make_request = MagicMock(
            return_value=SAMPLE_AUTH_STATUS_NOT_AUTHENTICATED
        )
        # Simulate time passing beyond the deadline
        mock_monotonic.side_effect = [0, 0, 10, 20]

        with pytest.raises(IBCAuthenticationError, match="timed out"):
            auth_service.wait_for_login(timeout=5, poll_interval=1)


# ---------------------------------------------------------------------------
# InteractiveBrokersAuthentication._is_already_running tests
# ---------------------------------------------------------------------------


class TestIsAlreadyRunning:
    """Tests for the _is_already_running methods."""

    @patch("ibc.utils.auth.sys.platform", "win32")
    @patch("ibc.utils.auth.subprocess.run")
    def test_windows_not_running(self, mock_run, auth_service):
        """Verify _is_already_running returns False when no gateway on Windows."""
        mock_run.return_value.stdout = b"INFO: No tasks are running"

        result = auth_service._is_already_running()

        assert result["is_running"] is False

    @patch("ibc.utils.auth.sys.platform", "win32")
    @patch("ibc.utils.auth.subprocess.run")
    def test_windows_running(self, mock_run, auth_service):
        """Verify _is_already_running returns True when gateway is on Windows."""
        csv_output = (
            '"Image Name","PID","Session Name","Session#","Mem Usage"\r\n'
            '"cmd.exe","12345","Console","1","5,000 K"\r\n'
        )
        mock_run.return_value.stdout = csv_output.encode()

        result = auth_service._is_already_running()

        assert result["is_running"] is True
        assert auth_service.server_process_id == "12345"

    @patch("ibc.utils.auth.sys.platform", "linux")
    @patch("ibc.utils.auth.subprocess.run")
    def test_unix_not_running(self, mock_run, auth_service):
        """Verify _is_already_running returns False on Unix when no gateway."""
        mock_run.return_value.stdout = b""

        result = auth_service._is_already_running()

        assert result["is_running"] is False

    @patch("ibc.utils.auth.sys.platform", "linux")
    @patch("ibc.utils.auth.subprocess.run")
    def test_unix_running(self, mock_run, auth_service):
        """Verify _is_already_running returns True on Unix when gateway running."""
        mock_run.return_value.stdout = b"12345\n"

        result = auth_service._is_already_running()

        assert result["is_running"] is True
        assert auth_service.server_process_id == "12345"

    @patch("ibc.utils.auth.sys.platform", "win32")
    @patch("ibc.utils.auth.subprocess.run")
    def test_windows_timeout_returns_not_running(self, mock_run, auth_service):
        """Verify _is_already_running handles subprocess timeout gracefully."""
        import subprocess
        mock_run.side_effect = subprocess.TimeoutExpired(cmd="tasklist", timeout=10)

        result = auth_service._is_already_running()

        assert result["is_running"] is False


# ---------------------------------------------------------------------------
# InteractiveBrokersAuthentication.close_gateway tests
# ---------------------------------------------------------------------------


class TestCloseGateway:
    """Tests for the InteractiveBrokersAuthentication.close_gateway method."""

    @patch("ibc.utils.auth.subprocess.run")
    def test_close_with_explicit_pid(self, mock_run, auth_service):
        """Verify close_gateway() terminates with explicit PID."""
        mock_run.return_value.stdout = b"SUCCESS"

        result = auth_service.close_gateway(pid=12345)

        assert result == "SUCCESS"

    @patch("ibc.utils.auth.subprocess.run")
    def test_close_uses_stored_pid(self, mock_run, auth_service):
        """Verify close_gateway() uses stored server_process_id."""
        auth_service.server_process_id = 99999
        mock_run.return_value.stdout = b"SUCCESS"

        result = auth_service.close_gateway()

        assert result == "SUCCESS"

    def test_raises_when_no_pid(self, auth_service):
        """Verify close_gateway() raises IBCAuthenticationError when no PID."""
        auth_service.server_process_id = None

        with pytest.raises(IBCAuthenticationError, match="No gateway process ID"):
            auth_service.close_gateway()

    def test_repr(self, auth_service):
        """Verify the service repr."""
        assert "InteractiveBrokersAuthentication" in repr(auth_service)

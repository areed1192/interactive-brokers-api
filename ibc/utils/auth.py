"""Module for handling authentication with the Interactive Brokers Client Portal Gateway."""

from __future__ import annotations

import csv
import logging
import subprocess
import sys
import time
import webbrowser
from typing import TYPE_CHECKING

import requests

from ibc.exceptions import IBCAuthenticationError, IBCRequestError, IBCValidationError
from ibc.models import AuthStatus
from ibc.session import InteractiveBrokersSession

if TYPE_CHECKING:
    from ibc.client import InteractiveBrokersClient

logger = logging.getLogger(__name__)

_GATEWAY_LOGIN_URL = "https://localhost:5000"


class InteractiveBrokersAuthentication:
    """Client for managing authentication with the Interactive Brokers Client Portal Gateway."""

    def __init__(self, ib_client: InteractiveBrokersClient, ib_session: InteractiveBrokersSession) -> None:
        """Initializes the `InteractiveBrokersAuthentication` client.

        ### Parameters
        ----
        ib_client : InteractiveBrokersClient
            The `InteractiveBrokersClient` Python Client.

        ib_session : InteractiveBrokersSession
            The IB session handler.
        """

        self.client = ib_client
        self.session = ib_session
        self.authenticated = False
        self.server_process_id = None

    def __repr__(self) -> str:
        return f"InteractiveBrokersAuthentication(authenticated={self.authenticated})"

    def login(self) -> AuthStatus:
        """Logs the user in to the Client Portal Gateway.

        ### Overview
        ----
        Checks if the user already has an authenticated session before
        starting the gateway. If already authenticated, returns the
        current auth status. If the gateway is running but the session
        is not authenticated, attempts to reauthenticate. Only starts
        the gateway process and opens the browser login page when the
        gateway is not running at all.

        ### Returns
        ----
        AuthStatus:
            The authentication status response from the gateway.
        """

        is_running_response = self._is_already_running()

        if is_running_response["is_running"]:
            logger.info("Gateway already running, checking authentication...")

            try:
                auth_status = self.is_authenticated()

                if auth_status.authenticated:
                    logger.info("Already authenticated, no login needed.")
                    self.authenticated = True
                    return auth_status

                # Gateway running but not authenticated — try to reauthenticate.
                logger.info("Session not authenticated, attempting reauthentication...")
                self.reauthenticate()

                # Verify it worked.
                auth_status = self.is_authenticated()
                if auth_status.authenticated:
                    logger.info("Reauthentication successful.")
                    self.authenticated = True
                    return auth_status

                # Reauthentication failed — open the browser for manual login.
                logger.info("Reauthentication failed, opening browser for manual login.")
                webbrowser.open(url=_GATEWAY_LOGIN_URL)
                return auth_status

            except (IBCRequestError, requests.RequestException):
                # Gateway process exists but isn't responding — open browser.
                logger.info("Gateway not responding, opening browser for manual login.")
                webbrowser.open(url=_GATEWAY_LOGIN_URL)
                return AuthStatus()

        # Gateway not running at all — start it up.
        self._startup_gateway()
        return AuthStatus()

    def wait_for_login(self, timeout: int = 300, poll_interval: int = 3) -> bool:
        """Polls the gateway until the user has authenticated or the timeout expires.

        ### Overview
        ----
        Calls ``login()`` and then polls ``check_auth()`` at regular intervals
        until the session is authenticated. Designed to replace the manual
        ``while not authenticated`` polling loops in calling code.

        ### Parameters
        ----
        timeout : int (optional, Default=300)
            Maximum number of seconds to wait for authentication before
            raising an error. Defaults to 5 minutes.

        poll_interval : int (optional, Default=3)
            Number of seconds between authentication status checks.

        ### Returns
        ----
        bool:
            ``True`` when the user has successfully authenticated.

        ### Raises
        ----
        IBCAuthenticationError:
            If the timeout expires before the user authenticates.
        """

        self.login()

        if self.authenticated:
            return True

        logger.info("Waiting for user to authenticate (timeout=%ds)...", timeout)

        deadline = time.monotonic() + timeout

        while time.monotonic() < deadline:
            time.sleep(poll_interval)
            self.check_auth()

            if self.authenticated:
                logger.info("Authentication successful.")
                return True

        raise IBCAuthenticationError(
            f"Authentication timed out after {timeout} seconds. Please ensure you completed the login in your browser."
        )

    def _startup_gateway(self) -> None:
        """Starts the Client Portal Gateway so the user can authenticate.

        ### Raises
        ----
        IBCAuthenticationError:
            If the gateway files are not installed or the platform is unsupported.
        """

        gateway = self.client.client_portal
        gateway_folder = gateway._gateway_folder

        if not gateway._is_gateway_installed():
            raise IBCAuthenticationError(
                f"Client Portal Gateway is not installed at {gateway_folder}. Call client.client_portal.setup() first."
            )

        if sys.platform == "win32":
            args = [
                "cmd",
                "/k",
                "start",
                "Interactive Brokers Python API",
                r"bin\run.bat",
                r"root\conf.yaml",
            ]
            server_process = subprocess.Popen(
                args=args,
                cwd=str(gateway_folder),
                creationflags=subprocess.CREATE_NEW_CONSOLE,
            )
        else:
            args = ["bash", "bin/run.sh", "root/conf.yaml"]
            server_process = subprocess.Popen(
                args=args,
                cwd=str(gateway_folder),
                start_new_session=True,
            )

        self.server_process_id = server_process.pid
        logger.info("Gateway started with PID %s", self.server_process_id)

        webbrowser.open(url=_GATEWAY_LOGIN_URL)

    def _is_already_running(self) -> dict:
        """Checks whether the gateway process is already running.

        ### Returns
        ----
        dict:
            A dict with ``'is_running'`` (bool) and ``'data'`` keys.
        """

        if sys.platform == "win32":
            return self._is_already_running_windows()

        return self._is_already_running_unix()

    def _is_already_running_windows(self) -> dict:
        """Windows-specific gateway process detection using ``tasklist``.

        ### Returns
        ----
        dict:
            A dict with ``'is_running'`` (bool) and ``'data'`` keys.
        """

        try:
            result = subprocess.run(
                args=[
                    "tasklist",
                    "/fi",
                    "WindowTitle eq Interactive Brokers Python API*",
                    "/FO",
                    "CSV",
                ],
                capture_output=True,
                timeout=10,
                check=False,
            )
            content = result.stdout.decode()
        except (subprocess.TimeoutExpired, OSError) as exc:
            logger.warning("Failed to check gateway process: %s", exc)
            return {"is_running": False, "data": []}

        if "INFO:" in content or not content.strip():
            return {"is_running": False, "data": [content]}

        lines = content.splitlines()
        if len(lines) < 2:
            return {"is_running": False, "data": [content]}

        headers = lines[0].replace('"', "").split(",")
        rows = list(csv.DictReader(f=lines[1:], fieldnames=headers))

        if rows and "PID" in rows[0]:
            self.server_process_id = rows[0]["PID"]
            return {"is_running": True, "data": rows}

        return {"is_running": False, "data": rows}

    def _is_already_running_unix(self) -> dict:
        """Unix/Linux/macOS gateway process detection using ``pgrep``.

        Searches for a running process whose command line contains
        ``clientportal``, which matches the gateway's Java process.

        ### Returns
        ----
        dict:
            A dict with ``'is_running'`` (bool) and ``'data'`` keys.
        """

        try:
            result = subprocess.run(
                args=["pgrep", "-f", "clientportal"],
                capture_output=True,
                timeout=10,
                check=False,
            )
            content = result.stdout.decode().strip()
        except (subprocess.TimeoutExpired, OSError) as exc:
            logger.warning("Failed to check gateway process: %s", exc)
            return {"is_running": False, "data": []}

        if not content:
            return {"is_running": False, "data": []}

        pids = content.splitlines()
        self.server_process_id = pids[0]
        return {"is_running": True, "data": pids}

    def close_gateway(self, pid: int = None) -> str:
        """Closes down the Client Portal Gateway.

        ### Parameters
        ----
        pid : int (optional, Default=None)
            The process ID to terminate. If not provided, uses the
            stored ``server_process_id`` from the last gateway start.

        ### Returns
        ----
        str:
            A message indicating whether the termination was successful.

        ### Raises
        ----
        IBCAuthenticationError:
            If no process ID is available to terminate.
        """

        if pid is None:
            pid = self.server_process_id

        if pid is None:
            raise IBCAuthenticationError("No gateway process ID available. Is the gateway running?")

        if sys.platform == "win32":
            result = subprocess.run(
                args=["Taskkill", "/F", "/PID", str(pid)],
                capture_output=True,
                check=False,
            )
        else:
            result = subprocess.run(
                args=["kill", str(pid)],
                capture_output=True,
                check=False,
            )

        return result.stdout.decode()

    def is_authenticated(self) -> AuthStatus:
        """Checks if session is authenticated.

        ### Overview
        ----
        Current Authentication status to the Brokerage system. Market Data and
        Trading is not possible if not authenticated, e.g. authenticated
        shows `False`.

        ### Returns
        ----
        AuthStatus:
            An ``AuthStatus`` model instance with authentication details.
        """

        content = self.session.make_request(method="post", endpoint="/api/iserver/auth/status")

        return AuthStatus.from_dict(content) if isinstance(content, dict) else AuthStatus()

    def update_server_account(self, account_id: str) -> dict:
        """Sets the account for the session.

        ### Overview
        ----
        If a user has multiple accounts and wants to get orders, trades,
        etc. of an account other than the currently selected account, then
        the user can update the currently selected account using this API
        and then fetch required information for the newly updated account.

        ### Parameters
        ----
        account_id : str
            The account ID you wish to set for the API Session. This will be used to
            grab historical data and make orders.

        ### Returns
        ----
        dict:
            A `ServerAccount` resource.

        ### Raises
        ----
        IBCValidationError:
            If ``account_id`` is empty or not a string.
        """

        if not account_id or not isinstance(account_id, str) or not account_id.strip():
            raise IBCValidationError(f"account_id must be a non-empty string, got {account_id!r}")

        payload = {"acctId": account_id}

        content = self.session.make_request(method="post", endpoint="/api/iserver/account", json_payload=payload)

        return content

    def sso_validate(self) -> dict:
        """Validates the current session for the SSO user.

        ### Returns
        ----
        dict :
            A `Validation` resource.
        """

        content = self.session.make_request(method="post", endpoint="/api/sso/validate")

        return content

    def reauthenticate(self) -> dict:
        """Reauthenticates to the Brokerage system.

        ### Overview
        ----
        When using the CP Gateway, this endpoint provides a way to
        reauthenticate to the Brokerage system as long as there is a
        valid SSO session, see ``sso_validate()``.

        ### Returns
        ----
        dict :
            An `Authentication` resource.
        """

        content = self.session.make_request(method="post", endpoint="/api/iserver/reauthenticate")

        return content

    def tickle(self) -> AuthStatus:
        """Pings the server to keep the session alive.

        ### Overview
        ----
        If the gateway has not received any requests for several minutes
        an open session will automatically timeout. The tickle endpoint
        pings the server to prevent the session from ending.

        ### Returns
        ----
        AuthStatus:
            An ``AuthStatus`` model instance with session status details.
        """

        content = self.session.make_request(method="post", endpoint="/api/tickle")

        return AuthStatus.from_dict(content) if isinstance(content, dict) else AuthStatus()

    def logout(self) -> dict:
        """Logs the user out of the gateway session.

        ### Overview
        ----
        Logs the user out of the gateway session. Any further activity
        requires re-authentication.

        ### Returns
        ----
        dict:
            A logout confirmation resource.
        """

        content = self.session.make_request(method="post", endpoint="/api/logout")

        self.authenticated = False

        return content

    def check_auth(self) -> None:
        """Checks the authentication status and updates the ``authenticated`` flag.

        Silently returns if the gateway is not reachable.
        """

        logger.info("Checking authentication status...")

        try:
            response = self.is_authenticated()
            if response.authenticated:
                self.authenticated = True
        except (IBCRequestError, requests.RequestException):
            return

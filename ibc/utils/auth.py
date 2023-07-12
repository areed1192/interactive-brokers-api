import csv
import os
import subprocess
import webbrowser
from ibc.session import InteractiveBrokersSession


class InteractiveBrokersAuthentication():

    def __init__(self, ib_client: object, ib_session: InteractiveBrokersSession) -> None:
        """Initializes the `InteractiveBrokersAuthentication` client.

        ### Parameters
        ----
        ib_client : object
            The `InteractiveBrokersClient` Python Client.

        ib_session : InteractiveBrokersSession
            The IB session handler.
        """

        from ibc.client import InteractiveBrokersClient

        self.client: InteractiveBrokersClient = ib_client
        self.session: InteractiveBrokersSession = ib_session
        self.authenticated = False
        self.server_process_id = None

        self.is_windows = os.name == 'nt'

    def login(self, _use_selenium: bool = False) -> dict:
        """Logs the user in to the Client Portal Gateway.

        ### Parameters
        ----
        _use_selenium (bool, optional, Default=False):
            If set to `True` will use Selenium to pass through your username and password
            to the login page. Can only be done if use with paper trading account, otherwise
            it will default to `False`. If set to `False` user will be redirected to the
            login form where the user will need to provide their credentials.

        ### Returns
        ----
        dict: 
            The process resource with the process ID of the client portal
            gateway.
        """

        is_running_response = self._is_already_running()

        if not is_running_response['is_running']:
            self._startup_gateway()
        else:
            print("Gateway already running, no need to start back up.")

    def _startup_gateway(self) -> None:
        """Starts the Client Portal Up so the user can authenticate."""

        subprocess_popn_kwargs = {
            "cwd":"ibc/resources/clientportal.beta.gw",
            "start_new_session":True,
            "stdin":subprocess.DEVNULL,
            "stdout":subprocess.DEVNULL,
            "stderr":subprocess.DEVNULL
        }

        if self.is_windows:
            subprocess_popn_kwargs['args'] = [
                "cmd", "/k", "start", "Interactive Brokers Python API", r"bin\run.bat", r"root\conf.yaml"
            ]
            subprocess_popn_kwargs['creationflags'] = subprocess.CREATE_NEW_CONSOLE
        else: 
            subprocess_popn_kwargs['args'] = [
                "bash", "-c", "exec -a Interactive_Brokers_Python_API bin/run.sh root/conf.yaml"
            ]

        server_process = subprocess.Popen(**subprocess_popn_kwargs)

        self.server_process_id = server_process.pid

        webbrowser.open(url='https://localhost:5000')

    def _is_already_running(self) -> dict:
        """Checks whether the gateway is already running.

        Returns
        -------
        dict:
            A response containing the process ID of the gateway
            if any, or a message saying the process wasn't found.
        """

        if self.is_windows:
            command = [
                'tasklist', '/fi', "WindowTitle eq Interactive Brokers Python API*", '/FO', 'CSV'
            ]
        else:
            command = [
                'pgrep', '-f', "Interactive Brokers Python API*"
            ]

        content = subprocess.run(
            args=command,
            capture_output=True
        ).stdout.decode()

        if self.is_windows:
            if 'INFO:' in content:
                data = content
            else:
                content = content.splitlines()
                headers = content[0].replace('"', '').split(',')
                data = content[1:]
                data = list(csv.DictReader(f=data, fieldnames=headers))

            if 'PID' in data[0]:
                self.server_process_id = data[0]['PID']

                return {
                    'is_running': True,
                    'data': data
                }
            else:
                return {
                    'is_running': False,
                    'data': data
                }
        else:
            if content == '':
                data = 'INFO: No tasks are running which match the specified criteria.'
            else:
                data = content.splitlines()
                self.server_process_id = data[0]

                return {
                    'is_running': True,
                    'data': data
                }

        return {
            'is_running': False,
            'data': data
        }

    def close_gateway(self, pid: int = None) -> str:
        """Closes down the Client Portal Gateway.

        Parameters
        ----------
        pid : int, optional (Default=None)
            If you'd like, you can manually close the process.

        Returns
        -------
        str:
            A message will be returned if the termination process was successful.
        """

        if pid is None:
            pid = self.server_process_id

        if self.is_windows:
            command = ['Taskkill', '/F', '/PID', str(pid)]
        else:
            command = ['kill', '-9', str(pid)]

        content = subprocess.run(
            args=command,
            capture_output=True
        )

        return content.stdout.decode()

    def is_authenticated(self, check: bool = False) -> dict:
        """Checks if session is authenticated.

        ### Overview
        ----
        Current Authentication status to the Brokerage system. Market Data and 
        Trading is not possible if not authenticated, e.g. authenticated 
        shows `False`.

        ### Returns
        ----
        dict:
            A dictionary with an authentication flag.   
        """

        # Make the request.
        content = self.session.make_request(
            method='post',
            endpoint='/api/iserver/auth/status'
        )

        return content

    def update_server_account(self, account_id: str) -> dict:
        """Sets the account for the session.

        ### Overview
        ----
        If an user has multiple accounts, and user wants to get orders, trades, 
        etc. of an account other than currently selected account, then user 
        can update the currently selected account using this API and then can 
        fetch required information for the newly updated account.

        ### Parameters
        ----
        account_id : str
            The account ID you wish to set for the API Session. This will be used to
            grab historical data and make orders.

        ### Returns
        ----
        dict:
            A `ServerAccount` resource.
        """

        payload = {
            'acctId': account_id
        }

        # Make the request.
        content = self.session.make_request(
            method='post',
            endpoint='/api/iserver/account',
            json_payload=payload
        )

        return content

    def sso_validate(self) -> dict:
        """Validates the current session for the SSO user.

        ### Returns
        ----
        dict :
            A `Validation` resource.
        """

        # Make the request.
        content = self.session.make_request(
            method='post',
            endpoint='/api/sso/validate'
        )

        return content

    def reauthenticate(self) -> dict:
        """When using the CP Gateway, this endpoint provides a way to
        reauthenticate to the Brokerage system as long as there is a
        valid SSO session, see /sso/validate.

        ### Returns
        ----
        dict :
            An `Authentication` resource.
        """

        # Make the request.
        content = self.session.make_request(
            method='post',
            endpoint='/api/iserver/reauthenticate'
        )

        return content

    def check_auth(self) -> None:
        """Checks the authentication of the user to see
        if they've logged in.
        """

        print("Checking authentication status...")

        try:
            response = self.is_authenticated()
            if response['authenticated'] == True:
                self.authenticated = True
                return
        except Exception:
            return

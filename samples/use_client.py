"""Example usage of the InteractiveBrokersClient initialization and login."""

from configparser import ConfigParser

from ibc.client import InteractiveBrokersClient

# Initialize the Parser.
config = ConfigParser()
config.read('config/config.ini')

# Get the specified credentials.
account_number = config.get('interactive_brokers_paper', 'paper_account')

# ---------------------------------------------------------------------------
# Initialize the client — this also downloads the gateway if needed.
# ---------------------------------------------------------------------------

ibc_client = InteractiveBrokersClient(
    account_number=account_number,
)
# Output: InteractiveBrokersClient(account_number='U1234567')

# ---------------------------------------------------------------------------
# Login and wait for browser-based authentication.
# ---------------------------------------------------------------------------

ibc_client.authentication.wait_for_login()
# Output: True

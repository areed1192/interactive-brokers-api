"""Example usage of the PnL service."""

from configparser import ConfigParser
from pprint import pprint

from ibc.client import InteractiveBrokersClient

config = ConfigParser()
config.read('config/config.ini')

account_number = config.get('interactive_brokers_paper', 'paper_account')
account_password = config.get('interactive_brokers_paper', 'paper_password')

ibc_client = InteractiveBrokersClient(
    account_number=account_number,
    password=account_password
)
ibc_client.authentication.wait_for_login()

pnl_service = ibc_client.pnl

# ---------------------------------------------------------------------------
# Get PnL for the currently selected server account.
# ---------------------------------------------------------------------------

pprint(pnl_service.pnl_server_account())
# Output: {'upnl': {'U1234567': {'dpl': -12.34, 'nl': 50000.0, ...}}}

"""Example usage of the Accounts service."""

from configparser import ConfigParser
from pprint import pprint

from ibc.client import InteractiveBrokersClient

config = ConfigParser()
config.read('config/config.ini')

account_number = config.get('interactive_brokers_paper', 'paper_account')

ibc_client = InteractiveBrokersClient(
    account_number=account_number,
)
ibc_client.authentication.wait_for_login()

accounts_service = ibc_client.accounts

# ---------------------------------------------------------------------------
# List all brokerage accounts.
# ---------------------------------------------------------------------------

pprint(accounts_service.accounts())
# Output: [{'accountId': 'U1234567', 'type': 'INDIVIDUAL', ...}]

# ---------------------------------------------------------------------------
# Get PnL for the currently selected server account.
# ---------------------------------------------------------------------------

pprint(accounts_service.pnl_server_account())
# Output: {'upnl': {'U1234567': {'dpl': -12.34, 'nl': 50000.0, ...}}}

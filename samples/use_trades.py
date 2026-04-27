"""Example usage of the Trades service."""

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

trades_service = ibc_client.trades

# ---------------------------------------------------------------------------
# Get recent trades.
# ---------------------------------------------------------------------------

pprint(trades_service.get_trades())
# Output: [{'execution_id': '...', 'symbol': 'AAPL', 'side': 'BUY', ...}]

"""Example usage of the Market Data service."""

from configparser import ConfigParser
from pprint import pprint

from ibc.client import InteractiveBrokersClient
from ibc.utils.enums import BarTypes

config = ConfigParser()
config.read('config/config.ini')

account_number = config.get('interactive_brokers_paper', 'paper_account')
account_password = config.get('interactive_brokers_paper', 'paper_password')

ibc_client = InteractiveBrokersClient(
    account_number=account_number,
    password=account_password
)
ibc_client.authentication.wait_for_login()

market_data_service = ibc_client.market_data

# ---------------------------------------------------------------------------
# Get a real-time quote snapshot.
# ---------------------------------------------------------------------------

pprint(market_data_service.snapshot(contract_ids=['265598']))
# Output: [{'conid': 265598, '31': '150.25', '84': '149.80', ...}]

# ---------------------------------------------------------------------------
# Get historical market data (5-minute bars over 5 days).
# ---------------------------------------------------------------------------

pprint(
    market_data_service.market_history(
        contract_id='265598',
        period='5d',
        market_bar=BarTypes.FiveMinute
    )
)
# Output: {'bars': [{'t': 1234567890, 'o': 150.0, 'c': 150.5, ...}]}

# ---------------------------------------------------------------------------
# Unsubscribe from market data for a contract.
# ---------------------------------------------------------------------------

pprint(market_data_service.unsubscribe(contract_id='265598'))
# Output: {'confirmed': True}

# ---------------------------------------------------------------------------
# Unsubscribe from all market data.
# ---------------------------------------------------------------------------

pprint(market_data_service.unsubscribe_all())
# Output: {'confirmed': True}

# ---------------------------------------------------------------------------
# Get market history (beta endpoint with HMDS).
# ---------------------------------------------------------------------------

pprint(
    market_data_service.market_history_beta(
        contract_id='265598',
        period='5d',
        market_bar='1h'
    )
)
# Output: [{'t': 1234567890, 'o': 150.0, 'c': 150.5, ...}]

# ---------------------------------------------------------------------------
# Get snapshot (beta endpoint).
# ---------------------------------------------------------------------------

pprint(market_data_service.snapshot_beta(contract_ids=['265598'], fields=['31', '84']))
# Output: [{'conid': 265598, '31': '150.25', '84': '149.80'}]

# ---------------------------------------------------------------------------
# Run a market scanner (beta HMDS endpoint).
# ---------------------------------------------------------------------------

scanner_body = {
    'instrument': 'STK',
    'locations': 'STK.US.MAJOR',
    'scanCode': 'TOP_PERC_GAIN',
}

pprint(market_data_service.scanner_beta(scanner=scanner_body))
# Output: [{'conid': 265598, 'symbol': 'AAPL', ...}]

"""Example usage of the Scanners service."""

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

scanners_service = ibc_client.scanners

# ---------------------------------------------------------------------------
# Get available scanner types and filter parameters.
# ---------------------------------------------------------------------------

pprint(scanners_service.scanners())
# Output: {'instrument_list': [...], 'scan_type_list': [...], ...}

# ---------------------------------------------------------------------------
# Run a scanner to find stocks matching criteria.
# ---------------------------------------------------------------------------

scanner = {
    "instrument": "STK",
    "type": "NOT_YET_TRADED_TODAY",
    "filter": [
        {"code": "priceAbove", "value": 50},
        {"code": "priceBelow", "value": 70},
        {"code": "volumeAbove", "value": None},
        {"code": "volumeBelow", "value": None},
    ],
    "location": "STK.US.MAJOR",
    "size": "25",
}

pprint(scanners_service.run_scanner(scanner=scanner))
# Output: [{'conid': 265598, 'symbol': 'AAPL', ...}]

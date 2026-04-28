"""Example usage of the Customer service."""

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

customer_service = ibc_client.customers

# ---------------------------------------------------------------------------
# Get customer entity information.
# ---------------------------------------------------------------------------

pprint(customer_service.customer_info())
# Output: {'applicantId': 12345, 'accountId': 'U1234567', ...}

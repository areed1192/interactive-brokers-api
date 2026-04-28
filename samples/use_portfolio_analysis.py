"""Example usage of the Portfolio Analysis service."""

from configparser import ConfigParser
from pprint import pprint

from ibc.client import InteractiveBrokersClient
from ibc.utils.enums import Frequency

config = ConfigParser()
config.read('config/config.ini')

account_number = config.get('interactive_brokers_paper', 'paper_account')

ibc_client = InteractiveBrokersClient(
    account_number=account_number,
)
ibc_client.authentication.wait_for_login()

analysis_service = ibc_client.portfolio_analysis

# ---------------------------------------------------------------------------
# Get account summary.
# ---------------------------------------------------------------------------

pprint(
    analysis_service.account_summary(
        account_ids=[ibc_client.account_number]
    )
)
# Output: {'rc': 0, 'view': '...', ...}

# ---------------------------------------------------------------------------
# Get account performance (quarterly).
# ---------------------------------------------------------------------------

pprint(
    analysis_service.account_performance(
        account_ids=[ibc_client.account_number],
        frequency=Frequency.Quarterly
    )
)
# Output: {'currencyType': 'base', 'rc': 0, ...}

# ---------------------------------------------------------------------------
# Get transaction history.
# ---------------------------------------------------------------------------

pprint(
    analysis_service.transactions_history(
        account_ids=[ibc_client.account_number]
    )
)
# Output: {'id': '...', 'currency': 'USD', 'transactions': [...]}

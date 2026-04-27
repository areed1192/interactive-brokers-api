"""Example usage of the Portfolio Accounts service."""

from configparser import ConfigParser
from pprint import pprint

from ibc.client import InteractiveBrokersClient
from ibc.utils.enums import SortDirection, SortFields

config = ConfigParser()
config.read('config/config.ini')

account_number = config.get('interactive_brokers_paper', 'paper_account')
account_password = config.get('interactive_brokers_paper', 'paper_password')

ibc_client = InteractiveBrokersClient(
    account_number=account_number,
    password=account_password
)
ibc_client.authentication.wait_for_login()

portfolio_service = ibc_client.portfolio_accounts

# ---------------------------------------------------------------------------
# List portfolio accounts.
# ---------------------------------------------------------------------------

pprint(portfolio_service.accounts())
# Output: [{'accountId': 'U1234567', 'type': 'INDIVIDUAL', ...}]

# ---------------------------------------------------------------------------
# List sub-accounts.
# ---------------------------------------------------------------------------

pprint(portfolio_service.subaccounts())
# Output: [{'acctId': 'U1234567', 'accountTitle': '...', ...}]

# ---------------------------------------------------------------------------
# List sub-accounts (paginated version).
# ---------------------------------------------------------------------------

pprint(portfolio_service.subaccounts2(page=0))
# Output: {'metadata': {'total': 1, ...}, 'subaccounts': [...]}

# ---------------------------------------------------------------------------
# Get account metadata.
# ---------------------------------------------------------------------------

pprint(portfolio_service.account_metadata(account_id=account_number))
# Output: {'accountId': 'U1234567', 'accountTitle': '...', ...}

# ---------------------------------------------------------------------------
# Get account summary.
# ---------------------------------------------------------------------------

pprint(portfolio_service.account_summary(account_id=account_number))
# Output: {'accountready': {'amount': 0.0, ...}, ...}

# ---------------------------------------------------------------------------
# Get account ledger.
# ---------------------------------------------------------------------------

pprint(portfolio_service.account_ledger(account_id=account_number))
# Output: {'BASE': {'cashbalance': 50000.0, ...}}

# ---------------------------------------------------------------------------
# Get account allocation.
# ---------------------------------------------------------------------------

pprint(portfolio_service.account_allocation(account_id=account_number))
# Output: {'assetClass': {'long': {'STK': 0.85, ...}, ...}}

# ---------------------------------------------------------------------------
# Get consolidated portfolio allocation for multiple accounts.
# ---------------------------------------------------------------------------

pprint(
    portfolio_service.portfolio_allocation(
        account_ids=[ibc_client.account_number]
    )
)
# Output: {'assetClass': {'long': {'STK': 0.85, ...}, ...}}

# ---------------------------------------------------------------------------
# Get portfolio positions sorted by unrealized PnL.
# ---------------------------------------------------------------------------

pprint(
    portfolio_service.portfolio_positions(
        account_id=ibc_client.account_number,
        page_id=0,
        sort=SortFields.BaseUnrealizedPnl,
        direction=SortDirection.Descending
    )
)
# Output: [{'conid': 265598, 'position': 10, 'mktValue': 1500.0, ...}]

# ---------------------------------------------------------------------------
# Get a specific position by contract ID.
# ---------------------------------------------------------------------------

pprint(
    portfolio_service.position_by_contract_id(
        account_id=ibc_client.account_number,
        contract_id='251962528'
    )
)
# Output: [{'conid': 251962528, 'position': 5, ...}]

# ---------------------------------------------------------------------------
# Get positions for a contract across all accounts.
# ---------------------------------------------------------------------------

pprint(portfolio_service.positions_by_contract_id(contract_id='251962528'))
# Output: {'U1234567': [{'conid': 251962528, ...}]}

# ---------------------------------------------------------------------------
# Invalidate the backend positions cache.
# ---------------------------------------------------------------------------

pprint(
    portfolio_service.invalidate_positions_cache(
        account_id=ibc_client.account_number
    )
)
# Output: {'message': 'success'}

"""Example usage of the Contracts service."""

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

contracts_service = ibc_client.contracts

# ---------------------------------------------------------------------------
# Get info for a specific contract by ID.
# ---------------------------------------------------------------------------

pprint(contracts_service.contract_info(contract_id='265598'))
# Output: {'conid': 265598, 'symbol': 'AAPL', 'secType': 'STK', ...}

# ---------------------------------------------------------------------------
# Search for futures contracts by symbol.
# ---------------------------------------------------------------------------

pprint(contracts_service.search_futures(symbols=['CL', 'ES']))
# Output: {'CL': [{'conid': ..., 'symbol': 'CL', ...}], ...}

# ---------------------------------------------------------------------------
# Search for multiple contracts by IDs.
# ---------------------------------------------------------------------------

pprint(contracts_service.search_multiple_contracts(contract_ids=[265598]))
# Output: {'265598': {'conid': 265598, 'company_name': 'APPLE INC', ...}}

# ---------------------------------------------------------------------------
# Search for a company by ticker.
# ---------------------------------------------------------------------------

pprint(contracts_service.search_symbol(symbol='MSFT', name=False))
# Output: [{'conid': 272093, 'companyName': 'MICROSOFT CORP', ...}]

# ---------------------------------------------------------------------------
# Search for a company by name.
# ---------------------------------------------------------------------------

pprint(contracts_service.search_symbol(symbol='Microsoft', name=True))
# Output: [{'conid': 272093, 'companyName': 'MICROSOFT CORP', ...}]

# ---------------------------------------------------------------------------
# Search for stock contracts by symbol.
# ---------------------------------------------------------------------------

pprint(contracts_service.search_stocks(symbols=['AAPL', 'MSFT']))
# Output: {'AAPL': [{'conid': 265598, 'name': 'APPLE INC', ...}], ...}

# ---------------------------------------------------------------------------
# Get trading schedule for a symbol.
# ---------------------------------------------------------------------------

pprint(contracts_service.trading_schedule(asset_class='STK', symbol='AAPL'))
# Output: {'schedules': [{'tradingTime': '09:30-16:00', ...}]}

# ---------------------------------------------------------------------------
# Get option strikes for a contract.
# ---------------------------------------------------------------------------

pprint(
    contracts_service.secdef_strikes(
        contract_id='265598', sectype='OPT', month='202501'
    )
)
# Output: {'call': [100, 110, 120, ...], 'put': [100, 110, 120, ...]}

# ---------------------------------------------------------------------------
# Get security definition info for an option.
# ---------------------------------------------------------------------------

pprint(
    contracts_service.secdef_info(
        contract_id='265598', sectype='OPT', month='202501',
        strike='150', right='C'
    )
)
# Output: [{'conid': 123456, 'symbol': 'AAPL', 'right': 'C', ...}]

# ---------------------------------------------------------------------------
# Get IB Algo parameters for a contract.
# ---------------------------------------------------------------------------

pprint(contracts_service.contract_algos(contract_id='265598'))
# Output: [{'name': 'Adaptive', 'id': 'Adaptive', 'params': [...]}]

# ---------------------------------------------------------------------------
# Get trading rules for a contract.
# ---------------------------------------------------------------------------

pprint(contracts_service.contract_rules(contract_id='265598', is_buy=True))
# Output: {'orderTypes': ['LMT', 'MKT', ...], 'tifTypes': ['DAY', 'GTC', ...]}

# ---------------------------------------------------------------------------
# Get combined info and rules for a contract.
# ---------------------------------------------------------------------------

pprint(contracts_service.contract_info_and_rules(contract_id='265598', is_buy=True))
# Output: {'conid': 265598, 'symbol': 'AAPL', 'rules': {...}}

# ---------------------------------------------------------------------------
# Get available currency pairs.
# ---------------------------------------------------------------------------

pprint(contracts_service.currency_pairs(currency='USD'))
# Output: {'USD': [{'symbol': 'EUR.USD', 'conid': 12087792, ...}]}

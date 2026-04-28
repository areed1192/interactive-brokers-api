"""Example usage of typed dataclass models returned by the API."""

from configparser import ConfigParser
from pprint import pprint

from ibc.client import InteractiveBrokersClient
from ibc.models import OrderRequest, ScannerFilter, ScannerParams
from ibc.utils.enums import BarTypes

config = ConfigParser()
config.read('config/config.ini')

account_number = config.get('interactive_brokers_paper', 'paper_account')

ibc_client = InteractiveBrokersClient(
    account_number=account_number,
)
ibc_client.authentication.wait_for_login()

# ---------------------------------------------------------------------------
# Typed contract info — access properties instead of raw dict keys.
# ---------------------------------------------------------------------------

contract = ibc_client.contracts.contract_info(contract_id='265598')
print(f"Company: {contract.company_name}")
print(f"Symbol:  {contract.local_symbol}")
print(f"Type:    {contract.instrument_type}")
print(f"Exchange: {contract.exchange}")
# Output: Company: APPLE INC
# Output: Symbol:  AAPL
# Output: Type:    STK
# Output: Exchange: NASDAQ

# ---------------------------------------------------------------------------
# Market data snapshot — typed fields from numeric API keys.
# ---------------------------------------------------------------------------

snapshots = ibc_client.market_data.snapshot(contract_ids=['265598'])
for quote in snapshots:
    print(f"[{quote.conid}] Last: {quote.last_price}  "
          f"Bid: {quote.bid_price}  Ask: {quote.ask_price}")
# Output: [265598] Last: 150.25  Bid: 149.80  Ask: 150.30

# ---------------------------------------------------------------------------
# Historical data — iterate over typed HistoryBar objects.
# ---------------------------------------------------------------------------

history = ibc_client.market_data.market_history(
    contract_id='265598',
    period='1d',
    market_bar=BarTypes.FiveMinute,
)
print(f"\n{history.symbol} — {history.time_period} ({len(history.data)} bars)")
for bar in history.data[:3]:
    print(f"  O={bar.open:.2f}  H={bar.high:.2f}  "
          f"L={bar.low:.2f}  C={bar.close:.2f}  V={bar.volume:.0f}")
# Output: AAPL — 1d (78 bars)
# Output:   O=150.00  H=151.20  L=149.50  C=150.80  V=1234567

# ---------------------------------------------------------------------------
# Build an order with OrderRequest — type-safe construction + to_dict().
# ---------------------------------------------------------------------------

order = OrderRequest(
    conid=265598,
    order_type="LMT",
    side="BUY",
    price=148.50,
    quantity=10,
    tif="DAY",
    outside_rth=True,
)
print("\nOrder payload:")
pprint(order.to_dict())
# Output: {'conid': 265598, 'orderType': 'LMT', 'outsideRTH': True,
#          'price': 148.5, 'quantity': 10, 'side': 'BUY', 'tif': 'DAY'}

# ---------------------------------------------------------------------------
# Build scanner params with typed model.
# ---------------------------------------------------------------------------

scanner = ScannerParams(
    instrument="STK",
    type="TOP_PERC_GAIN",
    location="STK.US.MAJOR",
    filter=[
        ScannerFilter(code="priceAbove", value=10.0),
        ScannerFilter(code="priceBelow", value=500.0),
    ],
)
print("\nScanner payload:")
pprint(scanner.to_dict())
# Output: {'instrument': 'STK', 'type': 'TOP_PERC_GAIN',
#          'location': 'STK.US.MAJOR',
#          'filter': [{'code': 'priceAbove', 'value': 10.0}, ...]}

# ---------------------------------------------------------------------------
# Portfolio positions — typed access to position data.
# ---------------------------------------------------------------------------

positions = ibc_client.portfolio_accounts.portfolio_positions(
    account_id=ibc_client.account_number
)
for pos in positions[:5]:
    print(f"  conid={pos.conid}  qty={pos.position}  avg_cost={pos.avg_cost:.2f}")
# Output:   conid=265598  qty=100.0  avg_cost=142.35

# ---------------------------------------------------------------------------
# Account ledger — typed financial summary.
# ---------------------------------------------------------------------------

ledger = ibc_client.portfolio_accounts.account_ledger(
    account_id=ibc_client.account_number
)
for currency, entry in ledger.items():
    print(f"  [{currency}] NLV={entry.net_liquidation_value:,.2f}  "
          f"Cash={entry.cash_balance:,.2f}  "
          f"Unrealized P&L={entry.unrealized_pnl:,.2f}")
# Output:   [USD] NLV=125,000.00  Cash=50,000.00  Unrealized P&L=3,200.00

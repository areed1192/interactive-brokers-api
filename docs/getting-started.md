# Getting Started

## Requirements

- Python 3.10+
- An Interactive Brokers account (paper or live)
- Java 8 update 192 or higher (OpenJDK 11+ also works)

## Installation

```console
pip install ibc-api
```

For development:

```console
pip install -e ".[dev,docs]"
```

## Authentication

The Client Portal API requires the IB Gateway running locally. On first use, the library
downloads and sets up the gateway automatically.

```python
from ibc.client import InteractiveBrokersClient

ibc_client = InteractiveBrokersClient(
    account_number="U1234567",
    password="your_password"
)

# This starts the gateway and opens a browser for login.
# It blocks until authentication succeeds or times out (default 5 minutes).
ibc_client.authentication.wait_for_login()
```

## Making Requests

All services are accessed as properties on the client. Methods return typed
dataclass models with structured attribute access:

```python
# Market data — returns list[MarketData]
snapshots = ibc_client.market_data.snapshot(contract_ids=["265598"])
for quote in snapshots:
    print(f"Last: {quote.last_price}  Bid: {quote.bid_price}  Ask: {quote.ask_price}")

# Historical bars — returns HistoryData with list[HistoryBar]
history = ibc_client.market_data.market_history(contract_id="265598", period="1d")
for bar in history.data:
    print(f"O={bar.open}  H={bar.high}  L={bar.low}  C={bar.close}")

# Contracts — returns Contract
contract = ibc_client.contracts.contract_info(contract_id="265598")
print(f"{contract.company_name} ({contract.instrument_type})")

# Orders — use OrderRequest for type-safe payload construction
from ibc.models import OrderRequest

order = OrderRequest(conid=265598, order_type="LMT", price=150, side="BUY", quantity=1, tif="DAY")
ibc_client.orders.place_order(account_id=ibc_client.account_number, order=order.to_dict())

# Portfolio positions — returns list[Position]
positions = ibc_client.portfolio.portfolio_positions(
    account_id=ibc_client.account_number, page_id=0
)
for pos in positions:
    print(f"conid={pos.conid}  qty={pos.position}  avg_cost={pos.avg_cost}")
```

See the [Models reference](api/models.md) for the full list of typed response and request models.

## Session Management

Keep your session alive with periodic tickle calls:

```python
ibc_client.authentication.tickle()
```

When done, log out cleanly:

```python
ibc_client.authentication.logout()
```

## SSL Certificates

The gateway uses a self-signed certificate on `localhost:5000`. The library defaults to
`verify_ssl=False`, which is standard for localhost usage. See the README for details on
configuring custom certificates.

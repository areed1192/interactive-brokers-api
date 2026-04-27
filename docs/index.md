# Interactive Brokers Client Portal API

An unofficial Python client for the [Interactive Brokers Client Portal Web API](https://interactivebrokers.github.io/cpwebapi/).

## Installation

```console
pip install ibc-api
```

## Quick Start

```python
from ibc.client import InteractiveBrokersClient

ibc_client = InteractiveBrokersClient(
    account_number="U1234567",
    password="your_password"
)

# Authenticate (opens browser for gateway login).
ibc_client.authentication.wait_for_login()

# Grab a market data snapshot — returns typed MarketData models.
snapshots = ibc_client.market_data.snapshot(contract_ids=["265598"])
for quote in snapshots:
    print(f"{quote.conid}: Last={quote.last_price} Bid={quote.bid_price} Ask={quote.ask_price}")
```

## Documentation

- [Getting Started](getting-started.md) — setup, authentication, first request
- [Models](api/models.md) — typed dataclass models for requests and responses
- [API Reference](api/client.md) — full method documentation auto-generated from source

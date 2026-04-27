# Interactive Brokers Client Portal API

[![Python](https://img.shields.io/pypi/pyversions/ibc-api)](https://pypi.org/project/ibc-api/)
[![PyPI](https://img.shields.io/pypi/v/ibc-api)](https://pypi.org/project/ibc-api/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An unofficial Python client for the [Interactive Brokers Client Portal Web API](https://interactivebrokers.github.io/cpwebapi/).
Manage trades, pull historical and real-time data, manage accounts, create and modify orders — all from Python.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [SSL Certificates](#ssl-certificates)
- [Documentation & Resources](#documentation-and-resources)
- [Support These Projects](#support-these-projects)

## Features

| Service            | Property                        | Description                                                        |
| ------------------ | ------------------------------- | ------------------------------------------------------------------ |
| Authentication     | `ibc_client.authentication`     | Login, logout, session keep-alive, SSO validation                  |
| Accounts           | `ibc_client.accounts`           | Account listing and server PnL                                     |
| Portfolio          | `ibc_client.portfolio_accounts` | Positions, ledger, allocation, sub-accounts                        |
| Orders             | `ibc_client.orders`             | Place, modify, cancel, bracket, and what-if orders                 |
| Trades             | `ibc_client.trades`             | Query executed trades                                              |
| Market Data        | `ibc_client.market_data`        | Snapshots, historical bars, subscriptions                          |
| Contracts          | `ibc_client.contracts`          | Search stocks/futures/options, security definitions, trading rules |
| Alerts             | `ibc_client.alerts`             | Create, activate, delete, and query alerts                         |
| Scanners           | `ibc_client.scanners`           | Market scanner parameters and execution                            |
| PnL                | `ibc_client.pnl`                | Real-time profit and loss                                          |
| FYI                | `ibc_client.fyi`                | Notifications, delivery options, disclaimers                       |
| Portfolio Analysis | `ibc_client.portfolio_analysis` | Performance summaries and transaction history                      |
| Customer           | `ibc_client.customers`          | Customer info                                                      |
| Data               | `ibc_client.data_services`      | News, calendar, and research data                                  |

## Requirements

- Python 3.10+
- An Interactive Brokers account (paper or live)
- [Java 8](https://developers.redhat.com/products/openjdk/download) update 192 or higher (OpenJDK 11+ also works)
- The [Client Portal Gateway](https://www.interactivebrokers.com/en/index.php?f=45185) (downloaded automatically on first use)

## Installation

Install from PyPI:

```console
pip install ibc-api
```

Or install in development mode from source:

```console
git clone https://github.com/areed1192/interactive-brokers-api.git
cd interactive-brokers-api
pip install -e ".[dev]"
```

## Quick Start

```python
from ibc import InteractiveBrokersClient

# Initialize the client.
ibc_client = InteractiveBrokersClient(
    account_number="U1234567",
    password="your_password"
)

# Authenticate (opens browser for gateway login).
ibc_client.authentication.wait_for_login()

# Grab a market data snapshot.
snapshot = ibc_client.market_data.snapshot(contract_ids=["265598"])
print(snapshot)

# Search for a contract.
results = ibc_client.contracts.search_symbol(symbol="AAPL")
print(results)

# Place an order.
order = {
    "conid": 265598,
    "orderType": "LMT",
    "price": 150.00,
    "side": "BUY",
    "quantity": 1,
    "tif": "DAY",
}
response = ibc_client.orders.place_order(
    account_id=ibc_client.account_number,
    order=order
)
print(response)
```

See the [`samples/`](samples/) directory for more complete examples.

## SSL Certificates

The Client Portal Gateway uses a self-signed SSL certificate on `localhost:5000`. Your browser will
warn about an insecure connection when you open the login page — this is expected. The connection is
only "insecure" between your code and your own machine; requests from the gateway to Interactive Brokers
are fully encrypted.

This library defaults to `verify_ssl=False` and suppresses the corresponding `urllib3` warnings, which
is the standard approach for localhost gateway usage.

If you want stricter local SSL verification, you can replace the gateway's keystore and pass
`verify_ssl=True`:

1. Generate a self-signed certificate and import it into a Java KeyStore (requires `keytool` from your
   Java installation):

   ```console
   keytool -genkey -keyalg RSA -alias selfsigned -keystore my.jks -storepass mypassword -validity 730 -keysize 2048
   ```

2. Replace `ibc/resources/clientportal.beta.gw/root/vertx.jks` with your new `my.jks` file and update
   `sslPwd` in `root/conf.yaml` to match your store password.

3. Pass `verify_ssl=True` (or a path to your CA bundle) when creating the client. You will also need to
   trust the certificate in your OS or Python's `certifi` bundle.

For most users, the default `verify_ssl=False` is the correct choice.

## Documentation and Resources

- [Getting Started](https://interactivebrokers.github.io/cpwebapi/index.html#login)
- [Endpoints](https://interactivebrokers.com/api/doc.html)
- [Websockets](https://interactivebrokers.github.io/cpwebapi/RealtimeSubscription.html)
- [Trade Workstation API](http://interactivebrokers.github.io/tws-api/)
- [Client Portal API](https://interactivebrokers.github.io/cpwebapi/)
- [Third Party API](https://www.interactivebrokers.com/webtradingapi/)

## Support These Projects

**Patreon:**
Help support this project and future projects by donating to my [Patreon Page](https://www.patreon.com/sigmacoding). I'm
always looking to add more content for individuals like yourself, unfortunately some of the APIs I would require me to
pay monthly fees.

**YouTube:**
If you'd like to watch more of my content, feel free to visit my YouTube channel [Sigma Coding](https://www.youtube.com/c/SigmaCoding).

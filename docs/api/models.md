# Models

Typed dataclass models provide structured access to API responses. All models are
frozen (immutable) and constructed via `from_dict()` classmethods. Request models
also provide `to_dict()` for building API payloads.

## Response Models

### Authentication

::: ibc.models.AuthStatus

### Accounts

::: ibc.models.Account

### Contracts

::: ibc.models.Contract

::: ibc.models.SecdefInfo

### Market Data

::: ibc.models.MarketData

::: ibc.models.HistoryData

::: ibc.models.HistoryBar

### Orders

::: ibc.models.Order

::: ibc.models.OrderStatus

### Trades

::: ibc.models.Trade

### Portfolio

::: ibc.models.Position

::: ibc.models.Ledger

### Alerts

::: ibc.models.AlertResponse

::: ibc.models.AlertCondition

### Scanners

::: ibc.models.ScannerResult

::: ibc.models.ScannerContract

### Portfolio Analysis

::: ibc.models.Transactions

::: ibc.models.Transaction

::: ibc.models.Summary

## Request Models

### Orders

::: ibc.models.OrderRequest

::: ibc.models.ModifyOrder

### Scanners

::: ibc.models.ScannerParams

::: ibc.models.ScannerFilter

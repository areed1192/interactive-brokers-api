"""Typed response models for the Interactive Brokers API.

Dataclasses generated from the IB Client Portal Web API v1.0.0 Swagger spec
(``api_doc.json``). Each model wraps the raw JSON dict returned by the API and
provides typed property access with sensible defaults for missing keys.
"""

from __future__ import annotations

from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class AuthStatus:
    """Authentication status response from ``/iserver/auth/status``."""

    authenticated: bool = False
    connected: bool = False
    competing: bool = False
    fail: str = ""
    message: str = ""
    prompts: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> AuthStatus:
        """Create an AuthStatus from a raw API response dict."""
        return cls(
            authenticated=data.get("authenticated", False),
            connected=data.get("connected", False),
            competing=data.get("competing", False),
            fail=data.get("fail", ""),
            message=data.get("message", ""),
            prompts=data.get("prompts") or [],
        )


# ---------------------------------------------------------------------------
# Account
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Account:
    """Account details from ``/portfolio/accounts``."""

    id: str = ""
    account_id: str = ""
    account_van: str = ""
    account_title: str = ""
    display_name: str = ""
    account_alias: str = ""
    account_status: float = 0
    currency: str = ""
    type: str = ""
    trading_type: str = ""
    faclient: bool = False
    clearing_status: str = ""
    covestor: bool = False
    desc: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> Account:
        """Create an Account from a raw API response dict."""
        return cls(
            id=data.get("id", ""),
            account_id=data.get("accountId", ""),
            account_van=data.get("accountVan", ""),
            account_title=data.get("accountTitle", ""),
            display_name=data.get("displayName", ""),
            account_alias=data.get("accountAlias", ""),
            account_status=data.get("accountStatus", 0),
            currency=data.get("currency", ""),
            type=data.get("type", ""),
            trading_type=data.get("tradingType", ""),
            faclient=data.get("faclient", False),
            clearing_status=data.get("clearingStatus", ""),
            covestor=data.get("covestor", False),
            desc=data.get("desc", ""),
        )


# ---------------------------------------------------------------------------
# Contract / Security Definition
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Contract:
    """Contract info from ``/iserver/contract/{conid}/info``."""

    r_t_h: bool = False
    con_id: str = ""
    company_name: str = ""
    exchange: str = ""
    local_symbol: str = ""
    instrument_type: str = ""
    currency: str = ""
    category: str = ""
    industry: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> Contract:
        """Create a Contract from a raw API response dict."""
        return cls(
            r_t_h=data.get("r_t_h", False),
            con_id=str(data.get("con_id", "")),
            company_name=data.get("company_name") or data.get("companyName", ""),
            exchange=data.get("exchange", ""),
            local_symbol=data.get("local_symbol", ""),
            instrument_type=data.get("instrument_type", ""),
            currency=data.get("currency", ""),
            category=data.get("category", ""),
            industry=data.get("industry", ""),
        )


@dataclass(frozen=True)
class SecdefInfo:
    """Security definition from ``/trsrv/secdef``."""

    conid: int = 0
    symbol: str = ""
    sec_type: str = ""
    exchange: str = ""
    listing_exchange: str = ""
    right: str = ""
    strike: str = ""
    currency: str = ""
    cusip: str = ""
    coupon: str = ""
    desc1: str = ""
    desc2: str = ""
    maturity_date: str = ""
    multiplier: str = ""
    trading_class: str = ""
    valid_exchanges: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> SecdefInfo:
        """Create a SecdefInfo from a raw API response dict."""
        return cls(
            conid=data.get("conid", 0),
            symbol=data.get("symbol", ""),
            sec_type=data.get("secType", ""),
            exchange=data.get("exchange", ""),
            listing_exchange=data.get("listingExchange", ""),
            right=data.get("right", ""),
            strike=str(data.get("strike", "")),
            currency=data.get("currency", ""),
            cusip=data.get("cusip", ""),
            coupon=str(data.get("coupon", "")),
            desc1=data.get("desc1", ""),
            desc2=data.get("desc2", ""),
            maturity_date=data.get("maturityDate", ""),
            multiplier=str(data.get("multiplier", "")),
            trading_class=data.get("tradingClass", ""),
            valid_exchanges=data.get("validExchanges", ""),
        )


# ---------------------------------------------------------------------------
# Orders
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Order:
    """Live order from ``/iserver/account/orders``."""

    acct: str = ""
    conid: int = 0
    order_desc: str = ""
    description1: str = ""
    ticker: str = ""
    sec_type: str = ""
    listing_exchange: str = ""
    remaining_quantity: str = ""
    filled_quantity: str = ""
    company_name: str = ""
    status: str = ""
    orig_order_type: str = ""
    side: str = ""
    price: float = 0.0
    order_id: int = 0
    parent_id: int = 0
    order_ref: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> Order:
        """Create an Order from a raw API response dict."""
        return cls(
            acct=data.get("acct", ""),
            conid=data.get("conid", 0),
            order_desc=data.get("orderDesc", ""),
            description1=data.get("description1", ""),
            ticker=data.get("ticker", ""),
            sec_type=data.get("secType", ""),
            listing_exchange=data.get("listingExchange", ""),
            remaining_quantity=str(data.get("remainingQuantity", "")),
            filled_quantity=str(data.get("filledQuantity", "")),
            company_name=data.get("companyName", ""),
            status=data.get("status", ""),
            orig_order_type=data.get("origOrderType", ""),
            side=data.get("side", ""),
            price=data.get("price", 0.0),
            order_id=data.get("orderId", 0),
            parent_id=data.get("parentId", 0),
            order_ref=data.get("order_ref", ""),
        )


@dataclass(frozen=True)
class OrderStatus:
    """Detailed order status from ``/iserver/account/order/status/{orderId}``."""

    sub_type: str = ""
    request_id: str = ""
    order_id: int = 0
    conidex: str = ""
    symbol: str = ""
    side: str = ""
    contract_description_1: str = ""
    listing_exchange: str = ""
    option_acct: str = ""
    company_name: str = ""
    size: str = ""
    total_size: str = ""
    currency: str = ""
    account: str = ""
    order_type: str = ""
    limit_price: str = ""
    stop_price: str = ""
    cum_fill: str = ""
    order_status: str = ""
    order_status_description: str = ""
    tif: str = ""
    order_not_editable: bool = False
    cannot_cancel_order: bool = False
    outside_rth: bool = False
    deactivate_order: bool = False
    use_price_mgmt_algo: bool = False
    sec_type: str = ""
    order_description: str = ""
    order_time: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> OrderStatus:
        """Create an OrderStatus from a raw API response dict."""
        return cls(
            sub_type=data.get("sub_type", ""),
            request_id=str(data.get("request_id", "")),
            order_id=data.get("order_id", 0),
            conidex=data.get("conidex", ""),
            symbol=data.get("symbol", ""),
            side=data.get("side", ""),
            contract_description_1=data.get("contract_description_1", ""),
            listing_exchange=data.get("listing_exchange", ""),
            option_acct=data.get("option_acct", ""),
            company_name=data.get("company_name", ""),
            size=str(data.get("size", "")),
            total_size=str(data.get("total_size", "")),
            currency=data.get("currency", ""),
            account=data.get("account", ""),
            order_type=data.get("order_type", ""),
            limit_price=str(data.get("limit_price", "")),
            stop_price=str(data.get("stop_price", "")),
            cum_fill=str(data.get("cum_fill", "")),
            order_status=data.get("order_status", ""),
            order_status_description=data.get("order_status_description", ""),
            tif=data.get("tif", ""),
            order_not_editable=data.get("order_not_editable", False),
            cannot_cancel_order=data.get("cannot_cancel_order", False),
            outside_rth=data.get("outside_rth", False),
            deactivate_order=data.get("deactivate_order", False),
            use_price_mgmt_algo=data.get("use_price_mgmt_algo", False),
            sec_type=data.get("sec_type", ""),
            order_description=data.get("order_description", ""),
            order_time=data.get("order_time", ""),
        )


@dataclass(frozen=True)
class OrderRequest:
    """Order placement request for ``/iserver/account/{accountId}/orders``."""

    acct_id: str = ""
    conid: int = 0
    conidex: str = ""
    sec_type: str = ""
    c_oid: str = ""
    parent_id: str = ""
    order_type: str = ""
    listing_exchange: str = ""
    is_single_group: bool = False
    outside_rth: bool = False
    price: float | None = None
    aux_price: float | None = None
    side: str = ""
    ticker: str = ""
    tif: str = ""
    trailing_amt: float | None = None
    trailing_type: str = ""
    referrer: str = ""
    quantity: float | None = None
    cash_qty: float | None = None
    fx_qty: float | None = None
    use_adaptive: bool = False
    is_ccy_conv: bool = False
    allocation_method: str = ""
    strategy: str = ""
    strategy_parameters: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        """Convert to the API-expected dict format."""
        result = {}
        if self.acct_id:
            result["acctId"] = self.acct_id
        if self.conid:
            result["conid"] = self.conid
        if self.conidex:
            result["conidex"] = self.conidex
        if self.sec_type:
            result["secType"] = self.sec_type
        if self.c_oid:
            result["cOID"] = self.c_oid
        if self.parent_id:
            result["parentId"] = self.parent_id
        if self.order_type:
            result["orderType"] = self.order_type
        if self.listing_exchange:
            result["listingExchange"] = self.listing_exchange
        if self.is_single_group:
            result["isSingleGroup"] = self.is_single_group
        if self.outside_rth:
            result["outsideRTH"] = self.outside_rth
        if self.price is not None:
            result["price"] = self.price
        if self.aux_price is not None:
            result["auxPrice"] = self.aux_price
        if self.side:
            result["side"] = self.side
        if self.ticker:
            result["ticker"] = self.ticker
        if self.tif:
            result["tif"] = self.tif
        if self.trailing_amt is not None:
            result["trailingAmt"] = self.trailing_amt
        if self.trailing_type:
            result["trailingType"] = self.trailing_type
        if self.referrer:
            result["referrer"] = self.referrer
        if self.quantity is not None:
            result["quantity"] = self.quantity
        if self.cash_qty is not None:
            result["cashQty"] = self.cash_qty
        if self.fx_qty is not None:
            result["fxQty"] = self.fx_qty
        if self.use_adaptive:
            result["useAdaptive"] = self.use_adaptive
        if self.is_ccy_conv:
            result["isCcyConv"] = self.is_ccy_conv
        if self.allocation_method:
            result["allocationMethod"] = self.allocation_method
        if self.strategy:
            result["strategy"] = self.strategy
        if self.strategy_parameters:
            result["strategyParameters"] = self.strategy_parameters
        return result


@dataclass(frozen=True)
class ModifyOrder:
    """Order modification request for ``/iserver/account/{accountId}/order/{orderId}``."""

    acct_id: str = ""
    conid: int = 0
    order_type: str = ""
    outside_rth: bool = False
    price: float | None = None
    aux_price: float | None = None
    side: str = ""
    listing_exchange: str = ""
    ticker: str = ""
    tif: str = ""
    quantity: float | None = None
    deactivated: bool = False

    def to_dict(self) -> dict:
        """Convert to the API-expected dict format."""
        result = {}
        if self.acct_id:
            result["acctId"] = self.acct_id
        if self.conid:
            result["conid"] = self.conid
        if self.order_type:
            result["orderType"] = self.order_type
        if self.outside_rth:
            result["outsideRTH"] = self.outside_rth
        if self.price is not None:
            result["price"] = self.price
        if self.aux_price is not None:
            result["auxPrice"] = self.aux_price
        if self.side:
            result["side"] = self.side
        if self.listing_exchange:
            result["listingExchange"] = self.listing_exchange
        if self.ticker:
            result["ticker"] = self.ticker
        if self.tif:
            result["tif"] = self.tif
        if self.quantity is not None:
            result["quantity"] = self.quantity
        if self.deactivated:
            result["deactivated"] = self.deactivated
        return result


# ---------------------------------------------------------------------------
# Trades
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Trade:
    """Trade execution from ``/iserver/account/trades``."""

    execution_id: str = ""
    symbol: str = ""
    side: str = ""
    order_description: str = ""
    trade_time: str = ""
    trade_time_r: float = 0.0
    size: str = ""
    price: str = ""
    order_ref: str = ""
    submitter: str = ""
    exchange: str = ""
    commission: float = 0.0
    net_amount: float = 0.0
    account: str = ""
    account_code: str = ""
    company_name: str = ""
    contract_description_1: str = ""
    sec_type: str = ""
    conid: str = ""
    conidex: str = ""
    position: str = ""
    clearing_id: str = ""
    clearing_name: str = ""
    liquidation_trade: float = 0.0

    @classmethod
    def from_dict(cls, data: dict) -> Trade:
        """Create a Trade from a raw API response dict."""
        return cls(
            execution_id=data.get("execution_id", ""),
            symbol=data.get("symbol", ""),
            side=data.get("side", ""),
            order_description=data.get("order_description", ""),
            trade_time=data.get("trade_time", ""),
            trade_time_r=data.get("trade_time_r", 0.0),
            size=str(data.get("size", "")),
            price=str(data.get("price", "")),
            order_ref=data.get("order_ref", ""),
            submitter=data.get("submitter", ""),
            exchange=data.get("exchange", ""),
            commission=data.get("commission", 0.0),
            net_amount=data.get("net_amount", 0.0),
            account=data.get("account", ""),
            account_code=data.get("acountCode", ""),
            company_name=data.get("company_name", ""),
            contract_description_1=data.get("contract_description_1", ""),
            sec_type=data.get("sec_type", ""),
            conid=str(data.get("conid", "")),
            conidex=data.get("conidex", ""),
            position=str(data.get("position", "")),
            clearing_id=data.get("clearing_id", ""),
            clearing_name=data.get("clearing_name", ""),
            liquidation_trade=data.get("liquidation_trade", 0.0),
        )


# ---------------------------------------------------------------------------
# Market Data / History
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class HistoryBar:
    """Single OHLCV bar from historical market data."""

    timestamp: float = 0.0
    open: float = 0.0
    close: float = 0.0
    high: float = 0.0
    low: float = 0.0
    volume: float = 0.0

    @classmethod
    def from_dict(cls, data: dict) -> HistoryBar:
        """Create a HistoryBar from a raw API response dict."""
        return cls(
            timestamp=data.get("t", 0.0),
            open=data.get("o", 0.0),
            close=data.get("c", 0.0),
            high=data.get("h", 0.0),
            low=data.get("l", 0.0),
            volume=data.get("v", 0.0),
        )


@dataclass(frozen=True)
class HistoryData:
    """Historical market data from ``/iserver/marketdata/history``."""

    symbol: str = ""
    text: str = ""
    price_factor: int = 0
    start_time: str = ""
    high: str = ""
    low: str = ""
    time_period: str = ""
    bar_length: int = 0
    md_availability: str = ""
    mkt_data_delay: int = 0
    outside_rth: bool = False
    trading_day_duration: int = 0
    volume_factor: int = 0
    negative_capable: bool = False
    message_version: int = 0
    data: list[HistoryBar] = field(default_factory=list)
    points: int = 0
    travel_time: int = 0

    @classmethod
    def from_dict(cls, data: dict) -> HistoryData:
        """Create a HistoryData from a raw API response dict."""
        bars = [HistoryBar.from_dict(b) for b in (data.get("data") or [])]
        return cls(
            symbol=data.get("symbol", ""),
            text=data.get("text", ""),
            price_factor=data.get("priceFactor", 0),
            start_time=data.get("startTime", ""),
            high=data.get("high", ""),
            low=data.get("low", ""),
            time_period=data.get("timePeriod", ""),
            bar_length=data.get("barLength", 0),
            md_availability=data.get("mdAvailability", ""),
            mkt_data_delay=data.get("mktDataDelay", 0),
            outside_rth=data.get("outsideRth", False),
            trading_day_duration=data.get("tradingDayDuration", 0),
            volume_factor=data.get("volumeFactor", 0),
            negative_capable=data.get("negativeCapable", False),
            message_version=data.get("messageVersion", 0),
            data=bars,
            points=data.get("points", 0),
            travel_time=data.get("travelTime", 0),
        )


@dataclass(frozen=True)
class MarketData:
    """Real-time market data snapshot from ``/iserver/marketdata/snapshot``."""

    conid: int = 0
    last_price: str = ""
    high: float = 0.0
    low: float = 0.0
    change: str = ""
    change_pct: float = 0.0
    bid_price: str = ""
    bid_size: str = ""
    ask_price: str = ""
    ask_size: str = ""
    volume: str = ""
    min_tick: float = 0.0

    @classmethod
    def from_dict(cls, data: dict) -> MarketData:
        """Create a MarketData from a raw API response dict."""
        return cls(
            conid=data.get("conid", 0),
            last_price=str(data.get("31", "")),
            high=data.get("70", 0.0),
            low=data.get("71", 0.0),
            change=str(data.get("82", "")),
            change_pct=data.get("83", 0.0),
            bid_price=str(data.get("84", "")),
            bid_size=str(data.get("88", "")),
            ask_price=str(data.get("86", "")),
            ask_size=str(data.get("85", "")),
            volume=str(data.get("87", "")),
            min_tick=data.get("minTick", 0.0),
        )


# ---------------------------------------------------------------------------
# Portfolio / Positions
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Position:
    """Position data from ``/portfolio/{accountId}/positions``."""

    conid: int = 0
    position: float = 0.0
    avg_cost: float = 0.0

    @classmethod
    def from_dict(cls, data: dict) -> Position:
        """Create a Position from a raw API response dict."""
        return cls(
            conid=data.get("conid", 0),
            position=data.get("position", 0.0),
            avg_cost=data.get("avgCost", 0.0),
        )


@dataclass(frozen=True)
class Ledger:
    """Account ledger from ``/portfolio/{accountId}/ledger``."""

    commodity_market_value: float = 0.0
    future_market_value: float = 0.0
    settled_cash: float = 0.0
    exchange_rate: float = 0.0
    session_id: int = 0
    cash_balance: float = 0.0
    corporate_bonds_market_value: float = 0.0
    warrants_market_value: float = 0.0
    net_liquidation_value: float = 0.0
    interest: float = 0.0
    unrealized_pnl: float = 0.0
    stock_market_value: float = 0.0
    money_funds: float = 0.0
    currency: str = ""
    realized_pnl: float = 0.0
    funds: float = 0.0
    acct_code: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> Ledger:
        """Create a Ledger from a raw API response dict."""
        return cls(
            commodity_market_value=data.get("commoditymarketvalue", 0.0),
            future_market_value=data.get("futuremarketvalue", 0.0),
            settled_cash=data.get("settledcash", 0.0),
            exchange_rate=data.get("exchangerate", 0.0),
            session_id=data.get("sessionid", 0),
            cash_balance=data.get("cashbalance", 0.0),
            corporate_bonds_market_value=data.get("corporatebondsmarketvalue", 0.0),
            warrants_market_value=data.get("warrantsmarketvalue", 0.0),
            net_liquidation_value=data.get("netliquidationvalue", 0.0),
            interest=data.get("interest", 0.0),
            unrealized_pnl=data.get("unrealizedpnl", 0.0),
            stock_market_value=data.get("stockmarketvalue", 0.0),
            money_funds=data.get("moneyfunds", 0.0),
            currency=data.get("currency", ""),
            realized_pnl=data.get("realizedpnl", 0.0),
            funds=data.get("funds", 0.0),
            acct_code=data.get("acctcode", ""),
        )


# ---------------------------------------------------------------------------
# Alerts
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class AlertCondition:
    """Single condition for an alert."""

    type: int = 0
    conidex: str = ""
    operator: str = ""
    trigger_method: str = ""
    value: str = ""
    logic_bind: str = ""
    time_zone: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> AlertCondition:
        """Create an AlertCondition from a raw API response dict."""
        return cls(
            type=data.get("type", 0),
            conidex=data.get("conidex", ""),
            operator=data.get("operator", ""),
            trigger_method=data.get("triggerMethod", ""),
            value=data.get("value", ""),
            logic_bind=data.get("logicBind", ""),
            time_zone=data.get("timeZone", ""),
        )


@dataclass(frozen=True)
class AlertResponse:
    """Alert details from ``/iserver/account/{accountId}/alerts``."""

    account: str = ""
    order_id: int = 0
    alert_name: str = ""
    alert_message: str = ""
    alert_active: int = 0
    alert_repeatable: int = 0
    alert_email: str = ""
    alert_send_message: int = 0
    tif: str = ""
    expire_time: str = ""
    order_status: str = ""
    outside_rth: int = 0
    itws_orders_only: int = 0
    alert_show_popup: int = 0
    alert_triggered: int = 0
    alert_play_audio: str = ""
    conditions: list[AlertCondition] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> AlertResponse:
        """Create an AlertResponse from a raw API response dict."""
        conditions = [AlertCondition.from_dict(c) for c in (data.get("conditions") or [])]
        return cls(
            account=data.get("account", ""),
            order_id=data.get("order_id", 0),
            alert_name=data.get("alert_name", ""),
            alert_message=data.get("alert_message", ""),
            alert_active=data.get("alert_active", 0),
            alert_repeatable=data.get("alert_repeatable", 0),
            alert_email=data.get("alert_email", ""),
            alert_send_message=data.get("alert_send_message", 0),
            tif=data.get("tif", ""),
            expire_time=data.get("expire_time", ""),
            order_status=data.get("order_status", ""),
            outside_rth=data.get("outsideRth", 0),
            itws_orders_only=data.get("itws_orders_only", 0),
            alert_show_popup=data.get("alert_show_popup", 0),
            alert_triggered=data.get("alert_triggered", 0),
            alert_play_audio=data.get("alert_play_audio", ""),
            conditions=conditions,
        )


# ---------------------------------------------------------------------------
# Scanner
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ScannerFilter:
    """A single filter for a scanner query."""

    code: str = ""
    value: float = 0.0

    @classmethod
    def from_dict(cls, data: dict) -> ScannerFilter:
        """Create a ScannerFilter from a raw API response dict."""
        return cls(
            code=data.get("code", ""),
            value=data.get("value", 0.0),
        )


@dataclass(frozen=True)
class ScannerParams:
    """Scanner parameters for ``/iserver/scanner/run``."""

    instrument: str = ""
    type: str = ""
    location: str = ""
    filter: list[ScannerFilter] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert to the API-expected dict format."""
        result: dict = {}
        if self.instrument:
            result["instrument"] = self.instrument
        if self.type:
            result["type"] = self.type
        if self.location:
            result["location"] = self.location
        if self.filter:
            result["filter"] = [{"code": f.code, "value": f.value} for f in self.filter]
        return result


@dataclass(frozen=True)
class ScannerContract:
    """A single contract in scanner results."""

    in_scan_time: str = ""
    distance: int = 0
    contract_id: int = 0

    @classmethod
    def from_dict(cls, data: dict) -> ScannerContract:
        """Create a ScannerContract from a raw API response dict."""
        return cls(
            in_scan_time=data.get("inScanTime", ""),
            distance=data.get("distance", 0),
            contract_id=data.get("contractID", 0),
        )


@dataclass(frozen=True)
class ScannerResult:
    """Scanner results from ``/iserver/scanner/run``."""

    total: int = 0
    size: int = 0
    offset: int = 0
    scan_time: str = ""
    id: float = 0.0
    position: str = ""
    contracts: list[ScannerContract] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> ScannerResult:
        """Create a ScannerResult from a raw API response dict."""
        contract_list = data.get("Contracts", {}).get("Contract", [])
        contracts = [ScannerContract.from_dict(c) for c in contract_list]
        return cls(
            total=data.get("total", 0),
            size=data.get("size", 0),
            offset=data.get("offset", 0),
            scan_time=data.get("scanTime", ""),
            id=data.get("id", 0.0),
            position=data.get("position", ""),
            contracts=contracts,
        )


# ---------------------------------------------------------------------------
# Portfolio Analysis
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Summary:
    """Account summary value."""

    amount: float = 0.0
    currency: str = ""
    is_null: bool = False
    timestamp: int = 0
    value: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> Summary:
        """Create a Summary from a raw API response dict."""
        return cls(
            amount=data.get("amount", 0.0),
            currency=data.get("currency", ""),
            is_null=data.get("isNull", False),
            timestamp=data.get("timestamp", 0),
            value=data.get("value", ""),
        )


@dataclass(frozen=True)
class Transaction:
    """A single transaction entry."""

    acct_id: str = ""
    conid: float = 0.0
    currency: str = ""
    fx_rate: float = 0.0
    desc: str = ""
    date: str = ""
    type: str = ""
    qty: float = 0.0
    price: float = 0.0
    amount: float = 0.0

    @classmethod
    def from_dict(cls, data: dict) -> Transaction:
        """Create a Transaction from a raw API response dict."""
        return cls(
            acct_id=data.get("acctid", ""),
            conid=data.get("conid", 0.0),
            currency=data.get("cur", ""),
            fx_rate=data.get("fxRate", 0.0),
            desc=data.get("desc", ""),
            date=data.get("date", ""),
            type=data.get("type", ""),
            qty=data.get("qty", 0.0),
            price=data.get("pr", 0.0),
            amount=data.get("amt", 0.0),
        )


@dataclass(frozen=True)
class Transactions:
    """Transaction history from ``/portfolio/{accountId}/transactions``."""

    id: str = ""
    currency: str = ""
    includes_real_time: bool = False
    from_date: float = 0.0
    to_date: float = 0.0
    transactions: list[Transaction] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> Transactions:
        """Create a Transactions from a raw API response dict."""
        txns = [Transaction.from_dict(t) for t in (data.get("transactions") or [])]
        return cls(
            id=data.get("id", ""),
            currency=data.get("currency", ""),
            includes_real_time=data.get("includesRealTime", False),
            from_date=data.get("from", 0.0),
            to_date=data.get("to", 0.0),
            transactions=txns,
        )


# ---------------------------------------------------------------------------
# System
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class IBSystemError:
    """System error response."""

    error: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> IBSystemError:
        """Create an IBSystemError from a raw API response dict."""
        return cls(error=data.get("error", ""))

"""Tests for response models (dataclasses)."""


import pytest

from ibc.models import (
    Account,
    AlertResponse,
    AuthStatus,
    Contract,
    HistoryBar,
    HistoryData,
    IBSystemError,
    Ledger,
    MarketData,
    ModifyOrder,
    Order,
    OrderRequest,
    OrderStatus,
    Position,
    ScannerFilter,
    ScannerParams,
    ScannerResult,
    SecdefInfo,
    Summary,
    Trade,
    Transactions,
)

# ---------------------------------------------------------------------------
# Sample raw data fixtures
# ---------------------------------------------------------------------------

SAMPLE_AUTH_STATUS = {
    "authenticated": True,
    "connected": True,
    "competing": False,
    "fail": "",
    "message": "All good",
    "prompts": ["prompt1"],
}

SAMPLE_ACCOUNT = {
    "id": "123",
    "accountId": "U1234567",
    "accountVan": "MyAccount",
    "accountTitle": "Individual",
    "displayName": "Main Account",
    "accountAlias": "Alias1",
    "accountStatus": 1234567890,
    "currency": "USD",
    "type": "INDIVIDUAL",
    "tradingType": "UNI",
    "faclient": False,
    "clearingStatus": "O",
    "covestor": False,
    "desc": "U1234567 - Alias1",
}

SAMPLE_CONTRACT = {
    "r_t_h": True,
    "con_id": "265598",
    "company_name": "Apple Inc",
    "exchange": "NASDAQ",
    "local_symbol": "AAPL",
    "instrument_type": "STK",
    "currency": "USD",
    "companyName": "Apple Inc",
    "category": "Technology",
    "industry": "Computers",
}

SAMPLE_SECDEF_INFO = {
    "conid": 265598,
    "symbol": "AAPL",
    "secType": "STK",
    "exchange": "SMART",
    "listingExchange": "NASDAQ",
    "right": "",
    "strike": "0",
    "currency": "USD",
    "cusip": "",
    "coupon": "",
    "desc1": "APPLE INC",
    "desc2": "",
    "maturityDate": "",
    "multiplier": "1",
    "tradingClass": "AAPL",
    "validExchanges": "SMART,AMEX,NYSE",
}

SAMPLE_ORDER = {
    "acct": "U1234567",
    "conid": 265598,
    "orderDesc": "BUY 100 AAPL LIMIT 150.00",
    "description1": "AAPL",
    "ticker": "AAPL",
    "secType": "STK",
    "listingExchange": "NASDAQ",
    "remainingQuantity": "100",
    "filledQuantity": "0",
    "companyName": "APPLE INC",
    "status": "Submitted",
    "origOrderType": "LIMIT",
    "side": "BUY",
    "price": 150.0,
    "orderId": 12345,
    "parentId": 0,
    "order_ref": "my-order-1",
}

SAMPLE_ORDER_STATUS = {
    "sub_type": "",
    "request_id": "req123",
    "order_id": 12345,
    "conidex": "265598",
    "symbol": "AAPL",
    "side": "B",
    "contract_description_1": "AAPL Stock (NASDAQ)",
    "listing_exchange": "NASDAQ",
    "company_name": "APPLE INC",
    "size": "100",
    "total_size": "100",
    "currency": "USD",
    "account": "U1234567",
    "order_type": "LIMIT",
    "limit_price": "150.00",
    "stop_price": "0",
    "cum_fill": "0",
    "order_status": "Submitted",
    "order_status_description": "Order working",
    "tif": "DAY",
    "order_not_editable": False,
    "cannot_cancel_order": False,
    "outside_rth": False,
    "deactivate_order": False,
    "use_price_mgmt_algo": True,
    "sec_type": "STK",
    "order_description": "BUY 100 LIMIT 150.0 DAY",
    "order_time": "1700000000",
}

SAMPLE_TRADE = {
    "execution_id": "exec123",
    "symbol": "AAPL",
    "side": "B",
    "order_description": "BUY 100 @ 150.00",
    "trade_time": "20231115-10:30:00",
    "trade_time_r": 1700000000.0,
    "size": "100",
    "price": "150.00",
    "order_ref": "my-order",
    "submitter": "user1",
    "exchange": "NASDAQ",
    "commission": 1.0,
    "net_amount": 15000.0,
    "account": "U1234567",
    "acountCode": "U1234567",
    "company_name": "APPLE INC",
    "contract_description_1": "AAPL Stock",
    "sec_type": "STK",
    "conid": "265598",
    "conidex": "265598@SMART",
    "position": "100",
    "clearing_id": "",
    "clearing_name": "",
    "liquidation_trade": 0,
}

SAMPLE_HISTORY_DATA = {
    "symbol": "AAPL",
    "text": "Apple Inc",
    "priceFactor": 100,
    "startTime": "20231101-09:30:00",
    "high": "155/1000/60",
    "low": "148/500/0",
    "timePeriod": "1d",
    "barLength": 300,
    "mdAvailability": "S",
    "mktDataDelay": 0,
    "outsideRth": False,
    "tradingDayDuration": 23400,
    "volumeFactor": 100,
    "negativeCapable": False,
    "messageVersion": 2,
    "data": [
        {"t": 1700000000, "o": 150.0, "c": 151.5, "h": 152.0, "l": 149.5, "v": 10000},
        {"t": 1700000300, "o": 151.5, "c": 152.0, "h": 152.5, "l": 151.0, "v": 8000},
    ],
    "points": 2,
    "travelTime": 50,
}

SAMPLE_MARKET_DATA = {
    "conid": 265598,
    "31": "150.50",
    "70": 152.0,
    "71": 149.0,
    "82": "+1.50",
    "83": 1.01,
    "84": "150.45",
    "85": "200",
    "86": "150.55",
    "87": "5.2M",
    "88": "150",
    "minTick": 0.01,
}

SAMPLE_POSITION = {
    "conid": 265598,
    "position": 100.0,
    "avgCost": 148.50,
}

SAMPLE_LEDGER = {
    "commoditymarketvalue": 0.0,
    "futuremarketvalue": 0.0,
    "settledcash": 50000.0,
    "exchangerate": 1.0,
    "sessionid": 123,
    "cashbalance": 50000.0,
    "corporatebondsmarketvalue": 0.0,
    "warrantsmarketvalue": 0.0,
    "netliquidationvalue": 100000.0,
    "interest": 0.5,
    "unrealizedpnl": 1500.0,
    "stockmarketvalue": 50000.0,
    "moneyfunds": 0.0,
    "currency": "USD",
    "realizedpnl": 500.0,
    "funds": 50000.0,
    "acctcode": "U1234567",
}

SAMPLE_ALERT_RESPONSE = {
    "account": "U1234567",
    "order_id": 999,
    "alert_name": "Price Alert",
    "alert_message": "AAPL hit target",
    "alert_active": 1,
    "alert_repeatable": 0,
    "alert_email": "user@example.com",
    "alert_send_message": 1,
    "tif": "GTC",
    "expire_time": "",
    "order_status": "Active",
    "outsideRth": 0,
    "itws_orders_only": 0,
    "alert_show_popup": 1,
    "alert_triggered": 0,
    "alert_play_audio": "bell.wav",
    "conditions": [
        {
            "type": 1,
            "conidex": "265598@SMART",
            "operator": ">=",
            "triggerMethod": "0",
            "value": "155",
            "logicBind": "n",
            "timeZone": "",
        }
    ],
}

SAMPLE_SCANNER_RESULT = {
    "total": 50,
    "size": 10,
    "offset": 0,
    "scanTime": "20231115-10:00:00",
    "id": 1.0,
    "position": "0",
    "Contracts": {
        "Contract": [
            {"inScanTime": "20231115", "distance": 0, "contractID": 265598},
            {"inScanTime": "20231115", "distance": 1, "contractID": 756733},
        ]
    },
}

SAMPLE_SUMMARY = {
    "amount": 100000.0,
    "currency": "USD",
    "isNull": False,
    "timestamp": 1700000000,
    "value": "100000.00",
}

SAMPLE_TRANSACTIONS = {
    "id": "getTransactions",
    "currency": "USD",
    "includesRealTime": True,
    "from": 1699900000.0,
    "to": 1700000000.0,
    "transactions": [
        {
            "acctid": "U1234567",
            "conid": 265598,
            "cur": "USD",
            "fxRate": 1.0,
            "desc": "Buy AAPL",
            "date": "20231115",
            "type": "Buy",
            "qty": 100,
            "pr": 150.0,
            "amt": -15000.0,
        }
    ],
}


# ---------------------------------------------------------------------------
# AuthStatus tests
# ---------------------------------------------------------------------------


class TestAuthStatus:
    """Tests for the AuthStatus model."""

    def test_from_dict_complete(self):
        """Verify all fields are populated from a complete dict."""
        status = AuthStatus.from_dict(SAMPLE_AUTH_STATUS)
        assert status.authenticated is True
        assert status.connected is True
        assert status.competing is False
        assert status.message == "All good"
        assert status.prompts == ["prompt1"]

    def test_from_dict_empty(self):
        """Verify defaults when dict is empty."""
        status = AuthStatus.from_dict({})
        assert status.authenticated is False
        assert status.connected is False
        assert status.prompts == []

    def test_frozen(self):
        """Verify the dataclass is frozen."""
        status = AuthStatus.from_dict(SAMPLE_AUTH_STATUS)
        with pytest.raises(AttributeError):
            status.authenticated = False  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Account tests
# ---------------------------------------------------------------------------


class TestAccount:
    """Tests for the Account model."""

    def test_from_dict_complete(self):
        """Verify all fields are populated from a complete dict."""
        account = Account.from_dict(SAMPLE_ACCOUNT)
        assert account.account_id == "U1234567"
        assert account.currency == "USD"
        assert account.type == "INDIVIDUAL"
        assert account.clearing_status == "O"
        assert account.desc == "U1234567 - Alias1"

    def test_from_dict_empty(self):
        """Verify defaults when dict is empty."""
        account = Account.from_dict({})
        assert account.account_id == ""
        assert account.currency == ""
        assert account.faclient is False

    def test_frozen(self):
        """Verify the dataclass is frozen."""
        account = Account.from_dict(SAMPLE_ACCOUNT)
        with pytest.raises(AttributeError):
            account.currency = "EUR"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Contract tests
# ---------------------------------------------------------------------------


class TestContract:
    """Tests for the Contract model."""

    def test_from_dict_complete(self):
        """Verify all fields are populated from a complete dict."""
        contract = Contract.from_dict(SAMPLE_CONTRACT)
        assert contract.con_id == "265598"
        assert contract.company_name == "Apple Inc"
        assert contract.exchange == "NASDAQ"
        assert contract.instrument_type == "STK"
        assert contract.r_t_h is True

    def test_company_name_fallback(self):
        """Verify company_name falls back to companyName key."""
        data = {"companyName": "Fallback Inc"}
        contract = Contract.from_dict(data)
        assert contract.company_name == "Fallback Inc"

    def test_from_dict_empty(self):
        """Verify defaults when dict is empty."""
        contract = Contract.from_dict({})
        assert contract.con_id == ""
        assert contract.company_name == ""


# ---------------------------------------------------------------------------
# SecdefInfo tests
# ---------------------------------------------------------------------------


class TestSecdefInfo:
    """Tests for the SecdefInfo model."""

    def test_from_dict_complete(self):
        """Verify all fields are populated from a complete dict."""
        secdef = SecdefInfo.from_dict(SAMPLE_SECDEF_INFO)
        assert secdef.conid == 265598
        assert secdef.symbol == "AAPL"
        assert secdef.sec_type == "STK"
        assert secdef.listing_exchange == "NASDAQ"
        assert secdef.valid_exchanges == "SMART,AMEX,NYSE"

    def test_from_dict_empty(self):
        """Verify defaults when dict is empty."""
        secdef = SecdefInfo.from_dict({})
        assert secdef.conid == 0
        assert secdef.symbol == ""


# ---------------------------------------------------------------------------
# Order tests
# ---------------------------------------------------------------------------


class TestOrder:
    """Tests for the Order model."""

    def test_from_dict_complete(self):
        """Verify all fields are populated from a complete dict."""
        order = Order.from_dict(SAMPLE_ORDER)
        assert order.acct == "U1234567"
        assert order.conid == 265598
        assert order.ticker == "AAPL"
        assert order.status == "Submitted"
        assert order.side == "BUY"
        assert order.price == 150.0
        assert order.order_id == 12345

    def test_from_dict_empty(self):
        """Verify defaults when dict is empty."""
        order = Order.from_dict({})
        assert order.conid == 0
        assert order.price == 0.0


# ---------------------------------------------------------------------------
# OrderStatus tests
# ---------------------------------------------------------------------------


class TestOrderStatus:
    """Tests for the OrderStatus model."""

    def test_from_dict_complete(self):
        """Verify all fields are populated from a complete dict."""
        status = OrderStatus.from_dict(SAMPLE_ORDER_STATUS)
        assert status.order_id == 12345
        assert status.symbol == "AAPL"
        assert status.order_status == "Submitted"
        assert status.use_price_mgmt_algo is True
        assert status.tif == "DAY"

    def test_from_dict_empty(self):
        """Verify defaults when dict is empty."""
        status = OrderStatus.from_dict({})
        assert status.order_id == 0
        assert status.order_not_editable is False


# ---------------------------------------------------------------------------
# OrderRequest tests
# ---------------------------------------------------------------------------


class TestOrderRequest:
    """Tests for the OrderRequest model."""

    def test_to_dict(self):
        """Verify to_dict produces correct API format."""
        req = OrderRequest(
            acct_id="U1234567",
            conid=265598,
            order_type="LMT",
            side="BUY",
            quantity=100,
            price=150.0,
            tif="DAY",
        )
        result = req.to_dict()
        assert result["acctId"] == "U1234567"
        assert result["conid"] == 265598
        assert result["orderType"] == "LMT"
        assert result["side"] == "BUY"
        assert result["quantity"] == 100
        assert result["price"] == 150.0

    def test_to_dict_omits_empty(self):
        """Verify to_dict omits fields that are empty/zero."""
        req = OrderRequest(conid=265598, order_type="MKT", side="BUY", quantity=10)
        result = req.to_dict()
        assert "acctId" not in result
        assert "ticker" not in result
        assert "price" not in result


# ---------------------------------------------------------------------------
# ModifyOrder tests
# ---------------------------------------------------------------------------


class TestModifyOrder:
    """Tests for the ModifyOrder model."""

    def test_to_dict(self):
        """Verify to_dict produces correct API format."""
        mod = ModifyOrder(
            acct_id="U1234567",
            conid=265598,
            order_type="LMT",
            price=155.0,
            side="BUY",
            quantity=50,
        )
        result = mod.to_dict()
        assert result["acctId"] == "U1234567"
        assert result["price"] == 155.0
        assert result["quantity"] == 50


# ---------------------------------------------------------------------------
# Trade tests
# ---------------------------------------------------------------------------


class TestTrade:
    """Tests for the Trade model."""

    def test_from_dict_complete(self):
        """Verify all fields are populated from a complete dict."""
        trade = Trade.from_dict(SAMPLE_TRADE)
        assert trade.execution_id == "exec123"
        assert trade.symbol == "AAPL"
        assert trade.commission == 1.0
        assert trade.net_amount == 15000.0
        assert trade.conid == "265598"

    def test_from_dict_empty(self):
        """Verify defaults when dict is empty."""
        trade = Trade.from_dict({})
        assert trade.execution_id == ""
        assert trade.commission == 0.0


# ---------------------------------------------------------------------------
# HistoryData / HistoryBar tests
# ---------------------------------------------------------------------------


class TestHistoryBar:
    """Tests for the HistoryBar model."""

    def test_from_dict(self):
        """Verify bar fields map correctly."""
        market_bar = HistoryBar.from_dict({"t": 1700000000, "o": 150.0, "c": 151.5, "h": 152.0, "l": 149.5, "v": 10000})
        assert market_bar.timestamp == 1700000000
        assert market_bar.open == 150.0
        assert market_bar.close == 151.5
        assert market_bar.high == 152.0
        assert market_bar.low == 149.5
        assert market_bar.volume == 10000


class TestHistoryData:
    """Tests for the HistoryData model."""

    def test_from_dict_complete(self):
        """Verify all fields including nested bars."""
        history = HistoryData.from_dict(SAMPLE_HISTORY_DATA)
        assert history.symbol == "AAPL"
        assert history.bar_length == 300
        assert history.points == 2
        assert len(history.data) == 2
        assert history.data[0].open == 150.0
        assert history.data[1].close == 152.0

    def test_from_dict_empty(self):
        """Verify defaults when dict is empty."""
        history = HistoryData.from_dict({})
        assert history.symbol == ""
        assert history.data == []


# ---------------------------------------------------------------------------
# MarketData tests
# ---------------------------------------------------------------------------


class TestMarketData:
    """Tests for the MarketData model."""

    def test_from_dict_complete(self):
        """Verify numeric field keys map to named properties."""
        md = MarketData.from_dict(SAMPLE_MARKET_DATA)
        assert md.conid == 265598
        assert md.last_price == "150.50"
        assert md.high == 152.0
        assert md.low == 149.0
        assert md.bid_price == "150.45"
        assert md.ask_price == "150.55"
        assert md.volume == "5.2M"
        assert md.min_tick == 0.01

    def test_from_dict_empty(self):
        """Verify defaults when dict is empty."""
        md = MarketData.from_dict({})
        assert md.conid == 0
        assert md.last_price == ""


# ---------------------------------------------------------------------------
# Position tests
# ---------------------------------------------------------------------------


class TestPosition:
    """Tests for the Position model."""

    def test_from_dict_complete(self):
        """Verify fields map correctly."""
        pos = Position.from_dict(SAMPLE_POSITION)
        assert pos.conid == 265598
        assert pos.position == 100.0
        assert pos.avg_cost == 148.50

    def test_from_dict_empty(self):
        """Verify defaults when dict is empty."""
        pos = Position.from_dict({})
        assert pos.conid == 0
        assert pos.position == 0.0


# ---------------------------------------------------------------------------
# Ledger tests
# ---------------------------------------------------------------------------


class TestLedger:
    """Tests for the Ledger model."""

    def test_from_dict_complete(self):
        """Verify all fields map correctly."""
        ledger = Ledger.from_dict(SAMPLE_LEDGER)
        assert ledger.settled_cash == 50000.0
        assert ledger.net_liquidation_value == 100000.0
        assert ledger.unrealized_pnl == 1500.0
        assert ledger.currency == "USD"
        assert ledger.acct_code == "U1234567"

    def test_from_dict_empty(self):
        """Verify defaults when dict is empty."""
        ledger = Ledger.from_dict({})
        assert ledger.settled_cash == 0.0
        assert ledger.currency == ""


# ---------------------------------------------------------------------------
# AlertResponse tests
# ---------------------------------------------------------------------------


class TestAlertResponse:
    """Tests for the AlertResponse model."""

    def test_from_dict_complete(self):
        """Verify all fields including nested conditions."""
        alert = AlertResponse.from_dict(SAMPLE_ALERT_RESPONSE)
        assert alert.account == "U1234567"
        assert alert.alert_name == "Price Alert"
        assert alert.tif == "GTC"
        assert len(alert.conditions) == 1
        assert alert.conditions[0].operator == ">="
        assert alert.conditions[0].value == "155"

    def test_from_dict_empty(self):
        """Verify defaults when dict is empty."""
        alert = AlertResponse.from_dict({})
        assert alert.conditions == []
        assert alert.alert_name == ""


# ---------------------------------------------------------------------------
# ScannerResult tests
# ---------------------------------------------------------------------------


class TestScannerResult:
    """Tests for the ScannerResult model."""

    def test_from_dict_complete(self):
        """Verify all fields including nested contracts."""
        result = ScannerResult.from_dict(SAMPLE_SCANNER_RESULT)
        assert result.total == 50
        assert result.size == 10
        assert len(result.contracts) == 2
        assert result.contracts[0].contract_id == 265598

    def test_from_dict_empty(self):
        """Verify defaults when dict is empty."""
        result = ScannerResult.from_dict({})
        assert result.contracts == []


# ---------------------------------------------------------------------------
# ScannerParams tests
# ---------------------------------------------------------------------------


class TestScannerParams:
    """Tests for the ScannerParams model."""

    def test_to_dict(self):
        """Verify to_dict produces correct API format."""
        params = ScannerParams(
            instrument="STK",
            type="MOST_ACTIVE_USD",
            location="STK.US.MAJOR",
            filter=[ScannerFilter(code="usdVolume", value=500)],
        )
        result = params.to_dict()
        assert result["instrument"] == "STK"
        assert result["type"] == "MOST_ACTIVE_USD"
        assert result["filter"] == [{"code": "usdVolume", "value": 500}]


# ---------------------------------------------------------------------------
# Summary tests
# ---------------------------------------------------------------------------


class TestSummary:
    """Tests for the Summary model."""

    def test_from_dict_complete(self):
        """Verify all fields map correctly."""
        summary = Summary.from_dict(SAMPLE_SUMMARY)
        assert summary.amount == 100000.0
        assert summary.currency == "USD"
        assert summary.is_null is False
        assert summary.timestamp == 1700000000

    def test_from_dict_empty(self):
        """Verify defaults when dict is empty."""
        summary = Summary.from_dict({})
        assert summary.amount == 0.0


# ---------------------------------------------------------------------------
# Transactions tests
# ---------------------------------------------------------------------------


class TestTransactions:
    """Tests for the Transactions model."""

    def test_from_dict_complete(self):
        """Verify all fields including nested transactions."""
        txns = Transactions.from_dict(SAMPLE_TRANSACTIONS)
        assert txns.id == "getTransactions"
        assert txns.includes_real_time is True
        assert len(txns.transactions) == 1
        assert txns.transactions[0].desc == "Buy AAPL"
        assert txns.transactions[0].qty == 100
        assert txns.transactions[0].amount == -15000.0

    def test_from_dict_empty(self):
        """Verify defaults when dict is empty."""
        txns = Transactions.from_dict({})
        assert txns.transactions == []


# ---------------------------------------------------------------------------
# SystemError tests
# ---------------------------------------------------------------------------


class TestIBSystemError:
    """Tests for the IBSystemError model."""

    def test_from_dict(self):
        """Verify error field maps correctly."""
        err = IBSystemError.from_dict({"error": "Something went wrong"})
        assert err.error == "Something went wrong"

    def test_from_dict_empty(self):
        """Verify defaults when dict is empty."""
        err = IBSystemError.from_dict({})
        assert err.error == ""

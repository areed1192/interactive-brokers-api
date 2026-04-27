"""Tests for the Contracts service."""


from unittest.mock import MagicMock

import pytest

from ibc.exceptions import IBCValidationError
from ibc.models import Contract, SecdefInfo
from ibc.rest.contract import Contracts

# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------

SAMPLE_CONTRACT_INFO = {
    "cfi_code": "",
    "symbol": "AAPL",
    "cusip": None,
    "expiry": None,
    "con_id": 265598,
    "company_name": "APPLE INC",
    "instrument_type": "STK",
}

SAMPLE_FUTURES = {
    "CL": [
        {"symbol": "CL", "conid": 174230005, "expiry": "20250120"}
    ]
}

SAMPLE_STOCKS = {
    "AAPL": [
        {"name": "APPLE INC", "conid": 265598, "assetClass": "STK"}
    ]
}

SAMPLE_SEARCH_RESULTS = [
    {"conid": 265598, "companyHeader": "APPLE INC - NASDAQ", "companyName": "APPLE INC"}
]

SAMPLE_SECDEF = [
    {"conid": 265598, "symbol": "AAPL", "secType": "STK"}
]

SAMPLE_SCHEDULE = {
    "id": "STK",
    "tradeVenueId": "NASDAQ",
    "schedules": [{"openingTime": "20250120-0930", "closingTime": "20250120-1600"}],
}

SAMPLE_STRIKES = {
    "call": ["140", "145", "150", "155", "160"],
    "put": ["140", "145", "150", "155", "160"],
}

SAMPLE_SECDEF_INFO = [
    {"conid": 500000001, "symbol": "AAPL", "secType": "OPT", "strike": "150", "right": "C"}
]

SAMPLE_ALGOS = [
    {"id": "algo1", "name": "Adaptive", "description": "Adaptive algorithm"}
]

SAMPLE_RULES = {
    "orderTypes": ["LMT", "MKT", "STP"],
    "tifTypes": ["DAY", "GTC"],
}

SAMPLE_INFO_AND_RULES = {
    "symbol": "AAPL",
    "conid": 265598,
    "rules": {"orderTypes": ["LMT", "MKT"]},
}

SAMPLE_CURRENCY_PAIRS = {
    "USD": [{"symbol": "EUR.USD", "conid": 12345}]
}


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def contracts_service(mock_session, mock_client):
    """Create a Contracts service with mocked session."""
    return Contracts(ib_client=mock_client, ib_session=mock_session)


# ---------------------------------------------------------------------------
# Contracts.contract_info tests
# ---------------------------------------------------------------------------


class TestContractInfo:
    """Tests for the Contracts.contract_info method."""

    def test_returns_contract_info(self, contracts_service, mock_session):
        """Verify contract_info() returns a Contract model."""
        mock_session.make_request = MagicMock(return_value=SAMPLE_CONTRACT_INFO)

        result = contracts_service.contract_info(contract_id='265598')

        assert isinstance(result, Contract)
        assert result.company_name == "APPLE INC"
        assert result.con_id == "265598"

    def test_calls_correct_endpoint(self, contracts_service, mock_session):
        """Verify contract_info() calls the correct API endpoint."""
        mock_session.make_request = MagicMock(return_value={})

        contracts_service.contract_info(contract_id='265598')

        mock_session.make_request.assert_called_once_with(
            method='get',
            endpoint='/api/iserver/contract/265598/info',
        )

    def test_validates_empty_contract_id(self, contracts_service):
        """Verify contract_info() raises IBCValidationError for empty ID."""
        with pytest.raises(IBCValidationError):
            contracts_service.contract_info(contract_id='')


# ---------------------------------------------------------------------------
# Contracts.search_futures tests
# ---------------------------------------------------------------------------


class TestSearchFutures:
    """Tests for the Contracts.search_futures method."""

    def test_returns_futures_response(self, contracts_service, mock_session):
        """Verify search_futures() returns the parsed JSON response."""
        mock_session.make_request = MagicMock(return_value=SAMPLE_FUTURES)

        result = contracts_service.search_futures(symbols=['CL'])

        assert result == SAMPLE_FUTURES

    def test_calls_correct_endpoint_with_params(self, contracts_service, mock_session):
        """Verify search_futures() passes symbols as comma-delimited params."""
        mock_session.make_request = MagicMock(return_value={})

        contracts_service.search_futures(symbols=['CL', 'ES'])

        mock_session.make_request.assert_called_once_with(
            method='get',
            endpoint='/api/trsrv/futures',
            params={'symbols': 'CL,ES'},
        )


# ---------------------------------------------------------------------------
# Contracts.search_stocks tests
# ---------------------------------------------------------------------------


class TestSearchStocks:
    """Tests for the Contracts.search_stocks method."""

    def test_returns_stocks_response(self, contracts_service, mock_session):
        """Verify search_stocks() returns the parsed JSON response."""
        mock_session.make_request = MagicMock(return_value=SAMPLE_STOCKS)

        result = contracts_service.search_stocks(symbols=['AAPL'])

        assert result == SAMPLE_STOCKS

    def test_calls_correct_endpoint_with_params(self, contracts_service, mock_session):
        """Verify search_stocks() passes symbols as comma-delimited params."""
        mock_session.make_request = MagicMock(return_value={})

        contracts_service.search_stocks(symbols=['AAPL', 'MSFT'])

        mock_session.make_request.assert_called_once_with(
            method='get',
            endpoint='/api/trsrv/stocks',
            params={'symbols': 'AAPL,MSFT'},
        )


# ---------------------------------------------------------------------------
# Contracts.search_symbol tests
# ---------------------------------------------------------------------------


class TestSearchSymbol:
    """Tests for the Contracts.search_symbol method."""

    def test_returns_search_results(self, contracts_service, mock_session):
        """Verify search_symbol() returns the parsed JSON response."""
        mock_session.make_request = MagicMock(return_value=SAMPLE_SEARCH_RESULTS)

        result = contracts_service.search_symbol(symbol='AAPL')

        assert result == SAMPLE_SEARCH_RESULTS

    def test_calls_correct_endpoint(self, contracts_service, mock_session):
        """Verify search_symbol() sends POST to secdef/search."""
        mock_session.make_request = MagicMock(return_value=[])

        contracts_service.search_symbol(symbol='AAPL', name=False, security_type='STK')

        mock_session.make_request.assert_called_once_with(
            method='post',
            endpoint='/api/iserver/secdef/search',
            json_payload={'symbol': 'AAPL', 'name': False, 'secType': 'STK'},
        )


# ---------------------------------------------------------------------------
# Contracts.trading_schedule tests
# ---------------------------------------------------------------------------


class TestTradingSchedule:
    """Tests for the Contracts.trading_schedule method."""

    def test_returns_schedule_response(self, contracts_service, mock_session):
        """Verify trading_schedule() returns the parsed JSON response."""
        mock_session.make_request = MagicMock(return_value=SAMPLE_SCHEDULE)

        result = contracts_service.trading_schedule(asset_class='STK', symbol='AAPL')

        assert result == SAMPLE_SCHEDULE

    def test_calls_correct_endpoint_with_params(self, contracts_service, mock_session):
        """Verify trading_schedule() passes all parameters."""
        mock_session.make_request = MagicMock(return_value={})

        contracts_service.trading_schedule(
            asset_class='STK', symbol='AAPL', exchange='NASDAQ'
        )

        mock_session.make_request.assert_called_once_with(
            method='get',
            endpoint='/api/trsrv/secdef/schedule',
            params={'assetClass': 'STK', 'symbol': 'AAPL', 'exchange': 'NASDAQ'},
        )


# ---------------------------------------------------------------------------
# Contracts.secdef_strikes tests
# ---------------------------------------------------------------------------


class TestSecdefStrikes:
    """Tests for the Contracts.secdef_strikes method."""

    def test_returns_strikes_response(self, contracts_service, mock_session):
        """Verify secdef_strikes() returns the parsed JSON response."""
        mock_session.make_request = MagicMock(return_value=SAMPLE_STRIKES)

        result = contracts_service.secdef_strikes(
            contract_id='265598', sectype='OPT', month='202501'
        )

        assert result == SAMPLE_STRIKES

    def test_calls_correct_endpoint(self, contracts_service, mock_session):
        """Verify secdef_strikes() passes all parameters."""
        mock_session.make_request = MagicMock(return_value={})

        contracts_service.secdef_strikes(
            contract_id='265598', sectype='OPT', month='202501', exchange='CBOE'
        )

        mock_session.make_request.assert_called_once_with(
            method='get',
            endpoint='/api/iserver/secdef/strikes',
            params={'conid': '265598', 'sectype': 'OPT', 'month': '202501', 'exchange': 'CBOE'},
        )

    def test_validates_empty_contract_id(self, contracts_service):
        """Verify secdef_strikes() raises IBCValidationError for empty ID."""
        with pytest.raises(IBCValidationError):
            contracts_service.secdef_strikes(contract_id='', sectype='OPT', month='202501')


# ---------------------------------------------------------------------------
# Contracts.secdef_info tests
# ---------------------------------------------------------------------------


class TestSecdefInfo:
    """Tests for the Contracts.secdef_info method."""

    def test_returns_secdef_info(self, contracts_service, mock_session):
        """Verify secdef_info() returns a list of SecdefInfo models."""
        mock_session.make_request = MagicMock(return_value=SAMPLE_SECDEF_INFO)

        result = contracts_service.secdef_info(contract_id='265598', sectype='OPT')

        assert len(result) == 1
        assert isinstance(result[0], SecdefInfo)
        assert result[0].conid == 500000001
        assert result[0].symbol == "AAPL"

    def test_calls_correct_endpoint_with_all_params(self, contracts_service, mock_session):
        """Verify secdef_info() passes all parameters."""
        mock_session.make_request = MagicMock(return_value=[])

        contracts_service.secdef_info(
            contract_id='265598', sectype='OPT', month='202501',
            exchange='CBOE', strike='150', right='C'
        )

        mock_session.make_request.assert_called_once_with(
            method='get',
            endpoint='/api/iserver/secdef/info',
            params={
                'conid': '265598', 'sectype': 'OPT', 'month': '202501',
                'exchange': 'CBOE', 'strike': '150', 'right': 'C',
            },
        )


# ---------------------------------------------------------------------------
# Contracts.contract_algos tests
# ---------------------------------------------------------------------------


class TestContractAlgos:
    """Tests for the Contracts.contract_algos method."""

    def test_returns_algos_response(self, contracts_service, mock_session):
        """Verify contract_algos() returns the parsed JSON response."""
        mock_session.make_request = MagicMock(return_value=SAMPLE_ALGOS)

        result = contracts_service.contract_algos(contract_id='265598')

        assert result == SAMPLE_ALGOS

    def test_calls_correct_endpoint(self, contracts_service, mock_session):
        """Verify contract_algos() calls the correct endpoint."""
        mock_session.make_request = MagicMock(return_value=[])

        contracts_service.contract_algos(contract_id='265598')

        mock_session.make_request.assert_called_once_with(
            method='get',
            endpoint='/api/iserver/contract/265598/algos',
            params={'algos': None, 'addDescription': None, 'addParams': None},
        )

    def test_validates_empty_contract_id(self, contracts_service):
        """Verify contract_algos() raises IBCValidationError for empty ID."""
        with pytest.raises(IBCValidationError):
            contracts_service.contract_algos(contract_id='')


# ---------------------------------------------------------------------------
# Contracts.contract_rules tests
# ---------------------------------------------------------------------------


class TestContractRules:
    """Tests for the Contracts.contract_rules method."""

    def test_returns_rules_response(self, contracts_service, mock_session):
        """Verify contract_rules() returns the parsed JSON response."""
        mock_session.make_request = MagicMock(return_value=SAMPLE_RULES)

        result = contracts_service.contract_rules(contract_id='265598')

        assert result == SAMPLE_RULES

    def test_calls_correct_endpoint(self, contracts_service, mock_session):
        """Verify contract_rules() sends POST with payload."""
        mock_session.make_request = MagicMock(return_value={})

        contracts_service.contract_rules(contract_id='265598', is_buy=False)

        mock_session.make_request.assert_called_once_with(
            method='post',
            endpoint='/api/iserver/contract/rules',
            json_payload={'conid': 265598, 'isBuy': False},
        )

    def test_validates_empty_contract_id(self, contracts_service):
        """Verify contract_rules() raises IBCValidationError for empty ID."""
        with pytest.raises(IBCValidationError):
            contracts_service.contract_rules(contract_id='')


# ---------------------------------------------------------------------------
# Contracts.contract_info_and_rules tests
# ---------------------------------------------------------------------------


class TestContractInfoAndRules:
    """Tests for the Contracts.contract_info_and_rules method."""

    def test_returns_combined_response(self, contracts_service, mock_session):
        """Verify contract_info_and_rules() returns the parsed JSON response."""
        mock_session.make_request = MagicMock(return_value=SAMPLE_INFO_AND_RULES)

        result = contracts_service.contract_info_and_rules(contract_id='265598')

        assert result == SAMPLE_INFO_AND_RULES

    def test_calls_correct_endpoint(self, contracts_service, mock_session):
        """Verify contract_info_and_rules() calls the correct endpoint."""
        mock_session.make_request = MagicMock(return_value={})

        contracts_service.contract_info_and_rules(contract_id='265598', is_buy=True)

        mock_session.make_request.assert_called_once_with(
            method='get',
            endpoint='/api/iserver/contract/265598/info-and-rules',
            params={'isBuy': True},
        )


# ---------------------------------------------------------------------------
# Contracts.currency_pairs tests
# ---------------------------------------------------------------------------


class TestCurrencyPairs:
    """Tests for the Contracts.currency_pairs method."""

    def test_returns_currency_pairs(self, contracts_service, mock_session):
        """Verify currency_pairs() returns the parsed JSON response."""
        mock_session.make_request = MagicMock(return_value=SAMPLE_CURRENCY_PAIRS)

        result = contracts_service.currency_pairs(currency='USD')

        assert result == SAMPLE_CURRENCY_PAIRS

    def test_calls_correct_endpoint(self, contracts_service, mock_session):
        """Verify currency_pairs() calls the correct endpoint."""
        mock_session.make_request = MagicMock(return_value={})

        contracts_service.currency_pairs(currency='USD')

        mock_session.make_request.assert_called_once_with(
            method='get',
            endpoint='/api/iserver/currency/pairs',
            params={'currency': 'USD'},
        )


# ---------------------------------------------------------------------------
# Contracts.search_multiple_contracts tests
# ---------------------------------------------------------------------------


class TestSearchMultipleContracts:
    """Tests for the Contracts.search_multiple_contracts method."""

    def test_returns_contracts_response(self, contracts_service, mock_session):
        """Verify search_multiple_contracts() returns the parsed JSON response."""
        mock_session.make_request = MagicMock(return_value=SAMPLE_SECDEF)

        result = contracts_service.search_multiple_contracts(contract_ids=[265598])

        assert result == SAMPLE_SECDEF

    def test_calls_correct_endpoint(self, contracts_service, mock_session):
        """Verify search_multiple_contracts() sends POST with conids."""
        mock_session.make_request = MagicMock(return_value=[])

        contracts_service.search_multiple_contracts(contract_ids=[265598])

        mock_session.make_request.assert_called_once_with(
            method='post',
            endpoint='/api/trsrv/secdef',
            json_payload={'conids': [265598]},
        )

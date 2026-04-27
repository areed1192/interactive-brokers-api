"""Tests for the Scanners service."""

# pylint: disable=redefined-outer-name

from unittest.mock import MagicMock

import pytest

from ibc.exceptions import IBCValidationError
from ibc.models import ScannerResult
from ibc.rest.scanner import Scanners


# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------

SAMPLE_SCANNER_PARAMS = {
    "scan_type_list": [{"name": "TOP_PERC_GAIN", "display_name": "Top % Gainers"}],
    "instrument_list": [{"type": "STK", "display_name": "US Stocks"}],
    "filter_list": [{"code": "priceAbove", "display_name": "Price Above"}],
    "location_tree": [{"display_name": "US", "type": "STK.US"}],
}

SAMPLE_SCANNER_RESULT = {
    "contracts": [
        {"conid": 265598, "symbol": "AAPL", "company_name": "Apple Inc"},
        {"conid": 272093, "symbol": "MSFT", "company_name": "Microsoft Corp"},
    ],
    "total": 2,
}

SAMPLE_SCANNER_PAYLOAD = {
    "instrument": "STK",
    "type": "NOT_YET_TRADED_TODAY",
    "filter": [
        {"code": "priceAbove", "value": 50},
        {"code": "priceBelow", "value": 70},
    ],
    "location": "STK.US.MAJOR",
    "size": "25",
}


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def scanners_service(mock_session, mock_client):
    """Create a Scanners service with mocked session."""
    return Scanners(ib_client=mock_client, ib_session=mock_session)


# ---------------------------------------------------------------------------
# Scanners.scanners tests
# ---------------------------------------------------------------------------


class TestScanners:
    """Tests for the Scanners.scanners method."""

    def test_returns_scanner_params(self, scanners_service, mock_session):
        """Verify scanners() returns the scanner parameters."""
        mock_session.make_request = MagicMock(return_value=SAMPLE_SCANNER_PARAMS)

        result = scanners_service.scanners()

        assert result == SAMPLE_SCANNER_PARAMS

    def test_calls_correct_endpoint(self, scanners_service, mock_session):
        """Verify scanners() calls the correct API endpoint."""
        mock_session.make_request = MagicMock(return_value={})

        scanners_service.scanners()

        mock_session.make_request.assert_called_once_with(
            method="get",
            endpoint="/api/iserver/scanner/params",
        )


# ---------------------------------------------------------------------------
# Scanners.run_scanner tests
# ---------------------------------------------------------------------------


class TestRunScanner:
    """Tests for the Scanners.run_scanner method."""

    def test_returns_scanner_result_model(self, scanners_service, mock_session):
        """Verify run_scanner() returns a ScannerResult model."""
        mock_session.make_request = MagicMock(return_value=SAMPLE_SCANNER_RESULT)

        result = scanners_service.run_scanner(scanner=SAMPLE_SCANNER_PAYLOAD)

        assert isinstance(result, ScannerResult)

    def test_calls_correct_endpoint(self, scanners_service, mock_session):
        """Verify run_scanner() calls the correct API endpoint."""
        mock_session.make_request = MagicMock(return_value=SAMPLE_SCANNER_RESULT)

        scanners_service.run_scanner(scanner=SAMPLE_SCANNER_PAYLOAD)

        mock_session.make_request.assert_called_once_with(
            method="post",
            endpoint="/api/iserver/scanner/run",
            json_payload=SAMPLE_SCANNER_PAYLOAD,
        )

    def test_validates_empty_scanner(self, scanners_service):
        """Verify run_scanner() raises IBCValidationError for empty dict."""
        with pytest.raises(IBCValidationError):
            scanners_service.run_scanner(scanner={})

    def test_validates_none_scanner(self, scanners_service):
        """Verify run_scanner() raises IBCValidationError for None."""
        with pytest.raises(IBCValidationError):
            scanners_service.run_scanner(scanner=None)

    def test_validates_non_dict_scanner(self, scanners_service):
        """Verify run_scanner() raises IBCValidationError for non-dict."""
        with pytest.raises(IBCValidationError):
            scanners_service.run_scanner(scanner="not a dict")

    def test_repr(self, scanners_service):
        """Verify the service repr."""
        assert repr(scanners_service) == "Scanners()"

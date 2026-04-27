"""Tests for the Data service."""


from unittest.mock import MagicMock

import pytest

from ibc.exceptions import IBCValidationError
from ibc.rest.data import Data

# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------

SAMPLE_PORTFOLIO_NEWS = [
    {"id": "news1", "headline": "Market Update", "source": "Reuters"}
]

SAMPLE_TOP_NEWS = [
    {"id": "news2", "headline": "Top Story", "source": "Bloomberg"}
]

SAMPLE_SOURCES = [
    {"id": "src1", "name": "Reuters"},
    {"id": "src2", "name": "Bloomberg"},
]

SAMPLE_BRIEFINGS = [
    {"id": "brief1", "title": "Morning Briefing"}
]

SAMPLE_SUMMARY = {
    "contractId": "265598",
    "company_name": "Apple Inc",
    "description": "Apple designs and manufactures consumer electronics.",
}

CONTRACT_ID = "265598"


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def data_service(mock_session, mock_client):
    """Create a Data service with mocked session."""
    return Data(ib_client=mock_client, ib_session=mock_session)


# ---------------------------------------------------------------------------
# Data.portfolio_news tests
# ---------------------------------------------------------------------------


class TestPortfolioNews:
    """Tests for the Data.portfolio_news method."""

    def test_returns_news(self, data_service, mock_session):
        """Verify portfolio_news() returns the response."""
        mock_session.make_request = MagicMock(return_value=SAMPLE_PORTFOLIO_NEWS)

        result = data_service.portfolio_news()

        assert result == SAMPLE_PORTFOLIO_NEWS

    def test_calls_correct_endpoint(self, data_service, mock_session):
        """Verify portfolio_news() calls the correct API endpoint."""
        mock_session.make_request = MagicMock(return_value=[])

        data_service.portfolio_news()

        mock_session.make_request.assert_called_once_with(
            method="get",
            endpoint="/api/iserver/news/portfolio",
        )


# ---------------------------------------------------------------------------
# Data.top_news tests
# ---------------------------------------------------------------------------


class TestTopNews:
    """Tests for the Data.top_news method."""

    def test_returns_news(self, data_service, mock_session):
        """Verify top_news() returns the response."""
        mock_session.make_request = MagicMock(return_value=SAMPLE_TOP_NEWS)

        result = data_service.top_news()

        assert result == SAMPLE_TOP_NEWS

    def test_calls_correct_endpoint(self, data_service, mock_session):
        """Verify top_news() calls the correct API endpoint."""
        mock_session.make_request = MagicMock(return_value=[])

        data_service.top_news()

        mock_session.make_request.assert_called_once_with(
            method="get",
            endpoint="/api/iserver/news/top",
        )


# ---------------------------------------------------------------------------
# Data.news_sources tests
# ---------------------------------------------------------------------------


class TestNewsSources:
    """Tests for the Data.news_sources method."""

    def test_returns_sources(self, data_service, mock_session):
        """Verify news_sources() returns the response."""
        mock_session.make_request = MagicMock(return_value=SAMPLE_SOURCES)

        result = data_service.news_sources()

        assert result == SAMPLE_SOURCES

    def test_calls_correct_endpoint(self, data_service, mock_session):
        """Verify news_sources() calls the correct API endpoint."""
        mock_session.make_request = MagicMock(return_value=[])

        data_service.news_sources()

        mock_session.make_request.assert_called_once_with(
            method="get",
            endpoint="/api/iserver/news/sources",
        )


# ---------------------------------------------------------------------------
# Data.news_briefings tests
# ---------------------------------------------------------------------------


class TestNewsBriefings:
    """Tests for the Data.news_briefings method."""

    def test_returns_briefings(self, data_service, mock_session):
        """Verify news_briefings() returns the response."""
        mock_session.make_request = MagicMock(return_value=SAMPLE_BRIEFINGS)

        result = data_service.news_briefings()

        assert result == SAMPLE_BRIEFINGS

    def test_calls_correct_endpoint(self, data_service, mock_session):
        """Verify news_briefings() calls the correct API endpoint."""
        mock_session.make_request = MagicMock(return_value=[])

        data_service.news_briefings()

        mock_session.make_request.assert_called_once_with(
            method="get",
            endpoint="/api/iserver/news/briefing",
        )


# ---------------------------------------------------------------------------
# Data.summary tests
# ---------------------------------------------------------------------------


class TestSummary:
    """Tests for the Data.summary method."""

    def test_returns_summary(self, data_service, mock_session):
        """Verify summary() returns the response."""
        mock_session.make_request = MagicMock(return_value=SAMPLE_SUMMARY)

        result = data_service.summary(contract_id=CONTRACT_ID)

        assert result == SAMPLE_SUMMARY

    def test_calls_correct_endpoint(self, data_service, mock_session):
        """Verify summary() calls the correct API endpoint."""
        mock_session.make_request = MagicMock(return_value={})

        data_service.summary(contract_id=CONTRACT_ID)

        mock_session.make_request.assert_called_once_with(
            method="get",
            endpoint=f"/api/iserver/fundamentals/{CONTRACT_ID}/summary",
        )

    def test_validates_empty_contract_id(self, data_service):
        """Verify summary() raises IBCValidationError for empty ID."""
        with pytest.raises(IBCValidationError):
            data_service.summary(contract_id="")

    def test_validates_none_contract_id(self, data_service):
        """Verify summary() raises IBCValidationError for None ID."""
        with pytest.raises(IBCValidationError):
            data_service.summary(contract_id=None)

    def test_validates_whitespace_contract_id(self, data_service):
        """Verify summary() raises IBCValidationError for whitespace-only ID."""
        with pytest.raises(IBCValidationError):
            data_service.summary(contract_id="   ")

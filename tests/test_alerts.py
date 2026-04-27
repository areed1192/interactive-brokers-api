"""Tests for the Alerts service."""


from unittest.mock import MagicMock

import pytest

from ibc.exceptions import IBCValidationError
from ibc.models import AlertResponse
from ibc.rest.alert import Alerts


# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------

SAMPLE_ALERTS = [
    {
        "order_id": 12345,
        "alert_name": "Price Alert",
        "alert_active": 1,
        "account": "U1234567",
    }
]

SAMPLE_MTA = [{"order_id": 99999, "alert_name": "MTA", "alert_active": 1}]

SAMPLE_CREATE_RESPONSE = {
    "request_id": 1,
    "order_id": 12345,
    "success": True,
}

SAMPLE_ACTIVATE_RESPONSE = {
    "request_id": 1,
    "order_id": 12345,
    "success": True,
}

SAMPLE_DELETE_RESPONSE = {
    "request_id": 1,
    "order_id": 12345,
    "success": True,
}

SAMPLE_ALERT_DETAILS = {
    "order_id": 12345,
    "alert_name": "Price Alert",
    "conditions": [{"type": 1, "conidex": "265598", "operator": ">=", "value": "150"}],
}

SAMPLE_ALERT_PAYLOAD = {
    "alertName": "Price Alert",
    "alertMessage": "AAPL crossed 150",
    "conditions": [
        {
            "type": 1,
            "conidex": "265598",
            "operator": ">=",
            "triggerMethod": "0",
            "value": "150",
        }
    ],
}

ACCOUNT_ID = "U1234567"
ALERT_ID = "12345"


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def alerts_service(mock_session, mock_client):
    """Create an Alerts service with mocked session."""
    return Alerts(ib_client=mock_client, ib_session=mock_session)


# ---------------------------------------------------------------------------
# Alerts.available_alerts tests
# ---------------------------------------------------------------------------


class TestAvailableAlerts:
    """Tests for the Alerts.available_alerts method."""

    def test_returns_alerts_response(self, alerts_service, mock_session):
        """Verify available_alerts() returns a list of AlertResponse models."""
        mock_session.make_request = MagicMock(return_value=SAMPLE_ALERTS)

        result = alerts_service.available_alerts(account_id=ACCOUNT_ID)

        assert len(result) == 1
        assert isinstance(result[0], AlertResponse)
        assert result[0].order_id == 12345
        assert result[0].alert_name == "Price Alert"

    def test_calls_correct_endpoint(self, alerts_service, mock_session):
        """Verify available_alerts() calls the correct API endpoint."""
        mock_session.make_request = MagicMock(return_value=[])

        alerts_service.available_alerts(account_id=ACCOUNT_ID)

        mock_session.make_request.assert_called_once_with(
            method="get",
            endpoint=f"/api/iserver/account/{ACCOUNT_ID}/alerts",
        )

    def test_validates_empty_account_id(self, alerts_service):
        """Verify available_alerts() raises IBCValidationError for empty ID."""
        with pytest.raises(IBCValidationError):
            alerts_service.available_alerts(account_id="")


# ---------------------------------------------------------------------------
# Alerts.mta_alerts tests
# ---------------------------------------------------------------------------


class TestMtaAlerts:
    """Tests for the Alerts.mta_alerts method."""

    def test_returns_mta_response(self, alerts_service, mock_session):
        """Verify mta_alerts() returns the parsed JSON response."""
        mock_session.make_request = MagicMock(return_value=SAMPLE_MTA)

        result = alerts_service.mta_alerts()

        assert result == SAMPLE_MTA

    def test_calls_correct_endpoint(self, alerts_service, mock_session):
        """Verify mta_alerts() calls the correct API endpoint."""
        mock_session.make_request = MagicMock(return_value=[])

        alerts_service.mta_alerts()

        mock_session.make_request.assert_called_once_with(
            method="get",
            endpoint="/api/iserver/account/mta",
        )


# ---------------------------------------------------------------------------
# Alerts.create_or_modify_alert tests
# ---------------------------------------------------------------------------


class TestCreateOrModifyAlert:
    """Tests for the Alerts.create_or_modify_alert method."""

    def test_returns_create_response(self, alerts_service, mock_session):
        """Verify create_or_modify_alert() returns the parsed JSON response."""
        mock_session.make_request = MagicMock(return_value=SAMPLE_CREATE_RESPONSE)

        result = alerts_service.create_or_modify_alert(
            account_id=ACCOUNT_ID, alert=SAMPLE_ALERT_PAYLOAD
        )

        assert result == SAMPLE_CREATE_RESPONSE

    def test_calls_correct_endpoint(self, alerts_service, mock_session):
        """Verify create_or_modify_alert() POSTs to the correct endpoint."""
        mock_session.make_request = MagicMock(return_value={})

        alerts_service.create_or_modify_alert(
            account_id=ACCOUNT_ID, alert=SAMPLE_ALERT_PAYLOAD
        )

        mock_session.make_request.assert_called_once_with(
            method="post",
            endpoint=f"/api/iserver/account/{ACCOUNT_ID}/alert",
            json_payload=SAMPLE_ALERT_PAYLOAD,
        )

    def test_validates_empty_account_id(self, alerts_service):
        """Verify create_or_modify_alert() raises IBCValidationError for empty ID."""
        with pytest.raises(IBCValidationError):
            alerts_service.create_or_modify_alert(account_id="", alert={})


# ---------------------------------------------------------------------------
# Alerts.activate_alert tests
# ---------------------------------------------------------------------------


class TestActivateAlert:
    """Tests for the Alerts.activate_alert method."""

    def test_returns_activation_response(self, alerts_service, mock_session):
        """Verify activate_alert() returns the parsed JSON response."""
        mock_session.make_request = MagicMock(return_value=SAMPLE_ACTIVATE_RESPONSE)

        result = alerts_service.activate_alert(
            account_id=ACCOUNT_ID, alert_id=ALERT_ID, activate=True
        )

        assert result == SAMPLE_ACTIVATE_RESPONSE

    def test_calls_correct_endpoint(self, alerts_service, mock_session):
        """Verify activate_alert() POSTs with correct payload."""
        mock_session.make_request = MagicMock(return_value={})

        alerts_service.activate_alert(
            account_id=ACCOUNT_ID, alert_id=ALERT_ID, activate=False
        )

        mock_session.make_request.assert_called_once_with(
            method="post",
            endpoint=f"/api/iserver/account/{ACCOUNT_ID}/alert/activate",
            json_payload={"alertId": 12345, "alertActive": 0},
        )

    def test_validates_empty_account_id(self, alerts_service):
        """Verify activate_alert() raises IBCValidationError for empty account_id."""
        with pytest.raises(IBCValidationError):
            alerts_service.activate_alert(account_id="", alert_id=ALERT_ID)

    def test_validates_empty_alert_id(self, alerts_service):
        """Verify activate_alert() raises IBCValidationError for empty alert_id."""
        with pytest.raises(IBCValidationError):
            alerts_service.activate_alert(account_id=ACCOUNT_ID, alert_id="")


# ---------------------------------------------------------------------------
# Alerts.delete_alert tests
# ---------------------------------------------------------------------------


class TestDeleteAlert:
    """Tests for the Alerts.delete_alert method."""

    def test_returns_delete_response(self, alerts_service, mock_session):
        """Verify delete_alert() returns the parsed JSON response."""
        mock_session.make_request = MagicMock(return_value=SAMPLE_DELETE_RESPONSE)

        result = alerts_service.delete_alert(account_id=ACCOUNT_ID, alert_id=ALERT_ID)

        assert result == SAMPLE_DELETE_RESPONSE

    def test_calls_correct_endpoint(self, alerts_service, mock_session):
        """Verify delete_alert() DELETEs the correct endpoint."""
        mock_session.make_request = MagicMock(return_value={})

        alerts_service.delete_alert(account_id=ACCOUNT_ID, alert_id=ALERT_ID)

        mock_session.make_request.assert_called_once_with(
            method="delete",
            endpoint=f"/api/iserver/account/{ACCOUNT_ID}/alert/{ALERT_ID}",
        )

    def test_validates_empty_alert_id(self, alerts_service):
        """Verify delete_alert() raises IBCValidationError for empty alert_id."""
        with pytest.raises(IBCValidationError):
            alerts_service.delete_alert(account_id=ACCOUNT_ID, alert_id="")


# ---------------------------------------------------------------------------
# Alerts.alert_details tests
# ---------------------------------------------------------------------------


class TestAlertDetails:
    """Tests for the Alerts.alert_details method."""

    def test_returns_alert_details(self, alerts_service, mock_session):
        """Verify alert_details() returns an AlertResponse model."""
        mock_session.make_request = MagicMock(return_value=SAMPLE_ALERT_DETAILS)

        result = alerts_service.alert_details(alert_id=ALERT_ID)

        assert isinstance(result, AlertResponse)
        assert result.order_id == 12345
        assert result.alert_name == "Price Alert"
        assert len(result.conditions) == 1

    def test_calls_correct_endpoint(self, alerts_service, mock_session):
        """Verify alert_details() GETs the correct endpoint."""
        mock_session.make_request = MagicMock(return_value={})

        alerts_service.alert_details(alert_id=ALERT_ID)

        mock_session.make_request.assert_called_once_with(
            method="get",
            endpoint=f"/api/iserver/account/alert/{ALERT_ID}",
        )

    def test_validates_empty_alert_id(self, alerts_service):
        """Verify alert_details() raises IBCValidationError for empty alert_id."""
        with pytest.raises(IBCValidationError):
            alerts_service.alert_details(alert_id="")

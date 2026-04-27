"""Tests for the FYI notifications service."""

# pylint: disable=redefined-outer-name

from unittest.mock import MagicMock

import pytest

from ibc.exceptions import IBCValidationError
from ibc.rest.fyi import FYI


# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------

SAMPLE_UNREAD = {"BN": 3}

SAMPLE_SETTINGS = [
    {"A": "System Notifications", "FC": "A", "H": 1},
    {"A": "Trading Notifications", "FC": "M", "H": 0},
]

SAMPLE_DISCLAIMER = {"FC": "A", "DT": "Disclaimer text here"}

SAMPLE_DELIVERY_OPTIONS = {
    "E": [{"A": "user@example.com", "I": "email-1", "UI": 1}],
    "M": [],
}

SAMPLE_NOTIFICATIONS = [
    {"id": "123456", "FC": "A", "MD": "System message", "R": 0}
]

SAMPLE_TOGGLE_RESPONSE = {"V": [1]}


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def fyi_service(mock_session, mock_client):
    """Create a FYI service with mocked session."""
    return FYI(ib_client=mock_client, ib_session=mock_session)


# ---------------------------------------------------------------------------
# FYI.unread_number tests
# ---------------------------------------------------------------------------


class TestUnreadNumber:
    """Tests for the FYI.unread_number method."""

    def test_returns_unread_count(self, fyi_service, mock_session):
        """Verify unread_number() returns the parsed JSON response."""
        mock_session.make_request = MagicMock(return_value=SAMPLE_UNREAD)

        result = fyi_service.unread_number()

        assert result == SAMPLE_UNREAD

    def test_calls_correct_endpoint(self, fyi_service, mock_session):
        """Verify unread_number() calls the correct API endpoint."""
        mock_session.make_request = MagicMock(return_value={})

        fyi_service.unread_number()

        mock_session.make_request.assert_called_once_with(
            method='get',
            endpoint='/api/fyi/unreadnumber',
        )


# ---------------------------------------------------------------------------
# FYI.settings tests
# ---------------------------------------------------------------------------


class TestSettings:
    """Tests for the FYI.settings method."""

    def test_returns_settings(self, fyi_service, mock_session):
        """Verify settings() returns the parsed JSON response."""
        mock_session.make_request = MagicMock(return_value=SAMPLE_SETTINGS)

        result = fyi_service.settings()

        assert result == SAMPLE_SETTINGS

    def test_calls_correct_endpoint(self, fyi_service, mock_session):
        """Verify settings() calls the correct API endpoint."""
        mock_session.make_request = MagicMock(return_value=[])

        fyi_service.settings()

        mock_session.make_request.assert_called_once_with(
            method='get',
            endpoint='/api/fyi/settings',
        )


# ---------------------------------------------------------------------------
# FYI.toggle_setting tests
# ---------------------------------------------------------------------------


class TestToggleSetting:
    """Tests for the FYI.toggle_setting method."""

    def test_returns_toggle_response(self, fyi_service, mock_session):
        """Verify toggle_setting() returns the parsed JSON response."""
        mock_session.make_request = MagicMock(return_value=SAMPLE_TOGGLE_RESPONSE)

        result = fyi_service.toggle_setting(typecode='A', enabled=True)

        assert result == SAMPLE_TOGGLE_RESPONSE

    def test_calls_correct_endpoint(self, fyi_service, mock_session):
        """Verify toggle_setting() POSTs to the correct endpoint."""
        mock_session.make_request = MagicMock(return_value={})

        fyi_service.toggle_setting(typecode='A', enabled=False)

        mock_session.make_request.assert_called_once_with(
            method='post',
            endpoint='/api/fyi/settings/A',
            json_payload={'enabled': False},
        )

    def test_validates_empty_typecode(self, fyi_service):
        """Verify toggle_setting() raises IBCValidationError for empty typecode."""
        with pytest.raises(IBCValidationError):
            fyi_service.toggle_setting(typecode='')


# ---------------------------------------------------------------------------
# FYI.disclaimer tests
# ---------------------------------------------------------------------------


class TestDisclaimer:
    """Tests for the FYI.disclaimer method."""

    def test_returns_disclaimer(self, fyi_service, mock_session):
        """Verify disclaimer() returns the parsed JSON response."""
        mock_session.make_request = MagicMock(return_value=SAMPLE_DISCLAIMER)

        result = fyi_service.disclaimer(typecode='A')

        assert result == SAMPLE_DISCLAIMER

    def test_calls_correct_endpoint(self, fyi_service, mock_session):
        """Verify disclaimer() GETs the correct endpoint."""
        mock_session.make_request = MagicMock(return_value={})

        fyi_service.disclaimer(typecode='A')

        mock_session.make_request.assert_called_once_with(
            method='get',
            endpoint='/api/fyi/disclaimer/A',
        )


# ---------------------------------------------------------------------------
# FYI.accept_disclaimer tests
# ---------------------------------------------------------------------------


class TestAcceptDisclaimer:
    """Tests for the FYI.accept_disclaimer method."""

    def test_calls_correct_endpoint(self, fyi_service, mock_session):
        """Verify accept_disclaimer() PUTs to the correct endpoint."""
        mock_session.make_request = MagicMock(return_value={})

        fyi_service.accept_disclaimer(typecode='A')

        mock_session.make_request.assert_called_once_with(
            method='put',
            endpoint='/api/fyi/disclaimer/A',
        )


# ---------------------------------------------------------------------------
# FYI.delivery_options tests
# ---------------------------------------------------------------------------


class TestDeliveryOptions:
    """Tests for the FYI.delivery_options method."""

    def test_returns_delivery_options(self, fyi_service, mock_session):
        """Verify delivery_options() returns the parsed JSON response."""
        mock_session.make_request = MagicMock(return_value=SAMPLE_DELIVERY_OPTIONS)

        result = fyi_service.delivery_options()

        assert result == SAMPLE_DELIVERY_OPTIONS

    def test_calls_correct_endpoint(self, fyi_service, mock_session):
        """Verify delivery_options() GETs the correct endpoint."""
        mock_session.make_request = MagicMock(return_value={})

        fyi_service.delivery_options()

        mock_session.make_request.assert_called_once_with(
            method='get',
            endpoint='/api/fyi/deliveryoptions',
        )


# ---------------------------------------------------------------------------
# FYI.toggle_email_delivery tests
# ---------------------------------------------------------------------------


class TestToggleEmailDelivery:
    """Tests for the FYI.toggle_email_delivery method."""

    def test_calls_correct_endpoint(self, fyi_service, mock_session):
        """Verify toggle_email_delivery() PUTs with correct payload."""
        mock_session.make_request = MagicMock(return_value={})

        fyi_service.toggle_email_delivery(enabled=True)

        mock_session.make_request.assert_called_once_with(
            method='put',
            endpoint='/api/fyi/deliveryoptions/email',
            json_payload={'enabled': True},
        )


# ---------------------------------------------------------------------------
# FYI.toggle_device_delivery tests
# ---------------------------------------------------------------------------


class TestToggleDeviceDelivery:
    """Tests for the FYI.toggle_device_delivery method."""

    def test_calls_correct_endpoint(self, fyi_service, mock_session):
        """Verify toggle_device_delivery() POSTs with correct payload."""
        mock_session.make_request = MagicMock(return_value={})

        fyi_service.toggle_device_delivery(device_id='dev-1', enabled=True)

        mock_session.make_request.assert_called_once_with(
            method='post',
            endpoint='/api/fyi/deliveryoptions/device',
            json_payload={'deviceId': 'dev-1', 'enabled': True},
        )

    def test_validates_empty_device_id(self, fyi_service):
        """Verify toggle_device_delivery() raises IBCValidationError for empty ID."""
        with pytest.raises(IBCValidationError):
            fyi_service.toggle_device_delivery(device_id='', enabled=True)


# ---------------------------------------------------------------------------
# FYI.delete_device tests
# ---------------------------------------------------------------------------


class TestDeleteDevice:
    """Tests for the FYI.delete_device method."""

    def test_calls_correct_endpoint(self, fyi_service, mock_session):
        """Verify delete_device() DELETEs the correct endpoint."""
        mock_session.make_request = MagicMock(return_value={})

        fyi_service.delete_device(device_id='dev-1')

        mock_session.make_request.assert_called_once_with(
            method='delete',
            endpoint='/api/fyi/deliveryoptions/dev-1',
        )

    def test_validates_empty_device_id(self, fyi_service):
        """Verify delete_device() raises IBCValidationError for empty ID."""
        with pytest.raises(IBCValidationError):
            fyi_service.delete_device(device_id='')


# ---------------------------------------------------------------------------
# FYI.notifications tests
# ---------------------------------------------------------------------------


class TestNotifications:
    """Tests for the FYI.notifications method."""

    def test_returns_notifications(self, fyi_service, mock_session):
        """Verify notifications() returns the parsed JSON response."""
        mock_session.make_request = MagicMock(return_value=SAMPLE_NOTIFICATIONS)

        result = fyi_service.notifications()

        assert result == SAMPLE_NOTIFICATIONS

    def test_calls_correct_endpoint_with_params(self, fyi_service, mock_session):
        """Verify notifications() passes parameters correctly."""
        mock_session.make_request = MagicMock(return_value=[])

        fyi_service.notifications(max_count='10', include_read=True)

        mock_session.make_request.assert_called_once_with(
            method='get',
            endpoint='/api/fyi/notifications',
            params={'max': '10', 'include': 'read'},
        )

    def test_calls_without_optional_params(self, fyi_service, mock_session):
        """Verify notifications() works without optional parameters."""
        mock_session.make_request = MagicMock(return_value=[])

        fyi_service.notifications()

        mock_session.make_request.assert_called_once_with(
            method='get',
            endpoint='/api/fyi/notifications',
            params={'max': None, 'include': None},
        )


# ---------------------------------------------------------------------------
# FYI.more_notifications tests
# ---------------------------------------------------------------------------


class TestMoreNotifications:
    """Tests for the FYI.more_notifications method."""

    def test_calls_correct_endpoint(self, fyi_service, mock_session):
        """Verify more_notifications() GETs the correct endpoint."""
        mock_session.make_request = MagicMock(return_value=[])

        fyi_service.more_notifications(notification_id='123456')

        mock_session.make_request.assert_called_once_with(
            method='get',
            endpoint='/api/fyi/notifications/more',
            params={'id': '123456'},
        )

    def test_validates_empty_notification_id(self, fyi_service):
        """Verify more_notifications() raises IBCValidationError for empty ID."""
        with pytest.raises(IBCValidationError):
            fyi_service.more_notifications(notification_id='')


# ---------------------------------------------------------------------------
# FYI.mark_notification_read tests
# ---------------------------------------------------------------------------


class TestMarkNotificationRead:
    """Tests for the FYI.mark_notification_read method."""

    def test_calls_correct_endpoint(self, fyi_service, mock_session):
        """Verify mark_notification_read() PUTs to the correct endpoint."""
        mock_session.make_request = MagicMock(return_value={})

        fyi_service.mark_notification_read(notification_id='123456')

        mock_session.make_request.assert_called_once_with(
            method='put',
            endpoint='/api/fyi/notifications/123456',
        )

    def test_validates_empty_notification_id(self, fyi_service):
        """Verify mark_notification_read() raises IBCValidationError for empty ID."""
        with pytest.raises(IBCValidationError):
            fyi_service.mark_notification_read(notification_id='')

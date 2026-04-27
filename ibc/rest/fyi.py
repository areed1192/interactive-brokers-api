"""FYI-related end-points for the Interactive Brokers API."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ibc.exceptions import IBCValidationError
from ibc.session import InteractiveBrokersSession

if TYPE_CHECKING:
    from ibc.client import InteractiveBrokersClient


class FYI:
    """Client for managing FYI notifications via the Interactive Brokers API."""

    def __init__(
        self, ib_client: InteractiveBrokersClient, ib_session: InteractiveBrokersSession
    ) -> None:
        """Initializes the `FYI` client.

        ### Parameters
        ----
        ib_client : InteractiveBrokersClient
            The `InteractiveBrokersClient` Python Client.

        ib_session : InteractiveBrokersSession
            The IB session handler.
        """

        self.client = ib_client
        self.session = ib_session

    def __repr__(self) -> str:
        return "FYI()"

    @staticmethod
    def _validate_id(value: str, name: str) -> None:
        """Validate that an ID parameter is a non-empty string."""
        if not value or not isinstance(value, str) or not value.strip():
            raise IBCValidationError(
                f"{name} must be a non-empty string, got {value!r}"
            )

    def unread_number(self) -> dict:
        """Returns the number of unread FYI notifications.

        ### Returns
        ----
        dict:
            A resource with the unread notification count.

        ### Usage
        ----
            >>> fyi_service = ibc_client.fyi
            >>> fyi_service.unread_number()
        """

        content = self.session.make_request(
            method="get", endpoint="/api/fyi/unreadnumber"
        )

        return content

    def settings(self) -> list:
        """Returns the current FYI notification settings/subscriptions.

        ### Returns
        ----
        list:
            A collection of FYI settings resources.

        ### Usage
        ----
            >>> fyi_service = ibc_client.fyi
            >>> fyi_service.settings()
        """

        content = self.session.make_request(method="get", endpoint="/api/fyi/settings")

        return content

    def toggle_setting(self, typecode: str, enabled: bool = True) -> dict:
        """Enable or disable a specific FYI notification type.

        ### Parameters
        ----
        typecode : str
            The FYI type code to toggle (e.g. ``"A"``, ``"M"``).

        enabled : bool (optional, Default=True)
            Whether to enable or disable the notification type.

        ### Returns
        ----
        dict:
            A confirmation resource.

        ### Usage
        ----
            >>> fyi_service = ibc_client.fyi
            >>> fyi_service.toggle_setting(typecode='A', enabled=True)
        """

        self._validate_id(typecode, "typecode")

        payload = {"enabled": enabled}

        content = self.session.make_request(
            method="post",
            endpoint=f"/api/fyi/settings/{typecode}",
            json_payload=payload,
        )

        return content

    def disclaimer(self, typecode: str) -> dict:
        """Returns the disclaimer for a specific FYI type.

        ### Parameters
        ----
        typecode : str
            The FYI type code.

        ### Returns
        ----
        dict:
            A disclaimer resource.

        ### Usage
        ----
            >>> fyi_service = ibc_client.fyi
            >>> fyi_service.disclaimer(typecode='A')
        """

        self._validate_id(typecode, "typecode")

        content = self.session.make_request(
            method="get", endpoint=f"/api/fyi/disclaimer/{typecode}"
        )

        return content

    def accept_disclaimer(self, typecode: str) -> dict:
        """Mark a FYI disclaimer as read/accepted.

        ### Parameters
        ----
        typecode : str
            The FYI type code.

        ### Returns
        ----
        dict:
            A confirmation resource.

        ### Usage
        ----
            >>> fyi_service = ibc_client.fyi
            >>> fyi_service.accept_disclaimer(typecode='A')
        """

        self._validate_id(typecode, "typecode")

        content = self.session.make_request(
            method="put", endpoint=f"/api/fyi/disclaimer/{typecode}"
        )

        return content

    def delivery_options(self) -> dict:
        """Returns the delivery options for FYI notifications.

        ### Returns
        ----
        dict:
            A delivery options resource.

        ### Usage
        ----
            >>> fyi_service = ibc_client.fyi
            >>> fyi_service.delivery_options()
        """

        content = self.session.make_request(
            method="get", endpoint="/api/fyi/deliveryoptions"
        )

        return content

    def toggle_email_delivery(self, enabled: bool = True) -> dict:
        """Enable or disable FYI email delivery.

        ### Parameters
        ----
        enabled : bool (optional, Default=True)
            Whether to enable email delivery.

        ### Returns
        ----
        dict:
            A confirmation resource.

        ### Usage
        ----
            >>> fyi_service = ibc_client.fyi
            >>> fyi_service.toggle_email_delivery(enabled=True)
        """

        payload = {"enabled": enabled}

        content = self.session.make_request(
            method="put",
            endpoint="/api/fyi/deliveryoptions/email",
            json_payload=payload,
        )

        return content

    def toggle_device_delivery(self, device_id: str, enabled: bool = True) -> dict:
        """Enable or disable FYI notifications for a specific device.

        ### Parameters
        ----
        device_id : str
            The device ID.

        enabled : bool (optional, Default=True)
            Whether to enable notifications for this device.

        ### Returns
        ----
        dict:
            A confirmation resource.

        ### Usage
        ----
            >>> fyi_service = ibc_client.fyi
            >>> fyi_service.toggle_device_delivery(
                device_id='my-device-123',
                enabled=True
            )
        """

        self._validate_id(device_id, "device_id")

        payload = {"deviceId": device_id, "enabled": enabled}

        content = self.session.make_request(
            method="post",
            endpoint="/api/fyi/deliveryoptions/device",
            json_payload=payload,
        )

        return content

    def delete_device(self, device_id: str) -> dict:
        """Delete a notification device.

        ### Parameters
        ----
        device_id : str
            The device ID to delete.

        ### Returns
        ----
        dict:
            A confirmation resource.

        ### Usage
        ----
            >>> fyi_service = ibc_client.fyi
            >>> fyi_service.delete_device(device_id='my-device-123')
        """

        self._validate_id(device_id, "device_id")

        content = self.session.make_request(
            method="delete", endpoint=f"/api/fyi/deliveryoptions/{device_id}"
        )

        return content

    def notifications(self, max_count: str = None, include_read: bool = None) -> list:
        """Returns a list of FYI notifications.

        ### Parameters
        ----
        max_count : str (optional, Default=None)
            Maximum number of notifications to return.

        include_read : bool (optional, Default=None)
            Whether to include read notifications.

        ### Returns
        ----
        list:
            A collection of notification resources.

        ### Usage
        ----
            >>> fyi_service = ibc_client.fyi
            >>> fyi_service.notifications(max_count='10')
        """

        params = {"max": max_count, "include": "read" if include_read else None}

        content = self.session.make_request(
            method="get", endpoint="/api/fyi/notifications", params=params
        )

        return content

    def more_notifications(self, notification_id: str) -> list:
        """Returns more notifications starting from the given ID.

        ### Parameters
        ----
        notification_id : str
            The notification ID to start from for pagination.

        ### Returns
        ----
        list:
            A collection of notification resources.

        ### Usage
        ----
            >>> fyi_service = ibc_client.fyi
            >>> fyi_service.more_notifications(notification_id='123456')
        """

        self._validate_id(notification_id, "notification_id")

        params = {"id": notification_id}

        content = self.session.make_request(
            method="get", endpoint="/api/fyi/notifications/more", params=params
        )

        return content

    def mark_notification_read(self, notification_id: str) -> dict:
        """Mark a specific notification as read.

        ### Parameters
        ----
        notification_id : str
            The notification ID to mark as read.

        ### Returns
        ----
        dict:
            A confirmation resource.

        ### Usage
        ----
            >>> fyi_service = ibc_client.fyi
            >>> fyi_service.mark_notification_read(notification_id='123456')
        """

        self._validate_id(notification_id, "notification_id")

        content = self.session.make_request(
            method="put", endpoint=f"/api/fyi/notifications/{notification_id}"
        )

        return content

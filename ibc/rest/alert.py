"""Alerts-related end-points for the Interactive Brokers API."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ibc.exceptions import IBCValidationError
from ibc.models import AlertResponse
from ibc.session import InteractiveBrokersSession

if TYPE_CHECKING:
    from ibc.client import InteractiveBrokersClient


class Alerts():

    """Client for managing account alerts via the Interactive Brokers API."""

    def __init__(self, ib_client: InteractiveBrokersClient, ib_session: InteractiveBrokersSession) -> None:
        """Initializes the `Alerts` client.

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
        return "Alerts()"

    @staticmethod
    def _validate_id(value: str, name: str) -> None:
        """Validate that an ID parameter is a non-empty string."""
        if not value or not isinstance(value, str) or not value.strip():
            raise IBCValidationError(f"{name} must be a non-empty string, got {value!r}")

    def available_alerts(self, account_id: str) -> list[AlertResponse]:
        """Returns Applicant Id with all owner related entities.

        ### Parameters
        ----
        account_id : str
            The account ID you want a list of alerts for.

        ### Returns
        ----
        list[AlertResponse]:
            A collection of `AlertResponse` resources.

        ### Usage
        ----
            >>> alerts_service = ibc_client.alerts
            >>> alerts_service.available_alerts(
                account_id=ibc_client.account_number
            )
        """

        self._validate_id(account_id, "account_id")

        content = self.session.make_request(
            method='get',
            endpoint=f'/api/iserver/account/{account_id}/alerts'
        )

        return [AlertResponse.from_dict(item) for item in content]

    def mta_alerts(self) -> list:
        """Returns the Mobile Trading Assistant Alert.

        ### Overview
        ----
        Each login user only has one mobile trading assistant (MTA)
        alert with it's own unique tool id. The tool id cannot be
        changed. When modified a new order Id is generated. MTA alerts
        can not be created or deleted. If you call delete 
        /iserver/account/:accountId/alert/:alertId, it will reset MTA
        to default. See here for more information on MTA alerts.

        ### Returns
        ----
        list:
            A collection of `MobileTradingAssistantAlert` resource.

        ### Usage
        ----
            >>> alerts_service = ibc_client.alerts
            >>> alerts_service.mta_alerts()
        """

        content = self.session.make_request(
            method='get',
            endpoint='/api/iserver/account/mta'
        )

        return content

    def create_or_modify_alert(self, account_id: str, alert: dict) -> dict:
        """Creates a new alert or modifies an existing one.

        ### Overview
        ----
        Please note here, if alertId isn't set, it will be a new alert creation,
        otherwise it will modify the existing alert of alertId.

        ### Parameters
        ----
        account_id : str
            The account ID for the alert.

        alert : dict
            The alert definition payload. Include ``alertId`` to modify an existing alert.

        ### Returns
        ----
        dict:
            An alert creation/modification response resource.

        ### Usage
        ----
            >>> alerts_service = ibc_client.alerts
            >>> alerts_service.create_or_modify_alert(
                account_id=ibc_client.account_number,
                alert={
                    "alertName": "Price Alert",
                    "alertMessage": "AAPL crossed 150",
                    "conditions": [
                        {
                            "type": 1,
                            "conidex": "265598",
                            "operator": ">=",
                            "triggerMethod": "0",
                            "value": "150"
                        }
                    ]
                }
            )
        """

        self._validate_id(account_id, "account_id")

        content = self.session.make_request(
            method='post',
            endpoint=f'/api/iserver/account/{account_id}/alert',
            json_payload=alert
        )

        return content

    def activate_alert(self, account_id: str, alert_id: str, activate: bool = True) -> dict:
        """Activates or deactivates an existing alert.

        ### Parameters
        ----
        account_id : str
            The account ID that owns the alert.

        alert_id : str
            The alert ID to activate or deactivate.

        activate : bool (optional, Default=True)
            Set to ``True`` to activate, ``False`` to deactivate.

        ### Returns
        ----
        dict:
            An alert activation response resource.

        ### Usage
        ----
            >>> alerts_service = ibc_client.alerts
            >>> alerts_service.activate_alert(
                account_id=ibc_client.account_number,
                alert_id='12345',
                activate=True
            )
        """

        self._validate_id(account_id, "account_id")
        self._validate_id(alert_id, "alert_id")

        payload = {
            'alertId': int(alert_id),
            'alertActive': int(activate)
        }

        content = self.session.make_request(
            method='post',
            endpoint=f'/api/iserver/account/{account_id}/alert/activate',
            json_payload=payload
        )

        return content

    def delete_alert(self, account_id: str, alert_id: str) -> dict:
        """Deletes an existing alert.

        ### Parameters
        ----
        account_id : str
            The account ID that owns the alert.

        alert_id : str
            The alert ID to delete.

        ### Returns
        ----
        dict:
            An alert deletion response resource.

        ### Usage
        ----
            >>> alerts_service = ibc_client.alerts
            >>> alerts_service.delete_alert(
                account_id=ibc_client.account_number,
                alert_id='12345'
            )
        """

        self._validate_id(account_id, "account_id")
        self._validate_id(alert_id, "alert_id")

        content = self.session.make_request(
            method='delete',
            endpoint=f'/api/iserver/account/{account_id}/alert/{alert_id}'
        )

        return content

    def alert_details(self, alert_id: str) -> AlertResponse:
        """Returns the details of a specific alert.

        ### Parameters
        ----
        alert_id : str
            The alert ID to retrieve.

        ### Returns
        ----
        AlertResponse:
            An alert detail resource.

        ### Usage
        ----
            >>> alerts_service = ibc_client.alerts
            >>> alerts_service.alert_details(alert_id='12345')
        """

        self._validate_id(alert_id, "alert_id")

        content = self.session.make_request(
            method='get',
            endpoint=f'/api/iserver/account/alert/{alert_id}'
        )

        return AlertResponse.from_dict(content)

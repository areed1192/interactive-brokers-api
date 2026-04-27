"""Example usage of the Alerts service."""

from pprint import pprint
from configparser import ConfigParser
from ibc.client import InteractiveBrokersClient

config = ConfigParser()
config.read('config/config.ini')

account_number = config.get('interactive_brokers_paper', 'paper_account')
account_password = config.get('interactive_brokers_paper', 'paper_password')

ibc_client = InteractiveBrokersClient(
    account_number=account_number,
    password=account_password
)
ibc_client.authentication.wait_for_login()

alerts_service = ibc_client.alerts

# ---------------------------------------------------------------------------
# Get all available alerts for the account.
# ---------------------------------------------------------------------------

pprint(alerts_service.available_alerts(account_id=ibc_client.account_number))
# Output: [{'alert_id': 12345, 'alert_name': 'Price Alert', ...}]

# ---------------------------------------------------------------------------
# Get MTA (Mobile Trading Assistant) alerts.
# ---------------------------------------------------------------------------

pprint(alerts_service.mta_alerts())
# Output: [{'alert_id': ..., 'alert_name': '...', ...}]

# ---------------------------------------------------------------------------
# Create or modify an alert.
# ---------------------------------------------------------------------------

alert_body = {
    'alertName': 'Price Alert',
    'alertMessage': 'AAPL crossed 150',
    'outsideRth': 1,
    'conditions': [
        {
            'type': 1,
            'conidex': '265598',
            'operator': '>=',
            'triggerMethod': '0',
            'value': '150'
        }
    ]
}

pprint(
    alerts_service.create_or_modify_alert(
        account_id=ibc_client.account_number,
        alert=alert_body
    )
)
# Output: {'request_id': 123, 'order_id': 456, 'success': True}

# ---------------------------------------------------------------------------
# Activate or deactivate an alert.
# ---------------------------------------------------------------------------

pprint(
    alerts_service.activate_alert(
        account_id=ibc_client.account_number,
        alert_id='12345',
        activate=True
    )
)
# Output: {'request_id': 123, 'order_id': 456, 'success': True}

# ---------------------------------------------------------------------------
# Get alert details.
# ---------------------------------------------------------------------------

pprint(alerts_service.alert_details(alert_id='12345'))
# Output: {'alert_id': 12345, 'alert_name': 'Price Alert', 'conditions': [...]}

# ---------------------------------------------------------------------------
# Delete an alert.
# ---------------------------------------------------------------------------

pprint(
    alerts_service.delete_alert(
        account_id=ibc_client.account_number,
        alert_id='12345'
    )
)
# Output: {'request_id': 123, 'order_id': 456, 'success': True}

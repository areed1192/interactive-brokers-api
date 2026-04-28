"""Example usage of the FYI notifications service."""

from configparser import ConfigParser
from pprint import pprint

from ibc.client import InteractiveBrokersClient

config = ConfigParser()
config.read('config/config.ini')

account_number = config.get('interactive_brokers_paper', 'paper_account')

ibc_client = InteractiveBrokersClient(
    account_number=account_number,
)
ibc_client.authentication.wait_for_login()

fyi_service = ibc_client.fyi

# ---------------------------------------------------------------------------
# Get the number of unread notifications.
# ---------------------------------------------------------------------------

pprint(fyi_service.unread_number())
# Output: {'BN': 3}

# ---------------------------------------------------------------------------
# Get FYI notification settings.
# ---------------------------------------------------------------------------

pprint(fyi_service.settings())
# Output: [{'typecode': 'A', 'description': '...', 'enabled': True}, ...]

# ---------------------------------------------------------------------------
# Get delivery options.
# ---------------------------------------------------------------------------

pprint(fyi_service.delivery_options())
# Output: [{'deviceId': '...', 'deviceName': '...', 'enabled': True}, ...]

# ---------------------------------------------------------------------------
# Get recent notifications.
# ---------------------------------------------------------------------------

pprint(fyi_service.notifications(max_count='10'))
# Output: [{'id': 'abc123', 'FC': 'A', 'HT': '...', 'R': 0}, ...]

# ---------------------------------------------------------------------------
# Get a disclaimer for a specific FYI type.
# ---------------------------------------------------------------------------

pprint(fyi_service.disclaimer(typecode='A'))
# Output: {'typecode': 'A', 'text': '...'}

# ---------------------------------------------------------------------------
# Toggle a specific FYI notification setting on or off.
# ---------------------------------------------------------------------------

pprint(fyi_service.toggle_setting(typecode='A', enabled=True))
# Output: {'V': ['A'], 'T': 1}

# ---------------------------------------------------------------------------
# Accept a disclaimer for a specific FYI type.
# ---------------------------------------------------------------------------

pprint(fyi_service.accept_disclaimer(typecode='A'))
# Output: {'T': 1, 'V': ['A']}

# ---------------------------------------------------------------------------
# Toggle email delivery for FYI notifications.
# ---------------------------------------------------------------------------

pprint(fyi_service.toggle_email_delivery(enabled=True))
# Output: {'T': 1}

# ---------------------------------------------------------------------------
# Toggle push delivery for a specific device.
# ---------------------------------------------------------------------------

# pprint(fyi_service.toggle_device_delivery(device_id='YOUR_DEVICE_ID', enabled=True))
# Output: {'T': 1}

# ---------------------------------------------------------------------------
# Delete a registered device (destructive — commented out).
# ---------------------------------------------------------------------------

# pprint(fyi_service.delete_device(device_id='YOUR_DEVICE_ID'))
# Output: {'T': 1}

# ---------------------------------------------------------------------------
# Fetch older notifications by providing the last notification ID.
# ---------------------------------------------------------------------------

# pprint(fyi_service.more_notifications(notification_id='LAST_NOTIFICATION_ID'))
# Output: [{'id': 'xyz456', 'FC': 'A', 'HT': '...', 'R': 0}, ...]

# ---------------------------------------------------------------------------
# Mark a notification as read.
# ---------------------------------------------------------------------------

# pprint(fyi_service.mark_notification_read(notification_id='NOTIFICATION_ID'))
# Output: {'T': 1}

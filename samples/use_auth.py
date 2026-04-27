"""Example usage of the Authentication service."""

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

auth_service = ibc_client.authentication

# ---------------------------------------------------------------------------
# Login and wait for browser-based authentication.
# ---------------------------------------------------------------------------

auth_service.wait_for_login()

# ---------------------------------------------------------------------------
# Check authentication status.
# ---------------------------------------------------------------------------

pprint(auth_service.is_authenticated())
# Output: {'authenticated': True, 'competing': False, ...}

# ---------------------------------------------------------------------------
# Validate the SSO session.
# ---------------------------------------------------------------------------

pprint(auth_service.sso_validate())
# Output: {'LOGIN_TYPE': 2, 'USER_NAME': 'U1234567', ...}

# ---------------------------------------------------------------------------
# Keep the session alive (tickle).
# ---------------------------------------------------------------------------

pprint(auth_service.tickle())
# Output: {'session': '...', 'ssoExpires': 1234567890, ...}

# ---------------------------------------------------------------------------
# Reauthenticate the session.
# ---------------------------------------------------------------------------

pprint(auth_service.reauthenticate())
# Output: {'message': 'triggered'}

# ---------------------------------------------------------------------------
# Set the active account for the server.
# ---------------------------------------------------------------------------

pprint(auth_service.update_server_account(account_id=ibc_client.account_number))
# Output: {'set': True, 'acctId': 'U1234567'}

# ---------------------------------------------------------------------------
# Logout — terminates the authenticated session.
# ---------------------------------------------------------------------------

# auth_service.logout()
# Output: {'confirmed': True}

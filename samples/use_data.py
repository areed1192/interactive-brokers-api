"""Example usage of the Data service (news, calendar, research)."""

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

data_service = ibc_client.data_services

# ---------------------------------------------------------------------------
# Get a company summary by contract ID.
# ---------------------------------------------------------------------------

pprint(data_service.summary(contract_id='265598'))
# Output: {'265598': {'conid': 265598, 'company_name': 'APPLE INC', ...}}

# ---------------------------------------------------------------------------
# Get news articles related to your portfolio.
# ---------------------------------------------------------------------------

pprint(data_service.portfolio_news())
# Output: [{'article_id': '...', 'headline': '...', ...}]

# ---------------------------------------------------------------------------
# Get the top news articles.
# ---------------------------------------------------------------------------

pprint(data_service.top_news())
# Output: [{'article_id': '...', 'headline': '...', ...}]

# ---------------------------------------------------------------------------
# Get news briefings.
# ---------------------------------------------------------------------------

pprint(data_service.news_briefings())
# Output: [{'article_id': '...', 'headline': '...', ...}]

# ---------------------------------------------------------------------------
# Get available news sources.
# ---------------------------------------------------------------------------

pprint(data_service.news_sources())
# Output: [{'name': 'Dow Jones', 'code': 'DJNL'}, ...]

"""Example usage of the async REST session with httpx."""

import asyncio
from configparser import ConfigParser
from pprint import pprint

from ibc.async_session import AsyncInteractiveBrokersSession
from ibc.client import InteractiveBrokersClient

config = ConfigParser()
config.read('config/config.ini')

account_number = config.get('interactive_brokers_paper', 'paper_account')
account_password = config.get('interactive_brokers_paper', 'paper_password')

ibc_client = InteractiveBrokersClient(
    account_number=account_number,
    password=account_password
)


async def main():
    """Demonstrate async REST requests to the IB Client Portal API."""

    # -----------------------------------------------------------------------
    # Initialize the async session as a context manager.
    # -----------------------------------------------------------------------

    async with AsyncInteractiveBrokersSession(ib_client=ibc_client) as session:

        # -------------------------------------------------------------------
        # Fetch portfolio accounts.
        # -------------------------------------------------------------------

        accounts = await session.make_request(
            method='get',
            endpoint='/api/portfolio/accounts'
        )
        pprint(accounts)
        # Output: [{'accountId': 'U1234567', 'type': 'INDIVIDUAL', ...}]

        # -------------------------------------------------------------------
        # Get a market data snapshot for AAPL (conid 265598).
        # -------------------------------------------------------------------

        snapshot = await session.make_request(
            method='get',
            endpoint='/api/iserver/marketdata/snapshot',
            params={'conids': '265598', 'fields': '31,84,86'}
        )
        pprint(snapshot)
        # Output: [{'conid': 265598, '31': '150.25', '84': '151.00', ...}]

        # -------------------------------------------------------------------
        # Search for a contract by symbol.
        # -------------------------------------------------------------------

        search = await session.make_request(
            method='post',
            endpoint='/api/iserver/secdef/search',
            json_payload={'symbol': 'AAPL', 'name': True}
        )
        pprint(search)
        # Output: [{'conid': 265598, 'companyName': 'APPLE INC', ...}]

        # -------------------------------------------------------------------
        # Multiple concurrent requests using asyncio.gather.
        # -------------------------------------------------------------------

        news_task = session.make_request(method='get', endpoint='/api/iserver/news/top')
        pnl_task = session.make_request(
            method='get',
            endpoint='/api/iserver/account/pnl/partitioned'
        )

        news, pnl = await asyncio.gather(news_task, pnl_task)
        print("\n--- Top News ---")
        pprint(news)
        print("\n--- PnL ---")
        pprint(pnl)


if __name__ == '__main__':
    asyncio.run(main())

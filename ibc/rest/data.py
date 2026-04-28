"""Module for managing accounts via the Interactive Brokers API."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ibc.session import InteractiveBrokersSession
from ibc.utils.validation import validate_id

if TYPE_CHECKING:
    from ibc.client import InteractiveBrokersClient


class Data:
    """Client for managing data services via the Interactive Brokers API."""

    def __init__(self, ib_client: InteractiveBrokersClient, ib_session: InteractiveBrokersSession) -> None:
        """Initializes the `Data` client.

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
        return "Data()"

    def portfolio_news(self) -> dict[str, Any]:
        """Returns a news summary for your portfolio.

        ### Returns
        ----
        list:
            A collection of `NewsArticle` resources.

        ### Usage
        ----
            >>> data_services = ibc_client.data_services
            >>> data_services.portfolio_news()
        """

        content = self.session.make_request(method="get", endpoint="/api/iserver/news/portfolio")

        return content

    def top_news(self) -> dict[str, Any]:
        """Returns the top news articles.

        ### Returns
        ----
        list:
            A collection of `NewsArticle` resources.

        ### Usage
        ----
            >>> data_services = ibc_client.data_services
            >>> data_services.top_news()
        """

        content = self.session.make_request(method="get", endpoint="/api/iserver/news/top")

        return content

    def news_sources(self) -> dict[str, Any]:
        """Returns news sources.

        ### Returns
        ----
        list:
            A collection of `Sources` resources.

        ### Usage
        ----
            >>> data_services = ibc_client.data_services
            >>> data_services.news_sources()
        """

        content = self.session.make_request(method="get", endpoint="/api/iserver/news/sources")

        return content

    def news_briefings(self) -> dict[str, Any]:
        """Returns news briefings.

        ### Returns
        ----
        list:
            A collection of `Briefings` resources.

        ### Usage
        ----
            >>> data_services = ibc_client.data_services
            >>> data_services.news_briefings()
        """

        content = self.session.make_request(method="get", endpoint="/api/iserver/news/briefing")

        return content

    def summary(self, contract_id: str) -> dict[str, Any]:
        """Returns a summary of the contract ID, items include
        company description and more.

        ### Parameters
        ----
        contract_id : str
            The contract Id you want to query.

        ### Returns
        ----
        list:
            A collection of `Summary` resources.

        ### Usage
        ----
            >>> data_services = ibc_client.data_services
            >>> data_services.summary(
                contract_id='265598'
            )
        """

        validate_id(contract_id, "contract_id")

        content = self.session.make_request(method="get", endpoint=f"/api/iserver/fundamentals/{contract_id}/summary")

        return content

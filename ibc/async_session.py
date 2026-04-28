"""Async session for the Interactive Brokers API using httpx."""

from __future__ import annotations

import json
import logging
from typing import TYPE_CHECKING

from ibc.exceptions import IBCRateLimitError, IBCRequestError
from ibc.session import IB_GATEWAY_BASE_URL

if TYPE_CHECKING:
    from ibc.client import InteractiveBrokersClient

logger = logging.getLogger(__name__)

_VALID_METHODS = {"get", "post", "put", "delete", "patch"}


class AsyncInteractiveBrokersSession:
    """Async session for the Interactive Brokers API using ``httpx``.

    .. note::

        This session provides basic retry on HTTP 429, but does **not**
        include the token-bucket rate limiter or configurable request
        timeout that :class:`~ibc.session.InteractiveBrokersSession`
        offers. If you need per-second rate limiting or strict timeout
        control, use the synchronous session or implement these on top
        of this class.
    """

    def __init__(
        self,
        ib_client: InteractiveBrokersClient,
        verify_ssl: bool = False,
        max_retries: int = 3,
    ) -> None:
        """Initializes the async session.

        ### Parameters
        ----
        ib_client : InteractiveBrokersClient
            The `InteractiveBrokersClient` Python Client.

        verify_ssl : bool (optional, Default=False)
            Whether to verify SSL certificates.

        max_retries : int (optional, Default=3)
            Maximum number of retry attempts for rate-limited requests.
        """
        import httpx

        self.client = ib_client
        self.verify_ssl = verify_ssl
        self.resource_url = IB_GATEWAY_BASE_URL
        self.max_retries = max_retries

        self._client = httpx.AsyncClient(
            verify=self.verify_ssl,
            headers={"Content-Type": "application/json"},
        )

    def __repr__(self) -> str:
        return f"AsyncInteractiveBrokersSession(resource_url={self.resource_url!r}, verify_ssl={self.verify_ssl})"

    def build_url(self, endpoint: str) -> str:
        """Build the full URL for a request."""
        return self.resource_url + endpoint

    async def close(self) -> None:
        """Close the underlying httpx client."""
        await self._client.aclose()

    async def __aenter__(self) -> AsyncInteractiveBrokersSession:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.close()

    async def make_request(
        self,
        method: str,
        endpoint: str,
        params: dict | None = None,
        json_payload: dict | None = None,
    ) -> dict:
        """Async version of make_request with retry on 429.

        ### Parameters
        ----
        method : str
            The request method (get, post, put, delete, patch).

        endpoint : str
            The API URL endpoint.

        params : dict (optional)
            URL query parameters.

        json_payload : dict (optional)
            JSON body payload.

        ### Returns
        ----
        dict:
            The parsed JSON response.
        """
        import asyncio

        method = method.lower()

        if method not in _VALID_METHODS:
            raise ValueError(f"Unsupported HTTP method {method!r}. Must be one of {_VALID_METHODS}.")

        url = self.build_url(endpoint=endpoint)
        attempts = 0
        backoff = 1.0

        while True:
            attempts += 1
            logger.info("Async Request: %s %s (attempt %d)", method.upper(), url, attempts)

            response = await self._client.request(
                method=method,
                url=url,
                params=params,
                json=json_payload,
            )

            logger.info("Response Status Code: %s", response.status_code)

            if response.is_success:
                if response.content:
                    data: dict[str, object] = response.json()
                    return data
                return {"message": "response successful", "status_code": response.status_code}

            if response.status_code == 429 and attempts < self.max_retries:
                logger.warning("Rate limited (429), retrying in %.1fs...", backoff)
                await asyncio.sleep(backoff)
                backoff = min(backoff * 2, 10.0)
                continue

            if response.status_code == 429:
                raise IBCRateLimitError(
                    status_code=429,
                    url=str(response.url),
                    method=method.upper(),
                )

            # Error path
            if not response.content:
                response_data = ""
            else:
                try:
                    response_data = response.json()
                except (ValueError, json.JSONDecodeError):
                    response_data = {"content": response.text}

            error_dict = {
                "error_code": response.status_code,
                "response_url": str(response.url),
                "response_body": response_data,
                "response_method": method.upper(),
            }

            logger.error(json.dumps(obj=error_dict, indent=4))

            raise IBCRequestError(
                status_code=response.status_code,
                url=str(response.url),
                method=method.upper(),
                response_body=response_data,
            )

"""Session class for the Interactive Brokers API."""

from __future__ import annotations

import json
import logging
import threading
import time
import warnings
from typing import TYPE_CHECKING

import requests
from urllib3.exceptions import InsecureRequestWarning
from fake_useragent import UserAgent
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from ibc.exceptions import IBCRequestError, IBCRateLimitError

if TYPE_CHECKING:
    from ibc.client import InteractiveBrokersClient

logger = logging.getLogger(__name__)

_VALID_METHODS = {"get", "post", "put", "delete", "patch"}

# Default retry/backoff settings
DEFAULT_MAX_RETRIES = 3
DEFAULT_WAIT_MIN = 1
DEFAULT_WAIT_MAX = 10

# Default rate limit settings (requests per second)
DEFAULT_RATE_LIMIT = 10


class TokenBucket:
    """Thread-safe token bucket rate limiter."""

    def __init__(self, rate: float, capacity: float | None = None) -> None:
        self._rate = rate
        self._capacity = capacity or rate
        self._tokens = self._capacity
        self._last_refill = time.monotonic()
        self._lock = threading.Lock()

    def acquire(self) -> None:
        """Block until a token is available."""
        while True:
            with self._lock:
                now = time.monotonic()
                elapsed = now - self._last_refill
                self._tokens = min(self._capacity, self._tokens + elapsed * self._rate)
                self._last_refill = now
                if self._tokens >= 1.0:
                    self._tokens -= 1.0
                    return
            time.sleep(1.0 / self._rate)


class InteractiveBrokersSession:
    """Serves as the Session for the Interactive Brokers API."""

    def __init__(
        self,
        ib_client: InteractiveBrokersClient,
        verify_ssl: bool = False,
        max_retries: int = DEFAULT_MAX_RETRIES,
        backoff_min: float = DEFAULT_WAIT_MIN,
        backoff_max: float = DEFAULT_WAIT_MAX,
        rate_limit: float = DEFAULT_RATE_LIMIT,
    ) -> None:
        """Initializes the `InteractiveBrokersSession` client.

        ### Overview
        ----
        The `InteractiveBrokersSession` object handles all the requests made
        for the different endpoints on the Interactive Brokers API. Uses a
        persistent ``requests.Session`` for connection pooling and automatic
        cookie handling (required by the IB Client Portal Gateway).

        ### Parameters
        ----
        ib_client : InteractiveBrokersClient
            The `InteractiveBrokersClient` Python Client.

        verify_ssl : bool (optional, Default=False)
            Whether to verify SSL certificates. Defaults to `False`
            because the IB Client Portal Gateway uses a self-signed
            certificate on localhost.

        max_retries : int (optional, Default=3)
            Maximum number of retry attempts for failed requests.

        backoff_min : float (optional, Default=1)
            Minimum wait time in seconds between retries.

        backoff_max : float (optional, Default=10)
            Maximum wait time in seconds between retries.

        rate_limit : float (optional, Default=10)
            Maximum number of requests per second.
        """

        self.client = ib_client
        self.verify_ssl = verify_ssl
        self.resource_url = "https://localhost:5000/v1"
        self.max_retries = max_retries
        self.backoff_min = backoff_min
        self.backoff_max = backoff_max

        self._rate_limiter = TokenBucket(rate=rate_limit)

        self._session = requests.Session()
        self._session.verify = self.verify_ssl
        self._session.headers.update({
            "Content-Type": "application/json",
            "User-Agent": UserAgent().edge,
        })

    def __repr__(self) -> str:
        return (
            f"InteractiveBrokersSession(resource_url={self.resource_url!r}, "
            f"verify_ssl={self.verify_ssl})"
        )

    def build_url(self, endpoint: str) -> str:
        """Build the full URL for a request.

        ### Parameters
        ----
        endpoint : str
            The API endpoint path (e.g. ``/api/iserver/accounts``).

        ### Returns
        ----
        str:
            The full URL with the endpoint appended.
        """

        return self.resource_url + endpoint

    def make_request(
        self,
        method: str,
        endpoint: str,
        params: dict | None = None,
        json_payload: dict | None = None,
    ) -> dict:
        """Handles all the requests in the library.

        ### Overview
        ---
        A central function used to handle all the requests made in the library,
        this function handles building the URL, defining Content-Type, passing
        through payloads, and handling any errors that may arise during the
        request. Includes automatic retry with exponential backoff and
        rate limiting.

        ### Parameters
        ----
        method : str
            The request method. One of ``'get'``, ``'post'``, ``'put'``,
            ``'delete'``, ``'patch'``.

        endpoint : str
            The API URL endpoint, e.g. ``'/api/iserver/accounts'``.

        params : dict (optional, Default=None)
            The URL query parameters for the request.

        json_payload : dict (optional, Default=None)
            A JSON data payload for the request body.

        ### Returns
        ----
        dict:
            The parsed JSON response.

        ### Raises
        ----
        ValueError:
            If ``method`` is not a supported HTTP method.

        IBCRequestError:
            If the response status code indicates an error.

        IBCRateLimitError:
            If the server returns HTTP 429 (rate limited) after all retries.
        """

        method = method.lower()

        if method not in _VALID_METHODS:
            raise ValueError(
                f"Unsupported HTTP method {method!r}. Must be one of {_VALID_METHODS}."
            )

        url = self.build_url(endpoint=endpoint)

        @retry(
            stop=stop_after_attempt(self.max_retries),
            wait=wait_exponential(min=self.backoff_min, max=self.backoff_max),
            retry=retry_if_exception_type(IBCRateLimitError),
            reraise=True,
        )
        def _do_request() -> dict:
            self._rate_limiter.acquire()

            logger.info("Request: %s %s", method.upper(), url)
            logger.info("JSON Payload: %s", json_payload)

            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=InsecureRequestWarning)
                response = self._session.request(
                    method=method,
                    url=url,
                    params=params,
                    json=json_payload,
                )

            logger.info("Response Status Code: %s", response.status_code)
            logger.debug("Response Content: %s", response.text)

            if response.ok:
                if response.content:
                    return response.json()
                return {"message": "response successful", "status_code": response.status_code}

            # Rate limit — raise retryable error
            if response.status_code == 429:
                raise IBCRateLimitError(
                    status_code=429,
                    url=response.url,
                    method=response.request.method,
                )

            # Error path — parse what we can from the response body.
            if not response.content:
                response_data = ""
            else:
                try:
                    response_data = response.json()
                except (ValueError, requests.JSONDecodeError):
                    response_data = {"content": response.text}

            error_dict = {
                "error_code": response.status_code,
                "response_url": response.url,
                "response_body": response_data,
                "response_request": dict(response.request.headers),
                "response_method": response.request.method,
            }

            logger.error(json.dumps(obj=error_dict, indent=4))

            raise IBCRequestError(
                status_code=response.status_code,
                url=response.url,
                method=response.request.method,
                response_body=response_data,
            )

        return _do_request()

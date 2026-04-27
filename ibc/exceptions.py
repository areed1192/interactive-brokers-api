"""Custom exceptions for the Interactive Brokers API client."""

from __future__ import annotations


class IBCError(Exception):
    """Base exception for all Interactive Brokers API client errors."""

    def __init__(self, message: str = "") -> None:
        self.message = message
        super().__init__(self.message)


class IBCRequestError(IBCError):
    """Raised when an API request fails (non-2xx response)."""

    def __init__(
        self,
        message: str = "",
        status_code: int | None = None,
        url: str = "",
        method: str = "",
        response_body: object = None,
    ) -> None:
        self.status_code = status_code
        self.url = url
        self.method = method
        self.response_body = response_body
        super().__init__(message or f"HTTP {status_code} {method} {url}")

    def __repr__(self) -> str:
        return (
            f"IBCRequestError(status_code={self.status_code}, "
            f"method={self.method!r}, url={self.url!r})"
        )


class IBCAuthenticationError(IBCError):
    """Raised when authentication with the IB gateway fails."""


class IBCRateLimitError(IBCRequestError):
    """Raised when the API returns HTTP 429 (Too Many Requests)."""


class IBCValidationError(IBCError):
    """Raised when input validation fails (e.g. empty IDs)."""

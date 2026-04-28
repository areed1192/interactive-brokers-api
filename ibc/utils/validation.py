"""Shared validation utilities for the Interactive Brokers API client."""

from __future__ import annotations

from ibc.exceptions import IBCValidationError


def validate_id(value: str, name: str) -> None:
    """Validate that an ID parameter is a non-empty string.

    ### Parameters
    ----
    value : str
        The value to validate.

    name : str
        The parameter name (used in error messages).

    ### Raises
    ----
    IBCValidationError
        If ``value`` is not a non-empty string.
    """
    if not value or not isinstance(value, str) or not value.strip():
        raise IBCValidationError(f"{name} must be a non-empty string, got {value!r}")


def validate_list(value: list, name: str) -> None:
    """Validate that a list parameter is non-empty.

    ### Parameters
    ----
    value : list
        The value to validate.

    name : str
        The parameter name (used in error messages).

    ### Raises
    ----
    IBCValidationError
        If ``value`` is not a non-empty list.
    """
    if not value or not isinstance(value, list):
        raise IBCValidationError(f"{name} must be a non-empty list, got {value!r}")

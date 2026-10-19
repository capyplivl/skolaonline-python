from __future__ import annotations

from collections.abc import Mapping
from datetime import date, datetime
from enum import Enum
from typing import Any


def parse_datetime(value: str) -> datetime:
    """Parse an ISO 8601 date or date and time returned by the API."""
    return datetime.fromisoformat(value)


def format_query_value(value: Any) -> Any:
    """Convert a Python value to its query string representation."""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, datetime | date):
        return value.isoformat()
    if isinstance(value, list | tuple):
        return [format_query_value(item) for item in value]
    return value


def build_query_params(params: Mapping[str, Any] | None) -> dict[str, Any]:
    """Format query parameters and drop the ones set to None."""
    if not params:
        return {}
    return {
        key: format_query_value(value)
        for key, value in params.items()
        if value is not None
    }


def build_headers(headers: Mapping[str, Any] | None) -> dict[str, str]:
    """Convert header values to strings and drop the ones set to None."""
    if not headers:
        return {}
    return {key: str(value) for key, value in headers.items() if value is not None}

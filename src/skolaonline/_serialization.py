from __future__ import annotations

from collections.abc import Mapping
from datetime import date, datetime
from enum import Enum
from typing import Any


def parse_datetime(value: str) -> datetime:
    return datetime.fromisoformat(value)


def format_query_value(value: Any) -> Any:
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
    if not params:
        return {}
    return {
        key: format_query_value(value)
        for key, value in params.items()
        if value is not None
    }


def build_headers(headers: Mapping[str, Any] | None) -> dict[str, str]:
    if not headers:
        return {}
    return {key: str(value) for key, value in headers.items() if value is not None}

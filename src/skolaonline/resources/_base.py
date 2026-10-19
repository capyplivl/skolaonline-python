from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING, Any, TypeVar
from urllib.parse import quote

import httpx

from skolaonline.models._base import SkolaOnlineModel

if TYPE_CHECKING:
    from skolaonline._async_client import AsyncSkolaOnline
    from skolaonline._client import SkolaOnline

M = TypeVar("M", bound=SkolaOnlineModel)


def encode_path(value: object) -> str:
    """Percent-encode a value for use as a single path segment."""
    return quote(str(value), safe="")


def parse_json(response: httpx.Response) -> Any:
    """Return the decoded JSON body, the text body, or None for an empty body."""
    if not response.content:
        return None
    try:
        return response.json()
    except ValueError:
        return response.text


def parse_model(response: httpx.Response, model: type[M]) -> M:
    """Parse a JSON object response into a model."""
    return model.from_dict(response.json())


def parse_model_list(response: httpx.Response, model: type[M]) -> list[M]:
    """Parse a JSON array response into a list of models."""
    return [model.from_dict(item) for item in response.json()]


def parse_int(response: httpx.Response) -> int:
    """Parse a JSON number response into an integer."""
    return int(response.json())


class SyncAPIResource:
    """Base class of resources used by the synchronous client."""

    def __init__(self, client: SkolaOnline) -> None:
        self._client = client

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: Mapping[str, Any] | None = None,
        json: Any = None,
        files: Sequence[tuple[str, Any]] | None = None,
        headers: Mapping[str, Any] | None = None,
    ) -> httpx.Response:
        return self._client.request(
            method, path, params=params, json=json, files=files, headers=headers
        )


class AsyncAPIResource:
    """Base class of resources used by the asynchronous client."""

    def __init__(self, client: AsyncSkolaOnline) -> None:
        self._client = client

    async def _request(
        self,
        method: str,
        path: str,
        *,
        params: Mapping[str, Any] | None = None,
        json: Any = None,
        files: Sequence[tuple[str, Any]] | None = None,
        headers: Mapping[str, Any] | None = None,
    ) -> httpx.Response:
        return await self._client.request(
            method, path, params=params, json=json, files=files, headers=headers
        )

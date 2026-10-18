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
    return quote(str(value), safe="")


def parse_json(response: httpx.Response) -> Any:
    if not response.content:
        return None
    try:
        return response.json()
    except ValueError:
        return response.text


def parse_model(response: httpx.Response, model: type[M]) -> M:
    return model.from_dict(response.json())


def parse_model_list(response: httpx.Response, model: type[M]) -> list[M]:
    return [model.from_dict(item) for item in response.json()]


def parse_int(response: httpx.Response) -> int:
    return int(response.json())


class SyncAPIResource:
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

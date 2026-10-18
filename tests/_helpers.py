from __future__ import annotations

import dataclasses
import inspect
import json
import re
import types
import typing
from collections.abc import Callable, Sequence
from datetime import date, datetime
from enum import Enum
from pathlib import Path
from typing import Any, get_args, get_origin, get_type_hints

import httpx

from skolaonline.models._base import SkolaOnlineModel

BASE_URL = "https://aplikace.skolaonline.cz/solapi"
SPEC_PATH = Path(__file__).parent / "fixtures" / "swagger.json"
HTTP_METHODS = ("get", "post", "put", "delete", "patch")


def load_spec() -> dict[str, Any]:
    return json.loads(SPEC_PATH.read_text(encoding="utf-8"))


@dataclasses.dataclass(frozen=True)
class SpecOperation:
    method: str
    path: str
    operation: dict[str, Any]

    @property
    def url_pattern(self) -> str:
        path = re.sub(r"\\\{\w+\\\}", "[^/]+", re.escape(self.path))
        return f"^{re.escape(BASE_URL)}{path}(\\?.*)?$"

    def parameters(self, location: str) -> dict[str, dict[str, Any]]:
        return {
            p["name"]: p
            for p in self.operation.get("parameters", [])
            if p["in"] == location
        }

    @property
    def body_content_type(self) -> str | None:
        body = self.operation.get("requestBody")
        if not body:
            return None
        return next(iter(body["content"]))

    def response_payload(self) -> httpx.Response:
        for code, response in self.operation.get("responses", {}).items():
            if not code.startswith("2"):
                continue
            content = response.get("content")
            if not content:
                return httpx.Response(int(code))
            schema = next(iter(content.values()))["schema"]
            if schema.get("type") == "array":
                return httpx.Response(int(code), json=[])
            if schema.get("type") == "integer":
                return httpx.Response(int(code), json=0)
            return httpx.Response(int(code), json={})
        return httpx.Response(200, content=b"payload")


def spec_operations() -> list[SpecOperation]:
    spec = load_spec()
    return [
        SpecOperation(method.upper(), path, operation)
        for path, item in spec["paths"].items()
        for method, operation in item.items()
        if method in HTTP_METHODS
    ]


def dummy_value(tp: Any) -> Any:
    if get_origin(tp) in (types.UnionType, typing.Union):
        members = [a for a in get_args(tp) if a is not type(None)]
        if bytes in members:
            return ("upload.txt", b"data", "text/plain")
        if set(members) == {date, datetime}:
            return date(2024, 9, 2)
        (tp,) = members
    origin = get_origin(tp)
    if origin in (list, Sequence):
        return [dummy_value(get_args(tp)[0])]
    if origin is dict:
        return {}
    if tp is Any:
        return None
    if issubclass(tp, Enum):
        return next(iter(tp))
    if issubclass(tp, SkolaOnlineModel):
        return build_model(tp)
    if tp is datetime:
        return datetime(2024, 9, 2, 8, 0)
    return {bool: True, int: 1, float: 1.5, str: "id-1"}[tp]


def build_model(cls: type[SkolaOnlineModel]) -> SkolaOnlineModel:
    hints = get_type_hints(cls)
    kwargs = {
        field.name: dummy_value(hints[field.name])
        for field in dataclasses.fields(cls)  # type: ignore[arg-type]
        if field.default is dataclasses.MISSING
    }
    return cls(**kwargs)


def call_arguments(method: Callable[..., Any]) -> tuple[list[Any], dict[str, Any]]:
    signature = inspect.signature(method)
    hints = get_type_hints(method)
    args: list[Any] = []
    kwargs: dict[str, Any] = {}
    for name, parameter in signature.parameters.items():
        value = dummy_value(hints[name])
        if parameter.kind is inspect.Parameter.KEYWORD_ONLY:
            kwargs[name] = value
        else:
            args.append(value)
    return args, kwargs


def public_methods(resource: object) -> list[tuple[str, Callable[..., Any]]]:
    return [
        (name, getattr(resource, name))
        for name in dir(resource)
        if not name.startswith("_") and callable(getattr(resource, name))
    ]

from __future__ import annotations

import inspect

import httpx
import respx

from skolaonline import AsyncSkolaOnline, SkolaOnline
from skolaonline.resources._base import AsyncAPIResource, SyncAPIResource
from tests._helpers import (
    SpecOperation,
    call_arguments,
    public_methods,
    spec_operations,
)

OPERATIONS = sorted(spec_operations(), key=lambda op: op.path.count("{"))


def _check_request(op: SpecOperation, request: httpx.Request) -> None:
    query = op.parameters("query")
    sent = set(request.url.params.keys())
    assert sent <= set(query), f"{op.method} {op.path}: unexpected {sent - set(query)}"
    required = {name for name, p in query.items() if p.get("required")}
    assert required <= sent, f"{op.method} {op.path}: missing {required - sent}"
    for name in op.parameters("header"):
        if name != "app-lang":
            assert name in request.headers, f"{op.method} {op.path}: header {name}"
    content_type = op.body_content_type
    if content_type is None:
        assert not request.content
    elif content_type == "multipart/form-data":
        assert request.headers["content-type"].startswith("multipart/form-data")
    else:
        assert request.headers["content-type"] == "application/json"
    assert request.headers["authorization"] == "Bearer token"


def _install_routes(router: respx.Router, hits: list[SpecOperation]) -> None:
    for op in OPERATIONS:

        def handler(request: httpx.Request, op: SpecOperation = op) -> httpx.Response:
            _check_request(op, request)
            hits.append(op)
            return op.response_payload()

        router.route(method=op.method, url__regex=op.url_pattern).mock(
            side_effect=handler
        )


def _resources(client: object, base: type) -> list[tuple[str, object]]:
    return [
        (name, value) for name, value in vars(client).items() if isinstance(value, base)
    ]


def _operation_key(op: SpecOperation) -> str:
    return f"{op.method} {op.path}"


def test_every_operation_is_implemented_by_exactly_one_sync_method() -> None:
    hits: list[SpecOperation] = []
    covered: dict[str, str] = {}
    with respx.mock(assert_all_called=False) as router:
        _install_routes(router, hits)
        with SkolaOnline(access_token="token") as client:
            for resource_name, resource in _resources(client, SyncAPIResource):
                for method_name, method in public_methods(resource):
                    args, kwargs = call_arguments(method)
                    hits.clear()
                    method(*args, **kwargs)
                    assert len(hits) == 1, f"{resource_name}.{method_name}"
                    key = _operation_key(hits[0])
                    assert key not in covered, f"{key} covered twice"
                    covered[key] = f"{resource_name}.{method_name}"
    assert set(covered) == {_operation_key(op) for op in OPERATIONS}


async def test_every_operation_is_implemented_by_exactly_one_async_method() -> None:
    hits: list[SpecOperation] = []
    covered: set[str] = set()
    with respx.mock(assert_all_called=False) as router:
        _install_routes(router, hits)
        async with AsyncSkolaOnline(access_token="token") as client:
            for resource_name, resource in _resources(client, AsyncAPIResource):
                for method_name, method in public_methods(resource):
                    args, kwargs = call_arguments(method)
                    hits.clear()
                    await method(*args, **kwargs)
                    assert len(hits) == 1, f"{resource_name}.{method_name}"
                    covered.add(_operation_key(hits[0]))
    assert covered == {_operation_key(op) for op in OPERATIONS}


def _signatures(client: object, base: type) -> dict[str, inspect.Signature]:
    result = {}
    for resource_name, resource in _resources(client, base):
        for method_name, method in public_methods(resource):
            result[f"{resource_name}.{method_name}"] = inspect.signature(method)
    return result


def test_sync_and_async_clients_expose_identical_methods() -> None:
    sync = _signatures(SkolaOnline(access_token="token"), SyncAPIResource)
    async_ = _signatures(AsyncSkolaOnline(access_token="token"), AsyncAPIResource)
    assert sync == async_
    assert len(sync) == len(OPERATIONS)


def test_all_methods_have_docstrings() -> None:
    client = SkolaOnline(access_token="token")
    undocumented = [
        f"{resource_name}.{method_name}"
        for resource_name, resource in _resources(client, SyncAPIResource)
        for method_name, method in public_methods(resource)
        if not inspect.getdoc(method)
    ]
    assert undocumented == []

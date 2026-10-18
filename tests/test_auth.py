from __future__ import annotations

import time
from urllib.parse import parse_qs

import httpx
import pytest
import respx

from skolaonline import (
    AsyncSkolaOnline,
    AuthenticationError,
    SkolaOnline,
    SkolaOnlineError,
    Token,
    async_get_token,
    async_refresh_access_token,
    get_token,
    refresh_access_token,
)
from tests._helpers import BASE_URL

TOKEN_URL = f"{BASE_URL}/api/connect/token"
PING_URL = f"{BASE_URL}/api/v1/test/ping"


def form(request: httpx.Request) -> dict[str, str]:
    return {k: v[0] for k, v in parse_qs(request.content.decode()).items()}


def token_payload(access: str, refresh: str | None = "refresh-1") -> dict[str, object]:
    payload: dict[str, object] = {
        "access_token": access,
        "token_type": "Bearer",
        "expires_in": 3600,
        "scope": "openid offline_access profile sol_api",
    }
    if refresh is not None:
        payload["refresh_token"] = refresh
    return payload


def test_token_from_response_computes_expiry() -> None:
    token = Token.from_response(token_payload("a"), issued_at=1000.0)
    assert token.expires_at == 4600.0
    assert token.refresh_token == "refresh-1"
    assert token.is_expired()


def test_token_without_expiry_never_expires() -> None:
    assert not Token(access_token="a").is_expired()


@respx.mock
def test_get_token_sends_password_grant() -> None:
    route = respx.post(TOKEN_URL).mock(
        return_value=httpx.Response(200, json=token_payload("access-1"))
    )
    token = get_token("user", "secret")
    assert token.access_token == "access-1"
    assert form(route.calls.last.request) == {
        "grant_type": "password",
        "username": "user",
        "password": "secret",
        "client_id": "test_client",
        "scope": "openid offline_access profile sol_api",
    }


@respx.mock
def test_refresh_access_token_sends_refresh_grant() -> None:
    route = respx.post(TOKEN_URL).mock(
        return_value=httpx.Response(200, json=token_payload("access-2"))
    )
    token = refresh_access_token("refresh-1", client_id="custom")
    assert token.access_token == "access-2"
    assert form(route.calls.last.request) == {
        "grant_type": "refresh_token",
        "refresh_token": "refresh-1",
        "client_id": "custom",
    }


@respx.mock
def test_token_endpoint_errors_raise_authentication_error() -> None:
    respx.post(TOKEN_URL).mock(
        return_value=httpx.Response(
            400,
            json={"error": "invalid_grant", "error_description": "Bad credentials"},
        )
    )
    with pytest.raises(AuthenticationError) as info:
        get_token("user", "wrong")
    assert info.value.status_code == 400
    assert info.value.message == "Bad credentials"
    assert info.value.error_code == "invalid_grant"


@respx.mock
def test_token_endpoint_invalid_payload() -> None:
    respx.post(TOKEN_URL).mock(return_value=httpx.Response(200, json={"foo": 1}))
    with pytest.raises(SkolaOnlineError, match="access_token"):
        get_token("user", "secret")


@respx.mock
def test_client_logs_in_lazily_and_reuses_token() -> None:
    token_route = respx.post(TOKEN_URL).mock(
        return_value=httpx.Response(200, json=token_payload("access-1"))
    )
    ping = respx.get(PING_URL).mock(return_value=httpx.Response(200))
    refreshed: list[Token] = []
    with SkolaOnline(
        username="user", password="secret", on_token_refresh=refreshed.append
    ) as client:
        assert client.token is None
        client.test.ping()
        client.test.ping()
        assert client.token is not None
        assert client.token.access_token == "access-1"
    assert token_route.call_count == 1
    assert ping.calls[0].request.headers["authorization"] == "Bearer access-1"
    assert [t.access_token for t in refreshed] == ["access-1"]


@respx.mock
def test_expired_token_is_refreshed_before_request() -> None:
    token_route = respx.post(TOKEN_URL).mock(
        return_value=httpx.Response(200, json=token_payload("access-2", None))
    )
    ping = respx.get(PING_URL).mock(return_value=httpx.Response(200))
    client = SkolaOnline(
        access_token="access-1", refresh_token="refresh-1", expires_at=time.time() - 1
    )
    client.test.ping()
    assert form(token_route.calls.last.request)["grant_type"] == "refresh_token"
    assert ping.calls.last.request.headers["authorization"] == "Bearer access-2"
    assert client.token is not None
    assert client.token.refresh_token == "refresh-1"


@respx.mock
def test_refresh_token_only_fetches_access_token_first() -> None:
    respx.post(TOKEN_URL).mock(
        return_value=httpx.Response(200, json=token_payload("access-2"))
    )
    ping = respx.get(PING_URL).mock(return_value=httpx.Response(200))
    SkolaOnline(refresh_token="refresh-1").test.ping()
    assert ping.calls.last.request.headers["authorization"] == "Bearer access-2"


@respx.mock
def test_unauthorized_response_triggers_single_refresh_and_retry() -> None:
    respx.post(TOKEN_URL).mock(
        return_value=httpx.Response(200, json=token_payload("access-2"))
    )
    ping = respx.get(PING_URL).mock(
        side_effect=[httpx.Response(401), httpx.Response(200)]
    )
    client = SkolaOnline(access_token="access-1", refresh_token="refresh-1")
    client.test.ping()
    assert [c.request.headers["authorization"] for c in ping.calls] == [
        "Bearer access-1",
        "Bearer access-2",
    ]


@respx.mock
def test_unauthorized_after_fresh_login_is_raised() -> None:
    token_route = respx.post(TOKEN_URL).mock(
        return_value=httpx.Response(200, json=token_payload("access-1"))
    )
    respx.get(PING_URL).mock(return_value=httpx.Response(401))
    client = SkolaOnline(username="user", password="secret")
    with pytest.raises(AuthenticationError):
        client.test.ping()
    assert token_route.call_count == 1


@respx.mock
def test_failed_refresh_falls_back_to_password_grant() -> None:
    token_route = respx.post(TOKEN_URL).mock(
        side_effect=[
            httpx.Response(400, json={"error": "invalid_grant"}),
            httpx.Response(200, json=token_payload("access-3")),
        ]
    )
    ping = respx.get(PING_URL).mock(return_value=httpx.Response(200))
    client = SkolaOnline(
        username="user",
        password="secret",
        access_token="access-1",
        refresh_token="stale",
        expires_at=0,
    )
    client.test.ping()
    grants = [form(c.request)["grant_type"] for c in token_route.calls]
    assert grants == ["refresh_token", "password"]
    assert ping.calls.last.request.headers["authorization"] == "Bearer access-3"


@respx.mock
def test_failed_refresh_without_credentials_raises() -> None:
    respx.post(TOKEN_URL).mock(
        return_value=httpx.Response(400, json={"error": "invalid_grant"})
    )
    client = SkolaOnline(refresh_token="stale")
    with pytest.raises(AuthenticationError):
        client.test.ping()


@respx.mock
def test_static_access_token_is_not_refreshed() -> None:
    respx.get(PING_URL).mock(return_value=httpx.Response(401))
    client = SkolaOnline(access_token="static")
    with pytest.raises(AuthenticationError):
        client.test.ping()


@respx.mock
def test_explicit_login() -> None:
    respx.post(TOKEN_URL).mock(
        return_value=httpx.Response(200, json=token_payload("access-1"))
    )
    client = SkolaOnline(username="user", password="secret")
    token = client.login()
    assert token.access_token == "access-1"
    assert client.token == token


def test_login_requires_oauth() -> None:
    with pytest.raises(SkolaOnlineError):
        SkolaOnline(api_key="key").login()


@respx.mock
def test_api_key_authentication() -> None:
    ping = respx.get(PING_URL).mock(return_value=httpx.Response(200))
    SkolaOnline(api_key="secret-key").test.ping()
    request = ping.calls.last.request
    assert request.headers["x-api-key"] == "secret-key"
    assert "authorization" not in request.headers


@respx.mock
def test_basic_authentication() -> None:
    ping = respx.get(PING_URL).mock(return_value=httpx.Response(200))
    SkolaOnline(basic_auth=("user", "pass")).test.ping()
    assert ping.calls.last.request.headers["authorization"] == "Basic dXNlcjpwYXNz"


@respx.mock
def test_anonymous_requests_have_no_credentials() -> None:
    ping = respx.get(PING_URL).mock(return_value=httpx.Response(200))
    SkolaOnline().test.ping()
    assert "authorization" not in ping.calls.last.request.headers


@pytest.mark.parametrize(
    "kwargs",
    [
        {"api_key": "a", "access_token": "b"},
        {"api_key": "a", "basic_auth": ("u", "p")},
        {"username": "user"},
        {"password": "secret"},
    ],
)
def test_invalid_auth_configuration(kwargs: dict[str, object]) -> None:
    with pytest.raises(SkolaOnlineError):
        SkolaOnline(**kwargs)  # type: ignore[arg-type]


@respx.mock
def test_custom_base_url_is_used_for_token_endpoint() -> None:
    token_route = respx.post("https://example.test/solapi/api/connect/token").mock(
        return_value=httpx.Response(200, json=token_payload("access-1"))
    )
    ping = respx.get("https://example.test/solapi/api/v1/test/ping").mock(
        return_value=httpx.Response(200)
    )
    client = SkolaOnline(
        username="user", password="secret", base_url="https://example.test/solapi/"
    )
    client.test.ping()
    assert token_route.called
    assert ping.called


@respx.mock
async def test_async_token_helpers() -> None:
    respx.post(TOKEN_URL).mock(
        side_effect=[
            httpx.Response(200, json=token_payload("access-1")),
            httpx.Response(200, json=token_payload("access-2")),
        ]
    )
    token = await async_get_token("user", "secret")
    assert token.access_token == "access-1"
    refreshed = await async_refresh_access_token("refresh-1")
    assert refreshed.access_token == "access-2"


@respx.mock
async def test_async_client_refreshes_on_unauthorized() -> None:
    respx.post(TOKEN_URL).mock(
        return_value=httpx.Response(200, json=token_payload("access-2"))
    )
    ping = respx.get(PING_URL).mock(
        side_effect=[httpx.Response(401), httpx.Response(200)]
    )
    async with AsyncSkolaOnline(
        access_token="access-1", refresh_token="refresh-1"
    ) as client:
        await client.test.ping()
    assert ping.calls.last.request.headers["authorization"] == "Bearer access-2"


@respx.mock
async def test_async_explicit_login() -> None:
    respx.post(TOKEN_URL).mock(
        return_value=httpx.Response(200, json=token_payload("access-1"))
    )
    async with AsyncSkolaOnline(username="user", password="secret") as client:
        token = await client.login()
    assert token.access_token == "access-1"

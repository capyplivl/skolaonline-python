from __future__ import annotations

import time
from collections.abc import Callable, Generator, Mapping
from dataclasses import dataclass, replace
from typing import Any

import httpx

from skolaonline._exceptions import (
    AuthenticationError,
    SkolaOnlineError,
    error_from_response,
)

DEFAULT_BASE_URL = "https://aplikace.skolaonline.cz/solapi"
DEFAULT_CLIENT_ID = "test_client"
DEFAULT_SCOPE = "openid offline_access profile sol_api"
DEFAULT_TIMEOUT = 30.0
TOKEN_PATH = "/api/connect/token"
EXPIRY_LEEWAY = 30.0

TokenCallback = Callable[["Token"], None]


@dataclass(frozen=True)
class Token:
    access_token: str
    token_type: str = "Bearer"
    refresh_token: str | None = None
    expires_at: float | None = None
    scope: str | None = None
    id_token: str | None = None

    @classmethod
    def from_response(
        cls, data: Mapping[str, Any], *, issued_at: float | None = None
    ) -> Token:
        issued = time.time() if issued_at is None else issued_at
        expires_in = data.get("expires_in")
        return cls(
            access_token=str(data["access_token"]),
            token_type=str(data.get("token_type") or "Bearer"),
            refresh_token=data.get("refresh_token"),
            expires_at=issued + float(expires_in) if expires_in is not None else None,
            scope=data.get("scope"),
            id_token=data.get("id_token"),
        )

    def is_expired(self, leeway: float = EXPIRY_LEEWAY) -> bool:
        if self.expires_at is None:
            return False
        return time.time() >= self.expires_at - leeway


def token_url(base_url: str) -> str:
    return base_url.rstrip("/") + TOKEN_PATH


def _token_request(
    data: dict[str, str], base_url: str, timeout: float
) -> httpx.Request:
    return httpx.Request(
        "POST",
        token_url(base_url),
        data=data,
        headers={"Accept": "application/json"},
        extensions={"timeout": httpx.Timeout(timeout).as_dict()},
    )


def build_password_request(
    *,
    username: str,
    password: str,
    base_url: str = DEFAULT_BASE_URL,
    client_id: str = DEFAULT_CLIENT_ID,
    scope: str = DEFAULT_SCOPE,
    timeout: float = DEFAULT_TIMEOUT,
) -> httpx.Request:
    data = {
        "grant_type": "password",
        "username": username,
        "password": password,
        "client_id": client_id,
        "scope": scope,
    }
    return _token_request(data, base_url, timeout)


def build_refresh_request(
    *,
    refresh_token: str,
    base_url: str = DEFAULT_BASE_URL,
    client_id: str = DEFAULT_CLIENT_ID,
    timeout: float = DEFAULT_TIMEOUT,
) -> httpx.Request:
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": client_id,
    }
    return _token_request(data, base_url, timeout)


def parse_token_response(
    response: httpx.Response, *, previous: Token | None = None
) -> Token:
    if response.is_error:
        raise error_from_response(response, error_class=AuthenticationError)
    try:
        data = response.json()
    except ValueError as exc:
        raise SkolaOnlineError("Token endpoint returned invalid JSON") from exc
    if not isinstance(data, dict) or "access_token" not in data:
        raise SkolaOnlineError("Token endpoint response is missing access_token")
    token = Token.from_response(data)
    if token.refresh_token is None and previous is not None:
        token = replace(token, refresh_token=previous.refresh_token)
    return token


def get_token(
    username: str,
    password: str,
    *,
    base_url: str = DEFAULT_BASE_URL,
    client_id: str = DEFAULT_CLIENT_ID,
    scope: str = DEFAULT_SCOPE,
    timeout: float = DEFAULT_TIMEOUT,
) -> Token:
    request = build_password_request(
        username=username,
        password=password,
        base_url=base_url,
        client_id=client_id,
        scope=scope,
        timeout=timeout,
    )
    with httpx.Client() as client:
        return parse_token_response(client.send(request))


def refresh_access_token(
    refresh_token: str,
    *,
    base_url: str = DEFAULT_BASE_URL,
    client_id: str = DEFAULT_CLIENT_ID,
    timeout: float = DEFAULT_TIMEOUT,
) -> Token:
    request = build_refresh_request(
        refresh_token=refresh_token,
        base_url=base_url,
        client_id=client_id,
        timeout=timeout,
    )
    with httpx.Client() as client:
        return parse_token_response(client.send(request))


async def async_get_token(
    username: str,
    password: str,
    *,
    base_url: str = DEFAULT_BASE_URL,
    client_id: str = DEFAULT_CLIENT_ID,
    scope: str = DEFAULT_SCOPE,
    timeout: float = DEFAULT_TIMEOUT,
) -> Token:
    request = build_password_request(
        username=username,
        password=password,
        base_url=base_url,
        client_id=client_id,
        scope=scope,
        timeout=timeout,
    )
    async with httpx.AsyncClient() as client:
        return parse_token_response(await client.send(request))


async def async_refresh_access_token(
    refresh_token: str,
    *,
    base_url: str = DEFAULT_BASE_URL,
    client_id: str = DEFAULT_CLIENT_ID,
    timeout: float = DEFAULT_TIMEOUT,
) -> Token:
    request = build_refresh_request(
        refresh_token=refresh_token,
        base_url=base_url,
        client_id=client_id,
        timeout=timeout,
    )
    async with httpx.AsyncClient() as client:
        return parse_token_response(await client.send(request))


class OAuth2Auth(httpx.Auth):
    requires_response_body = True

    def __init__(
        self,
        *,
        username: str | None = None,
        password: str | None = None,
        token: Token | None = None,
        base_url: str = DEFAULT_BASE_URL,
        client_id: str = DEFAULT_CLIENT_ID,
        scope: str = DEFAULT_SCOPE,
        timeout: float = DEFAULT_TIMEOUT,
        on_token_refresh: TokenCallback | None = None,
    ) -> None:
        if token is None and (username is None or password is None):
            raise SkolaOnlineError(
                "OAuth2Auth requires a token or both username and password"
            )
        self.token = token
        self._username = username
        self._password = password
        self._base_url = base_url
        self._client_id = client_id
        self._scope = scope
        self._timeout = timeout
        self._on_token_refresh = on_token_refresh

    @property
    def has_credentials(self) -> bool:
        return self._username is not None and self._password is not None

    def can_renew(self) -> bool:
        return self.has_credentials or (
            self.token is not None and self.token.refresh_token is not None
        )

    def auth_flow(
        self, request: httpx.Request
    ) -> Generator[httpx.Request, httpx.Response, None]:
        renewed = False
        if self.token is None or (self.token.is_expired() and self.can_renew()):
            yield from self.renew_flow()
            renewed = True
        self._apply(request)
        response = yield request
        if response.status_code == 401 and not renewed and self.can_renew():
            yield from self.renew_flow()
            self._apply(request)
            yield request

    def _apply(self, request: httpx.Request) -> None:
        assert self.token is not None
        request.headers["Authorization"] = f"Bearer {self.token.access_token}"

    def renew_flow(self) -> Generator[httpx.Request, httpx.Response, None]:
        previous = self.token
        if previous is not None and previous.refresh_token is not None:
            response = yield build_refresh_request(
                refresh_token=previous.refresh_token,
                base_url=self._base_url,
                client_id=self._client_id,
                timeout=self._timeout,
            )
            if response.is_success or not self.has_credentials:
                self._store(parse_token_response(response, previous=previous))
                return
        if not self.has_credentials:
            raise SkolaOnlineError("No refresh token or credentials available")
        assert self._username is not None
        assert self._password is not None
        response = yield build_password_request(
            username=self._username,
            password=self._password,
            base_url=self._base_url,
            client_id=self._client_id,
            scope=self._scope,
            timeout=self._timeout,
        )
        self._store(parse_token_response(response))

    def _store(self, token: Token) -> None:
        self.token = token
        if self._on_token_refresh is not None:
            self._on_token_refresh(token)


class ApiKeyAuth(httpx.Auth):
    header_name = "X-Api-Key"

    def __init__(self, api_key: str) -> None:
        self._api_key = api_key

    def auth_flow(
        self, request: httpx.Request
    ) -> Generator[httpx.Request, httpx.Response, None]:
        request.headers[self.header_name] = self._api_key
        yield request

from __future__ import annotations

from collections.abc import Mapping, Sequence
from importlib.metadata import version
from typing import Any

import httpx

from skolaonline._auth import (
    DEFAULT_BASE_URL,
    DEFAULT_CLIENT_ID,
    DEFAULT_SCOPE,
    DEFAULT_TIMEOUT,
    ApiKeyAuth,
    OAuth2Auth,
    Token,
    TokenCallback,
)
from skolaonline._exceptions import SkolaOnlineError
from skolaonline._serialization import build_headers, build_query_params

USER_AGENT = f"skolaonline-python/{version('skolaonline')}"


def build_auth(
    *,
    username: str | None,
    password: str | None,
    access_token: str | None,
    refresh_token: str | None,
    expires_at: float | None,
    api_key: str | None,
    basic_auth: tuple[str, str] | None,
    base_url: str,
    client_id: str,
    scope: str,
    timeout: float,
    on_token_refresh: TokenCallback | None,
) -> httpx.Auth | None:
    oauth = (
        username is not None
        or password is not None
        or access_token is not None
        or refresh_token is not None
    )
    selected = sum((oauth, api_key is not None, basic_auth is not None))
    if selected > 1:
        raise SkolaOnlineError(
            "Use only one of OAuth2 credentials, api_key or basic_auth"
        )
    if api_key is not None:
        return ApiKeyAuth(api_key)
    if basic_auth is not None:
        return httpx.BasicAuth(*basic_auth)
    if not oauth:
        return None
    if (username is None) != (password is None):
        raise SkolaOnlineError("username and password must be provided together")
    token = None
    if access_token is not None or refresh_token is not None:
        token = Token(
            access_token=access_token or "",
            refresh_token=refresh_token,
            expires_at=expires_at if access_token is not None else 0.0,
        )
    return OAuth2Auth(
        username=username,
        password=password,
        token=token,
        base_url=base_url,
        client_id=client_id,
        scope=scope,
        timeout=timeout,
        on_token_refresh=on_token_refresh,
    )


class BaseClient:
    def __init__(
        self,
        *,
        username: str | None = None,
        password: str | None = None,
        access_token: str | None = None,
        refresh_token: str | None = None,
        expires_at: float | None = None,
        api_key: str | None = None,
        basic_auth: tuple[str, str] | None = None,
        base_url: str = DEFAULT_BASE_URL,
        language: str | None = None,
        client_id: str = DEFAULT_CLIENT_ID,
        scope: str = DEFAULT_SCOPE,
        timeout: float = DEFAULT_TIMEOUT,
        headers: Mapping[str, str] | None = None,
        on_token_refresh: TokenCallback | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.language = language
        self.timeout = timeout
        self._headers = {
            "Accept": "application/json",
            "User-Agent": USER_AGENT,
            **(headers or {}),
        }
        self._auth = build_auth(
            username=username,
            password=password,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_at=expires_at,
            api_key=api_key,
            basic_auth=basic_auth,
            base_url=self.base_url,
            client_id=client_id,
            scope=scope,
            timeout=timeout,
            on_token_refresh=on_token_refresh,
        )

    @property
    def token(self) -> Token | None:
        if isinstance(self._auth, OAuth2Auth):
            return self._auth.token
        return None

    def _oauth(self) -> OAuth2Auth:
        if not isinstance(self._auth, OAuth2Auth):
            raise SkolaOnlineError("The client is not configured for OAuth2")
        return self._auth

    def _request_options(
        self,
        method: str,
        path: str,
        *,
        params: Mapping[str, Any] | None = None,
        json: Any = None,
        files: Sequence[tuple[str, Any]] | None = None,
        headers: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        merged = dict(self._headers)
        if self.language is not None:
            merged["app-lang"] = self.language
        merged.update(build_headers(headers))
        options: dict[str, Any] = {
            "method": method,
            "url": self.base_url + path,
            "params": build_query_params(params),
            "headers": merged,
            "timeout": self.timeout,
        }
        if self._auth is not None:
            options["auth"] = self._auth
        if json is not None:
            options["json"] = json
        if files is not None:
            options["files"] = list(files)
        return options

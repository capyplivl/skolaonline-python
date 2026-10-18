from __future__ import annotations

from collections.abc import Mapping, Sequence
from types import TracebackType
from typing import Any, Self

import httpx

from skolaonline._auth import (
    DEFAULT_BASE_URL,
    DEFAULT_CLIENT_ID,
    DEFAULT_SCOPE,
    DEFAULT_TIMEOUT,
    Token,
    TokenCallback,
)
from skolaonline._base_client import BaseClient
from skolaonline._exceptions import error_from_response
from skolaonline.resources import (
    AsyncAbsences,
    AsyncApologies,
    AsyncB2C,
    AsyncBehaviors,
    AsyncClassBooks,
    AsyncConfiguration,
    AsyncDataInterface,
    AsyncEmergency,
    AsyncFiles,
    AsyncHomeworks,
    AsyncMarks,
    AsyncMessages,
    AsyncNotifications,
    AsyncPayments,
    AsyncStudentStatus,
    AsyncTest,
    AsyncTimetable,
    AsyncUser,
)


class AsyncSkolaOnline(BaseClient):
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
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        super().__init__(
            username=username,
            password=password,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_at=expires_at,
            api_key=api_key,
            basic_auth=basic_auth,
            base_url=base_url,
            language=language,
            client_id=client_id,
            scope=scope,
            timeout=timeout,
            headers=headers,
            on_token_refresh=on_token_refresh,
        )
        self._owns_http_client = http_client is None
        self._http_client = http_client or httpx.AsyncClient()
        self.absences = AsyncAbsences(self)
        self.apologies = AsyncApologies(self)
        self.b2c = AsyncB2C(self)
        self.behaviors = AsyncBehaviors(self)
        self.class_books = AsyncClassBooks(self)
        self.configuration = AsyncConfiguration(self)
        self.data_interface = AsyncDataInterface(self)
        self.emergency = AsyncEmergency(self)
        self.files = AsyncFiles(self)
        self.homeworks = AsyncHomeworks(self)
        self.marks = AsyncMarks(self)
        self.messages = AsyncMessages(self)
        self.notifications = AsyncNotifications(self)
        self.payments = AsyncPayments(self)
        self.student_status = AsyncStudentStatus(self)
        self.test = AsyncTest(self)
        self.timetable = AsyncTimetable(self)
        self.user = AsyncUser(self)

    async def login(self) -> Token:
        """Obtain a new access token using the configured credentials."""
        auth = self._oauth()
        flow = auth.renew_flow()
        request = next(flow)
        while True:
            response = await self._http_client.send(request)
            try:
                request = flow.send(response)
            except StopIteration:
                break
        assert auth.token is not None
        return auth.token

    async def request(
        self,
        method: str,
        path: str,
        *,
        params: Mapping[str, Any] | None = None,
        json: Any = None,
        files: Sequence[tuple[str, Any]] | None = None,
        headers: Mapping[str, Any] | None = None,
    ) -> httpx.Response:
        """Send a request to an API path and raise on error responses."""
        response = await self._http_client.request(
            **self._request_options(
                method, path, params=params, json=json, files=files, headers=headers
            )
        )
        if response.is_error:
            raise error_from_response(response)
        return response

    async def close(self) -> None:
        """Close the underlying HTTP client if it is owned by this instance."""
        if self._owns_http_client:
            await self._http_client.aclose()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        await self.close()

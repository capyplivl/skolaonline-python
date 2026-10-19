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
    """Asynchronous client for the Škola OnLine API.

    Configure one authentication method: username and password, stored OAuth2
    tokens, an API key, or HTTP Basic credentials. Without credentials only
    anonymous endpoints can be called.

    Args:
        username: Username of the Škola OnLine account.
        password: Password of the Škola OnLine account.
        access_token: Stored OAuth2 access token.
        refresh_token: Stored OAuth2 refresh token used to renew the access token.
        expires_at: Expiry of the stored access token as a Unix timestamp.
        api_key: API key sent in the X-Api-Key header.
        basic_auth: Username and password for HTTP Basic authentication.
        base_url: API root, also used to locate the token endpoint.
        language: Response language sent in the app-lang header, cs or en.
        client_id: OAuth2 client ID.
        scope: Space separated scopes requested by the password grant.
        timeout: Timeout of API and token requests in seconds.
        headers: Extra headers sent with every request.
        on_token_refresh: Callback invoked with every newly obtained token.
        http_client: HTTPX async client to send requests with. A supplied client is not
            closed by this instance.

    Raises:
        SkolaOnlineError: The authentication arguments are inconsistent.
    """

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
        """Absences of students."""
        self.apologies = AsyncApologies(self)
        """Apologies for absences."""
        self.b2c = AsyncB2C(self)
        """User verification for business partners."""
        self.behaviors = AsyncBehaviors(self)
        """Behavior records of students."""
        self.class_books = AsyncClassBooks(self)
        """Class book entries and attendance."""
        self.configuration = AsyncConfiguration(self)
        """Application configuration."""
        self.data_interface = AsyncDataInterface(self)
        """Data interface for system integrations."""
        self.emergency = AsyncEmergency(self)
        """Emergencies and drills."""
        self.files = AsyncFiles(self)
        """Temporary file storage."""
        self.homeworks = AsyncHomeworks(self)
        """Homeworks."""
        self.marks = AsyncMarks(self)
        """Marks and report cards."""
        self.messages = AsyncMessages(self)
        """Messages."""
        self.notifications = AsyncNotifications(self)
        """Push notifications."""
        self.payments = AsyncPayments(self)
        """Payments of students."""
        self.student_status = AsyncStudentStatus(self)
        """Student status data."""
        self.test = AsyncTest(self)
        """API diagnostics."""
        self.timetable = AsyncTimetable(self)
        """Timetable."""
        self.user = AsyncUser(self)
        """Signed-in user."""

    async def login(self) -> Token:
        """Obtain a new token with the configured credentials or refresh token.

        Calling this method is optional. The client signs in automatically before
        the first request.

        Returns:
            Newly obtained token.

        Raises:
            AuthenticationError: The token endpoint rejected the request.
            SkolaOnlineError: The client is not configured for OAuth2.
        """
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
        """Send a request to an API path.

        Args:
            method: HTTP method.
            path: Path relative to the API root, for example /api/v1/user.
            params: Query parameters. None values are omitted.
            json: JSON body.
            files: Multipart files as HTTPX file entries.
            headers: Extra headers. None values are omitted.

        Returns:
            Successful HTTP response.

        Raises:
            APIError: The API answered with an error status code.
        """
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

from __future__ import annotations

from typing import Any

import httpx

_MESSAGE_KEYS = ("userMessage", "message", "detail", "title", "error_description")


class SkolaOnlineError(Exception):
    pass


class APIError(SkolaOnlineError):
    def __init__(
        self,
        message: str,
        *,
        status_code: int,
        response: httpx.Response,
        body: Any = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response = response
        self.body = body


class BadRequestError(APIError):
    pass


class AuthenticationError(APIError):
    @property
    def error_code(self) -> str | None:
        if isinstance(self.body, dict):
            value = self.body.get("error") or self.body.get("errorCode")
            return str(value) if value is not None else None
        return None


class PermissionDeniedError(APIError):
    pass


class NotFoundError(APIError):
    pass


class ConflictError(APIError):
    pass


class UnprocessableEntityError(APIError):
    pass


class RateLimitError(APIError):
    pass


class ServerError(APIError):
    pass


_STATUS_ERRORS: dict[int, type[APIError]] = {
    400: BadRequestError,
    401: AuthenticationError,
    403: PermissionDeniedError,
    404: NotFoundError,
    409: ConflictError,
    422: UnprocessableEntityError,
    429: RateLimitError,
}


def _read_body(response: httpx.Response) -> Any:
    if not response.content:
        return None
    try:
        return response.json()
    except ValueError:
        return response.text


def _extract_message(body: Any, response: httpx.Response) -> str:
    if isinstance(body, str) and body.strip():
        return body.strip()
    if isinstance(body, dict):
        for key in _MESSAGE_KEYS:
            value = body.get(key)
            if isinstance(value, str) and value:
                return value
        error = body.get("error")
        if isinstance(error, str) and error:
            return error
    return response.reason_phrase or f"HTTP {response.status_code}"


def error_from_response(
    response: httpx.Response, *, error_class: type[APIError] | None = None
) -> APIError:
    status = response.status_code
    body = _read_body(response)
    if error_class is None:
        error_class = _STATUS_ERRORS.get(
            status, ServerError if status >= 500 else APIError
        )
    return error_class(
        _extract_message(body, response),
        status_code=status,
        response=response,
        body=body,
    )

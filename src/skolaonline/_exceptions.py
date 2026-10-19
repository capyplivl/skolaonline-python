from __future__ import annotations

from typing import Any

import httpx

_MESSAGE_KEYS = ("userMessage", "message", "detail", "title", "error_description")


class SkolaOnlineError(Exception):
    """Base class of all exceptions raised by the library."""


class APIError(SkolaOnlineError):
    """The API answered with an error status code.

    Args:
        message: Error message taken from the response.
        status_code: HTTP status code of the response.
        response: Original HTTP response.
        body: Decoded JSON body, the response text, or None for an empty body.
    """

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
        """Error message taken from the response."""
        self.status_code = status_code
        """HTTP status code of the response."""
        self.response = response
        """Original HTTP response."""
        self.body = body
        """Decoded JSON body, the response text, or None for an empty body."""


class BadRequestError(APIError):
    """The request was invalid. Raised for HTTP 400."""


class AuthenticationError(APIError):
    """Authentication failed. Raised for HTTP 401 and token endpoint errors."""

    @property
    def error_code(self) -> str | None:
        """OAuth2 error code such as invalid_grant, or the API error code."""
        if isinstance(self.body, dict):
            value = self.body.get("error") or self.body.get("errorCode")
            return str(value) if value is not None else None
        return None


class PermissionDeniedError(APIError):
    """The user is not allowed to access the resource. Raised for HTTP 403."""


class NotFoundError(APIError):
    """The resource does not exist. Raised for HTTP 404."""


class ConflictError(APIError):
    """The request conflicts with the current state. Raised for HTTP 409."""


class UnprocessableEntityError(APIError):
    """The request could not be processed. Raised for HTTP 422."""


class RateLimitError(APIError):
    """Too many requests were sent. Raised for HTTP 429."""


class ServerError(APIError):
    """The server failed to process the request. Raised for HTTP 5xx."""


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
    """Create the exception matching an error response.

    Args:
        response: Error response of the API.
        error_class: Exception class to use instead of the one matching the status.

    Returns:
        Exception describing the error.
    """
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

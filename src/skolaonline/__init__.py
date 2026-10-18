from importlib.metadata import version

from skolaonline._async_client import AsyncSkolaOnline
from skolaonline._auth import (
    DEFAULT_BASE_URL,
    DEFAULT_CLIENT_ID,
    DEFAULT_SCOPE,
    ApiKeyAuth,
    OAuth2Auth,
    Token,
    async_get_token,
    async_refresh_access_token,
    get_token,
    refresh_access_token,
)
from skolaonline._client import SkolaOnline
from skolaonline._exceptions import (
    APIError,
    AuthenticationError,
    BadRequestError,
    ConflictError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
    ServerError,
    SkolaOnlineError,
    UnprocessableEntityError,
)
from skolaonline._files import DownloadedFile
from skolaonline._types import DateLike, FileInput

__version__ = version("skolaonline")

__all__ = [
    "DEFAULT_BASE_URL",
    "DEFAULT_CLIENT_ID",
    "DEFAULT_SCOPE",
    "APIError",
    "ApiKeyAuth",
    "AsyncSkolaOnline",
    "AuthenticationError",
    "BadRequestError",
    "ConflictError",
    "DateLike",
    "DownloadedFile",
    "FileInput",
    "NotFoundError",
    "OAuth2Auth",
    "PermissionDeniedError",
    "RateLimitError",
    "ServerError",
    "SkolaOnline",
    "SkolaOnlineError",
    "Token",
    "UnprocessableEntityError",
    "__version__",
    "async_get_token",
    "async_refresh_access_token",
    "get_token",
    "refresh_access_token",
]

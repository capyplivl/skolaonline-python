from __future__ import annotations

from skolaonline.resources._base import (
    AsyncAPIResource,
    SyncAPIResource,
)


class Test(SyncAPIResource):
    """Endpoints for API diagnostics."""

    def ping(self) -> None:
        """Call the API test endpoint."""
        self._request("GET", "/api/v1/test/ping")


class AsyncTest(AsyncAPIResource):
    """Asynchronous endpoints for API diagnostics."""

    async def ping(self) -> None:
        """Call the API test endpoint."""
        await self._request("GET", "/api/v1/test/ping")

from __future__ import annotations

from skolaonline.models import (
    MinAppVersion,
)
from skolaonline.resources._base import (
    AsyncAPIResource,
    SyncAPIResource,
    parse_model,
)


class Configuration(SyncAPIResource):
    """Endpoints for application configuration."""

    def min_app_version(self) -> MinAppVersion:
        """Return the minimum supported mobile app versions.

        Returns:
            Minimum supported versions of the mobile app.
        """
        response = self._request("GET", "/api/v1/minAppVersion")
        return parse_model(response, MinAppVersion)


class AsyncConfiguration(AsyncAPIResource):
    """Asynchronous endpoints for application configuration."""

    async def min_app_version(self) -> MinAppVersion:
        """Return the minimum supported mobile app versions.

        Returns:
            Minimum supported versions of the mobile app.
        """
        response = await self._request("GET", "/api/v1/minAppVersion")
        return parse_model(response, MinAppVersion)

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
    def min_app_version(self) -> MinAppVersion:
        """Return the minimum supported mobile app versions."""
        response = self._request("GET", "/api/v1/minAppVersion")
        return parse_model(response, MinAppVersion)


class AsyncConfiguration(AsyncAPIResource):
    async def min_app_version(self) -> MinAppVersion:
        """Return the minimum supported mobile app versions."""
        response = await self._request("GET", "/api/v1/minAppVersion")
        return parse_model(response, MinAppVersion)

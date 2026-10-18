from __future__ import annotations

from collections.abc import Sequence

from skolaonline.models import (
    Login,
    UserBulkRefresh,
    UserDetail,
)
from skolaonline.resources._base import (
    AsyncAPIResource,
    SyncAPIResource,
    parse_model,
)


class B2C(SyncAPIResource):
    def authenticate(self, body: Login) -> UserDetail:
        """Return detailed information about the user with the given credentials."""
        response = self._request("POST", "/api/v1/b2c/auth", json=body.to_dict())
        return parse_model(response, UserDetail)

    def synchronize(self, user_ids: Sequence[str]) -> UserBulkRefresh:
        """Return information about the given users."""
        response = self._request("POST", "/api/v1/b2c/synchronize", json=list(user_ids))
        return parse_model(response, UserBulkRefresh)


class AsyncB2C(AsyncAPIResource):
    async def authenticate(self, body: Login) -> UserDetail:
        """Return detailed information about the user with the given credentials."""
        response = await self._request("POST", "/api/v1/b2c/auth", json=body.to_dict())
        return parse_model(response, UserDetail)

    async def synchronize(self, user_ids: Sequence[str]) -> UserBulkRefresh:
        """Return information about the given users."""
        response = await self._request(
            "POST", "/api/v1/b2c/synchronize", json=list(user_ids)
        )
        return parse_model(response, UserBulkRefresh)

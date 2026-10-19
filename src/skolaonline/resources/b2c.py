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
    """Endpoints for user verification for business partners."""

    def authenticate(self, body: Login) -> UserDetail:
        """Return detailed information about the user with the given credentials.

        Args:
            body: Credentials of the user.

        Returns:
            Detailed information about a user.
        """
        response = self._request("POST", "/api/v1/b2c/auth", json=body.to_dict())
        return parse_model(response, UserDetail)

    def synchronize(self, user_ids: Sequence[str]) -> UserBulkRefresh:
        """Return information about the given users.

        Args:
            user_ids: IDs of the users.

        Returns:
            Study information of the requested users.
        """
        response = self._request("POST", "/api/v1/b2c/synchronize", json=list(user_ids))
        return parse_model(response, UserBulkRefresh)


class AsyncB2C(AsyncAPIResource):
    """Asynchronous endpoints for user verification for business partners."""

    async def authenticate(self, body: Login) -> UserDetail:
        """Return detailed information about the user with the given credentials.

        Args:
            body: Credentials of the user.

        Returns:
            Detailed information about a user.
        """
        response = await self._request("POST", "/api/v1/b2c/auth", json=body.to_dict())
        return parse_model(response, UserDetail)

    async def synchronize(self, user_ids: Sequence[str]) -> UserBulkRefresh:
        """Return information about the given users.

        Args:
            user_ids: IDs of the users.

        Returns:
            Study information of the requested users.
        """
        response = await self._request(
            "POST", "/api/v1/b2c/synchronize", json=list(user_ids)
        )
        return parse_model(response, UserBulkRefresh)

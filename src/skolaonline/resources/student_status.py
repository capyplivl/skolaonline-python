from __future__ import annotations

from skolaonline.models import (
    StudentStatusResponse,
)
from skolaonline.resources._base import (
    AsyncAPIResource,
    SyncAPIResource,
    parse_model,
)


class StudentStatus(SyncAPIResource):
    """Endpoints for student status data."""

    def list_students(self, *, page: int | None = None) -> StudentStatusResponse:
        """Return one page of student status records.

        Args:
            page: Page number. Each page contains one organization.

        Returns:
            Student status data of an organization.
        """
        response = self._request("GET", "/api/v1/StudentStatus", params={"page": page})
        return parse_model(response, StudentStatusResponse)


class AsyncStudentStatus(AsyncAPIResource):
    """Asynchronous endpoints for student status data."""

    async def list_students(self, *, page: int | None = None) -> StudentStatusResponse:
        """Return one page of student status records.

        Args:
            page: Page number. Each page contains one organization.

        Returns:
            Student status data of an organization.
        """
        response = await self._request(
            "GET", "/api/v1/StudentStatus", params={"page": page}
        )
        return parse_model(response, StudentStatusResponse)

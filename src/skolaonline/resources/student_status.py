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
    def list_students(self, *, page: int | None = None) -> StudentStatusResponse:
        """Return one page of student status records."""
        response = self._request("GET", "/api/v1/StudentStatus", params={"page": page})
        return parse_model(response, StudentStatusResponse)


class AsyncStudentStatus(AsyncAPIResource):
    async def list_students(self, *, page: int | None = None) -> StudentStatusResponse:
        """Return one page of student status records."""
        response = await self._request(
            "GET", "/api/v1/StudentStatus", params={"page": page}
        )
        return parse_model(response, StudentStatusResponse)

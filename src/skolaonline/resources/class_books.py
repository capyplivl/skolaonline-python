from __future__ import annotations

from skolaonline._types import DateLike
from skolaonline.models import (
    CalculatedNumberOfHourResponse,
    ClassbooksResponse,
    PostClassbookAttendanceRequest,
    PostClassbooksRequest,
)
from skolaonline.resources._base import (
    AsyncAPIResource,
    SyncAPIResource,
    parse_model,
)


class ClassBooks(SyncAPIResource):
    def list_entries(
        self,
        *,
        class_id: str,
        school_year_id: str | None = None,
        from_date: DateLike | None = None,
        to_date: DateLike | None = None,
        lesson_id: str | None = None,
        subject_id: str | None = None,
    ) -> ClassbooksResponse:
        """Return class book entries for a class in the selected period."""
        response = self._request(
            "GET",
            "/api/v1/classBooks",
            params={
                "SchoolYearId": school_year_id,
                "FromDate": from_date,
                "ToDate": to_date,
                "ClassId": class_id,
                "LessonId": lesson_id,
                "SubjectId": subject_id,
            },
        )
        return parse_model(response, ClassbooksResponse)

    def save(self, body: PostClassbooksRequest) -> None:
        """Create, update or delete class book entries."""
        self._request("POST", "/api/v1/classBooks", json=body.to_dict())

    def delete(self, *, entry_id: str, school_year_id: str) -> None:
        """Delete a class book entry."""
        self._request(
            "DELETE",
            "/api/v1/classBooks",
            params={"id": entry_id, "schoolYearId": school_year_id},
        )

    def calculate_lesson_number(
        self, *, event_id: str, event_order: int, school_year_id: str | None = None
    ) -> CalculatedNumberOfHourResponse:
        """Return the calculated lesson numbering for a scheduled event."""
        response = self._request(
            "GET",
            "/api/v1/classBooks/calculatedNumberOfHour",
            params={
                "SchoolYearId": school_year_id,
                "UdalostId": event_id,
                "Poradi": event_order,
            },
        )
        return parse_model(response, CalculatedNumberOfHourResponse)

    def save_attendance(self, body: PostClassbookAttendanceRequest) -> None:
        """Record or update attendance of students in a lesson."""
        self._request("POST", "/api/v1/classBooks/attendance", json=body.to_dict())


class AsyncClassBooks(AsyncAPIResource):
    async def list_entries(
        self,
        *,
        class_id: str,
        school_year_id: str | None = None,
        from_date: DateLike | None = None,
        to_date: DateLike | None = None,
        lesson_id: str | None = None,
        subject_id: str | None = None,
    ) -> ClassbooksResponse:
        """Return class book entries for a class in the selected period."""
        response = await self._request(
            "GET",
            "/api/v1/classBooks",
            params={
                "SchoolYearId": school_year_id,
                "FromDate": from_date,
                "ToDate": to_date,
                "ClassId": class_id,
                "LessonId": lesson_id,
                "SubjectId": subject_id,
            },
        )
        return parse_model(response, ClassbooksResponse)

    async def save(self, body: PostClassbooksRequest) -> None:
        """Create, update or delete class book entries."""
        await self._request("POST", "/api/v1/classBooks", json=body.to_dict())

    async def delete(self, *, entry_id: str, school_year_id: str) -> None:
        """Delete a class book entry."""
        await self._request(
            "DELETE",
            "/api/v1/classBooks",
            params={"id": entry_id, "schoolYearId": school_year_id},
        )

    async def calculate_lesson_number(
        self, *, event_id: str, event_order: int, school_year_id: str | None = None
    ) -> CalculatedNumberOfHourResponse:
        """Return the calculated lesson numbering for a scheduled event."""
        response = await self._request(
            "GET",
            "/api/v1/classBooks/calculatedNumberOfHour",
            params={
                "SchoolYearId": school_year_id,
                "UdalostId": event_id,
                "Poradi": event_order,
            },
        )
        return parse_model(response, CalculatedNumberOfHourResponse)

    async def save_attendance(self, body: PostClassbookAttendanceRequest) -> None:
        """Record or update attendance of students in a lesson."""
        await self._request(
            "POST", "/api/v1/classBooks/attendance", json=body.to_dict()
        )

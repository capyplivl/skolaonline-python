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
    """Endpoints for class book entries and attendance."""

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
        """Return class book entries for a class in the selected period.

        Args:
            class_id: ID of the class.
            school_year_id: ID of the requested school year.
            from_date: Return entries on or after this date.
            to_date: Return entries on or before this date.
            lesson_id: ID of the lesson.
            subject_id: ID of the subject.

        Returns:
            Class book entries of a class.
        """
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
        """Create, update or delete class book entries.

        Args:
            body: Class book entries to save.
        """
        self._request("POST", "/api/v1/classBooks", json=body.to_dict())

    def delete(self, *, entry_id: str, school_year_id: str) -> None:
        """Delete a class book entry.

        Args:
            entry_id: ID of the class book entry.
            school_year_id: ID of the school year.
        """
        self._request(
            "DELETE",
            "/api/v1/classBooks",
            params={"id": entry_id, "schoolYearId": school_year_id},
        )

    def calculate_lesson_number(
        self, *, event_id: str, event_order: int, school_year_id: str | None = None
    ) -> CalculatedNumberOfHourResponse:
        """Return the calculated lesson numbering for a scheduled event.

        Args:
            event_id: ID of the scheduled event.
            event_order: Order of the scheduled event.
            school_year_id: ID of the requested school year.

        Returns:
            Calculated numbering of taught lessons.
        """
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
        """Record or update attendance of students in a lesson.

        Args:
            body: Attendance to save.
        """
        self._request("POST", "/api/v1/classBooks/attendance", json=body.to_dict())


class AsyncClassBooks(AsyncAPIResource):
    """Asynchronous endpoints for class book entries and attendance."""

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
        """Return class book entries for a class in the selected period.

        Args:
            class_id: ID of the class.
            school_year_id: ID of the requested school year.
            from_date: Return entries on or after this date.
            to_date: Return entries on or before this date.
            lesson_id: ID of the lesson.
            subject_id: ID of the subject.

        Returns:
            Class book entries of a class.
        """
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
        """Create, update or delete class book entries.

        Args:
            body: Class book entries to save.
        """
        await self._request("POST", "/api/v1/classBooks", json=body.to_dict())

    async def delete(self, *, entry_id: str, school_year_id: str) -> None:
        """Delete a class book entry.

        Args:
            entry_id: ID of the class book entry.
            school_year_id: ID of the school year.
        """
        await self._request(
            "DELETE",
            "/api/v1/classBooks",
            params={"id": entry_id, "schoolYearId": school_year_id},
        )

    async def calculate_lesson_number(
        self, *, event_id: str, event_order: int, school_year_id: str | None = None
    ) -> CalculatedNumberOfHourResponse:
        """Return the calculated lesson numbering for a scheduled event.

        Args:
            event_id: ID of the scheduled event.
            event_order: Order of the scheduled event.
            school_year_id: ID of the requested school year.

        Returns:
            Calculated numbering of taught lessons.
        """
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
        """Record or update attendance of students in a lesson.

        Args:
            body: Attendance to save.
        """
        await self._request(
            "POST", "/api/v1/classBooks/attendance", json=body.to_dict()
        )

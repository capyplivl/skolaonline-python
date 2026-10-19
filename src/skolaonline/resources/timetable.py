from __future__ import annotations

from skolaonline._types import DateLike
from skolaonline.models import (
    TimetableCodeListsResponse,
    TimetableDetailResponse,
    TimetableResponse,
)
from skolaonline.resources._base import (
    AsyncAPIResource,
    SyncAPIResource,
    parse_model,
)


class Timetable(SyncAPIResource):
    """Endpoints for the timetable."""

    def retrieve(
        self,
        *,
        school_year_id: str | None = None,
        date_from: DateLike | None = None,
        date_to: DateLike | None = None,
        student_id: str | None = None,
        lesson_id: str | None = None,
        subject_id: str | None = None,
        class_id: str | None = None,
    ) -> TimetableResponse:
        """Return the timetable for the selected period.

        Args:
            school_year_id: ID of the requested school year.
            date_from: First day of the timetable.
            date_to: Last day of the timetable.
            student_id: ID of the student.
            lesson_id: ID of the lesson.
            subject_id: ID of the subject.
            class_id: ID of the class.

        Returns:
            Timetable for a date range.
        """
        response = self._request(
            "GET",
            "/api/v1/timeTable",
            params={
                "SchoolYearId": school_year_id,
                "DateFrom": date_from,
                "DateTo": date_to,
                "StudentId": student_id,
                "LessonId": lesson_id,
                "SubjectId": subject_id,
                "ClassId": class_id,
            },
        )
        return parse_model(response, TimetableResponse)

    def code_lists(
        self, *, school_year_id: str | None = None, student_id: str | None = None
    ) -> TimetableCodeListsResponse:
        """Return the code lists used by the timetable module.

        Args:
            school_year_id: ID of the school year. Defaults to the current school year.
            student_id: ID of the student. Used by parents.

        Returns:
            Code lists used by the timetable module.
        """
        response = self._request(
            "GET",
            "/api/v1/timeTable/codeLists",
            params={"schoolYearId": school_year_id, "studentId": student_id},
        )
        return parse_model(response, TimetableCodeListsResponse)

    def retrieve_detail(
        self,
        *,
        event_id: str,
        event_order: int,
        school_year_id: str | None = None,
        student_id: str | None = None,
    ) -> TimetableDetailResponse:
        """Return the detail of a scheduled event.

        Args:
            event_id: ID of the scheduled event.
            event_order: Order of the scheduled event.
            school_year_id: ID of the requested school year.
            student_id: ID of the student.

        Returns:
            Detail of a scheduled event.
        """
        response = self._request(
            "GET",
            "/api/v1/timeTableDetail",
            params={
                "SchoolYearId": school_year_id,
                "StudentId": student_id,
                "UdalostId": event_id,
                "Poradi": event_order,
            },
        )
        return parse_model(response, TimetableDetailResponse)


class AsyncTimetable(AsyncAPIResource):
    """Asynchronous endpoints for the timetable."""

    async def retrieve(
        self,
        *,
        school_year_id: str | None = None,
        date_from: DateLike | None = None,
        date_to: DateLike | None = None,
        student_id: str | None = None,
        lesson_id: str | None = None,
        subject_id: str | None = None,
        class_id: str | None = None,
    ) -> TimetableResponse:
        """Return the timetable for the selected period.

        Args:
            school_year_id: ID of the requested school year.
            date_from: First day of the timetable.
            date_to: Last day of the timetable.
            student_id: ID of the student.
            lesson_id: ID of the lesson.
            subject_id: ID of the subject.
            class_id: ID of the class.

        Returns:
            Timetable for a date range.
        """
        response = await self._request(
            "GET",
            "/api/v1/timeTable",
            params={
                "SchoolYearId": school_year_id,
                "DateFrom": date_from,
                "DateTo": date_to,
                "StudentId": student_id,
                "LessonId": lesson_id,
                "SubjectId": subject_id,
                "ClassId": class_id,
            },
        )
        return parse_model(response, TimetableResponse)

    async def code_lists(
        self, *, school_year_id: str | None = None, student_id: str | None = None
    ) -> TimetableCodeListsResponse:
        """Return the code lists used by the timetable module.

        Args:
            school_year_id: ID of the school year. Defaults to the current school year.
            student_id: ID of the student. Used by parents.

        Returns:
            Code lists used by the timetable module.
        """
        response = await self._request(
            "GET",
            "/api/v1/timeTable/codeLists",
            params={"schoolYearId": school_year_id, "studentId": student_id},
        )
        return parse_model(response, TimetableCodeListsResponse)

    async def retrieve_detail(
        self,
        *,
        event_id: str,
        event_order: int,
        school_year_id: str | None = None,
        student_id: str | None = None,
    ) -> TimetableDetailResponse:
        """Return the detail of a scheduled event.

        Args:
            event_id: ID of the scheduled event.
            event_order: Order of the scheduled event.
            school_year_id: ID of the requested school year.
            student_id: ID of the student.

        Returns:
            Detail of a scheduled event.
        """
        response = await self._request(
            "GET",
            "/api/v1/timeTableDetail",
            params={
                "SchoolYearId": school_year_id,
                "StudentId": student_id,
                "UdalostId": event_id,
                "Poradi": event_order,
            },
        )
        return parse_model(response, TimetableDetailResponse)

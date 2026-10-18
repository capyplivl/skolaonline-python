from __future__ import annotations

from skolaonline._types import DateLike
from skolaonline.models import (
    FinalMarksResponse,
    MarkCodeListsResponse,
    MarksListOrder,
    MarksListResponse,
    MarksListSigningFilter,
    MarksResponse,
    PostTeacherMarksRequest,
    PutMultipleSignRequest,
    SingleMark,
    TeacherMarkingStudentsResponse,
    TeacherMarksRequest,
    TeacherMarksResponse,
)
from skolaonline.resources._base import (
    AsyncAPIResource,
    SyncAPIResource,
    encode_path,
    parse_model,
)


class Marks(SyncAPIResource):
    def list_by_subject(
        self,
        student_id: str,
        *,
        school_year_id: str | None = None,
        semester_id: str | None = None,
        date_from: DateLike | None = None,
        date_to: DateLike | None = None,
    ) -> MarksResponse:
        """Return marks of a student grouped by subject."""
        response = self._request(
            "GET",
            f"/api/v1/students/{encode_path(student_id)}/marks/bySubject",
            params={
                "SchoolYearId": school_year_id,
                "SemesterId": semester_id,
                "DateFrom": date_from,
                "DateTo": date_to,
            },
        )
        return parse_model(response, MarksResponse)

    def list_marks(
        self,
        student_id: str,
        *,
        order_by: MarksListOrder | None = None,
        signing_filter: MarksListSigningFilter | None = None,
        subject_id: str | None = None,
        page_number: int | None = None,
        page_size: int | None = None,
        school_year_id: str | None = None,
        semester_id: str | None = None,
        date_from: DateLike | None = None,
        date_to: DateLike | None = None,
    ) -> MarksListResponse:
        """Return a flat list of marks of a student."""
        response = self._request(
            "GET",
            f"/api/v1/students/{encode_path(student_id)}/marks/list",
            params={
                "OrderBy": order_by,
                "SigningFilter": signing_filter,
                "SubjectId": subject_id,
                "Pagination.PageNumber": page_number,
                "Pagination.PageSize": page_size,
                "SchoolYearId": school_year_id,
                "SemesterId": semester_id,
                "DateFrom": date_from,
                "DateTo": date_to,
            },
        )
        return parse_model(response, MarksListResponse)

    def list_final(
        self, student_id: str, *, school_year_id: str | None = None
    ) -> FinalMarksResponse:
        """Return the final report card marks of a student."""
        response = self._request(
            "GET",
            f"/api/v1/students/{encode_path(student_id)}/marks/final",
            params={"schoolYearId": school_year_id},
        )
        return parse_model(response, FinalMarksResponse)

    def retrieve(self, mark_id: str, *, student_id: str | None = None) -> SingleMark:
        """Return a single mark of a student."""
        response = self._request(
            "GET",
            f"/api/v1/student/marks/{encode_path(mark_id)}",
            params={"studentId": student_id},
        )
        return parse_model(response, SingleMark)

    def code_lists(
        self, *, school_year_id: str | None = None, student_id: str | None = None
    ) -> MarkCodeListsResponse:
        """Return the code lists used by the marks module."""
        response = self._request(
            "GET",
            "/api/v1/marks/codeLists",
            params={"schoolYearId": school_year_id, "studentId": student_id},
        )
        return parse_model(response, MarkCodeListsResponse)

    def retrieve_for_teacher(
        self, marks_id: str, *, school_year_id: str | None = None
    ) -> TeacherMarksResponse:
        """Return a mark record created by the teacher."""
        response = self._request(
            "GET",
            f"/api/v1/teacher/marks/{encode_path(marks_id)}",
            params={"schoolYearId": school_year_id},
        )
        return parse_model(response, TeacherMarksResponse)

    def update_for_teacher(self, marks_id: str, body: TeacherMarksRequest) -> None:
        """Update a mark record created by the teacher."""
        self._request(
            "PUT", f"/api/v1/teacher/marks/{encode_path(marks_id)}", json=body.to_dict()
        )

    def delete_for_teacher(self, marks_id: str, *, school_year_id: str) -> None:
        """Delete a mark record created by the teacher."""
        self._request(
            "DELETE",
            f"/api/v1/teacher/marks/{encode_path(marks_id)}",
            params={"schoolYearId": school_year_id},
        )

    def list_marking_students(
        self, *, event_id: str, event_order: int, school_year_id: str
    ) -> TeacherMarkingStudentsResponse:
        """Return students that can be marked in a scheduled lesson."""
        response = self._request(
            "GET",
            "/api/v1/teacher/markingStudents",
            params={
                "udalostId": event_id,
                "poradi": event_order,
                "schoolYearId": school_year_id,
            },
        )
        return parse_model(response, TeacherMarkingStudentsResponse)

    def create_for_teacher(self, body: PostTeacherMarksRequest) -> None:
        """Create a new mark record for students."""
        self._request("POST", "/api/v1/teacher/marks", json=body.to_dict())

    def sign(self, student_id: str, mark_id: str) -> None:
        """Sign a single mark of a student."""
        self._request(
            "PUT",
            f"/api/v1/students/{encode_path(student_id)}/marks/{encode_path(mark_id)}/sign",
        )

    def sign_many(self, student_id: str, body: PutMultipleSignRequest) -> None:
        """Sign multiple marks of a student."""
        self._request(
            "PUT",
            f"/api/v1/students/{encode_path(student_id)}/marks/sign",
            json=body.to_dict(),
        )


class AsyncMarks(AsyncAPIResource):
    async def list_by_subject(
        self,
        student_id: str,
        *,
        school_year_id: str | None = None,
        semester_id: str | None = None,
        date_from: DateLike | None = None,
        date_to: DateLike | None = None,
    ) -> MarksResponse:
        """Return marks of a student grouped by subject."""
        response = await self._request(
            "GET",
            f"/api/v1/students/{encode_path(student_id)}/marks/bySubject",
            params={
                "SchoolYearId": school_year_id,
                "SemesterId": semester_id,
                "DateFrom": date_from,
                "DateTo": date_to,
            },
        )
        return parse_model(response, MarksResponse)

    async def list_marks(
        self,
        student_id: str,
        *,
        order_by: MarksListOrder | None = None,
        signing_filter: MarksListSigningFilter | None = None,
        subject_id: str | None = None,
        page_number: int | None = None,
        page_size: int | None = None,
        school_year_id: str | None = None,
        semester_id: str | None = None,
        date_from: DateLike | None = None,
        date_to: DateLike | None = None,
    ) -> MarksListResponse:
        """Return a flat list of marks of a student."""
        response = await self._request(
            "GET",
            f"/api/v1/students/{encode_path(student_id)}/marks/list",
            params={
                "OrderBy": order_by,
                "SigningFilter": signing_filter,
                "SubjectId": subject_id,
                "Pagination.PageNumber": page_number,
                "Pagination.PageSize": page_size,
                "SchoolYearId": school_year_id,
                "SemesterId": semester_id,
                "DateFrom": date_from,
                "DateTo": date_to,
            },
        )
        return parse_model(response, MarksListResponse)

    async def list_final(
        self, student_id: str, *, school_year_id: str | None = None
    ) -> FinalMarksResponse:
        """Return the final report card marks of a student."""
        response = await self._request(
            "GET",
            f"/api/v1/students/{encode_path(student_id)}/marks/final",
            params={"schoolYearId": school_year_id},
        )
        return parse_model(response, FinalMarksResponse)

    async def retrieve(
        self, mark_id: str, *, student_id: str | None = None
    ) -> SingleMark:
        """Return a single mark of a student."""
        response = await self._request(
            "GET",
            f"/api/v1/student/marks/{encode_path(mark_id)}",
            params={"studentId": student_id},
        )
        return parse_model(response, SingleMark)

    async def code_lists(
        self, *, school_year_id: str | None = None, student_id: str | None = None
    ) -> MarkCodeListsResponse:
        """Return the code lists used by the marks module."""
        response = await self._request(
            "GET",
            "/api/v1/marks/codeLists",
            params={"schoolYearId": school_year_id, "studentId": student_id},
        )
        return parse_model(response, MarkCodeListsResponse)

    async def retrieve_for_teacher(
        self, marks_id: str, *, school_year_id: str | None = None
    ) -> TeacherMarksResponse:
        """Return a mark record created by the teacher."""
        response = await self._request(
            "GET",
            f"/api/v1/teacher/marks/{encode_path(marks_id)}",
            params={"schoolYearId": school_year_id},
        )
        return parse_model(response, TeacherMarksResponse)

    async def update_for_teacher(
        self, marks_id: str, body: TeacherMarksRequest
    ) -> None:
        """Update a mark record created by the teacher."""
        await self._request(
            "PUT", f"/api/v1/teacher/marks/{encode_path(marks_id)}", json=body.to_dict()
        )

    async def delete_for_teacher(self, marks_id: str, *, school_year_id: str) -> None:
        """Delete a mark record created by the teacher."""
        await self._request(
            "DELETE",
            f"/api/v1/teacher/marks/{encode_path(marks_id)}",
            params={"schoolYearId": school_year_id},
        )

    async def list_marking_students(
        self, *, event_id: str, event_order: int, school_year_id: str
    ) -> TeacherMarkingStudentsResponse:
        """Return students that can be marked in a scheduled lesson."""
        response = await self._request(
            "GET",
            "/api/v1/teacher/markingStudents",
            params={
                "udalostId": event_id,
                "poradi": event_order,
                "schoolYearId": school_year_id,
            },
        )
        return parse_model(response, TeacherMarkingStudentsResponse)

    async def create_for_teacher(self, body: PostTeacherMarksRequest) -> None:
        """Create a new mark record for students."""
        await self._request("POST", "/api/v1/teacher/marks", json=body.to_dict())

    async def sign(self, student_id: str, mark_id: str) -> None:
        """Sign a single mark of a student."""
        await self._request(
            "PUT",
            f"/api/v1/students/{encode_path(student_id)}/marks/{encode_path(mark_id)}/sign",
        )

    async def sign_many(self, student_id: str, body: PutMultipleSignRequest) -> None:
        """Sign multiple marks of a student."""
        await self._request(
            "PUT",
            f"/api/v1/students/{encode_path(student_id)}/marks/sign",
            json=body.to_dict(),
        )

from __future__ import annotations

from skolaonline._files import DownloadedFile, downloaded_file, to_multipart
from skolaonline._types import DateLike, FileInput
from skolaonline.models import (
    HomeworkCodeListsResponse,
    HomeworkResponse,
    HomeworksFilterState,
    HomeworksResponse,
    HomeworkState,
    HomeworksTeacherResponse,
    HomeworkTeacherState,
    PutElaborationRequest,
)
from skolaonline.resources._base import (
    AsyncAPIResource,
    SyncAPIResource,
    encode_path,
    parse_model,
)


class Homeworks(SyncAPIResource):
    """Endpoints for homeworks."""

    def list_for_student(
        self,
        student_id: str,
        *,
        school_year_id: str | None = None,
        subject_id: str | None = None,
        date_from: DateLike | None = None,
        date_to: DateLike | None = None,
        filter: HomeworksFilterState | None = None,
        state: HomeworkState | None = None,
        page_number: int | None = None,
        page_size: int | None = None,
    ) -> HomeworksResponse:
        """Return homeworks of a student matching the filter.

        Args:
            student_id: ID of the student.
            school_year_id: ID of the requested school year.
            subject_id: ID of the subject.
            date_from: Start of the date range.
            date_to: End of the date range.
            filter: Filter of the homeworks.
            state: Filter by assignment and due dates.
            page_number: Page number, starting at 1.
            page_size: Page size.

        Returns:
            Homeworks of a student.
        """
        response = self._request(
            "GET",
            f"/api/v1/students/{encode_path(student_id)}/homeworks",
            params={
                "SchoolYearId": school_year_id,
                "SubjectId": subject_id,
                "DateFrom": date_from,
                "DateTo": date_to,
                "Filter": filter,
                "State": state,
                "Pagination.PageNumber": page_number,
                "Pagination.PageSize": page_size,
            },
        )
        return parse_model(response, HomeworksResponse)

    def download_assignment_attachment(
        self, attachment_id: str, *, student_id: str, school_year_id: str | None = None
    ) -> DownloadedFile:
        """Download an attachment of a homework assignment.

        Args:
            attachment_id: ID of the attachment.
            student_id: ID of the student.
            school_year_id: ID of the requested school year.

        Returns:
            Downloaded file with its name and content type.
        """
        response = self._request(
            "GET",
            f"/api/v1/student/homeworks/assignment/attachments/{encode_path(attachment_id)}",
            params={"SchoolYearId": school_year_id, "StudentId": student_id},
        )
        return downloaded_file(response)

    def download_elaboration_attachment(
        self, attachment_id: str, *, student_id: str, school_year_id: str | None = None
    ) -> DownloadedFile:
        """Download an attachment of a homework elaboration.

        Args:
            attachment_id: ID of the attachment.
            student_id: ID of the student.
            school_year_id: ID of the requested school year.

        Returns:
            Downloaded file with its name and content type.
        """
        response = self._request(
            "GET",
            f"/api/v1/student/homeworks/elaboration/attachments/{encode_path(attachment_id)}",
            params={"SchoolYearId": school_year_id, "StudentId": student_id},
        )
        return downloaded_file(response)

    def list_for_teacher(
        self,
        *,
        school_year_id: str | None = None,
        subject_id: str | None = None,
        date_from: DateLike | None = None,
        date_to: DateLike | None = None,
        closed: bool | None = None,
        state: HomeworkTeacherState | None = None,
        page_number: int | None = None,
        page_size: int | None = None,
    ) -> HomeworksTeacherResponse:
        """Return homeworks assigned by the teacher.

        Args:
            school_year_id: ID of the requested school year.
            subject_id: ID of the subject.
            date_from: Start of the date range.
            date_to: End of the date range.
            closed: Include closed homeworks.
            state: Filter of homeworks assigned by a teacher.
            page_number: Page number, starting at 1.
            page_size: Page size.

        Returns:
            Homeworks assigned by a teacher.
        """
        response = self._request(
            "GET",
            "/api/v1/teacher/homeworks",
            params={
                "SchoolYearId": school_year_id,
                "SubjectId": subject_id,
                "DateFrom": date_from,
                "DateTo": date_to,
                "Closed": closed,
                "State": state,
                "Pagination.PageNumber": page_number,
                "Pagination.PageSize": page_size,
            },
        )
        return parse_model(response, HomeworksTeacherResponse)

    def code_lists(
        self, *, school_year_id: str | None = None, student_id: str | None = None
    ) -> HomeworkCodeListsResponse:
        """Return the code lists used by the homeworks module.

        Args:
            school_year_id: ID of the school year. Defaults to the current school year.
            student_id: ID of the student. Used by parents.

        Returns:
            Code lists used by the homeworks module.
        """
        response = self._request(
            "GET",
            "/api/v1/homeWorks/codeLists",
            params={"schoolYearId": school_year_id, "studentId": student_id},
        )
        return parse_model(response, HomeworkCodeListsResponse)

    def retrieve(
        self, homework_id: str, *, student_id: str | None = None
    ) -> HomeworkResponse:
        """Return a single homework of a student.

        Args:
            homework_id: ID of the homework.
            student_id: ID of the student.

        Returns:
            Single homework of a student.
        """
        response = self._request(
            "GET",
            f"/api/v1/student/homeworks/{encode_path(homework_id)}",
            params={"studentId": student_id},
        )
        return parse_model(response, HomeworkResponse)

    def save_elaboration(self, homework_id: str, body: PutElaborationRequest) -> None:
        """Submit the elaboration of a homework.

        Args:
            homework_id: ID of the homework.
            body: Elaboration of the homework.
        """
        self._request(
            "POST",
            f"/api/v1/student/homeworks/{encode_path(homework_id)}/elaboration",
            json=body.to_dict(),
        )

    def upload_elaboration_attachment(
        self,
        homework_id: str,
        file: FileInput,
        *,
        submit: bool,
        school_year_id: str | None = None,
        display_name: str | None = None,
    ) -> None:
        """Attach a file to the elaboration of a homework.

        Args:
            homework_id: ID of the homework.
            file: File to attach.
            submit: Whether the homework is submitted. False saves it as a work in
                progress.
            school_year_id: ID of the requested school year.
            display_name: File name shown to users.
        """
        self._request(
            "POST",
            f"/api/v1/student/homeworks/{encode_path(homework_id)}/elaboration/attachments",
            params={
                "SchoolYearId": school_year_id,
                "Submit": submit,
                "NameUser": display_name,
            },
            files=[to_multipart("Data", file)],
        )

    def mark_done(self, homework_id: str, *, school_year_id: str | None = None) -> None:
        """Mark a homework without submission as done.

        Args:
            homework_id: ID of the homework.
            school_year_id: ID of the requested school year.
        """
        self._request(
            "PUT",
            f"/api/v1/student/homeworks/{encode_path(homework_id)}/elaboration/done",
            params={"SchoolYearId": school_year_id},
        )

    def delete_elaboration_attachment(
        self, homework_id: str, attachment_id: str, *, school_year_id: str | None = None
    ) -> None:
        """Delete an attachment of a homework elaboration.

        Args:
            homework_id: ID of the homework.
            attachment_id: ID of the attachment.
            school_year_id: ID of the requested school year.
        """
        self._request(
            "DELETE",
            f"/api/v1/student/homeworks/{encode_path(homework_id)}/elaboration/attachments/{encode_path(attachment_id)}",
            params={"SchoolYearId": school_year_id},
        )


class AsyncHomeworks(AsyncAPIResource):
    """Asynchronous endpoints for homeworks."""

    async def list_for_student(
        self,
        student_id: str,
        *,
        school_year_id: str | None = None,
        subject_id: str | None = None,
        date_from: DateLike | None = None,
        date_to: DateLike | None = None,
        filter: HomeworksFilterState | None = None,
        state: HomeworkState | None = None,
        page_number: int | None = None,
        page_size: int | None = None,
    ) -> HomeworksResponse:
        """Return homeworks of a student matching the filter.

        Args:
            student_id: ID of the student.
            school_year_id: ID of the requested school year.
            subject_id: ID of the subject.
            date_from: Start of the date range.
            date_to: End of the date range.
            filter: Filter of the homeworks.
            state: Filter by assignment and due dates.
            page_number: Page number, starting at 1.
            page_size: Page size.

        Returns:
            Homeworks of a student.
        """
        response = await self._request(
            "GET",
            f"/api/v1/students/{encode_path(student_id)}/homeworks",
            params={
                "SchoolYearId": school_year_id,
                "SubjectId": subject_id,
                "DateFrom": date_from,
                "DateTo": date_to,
                "Filter": filter,
                "State": state,
                "Pagination.PageNumber": page_number,
                "Pagination.PageSize": page_size,
            },
        )
        return parse_model(response, HomeworksResponse)

    async def download_assignment_attachment(
        self, attachment_id: str, *, student_id: str, school_year_id: str | None = None
    ) -> DownloadedFile:
        """Download an attachment of a homework assignment.

        Args:
            attachment_id: ID of the attachment.
            student_id: ID of the student.
            school_year_id: ID of the requested school year.

        Returns:
            Downloaded file with its name and content type.
        """
        response = await self._request(
            "GET",
            f"/api/v1/student/homeworks/assignment/attachments/{encode_path(attachment_id)}",
            params={"SchoolYearId": school_year_id, "StudentId": student_id},
        )
        return downloaded_file(response)

    async def download_elaboration_attachment(
        self, attachment_id: str, *, student_id: str, school_year_id: str | None = None
    ) -> DownloadedFile:
        """Download an attachment of a homework elaboration.

        Args:
            attachment_id: ID of the attachment.
            student_id: ID of the student.
            school_year_id: ID of the requested school year.

        Returns:
            Downloaded file with its name and content type.
        """
        response = await self._request(
            "GET",
            f"/api/v1/student/homeworks/elaboration/attachments/{encode_path(attachment_id)}",
            params={"SchoolYearId": school_year_id, "StudentId": student_id},
        )
        return downloaded_file(response)

    async def list_for_teacher(
        self,
        *,
        school_year_id: str | None = None,
        subject_id: str | None = None,
        date_from: DateLike | None = None,
        date_to: DateLike | None = None,
        closed: bool | None = None,
        state: HomeworkTeacherState | None = None,
        page_number: int | None = None,
        page_size: int | None = None,
    ) -> HomeworksTeacherResponse:
        """Return homeworks assigned by the teacher.

        Args:
            school_year_id: ID of the requested school year.
            subject_id: ID of the subject.
            date_from: Start of the date range.
            date_to: End of the date range.
            closed: Include closed homeworks.
            state: Filter of homeworks assigned by a teacher.
            page_number: Page number, starting at 1.
            page_size: Page size.

        Returns:
            Homeworks assigned by a teacher.
        """
        response = await self._request(
            "GET",
            "/api/v1/teacher/homeworks",
            params={
                "SchoolYearId": school_year_id,
                "SubjectId": subject_id,
                "DateFrom": date_from,
                "DateTo": date_to,
                "Closed": closed,
                "State": state,
                "Pagination.PageNumber": page_number,
                "Pagination.PageSize": page_size,
            },
        )
        return parse_model(response, HomeworksTeacherResponse)

    async def code_lists(
        self, *, school_year_id: str | None = None, student_id: str | None = None
    ) -> HomeworkCodeListsResponse:
        """Return the code lists used by the homeworks module.

        Args:
            school_year_id: ID of the school year. Defaults to the current school year.
            student_id: ID of the student. Used by parents.

        Returns:
            Code lists used by the homeworks module.
        """
        response = await self._request(
            "GET",
            "/api/v1/homeWorks/codeLists",
            params={"schoolYearId": school_year_id, "studentId": student_id},
        )
        return parse_model(response, HomeworkCodeListsResponse)

    async def retrieve(
        self, homework_id: str, *, student_id: str | None = None
    ) -> HomeworkResponse:
        """Return a single homework of a student.

        Args:
            homework_id: ID of the homework.
            student_id: ID of the student.

        Returns:
            Single homework of a student.
        """
        response = await self._request(
            "GET",
            f"/api/v1/student/homeworks/{encode_path(homework_id)}",
            params={"studentId": student_id},
        )
        return parse_model(response, HomeworkResponse)

    async def save_elaboration(
        self, homework_id: str, body: PutElaborationRequest
    ) -> None:
        """Submit the elaboration of a homework.

        Args:
            homework_id: ID of the homework.
            body: Elaboration of the homework.
        """
        await self._request(
            "POST",
            f"/api/v1/student/homeworks/{encode_path(homework_id)}/elaboration",
            json=body.to_dict(),
        )

    async def upload_elaboration_attachment(
        self,
        homework_id: str,
        file: FileInput,
        *,
        submit: bool,
        school_year_id: str | None = None,
        display_name: str | None = None,
    ) -> None:
        """Attach a file to the elaboration of a homework.

        Args:
            homework_id: ID of the homework.
            file: File to attach.
            submit: Whether the homework is submitted. False saves it as a work in
                progress.
            school_year_id: ID of the requested school year.
            display_name: File name shown to users.
        """
        await self._request(
            "POST",
            f"/api/v1/student/homeworks/{encode_path(homework_id)}/elaboration/attachments",
            params={
                "SchoolYearId": school_year_id,
                "Submit": submit,
                "NameUser": display_name,
            },
            files=[to_multipart("Data", file)],
        )

    async def mark_done(
        self, homework_id: str, *, school_year_id: str | None = None
    ) -> None:
        """Mark a homework without submission as done.

        Args:
            homework_id: ID of the homework.
            school_year_id: ID of the requested school year.
        """
        await self._request(
            "PUT",
            f"/api/v1/student/homeworks/{encode_path(homework_id)}/elaboration/done",
            params={"SchoolYearId": school_year_id},
        )

    async def delete_elaboration_attachment(
        self, homework_id: str, attachment_id: str, *, school_year_id: str | None = None
    ) -> None:
        """Delete an attachment of a homework elaboration.

        Args:
            homework_id: ID of the homework.
            attachment_id: ID of the attachment.
            school_year_id: ID of the requested school year.
        """
        await self._request(
            "DELETE",
            f"/api/v1/student/homeworks/{encode_path(homework_id)}/elaboration/attachments/{encode_path(attachment_id)}",
            params={"SchoolYearId": school_year_id},
        )

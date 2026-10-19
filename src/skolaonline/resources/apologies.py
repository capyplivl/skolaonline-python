from __future__ import annotations

from typing import Any

from skolaonline.models import (
    ApologyClassesResponse,
    ApologyCodeListsResponse,
    ApologyFilterState,
    ApologyPostData,
    ApologyPutData,
    OkWarningResponse,
    ParentApologiesResponse,
    ParentApologyResponse,
    ReasonsForAbsenceResponse,
    TeacherApologiesResponse,
    TeacherApologyResponse,
)
from skolaonline.resources._base import (
    AsyncAPIResource,
    SyncAPIResource,
    encode_path,
    parse_json,
    parse_model,
)


class Apologies(SyncAPIResource):
    """Endpoints for apologies for absences."""

    def list_times_from(self, student_id: str) -> Any:
        """Return the times from which an absence can be excused.

        Args:
            student_id: ID of the excused child.

        Returns:
            Decoded JSON response, or None when the response is empty.
        """
        response = self._request(
            "GET", f"/api/v1/students/{encode_path(student_id)}/apologies/timesFrom"
        )
        return parse_json(response)

    def list_times_to(self, student_id: str) -> Any:
        """Return the times until which an absence can be excused.

        Args:
            student_id: ID of the excused child.

        Returns:
            Decoded JSON response, or None when the response is empty.
        """
        response = self._request(
            "GET", f"/api/v1/students/{encode_path(student_id)}/apologies/timesTo"
        )
        return parse_json(response)

    def list_teacher_classes(self) -> ApologyClassesResponse:
        """Return current classes where the user is a class teacher or deputy.

        Returns:
            Classes in which the user can process apologies.
        """
        response = self._request("GET", "/api/v1/teacher/apologies/classes")
        return parse_model(response, ApologyClassesResponse)

    def list_absence_reasons(self) -> ReasonsForAbsenceResponse:
        """Return the available reasons for absence.

        Returns:
            Available reasons for absence.
        """
        response = self._request("GET", "/api/v1/apologies/reasonsForAbsence")
        return parse_model(response, ReasonsForAbsenceResponse)

    def list_for_teacher(
        self,
        *,
        state: ApologyFilterState | None = None,
        class_id: str | None = None,
        page_number: int | None = None,
        page_size: int | None = None,
    ) -> TeacherApologiesResponse:
        """Return apologies for classes taught by the user as a class teacher.

        Args:
            state: Filter by apology state.
            class_id: ID of the class. All classes of the user as a class teacher are
                used when omitted.
            page_number: Page number, starting at 1.
            page_size: Page size.

        Returns:
            Apologies in the classes of a class teacher.
        """
        response = self._request(
            "GET",
            "/api/v1/teacher/apologies",
            params={
                "State": state,
                "ClassId": class_id,
                "Pagination.PageNumber": page_number,
                "Pagination.PageSize": page_size,
            },
        )
        return parse_model(response, TeacherApologiesResponse)

    def retrieve_for_teacher(self, apology_id: str) -> TeacherApologyResponse:
        """Return a single apology as seen by a class teacher.

        Args:
            apology_id: ID of the apology.

        Returns:
            Single apology as seen by a class teacher.
        """
        response = self._request(
            "GET", f"/api/v1/teacher/apologies/{encode_path(apology_id)}"
        )
        return parse_model(response, TeacherApologyResponse)

    def list_for_student(
        self,
        student_id: str,
        *,
        state: ApologyFilterState | None = None,
        page_number: int | None = None,
        page_size: int | None = None,
    ) -> ParentApologiesResponse:
        """Return apologies of a child for the current school year.

        Args:
            student_id: ID of the child whose apologies are returned.
            state: Filter by apology state.
            page_number: Page number, starting at 1.
            page_size: Page size.

        Returns:
            Apologies of a child.
        """
        response = self._request(
            "GET",
            f"/api/v1/students/{encode_path(student_id)}/apologies",
            params={
                "State": state,
                "Pagination.PageNumber": page_number,
                "Pagination.PageSize": page_size,
            },
        )
        return parse_model(response, ParentApologiesResponse)

    def retrieve_for_student(self, apology_id: str) -> ParentApologyResponse:
        """Return a single apology as seen by a parent or student.

        Args:
            apology_id: ID of the apology.

        Returns:
            Single apology of a child.
        """
        response = self._request(
            "GET", f"/api/v1/student/apologies/{encode_path(apology_id)}"
        )
        return parse_model(response, ParentApologyResponse)

    def retrieve_rejection_reason(self, apology_id: str) -> Any:
        """Return the reason an apology was rejected.

        Args:
            apology_id: ID of the apology.

        Returns:
            Decoded JSON response, or None when the response is empty.
        """
        response = self._request(
            "GET", f"/api/v1/apologies/{encode_path(apology_id)}/rejectionReason"
        )
        return parse_json(response)

    def update_rejection_reason(
        self, apology_id: str, reason: str
    ) -> OkWarningResponse:
        """Change the reason an apology was rejected.

        Args:
            apology_id: ID of the apology.
            reason: Reason for rejecting the apology.

        Returns:
            Successful result that may contain a warning for the user.
        """
        response = self._request(
            "PUT",
            f"/api/v1/apologies/{encode_path(apology_id)}/rejectionReason",
            json=reason,
        )
        return parse_model(response, OkWarningResponse)

    def code_lists(
        self, *, school_year_id: str | None = None, student_id: str | None = None
    ) -> ApologyCodeListsResponse:
        """Return the code lists used by the apologies module.

        Args:
            school_year_id: ID of the school year. Defaults to the current school year.
            student_id: ID of the student. Used by parents.

        Returns:
            Code lists used by the apologies module.
        """
        response = self._request(
            "GET",
            "/api/v1/apologies/codeLists",
            params={"schoolYearId": school_year_id, "studentId": student_id},
        )
        return parse_model(response, ApologyCodeListsResponse)

    def create(self, body: ApologyPostData) -> Any:
        """Create a new apology for a child.

        Args:
            body: Data of the new apology.

        Returns:
            Decoded JSON response, or None when the response is empty.
        """
        response = self._request("POST", "/api/v1/apologies", json=body.to_dict())
        return parse_json(response)

    def accept(self, apology_id: str, *, absence_reason: str | None = None) -> Any:
        """Accept an apology, optionally recording the absence reason.

        Args:
            apology_id: ID of the apology to accept.
            absence_reason: Reason for absence filled in by the teacher. At most 100
                characters.

        Returns:
            Decoded JSON response, or None when the response is empty.
        """
        response = self._request(
            "PUT",
            f"/api/v1/apologies/{encode_path(apology_id)}/accept",
            json=absence_reason,
        )
        return parse_json(response)

    def reject(self, apology_id: str, reason: str) -> OkWarningResponse:
        """Reject an apology with the given reason.

        Args:
            apology_id: ID of the apology to reject.
            reason: Reason for rejecting the apology. At most 500 characters.

        Returns:
            Successful result that may contain a warning for the user.
        """
        response = self._request(
            "PUT", f"/api/v1/apologies/{encode_path(apology_id)}/reject", json=reason
        )
        return parse_model(response, OkWarningResponse)

    def cancel_rejection(self, apology_id: str) -> Any:
        """Cancel the rejection of an apology.

        Args:
            apology_id: ID of the apology whose rejection is canceled.

        Returns:
            Decoded JSON response, or None when the response is empty.
        """
        response = self._request(
            "PUT", f"/api/v1/apologies/{encode_path(apology_id)}/cancelRejection"
        )
        return parse_json(response)

    def update(self, apology_id: str, body: ApologyPutData) -> Any:
        """Update an existing apology.

        Args:
            apology_id: ID of the apology to update.
            body: Updated data of the apology.

        Returns:
            Decoded JSON response, or None when the response is empty.
        """
        response = self._request(
            "PUT", f"/api/v1/apologies/{encode_path(apology_id)}", json=body.to_dict()
        )
        return parse_json(response)

    def delete(self, apology_id: str) -> Any:
        """Delete an apology.

        Args:
            apology_id: ID of the apology to delete.

        Returns:
            Decoded JSON response, or None when the response is empty.
        """
        response = self._request(
            "DELETE", f"/api/v1/apologies/{encode_path(apology_id)}"
        )
        return parse_json(response)


class AsyncApologies(AsyncAPIResource):
    """Asynchronous endpoints for apologies for absences."""

    async def list_times_from(self, student_id: str) -> Any:
        """Return the times from which an absence can be excused.

        Args:
            student_id: ID of the excused child.

        Returns:
            Decoded JSON response, or None when the response is empty.
        """
        response = await self._request(
            "GET", f"/api/v1/students/{encode_path(student_id)}/apologies/timesFrom"
        )
        return parse_json(response)

    async def list_times_to(self, student_id: str) -> Any:
        """Return the times until which an absence can be excused.

        Args:
            student_id: ID of the excused child.

        Returns:
            Decoded JSON response, or None when the response is empty.
        """
        response = await self._request(
            "GET", f"/api/v1/students/{encode_path(student_id)}/apologies/timesTo"
        )
        return parse_json(response)

    async def list_teacher_classes(self) -> ApologyClassesResponse:
        """Return current classes where the user is a class teacher or deputy.

        Returns:
            Classes in which the user can process apologies.
        """
        response = await self._request("GET", "/api/v1/teacher/apologies/classes")
        return parse_model(response, ApologyClassesResponse)

    async def list_absence_reasons(self) -> ReasonsForAbsenceResponse:
        """Return the available reasons for absence.

        Returns:
            Available reasons for absence.
        """
        response = await self._request("GET", "/api/v1/apologies/reasonsForAbsence")
        return parse_model(response, ReasonsForAbsenceResponse)

    async def list_for_teacher(
        self,
        *,
        state: ApologyFilterState | None = None,
        class_id: str | None = None,
        page_number: int | None = None,
        page_size: int | None = None,
    ) -> TeacherApologiesResponse:
        """Return apologies for classes taught by the user as a class teacher.

        Args:
            state: Filter by apology state.
            class_id: ID of the class. All classes of the user as a class teacher are
                used when omitted.
            page_number: Page number, starting at 1.
            page_size: Page size.

        Returns:
            Apologies in the classes of a class teacher.
        """
        response = await self._request(
            "GET",
            "/api/v1/teacher/apologies",
            params={
                "State": state,
                "ClassId": class_id,
                "Pagination.PageNumber": page_number,
                "Pagination.PageSize": page_size,
            },
        )
        return parse_model(response, TeacherApologiesResponse)

    async def retrieve_for_teacher(self, apology_id: str) -> TeacherApologyResponse:
        """Return a single apology as seen by a class teacher.

        Args:
            apology_id: ID of the apology.

        Returns:
            Single apology as seen by a class teacher.
        """
        response = await self._request(
            "GET", f"/api/v1/teacher/apologies/{encode_path(apology_id)}"
        )
        return parse_model(response, TeacherApologyResponse)

    async def list_for_student(
        self,
        student_id: str,
        *,
        state: ApologyFilterState | None = None,
        page_number: int | None = None,
        page_size: int | None = None,
    ) -> ParentApologiesResponse:
        """Return apologies of a child for the current school year.

        Args:
            student_id: ID of the child whose apologies are returned.
            state: Filter by apology state.
            page_number: Page number, starting at 1.
            page_size: Page size.

        Returns:
            Apologies of a child.
        """
        response = await self._request(
            "GET",
            f"/api/v1/students/{encode_path(student_id)}/apologies",
            params={
                "State": state,
                "Pagination.PageNumber": page_number,
                "Pagination.PageSize": page_size,
            },
        )
        return parse_model(response, ParentApologiesResponse)

    async def retrieve_for_student(self, apology_id: str) -> ParentApologyResponse:
        """Return a single apology as seen by a parent or student.

        Args:
            apology_id: ID of the apology.

        Returns:
            Single apology of a child.
        """
        response = await self._request(
            "GET", f"/api/v1/student/apologies/{encode_path(apology_id)}"
        )
        return parse_model(response, ParentApologyResponse)

    async def retrieve_rejection_reason(self, apology_id: str) -> Any:
        """Return the reason an apology was rejected.

        Args:
            apology_id: ID of the apology.

        Returns:
            Decoded JSON response, or None when the response is empty.
        """
        response = await self._request(
            "GET", f"/api/v1/apologies/{encode_path(apology_id)}/rejectionReason"
        )
        return parse_json(response)

    async def update_rejection_reason(
        self, apology_id: str, reason: str
    ) -> OkWarningResponse:
        """Change the reason an apology was rejected.

        Args:
            apology_id: ID of the apology.
            reason: Reason for rejecting the apology.

        Returns:
            Successful result that may contain a warning for the user.
        """
        response = await self._request(
            "PUT",
            f"/api/v1/apologies/{encode_path(apology_id)}/rejectionReason",
            json=reason,
        )
        return parse_model(response, OkWarningResponse)

    async def code_lists(
        self, *, school_year_id: str | None = None, student_id: str | None = None
    ) -> ApologyCodeListsResponse:
        """Return the code lists used by the apologies module.

        Args:
            school_year_id: ID of the school year. Defaults to the current school year.
            student_id: ID of the student. Used by parents.

        Returns:
            Code lists used by the apologies module.
        """
        response = await self._request(
            "GET",
            "/api/v1/apologies/codeLists",
            params={"schoolYearId": school_year_id, "studentId": student_id},
        )
        return parse_model(response, ApologyCodeListsResponse)

    async def create(self, body: ApologyPostData) -> Any:
        """Create a new apology for a child.

        Args:
            body: Data of the new apology.

        Returns:
            Decoded JSON response, or None when the response is empty.
        """
        response = await self._request("POST", "/api/v1/apologies", json=body.to_dict())
        return parse_json(response)

    async def accept(
        self, apology_id: str, *, absence_reason: str | None = None
    ) -> Any:
        """Accept an apology, optionally recording the absence reason.

        Args:
            apology_id: ID of the apology to accept.
            absence_reason: Reason for absence filled in by the teacher. At most 100
                characters.

        Returns:
            Decoded JSON response, or None when the response is empty.
        """
        response = await self._request(
            "PUT",
            f"/api/v1/apologies/{encode_path(apology_id)}/accept",
            json=absence_reason,
        )
        return parse_json(response)

    async def reject(self, apology_id: str, reason: str) -> OkWarningResponse:
        """Reject an apology with the given reason.

        Args:
            apology_id: ID of the apology to reject.
            reason: Reason for rejecting the apology. At most 500 characters.

        Returns:
            Successful result that may contain a warning for the user.
        """
        response = await self._request(
            "PUT", f"/api/v1/apologies/{encode_path(apology_id)}/reject", json=reason
        )
        return parse_model(response, OkWarningResponse)

    async def cancel_rejection(self, apology_id: str) -> Any:
        """Cancel the rejection of an apology.

        Args:
            apology_id: ID of the apology whose rejection is canceled.

        Returns:
            Decoded JSON response, or None when the response is empty.
        """
        response = await self._request(
            "PUT", f"/api/v1/apologies/{encode_path(apology_id)}/cancelRejection"
        )
        return parse_json(response)

    async def update(self, apology_id: str, body: ApologyPutData) -> Any:
        """Update an existing apology.

        Args:
            apology_id: ID of the apology to update.
            body: Updated data of the apology.

        Returns:
            Decoded JSON response, or None when the response is empty.
        """
        response = await self._request(
            "PUT", f"/api/v1/apologies/{encode_path(apology_id)}", json=body.to_dict()
        )
        return parse_json(response)

    async def delete(self, apology_id: str) -> Any:
        """Delete an apology.

        Args:
            apology_id: ID of the apology to delete.

        Returns:
            Decoded JSON response, or None when the response is empty.
        """
        response = await self._request(
            "DELETE", f"/api/v1/apologies/{encode_path(apology_id)}"
        )
        return parse_json(response)

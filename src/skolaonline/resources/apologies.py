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
    def list_times_from(self, student_id: str) -> Any:
        """Return the times from which an absence can be excused."""
        response = self._request(
            "GET", f"/api/v1/students/{encode_path(student_id)}/apologies/timesFrom"
        )
        return parse_json(response)

    def list_times_to(self, student_id: str) -> Any:
        """Return the times until which an absence can be excused."""
        response = self._request(
            "GET", f"/api/v1/students/{encode_path(student_id)}/apologies/timesTo"
        )
        return parse_json(response)

    def list_teacher_classes(self) -> ApologyClassesResponse:
        """Return current classes where the user is a class teacher or deputy."""
        response = self._request("GET", "/api/v1/teacher/apologies/classes")
        return parse_model(response, ApologyClassesResponse)

    def list_absence_reasons(self) -> ReasonsForAbsenceResponse:
        """Return the available reasons for absence."""
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
        """Return apologies for classes taught by the user as a class teacher."""
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
        """Return a single apology as seen by a class teacher."""
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
        """Return apologies of a child for the current school year."""
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
        """Return a single apology as seen by a parent or student."""
        response = self._request(
            "GET", f"/api/v1/student/apologies/{encode_path(apology_id)}"
        )
        return parse_model(response, ParentApologyResponse)

    def retrieve_rejection_reason(self, apology_id: str) -> Any:
        """Return the reason an apology was rejected."""
        response = self._request(
            "GET", f"/api/v1/apologies/{encode_path(apology_id)}/rejectionReason"
        )
        return parse_json(response)

    def update_rejection_reason(
        self, apology_id: str, reason: str
    ) -> OkWarningResponse:
        """Change the reason an apology was rejected."""
        response = self._request(
            "PUT",
            f"/api/v1/apologies/{encode_path(apology_id)}/rejectionReason",
            json=reason,
        )
        return parse_model(response, OkWarningResponse)

    def code_lists(
        self, *, school_year_id: str | None = None, student_id: str | None = None
    ) -> ApologyCodeListsResponse:
        """Return the code lists used by the apologies module."""
        response = self._request(
            "GET",
            "/api/v1/apologies/codeLists",
            params={"schoolYearId": school_year_id, "studentId": student_id},
        )
        return parse_model(response, ApologyCodeListsResponse)

    def create(self, body: ApologyPostData) -> Any:
        """Create a new apology for a child."""
        response = self._request("POST", "/api/v1/apologies", json=body.to_dict())
        return parse_json(response)

    def accept(self, apology_id: str, *, absence_reason: str | None = None) -> Any:
        """Accept an apology, optionally recording the absence reason."""
        response = self._request(
            "PUT",
            f"/api/v1/apologies/{encode_path(apology_id)}/accept",
            json=absence_reason,
        )
        return parse_json(response)

    def reject(self, apology_id: str, reason: str) -> OkWarningResponse:
        """Reject an apology with the given reason."""
        response = self._request(
            "PUT", f"/api/v1/apologies/{encode_path(apology_id)}/reject", json=reason
        )
        return parse_model(response, OkWarningResponse)

    def cancel_rejection(self, apology_id: str) -> Any:
        """Cancel the rejection of an apology."""
        response = self._request(
            "PUT", f"/api/v1/apologies/{encode_path(apology_id)}/cancelRejection"
        )
        return parse_json(response)

    def update(self, apology_id: str, body: ApologyPutData) -> Any:
        """Update an existing apology."""
        response = self._request(
            "PUT", f"/api/v1/apologies/{encode_path(apology_id)}", json=body.to_dict()
        )
        return parse_json(response)

    def delete(self, apology_id: str) -> Any:
        """Delete an apology."""
        response = self._request(
            "DELETE", f"/api/v1/apologies/{encode_path(apology_id)}"
        )
        return parse_json(response)


class AsyncApologies(AsyncAPIResource):
    async def list_times_from(self, student_id: str) -> Any:
        """Return the times from which an absence can be excused."""
        response = await self._request(
            "GET", f"/api/v1/students/{encode_path(student_id)}/apologies/timesFrom"
        )
        return parse_json(response)

    async def list_times_to(self, student_id: str) -> Any:
        """Return the times until which an absence can be excused."""
        response = await self._request(
            "GET", f"/api/v1/students/{encode_path(student_id)}/apologies/timesTo"
        )
        return parse_json(response)

    async def list_teacher_classes(self) -> ApologyClassesResponse:
        """Return current classes where the user is a class teacher or deputy."""
        response = await self._request("GET", "/api/v1/teacher/apologies/classes")
        return parse_model(response, ApologyClassesResponse)

    async def list_absence_reasons(self) -> ReasonsForAbsenceResponse:
        """Return the available reasons for absence."""
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
        """Return apologies for classes taught by the user as a class teacher."""
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
        """Return a single apology as seen by a class teacher."""
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
        """Return apologies of a child for the current school year."""
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
        """Return a single apology as seen by a parent or student."""
        response = await self._request(
            "GET", f"/api/v1/student/apologies/{encode_path(apology_id)}"
        )
        return parse_model(response, ParentApologyResponse)

    async def retrieve_rejection_reason(self, apology_id: str) -> Any:
        """Return the reason an apology was rejected."""
        response = await self._request(
            "GET", f"/api/v1/apologies/{encode_path(apology_id)}/rejectionReason"
        )
        return parse_json(response)

    async def update_rejection_reason(
        self, apology_id: str, reason: str
    ) -> OkWarningResponse:
        """Change the reason an apology was rejected."""
        response = await self._request(
            "PUT",
            f"/api/v1/apologies/{encode_path(apology_id)}/rejectionReason",
            json=reason,
        )
        return parse_model(response, OkWarningResponse)

    async def code_lists(
        self, *, school_year_id: str | None = None, student_id: str | None = None
    ) -> ApologyCodeListsResponse:
        """Return the code lists used by the apologies module."""
        response = await self._request(
            "GET",
            "/api/v1/apologies/codeLists",
            params={"schoolYearId": school_year_id, "studentId": student_id},
        )
        return parse_model(response, ApologyCodeListsResponse)

    async def create(self, body: ApologyPostData) -> Any:
        """Create a new apology for a child."""
        response = await self._request("POST", "/api/v1/apologies", json=body.to_dict())
        return parse_json(response)

    async def accept(
        self, apology_id: str, *, absence_reason: str | None = None
    ) -> Any:
        """Accept an apology, optionally recording the absence reason."""
        response = await self._request(
            "PUT",
            f"/api/v1/apologies/{encode_path(apology_id)}/accept",
            json=absence_reason,
        )
        return parse_json(response)

    async def reject(self, apology_id: str, reason: str) -> OkWarningResponse:
        """Reject an apology with the given reason."""
        response = await self._request(
            "PUT", f"/api/v1/apologies/{encode_path(apology_id)}/reject", json=reason
        )
        return parse_model(response, OkWarningResponse)

    async def cancel_rejection(self, apology_id: str) -> Any:
        """Cancel the rejection of an apology."""
        response = await self._request(
            "PUT", f"/api/v1/apologies/{encode_path(apology_id)}/cancelRejection"
        )
        return parse_json(response)

    async def update(self, apology_id: str, body: ApologyPutData) -> Any:
        """Update an existing apology."""
        response = await self._request(
            "PUT", f"/api/v1/apologies/{encode_path(apology_id)}", json=body.to_dict()
        )
        return parse_json(response)

    async def delete(self, apology_id: str) -> Any:
        """Delete an apology."""
        response = await self._request(
            "DELETE", f"/api/v1/apologies/{encode_path(apology_id)}"
        )
        return parse_json(response)

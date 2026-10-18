from __future__ import annotations

from skolaonline._types import DateLike
from skolaonline.models import (
    AbsenceCodeListsResponse,
    AbsenceInDayResponse,
    AbsenceInPeriodFilterState,
    AbsenceInPeriodResponse,
    AbsenceInSubjectFilterOrder,
    AbsenceInSubjectResponse,
)
from skolaonline.resources._base import (
    AsyncAPIResource,
    SyncAPIResource,
    parse_model,
)


class Absences(SyncAPIResource):
    def code_lists(
        self, *, school_year_id: str | None = None
    ) -> AbsenceCodeListsResponse:
        """Return the code lists used by the absences module."""
        response = self._request(
            "GET", "/api/v1/absences/codeLists", params={"schoolYearId": school_year_id}
        )
        return parse_model(response, AbsenceCodeListsResponse)

    def list_in_period(
        self,
        *,
        date_from: DateLike,
        date_to: DateLike,
        state: AbsenceInPeriodFilterState | None = None,
        student_id: str | None = None,
    ) -> AbsenceInPeriodResponse:
        """Return absences in a date range for the user or the given child."""
        response = self._request(
            "GET",
            "/api/v1/absences/inPeriod",
            params={
                "State": state,
                "DateFrom": date_from,
                "DateTo": date_to,
                "studentId": student_id,
            },
        )
        return parse_model(response, AbsenceInPeriodResponse)

    def list_in_day(
        self, *, date: DateLike, student_id: str | None = None
    ) -> AbsenceInDayResponse:
        """Return absences on a single day for the user or the given child."""
        response = self._request(
            "GET",
            "/api/v1/absences/inDay",
            params={"Date": date, "studentId": student_id},
        )
        return parse_model(response, AbsenceInDayResponse)

    def list_by_subject(
        self,
        *,
        date_from: DateLike,
        date_to: DateLike,
        sort: AbsenceInSubjectFilterOrder | None = None,
        student_id: str | None = None,
    ) -> AbsenceInSubjectResponse:
        """Return absences grouped by subject for the user or the given child."""
        response = self._request(
            "GET",
            "/api/v1/absences/inSubject",
            params={
                "DateFrom": date_from,
                "DateTo": date_to,
                "Sort": sort,
                "studentId": student_id,
            },
        )
        return parse_model(response, AbsenceInSubjectResponse)


class AsyncAbsences(AsyncAPIResource):
    async def code_lists(
        self, *, school_year_id: str | None = None
    ) -> AbsenceCodeListsResponse:
        """Return the code lists used by the absences module."""
        response = await self._request(
            "GET", "/api/v1/absences/codeLists", params={"schoolYearId": school_year_id}
        )
        return parse_model(response, AbsenceCodeListsResponse)

    async def list_in_period(
        self,
        *,
        date_from: DateLike,
        date_to: DateLike,
        state: AbsenceInPeriodFilterState | None = None,
        student_id: str | None = None,
    ) -> AbsenceInPeriodResponse:
        """Return absences in a date range for the user or the given child."""
        response = await self._request(
            "GET",
            "/api/v1/absences/inPeriod",
            params={
                "State": state,
                "DateFrom": date_from,
                "DateTo": date_to,
                "studentId": student_id,
            },
        )
        return parse_model(response, AbsenceInPeriodResponse)

    async def list_in_day(
        self, *, date: DateLike, student_id: str | None = None
    ) -> AbsenceInDayResponse:
        """Return absences on a single day for the user or the given child."""
        response = await self._request(
            "GET",
            "/api/v1/absences/inDay",
            params={"Date": date, "studentId": student_id},
        )
        return parse_model(response, AbsenceInDayResponse)

    async def list_by_subject(
        self,
        *,
        date_from: DateLike,
        date_to: DateLike,
        sort: AbsenceInSubjectFilterOrder | None = None,
        student_id: str | None = None,
    ) -> AbsenceInSubjectResponse:
        """Return absences grouped by subject for the user or the given child."""
        response = await self._request(
            "GET",
            "/api/v1/absences/inSubject",
            params={
                "DateFrom": date_from,
                "DateTo": date_to,
                "Sort": sort,
                "studentId": student_id,
            },
        )
        return parse_model(response, AbsenceInSubjectResponse)

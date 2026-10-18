from __future__ import annotations

from collections.abc import Sequence

from skolaonline._types import DateLike
from skolaonline.models import (
    AdditionalDataDefinitionResponse,
    DataInterfaceClassesResponse,
    StudentsListResponse,
    StudentsResponse,
    StudentsWithConsentResponse,
)
from skolaonline.resources._base import (
    AsyncAPIResource,
    SyncAPIResource,
    encode_path,
    parse_model,
)


class DataInterface(SyncAPIResource):
    def list_students_with_consent(
        self, consent_id: str
    ) -> StudentsWithConsentResponse:
        """Return students who granted the given consent."""
        response = self._request(
            "GET", f"/if/2/gdpr/studentsWithConsent/{encode_path(consent_id)}"
        )
        return parse_model(response, StudentsWithConsentResponse)

    def list_students(self) -> StudentsResponse:
        """Return all students of the organization."""
        response = self._request("GET", "/if/2/common/students")
        return parse_model(response, StudentsResponse)

    def list_classes(self) -> DataInterfaceClassesResponse:
        """Return all classes of the organization."""
        response = self._request("GET", "/if/2/common/classes")
        return parse_model(response, DataInterfaceClassesResponse)

    def list_student_records(
        self,
        *,
        date: DateLike | None = None,
        additional_data: Sequence[str] | None = None,
    ) -> StudentsListResponse:
        """Return student records valid on a date with optional additional data."""
        response = self._request(
            "GET", "/zaci", params={"datum": date, "dalsiUdaje": additional_data}
        )
        return parse_model(response, StudentsListResponse)

    def list_additional_data_definitions(self) -> AdditionalDataDefinitionResponse:
        """Return definitions of the additional student data."""
        response = self._request("GET", "/zaci/dalsiUdaje")
        return parse_model(response, AdditionalDataDefinitionResponse)


class AsyncDataInterface(AsyncAPIResource):
    async def list_students_with_consent(
        self, consent_id: str
    ) -> StudentsWithConsentResponse:
        """Return students who granted the given consent."""
        response = await self._request(
            "GET", f"/if/2/gdpr/studentsWithConsent/{encode_path(consent_id)}"
        )
        return parse_model(response, StudentsWithConsentResponse)

    async def list_students(self) -> StudentsResponse:
        """Return all students of the organization."""
        response = await self._request("GET", "/if/2/common/students")
        return parse_model(response, StudentsResponse)

    async def list_classes(self) -> DataInterfaceClassesResponse:
        """Return all classes of the organization."""
        response = await self._request("GET", "/if/2/common/classes")
        return parse_model(response, DataInterfaceClassesResponse)

    async def list_student_records(
        self,
        *,
        date: DateLike | None = None,
        additional_data: Sequence[str] | None = None,
    ) -> StudentsListResponse:
        """Return student records valid on a date with optional additional data."""
        response = await self._request(
            "GET", "/zaci", params={"datum": date, "dalsiUdaje": additional_data}
        )
        return parse_model(response, StudentsListResponse)

    async def list_additional_data_definitions(
        self,
    ) -> AdditionalDataDefinitionResponse:
        """Return definitions of the additional student data."""
        response = await self._request("GET", "/zaci/dalsiUdaje")
        return parse_model(response, AdditionalDataDefinitionResponse)

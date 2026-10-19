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
    """Endpoints for the data interface for system integrations."""

    def list_students_with_consent(
        self, consent_id: str
    ) -> StudentsWithConsentResponse:
        """Return students who granted the given consent.

        Args:
            consent_id: ID of the consent.

        Returns:
            List of students who granted a consent.
        """
        response = self._request(
            "GET", f"/if/2/gdpr/studentsWithConsent/{encode_path(consent_id)}"
        )
        return parse_model(response, StudentsWithConsentResponse)

    def list_students(self) -> StudentsResponse:
        """Return all students of the organization.

        Returns:
            List of students.
        """
        response = self._request("GET", "/if/2/common/students")
        return parse_model(response, StudentsResponse)

    def list_classes(self) -> DataInterfaceClassesResponse:
        """Return all classes of the organization.

        Returns:
            List of classes.
        """
        response = self._request("GET", "/if/2/common/classes")
        return parse_model(response, DataInterfaceClassesResponse)

    def list_student_records(
        self,
        *,
        date: DateLike | None = None,
        additional_data: Sequence[str] | None = None,
    ) -> StudentsListResponse:
        """Return student records valid on a date with optional additional data.

        Args:
            date: Date the records are valid on. Defaults to today.
            additional_data: Names of additional data items to include, as returned by
                list_additional_data_definitions.

        Returns:
            Student records.
        """
        response = self._request(
            "GET", "/zaci", params={"datum": date, "dalsiUdaje": additional_data}
        )
        return parse_model(response, StudentsListResponse)

    def list_additional_data_definitions(self) -> AdditionalDataDefinitionResponse:
        """Return definitions of the additional student data.

        Returns:
            Definitions of additional student data.
        """
        response = self._request("GET", "/zaci/dalsiUdaje")
        return parse_model(response, AdditionalDataDefinitionResponse)


class AsyncDataInterface(AsyncAPIResource):
    """Asynchronous endpoints for the data interface for system integrations."""

    async def list_students_with_consent(
        self, consent_id: str
    ) -> StudentsWithConsentResponse:
        """Return students who granted the given consent.

        Args:
            consent_id: ID of the consent.

        Returns:
            List of students who granted a consent.
        """
        response = await self._request(
            "GET", f"/if/2/gdpr/studentsWithConsent/{encode_path(consent_id)}"
        )
        return parse_model(response, StudentsWithConsentResponse)

    async def list_students(self) -> StudentsResponse:
        """Return all students of the organization.

        Returns:
            List of students.
        """
        response = await self._request("GET", "/if/2/common/students")
        return parse_model(response, StudentsResponse)

    async def list_classes(self) -> DataInterfaceClassesResponse:
        """Return all classes of the organization.

        Returns:
            List of classes.
        """
        response = await self._request("GET", "/if/2/common/classes")
        return parse_model(response, DataInterfaceClassesResponse)

    async def list_student_records(
        self,
        *,
        date: DateLike | None = None,
        additional_data: Sequence[str] | None = None,
    ) -> StudentsListResponse:
        """Return student records valid on a date with optional additional data.

        Args:
            date: Date the records are valid on. Defaults to today.
            additional_data: Names of additional data items to include, as returned by
                list_additional_data_definitions.

        Returns:
            Student records.
        """
        response = await self._request(
            "GET", "/zaci", params={"datum": date, "dalsiUdaje": additional_data}
        )
        return parse_model(response, StudentsListResponse)

    async def list_additional_data_definitions(
        self,
    ) -> AdditionalDataDefinitionResponse:
        """Return definitions of the additional student data.

        Returns:
            Definitions of additional student data.
        """
        response = await self._request("GET", "/zaci/dalsiUdaje")
        return parse_model(response, AdditionalDataDefinitionResponse)

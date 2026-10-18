from __future__ import annotations

from skolaonline._types import DateLike
from skolaonline.models import (
    BehaviorClassesResponse,
    BehaviorCodeListsResponse,
    BehaviorOrder,
    BehaviorsResponse,
    ClassStatus,
    KindsOfBehaviorEvaluationsResponse,
    KindsOfEducationalMeasuresResponse,
    KindsOfNotesClassBookResponse,
    PostBehaviorRequest,
    PutBehaviorRequest,
    PutMultipleSignBehaviorsRequest,
    ReasonsOfEducationalMeasuresResponse,
    RecordsFilter,
    StudentBehaviorResponse,
    StudentBehaviorsResponse,
    StudentsOfClassResponse,
    TypesOfBehaviorResponse,
)
from skolaonline.resources._base import (
    AsyncAPIResource,
    SyncAPIResource,
    encode_path,
    parse_model,
)


class Behaviors(SyncAPIResource):
    def list_types(self) -> TypesOfBehaviorResponse:
        """Return the types of behavior records."""
        response = self._request("GET", "/api/v1/behaviors/typesOfBehavior")
        return parse_model(response, TypesOfBehaviorResponse)

    def list_note_kinds(
        self,
        *,
        kind_id: str | None = None,
        only_valid: bool | None = None,
        only_positive: bool | None = None,
        only_negative: bool | None = None,
    ) -> KindsOfNotesClassBookResponse:
        """Return the kinds of class book notes."""
        response = self._request(
            "GET",
            "/api/v1/behaviors/kindsOfNotesClassBook",
            params={
                "KindId": kind_id,
                "OnlyValid": only_valid,
                "OnlyPositive": only_positive,
                "OnlyNegative": only_negative,
            },
        )
        return parse_model(response, KindsOfNotesClassBookResponse)

    def list_educational_measure_kinds(
        self,
        *,
        kind_id: str | None = None,
        only_valid: bool | None = None,
        only_positive: bool | None = None,
        only_negative: bool | None = None,
    ) -> KindsOfEducationalMeasuresResponse:
        """Return the kinds of educational measures."""
        response = self._request(
            "GET",
            "/api/v1/behaviors/kindsOfEducationalMeasures",
            params={
                "KindId": kind_id,
                "OnlyValid": only_valid,
                "OnlyPositive": only_positive,
                "OnlyNegative": only_negative,
            },
        )
        return parse_model(response, KindsOfEducationalMeasuresResponse)

    def list_educational_measure_reasons(
        self,
        *,
        reason_id: str | None = None,
        search: str | None = None,
        only_valid: bool | None = None,
        only_positive: bool | None = None,
        only_negative: bool | None = None,
    ) -> ReasonsOfEducationalMeasuresResponse:
        """Return the reasons available for educational measures."""
        response = self._request(
            "GET",
            "/api/v1/teacher/behaviors/reasonsOfEducationalMeasures",
            params={
                "ReasonId": reason_id,
                "Search": search,
                "OnlyValid": only_valid,
                "OnlyPositive": only_positive,
                "OnlyNegative": only_negative,
            },
        )
        return parse_model(response, ReasonsOfEducationalMeasuresResponse)

    def list_evaluation_kinds(
        self, *, kind_id: str | None = None, school_year_id: str | None = None
    ) -> KindsOfBehaviorEvaluationsResponse:
        """Return the kinds of behavior evaluations."""
        response = self._request(
            "GET",
            "/api/v1/behaviors/kindsOfBehaviorEvaluations",
            params={"KindId": kind_id, "SchoolYearId": school_year_id},
        )
        return parse_model(response, KindsOfBehaviorEvaluationsResponse)

    def list_teacher_classes(
        self, *, class_status: ClassStatus, school_year_id: str | None = None
    ) -> BehaviorClassesResponse:
        """Return elementary and higher classes of the requested school year."""
        response = self._request(
            "GET",
            "/api/v1/teacher/behaviors/classes",
            params={"SenderPersonType": class_status, "SchoolYearId": school_year_id},
        )
        return parse_model(response, BehaviorClassesResponse)

    def list_students_of_class(
        self,
        *,
        class_id: str,
        school_year_id: str | None = None,
        to_date: DateLike | None = None,
    ) -> StudentsOfClassResponse:
        """Return the students of a class on a given date."""
        response = self._request(
            "GET",
            "/api/v1/teacher/behaviors/studentsOfClass",
            params={
                "ClassId": class_id,
                "SchoolYearId": school_year_id,
                "ToDate": to_date,
            },
        )
        return parse_model(response, StudentsOfClassResponse)

    def list_for_teacher(
        self,
        *,
        school_year_id: str | None = None,
        from_date: DateLike | None = None,
        to_date: DateLike | None = None,
        class_id: str | None = None,
        student_id: str | None = None,
        type_of_behavior_id: str | None = None,
        kind_of_notes_class_book_id: str | None = None,
        kind_of_educational_measures_id: str | None = None,
        kind_of_behavior_evaluations_id: str | None = None,
        order_by: BehaviorOrder | None = None,
        search: str | None = None,
        page_number: int | None = None,
        page_size: int | None = None,
    ) -> BehaviorsResponse:
        """Return behavior records of students matching the filter."""
        response = self._request(
            "GET",
            "/api/v1/teacher/behaviors",
            params={
                "SchoolYearId": school_year_id,
                "FromDate": from_date,
                "ToDate": to_date,
                "ClassId": class_id,
                "StudentId": student_id,
                "TypeOfBehaviorId": type_of_behavior_id,
                "KindOfNotesClassBookId": kind_of_notes_class_book_id,
                "KindOfEducationalMeasuresId": kind_of_educational_measures_id,
                "KindOfBehaviorEvaluationsId": kind_of_behavior_evaluations_id,
                "OrderBy": order_by,
                "Search": search,
                "Pagination.PageNumber": page_number,
                "Pagination.PageSize": page_size,
            },
        )
        return parse_model(response, BehaviorsResponse)

    def create(self, body: PostBehaviorRequest) -> None:
        """Create a new behavior record."""
        self._request("POST", "/api/v1/teacher/behaviors", json=body.to_dict())

    def list_for_student(
        self,
        student_id: str,
        *,
        school_year_id: str | None = None,
        from_date: DateLike | None = None,
        to_date: DateLike | None = None,
        type_of_behavior_id: str | None = None,
        kind_of_notes_class_book_id: str | None = None,
        kind_of_educational_measures_id: str | None = None,
        kind_of_behavior_evaluations_id: str | None = None,
        page_number: int | None = None,
        page_size: int | None = None,
        search: str | None = None,
        records_filter: RecordsFilter | None = None,
    ) -> StudentBehaviorsResponse:
        """Return behavior records of a student matching the filter."""
        response = self._request(
            "GET",
            f"/api/v1/students/{encode_path(student_id)}/behaviors",
            params={
                "SchoolYearId": school_year_id,
                "FromDate": from_date,
                "ToDate": to_date,
                "TypeOfBehaviorId": type_of_behavior_id,
                "KindOfNotesClassBookId": kind_of_notes_class_book_id,
                "KindOfEducationalMeasuresId": kind_of_educational_measures_id,
                "KindOfBehaviorEvaluationsId": kind_of_behavior_evaluations_id,
                "Pagination.PageNumber": page_number,
                "Pagination.PageSize": page_size,
                "Search": search,
                "RecordsFilter": records_filter,
            },
        )
        return parse_model(response, StudentBehaviorsResponse)

    def retrieve(
        self,
        behavior_id: str,
        *,
        school_year_id: str,
        type_of_behavior_id: str,
        student_id: str | None = None,
    ) -> StudentBehaviorResponse:
        """Return a single behavior record of a student."""
        response = self._request(
            "GET",
            f"/api/v1/students/behaviors/{encode_path(behavior_id)}",
            params={
                "SchoolYearId": school_year_id,
                "TypeOfBehaviorId": type_of_behavior_id,
                "StudentId": student_id,
            },
        )
        return parse_model(response, StudentBehaviorResponse)

    def code_lists(
        self, *, school_year_id: str | None = None
    ) -> BehaviorCodeListsResponse:
        """Return the code lists used by the behaviors module."""
        response = self._request(
            "GET",
            "/api/v1/behaviors/codeLists",
            params={"schoolYearId": school_year_id},
        )
        return parse_model(response, BehaviorCodeListsResponse)

    def update(self, behavior_id: str, body: PutBehaviorRequest) -> None:
        """Update an existing behavior record."""
        self._request(
            "PUT",
            f"/api/v1/teacher/behaviors/{encode_path(behavior_id)}",
            json=body.to_dict(),
        )

    def delete(
        self, behavior_id: str, *, type_of_behavior_id: str, school_year_id: str
    ) -> None:
        """Delete a behavior record."""
        self._request(
            "DELETE",
            f"/api/v1/teacher/behaviors/{encode_path(behavior_id)}",
            params={
                "TypeOfBehaviorId": type_of_behavior_id,
                "SchoolYearId": school_year_id,
            },
        )

    def sign(
        self, behavior_id: str, *, type_of_behavior_id: str, school_year_id: str
    ) -> None:
        """Sign a single behavior record."""
        self._request(
            "PUT",
            f"/api/v1/student/behaviors/{encode_path(behavior_id)}/sign",
            params={
                "TypeOfBehaviorId": type_of_behavior_id,
                "SchoolYearId": school_year_id,
            },
        )

    def sign_many(self, student_id: str, body: PutMultipleSignBehaviorsRequest) -> None:
        """Sign multiple behavior records of a student."""
        self._request(
            "PUT",
            f"/api/v1/student/{encode_path(student_id)}/behaviors/sign",
            json=body.to_dict(),
        )


class AsyncBehaviors(AsyncAPIResource):
    async def list_types(self) -> TypesOfBehaviorResponse:
        """Return the types of behavior records."""
        response = await self._request("GET", "/api/v1/behaviors/typesOfBehavior")
        return parse_model(response, TypesOfBehaviorResponse)

    async def list_note_kinds(
        self,
        *,
        kind_id: str | None = None,
        only_valid: bool | None = None,
        only_positive: bool | None = None,
        only_negative: bool | None = None,
    ) -> KindsOfNotesClassBookResponse:
        """Return the kinds of class book notes."""
        response = await self._request(
            "GET",
            "/api/v1/behaviors/kindsOfNotesClassBook",
            params={
                "KindId": kind_id,
                "OnlyValid": only_valid,
                "OnlyPositive": only_positive,
                "OnlyNegative": only_negative,
            },
        )
        return parse_model(response, KindsOfNotesClassBookResponse)

    async def list_educational_measure_kinds(
        self,
        *,
        kind_id: str | None = None,
        only_valid: bool | None = None,
        only_positive: bool | None = None,
        only_negative: bool | None = None,
    ) -> KindsOfEducationalMeasuresResponse:
        """Return the kinds of educational measures."""
        response = await self._request(
            "GET",
            "/api/v1/behaviors/kindsOfEducationalMeasures",
            params={
                "KindId": kind_id,
                "OnlyValid": only_valid,
                "OnlyPositive": only_positive,
                "OnlyNegative": only_negative,
            },
        )
        return parse_model(response, KindsOfEducationalMeasuresResponse)

    async def list_educational_measure_reasons(
        self,
        *,
        reason_id: str | None = None,
        search: str | None = None,
        only_valid: bool | None = None,
        only_positive: bool | None = None,
        only_negative: bool | None = None,
    ) -> ReasonsOfEducationalMeasuresResponse:
        """Return the reasons available for educational measures."""
        response = await self._request(
            "GET",
            "/api/v1/teacher/behaviors/reasonsOfEducationalMeasures",
            params={
                "ReasonId": reason_id,
                "Search": search,
                "OnlyValid": only_valid,
                "OnlyPositive": only_positive,
                "OnlyNegative": only_negative,
            },
        )
        return parse_model(response, ReasonsOfEducationalMeasuresResponse)

    async def list_evaluation_kinds(
        self, *, kind_id: str | None = None, school_year_id: str | None = None
    ) -> KindsOfBehaviorEvaluationsResponse:
        """Return the kinds of behavior evaluations."""
        response = await self._request(
            "GET",
            "/api/v1/behaviors/kindsOfBehaviorEvaluations",
            params={"KindId": kind_id, "SchoolYearId": school_year_id},
        )
        return parse_model(response, KindsOfBehaviorEvaluationsResponse)

    async def list_teacher_classes(
        self, *, class_status: ClassStatus, school_year_id: str | None = None
    ) -> BehaviorClassesResponse:
        """Return elementary and higher classes of the requested school year."""
        response = await self._request(
            "GET",
            "/api/v1/teacher/behaviors/classes",
            params={"SenderPersonType": class_status, "SchoolYearId": school_year_id},
        )
        return parse_model(response, BehaviorClassesResponse)

    async def list_students_of_class(
        self,
        *,
        class_id: str,
        school_year_id: str | None = None,
        to_date: DateLike | None = None,
    ) -> StudentsOfClassResponse:
        """Return the students of a class on a given date."""
        response = await self._request(
            "GET",
            "/api/v1/teacher/behaviors/studentsOfClass",
            params={
                "ClassId": class_id,
                "SchoolYearId": school_year_id,
                "ToDate": to_date,
            },
        )
        return parse_model(response, StudentsOfClassResponse)

    async def list_for_teacher(
        self,
        *,
        school_year_id: str | None = None,
        from_date: DateLike | None = None,
        to_date: DateLike | None = None,
        class_id: str | None = None,
        student_id: str | None = None,
        type_of_behavior_id: str | None = None,
        kind_of_notes_class_book_id: str | None = None,
        kind_of_educational_measures_id: str | None = None,
        kind_of_behavior_evaluations_id: str | None = None,
        order_by: BehaviorOrder | None = None,
        search: str | None = None,
        page_number: int | None = None,
        page_size: int | None = None,
    ) -> BehaviorsResponse:
        """Return behavior records of students matching the filter."""
        response = await self._request(
            "GET",
            "/api/v1/teacher/behaviors",
            params={
                "SchoolYearId": school_year_id,
                "FromDate": from_date,
                "ToDate": to_date,
                "ClassId": class_id,
                "StudentId": student_id,
                "TypeOfBehaviorId": type_of_behavior_id,
                "KindOfNotesClassBookId": kind_of_notes_class_book_id,
                "KindOfEducationalMeasuresId": kind_of_educational_measures_id,
                "KindOfBehaviorEvaluationsId": kind_of_behavior_evaluations_id,
                "OrderBy": order_by,
                "Search": search,
                "Pagination.PageNumber": page_number,
                "Pagination.PageSize": page_size,
            },
        )
        return parse_model(response, BehaviorsResponse)

    async def create(self, body: PostBehaviorRequest) -> None:
        """Create a new behavior record."""
        await self._request("POST", "/api/v1/teacher/behaviors", json=body.to_dict())

    async def list_for_student(
        self,
        student_id: str,
        *,
        school_year_id: str | None = None,
        from_date: DateLike | None = None,
        to_date: DateLike | None = None,
        type_of_behavior_id: str | None = None,
        kind_of_notes_class_book_id: str | None = None,
        kind_of_educational_measures_id: str | None = None,
        kind_of_behavior_evaluations_id: str | None = None,
        page_number: int | None = None,
        page_size: int | None = None,
        search: str | None = None,
        records_filter: RecordsFilter | None = None,
    ) -> StudentBehaviorsResponse:
        """Return behavior records of a student matching the filter."""
        response = await self._request(
            "GET",
            f"/api/v1/students/{encode_path(student_id)}/behaviors",
            params={
                "SchoolYearId": school_year_id,
                "FromDate": from_date,
                "ToDate": to_date,
                "TypeOfBehaviorId": type_of_behavior_id,
                "KindOfNotesClassBookId": kind_of_notes_class_book_id,
                "KindOfEducationalMeasuresId": kind_of_educational_measures_id,
                "KindOfBehaviorEvaluationsId": kind_of_behavior_evaluations_id,
                "Pagination.PageNumber": page_number,
                "Pagination.PageSize": page_size,
                "Search": search,
                "RecordsFilter": records_filter,
            },
        )
        return parse_model(response, StudentBehaviorsResponse)

    async def retrieve(
        self,
        behavior_id: str,
        *,
        school_year_id: str,
        type_of_behavior_id: str,
        student_id: str | None = None,
    ) -> StudentBehaviorResponse:
        """Return a single behavior record of a student."""
        response = await self._request(
            "GET",
            f"/api/v1/students/behaviors/{encode_path(behavior_id)}",
            params={
                "SchoolYearId": school_year_id,
                "TypeOfBehaviorId": type_of_behavior_id,
                "StudentId": student_id,
            },
        )
        return parse_model(response, StudentBehaviorResponse)

    async def code_lists(
        self, *, school_year_id: str | None = None
    ) -> BehaviorCodeListsResponse:
        """Return the code lists used by the behaviors module."""
        response = await self._request(
            "GET",
            "/api/v1/behaviors/codeLists",
            params={"schoolYearId": school_year_id},
        )
        return parse_model(response, BehaviorCodeListsResponse)

    async def update(self, behavior_id: str, body: PutBehaviorRequest) -> None:
        """Update an existing behavior record."""
        await self._request(
            "PUT",
            f"/api/v1/teacher/behaviors/{encode_path(behavior_id)}",
            json=body.to_dict(),
        )

    async def delete(
        self, behavior_id: str, *, type_of_behavior_id: str, school_year_id: str
    ) -> None:
        """Delete a behavior record."""
        await self._request(
            "DELETE",
            f"/api/v1/teacher/behaviors/{encode_path(behavior_id)}",
            params={
                "TypeOfBehaviorId": type_of_behavior_id,
                "SchoolYearId": school_year_id,
            },
        )

    async def sign(
        self, behavior_id: str, *, type_of_behavior_id: str, school_year_id: str
    ) -> None:
        """Sign a single behavior record."""
        await self._request(
            "PUT",
            f"/api/v1/student/behaviors/{encode_path(behavior_id)}/sign",
            params={
                "TypeOfBehaviorId": type_of_behavior_id,
                "SchoolYearId": school_year_id,
            },
        )

    async def sign_many(
        self, student_id: str, body: PutMultipleSignBehaviorsRequest
    ) -> None:
        """Sign multiple behavior records of a student."""
        await self._request(
            "PUT",
            f"/api/v1/student/{encode_path(student_id)}/behaviors/sign",
            json=body.to_dict(),
        )

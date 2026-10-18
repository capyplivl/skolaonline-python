from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from skolaonline.models._base import SkolaOnlineModel


class BehaviorOrder(StrEnum):
    DATE_DESC = "dateDesc"
    DATE_ASC = "dateAsc"
    NAME_DESC = "nameDesc"
    NAME_ASC = "nameAsc"


class ClassStatus(StrEnum):
    ALL = "all"
    CLASS_TEACHER = "classTeacher"
    CLASS_OR_DEPUTY_CLASS_TEACHER = "classOrDeputyClassTeacher"


class RecordsFilter(StrEnum):
    ALL = "all"
    UNSIGNED = "unsigned"
    NOTES_CLASS_BOOK = "notesClassBook"
    BEHAVIOR_EVALUATIONS = "behaviorEvaluations"
    POSITIVE_EDUCATIONAL_MEASURES = "positiveEducationalMeasures"
    NEGATIVE_EDUCATIONAL_MEASURES = "negativeEducationalMeasures"


@dataclass(kw_only=True)
class Behavior(SkolaOnlineModel):
    school_year_id: str
    semester_id: str
    type_of_behaviors_id: str
    kind_of_behaviors_id: str | None = None
    kind_of_behavior_name: str
    kind_of_behavior_abbrev: str | None = None
    behavior_id: str
    positive: bool | None = None
    behavior_reason: str | None = None
    reference_number: str | None = None
    internal_note: str | None = None
    date: datetime | None = None
    class_id: str
    class_name: str
    lesson_id: str | None = None
    label: str | None = None
    student_id: str
    student_name: str
    student_initials: str | None = None
    signed_date: datetime | None = None
    signed_id: str | None = None
    signed_name: str | None = None
    create_id: str
    create_name: str | None = None
    print_on_report: bool | None = None
    order: int | None = None
    edit_allowed: bool | None = None
    delete_allowed: bool | None = None


@dataclass(kw_only=True)
class BehaviorClass(SkolaOnlineModel):
    class_id: str
    name: str
    description: str | None = None
    order: int | None = None
    class_teacher: bool
    deputy_class_teacher: bool


@dataclass(kw_only=True)
class BehaviorClassesResponse(SkolaOnlineModel):
    classes: list[BehaviorClass]


@dataclass(kw_only=True)
class BehaviorCodeListsResponse(SkolaOnlineModel):
    behavioral_scale: list[BehavioralScale]
    lessons: list[BehaviorLesson]
    semester: list[BehaviorSemester]
    classes: list[CodeListClass]
    signing: bool
    enabled_signing: bool


@dataclass(kw_only=True)
class BehaviorLesson(SkolaOnlineModel):
    id: str
    name: str
    begin_time: datetime
    end_time: datetime


@dataclass(kw_only=True)
class BehaviorSemester(SkolaOnlineModel):
    id: str
    parent_id: str
    name: str
    date_from: datetime
    date_to: datetime
    order: int


@dataclass(kw_only=True)
class BehaviorSignItem(SkolaOnlineModel):
    id: str
    type_of_behavior_id: str


@dataclass(kw_only=True)
class BehaviorType(SkolaOnlineModel):
    type_id: str
    type_name: str


@dataclass(kw_only=True)
class BehavioralScale(SkolaOnlineModel):
    id: str
    name: str
    value: float | None = None
    percent_from: int | None = None
    percent_to: int | None = None
    include_percent_from: bool | None = None
    include_percent_to: bool | None = None


@dataclass(kw_only=True)
class BehaviorsResponse(SkolaOnlineModel):
    behaviors: list[Behavior]
    number_processed: int | None = None


@dataclass(kw_only=True)
class CodeListClass(SkolaOnlineModel):
    id: str
    name: str
    description: str | None = None
    order: int | None = None


@dataclass(kw_only=True)
class KindOfBehaviorEvaluations(SkolaOnlineModel):
    school_year: str
    kind_id: str
    value: str


@dataclass(kw_only=True)
class KindOfBehaviorNotes(SkolaOnlineModel):
    kind_id: str
    abbreviation: str
    name: str
    order: int | None = None
    positive: bool | None = None
    valid: bool


@dataclass(kw_only=True)
class KindOfEducationalMeasures(SkolaOnlineModel):
    kind_id: str
    description: str | None = None
    name: str
    positive: bool | None = None
    valid: bool


@dataclass(kw_only=True)
class KindsOfBehaviorEvaluationsResponse(SkolaOnlineModel):
    kinds_of_behavior_evaluations: list[KindOfBehaviorEvaluations]
    behavior_evaluation_method: str


@dataclass(kw_only=True)
class KindsOfEducationalMeasuresResponse(SkolaOnlineModel):
    kinds_of_educational_measures: list[KindOfEducationalMeasures]


@dataclass(kw_only=True)
class KindsOfNotesClassBookResponse(SkolaOnlineModel):
    kinds_of_notes_class_book: list[KindOfBehaviorNotes]


@dataclass(kw_only=True)
class PostBehaviorRequest(SkolaOnlineModel):
    school_year_id: str | None = None
    semester_id: str | None = None
    lesson_id: str | None = None
    type_of_behaviors_id: str
    kind_of_behaviors_id: str
    behavior_reason: str
    reference_number: str | None = None
    internal_note: str | None = None
    date: datetime
    print_on_report: bool | None = None
    students_id: list[PostBehaviorStudent]


@dataclass(kw_only=True)
class PostBehaviorStudent(SkolaOnlineModel):
    student_id: str


@dataclass(kw_only=True)
class PutBehaviorData(SkolaOnlineModel):
    semester_id: str | None = None
    lesson_id: str | None = None
    type_of_behaviors_id: str
    kind_of_behaviors_id: str
    behavior_reason: str
    reference_number: str | None = None
    internal_note: str | None = None
    date: datetime
    print_on_report: bool | None = None


@dataclass(kw_only=True)
class PutBehaviorRequest(SkolaOnlineModel):
    type_of_behavior_id: str
    school_year_id: str
    data: PutBehaviorData


@dataclass(kw_only=True)
class PutMultipleSignBehaviorsRequest(SkolaOnlineModel):
    school_year_id: str
    behaviors_id: list[BehaviorSignItem]


@dataclass(kw_only=True)
class ReasonOfEducationalMeasures(SkolaOnlineModel):
    reason_id: str
    name: str
    order: int | None = None
    positive: bool | None = None
    valid: bool


@dataclass(kw_only=True)
class ReasonsOfEducationalMeasuresResponse(SkolaOnlineModel):
    reasons_of_educational_measures: list[ReasonOfEducationalMeasures]


@dataclass(kw_only=True)
class StudentBehavior(SkolaOnlineModel):
    school_year_id: str
    semester_id: str
    type_of_behaviors_id: str
    kind_of_behaviors_id: str
    kind_of_behavior_name: str
    kind_of_behavior_abbrev: str | None = None
    behavior_id: str
    positive: bool | None = None
    behavior_reason: str | None = None
    reference_number: str | None = None
    date: datetime
    signed_date: datetime | None = None
    signed_id: str | None = None
    signed_name: str | None = None
    create_id: str
    create_name: str | None = None
    print_on_report: bool | None = None


@dataclass(kw_only=True)
class StudentBehaviorResponse(SkolaOnlineModel):
    behavior: StudentBehavior | None = None


@dataclass(kw_only=True)
class StudentBehaviorWithOrder(SkolaOnlineModel):
    school_year_id: str
    semester_id: str
    type_of_behaviors_id: str
    kind_of_behaviors_id: str
    kind_of_behavior_name: str
    kind_of_behavior_abbrev: str | None = None
    behavior_id: str
    positive: bool | None = None
    behavior_reason: str | None = None
    reference_number: str | None = None
    date: datetime
    signed_date: datetime | None = None
    signed_id: str | None = None
    signed_name: str | None = None
    create_id: str
    create_name: str | None = None
    print_on_report: bool | None = None
    order: int | None = None


@dataclass(kw_only=True)
class StudentBehaviorsResponse(SkolaOnlineModel):
    behaviors: list[StudentBehaviorWithOrder]
    number_processed: int | None = None


@dataclass(kw_only=True)
class StudentOfClass(SkolaOnlineModel):
    class_id: str
    class_name: str
    student_id: str
    first_name: str | None = None
    last_name: str
    display_name: str
    birthdate: datetime | None = None


@dataclass(kw_only=True)
class StudentsOfClassResponse(SkolaOnlineModel):
    students_of_class: list[StudentOfClass]


@dataclass(kw_only=True)
class TypesOfBehaviorResponse(SkolaOnlineModel):
    types_of_behavior: list[BehaviorType]

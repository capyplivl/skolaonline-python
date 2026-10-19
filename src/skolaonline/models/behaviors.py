from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from skolaonline.models._base import SkolaOnlineModel


class BehaviorOrder(StrEnum):
    """Sort order of behavior records. Defaults to newest first."""

    DATE_DESC = "dateDesc"
    """By date, newest first."""

    DATE_ASC = "dateAsc"
    """By date, oldest first."""

    NAME_DESC = "nameDesc"
    """By student name, descending."""

    NAME_ASC = "nameAsc"
    """By student name, ascending."""


class ClassStatus(StrEnum):
    """Which classes of the teacher are returned."""

    ALL = "all"
    """All classes."""

    CLASS_TEACHER = "classTeacher"
    """Classes where the user is the class teacher."""

    CLASS_OR_DEPUTY_CLASS_TEACHER = "classOrDeputyClassTeacher"
    """Classes where the user is the class teacher or the deputy class teacher."""


class RecordsFilter(StrEnum):
    """Filter of behavior records of a student."""

    ALL = "all"
    """All behavior records."""

    UNSIGNED = "unsigned"
    """Unsigned behavior records."""

    NOTES_CLASS_BOOK = "notesClassBook"
    """Class book notes only."""

    BEHAVIOR_EVALUATIONS = "behaviorEvaluations"
    """Behavior marks only."""

    POSITIVE_EDUCATIONAL_MEASURES = "positiveEducationalMeasures"
    """Positive educational measures only."""

    NEGATIVE_EDUCATIONAL_MEASURES = "negativeEducationalMeasures"
    """Negative educational measures only."""


@dataclass(kw_only=True)
class Behavior(SkolaOnlineModel):
    """Behavior record of a student."""

    school_year_id: str
    """ID of the school year."""

    semester_id: str
    """ID of the semester."""

    type_of_behaviors_id: str
    """Type of the behavior record."""

    kind_of_behaviors_id: str | None = None
    """Kind of the behavior record."""

    kind_of_behavior_name: str
    """Name of the kind of behavior record."""

    kind_of_behavior_abbrev: str | None = None
    """Abbreviation of the kind of behavior record."""

    behavior_id: str
    """ID of the behavior record."""

    positive: bool | None = None
    """Whether the behavior record is positive."""

    behavior_reason: str | None = None
    """Reason for the behavior record."""

    reference_number: str | None = None
    """Reference number of the behavior record."""

    internal_note: str | None = None
    """Internal note of the behavior record."""

    date: datetime | None = None
    """Date the behavior record was given."""

    class_id: str
    """ID of the class of the student on the date of the record."""

    class_name: str
    """Name of the class of the student on the date of the record."""

    lesson_id: str | None = None
    """ID of the lesson. Only set for class book notes."""

    label: str | None = None
    """Name of the lesson. Only set for class book notes."""

    student_id: str
    """ID of the student."""

    student_name: str
    """Full name of the student, surname first."""

    student_initials: str | None = None
    """Initials of the student."""

    signed_date: datetime | None = None
    """Date the record was signed."""

    signed_id: str | None = None
    """ID of the person who signed the record."""

    signed_name: str | None = None
    """Full name of the person who signed the record, surname first."""

    create_id: str
    """ID of the person who created the record. Empty string unless the school shows
    record authors in the given school year."""

    create_name: str | None = None
    """Full name of the person who created the record, surname first."""

    print_on_report: bool | None = None
    """Whether the record is printed on the report card."""

    order: int | None = None
    """Order of the behavior record."""

    edit_allowed: bool | None = None
    """Whether the user can edit the record."""

    delete_allowed: bool | None = None
    """Whether the user can delete the record."""


@dataclass(kw_only=True)
class BehaviorClass(SkolaOnlineModel):
    """Class available in the behaviors module."""

    class_id: str
    """ID of the class."""

    name: str
    """Name of the class."""

    description: str | None = None
    """Description of the class."""

    order: int | None = None
    """Display order."""

    class_teacher: bool
    """Whether the user is the class teacher."""

    deputy_class_teacher: bool
    """Whether the user is the deputy class teacher."""


@dataclass(kw_only=True)
class BehaviorClassesResponse(SkolaOnlineModel):
    """Classes available in the behaviors module."""

    classes: list[BehaviorClass]
    """Classes."""


@dataclass(kw_only=True)
class BehaviorCodeListsResponse(SkolaOnlineModel):
    """Code lists used by the behaviors module."""

    behavioral_scale: list[BehavioralScale]
    """Grades of the behavior evaluation scale."""

    lessons: list[BehaviorLesson]
    """Lessons of the school day."""

    semester: list[BehaviorSemester]
    """Semesters of the school year."""

    classes: list[CodeListClass]
    """Classes."""

    signing: bool
    """Whether the school allows signing, based on the application setting for
    signing the student record book."""

    enabled_signing: bool
    """Whether the signed-in person can sign."""


@dataclass(kw_only=True)
class BehaviorLesson(SkolaOnlineModel):
    """Lesson of the school day."""

    id: str
    """ID of the lesson."""

    name: str
    """Name of the lesson."""

    begin_time: datetime
    """Start time of the lesson."""

    end_time: datetime
    """End time of the lesson."""


@dataclass(kw_only=True)
class BehaviorSemester(SkolaOnlineModel):
    """Semester."""

    id: str
    """ID of the semester."""

    parent_id: str
    """ID of the parent semester."""

    name: str
    """Name of the semester."""

    date_from: datetime
    """First day of the semester."""

    date_to: datetime
    """Last day of the semester."""

    order: int
    """Order of the semester."""


@dataclass(kw_only=True)
class BehaviorSignItem(SkolaOnlineModel):
    """Behavior record to sign in bulk."""

    id: str
    """ID of the behavior record."""

    type_of_behavior_id: str
    """Type of the behavior record: N for a class book note, V for an educational
    measure, Z for a behavior mark, P for a behavior percentage."""


@dataclass(kw_only=True)
class BehaviorType(SkolaOnlineModel):
    """Type of behavior record."""

    type_id: str
    """ID of the type of behavior record."""

    type_name: str
    """Name of the type of behavior record."""


@dataclass(kw_only=True)
class BehavioralScale(SkolaOnlineModel):
    """Grade of the behavior evaluation scale."""

    id: str
    """ID of the grade."""

    name: str
    """Name of the grade."""

    value: float | None = None
    """Value of the grade."""

    percent_from: int | None = None
    """Lower bound of the percentage range."""

    percent_to: int | None = None
    """Upper bound of the percentage range."""

    include_percent_from: bool | None = None
    """Whether the lower bound is included in the range."""

    include_percent_to: bool | None = None
    """Whether the upper bound is included in the range."""


@dataclass(kw_only=True)
class BehaviorsResponse(SkolaOnlineModel):
    """Behavior records matching a filter."""

    behaviors: list[Behavior]
    """Behavior records."""

    number_processed: int | None = None
    """Total number of behavior records matching the filter."""


@dataclass(kw_only=True)
class CodeListClass(SkolaOnlineModel):
    """Class listed in the behaviors code lists."""

    id: str
    """ID of the class."""

    name: str
    """Name of the class."""

    description: str | None = None
    """Description of the class."""

    order: int | None = None
    """Display order."""


@dataclass(kw_only=True)
class KindOfBehaviorEvaluations(SkolaOnlineModel):
    """Kind of behavior evaluation."""

    school_year: str
    """ID of the school year."""

    kind_id: str
    """ID of the kind of behavior evaluation."""

    value: str
    """Value of the kind of behavior evaluation."""


@dataclass(kw_only=True)
class KindOfBehaviorNotes(SkolaOnlineModel):
    """Kind of class book note."""

    kind_id: str
    """ID of the kind of note."""

    abbreviation: str
    """Abbreviation."""

    name: str
    """Name."""

    order: int | None = None
    """Display order."""

    positive: bool | None = None
    """Whether the kind of note is positive."""

    valid: bool
    """Whether the kind of note is currently valid."""


@dataclass(kw_only=True)
class KindOfEducationalMeasures(SkolaOnlineModel):
    """Kind of educational measure."""

    kind_id: str
    """ID of the kind of educational measure."""

    description: str | None = None
    """Abbreviation."""

    name: str
    """Name."""

    positive: bool | None = None
    """Whether the kind of educational measure is positive."""

    valid: bool
    """Whether the kind of educational measure is currently valid."""


@dataclass(kw_only=True)
class KindsOfBehaviorEvaluationsResponse(SkolaOnlineModel):
    """Kinds of behavior evaluations."""

    kinds_of_behavior_evaluations: list[KindOfBehaviorEvaluations]
    """Kinds of behavior evaluations."""

    behavior_evaluation_method: str
    """How behavior evaluations are entered."""


@dataclass(kw_only=True)
class KindsOfEducationalMeasuresResponse(SkolaOnlineModel):
    """Kinds of educational measures."""

    kinds_of_educational_measures: list[KindOfEducationalMeasures]
    """Kinds of educational measures."""


@dataclass(kw_only=True)
class KindsOfNotesClassBookResponse(SkolaOnlineModel):
    """Kinds of class book notes."""

    kinds_of_notes_class_book: list[KindOfBehaviorNotes]
    """Kinds of class book notes."""


@dataclass(kw_only=True)
class PostBehaviorRequest(SkolaOnlineModel):
    """Data of a new behavior record."""

    school_year_id: str | None = None
    """ID of the school year."""

    semester_id: str | None = None
    """ID of the semester."""

    lesson_id: str | None = None
    """ID of the lesson."""

    type_of_behaviors_id: str
    """Type of the behavior record."""

    kind_of_behaviors_id: str
    """Kind of the behavior record."""

    behavior_reason: str
    """Reason for the behavior record."""

    reference_number: str | None = None
    """Reference number of the behavior record."""

    internal_note: str | None = None
    """Internal note of the behavior record."""

    date: datetime
    """Date the behavior record was given."""

    print_on_report: bool | None = None
    """Whether the record is printed on the report card."""

    students_id: list[PostBehaviorStudent]
    """Students the behavior record is created for."""


@dataclass(kw_only=True)
class PostBehaviorStudent(SkolaOnlineModel):
    """Student a new behavior record is created for."""

    student_id: str
    """ID of the student the behavior record is created for."""


@dataclass(kw_only=True)
class PutBehaviorData(SkolaOnlineModel):
    """Updated data of a behavior record."""

    semester_id: str | None = None
    """ID of the semester."""

    lesson_id: str | None = None
    """ID of the lesson."""

    type_of_behaviors_id: str
    """Type of the behavior record."""

    kind_of_behaviors_id: str
    """Kind of the behavior record."""

    behavior_reason: str
    """Reason for the behavior record."""

    reference_number: str | None = None
    """Reference number of the behavior record."""

    internal_note: str | None = None
    """Internal note of the behavior record."""

    date: datetime
    """Date the behavior record was given."""

    print_on_report: bool | None = None
    """Whether the record is printed on the report card."""


@dataclass(kw_only=True)
class PutBehaviorRequest(SkolaOnlineModel):
    """Update of an existing behavior record."""

    type_of_behavior_id: str
    """Type of the behavior record."""

    school_year_id: str
    """ID of the school year of the behavior record."""

    data: PutBehaviorData
    """Updated data of the behavior record."""


@dataclass(kw_only=True)
class PutMultipleSignBehaviorsRequest(SkolaOnlineModel):
    """Bulk signing of behavior records of a student."""

    school_year_id: str
    """ID of the school year shared by all records."""

    behaviors_id: list[BehaviorSignItem]
    """Behavior records to sign."""


@dataclass(kw_only=True)
class ReasonOfEducationalMeasures(SkolaOnlineModel):
    """Reason for an educational measure."""

    reason_id: str
    """ID of the reason for an educational measure."""

    name: str
    """Name."""

    order: int | None = None
    """Display order."""

    positive: bool | None = None
    """Whether the reason is positive."""

    valid: bool
    """Whether the reason is currently valid."""


@dataclass(kw_only=True)
class ReasonsOfEducationalMeasuresResponse(SkolaOnlineModel):
    """Reasons for educational measures."""

    reasons_of_educational_measures: list[ReasonOfEducationalMeasures]
    """Reasons for educational measures."""


@dataclass(kw_only=True)
class StudentBehavior(SkolaOnlineModel):
    """Behavior record of a student."""

    school_year_id: str
    """ID of the school year."""

    semester_id: str
    """ID of the semester."""

    type_of_behaviors_id: str
    """Type of the behavior record."""

    kind_of_behaviors_id: str
    """Kind of the behavior record."""

    kind_of_behavior_name: str
    """Name of the kind of behavior record."""

    kind_of_behavior_abbrev: str | None = None
    """Abbreviation of the kind of behavior record."""

    behavior_id: str
    """ID of the behavior record."""

    positive: bool | None = None
    """Whether the behavior record is positive."""

    behavior_reason: str | None = None
    """Reason for the behavior record."""

    reference_number: str | None = None
    """Reference number of the behavior record."""

    date: datetime
    """Date the behavior record was given."""

    signed_date: datetime | None = None
    """Date the record was signed."""

    signed_id: str | None = None
    """ID of the person who signed the record."""

    signed_name: str | None = None
    """Full name of the person who signed the record, surname first."""

    create_id: str
    """ID of the person who created the record."""

    create_name: str | None = None
    """Full name of the person who created the record, surname first."""

    print_on_report: bool | None = None
    """Whether the record is printed on the report card."""


@dataclass(kw_only=True)
class StudentBehaviorResponse(SkolaOnlineModel):
    """Single behavior record of a student."""

    behavior: StudentBehavior | None = None
    """Behavior record."""


@dataclass(kw_only=True)
class StudentBehaviorWithOrder(SkolaOnlineModel):
    """Behavior record of a student with its display order."""

    school_year_id: str
    """ID of the school year."""

    semester_id: str
    """ID of the semester."""

    type_of_behaviors_id: str
    """Type of the behavior record."""

    kind_of_behaviors_id: str
    """Kind of the behavior record."""

    kind_of_behavior_name: str
    """Name of the kind of behavior record."""

    kind_of_behavior_abbrev: str | None = None
    """Abbreviation of the kind of behavior record."""

    behavior_id: str
    """ID of the behavior record."""

    positive: bool | None = None
    """Whether the behavior record is positive."""

    behavior_reason: str | None = None
    """Reason for the behavior record."""

    reference_number: str | None = None
    """Reference number of the behavior record."""

    date: datetime
    """Date the behavior record was given."""

    signed_date: datetime | None = None
    """Date the record was signed."""

    signed_id: str | None = None
    """ID of the person who signed the record."""

    signed_name: str | None = None
    """Full name of the person who signed the record, surname first."""

    create_id: str
    """ID of the person who created the record."""

    create_name: str | None = None
    """Full name of the person who created the record, surname first."""

    print_on_report: bool | None = None
    """Whether the record is printed on the report card."""

    order: int | None = None
    """Order of the behavior record."""


@dataclass(kw_only=True)
class StudentBehaviorsResponse(SkolaOnlineModel):
    """Behavior records of a student."""

    behaviors: list[StudentBehaviorWithOrder]
    """Behavior records of the student matching the filter."""

    number_processed: int | None = None
    """Total number of behavior records matching the filter."""


@dataclass(kw_only=True)
class StudentOfClass(SkolaOnlineModel):
    """Student of a class."""

    class_id: str
    """ID of the class."""

    class_name: str
    """Name of the class."""

    student_id: str
    """ID of the student."""

    first_name: str | None = None
    """First name of the student."""

    last_name: str
    """Surname of the student."""

    display_name: str
    """Full name for display, including titles."""

    birthdate: datetime | None = None
    """Date of birth of the student."""


@dataclass(kw_only=True)
class StudentsOfClassResponse(SkolaOnlineModel):
    """Students of a class."""

    students_of_class: list[StudentOfClass]
    """Students of the class."""


@dataclass(kw_only=True)
class TypesOfBehaviorResponse(SkolaOnlineModel):
    """Types of behavior records."""

    types_of_behavior: list[BehaviorType]
    """Types of behavior records."""

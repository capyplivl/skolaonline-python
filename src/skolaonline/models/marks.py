from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from skolaonline.models._base import SkolaOnlineModel


class Achievement(StrEnum):
    """Overall result on the report card."""

    PASSED_WITH_HONORS = "passedWithHonors"
    """Passed with honors."""

    PASSED = "passed"
    """Passed."""

    FAILED = "failed"
    """Failed."""

    NOT_EVALUATED = "notEvaluated"
    """Not evaluated."""


class AssessmentMethod(StrEnum):
    """Kind of value of a mark."""

    MARKS = "marks"
    """Mark."""

    POINTS = "points"
    """Points."""

    PERCENTAGES = "percentages"
    """Percentage."""


class MarksListOrder(StrEnum):
    """Sort order of marks. Defaults to newest first."""

    DATE_DESC = "dateDesc"
    """By date, newest first."""

    DATE_ASC = "dateAsc"
    """By date, oldest first."""


class MarksListSigningFilter(StrEnum):
    """Filter of marks by signing state."""

    ALL = "all"
    """All marks."""

    UNSIGNED = "unsigned"
    """Unsigned marks only."""

    SIGNED = "signed"
    """Signed marks only."""


@dataclass(kw_only=True)
class CertificateTerm(SkolaOnlineModel):
    """Report card of a semester."""

    final_marks: list[FinalMark]
    """Final marks of the student in the school year."""

    subjects: list[MarkSubject]
    """Subjects of the school year."""

    grade_name: str
    """Name of the grade."""

    grade: str
    """Grade of the student."""

    school_year_name: str
    """Name of the school year."""

    school_year_order: int | None = None
    """Order of the school year."""

    semester_name: str
    """Name of the semester."""

    semester_abbrev: str | None = None
    """Abbreviation of the semester."""

    semester_order: int | None = None
    """Order of the semester within the school year."""

    closed: bool | None = None
    """Whether the data is closed."""

    achievement_text: str | None = None
    """Overall result as text."""

    achievement: Achievement | None = None
    """Overall result."""

    marks_average: float | None = None
    """Average of the marks on the report card."""

    absent_hours: int | None = None
    """Number of missed lessons."""

    excused_hours: int | None = None
    """Number of excused lessons."""

    not_excused_hours: int | None = None
    """Number of unexcused lessons."""

    final_verbal_evaluation: str | None = None
    """Overall verbal evaluation."""


@dataclass(kw_only=True)
class FinalMark(SkolaOnlineModel):
    """Final mark on a report card."""

    mark_date: datetime
    """Date the mark was given."""

    edit_date: datetime | None = None
    """Date the teacher entered or changed the mark."""

    mark_text: str | None = None
    """Mark for display."""

    shortcut_to_display: str | None = None
    """Abbreviation shown on the report card."""

    verbal_evaluation: str | None = None
    """Verbal evaluation."""

    unclassified: bool
    """Whether the student is not classified in the subject."""

    released: bool
    """Whether the student is exempt from the subject."""

    unevaluated: bool
    """Whether the student is not evaluated in the subject."""

    recognized: bool
    """Whether the subject is recognized for the student."""

    has_verbal_evaluation: bool
    """Whether the mark has a verbal evaluation."""

    subject_id: str
    """ID of the evaluated subject."""

    order: int | None = None
    """Order of the mark on the report card."""


@dataclass(kw_only=True)
class FinalMarksResponse(SkolaOnlineModel):
    """Report cards of a student."""

    certificate_terms: list[CertificateTerm]
    """Report cards of the student."""


@dataclass(kw_only=True)
class Mark(SkolaOnlineModel):
    """Mark of a student."""

    mark_date: datetime
    """Date the mark was given."""

    edit_date: datetime
    """Date the teacher entered or changed the mark."""

    theme: str | None = None
    """Topic of the evaluation."""

    mark_text: str | None = None
    """Mark for display."""

    verbal_evaluation: str | None = None
    """Verbal evaluation."""

    teacher_id: str
    """ID of the teacher who entered the mark."""

    type: str | None = None
    """Type of evaluation."""

    type_note: str | None = None
    """Description of the type of evaluation."""

    weight: float | None = None
    """Weight of the mark."""

    comment: str | None = None
    """Comment on the evaluation."""

    subject_id: str
    """ID of the subject."""

    is_points: bool
    """Whether the mark is expressed in points."""

    is_percents: bool
    """Whether the mark is expressed as a percentage."""

    calculated_mark_text: str | None = None
    """Calculated mark."""

    class_rank_text: str | None = None
    """Rank in the class for display."""

    value_to_average: str | None = None
    """Value used in the average."""

    class_average: str | None = None
    """Class average."""

    id: str
    """ID of the mark."""

    semester_id: str | None = None
    """ID of the semester."""

    lesson_id: str | None = None
    """ID of the lesson."""

    max_points: int | None = None
    """Maximum number of points."""

    signed_id: str | None = None
    """ID of the person who signed the mark."""

    signed_name: str | None = None
    """Full name of the person who signed the mark, surname first."""

    signed_date: datetime | None = None
    """Date the mark was signed."""


@dataclass(kw_only=True)
class MarkCodeListsResponse(SkolaOnlineModel):
    """Code lists used by the marks module."""

    rating_scale: list[RatingScale]
    """Rating scale."""

    semester: list[MarkSemester]
    """Semesters of the school year."""

    subjects: list[MarkSubject]
    """Subjects."""

    signing: bool
    """Whether the school allows signing, based on the application setting for
    signing the student record book."""

    enabled_signing: bool
    """Whether the signed-in person can sign."""

    lessons: list[MarkLesson]
    """Lessons of the school day."""

    method_evaluation: list[MethodEvaluation]
    """Evaluation methods."""

    types_evaluation: list[TypeEvaluation]
    """Types of evaluation."""

    is_theme_required: bool
    """Whether a topic is required when entering a mark."""

    enabled_class_rank: bool
    """Whether the rank of the student in the class is shown."""


@dataclass(kw_only=True)
class MarkId(SkolaOnlineModel):
    """Identifier of a mark to sign."""

    id: str
    """ID of the mark."""


@dataclass(kw_only=True)
class MarkLesson(SkolaOnlineModel):
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
class MarkSemester(SkolaOnlineModel):
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

    lock_classification: bool
    """Whether classification is locked after the closing date."""

    date_lock_classification: datetime | None = None
    """Classification closing date."""

    enabled_evaluate: bool
    """Whether the signed-in user can enter or edit marks in the semester."""


@dataclass(kw_only=True)
class MarkStudent(SkolaOnlineModel):
    """Student to be marked."""

    id: str
    """ID of the student."""

    first_name: str | None = None
    """First name of the student."""

    last_name: str
    """Surname of the student."""

    display_name: str
    """Full name of the student."""

    cvtv: int | None = None
    """Number of the student in the class register."""

    class_id: str
    """ID of the class of the student."""

    class_name: str
    """Name of the class of the student."""

    plan_mark: bool
    """Whether the mark is planned without a result yet."""

    mark_text: str | None = None
    """Mark of the student."""

    verbal_evaluation: str | None = None
    """Verbal evaluation of the student."""

    do_not_evaluate_in_subject: bool
    """Whether the student is not evaluated in the subject because of an exemption or
    recognition."""

    is_studying_abroad: bool
    """Whether the student fulfills compulsory schooling abroad."""


@dataclass(kw_only=True)
class MarkSubject(SkolaOnlineModel):
    """Subject of a mark."""

    id: str
    """ID of the subject."""

    abbrev: str | None = None
    """Abbreviation of the subject."""

    name: str
    """Name of the subject."""

    kind: str | None = None
    """Kind of subject."""


@dataclass(kw_only=True)
class MarkTeacher(SkolaOnlineModel):
    """Teacher who entered marks."""

    id: str
    """ID of the teacher."""

    abbrev: str | None = None
    """Abbreviation."""

    first_name: str | None = None
    """First name."""

    last_name: str
    """Surname."""

    title_before: str | None = None
    """Title before the name."""

    title_after: str | None = None
    """Title after the name."""

    display_name: str | None = None
    """Full name for display."""


@dataclass(kw_only=True)
class MarkWithoutAverage(SkolaOnlineModel):
    """Mark of a student without averages."""

    mark_date: datetime
    """Date the mark was given."""

    edit_date: datetime
    """Date the teacher entered or changed the mark."""

    theme: str | None = None
    """Topic of the evaluation."""

    mark_text: str | None = None
    """Mark for display."""

    verbal_evaluation: str | None = None
    """Verbal evaluation."""

    weight: float | None = None
    """Weight of the mark."""

    subject_id: str
    """ID of the subject."""

    is_points: bool
    """Whether the mark is expressed in points."""

    is_percents: bool
    """Whether the mark is expressed as a percentage."""

    id: str
    """ID of the mark."""

    semester_id: str | None = None
    """ID of the semester."""

    lesson_id: str | None = None
    """ID of the lesson."""

    max_points: int | None = None
    """Maximum number of points."""

    signed_id: str | None = None
    """ID of the person who signed the mark."""

    signed_name: str | None = None
    """Full name of the person who signed the mark, surname first."""

    signed_date: datetime | None = None
    """Date the mark was signed."""


@dataclass(kw_only=True)
class MarksListResponse(SkolaOnlineModel):
    """Flat list of marks of a student."""

    marks: list[MarkWithoutAverage]
    """Marks."""

    subjects: list[MarkSubject]
    """Subjects that have marks."""


@dataclass(kw_only=True)
class MarksResponse(SkolaOnlineModel):
    """Marks of a student grouped by subject."""

    subjects: list[MarksSubject]
    """Marks grouped by subject."""


@dataclass(kw_only=True)
class MarksSubject(SkolaOnlineModel):
    """Marks in a single subject."""

    marks: list[Mark]
    """Marks in the subject."""

    subject: MarkSubject
    """Subject."""

    teachers: list[MarkTeacher]
    """Teachers who entered marks in the subject."""

    average_text: str | None = None
    """Average mark in the subject."""

    average_text_type: AssessmentMethod | None = None
    """Type of the average mark."""


@dataclass(kw_only=True)
class MethodEvaluation(SkolaOnlineModel):
    """Evaluation method."""

    id: str
    """ID of the evaluation method."""

    name: str
    """Display name of the evaluation method."""


@dataclass(kw_only=True)
class PostTeacherMarksRequest(SkolaOnlineModel):
    """New mark record for students."""

    school_year_id: str
    """ID of the school year of the scheduled event."""

    semester_id: str
    """ID of the semester."""

    date_mark: datetime
    """Date of the evaluation."""

    other_date_mark: datetime | None = None
    """Different date when the evaluation took place."""

    lesson_id: str
    """ID of the lesson."""

    type_id: str
    """ID of the type of evaluation."""

    theme: str | None = None
    """Topic of the evaluation."""

    comment: str | None = None
    """Comment on the evaluation."""

    selected_method_evaluation: str
    """Selected evaluation method."""

    max_points: int | None = None
    """Maximum number of points for point evaluation."""

    students: list[PostTeacherMarksStudent]
    """Evaluated students."""

    udalost_id: str
    """ID of the scheduled event."""

    poradi: int
    """Order of the scheduled event."""


@dataclass(kw_only=True)
class PostTeacherMarksStudent(SkolaOnlineModel):
    """Mark of a student in a new mark record."""

    id: str
    """ID of the evaluated student."""

    plan_mark: bool
    """Whether the mark is planned without a result."""

    mark_text: str | None = None
    """Result of the evaluation."""

    verbal_evaluation: str | None = None
    """Result of the verbal evaluation."""


@dataclass(kw_only=True)
class PutMultipleSignRequest(SkolaOnlineModel):
    """Bulk signing of marks of a student."""

    marks_id: list[MarkId]
    """Marks to sign."""


@dataclass(kw_only=True)
class RatingScale(SkolaOnlineModel):
    """Grade of the rating scale."""

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

    include_percent_from: bool
    """Whether the lower bound is included in the range."""

    include_percent_to: bool
    """Whether the upper bound is included in the range."""


@dataclass(kw_only=True)
class SingleMark(SkolaOnlineModel):
    """Detail of a single mark."""

    mark_date: datetime
    """Date the mark was given."""

    edit_date: datetime
    """Date the teacher entered or changed the mark."""

    theme: str | None = None
    """Topic of the evaluation."""

    mark_text: str | None = None
    """Mark for display."""

    verbal_evaluation: str | None = None
    """Verbal evaluation."""

    teacher_id: str
    """ID of the teacher who entered the mark."""

    type: str | None = None
    """Type of evaluation."""

    type_note: str | None = None
    """Description of the type of evaluation."""

    weight: float | None = None
    """Weight of the mark."""

    comment: str | None = None
    """Comment on the evaluation."""

    subject_id: str
    """ID of the subject."""

    is_points: bool
    """Whether the mark is expressed in points."""

    is_percents: bool
    """Whether the mark is expressed as a percentage."""

    calculated_mark_text: str | None = None
    """Calculated mark."""

    class_rank_text: str | None = None
    """Rank in the class for display."""

    value_to_average: str | None = None
    """Value used in the average."""

    class_average: str | None = None
    """Class average."""

    id: str
    """ID of the mark."""

    semester_id: str | None = None
    """ID of the semester."""

    lesson_id: str | None = None
    """ID of the lesson."""

    max_points: int | None = None
    """Maximum number of points."""

    signed_id: str | None = None
    """ID of the person who signed the mark."""

    signed_name: str | None = None
    """Full name of the person who signed the mark, surname first."""

    signed_date: datetime | None = None
    """Date the mark was signed."""

    teacher_abbrev: str | None = None
    """Abbreviation of the teacher."""

    teacher_first_name: str | None = None
    """First name of the teacher."""

    teacher_last_name: str | None = None
    """Surname of the teacher."""

    teacher_title_before: str | None = None
    """Title before the teacher name."""

    teacher_title_after: str | None = None
    """Title after the teacher name."""

    teacher_display_name: str | None = None
    """Full name for display."""

    subject_abbrev: str | None = None
    """Abbreviation of the subject."""

    subject_name: str | None = None
    """Name of the subject."""

    subject_kind: str | None = None
    """Kind of subject."""

    average_text: str | None = None
    """Average mark in the subject."""

    average_text_type: AssessmentMethod | None = None
    """Type of the average mark."""


@dataclass(kw_only=True)
class TeacherMarkResponse(SkolaOnlineModel):
    """Mark record created by a teacher."""

    subject: MarkSubject
    """Subject of the evaluation."""

    lesson_id: str | None = None
    """ID of the lesson."""

    method_evaluation: list[MethodEvaluation]
    """Available evaluation methods."""

    selected_method_evaluation: str
    """Evaluation method already set."""

    max_points: int | None = None
    """Maximum number of points."""

    students: list[MarkStudent]
    """Students."""


@dataclass(kw_only=True)
class TeacherMarkingStudent(SkolaOnlineModel):
    """Student that can be marked in a lesson."""

    id: str
    """ID of the student."""

    first_name: str | None = None
    """First name of the student."""

    last_name: str
    """Surname of the student."""

    display_name: str
    """Full name of the student."""

    cvtv: int | None = None
    """Number of the student in the class register."""

    class_id: str
    """ID of the class of the student."""

    class_name: str
    """Name of the class of the student."""

    do_not_evaluate_in_subject: bool
    """Whether the student is not evaluated in the subject because of an exemption or
    recognition."""

    is_studying_abroad: bool
    """Whether the student fulfills compulsory schooling abroad."""


@dataclass(kw_only=True)
class TeacherMarkingStudentsResponse(SkolaOnlineModel):
    """Students that can be marked in a lesson."""

    students: list[TeacherMarkingStudent]
    """Students."""


@dataclass(kw_only=True)
class TeacherMarksRequest(SkolaOnlineModel):
    """Updated mark record."""

    school_year_id: str
    """ID of the school year of the scheduled event."""

    semester_id: str
    """ID of the semester."""

    date_mark: datetime
    """Date of the evaluation."""

    other_date_mark: datetime | None = None
    """Different date when the evaluation took place."""

    lesson_id: str
    """ID of the lesson."""

    type_id: str
    """ID of the type of evaluation."""

    theme: str | None = None
    """Topic of the evaluation."""

    comment: str | None = None
    """Comment on the evaluation."""

    selected_method_evaluation: str
    """Selected evaluation method."""

    max_points: int | None = None
    """Maximum number of points for point evaluation."""

    students: list[PostTeacherMarksStudent]
    """Evaluated students."""


@dataclass(kw_only=True)
class TeacherMarksResponse(SkolaOnlineModel):
    """Mark records created by a teacher."""

    marks: TeacherMarkResponse | None = None
    """Mark records."""


@dataclass(kw_only=True)
class TypeEvaluation(SkolaOnlineModel):
    """Type of evaluation."""

    id: str
    """ID of the type of evaluation."""

    name: str
    """Name of the type of evaluation."""

    note: str | None = None
    """Description of the type of evaluation."""

    weight: float | None = None
    """Weight of the type of evaluation."""

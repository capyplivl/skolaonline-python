from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from skolaonline.models._base import SkolaOnlineModel


class Achievement(StrEnum):
    PASSED_WITH_HONORS = "passedWithHonors"
    PASSED = "passed"
    FAILED = "failed"
    NOT_EVALUATED = "notEvaluated"


class AssessmentMethod(StrEnum):
    MARKS = "marks"
    POINTS = "points"
    PERCENTAGES = "percentages"


class MarksListOrder(StrEnum):
    DATE_DESC = "dateDesc"
    DATE_ASC = "dateAsc"


class MarksListSigningFilter(StrEnum):
    ALL = "all"
    UNSIGNED = "unsigned"
    SIGNED = "signed"


@dataclass(kw_only=True)
class CertificateTerm(SkolaOnlineModel):
    final_marks: list[FinalMark]
    subjects: list[MarkSubject]
    grade_name: str
    grade: str
    school_year_name: str
    school_year_order: int | None = None
    semester_name: str
    semester_abbrev: str | None = None
    semester_order: int | None = None
    closed: bool | None = None
    achievement_text: str | None = None
    achievement: Achievement | None = None
    marks_average: float | None = None
    absent_hours: int | None = None
    excused_hours: int | None = None
    not_excused_hours: int | None = None
    final_verbal_evaluation: str | None = None


@dataclass(kw_only=True)
class FinalMark(SkolaOnlineModel):
    mark_date: datetime
    edit_date: datetime | None = None
    mark_text: str | None = None
    shortcut_to_display: str | None = None
    verbal_evaluation: str | None = None
    unclassified: bool
    released: bool
    unevaluated: bool
    recognized: bool
    has_verbal_evaluation: bool
    subject_id: str
    order: int | None = None


@dataclass(kw_only=True)
class FinalMarksResponse(SkolaOnlineModel):
    certificate_terms: list[CertificateTerm]


@dataclass(kw_only=True)
class Mark(SkolaOnlineModel):
    mark_date: datetime
    edit_date: datetime
    theme: str | None = None
    mark_text: str | None = None
    verbal_evaluation: str | None = None
    teacher_id: str
    type: str | None = None
    type_note: str | None = None
    weight: float | None = None
    comment: str | None = None
    subject_id: str
    is_points: bool
    is_percents: bool
    calculated_mark_text: str | None = None
    class_rank_text: str | None = None
    value_to_average: str | None = None
    class_average: str | None = None
    id: str
    semester_id: str | None = None
    lesson_id: str | None = None
    max_points: int | None = None
    signed_id: str | None = None
    signed_name: str | None = None
    signed_date: datetime | None = None


@dataclass(kw_only=True)
class MarkCodeListsResponse(SkolaOnlineModel):
    rating_scale: list[RatingScale]
    semester: list[MarkSemester]
    subjects: list[MarkSubject]
    signing: bool
    enabled_signing: bool
    lessons: list[MarkLesson]
    method_evaluation: list[MethodEvaluation]
    types_evaluation: list[TypeEvaluation]
    is_theme_required: bool
    enabled_class_rank: bool


@dataclass(kw_only=True)
class MarkId(SkolaOnlineModel):
    id: str


@dataclass(kw_only=True)
class MarkLesson(SkolaOnlineModel):
    id: str
    name: str
    begin_time: datetime
    end_time: datetime


@dataclass(kw_only=True)
class MarkSemester(SkolaOnlineModel):
    id: str
    parent_id: str
    name: str
    date_from: datetime
    date_to: datetime
    order: int
    lock_classification: bool
    date_lock_classification: datetime | None = None
    enabled_evaluate: bool


@dataclass(kw_only=True)
class MarkStudent(SkolaOnlineModel):
    id: str
    first_name: str | None = None
    last_name: str
    display_name: str
    cvtv: int | None = None
    class_id: str
    class_name: str
    plan_mark: bool
    mark_text: str | None = None
    verbal_evaluation: str | None = None
    do_not_evaluate_in_subject: bool
    is_studying_abroad: bool


@dataclass(kw_only=True)
class MarkSubject(SkolaOnlineModel):
    id: str
    abbrev: str | None = None
    name: str
    kind: str | None = None


@dataclass(kw_only=True)
class MarkTeacher(SkolaOnlineModel):
    id: str
    abbrev: str | None = None
    first_name: str | None = None
    last_name: str
    title_before: str | None = None
    title_after: str | None = None
    display_name: str | None = None


@dataclass(kw_only=True)
class MarkWithoutAverage(SkolaOnlineModel):
    mark_date: datetime
    edit_date: datetime
    theme: str | None = None
    mark_text: str | None = None
    verbal_evaluation: str | None = None
    weight: float | None = None
    subject_id: str
    is_points: bool
    is_percents: bool
    id: str
    semester_id: str | None = None
    lesson_id: str | None = None
    max_points: int | None = None
    signed_id: str | None = None
    signed_name: str | None = None
    signed_date: datetime | None = None


@dataclass(kw_only=True)
class MarksListResponse(SkolaOnlineModel):
    marks: list[MarkWithoutAverage]
    subjects: list[MarkSubject]


@dataclass(kw_only=True)
class MarksResponse(SkolaOnlineModel):
    subjects: list[MarksSubject]


@dataclass(kw_only=True)
class MarksSubject(SkolaOnlineModel):
    marks: list[Mark]
    subject: MarkSubject
    teachers: list[MarkTeacher]
    average_text: str | None = None
    average_text_type: AssessmentMethod | None = None


@dataclass(kw_only=True)
class MethodEvaluation(SkolaOnlineModel):
    id: str
    name: str


@dataclass(kw_only=True)
class PostTeacherMarksRequest(SkolaOnlineModel):
    school_year_id: str
    semester_id: str
    date_mark: datetime
    other_date_mark: datetime | None = None
    lesson_id: str
    type_id: str
    theme: str | None = None
    comment: str | None = None
    selected_method_evaluation: str
    max_points: int | None = None
    students: list[PostTeacherMarksStudent]
    udalost_id: str
    poradi: int


@dataclass(kw_only=True)
class PostTeacherMarksStudent(SkolaOnlineModel):
    id: str
    plan_mark: bool
    mark_text: str | None = None
    verbal_evaluation: str | None = None


@dataclass(kw_only=True)
class PutMultipleSignRequest(SkolaOnlineModel):
    marks_id: list[MarkId]


@dataclass(kw_only=True)
class RatingScale(SkolaOnlineModel):
    id: str
    name: str
    value: float | None = None
    percent_from: int | None = None
    percent_to: int | None = None
    include_percent_from: bool
    include_percent_to: bool


@dataclass(kw_only=True)
class SingleMark(SkolaOnlineModel):
    mark_date: datetime
    edit_date: datetime
    theme: str | None = None
    mark_text: str | None = None
    verbal_evaluation: str | None = None
    teacher_id: str
    type: str | None = None
    type_note: str | None = None
    weight: float | None = None
    comment: str | None = None
    subject_id: str
    is_points: bool
    is_percents: bool
    calculated_mark_text: str | None = None
    class_rank_text: str | None = None
    value_to_average: str | None = None
    class_average: str | None = None
    id: str
    semester_id: str | None = None
    lesson_id: str | None = None
    max_points: int | None = None
    signed_id: str | None = None
    signed_name: str | None = None
    signed_date: datetime | None = None
    teacher_abbrev: str | None = None
    teacher_first_name: str | None = None
    teacher_last_name: str | None = None
    teacher_title_before: str | None = None
    teacher_title_after: str | None = None
    teacher_display_name: str | None = None
    subject_abbrev: str | None = None
    subject_name: str | None = None
    subject_kind: str | None = None
    average_text: str | None = None
    average_text_type: AssessmentMethod | None = None


@dataclass(kw_only=True)
class TeacherMarkResponse(SkolaOnlineModel):
    subject: MarkSubject
    lesson_id: str | None = None
    method_evaluation: list[MethodEvaluation]
    selected_method_evaluation: str
    max_points: int | None = None
    students: list[MarkStudent]


@dataclass(kw_only=True)
class TeacherMarkingStudent(SkolaOnlineModel):
    id: str
    first_name: str | None = None
    last_name: str
    display_name: str
    cvtv: int | None = None
    class_id: str
    class_name: str
    do_not_evaluate_in_subject: bool
    is_studying_abroad: bool


@dataclass(kw_only=True)
class TeacherMarkingStudentsResponse(SkolaOnlineModel):
    students: list[TeacherMarkingStudent]


@dataclass(kw_only=True)
class TeacherMarksRequest(SkolaOnlineModel):
    school_year_id: str
    semester_id: str
    date_mark: datetime
    other_date_mark: datetime | None = None
    lesson_id: str
    type_id: str
    theme: str | None = None
    comment: str | None = None
    selected_method_evaluation: str
    max_points: int | None = None
    students: list[PostTeacherMarksStudent]


@dataclass(kw_only=True)
class TeacherMarksResponse(SkolaOnlineModel):
    marks: TeacherMarkResponse | None = None


@dataclass(kw_only=True)
class TypeEvaluation(SkolaOnlineModel):
    id: str
    name: str
    note: str | None = None
    weight: float | None = None

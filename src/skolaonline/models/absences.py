from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from skolaonline.models._base import SkolaOnlineModel
from skolaonline.models.common import IdName


class AbsenceInPeriodFilterState(StrEnum):
    ALL = "all"
    EXCUSED = "excused"
    UNEXCUSED = "unexcused"
    NOT_COUNTED = "notCounted"
    UNEVALUATED = "unevaluated"
    UNEVALUATED_WITH_APOLOGY = "unevaluatedWithApology"


class AbsenceInSubjectFilterOrder(StrEnum):
    DEFAULT = "default"
    BY_PERCENT = "byPercent"
    BY_HOURS = "byHours"
    ALPHABETICALLY = "alphabetically"


class AbsenceType(StrEnum):
    UNDEFINED = "undefined"
    UNEVALUATED = "unevaluated"
    EXCUSED = "excused"
    UNEXCUSED = "unexcused"
    NOT_COUNTED = "notCounted"
    UNEVALUATED_WITH_APOLOGY = "unevaluatedWithApology"


@dataclass(kw_only=True)
class AbsenceCodeListsResponse(SkolaOnlineModel):
    lessons: list[AbsenceLesson]
    semesters: list[AbsenceSemester]
    use_timetable: bool | None = None


@dataclass(kw_only=True)
class AbsenceInDayResponse(SkolaOnlineModel):
    message: str | None = None
    absences: list[AbsenceInLesson]


@dataclass(kw_only=True)
class AbsenceInLesson(SkolaOnlineModel):
    lesson_id: str
    absence_type: AbsenceType | None = None
    timetable_lesson: list[AbsenceTimetableLesson]


@dataclass(kw_only=True)
class AbsenceInPeriodResponse(SkolaOnlineModel):
    message: str | None = None
    absences: list[AbsenceNumbersInDay]


@dataclass(kw_only=True)
class AbsenceInSubject(SkolaOnlineModel):
    subject: AbsenceSubject
    absence_all: int | None = None
    absence_all_percentage: float | None = None
    number_of_hours: int | None = None
    number_of_excused: int | None = None
    number_of_unexcused: int | None = None
    number_of_not_counted: int | None = None
    number_of_unevaluated: int | None = None
    number_of_unevaluated_with_apology: int | None = None
    allowed_absence: int | None = None
    allowed_absence_decimal: float | None = None
    allowed_absence_percentage: float | None = None


@dataclass(kw_only=True)
class AbsenceInSubjectResponse(SkolaOnlineModel):
    summary_absence_all: int | None = None
    summary_number_of_hours: int | None = None
    summary_number_of_excused: int | None = None
    summary_number_of_unexcused: int | None = None
    summary_number_of_not_counted: int | None = None
    summary_number_of_unevaluated: int | None = None
    summary_number_of_unevaluated_with_apology: int | None = None
    subjects: list[AbsenceInSubject]


@dataclass(kw_only=True)
class AbsenceLesson(SkolaOnlineModel):
    id: str
    order: int
    name: str
    time_from: str
    time_to: str


@dataclass(kw_only=True)
class AbsenceNumbersInDay(SkolaOnlineModel):
    date: datetime | None = None
    number_of_excused: int | None = None
    number_of_unexcused: int | None = None
    number_of_not_counted: int | None = None
    number_of_unevaluated: int | None = None
    number_of_unevaluated_with_apology: int | None = None


@dataclass(kw_only=True)
class AbsenceSemester(SkolaOnlineModel):
    id: str
    parent_id: str
    name: str
    date_from: datetime
    date_to: datetime
    order: int
    lock_attendance: bool
    date_lock_attendance: datetime | None = None


@dataclass(kw_only=True)
class AbsenceSubject(SkolaOnlineModel):
    id: str
    name: str


@dataclass(kw_only=True)
class AbsenceTimetableLesson(SkolaOnlineModel):
    subject: str
    teachers: list[IdName]

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from skolaonline.models._base import SkolaOnlineModel
from skolaonline.models.common import IdName


class AbsenceInPeriodFilterState(StrEnum):
    """Absence state filter. Defaults to all absences."""

    ALL = "all"
    """All absences."""

    EXCUSED = "excused"
    """Excused."""

    UNEXCUSED = "unexcused"
    """Unexcused."""

    NOT_COUNTED = "notCounted"
    """Not counted."""

    UNEVALUATED = "unevaluated"
    """Not evaluated yet."""

    UNEVALUATED_WITH_APOLOGY = "unevaluatedWithApology"
    """Not evaluated yet, with an apology being processed by the teacher."""


class AbsenceInSubjectFilterOrder(StrEnum):
    """Sort order of absences by subject."""

    DEFAULT = "default"
    """Default order."""

    BY_PERCENT = "byPercent"
    """By absence percentage."""

    BY_HOURS = "byHours"
    """By number of absent lessons."""

    ALPHABETICALLY = "alphabetically"
    """Alphabetically."""


class AbsenceType(StrEnum):
    """Type of absence."""

    UNDEFINED = "undefined"
    """Not specified."""

    UNEVALUATED = "unevaluated"
    """Not evaluated yet."""

    EXCUSED = "excused"
    """Excused."""

    UNEXCUSED = "unexcused"
    """Unexcused."""

    NOT_COUNTED = "notCounted"
    """Not counted."""

    UNEVALUATED_WITH_APOLOGY = "unevaluatedWithApology"
    """Not evaluated yet, with an apology being processed by the teacher."""


@dataclass(kw_only=True)
class AbsenceCodeListsResponse(SkolaOnlineModel):
    """Code lists used by the absences module."""

    lessons: list[AbsenceLesson]
    """Lessons of the school day."""

    semesters: list[AbsenceSemester]
    """Semesters of the school year."""

    use_timetable: bool | None = None
    """Whether the organization has the timetable enabled."""


@dataclass(kw_only=True)
class AbsenceInDayResponse(SkolaOnlineModel):
    """Absences on a single day."""

    message: str | None = None
    """Warning for the user when a non-essential part of the operation failed."""

    absences: list[AbsenceInLesson]
    """Absences in the individual periods of the day."""


@dataclass(kw_only=True)
class AbsenceInLesson(SkolaOnlineModel):
    """Absence in a period of the day."""

    lesson_id: str
    """ID of the period of the day."""

    absence_type: AbsenceType | None = None
    """Type of absence."""

    timetable_lesson: list[AbsenceTimetableLesson]
    """Lesson taking place in the period of the day."""


@dataclass(kw_only=True)
class AbsenceInPeriodResponse(SkolaOnlineModel):
    """Absences in a date range."""

    message: str | None = None
    """Warning for the user when a non-essential part of the operation failed."""

    absences: list[AbsenceNumbersInDay]
    """Absences on the individual days."""


@dataclass(kw_only=True)
class AbsenceInSubject(SkolaOnlineModel):
    """Absence in a subject."""

    subject: AbsenceSubject
    """Subject."""

    absence_all: int | None = None
    """Total absence in the subject."""

    absence_all_percentage: float | None = None
    """Total absence in the subject as a percentage."""

    number_of_hours: int | None = None
    """Number of scheduled lessons in the subject."""

    number_of_excused: int | None = None
    """Number of excused lessons in the subject."""

    number_of_unexcused: int | None = None
    """Number of unexcused lessons in the subject."""

    number_of_not_counted: int | None = None
    """Number of lessons not counted in the subject."""

    number_of_unevaluated: int | None = None
    """Number of lessons not evaluated yet in the subject."""

    number_of_unevaluated_with_apology: int | None = None
    """Number of lessons not evaluated yet with an apology being processed by the
    teacher."""

    allowed_absence: int | None = None
    """Allowed absence in the subject."""

    allowed_absence_decimal: float | None = None
    """Allowed absence in the subject with decimal precision."""

    allowed_absence_percentage: float | None = None
    """Allowed absence in the subject as a percentage."""


@dataclass(kw_only=True)
class AbsenceInSubjectResponse(SkolaOnlineModel):
    """Absences grouped by subject."""

    summary_absence_all: int | None = None
    """Total absence across all subjects."""

    summary_number_of_hours: int | None = None
    """Total number of scheduled lessons across all subjects."""

    summary_number_of_excused: int | None = None
    """Total number of excused lessons across all subjects."""

    summary_number_of_unexcused: int | None = None
    """Total number of unexcused lessons across all subjects."""

    summary_number_of_not_counted: int | None = None
    """Total number of lessons not counted across all subjects."""

    summary_number_of_unevaluated: int | None = None
    """Total number of lessons not evaluated yet across all subjects."""

    summary_number_of_unevaluated_with_apology: int | None = None
    """Total number of lessons not evaluated yet with an apology being processed,
    across all subjects."""

    subjects: list[AbsenceInSubject]
    """Absences in the individual subjects."""


@dataclass(kw_only=True)
class AbsenceLesson(SkolaOnlineModel):
    """Lesson of the school day."""

    id: str
    """ID of the lesson."""

    order: int
    """Order of the lesson in the school day."""

    name: str
    """Name of the lesson."""

    time_from: str
    """Start time of the lesson."""

    time_to: str
    """End time of the lesson."""


@dataclass(kw_only=True)
class AbsenceNumbersInDay(SkolaOnlineModel):
    """Absence counts on a single day."""

    date: datetime | None = None
    """Date."""

    number_of_excused: int | None = None
    """Number of excused lessons."""

    number_of_unexcused: int | None = None
    """Number of unexcused lessons."""

    number_of_not_counted: int | None = None
    """Number of lessons not counted."""

    number_of_unevaluated: int | None = None
    """Number of lessons not evaluated yet."""

    number_of_unevaluated_with_apology: int | None = None
    """Number of lessons not evaluated yet with an apology being processed by the
    teacher."""


@dataclass(kw_only=True)
class AbsenceSemester(SkolaOnlineModel):
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

    lock_attendance: bool
    """Whether attendance is locked after the attendance closing date."""

    date_lock_attendance: datetime | None = None
    """Attendance closing date."""


@dataclass(kw_only=True)
class AbsenceSubject(SkolaOnlineModel):
    """Subject information."""

    id: str
    """ID of the subject."""

    name: str
    """Name of the subject."""


@dataclass(kw_only=True)
class AbsenceTimetableLesson(SkolaOnlineModel):
    """Lesson taking place in the period of the day."""

    subject: str
    """Taught subject."""

    teachers: list[IdName]
    """Teachers of the lesson."""

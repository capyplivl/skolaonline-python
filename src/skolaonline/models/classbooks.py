from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import ClassVar

from skolaonline.models._base import SkolaOnlineModel
from skolaonline.models.timetable import TimetableNumberOfHour


@dataclass(kw_only=True)
class CalculatedNumberOfHourResponse(SkolaOnlineModel):
    """Calculated numbering of taught lessons."""

    calculated_number_of_hours: list[TimetableNumberOfHour]
    """Calculated numbers of taught lessons."""


@dataclass(kw_only=True)
class ClassbookClass(SkolaOnlineModel):
    """Class of a class book entry."""

    id: str
    """ID of the class."""

    name: str
    """Name of the class."""

    description: str | None = None
    """Description of the class."""


@dataclass(kw_only=True)
class ClassbookDay(SkolaOnlineModel):
    """Class book entries on a single day."""

    date: datetime
    """Date of the entry."""

    school_year_id: str
    """ID of the school year."""

    hours: list[ClassbookHour]
    """Class book entries."""


@dataclass(kw_only=True)
class ClassbookGroup(SkolaOnlineModel):
    """Group of a class book entry."""

    id: str
    """ID of the group."""

    name: str
    """Name of the group."""

    description: str | None = None
    """Description of the group."""


@dataclass(kw_only=True)
class ClassbookHour(SkolaOnlineModel):
    """Class book entry for a lesson."""

    _field_aliases: ClassVar[dict[str, str]] = {
        "udalost_id": "udalost_Id",
    }

    udalost_id: str | None = None
    """ID of the scheduled event."""

    poradi: int | None = None
    """Order of the scheduled event."""

    id: str
    """ID of the class book entry."""

    lesson_id: str
    """ID of the lesson."""

    number_lessons: int | None = None
    """Number of lessons."""

    label: str | None = None
    """Label of the lesson."""

    private_notice: str | None = None
    """Note."""

    teaching_informations: list[ClassbookTeachingInformation]
    """Teaching information."""

    theme: str | None = None
    """Topic taught."""

    number_of_hour: int | None = None
    """Number of taught lessons."""

    subject: ClassbookSubject | None = None
    """Taught subject."""

    class_: ClassbookClass
    """Class of the entry."""

    groups: list[ClassbookGroup]
    """Groups of the class of the entry."""


@dataclass(kw_only=True)
class ClassbookLesson(SkolaOnlineModel):
    """Lesson of the school day."""

    id: str
    """ID of the lesson."""

    caption: str
    """Label of the lesson."""

    begin_time: str
    """Start time of the lesson."""

    end_time: str
    """End time of the lesson."""


@dataclass(kw_only=True)
class ClassbookSubject(SkolaOnlineModel):
    """Subject of a class book entry."""

    id: str
    """ID of the subject."""

    abbrev: str | None = None
    """Abbreviation of the subject."""

    name: str
    """Name of the subject."""


@dataclass(kw_only=True)
class ClassbookTeachingInformation(SkolaOnlineModel):
    """Teaching information for a class or group."""

    class_id: str
    """ID of the class the information is meant for."""

    group_id: str
    """ID of the group the information is meant for."""

    information: str | None = None
    """Teaching information."""


@dataclass(kw_only=True)
class ClassbooksResponse(SkolaOnlineModel):
    """Class book entries of a class."""

    days: list[ClassbookDay]
    """Entries of the class on the individual days."""

    lessons: list[ClassbookLesson]
    """All lessons of the school day."""


@dataclass(kw_only=True)
class PostClassbookAttendanceLesson(SkolaOnlineModel):
    """Attendance of a student in a lesson."""

    id: str | None = None
    """ID of the lesson."""

    attendance: str | None = None
    """Attendance code: A for absent, O for excused absence, N for unexcused absence,
    S for absence not counted, P for present. Empty or null when attendance is not
    entered."""

    reason_for_absence: str | None = None
    """ID of the reason for absence."""


@dataclass(kw_only=True)
class PostClassbookAttendanceRequest(SkolaOnlineModel):
    """Attendance of students in a scheduled event."""

    school_year_id: str
    """ID of the school year."""

    udalost_id: str
    """ID of the scheduled event."""

    poradi: int
    """Order of the scheduled event."""

    students: list[PostClassbookAttendanceStudent]
    """Students."""


@dataclass(kw_only=True)
class PostClassbookAttendanceStudent(SkolaOnlineModel):
    """Attendance of a student."""

    id: str | None = None
    """ID of the student."""

    lessons: list[PostClassbookAttendanceLesson]
    """Lessons of the scheduled event."""


@dataclass(kw_only=True)
class PostClassbookClass(SkolaOnlineModel):
    """Class of a new class book entry."""

    id: str
    """ID of the class."""


@dataclass(kw_only=True)
class PostClassbookEntry(SkolaOnlineModel):
    """Class book entry to save."""

    lesson_id: str
    """ID of the lesson."""

    private_notice: str | None = None
    """Note."""

    theme: str | None = None
    """Topic taught."""

    number_of_hour: int | None = None
    """Number of taught lessons."""

    classes: list[PostClassbookClass]
    """Classes."""

    groups: list[PostClassbookGroup]
    """Groups."""


@dataclass(kw_only=True)
class PostClassbookGroup(SkolaOnlineModel):
    """Group of a new class book entry."""

    class_id: str
    """ID of the class."""

    id: str
    """ID of the group."""


@dataclass(kw_only=True)
class PostClassbooksRequest(SkolaOnlineModel):
    """Class book entries to save for a day."""

    date: datetime
    """Date of the entry."""

    school_year_id: str
    """ID of the school year."""

    subject_id: str | None = None
    """ID of the subject."""

    scheduled_event: ScheduledEventKey | None = None
    """Identification of the scheduled event."""

    entries: list[PostClassbookEntry] | None = None
    """Class book entries."""


@dataclass(kw_only=True)
class ScheduledEventKey(SkolaOnlineModel):
    """Identification of the scheduled event."""

    event_id: str | None = None
    """ID of the scheduled event."""

    event_order: int | None = None
    """Order of the scheduled event."""

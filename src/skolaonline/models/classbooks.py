from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import ClassVar

from skolaonline.models._base import SkolaOnlineModel
from skolaonline.models.timetable import TimetableNumberOfHour


@dataclass(kw_only=True)
class CalculatedNumberOfHourResponse(SkolaOnlineModel):
    calculated_number_of_hours: list[TimetableNumberOfHour]


@dataclass(kw_only=True)
class ClassbookClass(SkolaOnlineModel):
    id: str
    name: str
    description: str | None = None


@dataclass(kw_only=True)
class ClassbookDay(SkolaOnlineModel):
    date: datetime
    school_year_id: str
    hours: list[ClassbookHour]


@dataclass(kw_only=True)
class ClassbookGroup(SkolaOnlineModel):
    id: str
    name: str
    description: str | None = None


@dataclass(kw_only=True)
class ClassbookHour(SkolaOnlineModel):
    _field_aliases: ClassVar[dict[str, str]] = {
        "udalost_id": "udalost_Id",
    }

    udalost_id: str | None = None
    poradi: int | None = None
    id: str
    lesson_id: str
    number_lessons: int | None = None
    label: str | None = None
    private_notice: str | None = None
    teaching_informations: list[ClassbookTeachingInformation]
    theme: str | None = None
    number_of_hour: int | None = None
    subject: ClassbookSubject | None = None
    class_: ClassbookClass
    groups: list[ClassbookGroup]


@dataclass(kw_only=True)
class ClassbookLesson(SkolaOnlineModel):
    id: str
    caption: str
    begin_time: str
    end_time: str


@dataclass(kw_only=True)
class ClassbookSubject(SkolaOnlineModel):
    id: str
    abbrev: str | None = None
    name: str


@dataclass(kw_only=True)
class ClassbookTeachingInformation(SkolaOnlineModel):
    class_id: str
    group_id: str
    information: str | None = None


@dataclass(kw_only=True)
class ClassbooksResponse(SkolaOnlineModel):
    days: list[ClassbookDay]
    lessons: list[ClassbookLesson]


@dataclass(kw_only=True)
class PostClassbookAttendanceLesson(SkolaOnlineModel):
    id: str | None = None
    attendance: str | None = None
    reason_for_absence: str | None = None


@dataclass(kw_only=True)
class PostClassbookAttendanceRequest(SkolaOnlineModel):
    school_year_id: str
    udalost_id: str
    poradi: int
    students: list[PostClassbookAttendanceStudent]


@dataclass(kw_only=True)
class PostClassbookAttendanceStudent(SkolaOnlineModel):
    id: str | None = None
    lessons: list[PostClassbookAttendanceLesson]


@dataclass(kw_only=True)
class PostClassbookClass(SkolaOnlineModel):
    id: str


@dataclass(kw_only=True)
class PostClassbookEntry(SkolaOnlineModel):
    lesson_id: str
    private_notice: str | None = None
    theme: str | None = None
    number_of_hour: int | None = None
    classes: list[PostClassbookClass]
    groups: list[PostClassbookGroup]


@dataclass(kw_only=True)
class PostClassbookGroup(SkolaOnlineModel):
    class_id: str
    id: str


@dataclass(kw_only=True)
class PostClassbooksRequest(SkolaOnlineModel):
    date: datetime
    school_year_id: str
    subject_id: str | None = None
    scheduled_event: ScheduledEventKey | None = None
    entries: list[PostClassbookEntry] | None = None


@dataclass(kw_only=True)
class ScheduledEventKey(SkolaOnlineModel):
    event_id: str | None = None
    event_order: int | None = None

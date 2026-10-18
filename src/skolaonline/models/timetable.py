from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import ClassVar

from skolaonline.models._base import SkolaOnlineModel
from skolaonline.models.common import GroupKind, IdName, IdNameDesc, SubjectKind
from skolaonline.models.marks import MethodEvaluation


class AttendanceType(StrEnum):
    UNEVALUATED_ABSENCE = "a"
    UNEXCUSED_ABSENCE = "n"
    EXCUSED_ABSENCE = "o"
    UNCOUNTED_ABSENCE = "s"
    PRESENT = "p"


class TimetableContexMenuItem(StrEnum):
    CLASS_BOOK = "classBook"
    NEW_MARK = "newMark"
    NOTE_CLASS_BOOK = "noteClassBook"
    TEACHING_INFORMATION = "teachingInformation"
    NEW_MESSAGE = "newMessage"


@dataclass(kw_only=True)
class ClassroomDutyPerson(SkolaOnlineModel):
    name: str
    id: str


@dataclass(kw_only=True)
class Day(SkolaOnlineModel):
    school_year_id: str
    date: datetime
    schedules: list[ScheduledHour]
    classroom_duty: list[ClassroomDutyPerson] | None = None
    monitorings: list[MonitoringHour]
    emergencies: list[EmergencyHour]
    teaching_informations: list[TimetableTeachingInformation]
    evaluations: list[Evaluation]


@dataclass(kw_only=True)
class DetailHour(SkolaOnlineModel):
    id: str
    name: str
    order: float
    time_from: str
    timeto: str


@dataclass(kw_only=True)
class EmergencyHour(SkolaOnlineModel):
    emergency_id: str
    emergency_order: int
    lesson_id: str
    begin_time: datetime
    end_time: datetime
    hour_type: HourType
    hour_colour: str
    hour_colour_text: str
    teacher: TimetableTeacher


@dataclass(kw_only=True)
class Evaluation(SkolaOnlineModel):
    evaluation_id: str
    lesson_id: str
    scheduled_hour_id: str | None = None
    type: IdNameDesc
    theme: str | None = None
    weight: float
    comment: str | None = None
    entred: bool
    value_to_display: str
    value_to_average: str | None = None
    verbal_evaluation: str | None = None
    teacher: IdName
    evaluation_date: datetime
    school_year_id: str
    semester_id: str
    subject_name: str | None = None
    evaluation_method: str | None = None
    max_points: int | None = None


@dataclass(kw_only=True)
class Group(SkolaOnlineModel):
    id: str
    name: str
    kind: GroupKind
    class_id: str
    class_name: str


@dataclass(kw_only=True)
class HourKind(SkolaOnlineModel):
    id: str
    name: str
    description: str


@dataclass(kw_only=True)
class HourType(SkolaOnlineModel):
    id: str
    description: str
    display_name: str | None = None


@dataclass(kw_only=True)
class KindEvaluation(SkolaOnlineModel):
    id: str
    name: str
    description: str | None = None
    valid: bool
    order: int | None = None
    weight: float | None = None


@dataclass(kw_only=True)
class MonitoringHour(SkolaOnlineModel):
    monitoring_id: str
    lesson_id_from: str
    lesson_id_to: str
    begin_time: datetime
    end_time: datetime
    hour_type: HourType
    hour_kind: HourKind
    hour_colour: str
    hour_colour_text: str
    room: Room
    teacher: TimetableTeacher


@dataclass(kw_only=True)
class OrderlyServiceStudent(SkolaOnlineModel):
    date_from: datetime
    date_to: datetime
    class_id: str
    class_name: str
    student_id: str
    first_name: str | None = None
    lastname: str
    cvtv: str | None = None


@dataclass(kw_only=True)
class ReasonAbsence(SkolaOnlineModel):
    id: str
    name: str
    valid: bool
    order: int | None = None


@dataclass(kw_only=True)
class Room(SkolaOnlineModel):
    id: str
    abbrev: str
    name: str | None = None


@dataclass(kw_only=True)
class ScheduledHour(SkolaOnlineModel):
    scheduled_hour_id: str
    scheduled_hour_order: int
    lesson_id_from: str
    lesson_id_to: str
    begin_time: datetime
    end_time: datetime
    hour_type: HourType
    hour_kind: HourKind
    cycle: str | None = None
    subject: TimetableSubject | None = None
    hour_colour: str
    hour_colour_text: str
    groups: list[Group]
    rooms: list[Room]
    teachers: list[TimetableTeacher]
    context_menu: list[TimetableContexMenuItem]
    on_line_meeting: bool
    entry_class_book: bool | None = None
    detail_hours: list[DetailHour]
    orderly_service: list[OrderlyServiceStudent]
    title: str | None = None
    description: str | None = None


@dataclass(kw_only=True)
class SchoolYear(SkolaOnlineModel):
    school_year_id: str
    date_from: datetime
    date_to: datetime


@dataclass(kw_only=True)
class TimetableCodeListsResponse(SkolaOnlineModel):
    _field_aliases: ClassVar[dict[str, str]] = {
        "enabled_state_ons": "enabledStateONS",
    }

    semester: list[TimetableSemester]
    show_weekend: bool
    school_year: SchoolYear | None = None
    reason_absence: list[ReasonAbsence]
    kind_evaluation: list[KindEvaluation]
    method_evaluation: list[MethodEvaluation]
    symbol_attendance: str
    enabled_state_ons: bool
    required_number_of_lessons: bool


@dataclass(kw_only=True)
class TimetableDetailData(SkolaOnlineModel):
    class_: list[IdName]
    groups: list[IdName]
    lesson: list[IdName]
    theme: str | None = None
    private_notice: str | None = None
    number_of_hour: int | None = None


@dataclass(kw_only=True)
class TimetableDetailLesson(SkolaOnlineModel):
    id: str
    attendance: AttendanceType | None = None
    reason_for_absence: str | None = None


@dataclass(kw_only=True)
class TimetableDetailResponse(SkolaOnlineModel):
    data: list[TimetableDetailData]
    students: list[TimetableDetailStudent]
    without_entry_class_book: str | None = None
    substitutes_for: str | None = None
    substituted_by: str | None = None
    last_lesson_in_room: bool | None = None
    school_event_details: list[str] | None = None
    public_information: str | None = None


@dataclass(kw_only=True)
class TimetableDetailStudent(SkolaOnlineModel):
    student: TimetableStudent
    lessons: list[TimetableDetailLesson]
    before_lesson_attendance: AttendanceType | None = None
    after_lesson_attendance: AttendanceType | None = None


@dataclass(kw_only=True)
class TimetableGroupId(SkolaOnlineModel):
    group_id: str


@dataclass(kw_only=True)
class TimetableLesson(SkolaOnlineModel):
    id: str
    caption: str
    begin_time: datetime
    end_time: datetime


@dataclass(kw_only=True)
class TimetableNumberOfHour(SkolaOnlineModel):
    lesson_id: str
    class_id: str
    group_ids: list[TimetableGroupId]
    number_of_hour: int


@dataclass(kw_only=True)
class TimetableResponse(SkolaOnlineModel):
    days: list[Day]
    lessons: list[TimetableLesson]


@dataclass(kw_only=True)
class TimetableSemester(SkolaOnlineModel):
    id: str
    parent_id: str
    name: str
    date_from: datetime
    date_to: datetime
    order: int


@dataclass(kw_only=True)
class TimetableStudent(SkolaOnlineModel):
    id: str
    first_name: str | None = None
    lastname: str
    display_name: str
    cvtv: int | None = None
    class_id: str
    groups: list[TimetableStudentGroup] | None = None
    do_not_enter_attendance_in_subject: bool
    is_studying_abroad: bool
    is_studying_at_home: bool
    is_participating_school_event: bool


@dataclass(kw_only=True)
class TimetableStudentGroup(SkolaOnlineModel):
    group_id: str


@dataclass(kw_only=True)
class TimetableSubject(SkolaOnlineModel):
    id: str
    abbrev: str | None = None
    name: str
    kind: SubjectKind | None = None


@dataclass(kw_only=True)
class TimetableTeacher(SkolaOnlineModel):
    id: str
    abbrev: str | None = None
    name: str | None = None
    surname: str
    display_name: str


@dataclass(kw_only=True)
class TimetableTeachingInformation(SkolaOnlineModel):
    teaching_information_id: str
    lesson_id: str
    teacher_name: str | None = None
    information: str
    hour_type: HourType
    subject: TimetableSubject | None = None
    groups: list[Group] | None = None

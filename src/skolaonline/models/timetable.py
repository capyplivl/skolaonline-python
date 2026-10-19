from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import ClassVar

from skolaonline.models._base import SkolaOnlineModel
from skolaonline.models.common import GroupKind, IdName, IdNameDesc, SubjectKind
from skolaonline.models.marks import MethodEvaluation


class AttendanceType(StrEnum):
    """Attendance of a student in a lesson."""

    UNEVALUATED_ABSENCE = "a"
    """Absence not evaluated yet."""

    UNEXCUSED_ABSENCE = "n"
    """Unexcused absence."""

    EXCUSED_ABSENCE = "o"
    """Excused absence."""

    UNCOUNTED_ABSENCE = "s"
    """Absence not counted."""

    PRESENT = "p"
    """Present."""


class TimetableContexMenuItem(StrEnum):
    """Action in the context menu of a scheduled event."""

    CLASS_BOOK = "classBook"
    """Open the class book."""

    NEW_MARK = "newMark"
    """Enter a new mark."""

    NOTE_CLASS_BOOK = "noteClassBook"
    """Enter a class book note."""

    TEACHING_INFORMATION = "teachingInformation"
    """Enter teaching information."""

    NEW_MESSAGE = "newMessage"
    """Write a new message."""


@dataclass(kw_only=True)
class ClassroomDutyPerson(SkolaOnlineModel):
    """Student on classroom duty."""

    name: str
    """Name of the person on classroom duty."""

    id: str
    """ID of the person on classroom duty."""


@dataclass(kw_only=True)
class Day(SkolaOnlineModel):
    """Timetable of a single day."""

    school_year_id: str
    """ID of the school year of the scheduled event."""

    date: datetime
    """Date of the day."""

    schedules: list[ScheduledHour]
    """Scheduled events of the day, such as lessons, substitutions, general events
    and school events."""

    classroom_duty: list[ClassroomDutyPerson] | None = None
    """Classroom duty of the day."""

    monitorings: list[MonitoringHour]
    """Supervisions of the day."""

    emergencies: list[EmergencyHour]
    """Standby duties of the day."""

    teaching_informations: list[TimetableTeachingInformation]
    """Teaching information of the day."""

    evaluations: list[Evaluation]
    """Evaluations of the day."""


@dataclass(kw_only=True)
class DetailHour(SkolaOnlineModel):
    """Lesson covered by a scheduled event."""

    id: str
    """ID of the lesson."""

    name: str
    """Display name of the lesson."""

    order: float
    """Order of the lesson in the school day."""

    time_from: str
    """Start time of the lesson."""

    timeto: str
    """End time of the lesson."""


@dataclass(kw_only=True)
class EmergencyHour(SkolaOnlineModel):
    """Standby duty of a teacher."""

    emergency_id: str
    """ID of the event."""

    emergency_order: int
    """Order of the event."""

    lesson_id: str
    """ID of the lesson."""

    begin_time: datetime
    """Start time of the standby duty."""

    end_time: datetime
    """End time of the standby duty."""

    hour_type: HourType
    """Type of the event."""

    hour_colour: str
    """Color of the standby duty."""

    hour_colour_text: str
    """Text color of the standby duty."""

    teacher: TimetableTeacher
    """Teacher."""


@dataclass(kw_only=True)
class Evaluation(SkolaOnlineModel):
    """Evaluation in a lesson."""

    evaluation_id: str
    """ID of the evaluation."""

    lesson_id: str
    """ID of the lesson."""

    scheduled_hour_id: str | None = None
    """ID of the scheduled event."""

    type: IdNameDesc
    """Type of evaluation."""

    theme: str | None = None
    """Topic of the evaluation."""

    weight: float
    """Weight of the mark."""

    comment: str | None = None
    """Comment on the evaluation."""

    entred: bool
    """Whether an evaluation is entered. Used to show an icon."""

    value_to_display: str
    """Value shown for the evaluation."""

    value_to_average: str | None = None
    """Value used in the average."""

    verbal_evaluation: str | None = None
    """Verbal evaluation."""

    teacher: IdName
    """Teacher who entered the evaluation."""

    evaluation_date: datetime
    """Date of the evaluation."""

    school_year_id: str
    """ID of the school year."""

    semester_id: str
    """Semester the evaluation counts towards."""

    subject_name: str | None = None
    """Subject of the evaluation."""

    evaluation_method: str | None = None
    """Evaluation method: Marks, Percent or Points."""

    max_points: int | None = None
    """Maximum number of points."""


@dataclass(kw_only=True)
class Group(SkolaOnlineModel):
    """Class, group or seminar of a scheduled event."""

    id: str
    """ID of the class, group or seminar."""

    name: str
    """Name of the class, group or seminar."""

    kind: GroupKind
    """Kind of the group."""

    class_id: str
    """ID of the class."""

    class_name: str
    """Name of the class."""


@dataclass(kw_only=True)
class HourKind(SkolaOnlineModel):
    """Kind of scheduled event."""

    id: str
    """ID of the kind of scheduled event."""

    name: str
    """Name of the kind of scheduled event."""

    description: str
    """Description of the kind of scheduled event."""


@dataclass(kw_only=True)
class HourType(SkolaOnlineModel):
    """Type of scheduled event."""

    id: str
    """ID of the type of scheduled event."""

    description: str
    """Description of the type of scheduled event."""

    display_name: str | None = None
    """Detailed identification of the scheduled event."""


@dataclass(kw_only=True)
class KindEvaluation(SkolaOnlineModel):
    """Kind of evaluation."""

    id: str
    """ID of the type of evaluation."""

    name: str
    """Name of the type of evaluation."""

    description: str | None = None
    """Description of the type of evaluation."""

    valid: bool
    """Whether the kind of evaluation is valid."""

    order: int | None = None
    """Order of the kind of evaluation."""

    weight: float | None = None
    """Weight of the evaluation."""


@dataclass(kw_only=True)
class MonitoringHour(SkolaOnlineModel):
    """Supervision duty of a teacher."""

    monitoring_id: str
    """ID of the supervision."""

    lesson_id_from: str
    """ID of the first period of the supervision."""

    lesson_id_to: str
    """ID of the last period of the supervision."""

    begin_time: datetime
    """Start time of the supervision."""

    end_time: datetime
    """End time of the supervision."""

    hour_type: HourType
    """Type of the scheduled event."""

    hour_kind: HourKind
    """Kind of the scheduled event."""

    hour_colour: str
    """Color of the scheduled event."""

    hour_colour_text: str
    """Text color of the scheduled event."""

    room: Room
    """Place of the supervision."""

    teacher: TimetableTeacher
    """Supervising teachers."""


@dataclass(kw_only=True)
class OrderlyServiceStudent(SkolaOnlineModel):
    """Student on orderly service."""

    date_from: datetime
    """First day of the orderly service."""

    date_to: datetime
    """Last day of the orderly service."""

    class_id: str
    """ID of the class."""

    class_name: str
    """Name of the class."""

    student_id: str
    """ID of the student."""

    first_name: str | None = None
    """First name of the student."""

    lastname: str
    """Surname of the student."""

    cvtv: str | None = None
    """Number of the student in the class register."""


@dataclass(kw_only=True)
class ReasonAbsence(SkolaOnlineModel):
    """Reason for absence."""

    id: str
    """ID of the reason for absence."""

    name: str
    """Text of the reason for absence."""

    valid: bool
    """Whether the reason for absence is valid."""

    order: int | None = None
    """Display order of the reason for absence."""


@dataclass(kw_only=True)
class Room(SkolaOnlineModel):
    """Room of a scheduled event."""

    id: str
    """ID of the room."""

    abbrev: str
    """Abbreviation of the room."""

    name: str | None = None
    """Name of the room."""


@dataclass(kw_only=True)
class ScheduledHour(SkolaOnlineModel):
    """Scheduled event in the timetable, such as a lesson, substitution or school
    event."""

    scheduled_hour_id: str
    """ID of the scheduled event."""

    scheduled_hour_order: int
    """Order of the scheduled event."""

    lesson_id_from: str
    """ID of the first lesson."""

    lesson_id_to: str
    """ID of the last lesson."""

    begin_time: datetime
    """Start time of the scheduled event."""

    end_time: datetime
    """End time of the scheduled event."""

    hour_type: HourType
    """Type of the scheduled event."""

    hour_kind: HourKind
    """Kind of the scheduled event."""

    cycle: str | None = None
    """Workload cycle of the scheduled event."""

    subject: TimetableSubject | None = None
    """Subject of the scheduled event."""

    hour_colour: str
    """Color of the scheduled event."""

    hour_colour_text: str
    """Text color of the scheduled event."""

    groups: list[Group]
    """Classes, groups and seminars of the scheduled event."""

    rooms: list[Room]
    """Rooms of the scheduled event."""

    teachers: list[TimetableTeacher]
    """Teachers of the scheduled event."""

    context_menu: list[TimetableContexMenuItem]
    """Context menu actions available to the signed-in teacher."""

    on_line_meeting: bool
    """Whether the scheduled event is an online meeting."""

    entry_class_book: bool | None = None
    """Whether the scheduled event has a class book entry."""

    detail_hours: list[DetailHour]
    """Individual lessons of a multi-lesson event, used for class book entries per
    lesson."""

    orderly_service: list[OrderlyServiceStudent]
    """Students on orderly service from the classes of the scheduled event."""

    title: str | None = None
    """Name of the event."""

    description: str | None = None
    """Description of the event."""


@dataclass(kw_only=True)
class SchoolYear(SkolaOnlineModel):
    """School year."""

    school_year_id: str
    """ID of the school year."""

    date_from: datetime
    """First day of the school year."""

    date_to: datetime
    """Last day of the school year."""


@dataclass(kw_only=True)
class TimetableCodeListsResponse(SkolaOnlineModel):
    """Code lists used by the timetable module."""

    _field_aliases: ClassVar[dict[str, str]] = {
        "enabled_state_ons": "enabledStateONS",
    }

    semester: list[TimetableSemester]
    """Semesters of the school year."""

    show_weekend: bool
    """Whether Saturday and Sunday are shown, based on the user setting."""

    school_year: SchoolYear | None = None
    """Default school year."""

    reason_absence: list[ReasonAbsence]
    """Reasons for absence."""

    kind_evaluation: list[KindEvaluation]
    """Types of evaluation."""

    method_evaluation: list[MethodEvaluation]
    """Available evaluation methods."""

    symbol_attendance: str
    """Symbols for presence and absence in the class book. PRITOMEN_NEPRITOMEN means
    - is present and / is absent, NEPRITOMEN_PRITOMEN means the opposite."""

    enabled_state_ons: bool
    """Whether all teachers can enter the O, N and S attendance states. ANO allows
    them, NE does not."""

    required_number_of_lessons: bool
    """Whether the lesson number can be entered in class book entries."""


@dataclass(kw_only=True)
class TimetableDetailData(SkolaOnlineModel):
    """Class book data of a scheduled event."""

    class_: list[IdName]
    """Class."""

    groups: list[IdName]
    """Groups and seminars of the class."""

    lesson: list[IdName]
    """ID of the lesson."""

    theme: str | None = None
    """Topic taught."""

    private_notice: str | None = None
    """Note, such as safety training or EU project information."""

    number_of_hour: int | None = None
    """Number of taught lessons."""


@dataclass(kw_only=True)
class TimetableDetailLesson(SkolaOnlineModel):
    """Attendance of a student in a lesson of a scheduled event."""

    id: str
    """ID of the lesson."""

    attendance: AttendanceType | None = None
    """Attendance set for the student."""

    reason_for_absence: str | None = None
    """ID of the reason for absence."""


@dataclass(kw_only=True)
class TimetableDetailResponse(SkolaOnlineModel):
    """Detail of a scheduled event."""

    data: list[TimetableDetailData]
    """Class book entries of the scheduled event."""

    students: list[TimetableDetailStudent]
    """Students of the scheduled event."""

    without_entry_class_book: str | None = None
    """Previous lesson that has no class book entry."""

    substitutes_for: str | None = None
    """Lesson that this event substitutes."""

    substituted_by: str | None = None
    """Lessons substituting this event."""

    last_lesson_in_room: bool | None = None
    """Last lesson in the room."""

    school_event_details: list[str] | None = None
    """School event taking place at the same time that students participate in."""

    public_information: str | None = None
    """Public note on the school event in HTML."""


@dataclass(kw_only=True)
class TimetableDetailStudent(SkolaOnlineModel):
    """Student of a scheduled event."""

    student: TimetableStudent
    """Student."""

    lessons: list[TimetableDetailLesson]
    """Lessons of the scheduled event."""

    before_lesson_attendance: AttendanceType | None = None
    """Attendance in the lesson right before the scheduled event."""

    after_lesson_attendance: AttendanceType | None = None
    """Attendance in the lesson right after the scheduled event."""


@dataclass(kw_only=True)
class TimetableGroupId(SkolaOnlineModel):
    """Group of a student."""

    group_id: str
    """ID of the group of the student."""


@dataclass(kw_only=True)
class TimetableLesson(SkolaOnlineModel):
    """Lesson of the school day."""

    id: str
    """ID of the lesson."""

    caption: str
    """Label of the lesson."""

    begin_time: datetime
    """Start time of the lesson."""

    end_time: datetime
    """End time of the lesson."""


@dataclass(kw_only=True)
class TimetableNumberOfHour(SkolaOnlineModel):
    """Lesson numbering for a class and period of the day."""

    lesson_id: str
    """ID of the lesson."""

    class_id: str
    """ID of the class."""

    group_ids: list[TimetableGroupId]
    """IDs of the groups."""

    number_of_hour: int
    """Lesson number."""


@dataclass(kw_only=True)
class TimetableResponse(SkolaOnlineModel):
    """Timetable for a date range."""

    days: list[Day]
    """Scheduled events on the individual days."""

    lessons: list[TimetableLesson]
    """All lessons of the school day defined by the organization."""


@dataclass(kw_only=True)
class TimetableSemester(SkolaOnlineModel):
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
class TimetableStudent(SkolaOnlineModel):
    """Student in the timetable detail."""

    id: str
    """ID of the student."""

    first_name: str | None = None
    """First name of the student."""

    lastname: str
    """Surname of the student."""

    display_name: str
    """Full name of the student for display."""

    cvtv: int | None = None
    """Number of the student in the class register."""

    class_id: str
    """ID of the class of the student."""

    groups: list[TimetableStudentGroup] | None = None
    """Groups of the student."""

    do_not_enter_attendance_in_subject: bool
    """Whether attendance is not recorded because the student is exempt from the
    subject or has it recognized."""

    is_studying_abroad: bool
    """Whether the student fulfills compulsory schooling abroad."""

    is_studying_at_home: bool
    """Whether the student fulfills compulsory schooling through home education."""

    is_participating_school_event: bool
    """Whether the student participates in a school event."""


@dataclass(kw_only=True)
class TimetableStudentGroup(SkolaOnlineModel):
    """Group of a student."""

    group_id: str
    """ID of the group of the student."""


@dataclass(kw_only=True)
class TimetableSubject(SkolaOnlineModel):
    """Subject of a scheduled event."""

    id: str
    """ID of the subject."""

    abbrev: str | None = None
    """Abbreviation of the subject."""

    name: str
    """Name of the subject."""

    kind: SubjectKind | None = None
    """Kind of subject."""


@dataclass(kw_only=True)
class TimetableTeacher(SkolaOnlineModel):
    """Teacher of a scheduled event."""

    id: str
    """ID of the teacher."""

    abbrev: str | None = None
    """Abbreviation of the teacher."""

    name: str | None = None
    """First name of the teacher."""

    surname: str
    """Surname of the teacher."""

    display_name: str
    """Full name for display."""


@dataclass(kw_only=True)
class TimetableTeachingInformation(SkolaOnlineModel):
    """Teaching information in the timetable."""

    teaching_information_id: str
    """ID of the teaching information."""

    lesson_id: str
    """ID of the lesson."""

    teacher_name: str | None = None
    """Name of the teacher."""

    information: str
    """Teaching information."""

    hour_type: HourType
    """Type of the event."""

    subject: TimetableSubject | None = None
    """Subject."""

    groups: list[Group] | None = None
    """Classes or groups the teaching information is meant for."""

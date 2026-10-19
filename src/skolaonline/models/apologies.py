from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from skolaonline.models._base import SkolaOnlineModel


class ApologyFilterState(StrEnum):
    """Filter of apologies by state."""

    ALL = "all"
    """All apologies."""

    UNPROCESSED = "unprocessed"
    """Unprocessed apologies."""

    REJECTED = "rejected"
    """Rejected apologies."""

    ACCEPTED = "accepted"
    """Accepted apologies."""


class ApologyState(StrEnum):
    """State of an apology."""

    UNPROCESSED = "unprocessed"
    """Unprocessed."""

    REJECTED = "rejected"
    """Rejected."""

    ACCEPTED = "accepted"
    """Accepted."""


@dataclass(kw_only=True)
class Apology(SkolaOnlineModel):
    """Apology for an absence."""

    apology_id: str
    """ID of the apology."""

    class_id: str
    """ID of the class the excused person belongs to in the current school year."""

    excused_person_id: str
    """ID of the excused person."""

    excused_person_name: str
    """Full name of the excused person, surname first."""

    excused_persons_initials: str
    """Initials of the excused person."""

    excused_is_preschooler: bool
    """Whether the excused person is a preschooler."""

    apologetic_person_id: str
    """ID of the person who submitted the apology."""

    apologetic_person_name: str
    """Full name of the person who submitted the apology, surname first."""

    apologetic_persons_initials: str
    """Initials of the person who submitted the apology."""

    reason_absence_id: str
    """ID of the reason for absence."""

    reason_absence_name: str
    """Name of the reason for absence."""

    specification: str | None = None
    """Other reason."""

    next_information: str | None = None
    """Details of the reason."""

    date_from: datetime
    """Start date."""

    date_to: datetime
    """End date."""

    time_from: str | None = None
    """Start time."""

    time_to: str | None = None
    """End time."""

    daily_block_from: str | None = None
    """Abbreviation of the first daily block."""

    daily_block_to: str | None = None
    """Abbreviation of the last daily block."""

    lesson_from: str | None = None
    """Display label of the first lesson."""

    lesson_to: str | None = None
    """Display label of the last lesson."""

    state_id: ApologyState
    """State of the apology."""

    sent: datetime
    """Date and time the apology was sent."""

    processing: datetime | None = None
    """Date and time the apology was processed by the teacher."""

    rejection_reason: str | None = None
    """Reason for rejection."""

    order: int
    """Order."""

    lesson_from_time_start: str | None = None
    """Start time of the first lesson."""

    lesson_from_time_end: str | None = None
    """End time of the first lesson."""

    lesson_to_time_start: str | None = None
    """Start time of the last lesson."""

    lesson_to_time_end: str | None = None
    """End time of the last lesson."""


@dataclass(kw_only=True)
class ApologyChild(SkolaOnlineModel):
    """Child of the signed-in parent."""

    id: str
    """ID of the child."""

    can_be_excused: bool
    """Whether the parent can excuse the child."""


@dataclass(kw_only=True)
class ApologyClass(SkolaOnlineModel):
    """Class for which absences can be excused."""

    class_id: str
    """ID of the class."""

    name: str
    """Name of the class."""

    class_teacher: bool
    """Whether the signed-in user is the class teacher of this class."""

    deputy_class_teacher: bool
    """Whether the signed-in user is the deputy class teacher of this class."""


@dataclass(kw_only=True)
class ApologyClassesResponse(SkolaOnlineModel):
    """Classes in which the user can process apologies."""

    message: str | None = None
    """Warning for the user when a non-essential part of the operation failed."""

    classes: list[ApologyClass]
    """Classes in which the user can process apologies."""


@dataclass(kw_only=True)
class ApologyCodeListClass(SkolaOnlineModel):
    """Class in which the signed-in teacher teaches."""

    id: str
    """ID of the class."""

    name: str
    """Name of the class."""

    class_teacher: bool
    """Whether the user is the class teacher."""

    deputy_class_teacher: bool
    """Whether the user is the deputy class teacher."""


@dataclass(kw_only=True)
class ApologyCodeListsResponse(SkolaOnlineModel):
    """Code lists used by the apologies module."""

    daily_blocks: list[DailyBlock]
    """Daily educational blocks used by kindergartens."""

    lessons: list[ApologyLesson]
    """Lessons of the school day."""

    classes: list[ApologyCodeListClass]
    """Classes in which the signed-in teacher teaches."""

    reasons_for_absence: list[CodelistReasonForAbsence]
    """Reasons for absence."""

    semester: list[ApologySemester]
    """Semesters of the school year."""

    children: list[ApologyChild]
    """Children of the signed-in parent."""

    reasons_for_absence_teacher: list[str]
    """Reasons for absence filled in by the teacher."""


@dataclass(kw_only=True)
class ApologyLesson(SkolaOnlineModel):
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
class ApologyPostData(SkolaOnlineModel):
    """Data of a new apology."""

    excused_person_id: str
    """ID of the excused person."""

    reason_absence_id: str
    """ID of the reason for absence."""

    specification: str | None = None
    """Other reason."""

    next_information: str | None = None
    """Details of the reason."""

    date_from: datetime
    """Start date."""

    date_to: datetime
    """End date."""

    time_from: str | None = None
    """Start time."""

    time_to: str | None = None
    """End time."""


@dataclass(kw_only=True)
class ApologyPutData(SkolaOnlineModel):
    """Updated data of an existing apology."""

    reason_absence_id: str
    """ID of the reason for absence."""

    specification: str | None = None
    """Other reason."""

    next_information: str | None = None
    """Details of the reason."""

    date_from: datetime
    """Start date."""

    date_to: datetime
    """End date."""

    time_from: str | None = None
    """Start time."""

    time_to: str | None = None
    """End time."""


@dataclass(kw_only=True)
class ApologySemester(SkolaOnlineModel):
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
class CodelistReasonForAbsence(SkolaOnlineModel):
    """Reason for absence."""

    reason_id: str
    """ID of the reason."""

    name: str
    """Name of the reason."""


@dataclass(kw_only=True)
class DailyBlock(SkolaOnlineModel):
    """Daily educational block used by kindergartens."""

    id: str
    """ID of the daily educational block."""

    order: int
    """Order of the daily educational block."""

    abbrev: str
    """Abbreviation of the daily educational block."""

    name: str
    """Name of the daily educational block."""

    time_from: str
    """Start time of the daily educational block."""

    time_to: str
    """End time of the daily educational block."""


@dataclass(kw_only=True)
class ParentApologiesResponse(SkolaOnlineModel):
    """Apologies of a child."""

    message: str | None = None
    """Warning for the user when a non-essential part of the operation failed."""

    apologies: list[Apology]
    """Apologies."""

    number_processed: int | None = None
    """Total number of apologies of the child in the current school year that match
    the state filter."""


@dataclass(kw_only=True)
class ParentApologyResponse(SkolaOnlineModel):
    """Single apology of a child."""

    apology: Apology | None = None
    """Apology."""


@dataclass(kw_only=True)
class ReasonForAbsence(SkolaOnlineModel):
    """Reason for absence."""

    reason_id: str
    """ID of the reason."""

    name: str
    """Name of the reason."""


@dataclass(kw_only=True)
class ReasonsForAbsenceResponse(SkolaOnlineModel):
    """Available reasons for absence."""

    reasons: list[ReasonForAbsence]
    """Reasons for absence."""


@dataclass(kw_only=True)
class TeacherApologiesResponse(SkolaOnlineModel):
    """Apologies in the classes of a class teacher."""

    message: str | None = None
    """Warning for the user when a non-essential part of the operation failed."""

    apologies: list[Apology]
    """Apologies."""

    number_processed: int | None = None
    """Total number of apologies in the current school year that match the class and
    state filters."""


@dataclass(kw_only=True)
class TeacherApologyResponse(SkolaOnlineModel):
    """Single apology as seen by a class teacher."""

    apology: Apology | None = None
    """Apology."""

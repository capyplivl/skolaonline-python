from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from skolaonline.models._base import SkolaOnlineModel


class ApologyFilterState(StrEnum):
    ALL = "all"
    UNPROCESSED = "unprocessed"
    REJECTED = "rejected"
    ACCEPTED = "accepted"


class ApologyState(StrEnum):
    UNPROCESSED = "unprocessed"
    REJECTED = "rejected"
    ACCEPTED = "accepted"


@dataclass(kw_only=True)
class Apology(SkolaOnlineModel):
    apology_id: str
    class_id: str
    excused_person_id: str
    excused_person_name: str
    excused_persons_initials: str
    excused_is_preschooler: bool
    apologetic_person_id: str
    apologetic_person_name: str
    apologetic_persons_initials: str
    reason_absence_id: str
    reason_absence_name: str
    specification: str | None = None
    next_information: str | None = None
    date_from: datetime
    date_to: datetime
    time_from: str | None = None
    time_to: str | None = None
    daily_block_from: str | None = None
    daily_block_to: str | None = None
    lesson_from: str | None = None
    lesson_to: str | None = None
    state_id: ApologyState
    sent: datetime
    processing: datetime | None = None
    rejection_reason: str | None = None
    order: int
    lesson_from_time_start: str | None = None
    lesson_from_time_end: str | None = None
    lesson_to_time_start: str | None = None
    lesson_to_time_end: str | None = None


@dataclass(kw_only=True)
class ApologyChild(SkolaOnlineModel):
    id: str
    can_be_excused: bool


@dataclass(kw_only=True)
class ApologyClass(SkolaOnlineModel):
    class_id: str
    name: str
    class_teacher: bool
    deputy_class_teacher: bool


@dataclass(kw_only=True)
class ApologyClassesResponse(SkolaOnlineModel):
    message: str | None = None
    classes: list[ApologyClass]


@dataclass(kw_only=True)
class ApologyCodeListClass(SkolaOnlineModel):
    id: str
    name: str
    class_teacher: bool
    deputy_class_teacher: bool


@dataclass(kw_only=True)
class ApologyCodeListsResponse(SkolaOnlineModel):
    daily_blocks: list[DailyBlock]
    lessons: list[ApologyLesson]
    classes: list[ApologyCodeListClass]
    reasons_for_absence: list[CodelistReasonForAbsence]
    semester: list[ApologySemester]
    children: list[ApologyChild]
    reasons_for_absence_teacher: list[str]


@dataclass(kw_only=True)
class ApologyLesson(SkolaOnlineModel):
    id: str
    order: int
    name: str
    time_from: str
    time_to: str


@dataclass(kw_only=True)
class ApologyPostData(SkolaOnlineModel):
    excused_person_id: str
    reason_absence_id: str
    specification: str | None = None
    next_information: str | None = None
    date_from: datetime
    date_to: datetime
    time_from: str | None = None
    time_to: str | None = None


@dataclass(kw_only=True)
class ApologyPutData(SkolaOnlineModel):
    reason_absence_id: str
    specification: str | None = None
    next_information: str | None = None
    date_from: datetime
    date_to: datetime
    time_from: str | None = None
    time_to: str | None = None


@dataclass(kw_only=True)
class ApologySemester(SkolaOnlineModel):
    id: str
    parent_id: str
    name: str
    date_from: datetime
    date_to: datetime
    order: int


@dataclass(kw_only=True)
class CodelistReasonForAbsence(SkolaOnlineModel):
    reason_id: str
    name: str


@dataclass(kw_only=True)
class DailyBlock(SkolaOnlineModel):
    id: str
    order: int
    abbrev: str
    name: str
    time_from: str
    time_to: str


@dataclass(kw_only=True)
class ParentApologiesResponse(SkolaOnlineModel):
    message: str | None = None
    apologies: list[Apology]
    number_processed: int | None = None


@dataclass(kw_only=True)
class ParentApologyResponse(SkolaOnlineModel):
    apology: Apology | None = None


@dataclass(kw_only=True)
class ReasonForAbsence(SkolaOnlineModel):
    reason_id: str
    name: str


@dataclass(kw_only=True)
class ReasonsForAbsenceResponse(SkolaOnlineModel):
    reasons: list[ReasonForAbsence]


@dataclass(kw_only=True)
class TeacherApologiesResponse(SkolaOnlineModel):
    message: str | None = None
    apologies: list[Apology]
    number_processed: int | None = None


@dataclass(kw_only=True)
class TeacherApologyResponse(SkolaOnlineModel):
    apology: Apology | None = None

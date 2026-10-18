from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from skolaonline.models._base import SkolaOnlineModel
from skolaonline.models.common import SubjectKind


class EvaluationType(StrEnum):
    NONEVALUATION = "nonevaluation"
    DONE = "done"
    MARKS = "marks"
    PERCENT = "percent"
    POINTS = "points"


class HomeworkProcessingStatus(StrEnum):
    AWAITING_ELABORATION = "awaitingElaboration"
    WAITING_FOR_EVALUATION = "waitingForEvaluation"
    FULFILLED = "fulfilled"
    NOT_FULFILLED = "notFulfilled"
    EVALUATED = "evaluated"
    AFTER_THE_DEADLINE = "afterTheDeadline"
    CANCELED = "canceled"
    RETURNED = "returned"
    DONE = "done"


class HomeworkState(StrEnum):
    ALL = "all"
    ENTRED_TODAY = "entredToday"
    SUBMITED_TODAY = "submitedToday"
    SUBMITED_TOMORROW = "submitedTomorrow"
    ENTRED_THIS_WEEK = "entredThisWeek"
    SUBMITED_THIS_WEEK = "submitedThisWeek"


class HomeworkTeacherState(StrEnum):
    ALL = "all"
    ASSIGNED = "assigned"
    AFTER_DEADLINE = "afterDeadline"
    UNASSIGNED = "unassigned"


class HomeworksFilterState(StrEnum):
    ALL = "all"
    ACTIVE = "active"
    SUBMITTED = "submitted"
    AFTER_DEADLINE = "afterDeadline"
    CANCELED = "canceled"


class SubmissionType(StrEnum):
    NONSUBMISSION = "nonsubmission"
    TEXT = "text"
    TEXT_ATTACHMENT = "textAttachment"


@dataclass(kw_only=True)
class Homework(SkolaOnlineModel):
    id: str
    date_start: datetime
    date_end: datetime
    name: str
    content: str | None = None
    submission: SubmissionType
    method_evaluation: EvaluationType
    max_points: int | None = None
    done: bool
    done_teacher: bool
    closed: bool
    closed_date: datetime | None = None
    subject: HomeworkSubject | None = None
    teacher: HomeworkTeacher
    attachments: list[HomeworkAttachment]
    elaboration: str | None = None
    date_submitted: datetime | None = None
    attachments_elaboration: list[HomeworkAttachment]
    evaluation: str | None = None
    comment: str | None = None
    evaluation_teacher: HomeworkTeacher | None = None
    evaluation_date: datetime | None = None
    date_return: datetime | None = None
    reason_return: str | None = None
    date_end_student: datetime | None = None
    state_home_work: HomeworkProcessingStatus


@dataclass(kw_only=True)
class HomeworkAttachment(SkolaOnlineModel):
    id: str
    name: str
    name_user: str
    type: str | None = None
    size: int


@dataclass(kw_only=True)
class HomeworkClass(SkolaOnlineModel):
    id: str
    name: str


@dataclass(kw_only=True)
class HomeworkCodeListSubject(SkolaOnlineModel):
    id: str
    abbrev: str | None = None
    name: str
    kind: SubjectKind | None = None


@dataclass(kw_only=True)
class HomeworkCodeListsResponse(SkolaOnlineModel):
    subjects: list[HomeworkCodeListSubject]


@dataclass(kw_only=True)
class HomeworkResponse(SkolaOnlineModel):
    homework: Homework | None = None


@dataclass(kw_only=True)
class HomeworkStudent(SkolaOnlineModel):
    id: str
    first_name: str | None = None
    last_name: str
    elaboration: str | None = None
    done: bool
    done_teacher: bool
    date_submitted: datetime | None = None
    attachments_elaboration: list[HomeworkAttachment]
    evaluation: str | None = None
    comment: str | None = None
    evaluation_teacher: HomeworkTeacher | None = None
    evaluation_date: datetime | None = None
    date_return: datetime | None = None
    reason_return: str | None = None
    date_end_student: datetime | None = None


@dataclass(kw_only=True)
class HomeworkSubject(SkolaOnlineModel):
    id: str
    abbrev: str
    name: str
    kind: SubjectKind | None = None


@dataclass(kw_only=True)
class HomeworkTeacher(SkolaOnlineModel):
    id: str
    abbrev: str | None = None
    first_name: str | None = None
    last_name: str
    title_before: str | None = None
    title_after: str | None = None
    display_name: str


@dataclass(kw_only=True)
class HomeworksResponse(SkolaOnlineModel):
    homeworks: list[Homework]


@dataclass(kw_only=True)
class HomeworksTeacherResponse(SkolaOnlineModel):
    homeworks: list[TeacherHomework]


@dataclass(kw_only=True)
class PutElaborationRequest(SkolaOnlineModel):
    school_year_id: str | None = None
    submit: bool
    elaboration: str


@dataclass(kw_only=True)
class TeacherHomework(SkolaOnlineModel):
    id: str
    date_start: datetime
    date_end: datetime
    name: str
    content: str | None = None
    submission: SubmissionType | None = None
    method_evaluation: EvaluationType | None = None
    max_points: int | None = None
    closed: bool
    classes: list[HomeworkClass]
    students: list[HomeworkStudent]
    subject: HomeworkSubject | None = None
    attachments: list[HomeworkAttachment]

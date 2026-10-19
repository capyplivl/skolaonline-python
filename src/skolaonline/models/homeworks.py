from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from skolaonline.models._base import SkolaOnlineModel
from skolaonline.models.common import SubjectKind


class EvaluationType(StrEnum):
    """How a homework is evaluated."""

    NONEVALUATION = "nonevaluation"
    """Evaluation is not recorded."""

    DONE = "done"
    """Only done or not done is recorded."""

    MARKS = "marks"
    """Evaluated with marks."""

    PERCENT = "percent"
    """Evaluated with a percentage."""

    POINTS = "points"
    """Evaluated with points."""


class HomeworkProcessingStatus(StrEnum):
    """Processing status of a homework."""

    AWAITING_ELABORATION = "awaitingElaboration"
    """Assigned and not elaborated yet."""

    WAITING_FOR_EVALUATION = "waitingForEvaluation"
    """Submitted by the student and waiting for evaluation by the teacher."""

    FULFILLED = "fulfilled"
    """Submitted and evaluated by the teacher as fulfilled."""

    NOT_FULFILLED = "notFulfilled"
    """Submitted and evaluated by the teacher as not fulfilled."""

    EVALUATED = "evaluated"
    """Evaluated."""

    AFTER_THE_DEADLINE = "afterTheDeadline"
    """Past the due date."""

    CANCELED = "canceled"
    """Canceled by the teacher."""

    RETURNED = "returned"
    """Returned by the teacher and not elaborated again yet."""

    DONE = "done"
    """Homework without submission that the student marked as done or whose due date
    passed."""


class HomeworkState(StrEnum):
    """Homework filter by assignment and due dates."""

    ALL = "all"
    """All homeworks."""

    ENTRED_TODAY = "entredToday"
    """Homeworks assigned today."""

    SUBMITED_TODAY = "submitedToday"
    """Homeworks due today."""

    SUBMITED_TOMORROW = "submitedTomorrow"
    """Homeworks due tomorrow."""

    ENTRED_THIS_WEEK = "entredThisWeek"
    """Homeworks assigned this week."""

    SUBMITED_THIS_WEEK = "submitedThisWeek"
    """Homeworks due this week."""


class HomeworkTeacherState(StrEnum):
    """Filter of homeworks assigned by a teacher."""

    ALL = "all"
    """All homeworks."""

    ASSIGNED = "assigned"
    """Homeworks assigned to students."""

    AFTER_DEADLINE = "afterDeadline"
    """Homeworks past the due date."""

    UNASSIGNED = "unassigned"
    """Homeworks not assigned to any student."""


class HomeworksFilterState(StrEnum):
    """Filter of homeworks of a student."""

    ALL = "all"
    """All homeworks."""

    ACTIVE = "active"
    """Active homeworks."""

    SUBMITTED = "submitted"
    """Homeworks submitted by the student."""

    AFTER_DEADLINE = "afterDeadline"
    """Homeworks past the due date and not submitted."""

    CANCELED = "canceled"
    """Homeworks closed by the teacher."""


class SubmissionType(StrEnum):
    """How a homework is submitted."""

    NONSUBMISSION = "nonsubmission"
    """Submission is not recorded."""

    TEXT = "text"
    """The student writes the elaboration as text."""

    TEXT_ATTACHMENT = "textAttachment"
    """The student writes the elaboration as text and can attach files."""


@dataclass(kw_only=True)
class Homework(SkolaOnlineModel):
    """Homework of a student."""

    id: str
    """ID of the homework."""

    date_start: datetime
    """Date and time the homework was assigned."""

    date_end: datetime
    """Date and time the homework is due."""

    name: str
    """Name of the homework."""

    content: str | None = None
    """Assignment text."""

    submission: SubmissionType
    """How the homework is submitted."""

    method_evaluation: EvaluationType
    """How the homework is evaluated."""

    max_points: int | None = None
    """Maximum number of points for point evaluation."""

    done: bool
    """Whether the student marked the homework as done. Used when evaluation is not
    recorded."""

    done_teacher: bool
    """Whether the teacher marked the homework as done. Used when only done or not
    done is recorded."""

    closed: bool
    """Whether the homework is closed."""

    closed_date: datetime | None = None
    """Date the teacher closed the homework."""

    subject: HomeworkSubject | None = None
    """Subject of the homework."""

    teacher: HomeworkTeacher
    """Teacher who assigned the homework."""

    attachments: list[HomeworkAttachment]
    """Attachments of the assignment."""

    elaboration: str | None = None
    """Elaboration text written by the student."""

    date_submitted: datetime | None = None
    """Date the homework was submitted."""

    attachments_elaboration: list[HomeworkAttachment]
    """Attachments of the elaboration."""

    evaluation: str | None = None
    """Evaluation by the teacher."""

    comment: str | None = None
    """Verbal evaluation of the homework."""

    evaluation_teacher: HomeworkTeacher | None = None
    """Teacher who evaluated the homework."""

    evaluation_date: datetime | None = None
    """Date the teacher evaluated the homework."""

    date_return: datetime | None = None
    """Date the teacher returned the homework."""

    reason_return: str | None = None
    """Reason the teacher returned the homework."""

    date_end_student: datetime | None = None
    """New due date for the student."""

    state_home_work: HomeworkProcessingStatus
    """Processing status of the homework."""


@dataclass(kw_only=True)
class HomeworkAttachment(SkolaOnlineModel):
    """Attachment of a homework."""

    id: str
    """ID used to download the file."""

    name: str
    """Physical file name."""

    name_user: str
    """File name shown to users."""

    type: str | None = None
    """File type."""

    size: int
    """File size in bytes."""


@dataclass(kw_only=True)
class HomeworkClass(SkolaOnlineModel):
    """Class a homework is assigned to."""

    id: str
    """ID of the class."""

    name: str
    """Name of the class."""


@dataclass(kw_only=True)
class HomeworkCodeListSubject(SkolaOnlineModel):
    """Subject listed in the homeworks code lists."""

    id: str
    """ID of the subject."""

    abbrev: str | None = None
    """Abbreviation of the subject."""

    name: str
    """Name of the subject."""

    kind: SubjectKind | None = None
    """Kind of subject."""


@dataclass(kw_only=True)
class HomeworkCodeListsResponse(SkolaOnlineModel):
    """Code lists used by the homeworks module."""

    subjects: list[HomeworkCodeListSubject]
    """Subjects."""


@dataclass(kw_only=True)
class HomeworkResponse(SkolaOnlineModel):
    """Single homework of a student."""

    homework: Homework | None = None
    """Homework."""


@dataclass(kw_only=True)
class HomeworkStudent(SkolaOnlineModel):
    """Student a homework is assigned to."""

    id: str
    """ID of the student."""

    first_name: str | None = None
    """First name of the student."""

    last_name: str
    """Surname of the student."""

    elaboration: str | None = None
    """Elaboration text written by the student."""

    done: bool
    """Whether the student marked the homework as done. Used when evaluation is not
    recorded."""

    done_teacher: bool
    """Whether the teacher marked the homework as done. Used when only done or not
    done is recorded."""

    date_submitted: datetime | None = None
    """Date the student submitted the homework."""

    attachments_elaboration: list[HomeworkAttachment]
    """Attachments of the elaboration."""

    evaluation: str | None = None
    """Evaluation by the teacher."""

    comment: str | None = None
    """Verbal evaluation of the homework."""

    evaluation_teacher: HomeworkTeacher | None = None
    """Teacher who evaluated the homework."""

    evaluation_date: datetime | None = None
    """Date the teacher evaluated the homework."""

    date_return: datetime | None = None
    """Date the teacher returned the homework."""

    reason_return: str | None = None
    """Reason the teacher returned the homework."""

    date_end_student: datetime | None = None
    """New due date for the student."""


@dataclass(kw_only=True)
class HomeworkSubject(SkolaOnlineModel):
    """Subject of a homework."""

    id: str
    """ID of the subject."""

    abbrev: str
    """Abbreviation of the subject."""

    name: str
    """Name of the subject."""

    kind: SubjectKind | None = None
    """Kind of subject."""


@dataclass(kw_only=True)
class HomeworkTeacher(SkolaOnlineModel):
    """Teacher of a homework."""

    id: str
    """ID of the teacher."""

    abbrev: str | None = None
    """Abbreviation of the teacher."""

    first_name: str | None = None
    """First name of the teacher."""

    last_name: str
    """Surname of the teacher."""

    title_before: str | None = None
    """Title before the name."""

    title_after: str | None = None
    """Title after the name."""

    display_name: str
    """Full name for display."""


@dataclass(kw_only=True)
class HomeworksResponse(SkolaOnlineModel):
    """Homeworks of a student."""

    homeworks: list[Homework]
    """Homeworks of the student matching the filter."""


@dataclass(kw_only=True)
class HomeworksTeacherResponse(SkolaOnlineModel):
    """Homeworks assigned by a teacher."""

    homeworks: list[TeacherHomework]
    """Homeworks assigned by the teacher."""


@dataclass(kw_only=True)
class PutElaborationRequest(SkolaOnlineModel):
    """Elaboration of a homework."""

    school_year_id: str | None = None
    """ID of the requested school year."""

    submit: bool
    """Whether the homework is submitted. False saves it as a work in progress."""

    elaboration: str
    """Elaboration text of the homework."""


@dataclass(kw_only=True)
class TeacherHomework(SkolaOnlineModel):
    """Homework assigned by a teacher."""

    id: str
    """ID of the homework."""

    date_start: datetime
    """Date and time the homework was assigned."""

    date_end: datetime
    """Date and time the homework is due."""

    name: str
    """Name of the homework."""

    content: str | None = None
    """Assignment text."""

    submission: SubmissionType | None = None
    """How the homework is submitted."""

    method_evaluation: EvaluationType | None = None
    """How the homework is evaluated."""

    max_points: int | None = None
    """Maximum number of points for point evaluation."""

    closed: bool
    """Whether the homework is closed."""

    classes: list[HomeworkClass]
    """Classes of the students the homework is assigned to."""

    students: list[HomeworkStudent]
    """Students the homework is assigned to."""

    subject: HomeworkSubject | None = None
    """Subject of the homework."""

    attachments: list[HomeworkAttachment]
    """Attachments of the assignment."""

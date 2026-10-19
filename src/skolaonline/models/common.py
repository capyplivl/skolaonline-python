from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from skolaonline.models._base import SkolaOnlineModel


class GroupKind(StrEnum):
    """Kind of group."""

    CLASS = "c"
    """Class."""

    GROUP = "g"
    """Group."""

    SEMINAR = "s"
    """Seminar."""


class SubjectKind(StrEnum):
    """Kind of subject."""

    COMPULSORY = "p"
    """Compulsory."""

    ELECTIVE = "v"
    """Compulsory elective."""

    OPTIONAL = "n"
    """Optional."""


class UserType(StrEnum):
    """Type of user."""

    STUDENT = "student"
    """Student."""

    PARENT = "parent"
    """Parent."""

    EMPLOYEE = "employee"
    """Employee."""

    SYSTEM = "system"
    """System account."""


@dataclass(kw_only=True)
class ErrorResponse(SkolaOnlineModel):
    """Error returned by the API."""

    message: str | None = None
    """Internal message describing the error."""

    user_message: str | None = None
    """Message that can be shown to the user."""

    error_code: str | None = None
    """Error code for programmatic handling."""


@dataclass(kw_only=True)
class IdName(SkolaOnlineModel):
    """Identifier with a name."""

    id: str
    """Identifier."""

    name: str
    """Name."""


@dataclass(kw_only=True)
class IdNameDesc(SkolaOnlineModel):
    """Identifier with a name and a description."""

    id: str
    """Identifier."""

    name: str
    """Name."""

    description: str
    """Description."""


@dataclass(kw_only=True)
class ObjectInfo(SkolaOnlineModel):
    """Basic information about an entity."""

    id: str
    """Identifier."""

    abbrev: str | None = None
    """Abbreviation for display."""

    name: str
    """Name for display."""


@dataclass(kw_only=True)
class OkWarningResponse(SkolaOnlineModel):
    """Successful result that may contain a warning for the user."""

    message: str | None = None
    """Warning for the user when a non-essential part of the operation failed."""


@dataclass(kw_only=True)
class ProblemDetails(SkolaOnlineModel):
    """RFC 7807 problem details returned for failed requests."""

    type: str | None = None
    """URI reference identifying the problem type."""

    title: str | None = None
    """Short summary of the problem type."""

    status: int | None = None
    """HTTP status code."""

    detail: str | None = None
    """Explanation specific to this occurrence of the problem."""

    instance: str | None = None
    """URI reference identifying this occurrence of the problem."""

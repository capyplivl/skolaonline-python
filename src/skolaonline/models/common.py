from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from skolaonline.models._base import SkolaOnlineModel


class GroupKind(StrEnum):
    CLASS = "c"
    GROUP = "g"
    SEMINAR = "s"


class SubjectKind(StrEnum):
    COMPULSORY = "p"
    ELECTIVE = "v"
    OPTIONAL = "n"


class UserType(StrEnum):
    STUDENT = "student"
    PARENT = "parent"
    EMPLOYEE = "employee"
    SYSTEM = "system"


@dataclass(kw_only=True)
class ErrorResponse(SkolaOnlineModel):
    message: str | None = None
    user_message: str | None = None
    error_code: str | None = None


@dataclass(kw_only=True)
class IdName(SkolaOnlineModel):
    id: str
    name: str


@dataclass(kw_only=True)
class IdNameDesc(SkolaOnlineModel):
    id: str
    name: str
    description: str


@dataclass(kw_only=True)
class ObjectInfo(SkolaOnlineModel):
    id: str
    abbrev: str | None = None
    name: str


@dataclass(kw_only=True)
class OkWarningResponse(SkolaOnlineModel):
    message: str | None = None


@dataclass(kw_only=True)
class ProblemDetails(SkolaOnlineModel):
    type: str | None = None
    title: str | None = None
    status: int | None = None
    detail: str | None = None
    instance: str | None = None

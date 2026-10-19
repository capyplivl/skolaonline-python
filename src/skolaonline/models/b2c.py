from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from skolaonline.models._base import SkolaOnlineModel


class B2CUserType(StrEnum):
    """Type of user returned by the B2C endpoints."""

    STUDENT = "student"
    """Student."""

    PARENT = "parent"
    """Parent."""

    TEACHER = "teacher"
    """Teacher."""


@dataclass(kw_only=True)
class Login(SkolaOnlineModel):
    """Credentials of a user."""

    username: str
    """Username."""

    password: str
    """Password."""


@dataclass(kw_only=True)
class UserBulkRefresh(SkolaOnlineModel):
    """Study information of the requested users."""

    user_studies: list[UserStudy] | None = None
    """Study information of the users that were found."""

    missing_user_ids: list[str] | None = None
    """IDs of the users that were not found."""


@dataclass(kw_only=True)
class UserDetail(SkolaOnlineModel):
    """Detailed information about a user."""

    id: str
    """Unique identifier of the user."""

    first_name: str | None = None
    """First name."""

    last_name: str
    """Surname."""

    birthday: str | None = None
    """Date of birth."""

    type: B2CUserType | None = None
    """Type of user."""

    photo: str | None = None
    """Photo encoded in base64."""

    study_year: str | None = None
    """Current grade."""

    school_year: str
    """Current school year."""

    school_name: str | None = None
    """Name of the school."""

    school_address: str | None = None
    """Address of the school."""

    active: bool | None = None
    """Whether the user is actively studying."""


@dataclass(kw_only=True)
class UserStudy(SkolaOnlineModel):
    """Study information of a user."""

    id: str
    """Unique identifier of the user."""

    study_year: str | None = None
    """Current grade."""

    school_year: str
    """Current school year."""

    school_name: str | None = None
    """Name of the school."""

    school_address: str | None = None
    """Address of the school."""

    active: bool | None = None
    """Whether the user is actively studying."""

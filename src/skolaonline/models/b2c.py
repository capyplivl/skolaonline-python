from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from skolaonline.models._base import SkolaOnlineModel


class B2CUserType(StrEnum):
    STUDENT = "student"
    PARENT = "parent"
    TEACHER = "teacher"


@dataclass(kw_only=True)
class Login(SkolaOnlineModel):
    username: str
    password: str


@dataclass(kw_only=True)
class UserBulkRefresh(SkolaOnlineModel):
    user_studies: list[UserStudy] | None = None
    missing_user_ids: list[str] | None = None


@dataclass(kw_only=True)
class UserDetail(SkolaOnlineModel):
    id: str
    first_name: str | None = None
    last_name: str
    birthday: str | None = None
    type: B2CUserType | None = None
    photo: str | None = None
    study_year: str | None = None
    school_year: str
    school_name: str | None = None
    school_address: str | None = None
    active: bool | None = None


@dataclass(kw_only=True)
class UserStudy(SkolaOnlineModel):
    id: str
    study_year: str | None = None
    school_year: str
    school_name: str | None = None
    school_address: str | None = None
    active: bool | None = None

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any, ClassVar

from skolaonline.models._base import SkolaOnlineModel
from skolaonline.models.common import ObjectInfo, UserType


class ApiModule(StrEnum):
    API_DOCHAZKA_ZAK = "api_dochazka_zak"
    API_DOM_UKOLY_ZAK = "api_dom_ukoly_zak"
    API_DOM_UKOLY_ZAM = "api_dom_ukoly_zam"
    API_HODN_PREDMET_ZAK = "api_hodn_predmet_zak"
    API_HODNOCENI_ZAK = "api_hodnoceni_zak"
    API_HODNOCENI_ZAM = "api_hodnoceni_zam"
    API_CHOVANI_ZAK = "api_chovani_zak"
    API_CHOVANI_ZAM = "api_chovani_zam"
    API_OMLUVENKY_ZAK = "api_omluvenky_zak"
    API_OMLUVENKY_ZAM = "api_omluvenky_zam"
    API_PLATBY_ZAK = "api_platby_zak"
    API_ROZVRH_ZAK = "api_rozvrh_zak"
    API_ROZVRH_ZAM = "api_rozvrh_zam"
    API_VYSVEDCENI_ZAK = "api_vysvedceni_zak"
    API_ZPRAVY_ZAK = "api_zpravy_zak"
    API_ZPRAVY_ZAM = "api_zpravy_zam"
    MESSAGES = "messages"
    APOLOGIES = "apologies"
    API_EMERGENCY = "api_emergency"


class InstallType(StrEnum):
    NOT_SUPPORTED = "notSupported"
    SOL = "sol"
    DIGISKOLKA = "digiskolka"
    DM = "dm"
    MEGAPRUT = "megaprut"
    SPPK = "sppk"
    ZAPISY = "zapisy"


class LanguageCode(StrEnum):
    CS = "cs"
    EN = "en"
    DE = "de"


class SchoolType(StrEnum):
    KON = "kon"
    MS = "ms"
    PS = "ps"
    SS = "ss"
    SD = "sd"
    SK = "sk"
    VS = "vs"
    VOS = "vos"
    VZD = "vzd"
    ZS = "zs"
    ZR = "zr"


@dataclass(kw_only=True)
class ChangePasswordRequest(SkolaOnlineModel):
    current_password: str | None = None
    new_password: str
    confirm_password: str


@dataclass(kw_only=True)
class Module(SkolaOnlineModel):
    module_id: ApiModule
    module_name: str


@dataclass(kw_only=True)
class ModuleNotificationCount(SkolaOnlineModel):
    module_id: ApiModule
    count: int


@dataclass(kw_only=True)
class ModuleRights(SkolaOnlineModel):
    module: Module | None = None
    rights: list[str]
    module_settings: Any = None


@dataclass(kw_only=True)
class NotificationOffRequest(SkolaOnlineModel):
    fcm_token: str
    organization_id: str
    person_id: str


@dataclass(kw_only=True)
class NotificationsResponse(SkolaOnlineModel):
    notifications: list[ModuleNotificationCount]


@dataclass(kw_only=True)
class PasswordRequirementsResponse(SkolaOnlineModel):
    min_numeric_characters: int
    min_non_numeric_characters: int


@dataclass(kw_only=True)
class PostFeedbackRequest(SkolaOnlineModel):
    sender_email: str | None = None
    text: str
    attachments: list[str] | None = None


@dataclass(kw_only=True)
class UserChild(SkolaOnlineModel):
    id: str
    display_name: str
    first_name: str | None = None
    last_name: str
    persons_initials: str
    class_id: str | None = None
    class_name: str | None = None


@dataclass(kw_only=True)
class UserInfoChild(SkolaOnlineModel):
    id: str
    display_name: str
    first_name: str | None = None
    last_name: str
    persons_initials: str
    class_id: str | None = None
    class_name: str | None = None
    enabled_modules: list[ModuleRights] | None = None


@dataclass(kw_only=True)
class UserInfoResponse(SkolaOnlineModel):
    _field_aliases: ClassVar[dict[str, str]] = {
        "user_uid": "userUID",
        "organization_id": "organizationID",
        "person_id": "personID",
    }

    user_uid: str
    organization_id: str
    person_id: str
    campaign_category_code: str | None = None
    class_: ObjectInfo | None = None
    full_name: str
    first_name: str | None = None
    last_name: str | None = None
    detail_name: str
    persons_initials: str
    school_organization_name: str
    school_type: SchoolType | None = None
    user_type: UserType
    user_type_text: str
    study_year: int | None = None
    children: list[UserInfoChild]
    class_teacher_classes: list[str]
    deputy_class_teacher_classes: list[str]
    install_type: InstallType
    language: LanguageCode
    school_year_id: str | None = None
    enabled_modules: list[ModuleRights] | None = None

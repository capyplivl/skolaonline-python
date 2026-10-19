from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any, ClassVar

from skolaonline.models._base import SkolaOnlineModel
from skolaonline.models.common import ObjectInfo, UserType


class ApiModule(StrEnum):
    """Module of the API."""

    API_DOCHAZKA_ZAK = "api_dochazka_zak"
    """Attendance of a student."""

    API_DOM_UKOLY_ZAK = "api_dom_ukoly_zak"
    """Homeworks of a student."""

    API_DOM_UKOLY_ZAM = "api_dom_ukoly_zam"
    """Homeworks of an employee."""

    API_HODN_PREDMET_ZAK = "api_hodn_predmet_zak"
    """Marks of a student by subject."""

    API_HODNOCENI_ZAK = "api_hodnoceni_zak"
    """Marks of a student."""

    API_HODNOCENI_ZAM = "api_hodnoceni_zam"
    """Marks entered by an employee."""

    API_CHOVANI_ZAK = "api_chovani_zak"
    """Behavior of a student."""

    API_CHOVANI_ZAM = "api_chovani_zam"
    """Behavior records entered by an employee."""

    API_OMLUVENKY_ZAK = "api_omluvenky_zak"
    """Apologies of a student."""

    API_OMLUVENKY_ZAM = "api_omluvenky_zam"
    """Apologies processed by an employee."""

    API_PLATBY_ZAK = "api_platby_zak"
    """Payments of a student."""

    API_ROZVRH_ZAK = "api_rozvrh_zak"
    """Timetable of a student."""

    API_ROZVRH_ZAM = "api_rozvrh_zam"
    """Timetable of an employee."""

    API_VYSVEDCENI_ZAK = "api_vysvedceni_zak"
    """Report cards of a student."""

    API_ZPRAVY_ZAK = "api_zpravy_zak"
    """Messages of a student."""

    API_ZPRAVY_ZAM = "api_zpravy_zam"
    """Messages of an employee."""

    MESSAGES = "messages"
    """Messages."""

    APOLOGIES = "apologies"
    """Apologies."""

    API_EMERGENCY = "api_emergency"
    """Emergencies."""


class InstallType(StrEnum):
    """Installation type of the application."""

    NOT_SUPPORTED = "notSupported"
    """Not supported."""

    SOL = "sol"
    """Škola OnLine."""

    DIGISKOLKA = "digiskolka"
    """DigiŠkolka."""

    DM = "dm"
    """Installation type DM."""

    MEGAPRUT = "megaprut"
    """Installation type MEGAPRUT."""

    SPPK = "sppk"
    """Installation type SPPK."""

    ZAPISY = "zapisy"
    """Enrollment application."""


class LanguageCode(StrEnum):
    """Language code."""

    CS = "cs"
    """Czech."""

    EN = "en"
    """English."""

    DE = "de"
    """German."""


class SchoolType(StrEnum):
    """Type of school."""

    KON = "kon"
    """Conservatory."""

    MS = "ms"
    """Kindergarten."""

    PS = "ps"
    """School type code PS."""

    SS = "ss"
    """Secondary school."""

    SD = "sd"
    """School type code SD."""

    SK = "sk"
    """School type code SK."""

    VS = "vs"
    """University."""

    VOS = "vos"
    """Higher vocational school."""

    VZD = "vzd"
    """School type code VZD."""

    ZS = "zs"
    """Elementary school."""

    ZR = "zr"
    """School type code ZR."""


@dataclass(kw_only=True)
class ChangePasswordRequest(SkolaOnlineModel):
    """Password change of the signed-in user."""

    current_password: str | None = None
    """Current password. Not required when changing a one-time password."""

    new_password: str
    """New password."""

    confirm_password: str
    """Confirmation of the new password."""


@dataclass(kw_only=True)
class Module(SkolaOnlineModel):
    """Application module."""

    module_id: ApiModule
    """Identifier of the module."""

    module_name: str
    """Name of the module."""


@dataclass(kw_only=True)
class ModuleNotificationCount(SkolaOnlineModel):
    """Number of unprocessed records in a module."""

    module_id: ApiModule
    """Identifier of the module."""

    count: int
    """Number of unprocessed records."""


@dataclass(kw_only=True)
class ModuleRights(SkolaOnlineModel):
    """Rights of the user in a module."""

    module: Module | None = None
    """Module."""

    rights: list[str]
    """Rights of the user. Only rights needed by client applications are included;
    the back end enforces security."""

    module_settings: Any = None
    """Module specific settings. The structure differs per module."""


@dataclass(kw_only=True)
class NotificationOffRequest(SkolaOnlineModel):
    """Request to disable notifications for a device."""

    fcm_token: str
    """Firebase token."""

    organization_id: str
    """ID of the organization."""

    person_id: str
    """ID of the person."""


@dataclass(kw_only=True)
class NotificationsResponse(SkolaOnlineModel):
    """Modules with notifications."""

    notifications: list[ModuleNotificationCount]
    """Notification counts per module."""


@dataclass(kw_only=True)
class PasswordRequirementsResponse(SkolaOnlineModel):
    """Password complexity requirements for the signed-in user."""

    min_numeric_characters: int
    """Minimum number of digits in the password."""

    min_non_numeric_characters: int
    """Minimum number of non-digit characters in the password."""


@dataclass(kw_only=True)
class PostFeedbackRequest(SkolaOnlineModel):
    """Feedback about the application."""

    sender_email: str | None = None
    """Email address of the sender."""

    text: str
    """Feedback text."""

    attachments: list[str] | None = None
    """IDs of attached files."""


@dataclass(kw_only=True)
class UserChild(SkolaOnlineModel):
    """Child of the signed-in parent."""

    id: str
    """ID of the child."""

    display_name: str
    """Display name of the child."""

    first_name: str | None = None
    """First name of the child."""

    last_name: str
    """Surname of the child."""

    persons_initials: str
    """Initials of the child."""

    class_id: str | None = None
    """ID of the class of the child."""

    class_name: str | None = None
    """Name of the class of the child."""


@dataclass(kw_only=True)
class UserInfoChild(SkolaOnlineModel):
    """Child of the signed-in parent with access to modules."""

    id: str
    """ID of the child."""

    display_name: str
    """Display name of the child."""

    first_name: str | None = None
    """First name of the child."""

    last_name: str
    """Surname of the child."""

    persons_initials: str
    """Initials of the child."""

    class_id: str | None = None
    """ID of the class of the child."""

    class_name: str | None = None
    """Name of the class of the child."""

    enabled_modules: list[ModuleRights] | None = None
    """Rights of the child in the enabled modules."""


@dataclass(kw_only=True)
class UserInfoResponse(SkolaOnlineModel):
    """Information about the signed-in user."""

    _field_aliases: ClassVar[dict[str, str]] = {
        "user_uid": "userUID",
        "organization_id": "organizationID",
        "person_id": "personID",
    }

    user_uid: str
    """Globally unique ID of the user."""

    organization_id: str
    """ID of the organization of the user."""

    person_id: str
    """ID of the person. Use it as the student ID for student accounts."""

    campaign_category_code: str | None = None
    """Campaign category code."""

    class_: ObjectInfo | None = None
    """Class of the student. Only set for students."""

    full_name: str
    """Full name of the user."""

    first_name: str | None = None
    """First name."""

    last_name: str | None = None
    """Surname."""

    detail_name: str
    """Additional information to the name."""

    persons_initials: str
    """Initials."""

    school_organization_name: str
    """Name of the school."""

    school_type: SchoolType | None = None
    """Type of school."""

    user_type: UserType
    """Type of user."""

    user_type_text: str
    """Type of user for display."""

    study_year: int | None = None
    """Grade of study."""

    children: list[UserInfoChild]
    """Children of the signed-in parent."""

    class_teacher_classes: list[str]
    """IDs of the classes where the user is the class teacher."""

    deputy_class_teacher_classes: list[str]
    """IDs of the classes where the user is the deputy class teacher."""

    install_type: InstallType
    """Installation type of the application for the organization."""

    language: LanguageCode
    """Preferred language."""

    school_year_id: str | None = None
    """ID of the school year."""

    enabled_modules: list[ModuleRights] | None = None
    """Rights in the enabled modules."""

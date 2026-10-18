from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from skolaonline.models._base import SkolaOnlineModel


class EmergencyNotificationType(StrEnum):
    EMERGENCY_STARTED = "emergencyStarted"
    EMERGENCY_EXPANDED = "emergencyExpanded"
    EMERGENCY_ENDED = "emergencyEnded"
    NEW_MESSAGE_SENT = "newMessageSent"


class NotificationFailureReason(StrEnum):
    NO_ERROR = "noError"
    TOKEN_NOT_VALID = "tokenNotValid"
    EXCEPTION = "exception"


@dataclass(kw_only=True)
class EmergencyMultiNotificationRequest(SkolaOnlineModel):
    notification: EmergencyNotification
    notification_recipients: list[EmergencyNotificationRecipient]


@dataclass(kw_only=True)
class EmergencyNotification(SkolaOnlineModel):
    project_name: str
    entity_id: str | None = None
    silent_notification: bool | None = None
    drill_notification: bool | None = None
    notification_title: str | None = None
    notification_body: str | None = None
    notification_icon_url: str | None = None
    emergency_start_time: datetime | None = None
    emergency_incident_type: str | None = None
    notification_type: EmergencyNotificationType | None = None


@dataclass(kw_only=True)
class EmergencyNotificationRecipient(SkolaOnlineModel):
    registration_token: str
    organization_id: str
    user_id: str
    firestore_jwt: str | None = None
    emergency_user_key: str | None = None
    related_person_ids: list[str] | None = None


@dataclass(kw_only=True)
class NotificationGroups(SkolaOnlineModel):
    groups: list[NotificationPreferenceDto] | None = None


@dataclass(kw_only=True)
class NotificationPreferenceDto(SkolaOnlineModel):
    group_id: str | None = None
    group_display_name: str | None = None
    person_id: str | None = None
    for_person_id: str | None = None
    is_active: bool | None = None


@dataclass(kw_only=True)
class NotificationPreferencesGroup(SkolaOnlineModel):
    group_id: str | None = None
    for_person_id: str | None = None
    is_active: bool | None = None


@dataclass(kw_only=True)
class NotificationRecipient(SkolaOnlineModel):
    registration_token: str
    organization_id: str
    user_id: str


@dataclass(kw_only=True)
class NotificationResponse(SkolaOnlineModel):
    registration_token: str | None = None
    success: bool | None = None
    failure_reason: NotificationFailureReason | None = None


@dataclass(kw_only=True)
class SavePreferencesRequest(SkolaOnlineModel):
    groups: list[NotificationPreferencesGroup] | None = None


@dataclass(kw_only=True)
class SimpleMultiNotificationRequest(SkolaOnlineModel):
    notification: SimpleNotification
    notification_recipients: list[NotificationRecipient]


@dataclass(kw_only=True)
class SimpleNotification(SkolaOnlineModel):
    project_name: str
    entity_id: str | None = None
    notification_title: str | None = None
    notification_body: str | None = None
    data: dict[str, str | None] | None = None


@dataclass(kw_only=True)
class TwoFactorMultiNotificationRequest(SkolaOnlineModel):
    notification: TwoFactorNotification
    notification_recipients: list[NotificationRecipient]


@dataclass(kw_only=True)
class TwoFactorNotification(SkolaOnlineModel):
    project_name: str
    entity_id: str | None = None
    notification_title: str | None = None
    notification_body: str | None = None

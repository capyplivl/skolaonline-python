from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from skolaonline.models._base import SkolaOnlineModel


class EmergencyNotificationType(StrEnum):
    """Type of emergency notification."""

    EMERGENCY_STARTED = "emergencyStarted"
    """Emergency started."""

    EMERGENCY_EXPANDED = "emergencyExpanded"
    """Emergency expanded."""

    EMERGENCY_ENDED = "emergencyEnded"
    """Emergency ended."""

    NEW_MESSAGE_SENT = "newMessageSent"
    """New message sent during the emergency."""


class NotificationFailureReason(StrEnum):
    """Reason a notification was not sent."""

    NO_ERROR = "noError"
    """Sent without errors."""

    TOKEN_NOT_VALID = "tokenNotValid"
    """The service rejected the token as invalid."""

    EXCEPTION = "exception"
    """Error while sending."""


@dataclass(kw_only=True)
class EmergencyMultiNotificationRequest(SkolaOnlineModel):
    """Emergency notifications for multiple recipients."""

    notification: EmergencyNotification
    """Notification data."""

    notification_recipients: list[EmergencyNotificationRecipient]
    """Recipients of the notification."""


@dataclass(kw_only=True)
class EmergencyNotification(SkolaOnlineModel):
    """Notification about an emergency."""

    project_name: str
    """Identifier of the project the notification is meant for."""

    entity_id: str | None = None
    """ID of the notified entity."""

    silent_notification: bool | None = None
    """Whether the notification is silent."""

    drill_notification: bool | None = None
    """Whether the emergency is a drill."""

    notification_title: str | None = None
    """Title of the notification."""

    notification_body: str | None = None
    """Body text of the notification."""

    notification_icon_url: str | None = None
    """URL of the notification icon."""

    emergency_start_time: datetime | None = None
    """Date and time the emergency started."""

    emergency_incident_type: str | None = None
    """Kind of incident, such as fire or chemicals."""

    notification_type: EmergencyNotificationType | None = None
    """Type of emergency notification."""


@dataclass(kw_only=True)
class EmergencyNotificationRecipient(SkolaOnlineModel):
    """Recipient of an emergency notification."""

    registration_token: str
    """Firebase registration token identifying the recipient device."""

    organization_id: str
    """ID of the organization of the user."""

    user_id: str
    """ID of the person."""

    firestore_jwt: str | None = None
    """JWT authenticating the user against Firestore."""

    emergency_user_key: str | None = None
    """Key for authentication within the emergency."""

    related_person_ids: list[str] | None = None
    """IDs of the children concerned by the emergency. Only set for parents."""


@dataclass(kw_only=True)
class NotificationGroups(SkolaOnlineModel):
    """Notification preferences grouped by notification group."""

    groups: list[NotificationPreferenceDto] | None = None
    """Notification preferences."""


@dataclass(kw_only=True)
class NotificationPreferenceDto(SkolaOnlineModel):
    """Notification preference of a group."""

    group_id: str | None = None
    """ID of the notification group."""

    group_display_name: str | None = None
    """Display name of the notification group."""

    person_id: str | None = None
    """ID of the person the preference belongs to."""

    for_person_id: str | None = None
    """ID of the person the notifications are about."""

    is_active: bool | None = None
    """Whether notifications of the group are enabled."""


@dataclass(kw_only=True)
class NotificationPreferencesGroup(SkolaOnlineModel):
    """Notification preference to save."""

    group_id: str | None = None
    """ID of the notification group."""

    for_person_id: str | None = None
    """ID of the person the notifications are about."""

    is_active: bool | None = None
    """Whether notifications of the group are enabled."""


@dataclass(kw_only=True)
class NotificationRecipient(SkolaOnlineModel):
    """Recipient of a notification."""

    registration_token: str
    """Firebase registration token identifying the recipient device."""

    organization_id: str
    """ID of the organization of the user."""

    user_id: str
    """ID of the person."""


@dataclass(kw_only=True)
class NotificationResponse(SkolaOnlineModel):
    """Result of sending a notification."""

    registration_token: str | None = None
    """Firebase registration token."""

    success: bool | None = None
    """Whether the notification was sent."""

    failure_reason: NotificationFailureReason | None = None
    """Reason the notification was not sent."""


@dataclass(kw_only=True)
class SavePreferencesRequest(SkolaOnlineModel):
    """Notification preferences to save."""

    groups: list[NotificationPreferencesGroup] | None = None
    """Notification preferences."""


@dataclass(kw_only=True)
class SimpleMultiNotificationRequest(SkolaOnlineModel):
    """General notifications for multiple recipients."""

    notification: SimpleNotification
    """Notification data."""

    notification_recipients: list[NotificationRecipient]
    """Recipients of the notification."""


@dataclass(kw_only=True)
class SimpleNotification(SkolaOnlineModel):
    """General notification."""

    project_name: str
    """Identifier of the project the notification is meant for."""

    entity_id: str | None = None
    """ID of the notified entity."""

    notification_title: str | None = None
    """Title of the notification."""

    notification_body: str | None = None
    """Body text of the notification."""

    data: dict[str, str | None] | None = None
    """Additional notification data."""


@dataclass(kw_only=True)
class TwoFactorMultiNotificationRequest(SkolaOnlineModel):
    """Two-factor authentication notifications for multiple recipients."""

    notification: TwoFactorNotification
    """Notification data."""

    notification_recipients: list[NotificationRecipient]
    """Recipients of the notification."""


@dataclass(kw_only=True)
class TwoFactorNotification(SkolaOnlineModel):
    """Two-factor authentication notification."""

    project_name: str
    """Identifier of the project the notification is meant for."""

    entity_id: str | None = None
    """ID of the notified entity."""

    notification_title: str | None = None
    """Title of the notification."""

    notification_body: str | None = None
    """Body text of the notification."""

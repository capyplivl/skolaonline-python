from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import ClassVar

from skolaonline.models._base import SkolaOnlineModel


class EmergencyEventType(StrEnum):
    """Whether an emergency is real or a drill."""

    EMERGENCY = "emergency"
    """Real emergency."""

    DRILL = "drill"
    """Drill."""


class EmergencyIncidentType(StrEnum):
    """Kind of incident that triggered the emergency."""

    FIRE = "fire"
    """Fire."""

    EXPLOSION = "explosion"
    """Explosion."""

    ARMED_ASSAILANT = "armedAssailant"
    """Armed assailant."""

    DANGEROUS_GAS = "dangerousGas"
    """Dangerous gas leak."""

    SUSPICIOUS_ITEM = "suspiciousItem"
    """Suspicious item."""

    BOMB_THREAT = "bombThreat"
    """Bomb threat."""

    EVACUATION_DRILL = "evacuationDrill"
    """Evacuation drill."""

    LOCKDOWN_DRILL = "lockdownDrill"
    """Lockdown drill."""


class InformParticipantsType(StrEnum):
    """Group of people notified about an emergency."""

    EMPLOYEES_AND_STUDENTS = "employeesAndStudents"
    """Employees and students."""

    EMPLOYEES_ONLY = "employeesOnly"
    """Employees only."""

    CRISIS_TEAM_MEMBERS = "crisisTeamMembers"
    """Members of the crisis team."""


class ParticipantSelectionType(StrEnum):
    """Kind of node in the emergency participant tree."""

    CLASS = "class"
    """Class."""

    CLASS_GROUP = "classGroup"
    """Group of classes."""

    EMPLOYEE = "employee"
    """Employee."""

    EMPLOYEE_GROUP = "employeeGroup"
    """Group of employees."""

    STUDENT = "student"
    """Student."""

    STUDENT_GROUP = "studentGroup"
    """Group of students."""


@dataclass(kw_only=True)
class GetParticipantsSelectionItemResponseSolApi(SkolaOnlineModel):
    """Node of the emergency participant tree."""

    _field_aliases: ClassVar[dict[str, str]] = {
        "id": "Id",
        "display_name": "DisplayName",
        "class_display_name": "ClassDisplayName",
        "type": "Type",
        "is_person": "IsPerson",
    }

    id: str | None = None
    """Unique identifier of the node in the format prefix:value, or only prefix for
    top-level nodes."""

    display_name: str | None = None
    """Display name of the node, such as a person, class or group name."""

    class_display_name: str | None = None
    """Name of the class, mostly used for students."""

    type: ParticipantSelectionType | None = None
    """Kind of node, such as employee, student, class or group."""

    is_person: bool | None = None
    """Whether the node is a single person rather than a group or category."""


@dataclass(kw_only=True)
class GetScenariosItemResponse(SkolaOnlineModel):
    """Saved emergency scenario."""

    _field_aliases: ClassVar[dict[str, str]] = {
        "emergency_incident_type": "EmergencyIncidentType",
        "emergency_event_type": "EmergencyEventType",
        "inform_participants_type": "InformParticipantsType",
        "notification_text": "NotificationText",
        "safety_confirmation": "SafetyConfirmation",
        "inform_parents": "InformParents",
        "check_list": "CheckList",
    }

    emergency_incident_type: EmergencyIncidentType
    """Kind of incident, such as fire or attack."""

    emergency_event_type: EmergencyEventType
    """Whether the event is a real emergency or a drill."""

    inform_participants_type: InformParticipantsType | None = None
    """Who is notified about the emergency."""

    notification_text: str
    """Notification text sent to participants when the scenario starts."""

    safety_confirmation: bool = False
    """Whether participants must confirm they are safe."""

    inform_parents: bool = False
    """Whether legal representatives of students are notified as well."""

    check_list: str | None = None
    """Steps to take during the incident."""


@dataclass(kw_only=True)
class ParticipantsResponse(SkolaOnlineModel):
    """One level of the emergency participant tree."""

    _field_aliases: ClassVar[dict[str, str]] = {
        "items": "Items",
    }

    items: list[GetParticipantsSelectionItemResponseSolApi] | None = None
    """Nodes of the tree level."""


@dataclass(kw_only=True)
class StartEmergencyRequest(SkolaOnlineModel):
    """Request to start an emergency."""

    incident_type: EmergencyIncidentType
    """Kind of incident, such as fire or evacuation drill."""

    event_type: EmergencyEventType
    """Whether the event is a real emergency or a drill."""

    require_safety_confirmation: bool = False
    """Whether participants must confirm they are safe."""

    inform_participants_type: InformParticipantsType
    """Group of participants that receive notifications."""

    inform_legal_representatives: bool | None = None
    """Whether legal representatives of students are notified."""

    is_whole_school_participating: bool = False
    """Whether the whole school participates."""

    notification_text: str
    """Notification text sent to participants."""

    participants_selection_ids: list[str]
    """IDs of the selected participants in the format prefix:value, for example
    employeeGroups:teachers."""


@dataclass(kw_only=True)
class StartEmergencyResponse(SkolaOnlineModel):
    """Result of starting an emergency."""

    _field_aliases: ClassVar[dict[str, str]] = {
        "emergency_user_key": "EmergencyUserKey",
        "custom_firebase_jwt": "CustomFirebaseJwt",
        "notification_count": "NotificationCount",
        "success_count": "SuccessCount",
    }

    emergency_user_key: str | None = None
    """Authentication key for the central emergency service. Set on success."""

    custom_firebase_jwt: str | None = None
    """JWT for Firebase. Set on success."""

    notification_count: int | None = None
    """Number of notifications that were meant to be sent."""

    success_count: int | None = None
    """Number of notifications delivered successfully."""

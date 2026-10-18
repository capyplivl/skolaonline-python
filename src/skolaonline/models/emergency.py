from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import ClassVar

from skolaonline.models._base import SkolaOnlineModel


class EmergencyEventType(StrEnum):
    EMERGENCY = "emergency"
    DRILL = "drill"


class EmergencyIncidentType(StrEnum):
    FIRE = "fire"
    EXPLOSION = "explosion"
    ARMED_ASSAILANT = "armedAssailant"
    DANGEROUS_GAS = "dangerousGas"
    SUSPICIOUS_ITEM = "suspiciousItem"
    BOMB_THREAT = "bombThreat"
    EVACUATION_DRILL = "evacuationDrill"
    LOCKDOWN_DRILL = "lockdownDrill"


class InformParticipantsType(StrEnum):
    EMPLOYEES_AND_STUDENTS = "employeesAndStudents"
    EMPLOYEES_ONLY = "employeesOnly"
    CRISIS_TEAM_MEMBERS = "crisisTeamMembers"


class ParticipantSelectionType(StrEnum):
    CLASS = "class"
    CLASS_GROUP = "classGroup"
    EMPLOYEE = "employee"
    EMPLOYEE_GROUP = "employeeGroup"
    STUDENT = "student"
    STUDENT_GROUP = "studentGroup"


@dataclass(kw_only=True)
class GetParticipantsSelectionItemResponseSolApi(SkolaOnlineModel):
    _field_aliases: ClassVar[dict[str, str]] = {
        "id": "Id",
        "display_name": "DisplayName",
        "class_display_name": "ClassDisplayName",
        "type": "Type",
        "is_person": "IsPerson",
    }

    id: str | None = None
    display_name: str | None = None
    class_display_name: str | None = None
    type: ParticipantSelectionType | None = None
    is_person: bool | None = None


@dataclass(kw_only=True)
class GetScenariosItemResponse(SkolaOnlineModel):
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
    emergency_event_type: EmergencyEventType
    inform_participants_type: InformParticipantsType | None = None
    notification_text: str
    safety_confirmation: bool = False
    inform_parents: bool = False
    check_list: str | None = None


@dataclass(kw_only=True)
class ParticipantsResponse(SkolaOnlineModel):
    _field_aliases: ClassVar[dict[str, str]] = {
        "items": "Items",
    }

    items: list[GetParticipantsSelectionItemResponseSolApi] | None = None


@dataclass(kw_only=True)
class StartEmergencyRequest(SkolaOnlineModel):
    incident_type: EmergencyIncidentType
    event_type: EmergencyEventType
    require_safety_confirmation: bool = False
    inform_participants_type: InformParticipantsType
    inform_legal_representatives: bool | None = None
    is_whole_school_participating: bool = False
    notification_text: str
    participants_selection_ids: list[str]


@dataclass(kw_only=True)
class StartEmergencyResponse(SkolaOnlineModel):
    _field_aliases: ClassVar[dict[str, str]] = {
        "emergency_user_key": "EmergencyUserKey",
        "custom_firebase_jwt": "CustomFirebaseJwt",
        "notification_count": "NotificationCount",
        "success_count": "SuccessCount",
    }

    emergency_user_key: str | None = None
    custom_firebase_jwt: str | None = None
    notification_count: int | None = None
    success_count: int | None = None

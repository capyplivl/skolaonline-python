from __future__ import annotations

import dataclasses
from datetime import datetime, timedelta, timezone

import pytest

from skolaonline import models
from skolaonline.models import (
    AllPayments,
    ClassbookHour,
    DataInterfaceClass,
    EmergencyEventType,
    EmergencyIncidentType,
    GetScenariosItemResponse,
    InformParticipantsType,
    InstallType,
    MessageData,
    ObjectInfo,
    PaymentStatus,
    SimpleNotification,
    SkolaOnlineModel,
    StartEmergencyRequest,
    UserInfoResponse,
    UserType,
)
from skolaonline.models._base import to_camel_case

USER_INFO = {
    "userUID": "user-1",
    "organizationID": "org-1",
    "personID": "person-1",
    "class": {"id": "c1", "abbrev": "1.A", "name": "First A"},
    "fullName": "Jan Novak",
    "detailName": "Novak Jan",
    "personsInitials": "JN",
    "schoolOrganizationName": "School",
    "userType": "student",
    "userTypeText": "Student",
    "studyYear": 1,
    "children": [],
    "classTeacherClasses": [],
    "deputyClassTeacherClasses": [],
    "installType": "sol",
    "language": "cs",
    "enabledModules": [
        {
            "module": {"moduleId": "api_rozvrh_zak", "moduleName": "Timetable"},
            "rights": ["read"],
            "moduleSettings": {"anything": [1, 2]},
        }
    ],
}


def test_to_camel_case() -> None:
    assert to_camel_case("school_year_id") == "schoolYearId"
    assert to_camel_case("id") == "id"


def test_parses_aliases_keywords_and_nested_models() -> None:
    user = UserInfoResponse.from_dict(USER_INFO)
    assert user.user_uid == "user-1"
    assert user.organization_id == "org-1"
    assert user.class_ == ObjectInfo(id="c1", abbrev="1.A", name="First A")
    assert user.user_type is UserType.STUDENT
    assert user.install_type is InstallType.SOL
    assert user.enabled_modules is not None
    module = user.enabled_modules[0]
    assert module.module.module_name == "Timetable"
    assert module.module_settings == {"anything": [1, 2]}


def test_round_trip_preserves_original_keys() -> None:
    user = UserInfoResponse.from_dict(USER_INFO)
    data = user.to_dict()
    assert data["class"] == USER_INFO["class"]
    assert data["userUID"] == "user-1"
    assert data["organizationID"] == "org-1"
    assert UserInfoResponse.from_dict(data) == user


def test_unknown_enum_value_is_kept_as_string() -> None:
    user = UserInfoResponse.from_dict({**USER_INFO, "schoolType": "future"})
    assert user.school_type == "future"


def test_missing_required_fields_become_none() -> None:
    user = UserInfoResponse.from_dict({"userUID": "user-1"})
    assert user.user_uid == "user-1"
    assert user.full_name is None


def test_parses_datetimes_and_numbers() -> None:
    payments = AllPayments.from_dict(
        {
            "payments": [
                {
                    "paymentsId": "p1",
                    "dueDate": "2024-09-30T00:00:00.1234567+02:00",
                    "amount": 150,
                    "status": "partiallyPaid",
                }
            ]
        }
    )
    assert payments.payments is not None
    item = payments.payments[0]
    assert item.due_date == datetime(
        2024, 9, 30, 0, 0, 0, 123456, tzinfo=timezone(timedelta(hours=2))
    )
    assert item.amount == 150.0
    assert isinstance(item.amount, float)
    assert item.status is PaymentStatus.PARTIALLY_PAID


def test_pascal_case_and_irregular_keys() -> None:
    cls = DataInterfaceClass.from_dict(
        {"ID": "1", "Abbrev": "1.A", "ClassTeacherID": "t"}
    )
    assert cls.id == "1"
    assert cls.abbrev == "1.A"
    assert cls.class_teacher_id == "t"
    assert cls.to_dict() == {"ID": "1", "Abbrev": "1.A", "ClassTeacherID": "t"}
    hour = ClassbookHour.from_dict({"udalost_Id": "e1", "poradi": 2})
    assert hour.udalost_id == "e1"
    assert hour.poradi == 2


def test_dictionary_values() -> None:
    notification = SimpleNotification.from_dict({"data": {"a": "1", "b": None}})
    assert notification.data == {"a": "1", "b": None}


def test_schema_defaults_are_used_when_missing() -> None:
    scenario = GetScenariosItemResponse.from_dict(
        {
            "EmergencyIncidentType": "fire",
            "EmergencyEventType": "drill",
            "NotificationText": "Leave the building",
        }
    )
    assert scenario.emergency_incident_type is EmergencyIncidentType.FIRE
    assert scenario.safety_confirmation is False
    assert scenario.inform_parents is False


def test_to_dict_omits_unset_optional_fields_only() -> None:
    request = StartEmergencyRequest(
        incident_type=EmergencyIncidentType.FIRE,
        event_type=EmergencyEventType.DRILL,
        inform_participants_type=InformParticipantsType.EMPLOYEES_ONLY,
        notification_text="Drill",
        participants_selection_ids=["employees"],
    )
    assert request.to_dict() == {
        "incidentType": "fire",
        "eventType": "drill",
        "requireSafetyConfirmation": False,
        "informParticipantsType": "employeesOnly",
        "isWholeSchoolParticipating": False,
        "notificationText": "Drill",
        "participantsSelectionIds": ["employees"],
    }


def test_to_dict_serializes_datetimes_and_special_aliases() -> None:
    message = MessageData(
        title="Hello",
        text="Body",
        recipients=["r1"],
        attachments=[],
        send_as_email=False,
        send_as_sms=True,
        send_as_system_message=True,
        vote_options=[],
        attachments_delete_date=datetime(2024, 10, 1, 12, 30),
    )
    data = message.to_dict()
    assert data["sendAsSMS"] is True
    assert data["attachmentsDeleteDate"] == "2024-10-01T12:30:00"
    assert "previousMessageId" not in data


def test_required_fields_are_keyword_only() -> None:
    with pytest.raises(TypeError):
        ObjectInfo("1")  # type: ignore[misc]


@pytest.mark.parametrize("name", models.__all__)
def test_every_model_resolves_its_fields(name: str) -> None:
    cls = getattr(models, name)
    if dataclasses.is_dataclass(cls) and issubclass(cls, SkolaOnlineModel):
        instance = cls.from_dict({})
        assert isinstance(instance.to_dict(), dict)

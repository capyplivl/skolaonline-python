from __future__ import annotations

from dataclasses import dataclass
from typing import Any, ClassVar

from skolaonline.models._base import SkolaOnlineModel


@dataclass(kw_only=True)
class AdditionalDataDefinition(SkolaOnlineModel):
    """Definition of additional student data."""

    nazev: str
    """Name of the item."""

    popis: str
    """Description of the item."""


@dataclass(kw_only=True)
class AdditionalDataDefinitionResponse(SkolaOnlineModel):
    """Definitions of additional student data."""

    data: list[AdditionalDataDefinition]
    """Definitions."""


@dataclass(kw_only=True)
class DataInterfaceClass(SkolaOnlineModel):
    """Class information."""

    _field_aliases: ClassVar[dict[str, str]] = {
        "id": "ID",
        "abbrev": "Abbrev",
        "name": "Name",
        "from_year": "FromYear",
        "study_length": "StudyLength",
        "class_teacher_id": "ClassTeacherID",
        "room_id": "RoomID",
        "division_id": "DivisionID",
        "grade": "Grade",
    }

    id: str | None = None
    """ID of the class."""

    abbrev: str | None = None
    """Abbreviation of the class."""

    name: str | None = None
    """Name of the class."""

    from_year: int | None = None
    """Year the students started their studies."""

    study_length: int | None = None
    """Length of study in years."""

    class_teacher_id: str | None = None
    """ID of the class teacher."""

    room_id: str | None = None
    """ID of the room where the class is taught."""

    division_id: str | None = None
    """Type of school."""

    grade: int | None = None
    """Grade of the class."""


@dataclass(kw_only=True)
class DataInterfaceClassesResponse(SkolaOnlineModel):
    """List of classes."""

    _field_aliases: ClassVar[dict[str, str]] = {
        "message_type": "MessageType",
        "classes": "Classes",
    }

    message_type: str | None = None
    """Type of the message."""

    classes: list[DataInterfaceClass] | None = None
    """Classes."""


@dataclass(kw_only=True)
class ExtraItem(SkolaOnlineModel):
    """Additional information."""

    _field_aliases: ClassVar[dict[str, str]] = {
        "name": "Name",
        "value": "Value",
    }

    name: str | None = None
    """Name."""

    value: str | None = None
    """Value."""


@dataclass(kw_only=True)
class Student(SkolaOnlineModel):
    """Student information."""

    _field_aliases: ClassVar[dict[str, str]] = {
        "id": "ID",
        "first_name": "FirstName",
        "last_name": "LastName",
        "gender": "Gender",
        "deleted": "Deleted",
        "class_name": "ClassName",
        "extra_items": "ExtraItems",
        "rodne_cislo": "RodneCislo",
        "evid_num": "EvidNum",
        "leaved": "Leaved",
        "evid_until": "EvidUntil",
        "email": "Email",
        "phone": "Phone",
        "phone_mobile": "PhoneMobile",
        "address_street": "AddressStreet",
        "address_number": "AddressNumber",
        "address_city": "AddressCity",
        "address_zip": "AddressZIP",
    }

    id: str | None = None
    """ID of the student."""

    first_name: str | None = None
    """First name of the student."""

    last_name: str | None = None
    """Surname of the student."""

    gender: str | None = None
    """Gender of the student."""

    deleted: bool | None = None
    """Whether the student is deleted."""

    class_name: str | None = None
    """Class of the student."""

    extra_items: list[ExtraItem] | None = None
    """Additional information."""

    rodne_cislo: str | None = None
    """Czech personal identification number of the student."""

    evid_num: str | None = None
    """Registration number of the student."""

    leaved: str | None = None
    """Whether the student has left the school."""

    evid_until: str | None = None
    """Date until which the student is registered."""

    email: str | None = None
    """Email address of the student."""

    phone: str | None = None
    """Phone number of the student."""

    phone_mobile: str | None = None
    """Mobile phone number of the student."""

    address_street: str | None = None
    """Street of the student address."""

    address_number: str | None = None
    """House number of the student address."""

    address_city: str | None = None
    """City of the student address."""

    address_zip: str | None = None
    """Postal code of the student address."""


@dataclass(kw_only=True)
class StudentData(SkolaOnlineModel):
    """Student record with optional additional data."""

    jmeno: str | None = None
    """First name."""

    prijmeni: str
    """Surname."""

    organizace_id: str
    """ID of the organization."""

    skola: str
    """Name of the school."""

    cast_skoly: str
    """Part of the school."""

    osoba_id: str
    """ID of the person."""

    trida: str
    """Class."""

    oddeleni_skolni_druziny: str | None = None
    """After-school club department."""

    stravuje_se: bool
    """Whether the student eats in the school canteen."""

    ubytovan: bool
    """Whether the student is accommodated in a dormitory."""

    dalsi_udaje: Any = None
    """Additional data requested by name."""


@dataclass(kw_only=True)
class StudentsListResponse(SkolaOnlineModel):
    """Student records."""

    data: list[StudentData]
    """Student records."""


@dataclass(kw_only=True)
class StudentsResponse(SkolaOnlineModel):
    """List of students."""

    _field_aliases: ClassVar[dict[str, str]] = {
        "message_type": "MessageType",
        "students": "Students",
    }

    message_type: str | None = None
    """Type of the message."""

    students: list[Student] | None = None
    """Students."""


@dataclass(kw_only=True)
class StudentsWithConsentResponse(SkolaOnlineModel):
    """List of students who granted a consent."""

    _field_aliases: ClassVar[dict[str, str]] = {
        "message_type": "MessageType",
        "students": "Students",
    }

    message_type: str | None = None
    """Type of the message."""

    students: list[Student] | None = None
    """Students."""

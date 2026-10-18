from __future__ import annotations

from dataclasses import dataclass
from typing import Any, ClassVar

from skolaonline.models._base import SkolaOnlineModel


@dataclass(kw_only=True)
class AdditionalDataDefinition(SkolaOnlineModel):
    nazev: str
    popis: str


@dataclass(kw_only=True)
class AdditionalDataDefinitionResponse(SkolaOnlineModel):
    data: list[AdditionalDataDefinition]


@dataclass(kw_only=True)
class DataInterfaceClass(SkolaOnlineModel):
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
    abbrev: str | None = None
    name: str | None = None
    from_year: int | None = None
    study_length: int | None = None
    class_teacher_id: str | None = None
    room_id: str | None = None
    division_id: str | None = None
    grade: int | None = None


@dataclass(kw_only=True)
class DataInterfaceClassesResponse(SkolaOnlineModel):
    _field_aliases: ClassVar[dict[str, str]] = {
        "message_type": "MessageType",
        "classes": "Classes",
    }

    message_type: str | None = None
    classes: list[DataInterfaceClass] | None = None


@dataclass(kw_only=True)
class ExtraItem(SkolaOnlineModel):
    _field_aliases: ClassVar[dict[str, str]] = {
        "name": "Name",
        "value": "Value",
    }

    name: str | None = None
    value: str | None = None


@dataclass(kw_only=True)
class Student(SkolaOnlineModel):
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
    first_name: str | None = None
    last_name: str | None = None
    gender: str | None = None
    deleted: bool | None = None
    class_name: str | None = None
    extra_items: list[ExtraItem] | None = None
    rodne_cislo: str | None = None
    evid_num: str | None = None
    leaved: str | None = None
    evid_until: str | None = None
    email: str | None = None
    phone: str | None = None
    phone_mobile: str | None = None
    address_street: str | None = None
    address_number: str | None = None
    address_city: str | None = None
    address_zip: str | None = None


@dataclass(kw_only=True)
class StudentData(SkolaOnlineModel):
    jmeno: str | None = None
    prijmeni: str
    organizace_id: str
    skola: str
    cast_skoly: str
    osoba_id: str
    trida: str
    oddeleni_skolni_druziny: str | None = None
    stravuje_se: bool
    ubytovan: bool
    dalsi_udaje: Any = None


@dataclass(kw_only=True)
class StudentsListResponse(SkolaOnlineModel):
    data: list[StudentData]


@dataclass(kw_only=True)
class StudentsResponse(SkolaOnlineModel):
    _field_aliases: ClassVar[dict[str, str]] = {
        "message_type": "MessageType",
        "students": "Students",
    }

    message_type: str | None = None
    students: list[Student] | None = None


@dataclass(kw_only=True)
class StudentsWithConsentResponse(SkolaOnlineModel):
    _field_aliases: ClassVar[dict[str, str]] = {
        "message_type": "MessageType",
        "students": "Students",
    }

    message_type: str | None = None
    students: list[Student] | None = None

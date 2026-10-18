from __future__ import annotations

from dataclasses import dataclass

from skolaonline.models._base import SkolaOnlineModel


@dataclass(kw_only=True)
class StudentStatusResponse(SkolaOnlineModel):
    total_pages: int | None = None
    school: StudentStatusSchool | None = None
    students: list[StudentStatusStudent] | None = None


@dataclass(kw_only=True)
class StudentStatusSchool(SkolaOnlineModel):
    school_instance_id: str
    tax_number: str | None = None
    name: str | None = None
    address: StudentStatusSchoolAddress | None = None


@dataclass(kw_only=True)
class StudentStatusSchoolAddress(SkolaOnlineModel):
    city: str | None = None
    region: str | None = None
    district: str | None = None
    street: str | None = None
    street_number: str | None = None
    city_part: str | None = None
    post_number: str | None = None


@dataclass(kw_only=True)
class StudentStatusStudent(SkolaOnlineModel):
    first_name: str
    last_name: str
    birth_date: str
    student_address: StudentStatusStudentAddress | None = None
    studies: list[StudentStatusStudy] | None = None


@dataclass(kw_only=True)
class StudentStatusStudentAddress(SkolaOnlineModel):
    city: str | None = None
    region: str | None = None
    district: str | None = None
    street: str | None = None
    street_number: str | None = None
    city_part: str | None = None
    post_number: str | None = None


@dataclass(kw_only=True)
class StudentStatusStudy(SkolaOnlineModel):
    start_of_study: str | None = None
    end_of_study: str | None = None
    school_type: str | None = None
    study_type: int | None = None
    study_form: int | None = None
    grade: int | None = None
    study_length: int | None = None

from __future__ import annotations

from dataclasses import dataclass

from skolaonline.models._base import SkolaOnlineModel


@dataclass(kw_only=True)
class StudentStatusResponse(SkolaOnlineModel):
    """Student status data of an organization."""

    total_pages: int | None = None
    """Total number of pages, one page per organization."""

    school: StudentStatusSchool | None = None
    """School information."""

    students: list[StudentStatusStudent] | None = None
    """Students."""


@dataclass(kw_only=True)
class StudentStatusSchool(SkolaOnlineModel):
    """School in the student status data."""

    school_instance_id: str
    """Identifier of the organization the data belongs to."""

    tax_number: str | None = None
    """Company registration number of the school."""

    name: str | None = None
    """Name of the school."""

    address: StudentStatusSchoolAddress | None = None
    """Address of the school."""


@dataclass(kw_only=True)
class StudentStatusSchoolAddress(SkolaOnlineModel):
    """Address of a school."""

    city: str | None = None
    """City."""

    region: str | None = None
    """Region. One of Praha, Stredocesky, Jihocesky, Plzensky, Karlovarsky, Ustecky,
    Liberecky, Kralovehradecky, Pardubicky, Vysocina, Jihomoravsky, Olomoucky,
    Zlinsky, Moravskoslezsky."""

    district: str | None = None
    """District."""

    street: str | None = None
    """Street."""

    street_number: str | None = None
    """House number."""

    city_part: str | None = None
    """Part of the municipality."""

    post_number: str | None = None
    """Postal code."""


@dataclass(kw_only=True)
class StudentStatusStudent(SkolaOnlineModel):
    """Student in the student status data."""

    first_name: str
    """First name."""

    last_name: str
    """Surname."""

    birth_date: str
    """Date of birth."""

    student_address: StudentStatusStudentAddress | None = None
    """Address of the student."""

    studies: list[StudentStatusStudy] | None = None
    """Study information."""


@dataclass(kw_only=True)
class StudentStatusStudentAddress(SkolaOnlineModel):
    """Address of a student."""

    city: str | None = None
    """City."""

    region: str | None = None
    """Region of the permanent residence of the student. One of Praha, Stredocesky,
    Jihocesky, Plzensky, Karlovarsky, Ustecky, Liberecky, Kralovehradecky,
    Pardubicky, Vysocina, Jihomoravsky, Olomoucky, Zlinsky, Moravskoslezsky."""

    district: str | None = None
    """District."""

    street: str | None = None
    """Street."""

    street_number: str | None = None
    """House number."""

    city_part: str | None = None
    """Part of the municipality."""

    post_number: str | None = None
    """Postal code."""


@dataclass(kw_only=True)
class StudentStatusStudy(SkolaOnlineModel):
    """Study of a student."""

    start_of_study: str | None = None
    """Start date of the studies."""

    end_of_study: str | None = None
    """End date of the studies."""

    school_type: str | None = None
    """Type of school. One of Ms, Zs, Ss, Kon, Vos."""

    study_type: int | None = None
    """Code of the kind of education from the RADV code list. One of 10, 21, 22, 31,
    32, 34, 41, 42, 43, 61, 91, 92."""

    study_form: int | None = None
    """Code of the form of education from the RAFS code list. One of 10, 22, 23, 24,
    30."""

    grade: int | None = None
    """Code of the grade from the RARO code list. One of 1 to 10."""

    study_length: int | None = None
    """Code of the length of the educational program from the RADS code list. One of
    5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 80, 90, 100."""

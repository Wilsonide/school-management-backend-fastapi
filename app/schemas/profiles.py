from datetime import date
from typing import Union
from uuid import UUID

from pydantic import BaseModel


class BaseProfileResponse(BaseModel):
    id: UUID
    user_id: UUID
    school_id: UUID


class StudentProfileCreate(BaseModel):
    admission_number: str
    admission_date: date
    date_of_birth: date
    gender: str


class StudentProfileUpdate(BaseModel):
    admission_number: str | None = None
    admission_date: date | None = None
    date_of_birth: date | None = None
    gender: str | None = None
    class_id: UUID | None = None


class StudentProfileResponse(StudentProfileCreate):
    id: UUID
    user_id: UUID
    school_id: UUID

    class Config:
        from_attributes = True


class TeacherProfileCreate(BaseModel):
    employee_id: str
    hire_date: date
    qualification: str
    specialization: str


class TeacherProfileUpdate(BaseModel):
    employee_id: str | None = None
    hire_date: date | None = None
    qualification: str | None = None
    specialization: str | None = None


class TeacherProfileResponse(TeacherProfileCreate):
    id: UUID
    user_id: UUID
    school_id: UUID

    class Config:
        from_attributes = True


class ParentProfileCreate(BaseModel):
    occupation: str
    phone: str


class ParentProfileUpdate(BaseModel):
    occupation: str | None = None
    phone: str | None = None


class ParentProfileResponse(ParentProfileCreate):
    id: UUID
    user_id: UUID
    school_id: UUID

    class Config:
        from_attributes = True


ProfileCreateSchema = Union[
    StudentProfileCreate,
    TeacherProfileCreate,
    ParentProfileCreate,
]

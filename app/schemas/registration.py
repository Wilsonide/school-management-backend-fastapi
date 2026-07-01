from datetime import date
from typing import Literal

from pydantic import BaseModel, EmailStr

# ===============================
# STUDENT
# ===============================


class StudentRegistrationCreate(BaseModel):
    first_name: str
    last_name: str

    email: EmailStr
    username: str

    gender: str
    date_of_birth: date
    admission_date: date

    class_id: str


# ===============================
# TEACHER
# ===============================


class TeacherRegistrationCreate(BaseModel):
    first_name: str
    last_name: str

    email: EmailStr
    username: str

    qualification: str
    specialization: str

    hire_date: date

    class_id: str


# ===============================
# PARENT
# ===============================


class BatchImportResponse(BaseModel):
    total: int
    success: int
    failed: int
    users: list[dict]


class ParentRegistrationCreate(BaseModel):
    first_name: str
    last_name: str

    email: EmailStr
    username: str

    occupation: str
    phone: str


# ===============================
# RESPONSE
# ===============================


class RegistrationResponse(BaseModel):
    username: str
    password: str

    first_name: str
    last_name: str

    role: Literal[
        "STUDENT",
        "TEACHER",
        "PARENT",
    ]

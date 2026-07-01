from datetime import date
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

# =====================================================
# STUDENT SINGLE REGISTRATION
# =====================================================


class StudentRegistrationRequest(BaseModel):
    first_name: str = Field(..., max_length=100)
    last_name: str = Field(..., max_length=100)
    other_name: Optional[str] = None

    gender: str

    date_of_birth: Optional[date] = None

    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None

    address: Optional[str] = None

    class_id: UUID

    admission_number: str

    guardian_name: Optional[str] = None
    guardian_phone: Optional[str] = None


# =====================================================
# TEACHER SINGLE REGISTRATION
# =====================================================


class TeacherRegistrationRequest(BaseModel):
    first_name: str
    last_name: str
    other_name: Optional[str] = None

    gender: str

    email: EmailStr

    phone_number: Optional[str] = None

    address: Optional[str] = None

    staff_id: str

    qualification: Optional[str] = None


# =====================================================
# STUDENT EXCEL ROW
# =====================================================


class StudentImportRow(BaseModel):
    first_name: str

    last_name: str

    other_name: Optional[str] = None

    gender: str

    date_of_birth: Optional[date] = None

    admission_number: str

    email: Optional[EmailStr] = None

    phone_number: Optional[str] = None

    address: Optional[str] = None

    class_name: str

    guardian_name: Optional[str] = None

    guardian_phone: Optional[str] = None


# =====================================================
# TEACHER EXCEL ROW
# =====================================================


class TeacherImportRow(BaseModel):
    first_name: str

    last_name: str

    other_name: Optional[str] = None

    gender: str

    email: EmailStr

    phone_number: Optional[str] = None

    address: Optional[str] = None

    staff_id: str

    qualification: Optional[str] = None


# =====================================================
# IMPORT ERRORS
# =====================================================


class ImportError(BaseModel):
    row: int

    field: Optional[str] = None

    message: str


# =====================================================
# IMPORT SUMMARY
# =====================================================


class BulkImportResponse(BaseModel):
    total: int

    imported: int

    failed: int

    errors: list[ImportError] = []


# =====================================================
# LOGIN CREDENTIAL
# =====================================================


class CredentialResponse(BaseModel):
    id: UUID

    full_name: str

    username: str

    password: Optional[str] = None

    role: str

    active: bool


# =====================================================
# RESET PASSWORD
# =====================================================


class ResetPasswordRequest(BaseModel):
    new_password: Optional[str] = None


class ResetPasswordResponse(BaseModel):
    message: str

    username: str

    password: str


# =====================================================
# ACCOUNT STATUS
# =====================================================


class AccountStatusResponse(BaseModel):
    message: str


# =====================================================
# EXPORTED CREDENTIAL
# =====================================================


class ExportCredential(BaseModel):
    full_name: str

    username: str

    password: str

    role: str


# =====================================================
# TEMPLATE DOWNLOAD
# =====================================================


class TemplateResponse(BaseModel):
    filename: str

    message: str

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

# =====================================================
# INPUT SCHEMAS
# =====================================================


class SubjectScoreInput(BaseModel):
    subject_id: UUID

    ca_score: int = Field(
        ge=0,
        le=40,
    )

    exam_score: int = Field(
        ge=0,
        le=60,
    )

    teacher_comment: str | None = None


class StudentResultInput(BaseModel):
    student_id: UUID

    scores: list[SubjectScoreInput]


class ResultBatchCreate(BaseModel):
    class_id: UUID

    session_id: UUID

    term_id: UUID

    students: list[StudentResultInput]


# =====================================================
# TEACHER COMMENT
# =====================================================


class UpdateTeacherComment(BaseModel):
    teacher_comment: str

class TeacherComment(BaseModel):
    comment: str


# =====================================================
# ADMIN ACTIONS
# =====================================================


class RejectResultRequest(BaseModel):
    note: str


class PublishResultRequest(BaseModel):
    note: str | None = None


# =====================================================
# RESULT RECORD RESPONSE
# =====================================================


class ResultRecordResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID

    student_id: UUID

    subject_id: UUID

    ca_score: int

    exam_score: int

    total_score: int

    grade: str

    remark: str | None

    teacher_comment: str | None


# =====================================================
# SUBJECT VIEW FOR REPORT CARD
# =====================================================


class StudentSubjectResult(BaseModel):
    subject_id: UUID

    subject_name: str

    ca_score: int

    exam_score: int

    total_score: int

    grade: str

    remark: str | None

    teacher_comment: str | None


# =====================================================
# SUMMARY RESPONSE
# =====================================================


class ResultSummaryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    student_id: UUID

    total_score: int

    average_score: float

    subjects_offered: int

    passed_subjects: int

    failed_subjects: int

    position: int | None

    principal_comment: str | None


# =====================================================
# STUDENT RESULT VIEW
# =====================================================


class StudentResultResponse(BaseModel):
    student_id: UUID

    student_name: str

    class_name: str

    session_name: str

    term_name: str

    total_score: int

    average_score: float

    position: int | None

    principal_comment: str | None

    results: list[StudentSubjectResult]


# =====================================================
# CLASS RESULT VIEW
# =====================================================


class ClassStudentResult(BaseModel):
    student_id: UUID

    student_name: str

    total_score: int

    average_score: float

    position: int | None


class ClassResultResponse(BaseModel):
    batch_id: UUID

    class_id: UUID

    session_id: UUID

    term_id: UUID

    status: str

    created_at: datetime

    students: list[ClassStudentResult]


# =====================================================
# BATCH RESPONSE
# =====================================================


class ResultBatchResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID

    class_id: UUID

    session_id: UUID

    term_id: UUID

    status: str

    version: int

    requires_review: bool

    published_at: datetime | None


# =====================================================
# APPROVAL HISTORY
# =====================================================


class ResultApprovalResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID

    action: str

    action_by: UUID

    note: str | None

    action_at: datetime


# =====================================================
# SUBMIT RESPONSE
# =====================================================


class ResultSubmissionResponse(BaseModel):
    batch_id: UUID

    status: str

    total_students: int

    total_records: int


# =====================================================
# APPROVE RESPONSE
# =====================================================


class ResultApprovalActionResponse(BaseModel):
    batch_id: UUID

    status: str

    message: str

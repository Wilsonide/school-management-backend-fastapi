from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ApprovalHistoryItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    action: str
    note: str | None
    action_by: UUID
    action_at: datetime

class SubjectResultResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    subject_id: UUID
    subject_name: str

    ca_score: int
    exam_score: int

    total_score: int

    grade: str

    remark: str

    teacher_comment: str | None

class StudentResultResponse(BaseModel):

    student_id: UUID

    total_score: int

    average_score: float

    position: int

    passed_subjects: int

    failed_subjects: int

    subjects: list[SubjectResultResponse]
class ClassStudentResultResponse(BaseModel):

    student_id: UUID

    student_name: str

    total_score: int

    average_score: float

    position: int

class ClassResultResponse(BaseModel):

    batch_id: UUID

    class_id: UUID

    session_id: UUID

    term_id: UUID

    status: str

    students: list[ClassStudentResultResponse]

class ResultSubmissionResponse(BaseModel):

    batch_id: UUID

    status: str

    students: int

    records: int

class ResultBatchStatusResponse(BaseModel):
    batch_id: UUID
    status: str
    message: str
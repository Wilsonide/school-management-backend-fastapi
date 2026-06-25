from pydantic import BaseModel


class AssessmentInputSchema(BaseModel):
    student_id: str
    class_id: str
    subject_id: str
    session_id: str
    term_id: str

    ca_score: float = 0
    exam_score: float = 0
    assignment_score: float = 0
    attendance_score: float = 0
    participation_score: float = 0
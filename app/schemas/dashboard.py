from pydantic import BaseModel


class AttendanceSummarySchema(BaseModel):
    present: int
    absent: int
    late: int
    attendance_rate: float


class StudentDashboardResponse(BaseModel):
    student_name: str
    admission_number: str | None

    class_name: str | None

    current_session: str | None
    current_term: str | None

    attendance: AttendanceSummarySchema

    average_score: float
    position: int | None

    recent_lessons: list[dict]


class TeacherDashboardResponse(BaseModel):
    teacher_name: str

    assigned_classes: int
    assigned_subjects: int

    lessons_uploaded: int

    attendance_submissions: int

    results_submitted: int

    assignments: list[dict]
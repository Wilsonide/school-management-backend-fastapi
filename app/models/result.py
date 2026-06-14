from sqlalchemy import UUID, Float, ForeignKey, String
from sqlalchemy.orm import mapped_column

from app.db.base import Base, UUIDMixin


class Result(Base, UUIDMixin):
    __tablename__ = "results"

    assessment_id = mapped_column(UUID, ForeignKey("assessments.id"))

    student_id = mapped_column(UUID, ForeignKey("student_profiles.id"))

    score = mapped_column(Float)

    grade = mapped_column(String)

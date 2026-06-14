from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import mapped_column

from app.db.base import Base, UUIDMixin


class Enrollment(Base, UUIDMixin):
    __tablename__ = "enrollments"

    student_id = mapped_column(UUID, ForeignKey("student_profiles.id"))

    class_id = mapped_column(UUID, ForeignKey("classes.id"))

    session_id = mapped_column(UUID, ForeignKey("academic_sessions.id"))

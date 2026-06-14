from sqlalchemy import UUID, Date, ForeignKey, String
from sqlalchemy.orm import mapped_column

from app.db.base import Base, UUIDMixin


class Attendance(Base, UUIDMixin):
    __tablename__ = "attendance"

    student_id = mapped_column(UUID, ForeignKey("student_profiles.id"))

    class_id = mapped_column(UUID, ForeignKey("classes.id"))

    date = mapped_column(Date)

    status = mapped_column(String)

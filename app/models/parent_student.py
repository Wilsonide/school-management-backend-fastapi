from sqlalchemy import UUID, ForeignKey, String
from sqlalchemy.orm import mapped_column

from app.db.base import Base, UUIDMixin


class StudentParent(Base, UUIDMixin):
    __tablename__ = "student_parents"

    student_id = mapped_column(UUID, ForeignKey("student_profiles.id"))

    parent_id = mapped_column(UUID, ForeignKey("parent_profiles.id"))

    relationship = mapped_column(String)

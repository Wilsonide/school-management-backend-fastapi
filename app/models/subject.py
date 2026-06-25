from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import (
    Base,
    TenantMixin,
    UUIDMixin,
)


class Subject(
    Base,
    UUIDMixin,
    TenantMixin,
):
    __tablename__ = "subjects"

    name: Mapped[str] = mapped_column(
        String(255)
    )

    code: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    teacher_assignments = relationship(
        "TeacherClassSubject",
        back_populates="subject",
        cascade="all, delete-orphan",
    )

    class_subjects = relationship(
    "ClassSubject",
    back_populates="subject",
    cascade="all, delete-orphan",
)
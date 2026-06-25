from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import (
    Base,
    TenantMixin,
    TimestampMixin,
    UUIDMixin,
)


class Class(
    Base,
    UUIDMixin,
    TenantMixin,
    TimestampMixin,
):
    __tablename__ = "classes"

    name: Mapped[str] = mapped_column(String(100))

    level: Mapped[str] = mapped_column(String(50))

    enrollments = relationship(
        "StudentEnrollment",
        back_populates="school_class",
        cascade="all, delete-orphan",
    )

    teacher_assignments = relationship(
        "TeacherClassSubject",
        back_populates="school_class",
        cascade="all, delete-orphan",
    )
    class_subjects = relationship(
    "ClassSubject",
    back_populates="school_class",
    cascade="all, delete-orphan",
)

from uuid import UUID

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import (
    Base,
    TenantMixin,
    TimestampMixin,
    UUIDMixin,
)


class TeacherClassSubject(
    Base,
    UUIDMixin,
    TenantMixin,
    TimestampMixin,
):
    __tablename__ = "teacher_class_subjects"

    teacher_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        index=True,
    )

    class_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "classes.id",
            ondelete="CASCADE",
        ),
        index=True,
    )

    subject_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "subjects.id",
            ondelete="CASCADE",
        ),
        index=True,
    )

    teacher = relationship(
        "User",
        back_populates="teacher_assignments",
    )

    school_class = relationship(
        "Class",
        back_populates="teacher_assignments",
    )

    subject = relationship(
        "Subject",
        back_populates="teacher_assignments",
    )

    __table_args__ = (
        UniqueConstraint(
            "teacher_id",
            "class_id",
            "subject_id",
            name="uq_teacher_class_subject",
        ),
    )
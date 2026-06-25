from uuid import UUID

from sqlalchemy import Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import (
    Base,
    TenantMixin,
    TimestampMixin,
    UUIDMixin,
)


class StudentEnrollment(
    Base,
    UUIDMixin,
    TenantMixin,
    TimestampMixin,
):
    __tablename__ = "student_enrollments"

    student_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        index=True,
    )

    class_id: Mapped[UUID] = mapped_column(
        ForeignKey("classes.id"),
        index=True,
    )

    session_id: Mapped[UUID] = mapped_column(
        ForeignKey("academic_sessions.id"),
        index=True,
    )

    is_current: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    student = relationship(
        "User",
        back_populates="enrollments",
    )

    school_class = relationship(
        "Class",
        back_populates="enrollments",
    )

    session = relationship("AcademicSession")

    __table_args__ = (
        UniqueConstraint(
            "student_id",
            "session_id",
            name="uq_student_session_enrollment",
        ),
    )

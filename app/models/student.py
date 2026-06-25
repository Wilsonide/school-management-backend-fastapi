from uuid import UUID

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import (
    Base,
    TenantMixin,
    TimestampMixin,
    UUIDMixin,
)


class StudentProfile(
    Base,
    UUIDMixin,
    TenantMixin,
    TimestampMixin,
):
    __tablename__ = "student_profiles"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        unique=True,
        index=True,
    )

    admission_number: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
    )

    admission_date: Mapped[Date | None] = mapped_column(
        Date,
        nullable=True,
    )

    date_of_birth: Mapped[Date | None] = mapped_column(
        Date,
        nullable=True,
    )

    gender: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    user = relationship(
        "User",
        back_populates="student_profile",
    )

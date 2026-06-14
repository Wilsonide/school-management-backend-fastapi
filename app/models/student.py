from uuid import UUID

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TenantMixin, UUIDMixin


class StudentProfile(Base, UUIDMixin, TenantMixin):
    __tablename__ = "student_profiles"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        index=True,
    )

    admission_number: Mapped[str] = mapped_column(String, unique=True)

    admission_date: Mapped[Date] = mapped_column(Date, nullable=True)

    date_of_birth: Mapped[Date] = mapped_column(Date, nullable=True)

    gender: Mapped[str] = mapped_column(String, nullable=True)

    class_id: Mapped[UUID] = mapped_column(
        ForeignKey("classes.id"),
        nullable=True,
    )

    user = relationship("User", back_populates="student_profile")
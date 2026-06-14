from uuid import UUID

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TenantMixin, UUIDMixin


class TeacherProfile(Base, UUIDMixin, TenantMixin):
    __tablename__ = "teacher_profiles"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        index=True,
    )

    employee_id: Mapped[str] = mapped_column(String, unique=True)

    hire_date: Mapped[Date] = mapped_column(Date, nullable=True)

    qualification: Mapped[str] = mapped_column(String, nullable=True)

    specialization: Mapped[str] = mapped_column(String, nullable=True)

    user = relationship("User", back_populates="teacher_profile")
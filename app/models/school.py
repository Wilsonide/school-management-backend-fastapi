from typing import TYPE_CHECKING

from sqlalchemy import Boolean, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDMixin
if TYPE_CHECKING:
    from app.models.academic_session import AcademicSession
    from app.models.attendance import Attendance
    from app.models.classes import Class
    from app.models.exam import Exam
    from app.models.refresh_token import RefreshToken
    from app.models.user import User



class School(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "schools"

    name: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
    )

    email: Mapped[str] = mapped_column(String(255))
    phone: Mapped[str] = mapped_column(String(50))

    logo_url: Mapped[str | None] = mapped_column(String(255))
    address: Mapped[str | None] = mapped_column(Text)

    subscription_plan: Mapped[str] = mapped_column(default="basic")
    website: Mapped[str | None] = mapped_column(String(255))
    code: Mapped[str] = mapped_column(String(50), unique=True)  # INVITE CODE

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    users: Mapped[list["User"]] = relationship(
    "User",
    back_populates="school",
    cascade="all, delete-orphan",
)

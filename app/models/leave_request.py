from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TenantMixin, UUIDMixin


class LeaveRequest(Base, UUIDMixin, TenantMixin):
    __tablename__ = "leave_requests"

    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))

    reason: Mapped[str]

    status: Mapped[str] = mapped_column(
        String(50),
        default="pending",
    )

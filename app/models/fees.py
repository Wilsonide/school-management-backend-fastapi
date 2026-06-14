from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TenantMixin, UUIDMixin


class Fee(Base, UUIDMixin, TenantMixin):
    __tablename__ = "fees"

    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))

    amount: Mapped[float] = mapped_column(Numeric(10, 2))

    status: Mapped[str] = mapped_column(String(50))

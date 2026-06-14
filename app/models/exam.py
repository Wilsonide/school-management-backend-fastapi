from datetime import date

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TenantMixin, UUIDMixin


class Exam(Base, UUIDMixin, TenantMixin):
    __tablename__ = "exams"

    title: Mapped[str] = mapped_column(String(255))

    classroom_id: Mapped[int] = mapped_column(ForeignKey("classrooms.id"))

    exam_date: Mapped[date] = mapped_column(Date)

    term: Mapped[str]

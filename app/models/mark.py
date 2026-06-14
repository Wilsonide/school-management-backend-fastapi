from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TenantMixin, UUIDMixin


class Mark(Base, UUIDMixin, TenantMixin):
    __tablename__ = "marks"

    id: Mapped[int] = mapped_column(primary_key=True)

    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))

    exam_id: Mapped[int] = mapped_column(ForeignKey("exams.id"))

    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"))

    score: Mapped[float] = mapped_column(Numeric(5, 2))

    grade: Mapped[str]

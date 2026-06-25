from uuid import UUID

from sqlalchemy import ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import (
    Base,
    TenantMixin,
    TimestampMixin,
    UUIDMixin,
)


class ResultRecord(
    Base,
    UUIDMixin,
    TenantMixin,
    TimestampMixin,
):
    __tablename__ = "result_records"

    batch_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "result_batches.id",
            ondelete="CASCADE",
        ),
        index=True,
    )

    student_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"),
        index=True,
    )

    subject_id: Mapped[UUID] = mapped_column(
        ForeignKey("subjects.id"),
        index=True,
    )

    ca_score: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    exam_score: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    total_score: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    grade: Mapped[str] = mapped_column(
        String(5),
    )

    remark: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    teacher_comment: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    batch = relationship(
        "ResultBatch",
        back_populates="records",
    )

    student = relationship("User")

    subject = relationship("Subject")

    __table_args__ = (
        UniqueConstraint(
            "batch_id",
            "student_id",
            "subject_id",
            name="uq_result_record",
        ),
    )

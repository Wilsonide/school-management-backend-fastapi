from uuid import UUID

from sqlalchemy import Float, ForeignKey, Integer, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import (
    Base,
    TenantMixin,
    TimestampMixin,
    UUIDMixin,
)


class ResultSummary(
    Base,
    UUIDMixin,
    TenantMixin,
    TimestampMixin,
):
    __tablename__ = "result_summaries"

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

    total_score: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    average_score: Mapped[float] = mapped_column(
        Float,
        default=0,
    )

    subjects_offered: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    passed_subjects: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    failed_subjects: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    position: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    principal_comment: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    batch = relationship(
        "ResultBatch",
        back_populates="summaries",
    )

    student = relationship("User")

    __table_args__ = (
        UniqueConstraint(
            "batch_id",
            "student_id",
            name="uq_result_summary",
        ),
    )

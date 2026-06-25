from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import (
    Base,
    TenantMixin,
    TimestampMixin,
    UUIDMixin,
)


class ResultApproval(
    Base,
    UUIDMixin,
    TenantMixin,
    TimestampMixin,
):
    __tablename__ = "result_approvals"

    batch_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "result_batches.id",
            ondelete="CASCADE",
        ),
        index=True,
    )

    action_by: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"),
    )

    action: Mapped[str] = mapped_column()
    # SUBMITTED
    # APPROVED
    # REJECTED
    # PUBLISHED

    note: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    action_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
    )

    batch = relationship(
        "ResultBatch",
        back_populates="approvals",
    )

    actor = relationship("User")

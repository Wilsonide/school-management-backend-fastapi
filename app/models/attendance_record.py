from enum import Enum
from uuid import UUID

from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, Index, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import (
    Base,
    TenantMixin,
    TimestampMixin,
    UUIDMixin,
)


class AttendanceStatus(str, Enum):
    PRESENT = "PRESENT"
    ABSENT = "ABSENT"
    LATE = "LATE"


class AttendanceRecord(
    Base,
    UUIDMixin,
    TenantMixin,
    TimestampMixin,
):
    __tablename__ = "attendance_records"

    sheet_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "attendance_sheets.id",
            ondelete="CASCADE",
        ),
        index=True,
    )

    student_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"),
        index=True,
    )

    status: Mapped[AttendanceStatus] = mapped_column(
        SQLEnum(AttendanceStatus),
    )

    note: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    sheet = relationship(
        "AttendanceSheet",
        back_populates="records",
    )

    student = relationship(
        "User",
        back_populates="attendance_records",
    )

    __table_args__ = (
        Index(
            "ix_attendance_student_sheet",
            "student_id",
            "sheet_id",
        ),
    )

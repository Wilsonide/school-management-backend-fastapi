from sqlalchemy import (
    UUID,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import mapped_column, relationship

from app.db.base import (
    Base,
    TimestampMixin,
    UUIDMixin,
)


class ClassSubject(
    Base,
    UUIDMixin,
    TimestampMixin,
):
    __tablename__ = "class_subjects"

    class_id = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("classes.id", ondelete="CASCADE"),
        index=True,
    )

    subject_id = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("subjects.id", ondelete="CASCADE"),
        index=True,
    )

    __table_args__ = (
        UniqueConstraint(
            "class_id",
            "subject_id",
            name="uq_class_subject",
        ),
    )

    
    school_class = relationship(
        "Class",
        back_populates="class_subjects",
    )

    subject = relationship(
        "Subject",
        back_populates="class_subjects",
    )

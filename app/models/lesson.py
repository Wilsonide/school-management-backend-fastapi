from sqlalchemy import (
    UUID,
    Column,
    ForeignKey,
    String,
    Text,
    Boolean,
)

from sqlalchemy.orm import relationship

from app.db.base import (
    Base,
    UUIDMixin,
    TimestampMixin,
)


class Lesson(
    Base,
    UUIDMixin,
    TimestampMixin,
):
    __tablename__ = "lessons"

    # LERNA ADMIN
    created_by = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
    )

    class_id = Column(
        UUID(as_uuid=True),
        ForeignKey("classes.id"),
        nullable=False,
    )

    subject_id = Column(
        UUID(as_uuid=True),
        ForeignKey("subjects.id"),
        nullable=False,
    )

    session_id = Column(
        UUID(as_uuid=True),
        ForeignKey("academic_sessions.id"),
        nullable=False,
    )

    term_id = Column(
        UUID(as_uuid=True),
        ForeignKey("terms.id"),
        nullable=False,
    )

    title = Column(String, nullable=False)

    topic = Column(String, nullable=False)

    objectives = Column(Text)

    file_url = Column(Text)

    is_published = Column(
        Boolean,
        default=True,
    )

    class_obj = relationship("Class")
    subject = relationship("Subject")
    session = relationship("AcademicSession")
    term = relationship("Term")

    created_by_user = relationship("User")

    
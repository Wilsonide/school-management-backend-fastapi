from sqlalchemy import UUID, Column, ForeignKey

from app.db.base import Base, TimestampMixin, UUIDMixin


class ClassSubject(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "class_subjects"

    class_id = Column(UUID(as_uuid=True), ForeignKey("classes.id"))
    subject_id = Column(UUID(as_uuid=True), ForeignKey("subjects.id"))

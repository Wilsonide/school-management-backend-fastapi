from sqlalchemy import UUID, Column, ForeignKey

from app.db.base import Base, TimestampMixin, UUIDMixin


class TeacherClass(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "teacher_classes"

    teacher_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    class_id = Column(UUID(as_uuid=True), ForeignKey("classes.id"))

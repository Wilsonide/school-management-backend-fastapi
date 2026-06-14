from sqlalchemy import UUID, Column, ForeignKey, String, Time
from sqlalchemy.orm import relationship

from app.db.base import Base, TenantMixin, TimestampMixin, UUIDMixin


class Timetable(Base, TenantMixin, UUIDMixin, TimestampMixin):
    __tablename__ = "timetables"

    class_id = Column(UUID(as_uuid=True), ForeignKey("classes.id"))

    subject_id = Column(UUID(as_uuid=True), ForeignKey("subjects.id"))

    teacher_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    day_of_week = Column(String)  # Monday, Tuesday...

    start_time = Column(Time)
    end_time = Column(Time)
    subject = relationship("Subject")
    teacher = relationship("User")

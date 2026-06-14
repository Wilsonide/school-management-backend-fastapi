from sqlalchemy import UUID, ForeignKey, String
from sqlalchemy.orm import mapped_column

from app.db.base import Base, TenantMixin, UUIDMixin


class CourseMaterial(Base, UUIDMixin):
    __tablename__ = "course_materials"

    teacher_id = mapped_column(UUID, ForeignKey("teacher_profiles.id"))

    subject_id = mapped_column(UUID, ForeignKey("subjects.id"))

    title = mapped_column(String)

    file_url = mapped_column(String)

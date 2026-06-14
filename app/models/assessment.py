from sqlalchemy import UUID, ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column

from app.db.base import Base, UUIDMixin


class Assessment(Base, UUIDMixin):
    __tablename__ = "assessments"

    subject_id = mapped_column(UUID, ForeignKey("subjects.id"))

    term_id = mapped_column(UUID, ForeignKey("terms.id"))

    title = mapped_column(String)

    total_score = mapped_column(Integer)

from sqlalchemy import UUID, ForeignKey, String, Text
from sqlalchemy.orm import mapped_column

from app.db.base import Base, UUIDMixin


class Announcement(Base, UUIDMixin):
    __tablename__ = "announcements"

    title = mapped_column(String)

    content = mapped_column(Text)

    created_by = mapped_column(UUID, ForeignKey("users.id"))

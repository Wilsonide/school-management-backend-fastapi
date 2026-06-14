from sqlalchemy import String
from sqlalchemy.orm import mapped_column

from app.db.base import Base, TenantMixin, TimestampMixin, UUIDMixin


class Class(Base, UUIDMixin, TenantMixin, TimestampMixin):
    __tablename__ = "classes"

    name = mapped_column(String)

    level = mapped_column(String)

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TenantMixin, UUIDMixin


class Subject(Base, UUIDMixin, TenantMixin):
    __tablename__ = "subjects"

    name: Mapped[str] = mapped_column(String(255))
    code: Mapped[str] = mapped_column(String(50), nullable=True)

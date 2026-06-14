from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TenantMixin, UUIDMixin


class ParentProfile(Base, UUIDMixin, TenantMixin):
    __tablename__ = "parent_profiles"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        index=True,
    )

    occupation: Mapped[str] = mapped_column(String, nullable=True)

    phone: Mapped[str] = mapped_column(String, nullable=True)

    user = relationship("User", back_populates="parent_profile")
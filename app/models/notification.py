from sqlalchemy import Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TenantMixin, UUIDMixin


class Notification(Base, UUIDMixin, TenantMixin):
    __tablename__ = "notifications"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    title: Mapped[str]
    message: Mapped[str]

    is_read: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

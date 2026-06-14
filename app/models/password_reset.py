import uuid
from datetime import datetime, timedelta

from sqlalchemy import String, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import UUIDMixin,Base


class PasswordResetToken(Base,UUIDMixin):
    __tablename__ = "password_reset_tokens"



    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    token: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    used: Mapped[bool] = mapped_column(Boolean, default=False)
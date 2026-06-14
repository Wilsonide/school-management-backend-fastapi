from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, UUIDMixin


class Invite(Base, UUIDMixin):
    __tablename__ = "invites"

    email: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(50))

    school_id = mapped_column(ForeignKey("schools.id"))

    code: Mapped[str] = mapped_column(String(100), unique=True, index=True)

    is_used: Mapped[bool] = mapped_column(Boolean, default=False)

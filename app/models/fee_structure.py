from sqlalchemy import UUID, ForeignKey, Numeric, String
from sqlalchemy.orm import mapped_column

from app.db.base import Base, TenantMixin, UUIDMixin


class FeeStructure(Base, UUIDMixin, TenantMixin):
    __tablename__ = "fee_structures"

    class_id = mapped_column(UUID, ForeignKey("classes.id"))

    name = mapped_column(String)

    amount = mapped_column(Numeric)

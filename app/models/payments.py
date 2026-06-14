from sqlalchemy import UUID, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import mapped_column

from app.db.base import Base, UUIDMixin


class Payment(Base, UUIDMixin):
    __tablename__ = "payments"

    student_id = mapped_column(UUID, ForeignKey("student_profiles.id"))

    fee_id = mapped_column(UUID, ForeignKey("fee_structures.id"))

    amount_paid = mapped_column(Numeric)

    payment_date = mapped_column(DateTime)

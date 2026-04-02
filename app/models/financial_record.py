from sqlalchemy import (
    Column, Integer, String, Numeric, Enum, Date,
    DateTime, Text, ForeignKey, Boolean, Index
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.database import Base


class RecordType(str, enum.Enum):
    income = "income"
    expense = "expense"


class FinancialRecord(Base):
    __tablename__ = "financial_records"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Numeric(precision=15, scale=2), nullable=False)
    type = Column(Enum(RecordType), nullable=False)
    category = Column(String(100), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    notes = Column(Text, nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)  # soft delete
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    creator = relationship("User", back_populates="financial_records", foreign_keys=[created_by])

    __table_args__ = (
        # Composite index for common dashboard queries
        Index("ix_records_type_date", "type", "date", "is_deleted"),
        Index("ix_records_category_date", "category", "date", "is_deleted"),
    )

    def __repr__(self) -> str:
        return f"<FinancialRecord id={self.id} type={self.type} amount={self.amount}>"

from sqlalchemy import Column, Integer, String, Enum, DateTime, Boolean, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.database import Base


class UserRole(str, enum.Enum):
    viewer = "viewer"
    analyst = "analyst"
    admin = "admin"


class UserStatus(str, enum.Enum):
    active = "active"
    inactive = "inactive"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.viewer)
    status = Column(Enum(UserStatus), nullable=False, default=UserStatus.active)
    is_deleted = Column(Boolean, default=False, nullable=False)  # soft delete
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    financial_records = relationship(
        "FinancialRecord",
        back_populates="creator",
        foreign_keys="FinancialRecord.created_by",
    )

    __table_args__ = (
        Index("ix_users_email_active", "email", "is_deleted"),
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email} role={self.role}>"

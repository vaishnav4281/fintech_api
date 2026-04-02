from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime
from app.models.user import UserRole, UserStatus


# ── Request schemas ──────────────────────────────────────────────────────────

class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, examples=["Alice Johnson"])
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128, examples=["Str0ngP@ss!"])
    role: UserRole = UserRole.viewer

    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("name must not be blank")
        return v.strip()


<<<<<<< HEAD
=======
class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)


>>>>>>> fb8f58e (Initialize project with full API features and documentation)
class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    password: Optional[str] = Field(None, min_length=8, max_length=128)

    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("name must not be blank")
        return v.strip() if v else v


class UserStatusUpdate(BaseModel):
    status: UserStatus


# ── Response schemas ─────────────────────────────────────────────────────────

class UserResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    name: str
    email: str
    role: UserRole
    status: UserStatus
    created_at: datetime


class UserListResponse(BaseModel):
    total: int
    page: int
    limit: int
    items: list[UserResponse]

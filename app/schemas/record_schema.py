from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date, datetime
from decimal import Decimal
from app.models.financial_record import RecordType


# ── Request schemas ──────────────────────────────────────────────────────────

class RecordCreate(BaseModel):
    amount: Decimal = Field(..., gt=0, decimal_places=2, examples=[1500.00])
    type: RecordType
    category: str = Field(..., min_length=1, max_length=100, examples=["Salary"])
    date: date
    notes: Optional[str] = Field(None, max_length=1000)

    @field_validator("category")
    @classmethod
    def category_must_not_be_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("category must not be blank")
        return v.strip()

    @field_validator("amount")
    @classmethod
    def amount_must_be_positive(cls, v: Decimal) -> Decimal:
        if v <= 0:
            raise ValueError("amount must be a positive number")
        return v


class RecordUpdate(BaseModel):
    amount: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    type: Optional[RecordType] = None
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    date: Optional[date] = None
    notes: Optional[str] = Field(None, max_length=1000)

    @field_validator("category")
    @classmethod
    def category_must_not_be_blank(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("category must not be blank")
        return v.strip() if v else v


# ── Response schemas ─────────────────────────────────────────────────────────

class RecordResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    amount: Decimal
    type: RecordType
    category: str
    date: date
    notes: Optional[str]
    created_by: int
    created_at: datetime


class RecordListResponse(BaseModel):
    total: int
    page: int
    limit: int
    items: list[RecordResponse]


# ── Dashboard schemas ────────────────────────────────────────────────────────

class DashboardSummary(BaseModel):
    total_income: Decimal
    total_expenses: Decimal
    net_balance: Decimal


class CategorySummaryItem(BaseModel):
    category: str
    type: RecordType
    total: Decimal
    count: int


class MonthlySummaryItem(BaseModel):
    year: int
    month: int
    total_income: Decimal
    total_expenses: Decimal
    net_balance: Decimal

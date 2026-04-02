from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.record_schema import (
    DashboardSummary, CategorySummaryItem, RecordResponse, MonthlySummaryItem,
)
from app.services import dashboard_service
from app.auth.permissions import require_dashboard_access

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get(
    "/summary",
    response_model=DashboardSummary,
    summary="Total income, expenses, and net balance (all roles)",
)
def get_summary(
    db: Session = Depends(get_db),
    _: User = Depends(require_dashboard_access),
):
    return dashboard_service.get_summary(db)


@router.get(
    "/category-summary",
    response_model=list[CategorySummaryItem],
    summary="Totals grouped by category and type (all roles)",
)
def get_category_summary(
    db: Session = Depends(get_db),
    _: User = Depends(require_dashboard_access),
):
    return dashboard_service.get_category_summary(db)


@router.get(
    "/recent",
    response_model=list[RecordResponse],
    summary="10 most recent financial records (all roles)",
)
def get_recent(
    db: Session = Depends(get_db),
    _: User = Depends(require_dashboard_access),
):
    return dashboard_service.get_recent_records(db)


@router.get(
    "/monthly-trends",
    response_model=list[MonthlySummaryItem],
    summary="Income and expenses aggregated by month (all roles)",
)
def get_monthly_trends(
    db: Session = Depends(get_db),
    _: User = Depends(require_dashboard_access),
):
    return dashboard_service.get_monthly_trends(db)

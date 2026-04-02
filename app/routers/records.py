from typing import Optional
from datetime import date
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.financial_record import RecordType
from app.schemas.record_schema import (
    RecordCreate, RecordUpdate, RecordResponse, RecordListResponse,
)
from app.services import record_service
from app.auth.jwt_handler import get_current_user
from app.auth.permissions import require_analyst_or_above, require_admin

router = APIRouter(prefix="/records", tags=["Financial Records"])


@router.post(
    "",
    response_model=RecordResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a financial record (admin only)",
)
def create_record(
    payload: RecordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return record_service.create_record(db, payload, current_user)


@router.get(
    "",
    response_model=RecordListResponse,
    summary="List records with filters and pagination (analyst/admin)",
)
def list_records(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    type: Optional[RecordType] = Query(None, description="Filter by income or expense"),
    category: Optional[str] = Query(None, description="Filter by category (partial match)"),
    start_date: Optional[date] = Query(None, description="Records on or after this date (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="Records on or before this date (YYYY-MM-DD)"),
    search: Optional[str] = Query(None, description="Search notes and category"),
    db: Session = Depends(get_db),
    _: User = Depends(require_analyst_or_above),
):
    return record_service.list_records(
        db,
        page=page,
        limit=limit,
        type=type,
        category=category,
        start_date=start_date,
        end_date=end_date,
        search=search,
    )


@router.get(
    "/{record_id}",
    response_model=RecordResponse,
    summary="Get a single record by ID (analyst/admin)",
)
def get_record(
    record_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_analyst_or_above),
):
    return record_service.get_record_by_id(db, record_id)


@router.put(
    "/{record_id}",
    response_model=RecordResponse,
    summary="Update a record (admin only)",
)
def update_record(
    record_id: int,
    payload: RecordUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    return record_service.update_record(db, record_id, payload)


@router.delete(
    "/{record_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Soft-delete a record (admin only)",
)
def delete_record(
    record_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    record_service.delete_record(db, record_id)

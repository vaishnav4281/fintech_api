from typing import Optional
from datetime import date
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.financial_record import FinancialRecord, RecordType
from app.models.user import User
from app.schemas.record_schema import RecordCreate, RecordUpdate


def create_record(db: Session, payload: RecordCreate, current_user: User) -> FinancialRecord:
    record = FinancialRecord(
        amount=payload.amount,
        type=payload.type,
        category=payload.category,
        date=payload.date,
        notes=payload.notes,
        created_by=current_user.id,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_record_by_id(db: Session, record_id: int) -> FinancialRecord:
    record = db.query(FinancialRecord).filter(
        FinancialRecord.id == record_id,
        FinancialRecord.is_deleted == False,  # noqa: E712
    ).first()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found.")
    return record


def list_records(
    db: Session,
    page: int = 1,
    limit: int = 10,
    type: Optional[RecordType] = None,
    category: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    search: Optional[str] = None,
) -> dict:
    query = db.query(FinancialRecord).filter(FinancialRecord.is_deleted == False)  # noqa: E712

    if type:
        query = query.filter(FinancialRecord.type == type)
    if category:
        query = query.filter(FinancialRecord.category.ilike(f"%{category}%"))
    if start_date:
        query = query.filter(FinancialRecord.date >= start_date)
    if end_date:
        query = query.filter(FinancialRecord.date <= end_date)
    if search:
        # Full-text search over notes and category
        query = query.filter(
            FinancialRecord.notes.ilike(f"%{search}%")
            | FinancialRecord.category.ilike(f"%{search}%")
        )

    total = query.count()
    items = (
        query.order_by(FinancialRecord.date.desc(), FinancialRecord.created_at.desc())
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )
    return {"total": total, "page": page, "limit": limit, "items": items}


def update_record(db: Session, record_id: int, payload: RecordUpdate) -> FinancialRecord:
    record = get_record_by_id(db, record_id)

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(record, field, value)

    db.commit()
    db.refresh(record)
    return record


def delete_record(db: Session, record_id: int) -> None:
    """Soft-delete: marks is_deleted=True."""
    record = get_record_by_id(db, record_id)
    record.is_deleted = True
    db.commit()

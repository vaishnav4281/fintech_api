from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import func, extract, case

from app.models.financial_record import FinancialRecord, RecordType


def _base_query(db: Session):
    """Return a query scoped to non-deleted records."""
    return db.query(FinancialRecord).filter(FinancialRecord.is_deleted == False)  # noqa: E712


def get_summary(db: Session) -> dict:
    """Return total income, total expenses, and net balance."""
    result = db.query(
        func.coalesce(
            func.sum(
                case((FinancialRecord.type == RecordType.income, FinancialRecord.amount), else_=0)
            ),
            Decimal("0.00"),
        ).label("total_income"),
        func.coalesce(
            func.sum(
                case((FinancialRecord.type == RecordType.expense, FinancialRecord.amount), else_=0)
            ),
            Decimal("0.00"),
        ).label("total_expenses"),
    ).filter(FinancialRecord.is_deleted == False).one()  # noqa: E712

    total_income = result.total_income or Decimal("0.00")
    total_expenses = result.total_expenses or Decimal("0.00")

    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "net_balance": total_income - total_expenses,
    }


def get_category_summary(db: Session) -> list[dict]:
    """Return totals grouped by category and record type."""
    rows = (
        db.query(
            FinancialRecord.category,
            FinancialRecord.type,
            func.sum(FinancialRecord.amount).label("total"),
            func.count(FinancialRecord.id).label("count"),
        )
        .filter(FinancialRecord.is_deleted == False)  # noqa: E712
        .group_by(FinancialRecord.category, FinancialRecord.type)
        .order_by(FinancialRecord.type, func.sum(FinancialRecord.amount).desc())
        .all()
    )

    return [
        {
            "category": row.category,
            "type": row.type,
            "total": row.total,
            "count": row.count,
        }
        for row in rows
    ]


def get_recent_records(db: Session, limit: int = 10) -> list[FinancialRecord]:
    """Return the N most recent financial records."""
    return (
        _base_query(db)
        .order_by(FinancialRecord.date.desc(), FinancialRecord.created_at.desc())
        .limit(limit)
        .all()
    )


def get_monthly_trends(db: Session) -> list[dict]:
    """
    Return income and expense totals grouped by year-month.
    Uses a single-pass aggregation via conditional SUMs.
    """
    rows = (
        db.query(
            extract("year", FinancialRecord.date).label("year"),
            extract("month", FinancialRecord.date).label("month"),
            func.coalesce(
                func.sum(
                    case(
                        (FinancialRecord.type == RecordType.income, FinancialRecord.amount),
                        else_=0,
                    )
                ),
                Decimal("0.00"),
            ).label("total_income"),
            func.coalesce(
                func.sum(
                    case(
                        (FinancialRecord.type == RecordType.expense, FinancialRecord.amount),
                        else_=0,
                    )
                ),
                Decimal("0.00"),
            ).label("total_expenses"),
        )
        .filter(FinancialRecord.is_deleted == False)  # noqa: E712
        .group_by("year", "month")
        .order_by("year", "month")
        .all()
    )

    return [
        {
            "year": int(row.year),
            "month": int(row.month),
            "total_income": row.total_income or Decimal("0.00"),
            "total_expenses": row.total_expenses or Decimal("0.00"),
            "net_balance": (row.total_income or Decimal("0.00")) - (row.total_expenses or Decimal("0.00")),
        }
        for row in rows
    ]

#!/usr/bin/env python3
"""
Seed the database with an admin user and sample financial records.

Usage:
    python scripts/seed_db.py
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from datetime import date, timedelta
from decimal import Decimal
import random

from app.database import SessionLocal, engine
from app.database import Base
from app.models.user import User, UserRole, UserStatus
from app.models.financial_record import FinancialRecord, RecordType
from app.services.user_service import hash_password

Base.metadata.create_all(bind=engine)

INCOME_CATEGORIES = ["Salary", "Freelance", "Investments", "Rental Income", "Bonus"]
EXPENSE_CATEGORIES = ["Rent", "Groceries", "Utilities", "Transport", "Healthcare", "Entertainment", "Insurance"]


def seed():
    db = SessionLocal()
    try:
        # ── Users ─────────────────────────────────────────────────────────────
        existing = db.query(User).count()
        if existing > 0:
            print("Database already seeded. Skipping.")
            return

        users_data = [
            dict(name="Alice Admin",    email="admin@example.com",    role=UserRole.admin,    password="Admin1234!"),
            dict(name="Bob Analyst",    email="analyst@example.com",  role=UserRole.analyst,  password="Analyst1234!"),
            dict(name="Carol Viewer",   email="viewer@example.com",   role=UserRole.viewer,   password="Viewer1234!"),
        ]

        users = []
        for u in users_data:
            user = User(
                name=u["name"],
                email=u["email"],
                password_hash=hash_password(u["password"]),
                role=u["role"],
                status=UserStatus.active,
            )
            db.add(user)
            users.append(user)

        db.commit()
        for u in users:
            db.refresh(u)

        admin = users[0]

        # ── Financial Records (12 months of data) ─────────────────────────────
        today = date.today()
        records_created = 0

        for month_offset in range(12):
            record_date = date(today.year if today.month > month_offset else today.year - 1,
                               ((today.month - month_offset - 1) % 12) + 1, 1)

            # Monthly salary income
            db.add(FinancialRecord(
                amount=Decimal("5000.00"),
                type=RecordType.income,
                category="Salary",
                date=record_date.replace(day=1),
                notes="Monthly salary payment",
                created_by=admin.id,
            ))
            records_created += 1

            # Monthly rent expense
            db.add(FinancialRecord(
                amount=Decimal("1500.00"),
                type=RecordType.expense,
                category="Rent",
                date=record_date.replace(day=3),
                notes="Monthly rent",
                created_by=admin.id,
            ))
            records_created += 1

            # Random additional records
            for _ in range(random.randint(4, 8)):
                is_income = random.random() < 0.3
                category = random.choice(INCOME_CATEGORIES if is_income else EXPENSE_CATEGORIES)
                amount = Decimal(str(round(random.uniform(50, 800), 2)))
                day = random.randint(1, 28)
                db.add(FinancialRecord(
                    amount=amount,
                    type=RecordType.income if is_income else RecordType.expense,
                    category=category,
                    date=record_date.replace(day=day),
                    notes=f"Auto-generated {category.lower()} record",
                    created_by=admin.id,
                ))
                records_created += 1

        db.commit()

        print("✅ Seed complete.")
        print(f"   Users created : {len(users)}")
        print(f"   Records created: {records_created}")
        print()
        print("Login credentials:")
        for u in users_data:
            print(f"  {u['role'].value:8s}  {u['email']}  /  {u['password']}")

    finally:
        db.close()


if __name__ == "__main__":
    seed()

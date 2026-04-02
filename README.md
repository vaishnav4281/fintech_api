# Finance Dashboard API

A production-grade REST backend for a **Finance Dashboard System** — built with FastAPI, PostgreSQL, SQLAlchemy, and JWT authentication.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Role & Permission Matrix](#role--permission-matrix)
- [Getting Started](#getting-started)
  - [1. Prerequisites](#1-prerequisites)
  - [2. PostgreSQL Setup](#2-postgresql-setup)
  - [3. Configure Environment](#3-configure-environment)
  - [4. Install Dependencies](#4-install-dependencies)
  - [5. Run Migrations](#5-run-migrations)
  - [6. Seed Sample Data](#6-seed-sample-data)
  - [7. Start the Server](#7-start-the-server)
- [API Reference](#api-reference)
  - [Authentication](#authentication)
  - [Users](#users)
  - [Financial Records](#financial-records)
  - [Dashboard](#dashboard)
  - [Health](#health)
- [Data Models](#data-models)
- [Validation Rules](#validation-rules)
- [Error Responses](#error-responses)
- [Running Tests](#running-tests)
- [Design Decisions & Assumptions](#design-decisions--assumptions)

---

## Overview

This backend powers a multi-role finance dashboard where:

- **Admins** manage users and financial records (full CRUD).
- **Analysts** read records and explore dashboard analytics.
- **Viewers** access high-level dashboard summaries only.

The system emphasises clear separation of concerns, strict role-based access control, aggregated analytics queries, soft-delete semantics, and full input validation.

---

## Architecture

```
HTTP Request
    │
    ▼
FastAPI Router          ← validates request shape, enforces auth/role via Depends()
    │
    ▼
Service Layer           ← business logic, raises HTTPException on rule violations
    │
    ▼
SQLAlchemy ORM          ← typed models, relationships, indexes
    │
    ▼
PostgreSQL
```

Each layer has a single responsibility:

| Layer       | Location               | Responsibility                              |
|-------------|------------------------|---------------------------------------------|
| **Routers** | `app/routers/`         | HTTP surface, request/response binding      |
| **Services**| `app/services/`        | Business rules, validation, DB coordination |
| **Models**  | `app/models/`          | SQLAlchemy ORM definitions                  |
| **Schemas** | `app/schemas/`         | Pydantic request/response contracts         |
| **Auth**    | `app/auth/`            | JWT issuing/verification, RBAC dependencies |

---

## Tech Stack

| Concern          | Technology                        |
|------------------|-----------------------------------|
| Framework        | FastAPI 0.111                     |
| Database         | PostgreSQL 14+                    |
| ORM              | SQLAlchemy 2.0                    |
| Schema / Validation | Pydantic v2                    |
| Migrations       | Alembic                           |
| Auth             | JWT (python-jose), bcrypt (passlib) |
| Testing          | pytest + httpx TestClient         |
| Server           | Uvicorn                           |

---

## Project Structure

```
finance-dashboard/
├── app/
│   ├── main.py                  # App factory, middleware, exception handlers
│   ├── config.py                # Pydantic-settings config (reads .env)
│   ├── database.py              # SQLAlchemy engine, session, Base
│   ├── models/
│   │   ├── user.py              # User model (roles, status, soft-delete)
│   │   └── financial_record.py  # FinancialRecord model
│   ├── schemas/
│   │   ├── user_schema.py       # UserCreate / UserUpdate / UserResponse
│   │   └── record_schema.py     # RecordCreate / RecordUpdate / Dashboard schemas
│   ├── routers/
│   │   ├── auth.py              # POST /auth/login
│   │   ├── users.py             # CRUD /users
│   │   ├── records.py           # CRUD /records (with filters)
│   │   └── dashboard.py         # GET /dashboard/*
│   ├── services/
│   │   ├── user_service.py      # User CRUD + authentication helper
│   │   ├── record_service.py    # Record CRUD + filtering
│   │   └── dashboard_service.py # Aggregation queries (SQLAlchemy)
│   └── auth/
│       ├── jwt_handler.py       # Token creation, decoding, get_current_user
│       └── permissions.py       # Role-guard dependency factories
├── alembic/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│       └── 001_initial_schema.py
├── scripts/
│   └── seed_db.py               # Seed admin + 12 months of sample data
├── tests/
│   ├── conftest.py              # SQLite in-memory fixtures, shared helpers
│   ├── test_auth.py
│   ├── test_users.py
│   ├── test_records.py
│   └── test_dashboard.py
├── alembic.ini
├── pytest.ini
├── requirements.txt
└── .env.example
```

---

## Role & Permission Matrix

| Endpoint group          | viewer | analyst | admin |
|-------------------------|:------:|:-------:|:-----:|
| `POST /auth/login`      | ✅     | ✅      | ✅    |
| `GET /users/me`         | ✅     | ✅      | ✅    |
| `POST /users`           | ❌     | ❌      | ✅    |
| `GET /users`            | ❌     | ❌      | ✅    |
| `GET /users/{id}`       | ❌     | ❌      | ✅    |
| `PUT /users/{id}`       | ❌     | ❌      | ✅    |
| `PATCH /users/{id}/status` | ❌  | ❌      | ✅    |
| `DELETE /users/{id}`    | ❌     | ❌      | ✅    |
| `POST /records`         | ❌     | ❌      | ✅    |
| `GET /records`          | ❌     | ✅      | ✅    |
| `GET /records/{id}`     | ❌     | ✅      | ✅    |
| `PUT /records/{id}`     | ❌     | ❌      | ✅    |
| `DELETE /records/{id}`  | ❌     | ❌      | ✅    |
| `GET /dashboard/*`      | ✅     | ✅      | ✅    |

Unauthorized attempts return `HTTP 403 Forbidden`.

---

## Getting Started

### 1. Prerequisites

- Python 3.11+
- PostgreSQL 14+
- pip / virtualenv

### 2. PostgreSQL Setup

```sql
-- Connect as a superuser and run:
CREATE DATABASE finance_dashboard;
CREATE USER finance_user WITH ENCRYPTED PASSWORD 'yourpassword';
GRANT ALL PRIVILEGES ON DATABASE finance_dashboard TO finance_user;
```

### 3. Configure Environment

```bash
cp .env.example .env
```

Edit `.env`:

```env
DATABASE_URL=postgresql://finance_user:yourpassword@localhost:5432/finance_dashboard
SECRET_KEY=replace-with-a-random-32-char-string
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
APP_ENV=development
```

Generate a strong secret key:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 4. Install Dependencies

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 5. Run Migrations

```bash
alembic upgrade head
```

To generate a new migration after model changes:
```bash
alembic revision --autogenerate -m "describe change"
alembic upgrade head
```

### 6. Seed Sample Data

```bash
python scripts/seed_db.py
```

This creates three users and ~12 months of financial records:

| Role    | Email                  | Password      |
|---------|------------------------|---------------|
| admin   | admin@example.com      | Admin1234!    |
| analyst | analyst@example.com    | Analyst1234!  |
| viewer  | viewer@example.com     | Viewer1234!   |

### 7. Start the Server

```bash
uvicorn app.main:app --reload
```

- API: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## API Reference

### Authentication

#### `POST /auth/login`

Obtain a JWT Bearer token.

**Request** (form-data):
```
username=admin@example.com
password=Admin1234!
```

**Response `200`:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "role": "admin"
}
```

All subsequent requests require:
```
Authorization: Bearer <access_token>
```

---

### Users

#### `POST /users` — Create user _(admin)_

```json
{
  "name": "Jane Smith",
  "email": "jane@example.com",
  "password": "Secure1234!",
  "role": "analyst"
}
```

#### `GET /users` — List users _(admin)_

Query params: `page`, `limit`, `role`, `status`

```
GET /users?page=1&limit=20&role=analyst&status=active
```

#### `GET /users/me` — Own profile _(all roles)_

#### `GET /users/{id}` — Get user _(admin)_

#### `PUT /users/{id}` — Update user _(admin)_

```json
{
  "name": "Updated Name",
  "role": "admin"
}
```

#### `PATCH /users/{id}/status` — Change status _(admin)_

```json
{ "status": "inactive" }
```

#### `DELETE /users/{id}` — Soft-delete user _(admin)_ → `204`

---

### Financial Records

#### `POST /records` — Create record _(admin)_

```json
{
  "amount": 3500.00,
  "type": "income",
  "category": "Freelance",
  "date": "2024-03-20",
  "notes": "Website project payment"
}
```

#### `GET /records` — List records _(analyst, admin)_

| Parameter    | Type   | Description                              |
|--------------|--------|------------------------------------------|
| `page`       | int    | Page number (default: 1)                 |
| `limit`      | int    | Items per page (default: 10, max: 100)   |
| `type`       | string | `income` or `expense`                    |
| `category`   | string | Partial match on category name           |
| `start_date` | date   | Records on or after `YYYY-MM-DD`         |
| `end_date`   | date   | Records on or before `YYYY-MM-DD`        |
| `search`     | string | Full-text search across category + notes |

```
GET /records?type=expense&category=rent&start_date=2024-01-01&page=1&limit=10
```

**Response:**
```json
{
  "total": 42,
  "page": 1,
  "limit": 10,
  "items": [...]
}
```

#### `GET /records/{id}` — Get record _(analyst, admin)_

#### `PUT /records/{id}` — Update record _(admin)_

```json
{
  "amount": 4000.00,
  "notes": "Revised invoice amount"
}
```

#### `DELETE /records/{id}` — Soft-delete record _(admin)_ → `204`

---

### Dashboard

All dashboard endpoints are accessible by **all authenticated roles**.

#### `GET /dashboard/summary`

```json
{
  "total_income": "62500.00",
  "total_expenses": "28340.50",
  "net_balance": "34159.50"
}
```

#### `GET /dashboard/category-summary`

```json
[
  { "category": "Salary",    "type": "income",  "total": "60000.00", "count": 12 },
  { "category": "Rent",      "type": "expense", "total": "18000.00", "count": 12 },
  { "category": "Freelance", "type": "income",  "total": "2500.00",  "count": 3  }
]
```

#### `GET /dashboard/recent`

Returns the 10 most recent records ordered by date descending.

#### `GET /dashboard/monthly-trends`

```json
[
  {
    "year": 2024,
    "month": 1,
    "total_income": "5800.00",
    "total_expenses": "2100.00",
    "net_balance": "3700.00"
  },
  ...
]
```

---

### Health

#### `GET /health`

```json
{
  "status": "ok",
  "version": "1.0.0",
  "environment": "development"
}
```

---

## Data Models

### User

| Column          | Type        | Constraints                          |
|-----------------|-------------|--------------------------------------|
| `id`            | integer     | PK, auto-increment                   |
| `name`          | varchar(100)| not null                             |
| `email`         | varchar(255)| unique, indexed, not null            |
| `password_hash` | varchar(255)| bcrypt hash, not null                |
| `role`          | enum        | `viewer`, `analyst`, `admin`         |
| `status`        | enum        | `active`, `inactive`                 |
| `is_deleted`    | boolean     | soft-delete flag, default `false`    |
| `created_at`    | timestamptz | server default `now()`               |
| `updated_at`    | timestamptz | auto-updated on change               |

### FinancialRecord

| Column       | Type           | Constraints                          |
|--------------|----------------|--------------------------------------|
| `id`         | integer        | PK, auto-increment                   |
| `amount`     | numeric(15, 2) | positive, not null                   |
| `type`       | enum           | `income`, `expense`                  |
| `category`   | varchar(100)   | indexed, not null                    |
| `date`       | date           | indexed, not null                    |
| `notes`      | text           | optional                             |
| `created_by` | integer        | FK → users.id                        |
| `is_deleted` | boolean        | soft-delete flag, default `false`    |
| `created_at` | timestamptz    | server default `now()`               |
| `updated_at` | timestamptz    | auto-updated on change               |

---

## Validation Rules

| Field      | Rule                                          |
|------------|-----------------------------------------------|
| `amount`   | Must be a positive decimal (`> 0`)            |
| `type`     | Must be `income` or `expense`                 |
| `category` | Required, non-blank, max 100 chars            |
| `date`     | Required, ISO 8601 format (`YYYY-MM-DD`)      |
| `email`    | Valid email format, unique per active user    |
| `password` | Minimum 8 characters, maximum 128 characters |
| `role`     | Must be `viewer`, `analyst`, or `admin`       |

Invalid requests return `HTTP 422 Unprocessable Entity` with field-level error details:

```json
{
  "detail": "Validation failed",
  "errors": [
    {
      "field": "amount",
      "message": "Input should be greater than 0",
      "type": "greater_than"
    }
  ]
}
```

---

## Error Responses

| HTTP Code | Meaning                                        |
|-----------|------------------------------------------------|
| `400`     | Bad request (malformed input)                  |
| `401`     | Missing or invalid JWT token                   |
| `403`     | Authenticated but insufficient role            |
| `404`     | Resource not found (or soft-deleted)           |
| `409`     | Conflict — e.g. duplicate email                |
| `422`     | Validation error with field details            |
| `500`     | Internal server error                          |

All error bodies follow:
```json
{ "detail": "Human-readable message" }
```

---

## Running Tests

Tests use an **in-memory SQLite database** — no PostgreSQL required.

```bash
# Install test dependencies (already in requirements.txt)
pip install -r requirements.txt

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run a specific test file
pytest tests/test_dashboard.py -v

# Run with coverage
pip install pytest-cov
pytest --cov=app --cov-report=term-missing
```

**Test coverage areas:**

| File                    | What it covers                                      |
|-------------------------|-----------------------------------------------------|
| `test_auth.py`          | Login success/failure, bad tokens, inactive users   |
| `test_users.py`         | CRUD, role guards, pagination, soft-delete, status  |
| `test_records.py`       | CRUD, all filters, pagination, validation, RBAC     |
| `test_dashboard.py`     | Summary maths, category grouping, monthly trends    |

---

## Design Decisions & Assumptions

**Soft delete over hard delete**
Both users and records are soft-deleted (`is_deleted = true`) rather than removed from the database. This preserves audit history and referential integrity — a deleted user's records remain queryable by admins if needed.

**Single migration file**
The initial migration captures the full schema. In a real team environment, each schema change would be a separate numbered migration.

**Decimal precision**
Amounts are stored as `NUMERIC(15, 2)` to avoid floating-point rounding errors. All monetary values are handled with Python's `Decimal` type end-to-end.

**Pydantic v2**
The codebase targets Pydantic v2 (`model_dump`, `model_config`, `field_validator`). Pydantic v1 compatibility is not maintained.

**`/users/me` endpoint**
Added as a convenience for any authenticated user to retrieve their own profile without requiring admin access. This is a common pattern in real-world APIs.

**Search**
The `search` query parameter on `GET /records` performs a case-insensitive `ILIKE` match on both `category` and `notes`. For production scale, this should be replaced with PostgreSQL full-text search (`tsvector`/`tsquery`) or an external search engine.

**CORS**
CORS is currently configured to allow all origins (`*`). In production, restrict `allow_origins` to your frontend's specific domain(s).

**Password policy**
Passwords require a minimum of 8 characters. More complex policies (uppercase, digit, special character enforcement) can be added via an extended `field_validator` in `UserCreate`.

# 📊 Finance Dashboard API

A production-grade, multi-role REST backend for a **Finance Dashboard System** — built with FastAPI, PostgreSQL/SQLite, SQLAlchemy 2.0, and JWT authentication.

---

## 🚀 Recent Updates & Fixes (Ver. 1.1)
- **Unified JSON Authentication**: Converted `/auth/login` to accept JSON bodies for consistency with the rest of the API.
- **Fixed Dependency Issues**: Pinning `bcrypt<4.0.0` to resolve `passlib` compatibility crashes.
- **Improved Documentation**: Added `endpoints.md` for Postman testing and `test.md` for a comprehensive examiner's guide.
- **SQLite Support**: Added full support for local SQLite development with cross-compatible migrations.

---

## 🛠️ Tech Stack & Architecture

| Feature | Technology |
| :--- | :--- |
| **Framework** | FastAPI (Python 3.12+) |
| **Database** | PostgreSQL (Production) / SQLite (Local Dev) |
| **ORM** | SQLAlchemy 2.0 |
| **Migrations** | Alembic |
| **Auth** | JWT (python-jose), bcrypt (passlib) |
| **Testing** | pytest + httpx |

---

## 📂 Project Structure

```text
finance-dashboard/
├── app/
│   ├── main.py                  # App initialization & global error handlers
│   ├── auth/                    # JWT handling & Role-Based Access Control (RBAC)
│   ├── models/                  # SQLAlchemy Database Models
│   ├── routers/                 # API Route Controllers (Auth, Records, Users, Dashboard)
│   ├── schemas/                 # Pydantic Request/Response Models
│   └── services/                # Business Logic Layer
├── alembic/                     # Database Migration Scripts
├── scripts/                     # Utility scripts (seeding database)
├── tests/                       # 39+ Automated Unit/Integration Tests
├── endpoints.md                 # Postman/Manual Testing Guide
└── test.md                      # Comprehensive Examiner Testing Guide
```

---

## 🔐 Role-Based Access Control (RBAC)

The system enforces strict permissions across three user levels:

| Role | Permissions |
| :--- | :--- |
| **Admin** | Full Management Access (Create/Update/Delete Records & Users) |
| **Analyst**| View Records, Access Dashboard Analytics |
| **Viewer** | Access Dashboard Summaries Only |

---

## 🏁 Getting Started (Local Development)

### 1. Setup Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Create a `.env` file based on `.env.example`:
```env
DATABASE_URL=sqlite:///./finance.db
SECRET_KEY=your_secret_hex_key
ALGORITHM=HS256
```

### 3. Initialize Database & Seed Data
```bash
# Apply migrations
alembic upgrade head

# Seed with 3 users (Admin, Analyst, Viewer) and 1 year of data
python scripts/seed_db.py
```

### 4. Run the Server
```bash
uvicorn app.main:app --reload
```
- **Swagger Docs**: `http://localhost:8000/docs`

---

## 🧪 Testing

We maintain a high-quality codebase with 39 automated tests.

```bash
# Run all tests (automatic SQLite in-memory DB used)
python -m pytest -v
```

---

## ☁️ Deployment (Render/Vercel)

This project is ready for one-click deployment to **Render**:
1. Connect your GitHub repository.
2. Build Command: `pip install -r requirements.txt`
3. Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Set Environment Variables: (See `.env.example`)

---

## 📄 Documentation Reference
- **[test.md](test.md)**: The definitive guide for examiners and manual testing.
- **[endpoints.md](endpoints.md)**: Quick reference for Postman JSON payloads and cURL commands.

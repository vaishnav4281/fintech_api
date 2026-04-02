# API Test Cases & Procedure

This document outlines the API endpoints available in the Finance Dashboard and provides test cases that you can run to ensure everything is working correctly.

---

## How to Run Automated Tests (pytest) — Exact Steps

The automated test suite uses an **in-memory SQLite database**, so no PostgreSQL or Neon connection is needed. Follow these steps exactly for a successful run:

<<<<<<< HEAD
### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Pin bcrypt to a Compatible Version
`passlib` is not compatible with `bcrypt>=5.0.0`. You must downgrade bcrypt:
```bash
pip install bcrypt==4.2.1
=======
### Step 1: Create and activate a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
>>>>>>> fb8f58e (Initialize project with full API features and documentation)
```

### Step 3: Run All Tests
```bash
python -m pytest -v
```

> **Note:** Use `python -m pytest` (not bare `pytest`) to ensure it uses the correct Python environment.

### Expected Output
```
============================= test session starts =============================
collected 39 items

tests/test_auth.py::TestLogin::test_login_success PASSED                 [  2%]
tests/test_auth.py::TestLogin::test_login_wrong_password PASSED          [  5%]
tests/test_auth.py::TestLogin::test_login_unknown_email PASSED           [  7%]
tests/test_auth.py::TestLogin::test_protected_route_without_token PASSED [ 10%]
tests/test_auth.py::TestLogin::test_protected_route_with_invalid_token PASSED [ 12%]
tests/test_dashboard.py ... (6 tests) PASSED
tests/test_records.py  ... (13 tests) PASSED
tests/test_users.py    ... (11 tests) PASSED

======================= 39 passed in ~23s =======================
```

<<<<<<< HEAD
### Quick One-Liner (Copy-Paste)
```bash
pip install -r requirements.txt && pip install bcrypt==4.2.1 && python -m pytest -v
=======
---

## 🛠️ Fixed Setup Command (Recommended for Local Dev)

If you want to run the full app locally with the persistent database:

```bash
# 1. Setup Environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Apply Migrations (Local SQLite)
alembic upgrade head

# 3. Seed Sample Data
python scripts/seed_db.py

# 4. Start the Server
uvicorn app.main:app --reload
>>>>>>> fb8f58e (Initialize project with full API features and documentation)
```

---

## Manual API Testing (Swagger UI / Postman / cURL)

<<<<<<< HEAD
### Prerequisites

1.  **Install Dependencies:** `pip install -r requirements.txt` and `pip install bcrypt==4.2.1`
2.  **Apply Database Migrations:** Run Alembic migrations so the remote Neon database creates the required tables.
    ```bash
    python -m alembic upgrade head
    ```
3.  **Seed Sample Data (optional):**
    ```bash
    python scripts/seed_db.py
    ```
4.  **Start the Server:**
    ```bash
    uvicorn app.main:app --reload
    ```
5.  **Swagger UI:** Navigate to: `http://localhost:8000/docs`.

---

## Scenario 1: User Registration & Authentication

Before any operations can be performed, you must create users with different roles.

### 1.1 Create Admin User
=======
### Scenario 1: User Registration & Authentication

#### 1.1 Create Admin User
>>>>>>> fb8f58e (Initialize project with full API features and documentation)
- **Endpoint:** `POST /auth/register`
- **Body (JSON):**
  ```json
  {
    "name": "Admin User",
    "email": "admin@example.com",
    "password": "Password123!",
    "role": "admin"
  }
  ```
<<<<<<< HEAD
- **Expected:** `201 Created` with user details.

### 1.2 Create Analyst User
- **Endpoint:** `POST /auth/register`
- **Body (JSON):**
  ```json
  {
    "name": "Analyst User",
    "email": "analyst@example.com",
    "password": "Password123!",
    "role": "analyst"
  }
  ```
- **Expected:** `201 Created`

### 1.3 Create Viewer User
- **Endpoint:** `POST /auth/register`
- **Body (JSON):**
  ```json
  {
    "name": "Viewer User",
    "email": "viewer@example.com",
    "password": "Password123!",
    "role": "viewer"
  }
  ```
- **Expected:** `201 Created`

### 1.4 Get Access Token (Login)
- **Endpoint:** `POST /auth/login`
- **Body (x-www-form-urlencoded):**
  - `username`: `admin@example.com`
  - `password`: `Password123!`
- **Expected:** `200 OK` returning an `access_token`. 
- *(Save this token and use it as a Bearer Token for subsequent requests)*.
=======
- **Expected:** `201 Created`

#### 1.2 Get Access Token (Login)
- **Endpoint:** `POST /auth/login`
- **Body (JSON):**
  ```json
  {
    "email": "admin@example.com",
    "password": "Password123!"
  }
  ```
- **Expected:** `200 OK`
- **Example Output:**
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "role": "admin"
  }
  ```
- *(Save this token and use it as a Bearer Token for subsequent requests. **Do NOT include < > brackets in the header.**)*
>>>>>>> fb8f58e (Initialize project with full API features and documentation)

---

## Scenario 2: Financial Records Management

<<<<<<< HEAD
Log in as the **Admin User** and use their token.

### 2.1 Create an Income Record (Admin Only)
- **Endpoint:** `POST /records`
- **Headers:** `Authorization: Bearer <Admin-Token>`
=======
### 2.1 Create an Income Record (Admin Only)
- **Endpoint:** `POST /records`
- **Headers:** `Authorization: Bearer YOUR_TOKEN_HERE`
>>>>>>> fb8f58e (Initialize project with full API features and documentation)
- **Body (JSON):**
  ```json
  {
    "amount": 5000,
    "type": "income",
    "category": "Salary",
    "date": "2023-10-01",
    "notes": "October Salary"
  }
  ```
- **Expected:** `201 Created`
<<<<<<< HEAD

### 2.2 Create an Expense Record (Admin Only)
- **Endpoint:** `POST /records`
- **Headers:** `Authorization: Bearer <Admin-Token>`
- **Body (JSON):**
  ```json
  {
    "amount": 1500,
    "type": "expense",
    "category": "Rent",
    "date": "2023-10-02"
  }
  ```
- **Expected:** `201 Created`

### 2.3 Attempt to Create Record as Analyst (Should Fail)
- **Endpoint:** `POST /records`
- **Headers:** `Authorization: Bearer <Analyst-Token>`
- **Expected:** `403 Forbidden` (Only Admins can create records).

### 2.4 List Financial Records (Analyst / Admin)
- **Endpoint:** `GET /records?page=1&limit=10&type=income`
- **Headers:** `Authorization: Bearer <Admin-Token>` OR `<Analyst-Token>`
- **Expected:** `200 OK` returning a paginated list of records.

### 2.5 Update a Record (Admin Only)
- **Endpoint:** `PUT /records/1`
- **Headers:** `Authorization: Bearer <Admin-Token>`
- **Body (JSON):**
  ```json
  {
    "amount": 5500,
    "notes": "Updated Salary"
  }
  ```
- **Expected:** `200 OK`

=======
- **Example Output:**
  ```json
  {
    "id": 92,
    "amount": "5000.00",
    "type": "income",
    "category": "Salary",
    "date": "2023-10-01",
    "notes": "October Salary",
    "created_by": 1,
    "created_at": "2026-04-02T11:58:10"
  }
  ```

### 2.2 List Financial Records (Public/Authenticated)
- **Endpoint:** `GET /records?page=1&limit=10`
- **Headers:** `Authorization: Bearer YOUR_TOKEN_HERE`
- **Expected:** `200 OK` returning a paginated list of records.

>>>>>>> fb8f58e (Initialize project with full API features and documentation)
---

## Scenario 3: Dashboard Summaries

<<<<<<< HEAD
All roles (Viewer, Analyst, Admin) have access to dashboard endpoints. Use the `<Viewer-Token>` to verify.

### 3.1 Get General Summary
- **Endpoint:** `GET /dashboard/summary`
- **Headers:** `Authorization: Bearer <Viewer-Token>`
=======
### 3.1 Get General Summary
- **Endpoint:** `GET /dashboard/summary`
- **Headers:** `Authorization: Bearer YOUR_TOKEN_HERE`
>>>>>>> fb8f58e (Initialize project with full API features and documentation)
- **Expected:** `200 OK` returning `total_income`, `total_expenses`, and `net_balance`.

### 3.2 Get Category Summary
- **Endpoint:** `GET /dashboard/category-summary`
<<<<<<< HEAD
- **Headers:** `Authorization: Bearer <Viewer-Token>`
- **Expected:** `200 OK` returning grouped totals (e.g., total spent on "Rent" vs earned in "Salary").

### 3.3 Get Recent Records
- **Endpoint:** `GET /dashboard/recent`
- **Headers:** `Authorization: Bearer <Viewer-Token>`
- **Expected:** `200 OK` returning max 10 recent transactions.

### 3.4 Get Monthly Trends
- **Endpoint:** `GET /dashboard/monthly-trends`
- **Headers:** `Authorization: Bearer <Viewer-Token>`
- **Expected:** `200 OK` returning data aggregated year-month.
=======
- **Headers:** `Authorization: Bearer YOUR_TOKEN_HERE`
- **Expected:** `200 OK`
>>>>>>> fb8f58e (Initialize project with full API features and documentation)

---

## Checklists for Expected Failure / Access Control

<<<<<<< HEAD
- [ ] **Viewer** tries to `GET /records` -> Expected HTTP `403 Forbidden`
- [ ] **Viewer** or **Analyst** tries to `POST /records` -> Expected HTTP `403 Forbidden`
- [ ] **Viewer** or **Analyst** tries to `DELETE /records/1` -> Expected HTTP `403 Forbidden`
- [ ] **Unauthorized (No Token)** tries to `GET /dashboard/summary` -> Expected HTTP `401 Unauthorized`
- [ ] Submitting a record with an invalid category or missing amount -> Expected HTTP `422 Unprocessable Entity` (Pydantic validation)
=======
- [X] **Missing Token** -> Expected HTTP `401 Unauthorized`
- [X] **Invalid Token Pattern (including < >)** -> Expected HTTP `401 Unauthorized`
- [X] **Analyst/Viewer** tries to `POST /records` -> Expected HTTP `403 Forbidden`
- [X] **Invalid Payload** (missing amount) -> Expected HTTP `422 Unprocessable Entity`
>>>>>>> fb8f58e (Initialize project with full API features and documentation)

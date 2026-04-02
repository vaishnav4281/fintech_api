"""
Test configuration.

Uses an in-memory SQLite database so tests run without PostgreSQL.
Sets DATABASE_URL env var BEFORE importing the app so the engine
is created with SQLite, not the production Postgres URL.
"""
import os

# ── Override DB URL before any app module is imported ────────────────────────
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app
from app.services.user_service import create_user
from app.schemas.user_schema import UserCreate
from app.models.user import UserRole

SQLITE_URL = "sqlite:///./test.db"

engine = create_engine(SQLITE_URL, connect_args={"check_same_thread": False})

# Enable foreign key enforcement in SQLite
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


# ── Reusable user fixtures ────────────────────────────────────────────────────

def _make_user(db, role: UserRole, email: str = None):
    email = email or f"{role.value}@test.com"
    return create_user(
        db,
        UserCreate(name=role.value.title(), email=email, password="Test1234!", role=role),
    )


@pytest.fixture
def admin_user(db):
    return _make_user(db, UserRole.admin)


@pytest.fixture
def analyst_user(db):
    return _make_user(db, UserRole.analyst)


@pytest.fixture
def viewer_user(db):
    return _make_user(db, UserRole.viewer)


def _login(client, email: str, password: str = "Test1234!") -> str:
    resp = client.post("/auth/login", data={"username": email, "password": password})
    assert resp.status_code == 200, resp.text
    return resp.json()["access_token"]


@pytest.fixture
def admin_token(client, admin_user):
    return _login(client, admin_user.email)


@pytest.fixture
def analyst_token(client, analyst_user):
    return _login(client, analyst_user.email)


@pytest.fixture
def viewer_token(client, viewer_user):
    return _login(client, viewer_user.email)


def auth_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}

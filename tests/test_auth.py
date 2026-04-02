import pytest
from tests.conftest import auth_headers


class TestLogin:
    def test_login_success(self, client, admin_user):
        resp = client.post("/auth/login", data={"username": admin_user.email, "password": "Test1234!"})
        assert resp.status_code == 200
        body = resp.json()
        assert "access_token" in body
        assert body["token_type"] == "bearer"
        assert body["role"] == "admin"

    def test_login_wrong_password(self, client, admin_user):
        resp = client.post("/auth/login", data={"username": admin_user.email, "password": "WrongPass!"})
        assert resp.status_code == 401

    def test_login_unknown_email(self, client):
        resp = client.post("/auth/login", data={"username": "ghost@nowhere.com", "password": "Test1234!"})
        assert resp.status_code == 401

    def test_protected_route_without_token(self, client):
        resp = client.get("/users")
        assert resp.status_code == 401

    def test_protected_route_with_invalid_token(self, client):
        resp = client.get("/users", headers={"Authorization": "Bearer totally.invalid.token"})
        assert resp.status_code == 401

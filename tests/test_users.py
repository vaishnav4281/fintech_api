import pytest
from tests.conftest import auth_headers


class TestCreateUser:
    def test_admin_can_create_user(self, client, admin_token):
        resp = client.post(
            "/users",
            json={"name": "New Analyst", "email": "new@test.com", "password": "Test1234!", "role": "analyst"},
            headers=auth_headers(admin_token),
        )
        assert resp.status_code == 201
        body = resp.json()
        assert body["email"] == "new@test.com"
        assert body["role"] == "analyst"

    def test_duplicate_email_rejected(self, client, admin_token, admin_user):
        resp = client.post(
            "/users",
            json={"name": "Dupe", "email": admin_user.email, "password": "Test1234!", "role": "viewer"},
            headers=auth_headers(admin_token),
        )
        assert resp.status_code == 409

    def test_analyst_cannot_create_user(self, client, analyst_token):
        resp = client.post(
            "/users",
            json={"name": "X", "email": "x@x.com", "password": "Test1234!", "role": "viewer"},
            headers=auth_headers(analyst_token),
        )
        assert resp.status_code == 403

    def test_viewer_cannot_create_user(self, client, viewer_token):
        resp = client.post(
            "/users",
            json={"name": "X", "email": "x2@x.com", "password": "Test1234!", "role": "viewer"},
            headers=auth_headers(viewer_token),
        )
        assert resp.status_code == 403

    def test_short_password_rejected(self, client, admin_token):
        resp = client.post(
            "/users",
            json={"name": "Short", "email": "short@test.com", "password": "12", "role": "viewer"},
            headers=auth_headers(admin_token),
        )
        assert resp.status_code == 422


class TestListUsers:
    def test_admin_can_list_users(self, client, admin_token, admin_user):
        resp = client.get("/users", headers=auth_headers(admin_token))
        assert resp.status_code == 200
        body = resp.json()
        assert body["total"] >= 1
        assert isinstance(body["items"], list)

    def test_pagination(self, client, admin_token, db):
        from tests.conftest import _make_user
        from app.models.user import UserRole
        for i in range(5):
            _make_user(db, UserRole.viewer, f"viewer{i}@test.com")

        resp = client.get("/users?page=1&limit=2", headers=auth_headers(admin_token))
        assert resp.status_code == 200
        assert len(resp.json()["items"]) == 2


class TestUpdateUser:
    def test_admin_can_update_name(self, client, admin_token, viewer_user):
        resp = client.put(
            f"/users/{viewer_user.id}",
            json={"name": "Updated Name"},
            headers=auth_headers(admin_token),
        )
        assert resp.status_code == 200
        assert resp.json()["name"] == "Updated Name"

    def test_update_nonexistent_user(self, client, admin_token):
        resp = client.put("/users/99999", json={"name": "X"}, headers=auth_headers(admin_token))
        assert resp.status_code == 404


class TestUserStatus:
    def test_admin_can_deactivate_user(self, client, admin_token, viewer_user):
        resp = client.patch(
            f"/users/{viewer_user.id}/status",
            json={"status": "inactive"},
            headers=auth_headers(admin_token),
        )
        assert resp.status_code == 200
        assert resp.json()["status"] == "inactive"

    def test_inactive_user_cannot_login(self, client, admin_token, viewer_user):
        client.patch(
            f"/users/{viewer_user.id}/status",
            json={"status": "inactive"},
            headers=auth_headers(admin_token),
        )
        resp = client.post("/auth/login", data={"username": viewer_user.email, "password": "Test1234!"})
        assert resp.status_code == 403


class TestDeleteUser:
    def test_admin_can_delete_user(self, client, admin_token, viewer_user):
        resp = client.delete(f"/users/{viewer_user.id}", headers=auth_headers(admin_token))
        assert resp.status_code == 204
        # Confirm gone
        resp2 = client.get(f"/users/{viewer_user.id}", headers=auth_headers(admin_token))
        assert resp2.status_code == 404

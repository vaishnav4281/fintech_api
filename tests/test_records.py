import pytest
from datetime import date
from tests.conftest import auth_headers


SAMPLE_RECORD = {
    "amount": 2500.00,
    "type": "income",
    "category": "Salary",
    "date": "2024-03-15",
    "notes": "March salary",
}


class TestCreateRecord:
    def test_admin_can_create_record(self, client, admin_token):
        resp = client.post("/records", json=SAMPLE_RECORD, headers=auth_headers(admin_token))
        assert resp.status_code == 201
        body = resp.json()
        assert body["category"] == "Salary"
        assert float(body["amount"]) == 2500.00
        assert body["type"] == "income"

    def test_analyst_cannot_create_record(self, client, analyst_token):
        resp = client.post("/records", json=SAMPLE_RECORD, headers=auth_headers(analyst_token))
        assert resp.status_code == 403

    def test_viewer_cannot_create_record(self, client, viewer_token):
        resp = client.post("/records", json=SAMPLE_RECORD, headers=auth_headers(viewer_token))
        assert resp.status_code == 403

    def test_negative_amount_rejected(self, client, admin_token):
        bad = {**SAMPLE_RECORD, "amount": -100}
        resp = client.post("/records", json=bad, headers=auth_headers(admin_token))
        assert resp.status_code == 422

    def test_zero_amount_rejected(self, client, admin_token):
        bad = {**SAMPLE_RECORD, "amount": 0}
        resp = client.post("/records", json=bad, headers=auth_headers(admin_token))
        assert resp.status_code == 422

    def test_invalid_type_rejected(self, client, admin_token):
        bad = {**SAMPLE_RECORD, "type": "transfer"}
        resp = client.post("/records", json=bad, headers=auth_headers(admin_token))
        assert resp.status_code == 422

    def test_missing_required_fields_rejected(self, client, admin_token):
        resp = client.post("/records", json={"amount": 100}, headers=auth_headers(admin_token))
        assert resp.status_code == 422


class TestListRecords:
    def _create(self, client, token, overrides=None):
        payload = {**SAMPLE_RECORD, **(overrides or {})}
        return client.post("/records", json=payload, headers=auth_headers(token))

    def test_analyst_can_list_records(self, client, admin_token, analyst_token):
        self._create(client, admin_token)
        resp = client.get("/records", headers=auth_headers(analyst_token))
        assert resp.status_code == 200
        assert resp.json()["total"] >= 1

    def test_viewer_cannot_list_records(self, client, viewer_token):
        resp = client.get("/records", headers=auth_headers(viewer_token))
        assert resp.status_code == 403

    def test_filter_by_type(self, client, admin_token):
        self._create(client, admin_token, {"type": "income"})
        self._create(client, admin_token, {"type": "expense", "category": "Rent"})
        resp = client.get("/records?type=income", headers=auth_headers(admin_token))
        items = resp.json()["items"]
        assert all(r["type"] == "income" for r in items)

    def test_filter_by_category(self, client, admin_token):
        self._create(client, admin_token, {"category": "Groceries"})
        self._create(client, admin_token, {"category": "Transport"})
        resp = client.get("/records?category=Groceries", headers=auth_headers(admin_token))
        items = resp.json()["items"]
        assert all("groceries" in r["category"].lower() for r in items)

    def test_filter_by_date_range(self, client, admin_token):
        self._create(client, admin_token, {"date": "2024-01-10"})
        self._create(client, admin_token, {"date": "2024-06-20"})
        resp = client.get(
            "/records?start_date=2024-01-01&end_date=2024-03-31",
            headers=auth_headers(admin_token),
        )
        items = resp.json()["items"]
        for r in items:
            assert r["date"] <= "2024-03-31"

    def test_pagination(self, client, admin_token):
        for i in range(5):
            self._create(client, admin_token, {"category": f"Cat{i}"})
        resp = client.get("/records?page=1&limit=2", headers=auth_headers(admin_token))
        assert len(resp.json()["items"]) == 2


class TestUpdateRecord:
    def test_admin_can_update_record(self, client, admin_token):
        create_resp = client.post("/records", json=SAMPLE_RECORD, headers=auth_headers(admin_token))
        record_id = create_resp.json()["id"]
        resp = client.put(
            f"/records/{record_id}",
            json={"amount": 3000.00, "notes": "Updated"},
            headers=auth_headers(admin_token),
        )
        assert resp.status_code == 200
        assert float(resp.json()["amount"]) == 3000.00

    def test_analyst_cannot_update_record(self, client, admin_token, analyst_token):
        create_resp = client.post("/records", json=SAMPLE_RECORD, headers=auth_headers(admin_token))
        record_id = create_resp.json()["id"]
        resp = client.put(
            f"/records/{record_id}",
            json={"amount": 9999},
            headers=auth_headers(analyst_token),
        )
        assert resp.status_code == 403


class TestDeleteRecord:
    def test_admin_can_delete_record(self, client, admin_token):
        create_resp = client.post("/records", json=SAMPLE_RECORD, headers=auth_headers(admin_token))
        record_id = create_resp.json()["id"]
        resp = client.delete(f"/records/{record_id}", headers=auth_headers(admin_token))
        assert resp.status_code == 204
        # Confirm soft-deleted
        resp2 = client.get(f"/records/{record_id}", headers=auth_headers(admin_token))
        assert resp2.status_code == 404

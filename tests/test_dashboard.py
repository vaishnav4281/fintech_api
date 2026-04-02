import pytest
from tests.conftest import auth_headers


def _seed_records(client, token):
    records = [
        {"amount": 5000, "type": "income", "category": "Salary", "date": "2024-01-15"},
        {"amount": 1200, "type": "expense", "category": "Rent", "date": "2024-01-20"},
        {"amount": 300, "type": "expense", "category": "Groceries", "date": "2024-02-05"},
        {"amount": 800, "type": "income", "category": "Freelance", "date": "2024-02-10"},
    ]
    for r in records:
        client.post("/records", json=r, headers=auth_headers(token))


class TestDashboardSummary:
    def test_viewer_can_access_summary(self, client, admin_token, viewer_token):
        _seed_records(client, admin_token)
        resp = client.get("/dashboard/summary", headers=auth_headers(viewer_token))
        assert resp.status_code == 200
        body = resp.json()
        assert float(body["total_income"]) == 5800.0
        assert float(body["total_expenses"]) == 1500.0
        assert float(body["net_balance"]) == 4300.0

    def test_unauthenticated_cannot_access(self, client):
        resp = client.get("/dashboard/summary")
        assert resp.status_code == 401


class TestCategorySummary:
    def test_returns_grouped_totals(self, client, admin_token):
        _seed_records(client, admin_token)
        resp = client.get("/dashboard/category-summary", headers=auth_headers(admin_token))
        assert resp.status_code == 200
        items = resp.json()
        categories = [i["category"] for i in items]
        assert "Salary" in categories
        assert "Rent" in categories


class TestRecentRecords:
    def test_returns_at_most_10(self, client, admin_token):
        for i in range(12):
            client.post(
                "/records",
                json={"amount": 100, "type": "income", "category": f"Cat{i}", "date": "2024-03-01"},
                headers=auth_headers(admin_token),
            )
        resp = client.get("/dashboard/recent", headers=auth_headers(admin_token))
        assert resp.status_code == 200
        assert len(resp.json()) <= 10


class TestMonthlyTrends:
    def test_returns_monthly_breakdown(self, client, admin_token):
        _seed_records(client, admin_token)
        resp = client.get("/dashboard/monthly-trends", headers=auth_headers(admin_token))
        assert resp.status_code == 200
        months = resp.json()
        assert len(months) == 2  # January and February
        jan = next(m for m in months if m["month"] == 1)
        assert float(jan["total_income"]) == 5000.0
        assert float(jan["total_expenses"]) == 1200.0

    def test_viewer_can_access_trends(self, client, admin_token, viewer_token):
        _seed_records(client, admin_token)
        resp = client.get("/dashboard/monthly-trends", headers=auth_headers(viewer_token))
        assert resp.status_code == 200

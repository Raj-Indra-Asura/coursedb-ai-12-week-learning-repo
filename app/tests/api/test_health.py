"""Tests for the health-check endpoints."""

from fastapi.testclient import TestClient


def test_health_check_returns_200(client: TestClient) -> None:
    response = client.get("/health/")
    assert response.status_code == 200


def test_health_check_reports_healthy_status(client: TestClient) -> None:
    data = client.get("/health/").json()
    assert data["status"] == "healthy"
    assert data["version"] == "1.0.0"


def test_health_check_returns_json(client: TestClient) -> None:
    response = client.get("/health/")
    assert response.headers["content-type"].startswith("application/json")


def test_database_health_connected(client: TestClient) -> None:
    data = client.get("/health/db").json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"


def test_db_tables_endpoint_lists_tables(client: TestClient) -> None:
    response = client.get("/health/db/tables")
    assert response.status_code == 200
    body = response.json()
    assert "status" in body


def test_db_counts_endpoint(client: TestClient) -> None:
    response = client.get("/health/db/counts")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_root_endpoint(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == 200

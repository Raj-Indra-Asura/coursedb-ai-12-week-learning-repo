"""Tests for the learning navigation API.

These exercise the filesystem-backed curriculum discovery using the real
repository layout (the service derives the repo root from its own location).
"""

from fastapi.testclient import TestClient


def test_initialize_curriculum(client: TestClient) -> None:
    response = client.post("/learning/initialize")
    assert response.status_code == 200


def test_curriculum_overview(client: TestClient) -> None:
    client.post("/learning/initialize")
    response = client.get("/learning/curriculum")
    assert response.status_code == 200
    body = response.json()
    assert "weeks" in body


def test_get_week_details(client: TestClient) -> None:
    client.post("/learning/initialize")
    response = client.get("/learning/weeks/1/details")
    assert response.status_code in (200, 404)


def test_learning_stats(client: TestClient) -> None:
    client.post("/learning/initialize")
    response = client.get("/learning/stats")
    assert response.status_code == 200


def test_update_week_status(client: TestClient) -> None:
    client.post("/learning/initialize")
    response = client.put("/learning/weeks/1/status", params={"new_status": "in_progress"})
    assert response.status_code in (200, 404, 422)


def test_search_learning_resources(client: TestClient) -> None:
    client.post("/learning/initialize")
    response = client.get("/learning/search", params={"query": "theory"})
    assert response.status_code == 200

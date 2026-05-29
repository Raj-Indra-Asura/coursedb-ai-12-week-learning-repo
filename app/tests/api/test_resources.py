"""Tests for the resources CRUD API."""

from fastapi.testclient import TestClient


def _make_course(client: TestClient) -> int:
    return client.post(
        "/api/courses/",
        json={"course_code": "CSE2203", "course_title": "DBMS", "credit": 3},
    ).json()["course_id"]


def _resource_payload(course_id: int, **overrides) -> dict:
    payload = {
        "course_id": course_id,
        "title": "DBMS Lecture Notes",
        "resource_type": "note",
        "description": "Week 1 notes",
    }
    payload.update(overrides)
    return payload


def test_create_resource(client: TestClient) -> None:
    course_id = _make_course(client)
    response = client.post("/api/resources/", json=_resource_payload(course_id))
    assert response.status_code == 201
    assert response.json()["title"] == "DBMS Lecture Notes"


def test_list_resources(client: TestClient) -> None:
    course_id = _make_course(client)
    client.post("/api/resources/", json=_resource_payload(course_id))
    response = client.get("/api/resources/")
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_get_resource_by_id(client: TestClient) -> None:
    course_id = _make_course(client)
    created = client.post("/api/resources/", json=_resource_payload(course_id)).json()
    response = client.get(f"/api/resources/{created['resource_id']}")
    assert response.status_code == 200


def test_get_missing_resource_returns_404(client: TestClient) -> None:
    assert client.get("/api/resources/99999").status_code == 404


def test_invalid_resource_type_rejected(client: TestClient) -> None:
    course_id = _make_course(client)
    response = client.post(
        "/api/resources/", json=_resource_payload(course_id, resource_type="bogus")
    )
    assert response.status_code == 422


def test_delete_resource(client: TestClient) -> None:
    course_id = _make_course(client)
    created = client.post("/api/resources/", json=_resource_payload(course_id)).json()
    assert client.delete(f"/api/resources/{created['resource_id']}").status_code == 204
    assert client.get(f"/api/resources/{created['resource_id']}").status_code == 404


def test_resource_chunks_endpoint(client: TestClient) -> None:
    course_id = _make_course(client)
    created = client.post("/api/resources/", json=_resource_payload(course_id)).json()
    response = client.get(f"/api/resources/{created['resource_id']}/chunks")
    assert response.status_code == 200

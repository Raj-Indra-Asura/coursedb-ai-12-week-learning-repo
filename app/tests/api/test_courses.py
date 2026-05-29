"""Tests for the courses CRUD API."""

from fastapi.testclient import TestClient


def _course_payload(**overrides) -> dict:
    payload = {
        "course_code": "CSE2204",
        "course_title": "DBMS Sessional",
        "semester": "Fall",
        "credit": 2,
    }
    payload.update(overrides)
    return payload


def test_create_course(client: TestClient) -> None:
    response = client.post("/api/courses/", json=_course_payload())
    assert response.status_code == 201
    body = response.json()
    assert body["course_code"] == "CSE2204"
    assert body["course_id"] > 0


def test_list_courses(client: TestClient) -> None:
    client.post("/api/courses/", json=_course_payload())
    response = client.get("/api/courses/")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_course_by_id(client: TestClient) -> None:
    created = client.post("/api/courses/", json=_course_payload()).json()
    response = client.get(f"/api/courses/{created['course_id']}")
    assert response.status_code == 200
    assert response.json()["course_title"] == "DBMS Sessional"


def test_get_missing_course_returns_404(client: TestClient) -> None:
    assert client.get("/api/courses/99999").status_code == 404


def test_duplicate_course_code_rejected(client: TestClient) -> None:
    client.post("/api/courses/", json=_course_payload())
    response = client.post("/api/courses/", json=_course_payload())
    assert response.status_code == 400


def test_update_course(client: TestClient) -> None:
    created = client.post("/api/courses/", json=_course_payload()).json()
    response = client.put(
        f"/api/courses/{created['course_id']}", json={"course_title": "Updated Title"}
    )
    assert response.status_code == 200
    assert response.json()["course_title"] == "Updated Title"


def test_delete_course(client: TestClient) -> None:
    created = client.post("/api/courses/", json=_course_payload()).json()
    assert client.delete(f"/api/courses/{created['course_id']}").status_code == 204
    assert client.get(f"/api/courses/{created['course_id']}").status_code == 404


def test_create_course_invalid_credit_rejected(client: TestClient) -> None:
    response = client.post("/api/courses/", json=_course_payload(credit=0))
    assert response.status_code == 422

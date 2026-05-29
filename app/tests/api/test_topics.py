"""Tests for the topics CRUD API."""

from fastapi.testclient import TestClient

from app.db.models import Course


def _make_course(client: TestClient, code: str = "CSE2203") -> int:
    body = client.post(
        "/api/courses/",
        json={"course_code": code, "course_title": "DBMS", "credit": 3},
    ).json()
    return body["course_id"]


def test_create_topic(client: TestClient) -> None:
    course_id = _make_course(client)
    response = client.post(
        "/api/topics/",
        json={"course_id": course_id, "topic_name": "Indexing", "week_number": 7},
    )
    assert response.status_code == 201
    assert response.json()["topic_name"] == "Indexing"


def test_list_topics(client: TestClient) -> None:
    course_id = _make_course(client)
    client.post(
        "/api/topics/",
        json={"course_id": course_id, "topic_name": "B+ Trees", "week_number": 7},
    )
    response = client.get("/api/topics/")
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_get_topic_by_id(client: TestClient) -> None:
    course_id = _make_course(client)
    created = client.post(
        "/api/topics/",
        json={"course_id": course_id, "topic_name": "ACID", "week_number": 9},
    ).json()
    response = client.get(f"/api/topics/{created['topic_id']}")
    assert response.status_code == 200
    assert response.json()["topic_name"] == "ACID"


def test_get_missing_topic_returns_404(client: TestClient) -> None:
    assert client.get("/api/topics/99999").status_code == 404


def test_update_topic(client: TestClient) -> None:
    course_id = _make_course(client)
    created = client.post(
        "/api/topics/",
        json={"course_id": course_id, "topic_name": "Joins", "week_number": 2},
    ).json()
    response = client.put(f"/api/topics/{created['topic_id']}", json={"topic_name": "SQL Joins"})
    assert response.status_code == 200
    assert response.json()["topic_name"] == "SQL Joins"


def test_delete_topic(client: TestClient) -> None:
    course_id = _make_course(client)
    created = client.post(
        "/api/topics/",
        json={"course_id": course_id, "topic_name": "Locks", "week_number": 9},
    ).json()
    assert client.delete(f"/api/topics/{created['topic_id']}").status_code == 204
    assert client.get(f"/api/topics/{created['topic_id']}").status_code == 404


def test_invalid_week_number_rejected(client: TestClient) -> None:
    course_id = _make_course(client)
    response = client.post(
        "/api/topics/",
        json={"course_id": course_id, "topic_name": "Bad", "week_number": 0},
    )
    assert response.status_code == 422

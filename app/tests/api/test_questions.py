"""Tests for the questions CRUD API."""

from fastapi.testclient import TestClient


def _setup_course_topic(client: TestClient) -> tuple[int, int]:
    course_id = client.post(
        "/api/courses/",
        json={"course_code": "CSE2203", "course_title": "DBMS", "credit": 3},
    ).json()["course_id"]
    topic_id = client.post(
        "/api/topics/",
        json={"course_id": course_id, "topic_name": "Normalization", "week_number": 4},
    ).json()["topic_id"]
    return course_id, topic_id


def _question_payload(course_id: int, topic_id: int, **overrides) -> dict:
    payload = {
        "course_id": course_id,
        "topic_id": topic_id,
        "question_text": "Define 3NF.",
        "year": 2023,
        "exam_type": "final",
        "difficulty": "medium",
        "marks": 5,
    }
    payload.update(overrides)
    return payload


def test_create_question(client: TestClient) -> None:
    course_id, topic_id = _setup_course_topic(client)
    response = client.post("/api/questions/", json=_question_payload(course_id, topic_id))
    assert response.status_code == 201
    assert response.json()["question_text"] == "Define 3NF."


def test_list_questions(client: TestClient) -> None:
    course_id, topic_id = _setup_course_topic(client)
    client.post("/api/questions/", json=_question_payload(course_id, topic_id))
    response = client.get("/api/questions/")
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_get_question_by_id(client: TestClient) -> None:
    course_id, topic_id = _setup_course_topic(client)
    created = client.post("/api/questions/", json=_question_payload(course_id, topic_id)).json()
    response = client.get(f"/api/questions/{created['question_id']}")
    assert response.status_code == 200


def test_get_missing_question_returns_404(client: TestClient) -> None:
    assert client.get("/api/questions/99999").status_code == 404


def test_invalid_difficulty_rejected(client: TestClient) -> None:
    course_id, topic_id = _setup_course_topic(client)
    response = client.post(
        "/api/questions/",
        json=_question_payload(course_id, topic_id, difficulty="impossible"),
    )
    assert response.status_code == 422


def test_invalid_year_rejected(client: TestClient) -> None:
    course_id, topic_id = _setup_course_topic(client)
    response = client.post(
        "/api/questions/", json=_question_payload(course_id, topic_id, year=1999)
    )
    assert response.status_code == 422


def test_delete_question(client: TestClient) -> None:
    course_id, topic_id = _setup_course_topic(client)
    created = client.post("/api/questions/", json=_question_payload(course_id, topic_id)).json()
    assert client.delete(f"/api/questions/{created['question_id']}").status_code == 204

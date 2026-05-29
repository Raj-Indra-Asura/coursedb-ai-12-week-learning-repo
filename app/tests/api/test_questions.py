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


def test_list_questions_filters(client: TestClient) -> None:
    course_id, topic_id = _setup_course_topic(client)
    client.post(
        "/api/questions/",
        json=_question_payload(
            course_id,
            topic_id,
            question_text="Explain normalization.",
            year=2023,
            exam_type="final",
            difficulty="hard",
        ),
    )
    client.post(
        "/api/questions/",
        json=_question_payload(
            course_id,
            topic_id,
            question_text="Define a primary key.",
            year=2022,
            exam_type="quiz",
            difficulty="easy",
        ),
    )

    # Each filter branch should narrow the result set.
    assert len(client.get(f"/api/questions/?course_id={course_id}").json()) == 2
    assert len(client.get(f"/api/questions/?topic_id={topic_id}").json()) == 2
    assert len(client.get("/api/questions/?year=2023").json()) == 1
    assert len(client.get("/api/questions/?exam_type=quiz").json()) == 1
    assert len(client.get("/api/questions/?difficulty=hard").json()) == 1
    assert len(client.get("/api/questions/?search=normalization").json()) == 1


def test_create_question_invalid_course_returns_400(client: TestClient) -> None:
    _course_id, topic_id = _setup_course_topic(client)
    response = client.post("/api/questions/", json=_question_payload(99999, topic_id))
    assert response.status_code == 400


def test_create_question_invalid_topic_returns_400(client: TestClient) -> None:
    course_id, _topic_id = _setup_course_topic(client)
    response = client.post("/api/questions/", json=_question_payload(course_id, 99999))
    assert response.status_code == 400


def test_update_question_success(client: TestClient) -> None:
    course_id, topic_id = _setup_course_topic(client)
    created = client.post("/api/questions/", json=_question_payload(course_id, topic_id)).json()
    response = client.put(
        f"/api/questions/{created['question_id']}",
        json={"difficulty": "easy", "marks": 8},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["difficulty"] == "easy"
    assert body["marks"] == 8


def test_update_missing_question_returns_404(client: TestClient) -> None:
    assert client.put("/api/questions/99999", json={"marks": 5}).status_code == 404


def test_update_question_invalid_topic_returns_400(client: TestClient) -> None:
    course_id, topic_id = _setup_course_topic(client)
    created = client.post("/api/questions/", json=_question_payload(course_id, topic_id)).json()
    response = client.put(f"/api/questions/{created['question_id']}", json={"topic_id": 99999})
    assert response.status_code == 400


def test_delete_missing_question_returns_404(client: TestClient) -> None:
    assert client.delete("/api/questions/99999").status_code == 404


def test_search_questions_by_topic_name(client: TestClient) -> None:
    course_id, topic_id = _setup_course_topic(client)
    client.post(
        "/api/questions/",
        json=_question_payload(course_id, topic_id, topic_name="Normalization"),
    )
    response = client.get("/api/questions/search/by-topic/normal")
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_questions_stats_by_year(client: TestClient) -> None:
    course_id, topic_id = _setup_course_topic(client)
    client.post("/api/questions/", json=_question_payload(course_id, topic_id, year=2023))
    client.post("/api/questions/", json=_question_payload(course_id, topic_id, year=2023))
    client.post("/api/questions/", json=_question_payload(course_id, topic_id, year=2022))
    stats = client.get("/api/questions/stats/by-year").json()
    by_year = {row["year"]: row["count"] for row in stats}
    assert by_year[2023] == 2
    assert by_year[2022] == 1


def test_questions_stats_by_difficulty(client: TestClient) -> None:
    course_id, topic_id = _setup_course_topic(client)
    client.post("/api/questions/", json=_question_payload(course_id, topic_id, difficulty="hard"))
    client.post("/api/questions/", json=_question_payload(course_id, topic_id, difficulty="easy"))
    stats = client.get("/api/questions/stats/by-difficulty").json()
    by_difficulty = {row["difficulty"]: row["count"] for row in stats}
    assert by_difficulty["hard"] == 1
    assert by_difficulty["easy"] == 1

"""Tests for the analytics API endpoints."""

from fastapi.testclient import TestClient

from app.db.models import Question


def test_overview_counts(client: TestClient, sample_questions: list[Question]) -> None:
    data = client.get("/api/analytics/overview").json()
    assert data["total_courses"] == 1
    assert data["total_topics"] == 1
    assert data["total_questions"] == 3


def test_topic_frequency(client: TestClient, sample_questions: list[Question]) -> None:
    data = client.get("/api/analytics/topic-frequency").json()
    assert isinstance(data, list)
    assert data[0]["question_count"] == 3


def test_difficulty_distribution(client: TestClient, sample_questions: list[Question]) -> None:
    data = client.get("/api/analytics/difficulty-distribution").json()
    counts = {row["difficulty"]: row["count"] for row in data}
    assert counts.get("easy") == 1
    assert counts.get("medium") == 1
    assert counts.get("hard") == 1


def test_exam_type_distribution(client: TestClient, sample_questions: list[Question]) -> None:
    data = client.get("/api/analytics/exam-type-distribution").json()
    assert sum(row["count"] for row in data) == 3


def test_year_wise_trends(client: TestClient, sample_questions: list[Question]) -> None:
    response = client.get("/api/analytics/year-wise-trends")
    assert response.status_code == 200


def test_resource_summary_empty(client: TestClient) -> None:
    response = client.get("/api/analytics/resource-summary")
    assert response.status_code == 200
    assert "by_type" in response.json()


def test_overview_empty_database(client: TestClient) -> None:
    data = client.get("/api/analytics/overview").json()
    assert data["total_questions"] == 0

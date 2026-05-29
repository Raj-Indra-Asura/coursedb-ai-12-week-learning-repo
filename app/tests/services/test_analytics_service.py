"""Tests for the AnalyticsService ORM aggregate queries."""

from sqlalchemy.orm import Session

from app.db.models import Question, Resource
from app.services.analytics_service import AnalyticsService


def test_topic_frequency(test_db: Session, sample_questions: list[Question]) -> None:
    result = AnalyticsService(test_db).get_topic_frequency()
    assert result[0]["topic_name"] == "Normalization"
    assert result[0]["question_count"] == 3


def test_difficulty_distribution(test_db: Session, sample_questions: list[Question]) -> None:
    dist = AnalyticsService(test_db).get_difficulty_distribution()
    assert dist == {"easy": 1, "medium": 1, "hard": 1}


def test_difficulty_distribution_empty(test_db: Session) -> None:
    assert AnalyticsService(test_db).get_difficulty_distribution() == {
        "easy": 0,
        "medium": 0,
        "hard": 0,
    }


def test_year_wise_trends(test_db: Session, sample_questions: list[Question]) -> None:
    trends = AnalyticsService(test_db).get_year_wise_trends()
    years = {row["year"] for row in trends}
    assert years == {2022, 2023}


def test_resource_summary(test_db: Session, sample_course) -> None:
    test_db.add(Resource(course_id=sample_course.course_id, title="N", resource_type="note"))
    test_db.add(Resource(course_id=sample_course.course_id, title="B", resource_type="textbook"))
    test_db.commit()
    summary = AnalyticsService(test_db).get_resource_summary()
    assert summary["total_resources"] == 2
    assert summary["by_type"]["note"] == 1
    assert summary["by_type"]["textbook"] == 1

"""Tests for the SQL search service."""

from sqlalchemy.orm import Session

from app.db.models import Question, Resource
from app.services.sql_search_service import SQLSearchService


def test_search_questions_no_filters(test_db: Session, sample_questions: list[Question]) -> None:
    results = SQLSearchService(test_db).search_questions()
    assert len(results) == 3


def test_search_questions_by_difficulty(test_db: Session, sample_questions: list[Question]) -> None:
    results = SQLSearchService(test_db).search_questions(difficulty="hard")
    assert len(results) == 1


def test_search_questions_by_year(test_db: Session, sample_questions: list[Question]) -> None:
    results = SQLSearchService(test_db).search_questions(year=2023)
    assert len(results) == 2


def test_search_questions_by_topic_name(test_db: Session, sample_questions: list[Question]) -> None:
    results = SQLSearchService(test_db).search_questions(topic_name="normal")
    assert len(results) == 3


def test_search_questions_limit(test_db: Session, sample_questions: list[Question]) -> None:
    results = SQLSearchService(test_db).search_questions(limit=1)
    assert len(results) == 1


def test_search_resources(test_db: Session, sample_course) -> None:
    test_db.add(
        Resource(
            course_id=sample_course.course_id,
            title="Notes",
            resource_type="note",
            year_published=2023,
        )
    )
    test_db.commit()
    results = SQLSearchService(test_db).search_resources(resource_type="note")
    assert len(results) == 1
    assert results[0]["year"] == 2023


def test_search_topics(test_db: Session, sample_topic) -> None:
    results = SQLSearchService(test_db).search_topics(topic_name="Normalization")
    assert len(results) >= 1

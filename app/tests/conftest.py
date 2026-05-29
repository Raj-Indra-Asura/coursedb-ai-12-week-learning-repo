"""Pytest configuration and shared fixtures.

Provides:
    - An isolated in-memory SQLite database per test (``test_db``).
    - A FastAPI ``TestClient`` with the ``get_db`` dependency overridden
      (``client``).
    - Factory fixtures for sample data (``sample_course``, ``sample_topic``,
      ``sample_questions``).

Vector-search tests that need a real ``pgvector`` backend are marked with the
``requires_pgvector`` marker and skipped on SQLite.

Learning Objectives:
    - Understand pytest fixtures and dependency overrides.
    - Set up a disposable test database.
    - Keep tests deterministic and free of network calls.
"""

from __future__ import annotations

import os
from collections.abc import Iterator

import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

# Ensure the application engine never tries to reach a real PostgreSQL while
# importing application modules during tests.
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")

from fastapi.testclient import TestClient  # noqa: E402

from app.backend.main import app  # noqa: E402
from app.db.database import get_db  # noqa: E402
from app.db.models import Base, Course, Question, Topic  # noqa: E402


@event.listens_for(Engine, "connect")
def _enable_sqlite_foreign_keys(dbapi_connection, _connection_record) -> None:
    """Enforce foreign-key constraints on SQLite (off by default)."""
    if dbapi_connection.__class__.__module__.startswith("sqlite3"):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


@pytest.fixture(scope="function")
def test_db() -> Iterator[Session]:
    """Create a fresh in-memory SQLite database for each test.

    Yields:
        A SQLAlchemy session bound to the disposable database.
    """
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    testing_session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = testing_session_local()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


@pytest.fixture(scope="function")
def client(test_db: Session) -> Iterator[TestClient]:
    """FastAPI test client with the ``get_db`` dependency overridden.

    Args:
        test_db: The disposable test session to inject into endpoints.

    Yields:
        A configured ``TestClient``.
    """

    def override_get_db() -> Iterator[Session]:
        yield test_db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def sample_course(test_db: Session) -> Course:
    """Create and persist a sample course.

    Returns:
        The persisted :class:`Course`.
    """
    course = Course(
        course_code="CSE2203",
        course_title="Database Management Systems",
        semester="Fall",
        credit=3,
    )
    test_db.add(course)
    test_db.commit()
    test_db.refresh(course)
    return course


@pytest.fixture
def sample_topic(test_db: Session, sample_course: Course) -> Topic:
    """Create and persist a sample topic linked to ``sample_course``.

    Returns:
        The persisted :class:`Topic`.
    """
    topic = Topic(
        course_id=sample_course.course_id,
        topic_name="Normalization",
        description="Functional dependencies and normal forms.",
        week_number=4,
    )
    test_db.add(topic)
    test_db.commit()
    test_db.refresh(topic)
    return topic


@pytest.fixture
def sample_questions(
    test_db: Session, sample_course: Course, sample_topic: Topic
) -> list[Question]:
    """Create and persist a small set of sample questions.

    Returns:
        The list of persisted :class:`Question` objects.
    """
    questions = [
        Question(
            course_id=sample_course.course_id,
            topic_id=sample_topic.topic_id,
            question_text="Define third normal form (3NF).",
            year=2022,
            exam_type="final",
            difficulty="medium",
            marks=5,
        ),
        Question(
            course_id=sample_course.course_id,
            topic_id=sample_topic.topic_id,
            question_text="Explain a transitive dependency with an example.",
            year=2023,
            exam_type="midterm",
            difficulty="hard",
            marks=10,
        ),
        Question(
            course_id=sample_course.course_id,
            topic_id=sample_topic.topic_id,
            question_text="What is a candidate key?",
            year=2023,
            exam_type="quiz",
            difficulty="easy",
            marks=2,
        ),
    ]
    test_db.add_all(questions)
    test_db.commit()
    for question in questions:
        test_db.refresh(question)
    return questions

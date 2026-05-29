"""Tests for SQLAlchemy models: constraints, cascades and foreign keys."""

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.models import ChunkEmbedding, Course, Question, Resource, ResourceChunk, Topic


def test_course_persisted_with_id(test_db: Session) -> None:
    course = Course(course_code="CSE2203", course_title="DBMS", credit=3)
    test_db.add(course)
    test_db.commit()
    assert course.course_id is not None


def test_unique_course_code_constraint(test_db: Session) -> None:
    test_db.add(Course(course_code="DUP", course_title="A", credit=3))
    test_db.commit()
    test_db.add(Course(course_code="DUP", course_title="B", credit=3))
    with pytest.raises(IntegrityError):
        test_db.commit()
    test_db.rollback()


def test_topic_requires_course_fk(test_db: Session) -> None:
    # course_id references a non-existent course -> FK violation (PRAGMA on).
    test_db.add(Topic(course_id=9999, topic_name="Orphan", week_number=1))
    with pytest.raises(IntegrityError):
        test_db.commit()
    test_db.rollback()


def test_cascade_delete_topics(test_db: Session) -> None:
    course = Course(course_code="CAS", course_title="DBMS", credit=3)
    test_db.add(course)
    test_db.commit()
    test_db.add(Topic(course_id=course.course_id, topic_name="T1", week_number=1))
    test_db.commit()
    test_db.delete(course)
    test_db.commit()
    assert test_db.query(Topic).count() == 0


def test_chunk_embedding_cascade(test_db: Session) -> None:
    course = Course(course_code="EMB", course_title="DBMS", credit=3)
    test_db.add(course)
    test_db.commit()
    resource = Resource(course_id=course.course_id, title="Doc", resource_type="note")
    test_db.add(resource)
    test_db.commit()
    chunk = ResourceChunk(resource_id=resource.resource_id, chunk_index=0, chunk_text="t")
    test_db.add(chunk)
    test_db.commit()
    test_db.add(ChunkEmbedding(chunk_id=chunk.chunk_id))
    test_db.commit()
    test_db.delete(resource)
    test_db.commit()
    assert test_db.query(ResourceChunk).count() == 0
    assert test_db.query(ChunkEmbedding).count() == 0


def test_question_relationship_backref(test_db: Session) -> None:
    course = Course(course_code="REL", course_title="DBMS", credit=3)
    test_db.add(course)
    test_db.commit()
    question = Question(
        course_id=course.course_id,
        question_text="Q?",
        year=2023,
        exam_type="final",
        difficulty="easy",
        marks=1,
    )
    test_db.add(question)
    test_db.commit()
    assert question.course.course_code == "REL"
    assert course.questions[0].question_id == question.question_id


def test_repr_methods(test_db: Session) -> None:
    course = Course(course_code="RPR", course_title="DBMS", credit=3)
    assert "RPR" in repr(course)

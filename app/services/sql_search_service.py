"""
SQL Search Service

Week 6: SQL Queries, Views, Triggers, Constraints

Implements SQL-based search with filters.

Learning Objectives:
- Build complex SQL queries programmatically
- Use SQLAlchemy query API effectively
- Implement filtering, sorting, pagination
- Optimize queries with proper indexing

Filter Options:
- topic_name: Partial match on topic name
- difficulty: exact match (Easy, Medium, Hard)
- year: exact match
- exam_type: exact match (MidTerm, EndTerm, Quiz)
- course_id: exact match
"""

from typing import Any

from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from app.db.models import Course, Question, Resource, Topic


class SQLSearchService:
    """Service for SQL-based search operations"""

    def __init__(self, db: Session):
        """
        Initialize SQL search service

        Args:
            db: Database session
        """
        self.db = db

    def search_questions(
        self,
        topic_name: str | None = None,
        difficulty: str | None = None,
        year: int | None = None,
        exam_type: str | None = None,
        course_id: int | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        """
        Search questions with SQL filters

        Args:
            topic_name: Partial match on topic name (case-insensitive)
            difficulty: Exact match (Easy, Medium, Hard)
            year: Exact match on academic year
            exam_type: Exact match (MidTerm, EndTerm, Quiz)
            course_id: Filter by course
            limit: Maximum results to return
            offset: Number of results to skip (for pagination)

        Returns:
            List of question dictionaries with metadata

        Learning Note:
        - Uses SQLAlchemy ORM for type-safe queries
        - Builds dynamic WHERE clause based on provided filters
        - Eager loads relationships to avoid N+1 queries
        - Uses ILIKE for case-insensitive pattern matching
        """
        # Start with base query
        query = self.db.query(Question).options(
            joinedload(Question.topic), joinedload(Question.course)
        )

        # Apply filters dynamically
        if topic_name:
            query = query.join(Topic).filter(Topic.topic_name.ilike(f"%{topic_name}%"))

        if difficulty:
            query = query.filter(Question.difficulty == difficulty)

        if year:
            query = query.filter(Question.year == year)

        if exam_type:
            query = query.filter(Question.exam_type == exam_type)

        if course_id:
            query = query.filter(Question.course_id == course_id)

        # Order by year descending, then by question_id
        query = query.order_by(Question.year.desc(), Question.question_id)

        # Apply pagination
        query = query.limit(limit).offset(offset)

        # Execute query
        questions = query.all()

        # Format results
        return [
            {
                "question_id": q.question_id,
                "question_text": q.question_text,
                "difficulty": q.difficulty,
                "marks": q.marks,
                "year": q.year,
                "exam_type": q.exam_type,
                "topic_id": q.topic_id,
                "topic_name": q.topic.topic_name if q.topic else None,
                "course_id": q.course_id,
                "course_title": q.course.course_title if q.course else None,
            }
            for q in questions
        ]

    def search_resources(
        self,
        resource_type: str | None = None,
        year: int | None = None,
        course_id: int | None = None,
        topic_id: int | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        """
        Search resources with filters

        Args:
            resource_type: Filter by type (Video, PDF, Article, Tutorial, Other)
            year: Filter by academic year
            course_id: Filter by course
            topic_id: Filter by topic
            limit: Maximum results
            offset: Pagination offset

        Returns:
            List of resource dictionaries

        Learning Note:
        - Resources can be filtered by type, year, and course
        - Useful for browsing learning materials
        """
        # Start with base query
        query = self.db.query(Resource).options(
            joinedload(Resource.course), joinedload(Resource.topic)
        )

        # Apply filters
        if resource_type:
            query = query.filter(Resource.resource_type == resource_type)

        if year:
            query = query.filter(Resource.year_published == year)

        if course_id:
            query = query.filter(Resource.course_id == course_id)

        if topic_id:
            query = query.filter(Resource.topic_id == topic_id)

        # Order by year descending
        query = query.order_by(Resource.year_published.desc(), Resource.resource_id)

        # Apply pagination
        query = query.limit(limit).offset(offset)

        # Execute query
        resources = query.all()

        # Format results
        return [
            {
                "resource_id": r.resource_id,
                "title": r.title,
                "resource_type": r.resource_type,
                "url": r.url,
                "year": r.year_published,
                "course_id": r.course_id,
                "course_title": r.course.course_title if r.course else None,
                "topic_id": r.topic_id,
                "topic_name": r.topic.topic_name if r.topic else None,
                "description": r.description,
            }
            for r in resources
        ]

    def search_topics(
        self, topic_name: str | None = None, course_id: int | None = None, limit: int = 50
    ) -> list[dict[str, Any]]:
        """
        Search topics

        Args:
            topic_name: Partial match on topic name
            course_id: Filter by course
            limit: Maximum results

        Returns:
            List of topics with question counts

        Learning Note:
        - Uses aggregate function to count questions per topic
        - GROUP BY to aggregate data
        """
        query = (
            self.db.query(
                Topic.topic_id,
                Topic.topic_name,
                Topic.course_id,
                Course.course_title,
                func.count(Question.question_id).label("question_count"),
            )
            .join(Course, Topic.course_id == Course.course_id)
            .outerjoin(Question, Topic.topic_id == Question.topic_id)
            .group_by(Topic.topic_id, Topic.topic_name, Topic.course_id, Course.course_title)
        )

        # Apply filters
        if topic_name:
            query = query.filter(Topic.topic_name.ilike(f"%{topic_name}%"))

        if course_id:
            query = query.filter(Topic.course_id == course_id)

        # Order by question count descending
        query = query.order_by(func.count(Question.question_id).desc())

        # Limit results
        query = query.limit(limit)

        # Execute and format
        results = query.all()

        return [
            {
                "topic_id": row.topic_id,
                "topic_name": row.topic_name,
                "course_id": row.course_id,
                "course_title": row.course_title,
                "question_count": row.question_count,
            }
            for row in results
        ]

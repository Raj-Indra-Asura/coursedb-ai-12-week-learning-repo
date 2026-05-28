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
- topic: Partial match on topic name
- difficulty: exact match (easy, medium, hard)
- academic_year: exact match
- question_type: exact match (mcq, short, long, problem)
- marks_min, marks_max: range filter

TODO (Week 6):
1. Implement dynamic query builder
2. Add filter validation
3. Implement pagination
4. Test with various filter combinations
5. Add sorting options
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional


class SQLSearchService:
    """Service for SQL-based search operations"""

    def __init__(self, db: Session):
        self.db = db

    # TODO (Week 6): Implement search methods

    def search_questions(
        self,
        topic: Optional[str] = None,
        difficulty: Optional[str] = None,
        academic_year: Optional[str] = None,
        question_type: Optional[str] = None,
        marks_min: Optional[int] = None,
        marks_max: Optional[int] = None,
        limit: int = 20,
        offset: int = 0
    ):
        """
        Search questions with SQL filters

        Example SQL (generated):
        SELECT q.* FROM questions q
        JOIN question_topics qt ON q.question_id = qt.question_id
        JOIN topics t ON qt.topic_id = t.topic_id
        JOIN resources r ON q.resource_id = r.resource_id
        WHERE t.topic_name ILIKE '%normalization%'
        AND q.difficulty = 'medium'
        AND r.academic_year = '2023'
        LIMIT 20 OFFSET 0;
        """
        # TODO (Week 6): Implement query logic
        pass

    def search_resources(
        self,
        resource_type: Optional[str] = None,
        academic_year: Optional[str] = None,
        course_id: Optional[int] = None,
        limit: int = 20,
        offset: int = 0
    ):
        """Search resources with filters"""
        # TODO (Week 6): Implement resource search
        pass

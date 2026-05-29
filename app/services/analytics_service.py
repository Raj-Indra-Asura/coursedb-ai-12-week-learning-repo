"""Analytics service.

Week 6: SQL Queries, Views, Triggers, Constraints.

Generates analytical insights from academic data using SQLAlchemy ORM
aggregate queries. All queries are parameterised by the ORM layer; no raw
string interpolation is used.

Learning Objectives:
    - Use SQL aggregate functions (``COUNT``, ``GROUP BY``).
    - Translate analytical questions into ORM queries.
    - Generate statistical summaries for dashboards.

Analytics Provided:
    1. Topic frequency distribution.
    2. Year-wise topic trends.
    3. Difficulty distribution.
    4. Resource type summary.
"""

from __future__ import annotations

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.models import Question, Resource, Topic


class AnalyticsService:
    """Service for analytical queries over the academic dataset."""

    def __init__(self, db: Session) -> None:
        """Store the database session.

        Args:
            db: Active SQLAlchemy session.
        """
        self.db = db

    def get_topic_frequency(self) -> list[dict]:
        """Return the number of questions associated with each topic.

        Topics are matched to questions through the ``topic_id`` foreign key.
        Results are ordered from most to least frequent.

        Returns:
            A list of ``{"topic_name": str, "question_count": int}`` dicts,
            ordered by descending ``question_count``.
        """
        rows = (
            self.db.query(
                Topic.topic_name.label("topic_name"),
                func.count(Question.question_id).label("question_count"),
            )
            .join(Question, Question.topic_id == Topic.topic_id)
            .group_by(Topic.topic_name)
            .order_by(func.count(Question.question_id).desc())
            .all()
        )
        return [
            {"topic_name": row.topic_name, "question_count": int(row.question_count)}
            for row in rows
        ]

    def get_year_wise_trends(self) -> list[dict]:
        """Return the distribution of questions per topic per year.

        Returns:
            A list of ``{"year": int, "topic_name": str, "question_count": int}``
            dicts, ordered by year then descending count.
        """
        rows = (
            self.db.query(
                Question.year.label("year"),
                Topic.topic_name.label("topic_name"),
                func.count(Question.question_id).label("question_count"),
            )
            .join(Topic, Question.topic_id == Topic.topic_id)
            .filter(Question.year.isnot(None))
            .group_by(Question.year, Topic.topic_name)
            .order_by(Question.year, func.count(Question.question_id).desc())
            .all()
        )
        return [
            {
                "year": int(row.year),
                "topic_name": row.topic_name,
                "question_count": int(row.question_count),
            }
            for row in rows
        ]

    def get_difficulty_distribution(self) -> dict[str, int]:
        """Return the number of questions per difficulty level.

        Returns:
            A mapping of difficulty label (``"easy"``, ``"medium"``,
            ``"hard"``) to question count. Levels with no questions are
            reported as ``0``.
        """
        rows = (
            self.db.query(
                Question.difficulty.label("difficulty"),
                func.count(Question.question_id).label("count"),
            )
            .filter(Question.difficulty.isnot(None))
            .group_by(Question.difficulty)
            .all()
        )
        distribution: dict[str, int] = {"easy": 0, "medium": 0, "hard": 0}
        for row in rows:
            distribution[row.difficulty] = int(row.count)
        return distribution

    def get_resource_summary(self) -> dict:
        """Return summary statistics for resources.

        Returns:
            A dict with the total resource count and a per-``resource_type``
            breakdown::

                {
                    "total_resources": 12,
                    "by_type": {"note": 5, "textbook": 3, ...},
                }
        """
        total = self.db.query(func.count(Resource.resource_id)).scalar() or 0
        rows = (
            self.db.query(
                Resource.resource_type.label("resource_type"),
                func.count(Resource.resource_id).label("count"),
            )
            .filter(Resource.resource_type.isnot(None))
            .group_by(Resource.resource_type)
            .all()
        )
        by_type = {row.resource_type: int(row.count) for row in rows}
        return {"total_resources": int(total), "by_type": by_type}

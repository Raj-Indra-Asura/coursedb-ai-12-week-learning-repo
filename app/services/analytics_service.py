"""
Analytics Service

Week 6: SQL Queries, Views, Triggers, Constraints

Generates analytical insights from academic data.

Learning Objectives:
- Use SQL aggregate functions
- Query database views
- Generate statistical summaries
- Optimize analytical queries

Analytics Provided:
1. Topic frequency distribution
2. Year-wise topic trends
3. Difficulty distribution
4. Resource type distribution
5. Question type distribution

TODO (Week 6):
1. Query views for analytics
2. Calculate aggregates
3. Format data for visualization
4. Add caching for expensive queries
"""

from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Dict, List


class AnalyticsService:
    """Service for analytical queries"""

    def __init__(self, db: Session):
        self.db = db

    # TODO (Week 6): Implement analytics methods

    def get_topic_frequency(self) -> List[Dict]:
        """
        Get question count per topic

        Uses view: topic_question_frequency

        Returns:
        [
            {"topic_name": "Normalization", "question_count": 25},
            {"topic_name": "Indexing", "question_count": 18},
            ...
        ]
        """
        # TODO (Week 6): Query topic_question_frequency view
        pass

    def get_year_wise_trends(self) -> List[Dict]:
        """
        Get topic distribution by year

        Uses view: year_wise_topic_frequency
        """
        # TODO (Week 6): Query year_wise_topic_frequency view
        pass

    def get_difficulty_distribution(self) -> Dict[str, int]:
        """
        Get count of questions by difficulty

        Returns:
        {
            "easy": 15,
            "medium": 30,
            "hard": 10
        }
        """
        # TODO (Week 6): Implement difficulty aggregation
        pass

    def get_resource_summary(self) -> Dict:
        """Get summary statistics for resources"""
        # TODO (Week 6): Implement resource summary
        pass

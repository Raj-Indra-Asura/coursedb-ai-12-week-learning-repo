"""
Topics API Endpoints

Week 6: SQL Queries, Views, Triggers, Constraints

Handles operations for topics (hierarchical DBMS concepts).

Database Table: topics
- topic_id (PK)
- course_id (FK)
- parent_topic_id (FK, self-referencing for hierarchy)
- topic_name
- description

Learning Notes:
- Topics are hierarchical (e.g., "DBMS" > "Normalization" > "3NF")
- Self-referencing foreign key enables tree structure
- Consider recursive queries for subtopic retrieval

TODO (Week 6):
1. Implement topic CRUD operations
2. Handle hierarchical relationships
3. Add endpoint to get subtopics
4. Add endpoint to get topic tree
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter(prefix="/topics", tags=["topics"])

# TODO (Week 6): Implement topic endpoints
# - GET /topics - list all topics
# - GET /topics/{id} - get topic by ID
# - GET /topics/{id}/subtopics - get child topics
# - POST /topics - create new topic
# - PUT /topics/{id} - update topic
# - DELETE /topics/{id} - delete topic

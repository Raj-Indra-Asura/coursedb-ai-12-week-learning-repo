"""
Questions API Endpoints

Week 6: SQL Queries, Views, Triggers, Constraints

Handles previous-year exam questions with topic mapping.

Database Tables:
- questions (question_id, resource_id, question_text, marks, difficulty, question_type)
- question_topics (M:N relationship with topics)

Learning Notes:
- Questions have many-to-many relationship with topics
- Audit trigger logs all question inserts/updates
- Difficulty: easy, medium, hard
- Question types: mcq, short, long, problem

TODO (Week 6):
1. Implement question CRUD
2. Handle question-topic relationships
3. Add filtering by difficulty, topic, year
4. Test audit trigger behavior
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

router = APIRouter(prefix="/questions", tags=["questions"])

# TODO (Week 6): Implement question endpoints
# - GET /questions - list questions with filters
# - GET /questions/{id} - get question by ID
# - POST /questions - create question (triggers audit log)
# - PUT /questions/{id} - update question (triggers audit log)
# - DELETE /questions/{id} - delete question
# - GET /questions?difficulty=medium&topic=normalization - filter questions
# - POST /questions/{id}/topics - assign topics to question

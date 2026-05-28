"""
Resources API Endpoints

Week 6: SQL Queries, Views, Triggers, Constraints

Handles academic resources (notes, textbooks, question papers).

Database Table: resources
- resource_id (PK)
- course_id (FK)
- title
- resource_type (notes, question_paper, textbook, assignment, slides)
- source_name
- academic_year
- file_path
- created_at

TODO (Week 6):
1. Implement resource CRUD
2. Add filtering by type, year, course
3. Handle file uploads (Week 11)
4. Link resources to chapters and tags
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

router = APIRouter(prefix="/resources", tags=["resources"])

# TODO (Week 6): Implement resource endpoints
# - GET /resources - list resources with filters
# - GET /resources/{id} - get resource by ID
# - POST /resources - create resource
# - PUT /resources/{id} - update resource
# - DELETE /resources/{id} - delete resource
# - GET /resources?type=question_paper&year=2023 - filter resources

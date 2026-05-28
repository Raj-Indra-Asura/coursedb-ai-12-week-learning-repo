"""
Courses API Endpoints

Week 6: SQL Queries, Views, Triggers, Constraints

This module handles CRUD operations for courses.

Learning Objectives:
- Implement RESTful API patterns
- Use SQLAlchemy ORM for database operations
- Handle request validation with Pydantic
- Implement error handling

Database Table: courses
- course_id (PK)
- course_code
- course_title
- semester
- credit

TODO (Week 6):
1. Create Pydantic schemas for request/response
2. Implement GET /courses (list all courses)
3. Implement GET /courses/{id} (get single course)
4. Implement POST /courses (create course)
5. Implement PUT /courses/{id} (update course)
6. Implement DELETE /courses/{id} (delete course)
7. Add proper error handling
8. Add input validation
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
# TODO (Week 6): Import models and schemas
# from app.db.models import Course
# from app.db.database import get_db
# from app.schemas.course import CourseCreate, CourseUpdate, CourseResponse

router = APIRouter(prefix="/courses", tags=["courses"])


# TODO (Week 6): Implement endpoints
# @router.get("/", response_model=List[CourseResponse])
# async def list_courses(db: Session = Depends(get_db)):
#     """List all courses"""
#     pass
#
# @router.get("/{course_id}", response_model=CourseResponse)
# async def get_course(course_id: int, db: Session = Depends(get_db)):
#     """Get a specific course by ID"""
#     pass
#
# @router.post("/", response_model=CourseResponse)
# async def create_course(course: CourseCreate, db: Session = Depends(get_db)):
#     """Create a new course"""
#     pass
#
# @router.put("/{course_id}", response_model=CourseResponse)
# async def update_course(course_id: int, course: CourseUpdate, db: Session = Depends(get_db)):
#     """Update an existing course"""
#     pass
#
# @router.delete("/{course_id}")
# async def delete_course(course_id: int, db: Session = Depends(get_db)):
#     """Delete a course"""
#     pass

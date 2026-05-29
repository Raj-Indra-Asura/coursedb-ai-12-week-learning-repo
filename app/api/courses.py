"""
Courses API Endpoints

Week 6: SQL Queries, Views, Triggers, Constraints

This module implements complete CRUD operations for courses.

Learning Objectives:
- Implement RESTful API patterns
- Use SQLAlchemy ORM for database operations
- Handle request validation with Pydantic
- Implement proper error handling
- Return appropriate HTTP status codes

Database Table: courses
- course_id (PK)
- course_code (UNIQUE)
- course_title
- semester
- credit
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Course
from app.schemas import CourseCreate, CourseResponse, CourseUpdate

router = APIRouter(prefix="/api/courses", tags=["courses"])


@router.get("/", response_model=list[CourseResponse])
async def list_courses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    List all courses with pagination

    Learning Objectives:
    - Implement pagination (skip, limit)
    - Query all records from database
    - Return list of results

    Args:
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return
        db: Database session (injected)

    Returns:
        List of courses

    Example:
        GET /api/courses?skip=0&limit=10
    """
    courses = db.query(Course).offset(skip).limit(limit).all()
    return courses


@router.get("/{course_id}", response_model=CourseResponse)
async def get_course(course_id: int, db: Session = Depends(get_db)):
    """
    Get a specific course by ID

    Learning Objectives:
    - Query single record by primary key
    - Handle 404 Not Found errors
    - Use HTTPException for errors

    Args:
        course_id: Course ID to retrieve
        db: Database session

    Returns:
        Course details

    Raises:
        HTTPException 404: Course not found
    """
    course = db.query(Course).filter(Course.course_id == course_id).first()

    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Course with ID {course_id} not found"
        )

    return course


@router.post("/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
async def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    """
    Create a new course

    Learning Objectives:
    - Insert new record into database
    - Handle UNIQUE constraint violations
    - Return 201 Created status
    - Use db.commit() and db.refresh()

    Args:
        course: Course data (validated by Pydantic)
        db: Database session

    Returns:
        Created course with generated ID

    Raises:
        HTTPException 400: Duplicate course_code

    Example Request Body:
    {
        "course_code": "CS201",
        "course_title": "Database Management Systems",
        "semester": "Fall 2024",
        "credit": 4
    }
    """
    try:
        # Create new Course instance from Pydantic model
        db_course = Course(**course.dict())

        # Add to session and commit
        db.add(db_course)
        db.commit()
        db.refresh(db_course)  # Get auto-generated ID and timestamps

        return db_course

    except IntegrityError:
        db.rollback()
        # UNIQUE constraint violation (duplicate course_code)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Course code '{course.course_code}' already exists",
        )


@router.put("/{course_id}", response_model=CourseResponse)
async def update_course(course_id: int, course: CourseUpdate, db: Session = Depends(get_db)):
    """
    Update an existing course

    Learning Objectives:
    - Update record in database
    - Handle partial updates (only provided fields)
    - Check if record exists before updating

    Args:
        course_id: ID of course to update
        course: Updated course data (all fields optional)
        db: Database session

    Returns:
        Updated course

    Raises:
        HTTPException 404: Course not found
        HTTPException 400: Duplicate course_code
    """
    # Find existing course
    db_course = db.query(Course).filter(Course.course_id == course_id).first()

    if not db_course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Course with ID {course_id} not found"
        )

    try:
        # Update only provided fields
        update_data = course.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_course, field, value)

        db.commit()
        db.refresh(db_course)

        return db_course

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Course code already exists"
        )


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(course_id: int, db: Session = Depends(get_db)):
    """
    Delete a course

    Learning Objectives:
    - Delete record from database
    - Handle cascade deletes (topics, questions deleted too)
    - Return 204 No Content on success

    Args:
        course_id: ID of course to delete
        db: Database session

    Returns:
        No content (204 status)

    Raises:
        HTTPException 404: Course not found

    Note:
        This will CASCADE delete all related topics and questions!
        In production, you might want soft deletes instead.
    """
    db_course = db.query(Course).filter(Course.course_id == course_id).first()

    if not db_course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Course with ID {course_id} not found"
        )

    db.delete(db_course)
    db.commit()

    return None  # 204 No Content


@router.get("/{course_id}/topics", response_model=list[dict])
async def get_course_topics(course_id: int, db: Session = Depends(get_db)):
    """
    Get all topics for a specific course

    Learning Objectives:
    - Use relationships (course.topics)
    - Filter by foreign key
    - JOIN tables implicitly

    Args:
        course_id: Course ID
        db: Database session

    Returns:
        List of topics for the course

    Raises:
        HTTPException 404: Course not found
    """
    course = db.query(Course).filter(Course.course_id == course_id).first()

    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Course with ID {course_id} not found"
        )

    # Use relationship to get topics (SQLAlchemy automatically JOINs)
    topics = course.topics

    return [
        {
            "topic_id": t.topic_id,
            "topic_name": t.topic_name,
            "description": t.description,
            "week_number": t.week_number,
        }
        for t in topics
    ]


"""
Learning Notes:

1. **CRUD Pattern**:
   - Create: POST with 201 Created
   - Read: GET (list + detail)
   - Update: PUT with partial updates
   - Delete: DELETE with 204 No Content

2. **HTTP Status Codes**:
   - 200: Success (GET, PUT)
   - 201: Created (POST)
   - 204: No Content (DELETE)
   - 400: Bad Request (validation error)
   - 404: Not Found
   - 500: Internal Server Error

3. **Error Handling**:
   - Use HTTPException for client errors
   - Catch IntegrityError for constraint violations
   - Always rollback on error

4. **Database Operations**:
   - db.add(): Add new record
   - db.commit(): Save changes
   - db.refresh(): Get auto-generated fields
   - db.rollback(): Undo changes on error
   - db.delete(): Delete record

5. **Pydantic Validation**:
   - CourseCreate: All required fields
   - CourseUpdate: All optional fields (partial update)
   - CourseResponse: Includes ID and timestamps

6. **Relationships**:
   - course.topics: Automatically JOINs via relationship
   - CASCADE delete: Deleting course deletes topics

Testing:
```bash
# Create course
curl -X POST http://localhost:8000/api/courses \
  -H "Content-Type: application/json" \
  -d '{"course_code":"CS201","course_title":"DBMS","credit":4}'

# List courses
curl http://localhost:8000/api/courses

# Get course
curl http://localhost:8000/api/courses/1

# Update course
curl -X PUT http://localhost:8000/api/courses/1 \
  -H "Content-Type: application/json" \
  -d '{"course_title":"Advanced DBMS"}'

# Delete course
curl -X DELETE http://localhost:8000/api/courses/1
```

Next Steps:
- Implement similar CRUD for topics, questions, resources
- Add filtering and search
- Add authentication (Week 11)
"""
#     """Update an existing course"""
#     pass
#
# @router.delete("/{course_id}")
# async def delete_course(course_id: int, db: Session = Depends(get_db)):
#     """Delete a course"""
#     pass

"""
Topics API Endpoints
CRUD operations for topics

Learning objectives:
- RESTful API design patterns
- Relationship handling (topic belongs to course)
- Query parameter filtering
- Foreign key constraints
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db.database import get_db
from app.db.models import Topic, Course
from app.schemas import TopicCreate, TopicUpdate, TopicResponse

router = APIRouter(
    prefix="/api/topics",
    tags=["topics"]
)


@router.get("/", response_model=List[TopicResponse])
async def list_topics(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Max records to return"),
    course_id: Optional[int] = Query(None, description="Filter by course ID"),
    week_number: Optional[int] = Query(None, ge=1, le=12, description="Filter by week number"),
    db: Session = Depends(get_db)
):
    """
    List all topics with optional filtering.

    Query Parameters:
    - skip: Pagination offset
    - limit: Maximum number of results
    - course_id: Filter topics by specific course
    - week_number: Filter topics by week number

    Returns:
        List of topics

    Example:
        GET /api/topics?course_id=1&week_number=3
    """
    query = db.query(Topic)

    # Apply filters
    if course_id is not None:
        query = query.filter(Topic.course_id == course_id)
    if week_number is not None:
        query = query.filter(Topic.week_number == week_number)

    topics = query.offset(skip).limit(limit).all()
    return topics


@router.get("/{topic_id}", response_model=TopicResponse)
async def get_topic(
    topic_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific topic by ID.

    Args:
        topic_id: Topic identifier

    Returns:
        Topic details with related course information

    Raises:
        404: Topic not found

    Example:
        GET /api/topics/5
    """
    topic = db.query(Topic).filter(Topic.topic_id == topic_id).first()

    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Topic with id {topic_id} not found"
        )

    return topic


@router.post("/", response_model=TopicResponse, status_code=status.HTTP_201_CREATED)
async def create_topic(
    topic: TopicCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new topic.

    Request Body:
        - course_id: Foreign key to courses table (required)
        - topic_name: Name of the topic (required)
        - week_number: Week when topic is covered (1-12, required)

    Returns:
        Created topic with generated topic_id

    Raises:
        400: Invalid course_id (foreign key violation)
        500: Database error

    Example:
        POST /api/topics
        {
            "course_id": 1,
            "topic_name": "ER Modeling",
            "week_number": 3
        }
    """
    try:
        # Verify course exists
        course = db.query(Course).filter(Course.course_id == topic.course_id).first()
        if not course:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Course with id {topic.course_id} does not exist"
            )

        # Create new topic
        db_topic = Topic(**topic.dict())
        db.add(db_topic)
        db.commit()
        db.refresh(db_topic)
        return db_topic

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Database constraint violation: {str(e.orig)}"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create topic: {str(e)}"
        )


@router.put("/{topic_id}", response_model=TopicResponse)
async def update_topic(
    topic_id: int,
    topic: TopicUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing topic (partial update supported).

    Args:
        topic_id: Topic identifier

    Request Body (all fields optional):
        - course_id: New course assignment
        - topic_name: New topic name
        - week_number: New week number

    Returns:
        Updated topic

    Raises:
        404: Topic not found
        400: Invalid course_id or constraint violation

    Example:
        PUT /api/topics/5
        {
            "topic_name": "Advanced ER Modeling",
            "week_number": 4
        }
    """
    # Fetch existing topic
    db_topic = db.query(Topic).filter(Topic.topic_id == topic_id).first()

    if not db_topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Topic with id {topic_id} not found"
        )

    try:
        # Update only provided fields
        update_data = topic.dict(exclude_unset=True)

        # If updating course_id, verify new course exists
        if "course_id" in update_data:
            course = db.query(Course).filter(Course.course_id == update_data["course_id"]).first()
            if not course:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Course with id {update_data['course_id']} does not exist"
                )

        for field, value in update_data.items():
            setattr(db_topic, field, value)

        db.commit()
        db.refresh(db_topic)
        return db_topic

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Database constraint violation: {str(e.orig)}"
        )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update topic: {str(e)}"
        )


@router.delete("/{topic_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_topic(
    topic_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a topic.

    Args:
        topic_id: Topic identifier

    Returns:
        204 No Content on success

    Raises:
        404: Topic not found

    Note:
        This will also affect related questions (based on ON DELETE behavior):
        - Questions referencing this topic will have topic_id set to NULL (ON DELETE SET NULL)

    Example:
        DELETE /api/topics/5
    """
    db_topic = db.query(Topic).filter(Topic.topic_id == topic_id).first()

    if not db_topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Topic with id {topic_id} not found"
        )

    try:
        db.delete(db_topic)
        db.commit()
        return None  # 204 No Content

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete topic: {str(e)}"
        )


@router.get("/{topic_id}/questions")
async def get_topic_questions(
    topic_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all questions for a specific topic.

    Args:
        topic_id: Topic identifier

    Returns:
        List of questions related to this topic

    Raises:
        404: Topic not found

    Example:
        GET /api/topics/5/questions
    """
    # Verify topic exists
    topic = db.query(Topic).filter(Topic.topic_id == topic_id).first()

    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Topic with id {topic_id} not found"
        )

    # Return questions through relationship
    return topic.questions

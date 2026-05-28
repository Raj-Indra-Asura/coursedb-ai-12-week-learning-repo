"""
Questions API Endpoints
CRUD operations for exam questions

Learning objectives:
- Complex filtering with multiple query parameters
- Foreign key validation for multiple relationships
- Handling optional relationships (course, topic)
- Search functionality with ILIKE
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_, and_

from app.db.database import get_db
from app.db.models import Question, Course, Topic
from app.schemas import QuestionCreate, QuestionUpdate, QuestionResponse

router = APIRouter(
    prefix="/api/questions",
    tags=["questions"]
)


@router.get("/", response_model=List[QuestionResponse])
async def list_questions(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Max records to return"),
    course_id: Optional[int] = Query(None, description="Filter by course ID"),
    topic_id: Optional[int] = Query(None, description="Filter by topic ID"),
    year: Optional[int] = Query(None, ge=2010, le=2030, description="Filter by year"),
    exam_type: Optional[str] = Query(None, description="Filter by exam type (midterm, final, quiz, assignment)"),
    difficulty: Optional[str] = Query(None, description="Filter by difficulty (easy, medium, hard)"),
    search: Optional[str] = Query(None, description="Search in question text"),
    db: Session = Depends(get_db)
):
    """
    List all questions with extensive filtering options.

    Query Parameters:
    - skip: Pagination offset
    - limit: Maximum number of results
    - course_id: Filter by specific course
    - topic_id: Filter by specific topic
    - year: Filter by exam year
    - exam_type: Filter by exam type
    - difficulty: Filter by difficulty level
    - search: Search for text in question_text

    Returns:
        List of questions matching filters

    Example:
        GET /api/questions?difficulty=hard&year=2023&search=normalization
    """
    query = db.query(Question)

    # Apply filters
    if course_id is not None:
        query = query.filter(Question.course_id == course_id)
    if topic_id is not None:
        query = query.filter(Question.topic_id == topic_id)
    if year is not None:
        query = query.filter(Question.year == year)
    if exam_type is not None:
        query = query.filter(Question.exam_type == exam_type)
    if difficulty is not None:
        query = query.filter(Question.difficulty == difficulty)
    if search is not None:
        # Case-insensitive search in question text
        query = query.filter(Question.question_text.ilike(f"%{search}%"))

    questions = query.offset(skip).limit(limit).all()
    return questions


@router.get("/{question_id}", response_model=QuestionResponse)
async def get_question(
    question_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific question by ID.

    Args:
        question_id: Question identifier

    Returns:
        Question details with related course and topic information

    Raises:
        404: Question not found

    Example:
        GET /api/questions/42
    """
    question = db.query(Question).filter(Question.question_id == question_id).first()

    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Question with id {question_id} not found"
        )

    return question


@router.post("/", response_model=QuestionResponse, status_code=status.HTTP_201_CREATED)
async def create_question(
    question: QuestionCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new question.

    Request Body:
        - course_id: Foreign key to courses table (required)
        - topic_id: Foreign key to topics table (optional)
        - question_text: Full text of the question (required)
        - course_code: Redundant denormalized field for learning (optional)
        - topic_name: Redundant denormalized field for learning (optional)
        - year: Exam year (required, 2010-2030)
        - exam_type: Type of exam (required: midterm, final, quiz, assignment)
        - difficulty: Difficulty level (required: easy, medium, hard)
        - marks: Points awarded (required, > 0)

    Returns:
        Created question with generated question_id

    Raises:
        400: Invalid course_id or topic_id, or constraint violation
        500: Database error

    Example:
        POST /api/questions
        {
            "course_id": 1,
            "topic_id": 5,
            "question_text": "Explain the normalization process up to BCNF.",
            "year": 2023,
            "exam_type": "final",
            "difficulty": "hard",
            "marks": 10
        }
    """
    try:
        # Verify course exists
        course = db.query(Course).filter(Course.course_id == question.course_id).first()
        if not course:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Course with id {question.course_id} does not exist"
            )

        # Verify topic exists (if provided)
        if question.topic_id is not None:
            topic = db.query(Topic).filter(Topic.topic_id == question.topic_id).first()
            if not topic:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Topic with id {question.topic_id} does not exist"
                )

        # Create new question
        db_question = Question(**question.dict())
        db.add(db_question)
        db.commit()
        db.refresh(db_question)
        return db_question

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
            detail=f"Failed to create question: {str(e)}"
        )


@router.put("/{question_id}", response_model=QuestionResponse)
async def update_question(
    question_id: int,
    question: QuestionUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing question (partial update supported).

    Args:
        question_id: Question identifier

    Request Body (all fields optional):
        - course_id: New course assignment
        - topic_id: New topic assignment
        - question_text: Updated question text
        - year: Updated year
        - exam_type: Updated exam type
        - difficulty: Updated difficulty
        - marks: Updated marks

    Returns:
        Updated question

    Raises:
        404: Question not found
        400: Invalid course_id or topic_id, or constraint violation

    Example:
        PUT /api/questions/42
        {
            "difficulty": "medium",
            "marks": 8
        }
    """
    # Fetch existing question
    db_question = db.query(Question).filter(Question.question_id == question_id).first()

    if not db_question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Question with id {question_id} not found"
        )

    try:
        # Update only provided fields
        update_data = question.dict(exclude_unset=True)

        # If updating course_id, verify new course exists
        if "course_id" in update_data:
            course = db.query(Course).filter(Course.course_id == update_data["course_id"]).first()
            if not course:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Course with id {update_data['course_id']} does not exist"
                )

        # If updating topic_id, verify new topic exists (allow None)
        if "topic_id" in update_data and update_data["topic_id"] is not None:
            topic = db.query(Topic).filter(Topic.topic_id == update_data["topic_id"]).first()
            if not topic:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Topic with id {update_data['topic_id']} does not exist"
                )

        for field, value in update_data.items():
            setattr(db_question, field, value)

        db.commit()
        db.refresh(db_question)
        return db_question

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
            detail=f"Failed to update question: {str(e)}"
        )


@router.delete("/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_question(
    question_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a question.

    Args:
        question_id: Question identifier

    Returns:
        204 No Content on success

    Raises:
        404: Question not found

    Example:
        DELETE /api/questions/42
    """
    db_question = db.query(Question).filter(Question.question_id == question_id).first()

    if not db_question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Question with id {question_id} not found"
        )

    try:
        db.delete(db_question)
        db.commit()
        return None  # 204 No Content

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete question: {str(e)}"
        )


@router.get("/search/by-topic/{topic_name}")
async def search_questions_by_topic_name(
    topic_name: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    Search questions by topic name (case-insensitive partial match).

    Args:
        topic_name: Topic name to search for

    Returns:
        List of questions matching the topic name

    Example:
        GET /api/questions/search/by-topic/normalization
    """
    questions = db.query(Question).filter(
        Question.topic_name.ilike(f"%{topic_name}%")
    ).offset(skip).limit(limit).all()

    return questions


@router.get("/stats/by-year")
async def get_questions_by_year(db: Session = Depends(get_db)):
    """
    Get question count grouped by year.

    Returns:
        List of dictionaries with year and count

    Example:
        GET /api/questions/stats/by-year
        Response: [{"year": 2023, "count": 15}, {"year": 2022, "count": 12}, ...]
    """
    from sqlalchemy import func

    results = db.query(
        Question.year,
        func.count(Question.question_id).label('count')
    ).group_by(Question.year).order_by(Question.year.desc()).all()

    return [{"year": year, "count": count} for year, count in results]


@router.get("/stats/by-difficulty")
async def get_questions_by_difficulty(db: Session = Depends(get_db)):
    """
    Get question count grouped by difficulty.

    Returns:
        List of dictionaries with difficulty and count

    Example:
        GET /api/questions/stats/by-difficulty
        Response: [{"difficulty": "hard", "count": 20}, {"difficulty": "medium", "count": 35}, ...]
    """
    from sqlalchemy import func

    results = db.query(
        Question.difficulty,
        func.count(Question.question_id).label('count')
    ).group_by(Question.difficulty).all()

    return [{"difficulty": difficulty, "count": count} for difficulty, count in results]

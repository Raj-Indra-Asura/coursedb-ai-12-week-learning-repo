"""
Analytics API Endpoints
Dashboard data and insights for CourseDB-AI

Learning objectives:
- Aggregate functions (COUNT, SUM, AVG, GROUP BY)
- Multi-table joins for analytics
- Data visualization preparation
- Query optimization for reporting
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_

from app.db.database import get_db
from app.db.models import Question, Topic, Course, Resource

router = APIRouter(
    prefix="/api/analytics",
    tags=["analytics"]
)


@router.get("/overview")
async def get_overview_stats(db: Session = Depends(get_db)):
    """
    Get overall system statistics.

    Returns:
        Dictionary with counts of all major entities

    Example:
        GET /api/analytics/overview
        Response: {
            "total_courses": 5,
            "total_topics": 42,
            "total_questions": 156,
            "total_resources": 89,
            "avg_questions_per_topic": 3.7
        }
    """
    total_courses = db.query(func.count(Course.course_id)).scalar()
    total_topics = db.query(func.count(Topic.topic_id)).scalar()
    total_questions = db.query(func.count(Question.question_id)).scalar()
    total_resources = db.query(func.count(Resource.resource_id)).scalar()

    # Calculate average questions per topic
    avg_questions_per_topic = (
        total_questions / total_topics if total_topics > 0 else 0
    )

    return {
        "total_courses": total_courses or 0,
        "total_topics": total_topics or 0,
        "total_questions": total_questions or 0,
        "total_resources": total_resources or 0,
        "avg_questions_per_topic": round(avg_questions_per_topic, 2)
    }


@router.get("/topic-frequency")
async def get_topic_frequency(
    limit: int = Query(20, ge=1, le=100, description="Max topics to return"),
    db: Session = Depends(get_db)
):
    """
    Get question count per topic, ordered by frequency.

    Query Parameters:
    - limit: Maximum number of topics to return

    Returns:
        List of topics with question counts

    Example:
        GET /api/analytics/topic-frequency?limit=10
        Response: [
            {"topic_id": 5, "topic_name": "Normalization", "question_count": 28, "course_title": "DBMS"},
            {"topic_id": 12, "topic_name": "Transactions", "question_count": 24, "course_title": "DBMS"}
        ]
    """
    results = db.query(
        Topic.topic_id,
        Topic.topic_name,
        Course.course_title,
        func.count(Question.question_id).label('question_count')
    ).join(
        Question, Topic.topic_id == Question.topic_id, isouter=True
    ).join(
        Course, Topic.course_id == Course.course_id
    ).group_by(
        Topic.topic_id, Topic.topic_name, Course.course_title
    ).order_by(
        desc('question_count')
    ).limit(limit).all()

    return [
        {
            "topic_id": topic_id,
            "topic_name": topic_name,
            "course_title": course_title,
            "question_count": question_count
        }
        for topic_id, topic_name, course_title, question_count in results
    ]


@router.get("/year-wise-trends")
async def get_year_wise_trends(
    start_year: Optional[int] = Query(None, ge=2010, le=2030),
    end_year: Optional[int] = Query(None, ge=2010, le=2030),
    db: Session = Depends(get_db)
):
    """
    Get topic distribution trends by academic year.

    Query Parameters:
    - start_year: Filter from this year (optional)
    - end_year: Filter to this year (optional)

    Returns:
        Year-wise breakdown of questions and topics

    Example:
        GET /api/analytics/year-wise-trends?start_year=2020&end_year=2024
    """
    query = db.query(
        Question.year,
        func.count(Question.question_id).label('question_count'),
        func.count(func.distinct(Question.topic_id)).label('unique_topics')
    )

    # Apply year filters
    if start_year:
        query = query.filter(Question.year >= start_year)
    if end_year:
        query = query.filter(Question.year <= end_year)

    results = query.group_by(Question.year).order_by(Question.year.desc()).all()

    return [
        {
            "year": year,
            "question_count": question_count,
            "unique_topics": unique_topics
        }
        for year, question_count, unique_topics in results
    ]


@router.get("/difficulty-distribution")
async def get_difficulty_distribution(
    course_id: Optional[int] = Query(None, description="Filter by course"),
    year: Optional[int] = Query(None, ge=2010, le=2030, description="Filter by year"),
    db: Session = Depends(get_db)
):
    """
    Get distribution of questions by difficulty level.

    Query Parameters:
    - course_id: Filter by specific course (optional)
    - year: Filter by specific year (optional)

    Returns:
        Difficulty distribution with counts and percentages

    Example:
        GET /api/analytics/difficulty-distribution?course_id=1
        Response: [
            {"difficulty": "hard", "count": 45, "percentage": 28.8},
            {"difficulty": "medium", "count": 78, "percentage": 50.0},
            {"difficulty": "easy", "count": 33, "percentage": 21.2}
        ]
    """
    query = db.query(
        Question.difficulty,
        func.count(Question.question_id).label('count')
    )

    # Apply filters
    if course_id:
        query = query.filter(Question.course_id == course_id)
    if year:
        query = query.filter(Question.year == year)

    results = query.group_by(Question.difficulty).all()

    # Calculate total and percentages
    total = sum(count for _, count in results)

    return [
        {
            "difficulty": difficulty,
            "count": count,
            "percentage": round((count / total * 100) if total > 0 else 0, 1)
        }
        for difficulty, count in results
    ]


@router.get("/exam-type-distribution")
async def get_exam_type_distribution(
    year: Optional[int] = Query(None, ge=2010, le=2030),
    db: Session = Depends(get_db)
):
    """
    Get distribution of questions by exam type.

    Query Parameters:
    - year: Filter by specific year (optional)

    Returns:
        Exam type distribution with counts

    Example:
        GET /api/analytics/exam-type-distribution?year=2023
    """
    query = db.query(
        Question.exam_type,
        func.count(Question.question_id).label('count')
    )

    if year:
        query = query.filter(Question.year == year)

    results = query.group_by(Question.exam_type).order_by(desc('count')).all()

    return [
        {"exam_type": exam_type, "count": count}
        for exam_type, count in results
    ]


@router.get("/resource-summary")
async def get_resource_summary(db: Session = Depends(get_db)):
    """
    Get summary statistics for resources.

    Returns:
        Resource counts by type, year distribution, and course breakdown

    Example:
        GET /api/analytics/resource-summary
        Response: {
            "by_type": [...],
            "by_year": [...],
            "by_course": [...]
        }
    """
    # Resources by type
    by_type = db.query(
        Resource.resource_type,
        func.count(Resource.resource_id).label('count')
    ).group_by(Resource.resource_type).all()

    # Resources by year
    by_year = db.query(
        Resource.year_published,
        func.count(Resource.resource_id).label('count')
    ).filter(
        Resource.year_published.isnot(None)
    ).group_by(
        Resource.year_published
    ).order_by(
        Resource.year_published.desc()
    ).all()

    # Resources by course
    by_course = db.query(
        Course.course_title,
        func.count(Resource.resource_id).label('count')
    ).join(
        Resource, Course.course_id == Resource.course_id, isouter=True
    ).group_by(
        Course.course_title
    ).all()

    return {
        "by_type": [
            {"resource_type": rt, "count": count}
            for rt, count in by_type
        ],
        "by_year": [
            {"academic_year": year, "count": count}
            for year, count in by_year
        ],
        "by_course": [
            {"course_title": course, "count": count}
            for course, count in by_course
        ]
    }


@router.get("/topic-coverage")
async def get_topic_coverage(
    course_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Get topic coverage analysis showing which topics have questions/resources.

    Query Parameters:
    - course_id: Filter by specific course (optional)

    Returns:
        Topics with their question and resource counts

    Example:
        GET /api/analytics/topic-coverage?course_id=1
    """
    query = db.query(
        Topic.topic_id,
        Topic.topic_name,
        Course.course_title,
        func.count(func.distinct(Question.question_id)).label('question_count'),
        func.count(func.distinct(Resource.resource_id)).label('resource_count')
    ).join(
        Course, Topic.course_id == Course.course_id
    ).join(
        Question, Topic.topic_id == Question.topic_id, isouter=True
    ).join(
        Resource, Topic.course_id == Resource.course_id, isouter=True
    )

    if course_id:
        query = query.filter(Topic.course_id == course_id)

    results = query.group_by(
        Topic.topic_id, Topic.topic_name, Course.course_title
    ).order_by(
        desc('question_count')
    ).all()

    return [
        {
            "topic_id": topic_id,
            "topic_name": topic_name,
            "course_title": course_title,
            "question_count": question_count,
            "resource_count": resource_count,
            "has_content": question_count > 0 or resource_count > 0
        }
        for topic_id, topic_name, course_title, question_count, resource_count in results
    ]


@router.get("/marks-distribution")
async def get_marks_distribution(
    course_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Get distribution of marks across questions.

    Query Parameters:
    - course_id: Filter by specific course (optional)

    Returns:
        Marks distribution with statistics

    Example:
        GET /api/analytics/marks-distribution
        Response: {
            "distribution": [...],
            "statistics": {
                "avg_marks": 8.5,
                "min_marks": 2,
                "max_marks": 15,
                "total_marks": 850
            }
        }
    """
    query = db.query(Question)

    if course_id:
        query = query.filter(Question.course_id == course_id)

    # Get distribution
    distribution = db.query(
        Question.marks,
        func.count(Question.question_id).label('count')
    )
    if course_id:
        distribution = distribution.filter(Question.course_id == course_id)

    dist_results = distribution.group_by(Question.marks).order_by(Question.marks).all()

    # Get statistics
    stats = db.query(
        func.avg(Question.marks).label('avg_marks'),
        func.min(Question.marks).label('min_marks'),
        func.max(Question.marks).label('max_marks'),
        func.sum(Question.marks).label('total_marks')
    )
    if course_id:
        stats = stats.filter(Question.course_id == course_id)

    stats_result = stats.first()

    return {
        "distribution": [
            {"marks": marks, "count": count}
            for marks, count in dist_results
        ],
        "statistics": {
            "avg_marks": round(float(stats_result.avg_marks or 0), 2),
            "min_marks": stats_result.min_marks or 0,
            "max_marks": stats_result.max_marks or 0,
            "total_marks": stats_result.total_marks or 0
        }
    }


@router.get("/course-statistics")
async def get_course_statistics(db: Session = Depends(get_db)):
    """
    Get detailed statistics for each course.

    Returns:
        Per-course statistics with questions, topics, and resources

    Example:
        GET /api/analytics/course-statistics
    """
    results = db.query(
        Course.course_id,
        Course.course_code,
        Course.course_title,
        func.count(func.distinct(Topic.topic_id)).label('topic_count'),
        func.count(func.distinct(Question.question_id)).label('question_count'),
        func.count(func.distinct(Resource.resource_id)).label('resource_count')
    ).join(
        Topic, Course.course_id == Topic.course_id, isouter=True
    ).join(
        Question, Course.course_id == Question.course_id, isouter=True
    ).join(
        Resource, Course.course_id == Resource.course_id, isouter=True
    ).group_by(
        Course.course_id, Course.course_code, Course.course_title
    ).all()

    return [
        {
            "course_id": course_id,
            "course_code": course_code,
            "course_title": course_title,
            "topic_count": topic_count,
            "question_count": question_count,
            "resource_count": resource_count,
            "total_items": topic_count + question_count + resource_count
        }
        for course_id, course_code, course_title, topic_count, question_count, resource_count in results
    ]

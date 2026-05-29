"""
Learning Navigation API Endpoints

Provides unified navigation across the 12-week learning curriculum.
Enables progressive navigation, resource discovery, and progress tracking.

Endpoints:
- GET /learning/curriculum - Get complete curriculum overview
- GET /learning/weeks/{week_number} - Get specific week with navigation
- GET /learning/weeks/{week_number}/resources - Get resources for a week
- PUT /learning/weeks/{week_number}/status - Update week status
- POST /learning/initialize - Initialize/refresh curriculum from filesystem

Learning Objectives:
- Build RESTful API for learning navigation
- Enable unified access to curriculum structure
- Track learning progress via API
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.services.learning_navigation_service import LearningNavigationService
from app.schemas import (
    LearningWeekResponse,
    LearningResourceResponse,
    NavigationResponse,
    CurriculumOverviewResponse,
    LearningWeekUpdate,
)

router = APIRouter(prefix="/learning", tags=["Learning Navigation"])

# Initialize navigation service
nav_service = LearningNavigationService()


@router.get("/curriculum", response_model=CurriculumOverviewResponse)
def get_curriculum_overview(db: Session = Depends(get_db)):
    """
    Get complete overview of the 12-week learning curriculum

    Returns:
        - All weeks with their resources
        - Progress statistics (completed, in_progress, not_started)
        - Overall progress percentage

    Example:
        GET /learning/curriculum
    """
    try:
        return nav_service.get_curriculum_overview(db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch curriculum overview: {str(e)}"
        )


@router.get("/weeks/{week_number}", response_model=NavigationResponse)
def get_week_navigation(
    week_number: int,
    db: Session = Depends(get_db)
):
    """
    Get navigation context for a specific week

    Args:
        week_number: Week number (1-12)

    Returns:
        - Current week details with resources
        - Previous week (if exists)
        - Next week (if exists)
        - Overall progress percentage

    Example:
        GET /learning/weeks/5
    """
    if week_number < 1 or week_number > 12:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Week number must be between 1 and 12"
        )

    navigation = nav_service.get_navigation(db, week_number)
    if not navigation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Week {week_number} not found. Try initializing curriculum first."
        )

    return navigation


@router.get("/weeks/{week_number}/details", response_model=LearningWeekResponse)
def get_week_details(
    week_number: int,
    db: Session = Depends(get_db)
):
    """
    Get detailed information about a specific week

    Args:
        week_number: Week number (1-12)

    Returns:
        Week details with all resources

    Example:
        GET /learning/weeks/3/details
    """
    if week_number < 1 or week_number > 12:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Week number must be between 1 and 12"
        )

    week = nav_service.get_week_by_number(db, week_number)
    if not week:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Week {week_number} not found"
        )

    return LearningWeekResponse.from_orm(week)


@router.put("/weeks/{week_number}/status", response_model=LearningWeekResponse)
def update_week_status(
    week_number: int,
    update_data: LearningWeekUpdate,
    db: Session = Depends(get_db)
):
    """
    Update the status of a learning week

    Args:
        week_number: Week number (1-12)
        update_data: Status update ('not_started', 'in_progress', 'completed')

    Returns:
        Updated week details

    Example:
        PUT /learning/weeks/5/status
        Body: {"status": "completed"}
    """
    if week_number < 1 or week_number > 12:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Week number must be between 1 and 12"
        )

    if not update_data.status:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Status field is required"
        )

    week = nav_service.update_week_status(db, week_number, update_data.status.value)
    if not week:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Week {week_number} not found"
        )

    return LearningWeekResponse.from_orm(week)


@router.post("/initialize", response_model=dict)
def initialize_curriculum(db: Session = Depends(get_db)):
    """
    Initialize or refresh the learning curriculum from filesystem

    Scans the weeks/ directory and:
    - Discovers all week directories
    - Indexes learning resources (docs, exercises, notebooks, etc.)
    - Creates/updates database entries

    This endpoint should be called:
    - On first setup
    - When new weeks or resources are added
    - To refresh the curriculum structure

    Returns:
        Summary of initialized weeks and resources

    Example:
        POST /learning/initialize
    """
    try:
        weeks = nav_service.initialize_curriculum(db)

        # Count resources
        total_resources = sum(len(week.resources) for week in weeks)

        return {
            "message": "Curriculum initialized successfully",
            "total_weeks": len(weeks),
            "total_resources": total_resources,
            "weeks": [
                {
                    "week_number": week.week_number,
                    "title": week.title,
                    "resources_count": len(week.resources)
                }
                for week in weeks
            ]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to initialize curriculum: {str(e)}"
        )


@router.get("/search", response_model=List[LearningResourceResponse])
def search_learning_resources(
    query: str,
    resource_type: str = None,
    db: Session = Depends(get_db)
):
    """
    Search for learning resources across all weeks

    Args:
        query: Search query (searches in title and file path)
        resource_type: Optional filter by resource type

    Returns:
        List of matching resources

    Example:
        GET /learning/search?query=exercise&resource_type=exercise
    """
    from app.db.models import LearningResource

    # Build query
    search_query = db.query(LearningResource)

    # Filter by resource type if provided
    if resource_type:
        search_query = search_query.filter(LearningResource.resource_type == resource_type)

    # Search in title and file path
    search_pattern = f"%{query}%"
    search_query = search_query.filter(
        (LearningResource.title.ilike(search_pattern)) |
        (LearningResource.file_path.ilike(search_pattern))
    )

    resources = search_query.limit(50).all()

    return [LearningResourceResponse.from_orm(r) for r in resources]


@router.get("/stats", response_model=dict)
def get_learning_stats(db: Session = Depends(get_db)):
    """
    Get statistics about the learning curriculum

    Returns:
        - Total weeks, resources
        - Resources by type
        - Progress statistics

    Example:
        GET /learning/stats
    """
    from app.db.models import LearningWeek, LearningResource
    from sqlalchemy import func

    total_weeks = db.query(func.count(LearningWeek.week_id)).scalar() or 0
    total_resources = db.query(func.count(LearningResource.resource_id)).scalar() or 0

    # Count by resource type
    resources_by_type = db.query(
        LearningResource.resource_type,
        func.count(LearningResource.resource_id).label('count')
    ).group_by(LearningResource.resource_type).all()

    # Count by status
    weeks_by_status = db.query(
        LearningWeek.status,
        func.count(LearningWeek.week_id).label('count')
    ).group_by(LearningWeek.status).all()

    return {
        "total_weeks": total_weeks,
        "total_resources": total_resources,
        "resources_by_type": {rtype: count for rtype, count in resources_by_type},
        "weeks_by_status": {status: count for status, count in weeks_by_status}
    }

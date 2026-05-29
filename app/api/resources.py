"""
Resources API Endpoints
CRUD operations for academic resources

Learning objectives:
- Resource management (notes, question papers, textbooks)
- File metadata handling
- Filtering by type, year, course
- Optional foreign key relationships
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Course, Resource
from app.schemas import ResourceCreate, ResourceResponse, ResourceUpdate

router = APIRouter(prefix="/api/resources", tags=["resources"])


@router.get("/", response_model=list[ResourceResponse])
async def list_resources(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Max records to return"),
    course_id: int | None = Query(None, description="Filter by course ID"),
    resource_type: str | None = Query(
        None, description="Filter by type (notes, question_paper, textbook, assignment, slides)"
    ),
    academic_year: int | None = Query(
        None, ge=2010, le=2030, description="Filter by academic year"
    ),
    search: str | None = Query(None, description="Search in title or source_name"),
    db: Session = Depends(get_db),
):
    """
    List all resources with extensive filtering options.

    Query Parameters:
    - skip: Pagination offset
    - limit: Maximum number of results
    - course_id: Filter by specific course
    - resource_type: Filter by resource type
    - academic_year: Filter by academic year
    - search: Search in title or source_name

    Returns:
        List of resources matching filters

    Example:
        GET /api/resources?resource_type=question_paper&academic_year=2023
    """
    query = db.query(Resource)

    # Apply filters
    if course_id is not None:
        query = query.filter(Resource.course_id == course_id)
    if resource_type is not None:
        query = query.filter(Resource.resource_type == resource_type)
    if academic_year is not None:
        query = query.filter(Resource.year_published == academic_year)
    if search is not None:
        # Case-insensitive search in title or source_name
        search_filter = f"%{search}%"
        query = query.filter(
            (Resource.title.ilike(search_filter)) | (Resource.source_name.ilike(search_filter))
        )

    resources = query.offset(skip).limit(limit).all()
    return resources


@router.get("/{resource_id}", response_model=ResourceResponse)
async def get_resource(resource_id: int, db: Session = Depends(get_db)):
    """
    Get a specific resource by ID.

    Args:
        resource_id: Resource identifier

    Returns:
        Resource details with related course information

    Raises:
        404: Resource not found

    Example:
        GET /api/resources/10
    """
    resource = db.query(Resource).filter(Resource.resource_id == resource_id).first()

    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resource with id {resource_id} not found",
        )

    return resource


@router.post("/", response_model=ResourceResponse, status_code=status.HTTP_201_CREATED)
async def create_resource(resource: ResourceCreate, db: Session = Depends(get_db)):
    """
    Create a new resource.

    Request Body:
        - course_id: Foreign key to courses table (optional)
        - title: Resource title (required)
        - resource_type: Type of resource (required: notes, question_paper, textbook, assignment, slides)
        - source_name: Source or author name (optional)
        - academic_year: Academic year (optional, 2010-2030)
        - file_path: Path to resource file (optional)

    Returns:
        Created resource with generated resource_id

    Raises:
        400: Invalid course_id or constraint violation
        500: Database error

    Example:
        POST /api/resources
        {
            "course_id": 1,
            "title": "DBMS Final Exam 2023",
            "resource_type": "question_paper",
            "source_name": "University of XYZ",
            "academic_year": 2023,
            "file_path": "/uploads/dbms_final_2023.pdf"
        }
    """
    try:
        # Verify course exists (if provided)
        if resource.course_id is not None:
            course = db.query(Course).filter(Course.course_id == resource.course_id).first()
            if not course:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Course with id {resource.course_id} does not exist",
                )

        # Create new resource
        db_resource = Resource(**resource.dict())
        db.add(db_resource)
        db.commit()
        db.refresh(db_resource)
        return db_resource

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Database constraint violation: {str(e.orig)}",
        )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create resource: {str(e)}",
        )


@router.put("/{resource_id}", response_model=ResourceResponse)
async def update_resource(
    resource_id: int, resource: ResourceUpdate, db: Session = Depends(get_db)
):
    """
    Update an existing resource (partial update supported).

    Args:
        resource_id: Resource identifier

    Request Body (all fields optional):
        - course_id: New course assignment
        - title: Updated title
        - resource_type: Updated resource type
        - source_name: Updated source name
        - academic_year: Updated academic year
        - file_path: Updated file path

    Returns:
        Updated resource

    Raises:
        404: Resource not found
        400: Invalid course_id or constraint violation

    Example:
        PUT /api/resources/10
        {
            "title": "DBMS Final Exam 2023 - Updated",
            "academic_year": 2024
        }
    """
    # Fetch existing resource
    db_resource = db.query(Resource).filter(Resource.resource_id == resource_id).first()

    if not db_resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resource with id {resource_id} not found",
        )

    try:
        # Update only provided fields
        update_data = resource.dict(exclude_unset=True)

        # If updating course_id, verify new course exists (allow None)
        if "course_id" in update_data and update_data["course_id"] is not None:
            course = db.query(Course).filter(Course.course_id == update_data["course_id"]).first()
            if not course:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Course with id {update_data['course_id']} does not exist",
                )

        for field, value in update_data.items():
            setattr(db_resource, field, value)

        db.commit()
        db.refresh(db_resource)
        return db_resource

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Database constraint violation: {str(e.orig)}",
        )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update resource: {str(e)}",
        )


@router.delete("/{resource_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resource(resource_id: int, db: Session = Depends(get_db)):
    """
    Delete a resource.

    Args:
        resource_id: Resource identifier

    Returns:
        204 No Content on success

    Raises:
        404: Resource not found

    Note:
        This will cascade delete related resource_chunks and chunk_embeddings

    Example:
        DELETE /api/resources/10
    """
    db_resource = db.query(Resource).filter(Resource.resource_id == resource_id).first()

    if not db_resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resource with id {resource_id} not found",
        )

    try:
        db.delete(db_resource)
        db.commit()
        return None  # 204 No Content

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete resource: {str(e)}",
        )


@router.get("/stats/by-type")
async def get_resources_by_type(db: Session = Depends(get_db)):
    """
    Get resource count grouped by type.

    Returns:
        List of dictionaries with resource_type and count

    Example:
        GET /api/resources/stats/by-type
        Response: [
            {"resource_type": "question_paper", "count": 25},
            {"resource_type": "notes", "count": 40},
            {"resource_type": "textbook", "count": 15}
        ]
    """
    from sqlalchemy import func

    results = (
        db.query(Resource.resource_type, func.count(Resource.resource_id).label("count"))
        .group_by(Resource.resource_type)
        .all()
    )

    return [{"resource_type": resource_type, "count": count} for resource_type, count in results]


@router.get("/stats/by-year")
async def get_resources_by_year(db: Session = Depends(get_db)):
    """
    Get resource count grouped by academic year.

    Returns:
        List of dictionaries with academic_year and count

    Example:
        GET /api/resources/stats/by-year
        Response: [
            {"academic_year": 2024, "count": 35},
            {"academic_year": 2023, "count": 42},
            {"academic_year": 2022, "count": 38}
        ]
    """
    from sqlalchemy import func

    results = (
        db.query(Resource.year_published, func.count(Resource.resource_id).label("count"))
        .filter(Resource.year_published.isnot(None))
        .group_by(Resource.year_published)
        .order_by(Resource.year_published.desc())
        .all()
    )

    return [{"academic_year": year, "count": count} for year, count in results]


@router.get("/{resource_id}/chunks")
async def get_resource_chunks(resource_id: int, db: Session = Depends(get_db)):
    """
    Get all chunks for a specific resource.

    Args:
        resource_id: Resource identifier

    Returns:
        List of resource chunks

    Raises:
        404: Resource not found

    Note:
        This endpoint is useful for Week 10 semantic search implementation

    Example:
        GET /api/resources/10/chunks
    """
    # Verify resource exists
    resource = db.query(Resource).filter(Resource.resource_id == resource_id).first()

    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resource with id {resource_id} not found",
        )

    # Return chunks through relationship
    return resource.chunks

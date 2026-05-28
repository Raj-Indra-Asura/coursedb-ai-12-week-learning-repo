"""
Health Check Endpoint

Week 5: PostgreSQL + FastAPI Foundation

This endpoint provides a simple health check for the API and database connection.

Learning Objectives:
- Understand basic FastAPI routing
- Learn how to structure API endpoints
- Test database connectivity
- Implement health monitoring

TODO (Week 5):
1. Import FastAPI dependencies
2. Create health check route
3. Add database connection test
4. Return system status

Example Response:
{
    "status": "healthy",
    "database": "connected",
    "timestamp": "2026-05-28T10:00:00Z"
}
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
# TODO (Week 5): Import database session dependency
# from app.db.database import get_db

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/")
async def health_check():
    """
    Health check endpoint

    TODO (Week 5): Implement health check
    - Check API is running
    - Check database connection
    - Return status
    """
    # TODO (Week 5): Implement actual health check
    return {
        "status": "healthy",
        "message": "API is running (Week 5: implement database check)"
    }


# TODO (Week 5): Add database health check
# @router.get("/db")
# async def database_health(db: Session = Depends(get_db)):
#     """Check database connection"""
#     try:
#         # Execute simple query
#         db.execute("SELECT 1")
#         return {"status": "healthy", "database": "connected"}
#     except Exception as e:
#         return {"status": "unhealthy", "database": "disconnected", "error": str(e)}

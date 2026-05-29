"""
Health Check Endpoint

Week 5: PostgreSQL + FastAPI Foundation

This endpoint provides health checks for the API and database connection.

Learning Objectives:
- Understand basic FastAPI routing
- Learn how to structure API endpoints
- Test database connectivity
- Implement health monitoring
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime

from app.db.database import get_db, get_db_info

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/")
async def health_check():
    """
    Basic health check endpoint

    Returns:
        dict: API status and timestamp

    Learning Note:
    - This is the simplest endpoint
    - No database dependency
    - Fast response for load balancers
    - Use GET method (read-only, idempotent)
    """
    return {
        "status": "healthy",
        "message": "CourseDB-AI API is running",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "version": "1.0.0"
    }


@router.get("/db")
async def database_health(db: Session = Depends(get_db)):
    """
    Check database connection health

    Learning Objectives:
    - Use dependency injection (Depends)
    - Test database connectivity
    - Handle database errors
    - Return structured responses

    Args:
        db: Database session (injected by FastAPI)

    Returns:
        dict: Database connection status

    How it works:
    1. FastAPI calls get_db() to get database session
    2. Execute simple query (SELECT 1)
    3. If successful, database is healthy
    4. If error, catch exception and return unhealthy
    """
    try:
        # Execute simple query to test connection
        result = db.execute(text("SELECT 1 as health_check"))
        result.fetchone()

        # Get database info (without password)
        db_info = get_db_info()

        return {
            "status": "healthy",
            "database": "connected",
            "connection": {
                "driver": db_info["driver"],
                "host": db_info["host"],
                "port": db_info["port"],
                "database": db_info["database"],
            },
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

    except Exception as e:
        # Database connection failed
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
            "error_type": type(e).__name__,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }


@router.get("/db/tables")
async def check_tables(db: Session = Depends(get_db)):
    """
    Check if database tables exist

    Learning Objectives:
    - Query database metadata
    - Verify schema is set up correctly
    - Use raw SQL with SQLAlchemy

    Returns:
        dict: List of tables in database

    Use case:
    - Verify migrations ran successfully
    - Debug table creation issues
    - Confirm schema setup
    """
    try:
        # Use SQLAlchemy's dialect-agnostic inspector so this works on both
        # PostgreSQL (production) and SQLite (tests).
        from sqlalchemy import inspect as sa_inspect

        inspector = sa_inspect(db.bind)
        tables = sorted(inspector.get_table_names())

        # Expected tables from models.py
        expected_tables = [
            "courses",
            "topics",
            "questions",
            "resources",
            "resource_chunks",
            "chunk_embeddings",
            "users",
            "search_logs",
        ]

        missing_tables = [t for t in expected_tables if t not in tables]
        extra_tables = [t for t in tables if t not in expected_tables]

        return {
            "status": "healthy" if not missing_tables else "incomplete",
            "tables_found": len(tables),
            "tables_expected": len(expected_tables),
            "tables": tables,
            "missing_tables": missing_tables,
            "extra_tables": extra_tables,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to check tables: {str(e)}"
        )


@router.get("/db/counts")
async def data_counts(db: Session = Depends(get_db)):
    """
    Get row counts for all main tables

    Learning Objectives:
    - Execute multiple queries
    - Aggregate data from different tables
    - Handle missing tables gracefully

    Returns:
        dict: Row count for each table

    Use case:
    - Quick data overview
    - Verify seed data loaded
    - Monitor data growth
    """
    try:
        counts = {}

        # Count rows in each table
        tables = ["courses", "topics", "questions", "resources", "users", "search_logs"]

        for table in tables:
            try:
                result = db.execute(text(f"SELECT COUNT(*) FROM {table}"))
                count = result.scalar()
                counts[table] = count
            except Exception:
                counts[table] = "table_not_found"

        total_rows = sum(v for v in counts.values() if isinstance(v, int))

        return {
            "status": "healthy",
            "counts": counts,
            "total_rows": total_rows,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get counts: {str(e)}"
        )


"""
Learning Notes:

1. **Health Check Patterns**:
   - /health: Fast check (no DB)
   - /health/db: Database connectivity
   - /health/db/tables: Schema verification
   - /health/db/counts: Data verification

2. **Dependency Injection**:
   ```python
   async def endpoint(db: Session = Depends(get_db)):
       # db is automatically provided by FastAPI
       # Session is closed automatically after function returns
   ```

3. **Error Handling**:
   - Try/except for database operations
   - Return structured error responses
   - Use HTTPException for HTTP errors

4. **Raw SQL with SQLAlchemy**:
   ```python
   result = db.execute(text("SELECT * FROM table"))
   rows = result.fetchall()
   ```

5. **HTTP Status Codes**:
   - 200: Success (default for GET)
   - 500: Internal server error
   - 503: Service unavailable (use for unhealthy)

Testing:
```bash
# Test basic health check
curl http://localhost:8000/health

# Test database health
curl http://localhost:8000/health/db

# Check tables exist
curl http://localhost:8000/health/db/tables

# Get row counts
curl http://localhost:8000/health/db/counts
```

Next Steps (Week 6):
- Implement CRUD endpoints for courses
- Add proper error responses
- Add authentication (Week 11)
"""

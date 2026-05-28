"""
Database Connection and Session Management

Week 5: PostgreSQL + FastAPI Foundation

This module handles:
- SQLAlchemy engine creation
- Session management
- Dependency injection for database sessions

Learning Objectives:
- Understand database connection pooling
- Learn session lifecycle management
- Practice dependency injection pattern
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from typing import Generator

# Read database URL from environment variable
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://coursedb_user:coursedb_password@localhost:5432/coursedb_ai"
)

# Learning Note: Connection String Format
# postgresql://username:password@host:port/database_name
# For local development with docker-compose:
# - host: localhost (or 'db' if running inside docker network)
# - port: 5432 (default PostgreSQL port)
# - database: coursedb_ai
# - user/password: defined in docker-compose.yml

# Create SQLAlchemy engine
# Learning Note: Engine Configuration
# - echo=False: Don't log all SQL statements (set True for debugging)
# - pool_pre_ping=True: Verify connections before using (handle stale connections)
# - pool_size=5: Number of connections to keep in pool
# - max_overflow=10: Additional connections when pool is exhausted
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set to True to see SQL queries in console
    pool_pre_ping=True,  # Verify connection health before use
    pool_size=5,
    max_overflow=10,
)

# Create SessionLocal class
# Learning Note: Session Factory
# - autocommit=False: Explicit transaction control (safer)
# - autoflush=False: Don't automatically flush changes (explicit control)
# - bind=engine: Connect to our database engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    Database dependency for FastAPI

    Learning Objectives (Week 5):
    - Understand dependency injection in FastAPI
    - Learn session lifecycle (create → use → close)
    - Practice proper resource cleanup with try/finally

    Usage in FastAPI endpoint:
    ```python
    @router.get("/courses")
    def get_courses(db: Session = Depends(get_db)):
        courses = db.query(Course).all()
        return courses
    ```

    How it works:
    1. FastAPI calls get_db() before executing endpoint
    2. Creates new database session
    3. Injects session into endpoint function
    4. After endpoint finishes, closes session (finally block)
    5. Even if error occurs, session is properly closed
    """
    db = SessionLocal()
    try:
        yield db  # Provide session to endpoint
    finally:
        db.close()  # Always close session (even if error)


def init_db():
    """
    Initialize database (create all tables)

    Learning Note (Week 5):
    - This creates tables based on SQLAlchemy models
    - Only use in development (use Alembic migrations in production)
    - Idempotent: Safe to call multiple times (won't duplicate tables)

    Usage:
    ```python
    from app.db.database import init_db
    from app.db.models import Base

    init_db()  # Creates all tables defined in models.py
    ```
    """
    from app.db.models import Base
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully")


def get_db_info():
    """
    Get database connection information (for debugging)

    Returns:
        dict: Database connection details (without password)
    """
    from sqlalchemy.engine.url import make_url
    url = make_url(DATABASE_URL)
    return {
        "driver": url.drivername,
        "host": url.host,
        "port": url.port,
        "database": url.database,
        "username": url.username,
    }


# Learning Notes:

"""
Key Concepts Demonstrated:

1. **Database Engine**:
   - Manages connection pool to database
   - Handles low-level database communication
   - Reuses connections for efficiency

2. **Session**:
   - Represents a "conversation" with database
   - Tracks changes (insert, update, delete)
   - Commits/rollbacks transactions
   - Must be closed after use

3. **Dependency Injection**:
   - FastAPI automatically calls get_db()
   - Provides session to endpoint
   - Ensures proper cleanup

4. **Connection Pooling**:
   - pool_size=5: Keep 5 connections ready
   - max_overflow=10: Create up to 10 more if needed
   - Improves performance (no connection overhead per request)

5. **Session Lifecycle**:
   ```
   Create Session → Execute Queries → Commit Changes → Close Session
   ```

Common Patterns:

1. **Query data**:
   ```python
   db.query(Course).filter(Course.course_code == "CS201").first()
   ```

2. **Insert data**:
   ```python
   new_course = Course(course_code="CS201", course_title="DBMS")
   db.add(new_course)
   db.commit()
   db.refresh(new_course)  # Get ID
   ```

3. **Update data**:
   ```python
   course = db.query(Course).filter_by(course_id=1).first()
   course.course_title = "Advanced DBMS"
   db.commit()
   ```

4. **Delete data**:
   ```python
   course = db.query(Course).filter_by(course_id=1).first()
   db.delete(course)
   db.commit()
   ```

Next Steps:
- Implement CRUD operations in API endpoints
- Add error handling for database operations
- Learn Alembic for schema migrations
"""

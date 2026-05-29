"""
CourseDB-AI Backend Application

Week 5: PostgreSQL + FastAPI Foundation

This is the main FastAPI application entry point.

Features:
- FastAPI app initialization
- CORS middleware for frontend access
- Database connection via dependency injection
- API router registration
- Health check endpoint

Learning Objectives:
- Understand FastAPI application structure
- Learn middleware configuration
- Practice API organization with routers
- Implement proper error handling
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

# Import API routers
from app.api import health, courses, topics, questions, resources, analytics, search

# Import database initialization
from app.db.database import init_db

# Create FastAPI application
app = FastAPI(
    title="CourseDB-AI API",
    description="A hybrid relational database + vector search system for semantic academic resource retrieval",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI at http://localhost:8000/docs
    redoc_url="/redoc",  # ReDoc at http://localhost:8000/redoc
)

# Learning Note: CORS Middleware
# CORS (Cross-Origin Resource Sharing) allows frontend (e.g., Streamlit, React)
# running on different port/domain to access this API
# Without CORS, browsers block requests due to security policy

origins = [
    "http://localhost:3000",  # React default
    "http://localhost:8501",  # Streamlit default
    "http://localhost:8080",  # Alternative frontend port
    "http://127.0.0.1:8501",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Which origins can access API
    allow_credentials=True,  # Allow cookies/auth headers
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Allow all headers
)


# Learning Note: Startup Event
# This function runs once when server starts
# Use it for one-time initialization tasks
@app.on_event("startup")
async def startup_event():
    """
    Initialize application on startup

    Tasks:
    1. Create database tables (if they don't exist)
    2. Log startup message
    3. TODO (Week 5): Load any initial data
    4. TODO (Week 10): Load embedding model
    """
    print("🚀 Starting CourseDB-AI Backend...")
    print("📦 Initializing database...")

    try:
        init_db()  # Create tables from SQLAlchemy models
        print("✅ Database initialized successfully")
    except Exception as e:
        print(f"⚠️  Database initialization warning: {e}")
        print("   (This is normal if database is not running yet)")

    print("✅ API is ready at http://localhost:8000")
    print("📚 API docs at http://localhost:8000/docs")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Cleanup on application shutdown
    """
    print("👋 Shutting down CourseDB-AI Backend...")


# Register API routers
# Learning Note: Router Organization
# Each router handles a specific resource (courses, questions, etc.)
# Keeps code organized and maintainable

app.include_router(health.router)
app.include_router(courses.router)
app.include_router(topics.router)
app.include_router(questions.router)
app.include_router(resources.router)
app.include_router(analytics.router)
app.include_router(search.router)


# Root endpoint
@app.get("/")
async def root():
    """
    Root endpoint - API information

    Learning Note:
    - Good practice to have a root endpoint
    - Provides basic API information
    - Helps verify API is running
    """
    return {
        "name": "CourseDB-AI API",
        "version": "1.0.0",
        "description": "Hybrid relational + vector database for semantic academic resource retrieval",
        "status": "operational",
        "docs": "/docs",
        "health": "/health",
    }


# Global exception handler
# Learning Note: Error Handling
# Catches unhandled exceptions and returns proper JSON response
# Prevents server from crashing on errors
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Handle all unhandled exceptions

    Returns 500 Internal Server Error with error details
    """
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error": str(exc),
            "type": type(exc).__name__,
        }
    )


# Learning Note: HTTP Exception Handler
# Handles FastAPI's HTTPException (e.g., 404, 400, etc.)
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """
    Handle HTTP exceptions (4xx, 5xx errors)
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "status_code": exc.status_code,
        }
    )


# Main entry point
if __name__ == "__main__":
    """
    Run the FastAPI application with Uvicorn

    Learning Note: Uvicorn
    - ASGI server for FastAPI
    - host="0.0.0.0": Listen on all network interfaces
    - port=8000: Default port for API
    - reload=True: Auto-reload on code changes (development only)
    """
    print("=" * 50)
    print("CourseDB-AI Backend Server")
    print("=" * 50)
    print("\n📖 Learning Note:")
    print("   This is a FastAPI application with:")
    print("   ✓ Database connection (PostgreSQL)")
    print("   ✓ CORS middleware (for frontend)")
    print("   ✓ Health check endpoint")
    print("   ✓ Auto-generated API docs")
    print("\n🌐 Access:")
    print("   • API: http://localhost:8000")
    print("   • Docs: http://localhost:8000/docs")
    print("   • Health: http://localhost:8000/health")
    print("\n🛑 Press Ctrl+C to stop")
    print("=" * 50)
    print()

    uvicorn.run(
        "app.backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload on file changes
        log_level="info",
    )


"""
Learning Notes:

1. **FastAPI Application Structure**:
   ```
   main.py (this file)
   ├── Create FastAPI app
   ├── Add middleware (CORS)
   ├── Register routers (health, courses, etc.)
   ├── Define startup/shutdown events
   └── Run with Uvicorn
   ```

2. **Router Pattern**:
   - Each resource has its own router file (health.py, courses.py, etc.)
   - Routers are registered with app.include_router()
   - Keeps code organized and testable

3. **Middleware**:
   - Functions that run before/after each request
   - CORS: Allows cross-origin requests
   - Future: Authentication, logging, rate limiting

4. **Dependency Injection**:
   - get_db() provides database session to endpoints
   - FastAPI handles lifecycle automatically
   - Clean, testable code

5. **API Documentation**:
   - /docs: Interactive Swagger UI
   - /redoc: Alternative documentation
   - Auto-generated from code + docstrings

How to Use:
1. Start PostgreSQL: `docker-compose up -d`
2. Run API: `python app/backend/main.py`
3. Visit http://localhost:8000/docs
4. Try health check endpoint

Next Steps (Week 6):
- Implement CRUD endpoints for courses
- Add request validation with Pydantic
- Implement error handling
- Add authentication (Week 11)
"""

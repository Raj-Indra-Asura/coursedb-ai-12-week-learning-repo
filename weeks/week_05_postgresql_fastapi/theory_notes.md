# Week 5: PostgreSQL + FastAPI Foundation - Theory Notes

## 📚 Core Concepts

### 1. PostgreSQL Basics

**PostgreSQL** is a powerful, open-source relational database.

**Key Features:**
- ACID compliance (transactions)
- Advanced indexing (B-tree, Hash, GiST, GIN)
- JSON support
- Full-text search
- Extensions (pgvector for embeddings!)

**Why PostgreSQL for CourseDB-AI?**
- Free and open-source
- Excellent performance
- pgvector extension for semantic search
- Strong community support

---

### 2. FastAPI Framework

**FastAPI** is a modern Python web framework for building APIs.

**Key Features:**
- Fast performance (async/await)
- Auto-generated API docs (Swagger UI)
- Type validation with Pydantic
- Dependency injection
- Easy to learn

**Why FastAPI?**
- Fastest Python framework
- Built-in data validation
- Excellent for learning
- Production-ready

---

### 3. SQLAlchemy ORM

**ORM (Object-Relational Mapping)**: Write Python classes instead of SQL

**Example:**
```python
# Without ORM (raw SQL)
cursor.execute("SELECT * FROM courses WHERE course_code = ?", ("CS201",))

# With ORM (SQLAlchemy)
course = db.query(Course).filter(Course.course_code == "CS201").first()
```

**Benefits:**
- Write Python, not SQL
- Type safety
- Relationships handled automatically
- Database-agnostic code

---

### 4. API Architecture

**Three-Layer Architecture:**

```
┌─────────────────┐
│   Frontend      │  (Streamlit/React)
│   (Week 11)     │
└────────┬────────┘
         │ HTTP Requests
┌────────▼────────┐
│   API Layer     │  (FastAPI - this week!)
│   - Routing     │
│   - Validation  │
└────────┬────────┘
         │ SQL Queries
┌────────▼────────┐
│   Database      │  (PostgreSQL)
│   - Tables      │
│   - Constraints │
└─────────────────┘
```

---

### 5. RESTful API Design

**REST Principles:**
- **Resources**: Identified by URLs (/courses, /questions)
- **HTTP Methods**: GET (read), POST (create), PUT (update), DELETE (delete)
- **Stateless**: Each request independent
- **JSON**: Standard data format

**Example Endpoints:**
```
GET    /api/courses         → List all courses
GET    /api/courses/1       → Get course with ID 1
POST   /api/courses         → Create new course
PUT    /api/courses/1       → Update course 1
DELETE /api/courses/1       → Delete course 1
```

---

### 6. Request/Response Flow

**How a Request Works:**

1. **Client** sends HTTP request: `GET /api/courses/1`
2. **FastAPI** routes to endpoint function
3. **Dependency Injection** provides database session
4. **Query Database** using SQLAlchemy ORM
5. **Pydantic** validates and serializes response
6. **Return JSON** to client

**Code Example:**
```python
@router.get("/courses/{course_id}")
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.course_id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course
```

---

### 7. Pydantic Models

**Pydantic**: Data validation using Python type hints

**Example:**
```python
class CourseCreate(BaseModel):
    course_code: str = Field(..., max_length=20)
    course_title: str = Field(..., max_length=200)
    credit: int = Field(..., gt=0)
```

**Benefits:**
- Automatic validation
- Clear error messages
- API documentation
- Type safety

---

### 8. Database Connection Pooling

**Connection Pool**: Reuse database connections instead of creating new ones

**Why?**
- Opening connections is expensive
- Limited database connections
- Better performance

**Configuration:**
```python
engine = create_engine(
    DATABASE_URL,
    pool_size=5,        # Keep 5 connections ready
    max_overflow=10,    # Create 10 more if needed
)
```

---

### 9. Dependency Injection

**Pattern**: FastAPI provides dependencies automatically

**Example:**
```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/courses")
def list_courses(db: Session = Depends(get_db)):
    # db is automatically provided by FastAPI
    return db.query(Course).all()
```

**Benefits:**
- Clean code
- Easy testing (mock dependencies)
- Proper resource cleanup

---

### 10. CRUD Operations

**CRUD**: Create, Read, Update, Delete

#### **Create:**
```python
new_course = Course(course_code="CS201", course_title="DBMS")
db.add(new_course)
db.commit()
db.refresh(new_course)  # Get auto-generated ID
```

#### **Read:**
```python
# Get one
course = db.query(Course).filter(Course.course_id == 1).first()

# Get all
courses = db.query(Course).all()

# Filter
courses = db.query(Course).filter(Course.credit > 3).all()
```

#### **Update:**
```python
course = db.query(Course).filter(Course.course_id == 1).first()
course.course_title = "Advanced DBMS"
db.commit()
```

#### **Delete:**
```python
course = db.query(Course).filter(Course.course_id == 1).first()
db.delete(course)
db.commit()
```

---

## 🎯 CourseDB-AI Week 5 Implementation

### What We Built:
1. **Database Connection** (`app/db/database.py`)
   - Connection pooling
   - Session management
   - Dependency injection

2. **SQLAlchemy Models** (`app/db/models.py`)
   - Course, Topic, Question, Resource
   - Relationships and constraints

3. **Pydantic Schemas** (`app/schemas/`)
   - Request validation
   - Response serialization

4. **FastAPI App** (`app/backend/main.py`)
   - Application setup
   - CORS middleware
   - Health check endpoints

5. **Health Endpoints** (`app/api/health.py`)
   - `/health` - API status
   - `/health/db` - Database connectivity
   - `/health/db/tables` - Schema verification

---

## ✅ Self-Check Questions

1. What's the difference between ORM and raw SQL?
2. Why do we need connection pooling?
3. What HTTP method do you use to create a resource?
4. What's the role of Pydantic in FastAPI?
5. How does dependency injection work in FastAPI?
6. What's the difference between POST and PUT?
7. Why is FastAPI called "fast"?
8. What's CORS and why do we need it?

---

## 🚀 Testing Your API

```bash
# 1. Start database
docker-compose up -d

# 2. Run FastAPI
python app/backend/main.py

# 3. Test endpoints
curl http://localhost:8000/health
curl http://localhost:8000/health/db

# 4. Visit interactive docs
# http://localhost:8000/docs
```

---

**Next Week (Week 6):** Implement CRUD endpoints for courses, topics, and questions!

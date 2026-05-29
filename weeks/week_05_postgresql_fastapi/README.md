# Week 5: PostgreSQL + FastAPI Foundation

**Duration**: 7 days
**Status**: 🔄 Ready to Start

## 🧭 Navigation

**[← Previous: Week 4](../week_04_normalization/reflection.md)** | **[View Learning Path](../../LEARNING_PATH.md)** | **[Next: Theory Notes →](theory_notes.md)**

---

## 🎯 Why This Week Matters

After 4 weeks of database theory (DBMS, SQL, ER modeling, normalization), it's time to **build the backend!**

Week 5 bridges theory and practice by:
- Installing and configuring PostgreSQL production database
- Setting up FastAPI Python backend framework
- Mapping normalized schemas to SQLAlchemy ORM models
- Creating database migrations for version control
- Building your first CRUD API endpoints
- Connecting CourseDB-AI frontend to backend

**Why PostgreSQL + FastAPI?**
- **PostgreSQL**: Production-grade relational database with pgvector for AI
- **FastAPI**: Modern Python framework with automatic API docs, type safety, async support
- **SQLAlchemy**: Industry-standard ORM for database operations
- **Alembic**: Database migration tool for schema versioning

**Real-world impact:**
- Companies like Instagram, Spotify use PostgreSQL at massive scale
- FastAPI powers ML APIs at Microsoft, Uber, Netflix
- SQLAlchemy is the de facto Python ORM
- These skills directly translate to job requirements

---

## 📚 Learning Objectives

By the end of this week, you will be able to:

✅ Install and configure PostgreSQL database locally
✅ Create databases, users, and manage permissions
✅ Set up a FastAPI project with proper structure
✅ Define SQLAlchemy ORM models from ER diagrams
✅ Configure database connections with environment variables
✅ Create and run Alembic migrations
✅ Build CRUD API endpoints (Create, Read, Update, Delete)
✅ Test APIs using FastAPI's automatic documentation
✅ Understand ORM relationships (foreign keys, backref)
✅ Handle database sessions and transactions

---

## 📖 Concepts to Learn

### **1. PostgreSQL Fundamentals**

**What is PostgreSQL?**
- Open-source relational database (RDBMS)
- ACID compliant (Atomicity, Consistency, Isolation, Durability)
- Supports JSON, arrays, full-text search, and pgvector (for embeddings)
- Used by Apple, Instagram, Reddit, Spotify

**Key PostgreSQL Concepts:**

**Databases vs Schemas:**
```sql
-- Database: Top-level container
CREATE DATABASE coursedb_dev;

-- Schema: Namespace within database (default: public)
CREATE SCHEMA app_schema;
```

**Users and Permissions:**
```sql
-- Create user
CREATE USER coursedb_user WITH PASSWORD 'secure_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE coursedb_dev TO coursedb_user;
```

**Connection Strings:**
```
postgresql://username:password@host:port/database
postgresql://coursedb_user:password@localhost:5432/coursedb_dev
```

### **2. FastAPI Framework**

**What is FastAPI?**
Modern Python web framework for building APIs with:
- Automatic interactive API docs (Swagger UI)
- Type hints for validation
- Async/await support for performance
- Dependency injection for clean code

**Basic FastAPI App:**
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

# Run: uvicorn main:app --reload
# Docs: http://localhost:8000/docs
```

**Path Parameters:**
```python
@app.get("/courses/{course_id}")
def get_course(course_id: int):
    return {"course_id": course_id}
```

**Query Parameters:**
```python
@app.get("/courses")
def list_courses(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}
```

**Request Body with Pydantic:**
```python
from pydantic import BaseModel

class CourseCreate(BaseModel):
    course_code: str
    title: str
    credits: int

@app.post("/courses")
def create_course(course: CourseCreate):
    return course
```

### **3. SQLAlchemy ORM**

**What is an ORM?**
Object-Relational Mapping - write Python code instead of SQL:
- Models = Tables
- Instances = Rows
- Attributes = Columns
- Methods = Operations

**SQLAlchemy Model Example:**
```python
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Course(Base):
    __tablename__ = "courses"

    course_id = Column(Integer, primary_key=True)
    course_code = Column(String(20), unique=True, nullable=False)
    title = Column(String(255), nullable=False)
    credits = Column(Integer)

    # Relationship
    topics = relationship("Topic", back_populates="course")
```

**Relationships:**
```python
# One-to-Many: Course → Topics
class Course(Base):
    topics = relationship("Topic", back_populates="course")

class Topic(Base):
    course_id = Column(Integer, ForeignKey("courses.course_id"))
    course = relationship("Course", back_populates="topics")
```

**CRUD Operations:**
```python
# Create
course = Course(course_code="CS201", title="DBMS")
db.add(course)
db.commit()

# Read
course = db.query(Course).filter(Course.course_id == 1).first()

# Update
course.title = "Database Management Systems"
db.commit()

# Delete
db.delete(course)
db.commit()
```

### **4. Database Migrations with Alembic**

**Why Migrations?**
- Version control for database schema
- Safely evolve schema in production
- Rollback changes if needed
- Team collaboration on schema changes

**Alembic Commands:**
```bash
# Initialize Alembic
alembic init alembic

# Create migration
alembic revision --autogenerate -m "create courses table"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

**Migration File:**
```python
def upgrade():
    op.create_table(
        'courses',
        sa.Column('course_id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.String(255), nullable=False)
    )

def downgrade():
    op.drop_table('courses')
```

### **5. Project Structure**

**FastAPI Project Layout:**
```
coursedb-ai/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app
│   ├── database.py          # DB connection
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   └── api/
│       ├── __init__.py
│       ├── courses.py       # Course endpoints
│       └── topics.py        # Topic endpoints
├── alembic/                 # Migrations
├── .env                     # Environment variables
├── requirements.txt         # Dependencies
└── README.md
```

**Separation of Concerns:**
- **models.py**: Database tables (SQLAlchemy)
- **schemas.py**: API request/response (Pydantic)
- **api/*.py**: Route handlers (FastAPI endpoints)
- **database.py**: Connection setup

### **6. Environment Configuration**

**`.env` File:**
```env
DATABASE_URL=postgresql://user:password@localhost:5432/coursedb_dev
SECRET_KEY=your-secret-key-here
DEBUG=True
```

**Loading Environment Variables:**
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    debug: bool = False

    class Config:
        env_file = ".env"

settings = Settings()
```

### **7. Database Session Management**

**Session Lifecycle:**
```python
from sqlalchemy.orm import Session
from fastapi import Depends

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Use in endpoint
@app.get("/courses")
def list_courses(db: Session = Depends(get_db)):
    courses = db.query(Course).all()
    return courses
```

**Why Dependency Injection?**
- Automatic session management
- Easy to test (can inject mock DB)
- Clean, reusable code

---

## 🛠️ This Week's Exercises

### **Exercise 1: PostgreSQL Setup**
- Install PostgreSQL locally
- Create `coursedb_dev` database
- Create `coursedb_user` with password
- Grant permissions
- Connect using psql or GUI tool

### **Exercise 2: FastAPI Hello World**
- Create basic FastAPI app
- Define health check endpoint
- Run with uvicorn
- Access Swagger docs

### **Exercise 3: SQLAlchemy Models**
- Define Course model
- Define Topic model with foreign key
- Create database connection
- Test model creation

### **Exercise 4: First Migration**
- Initialize Alembic
- Generate migration for Course table
- Apply migration
- Verify table created in PostgreSQL

### **Exercise 5: CRUD Endpoints**
- Create course (POST /courses)
- List courses (GET /courses)
- Get course by ID (GET /courses/{id})
- Update course (PUT /courses/{id})
- Delete course (DELETE /courses/{id})

### **Exercise 6: CourseDB-AI Implementation**
- Implement all CourseDB-AI models
- Create migrations for all tables
- Build CRUD for courses, topics, questions
- Test with Swagger UI

---

## 📦 Deliverables

By the end of Week 5, you should have:

1. **PostgreSQL Database**
   - Installed and running
   - `coursedb_dev` database created
   - User with proper permissions
   - Connection verified

2. **FastAPI Project**
   - Proper project structure
   - All dependencies in requirements.txt
   - Environment configuration (.env)
   - Database connection working

3. **SQLAlchemy Models**
   - All CourseDB-AI entities as models
   - Relationships configured (foreign keys, backref)
   - Models match Week 3 ER diagram

4. **Database Migrations**
   - Alembic initialized
   - Migrations for all tables
   - Clean upgrade/downgrade

5. **CRUD API Endpoints**
   - At least courses and topics endpoints
   - All 5 operations (Create, Read, List, Update, Delete)
   - Proper error handling
   - Tested via Swagger UI

6. **Documentation**
   - README with setup instructions
   - API endpoint documentation
   - Environment setup guide

---

## ✅ Self-Check Quiz

Test your understanding before moving to Week 6:

1. **What's the difference between a database and a schema in PostgreSQL?**
   - Answer: _______

2. **What is an ORM and why use it?**
   - Answer: _______

3. **What's the difference between SQLAlchemy models and Pydantic schemas?**
   - Answer: _______

4. **Why use database migrations instead of manual schema changes?**
   - Answer: _______

5. **What does `db: Session = Depends(get_db)` do in FastAPI?**
   - Answer: _______

6. **How do you define a one-to-many relationship in SQLAlchemy?**
   - Answer: _______

7. **What's the command to apply all pending migrations?**
   - Answer: _______

8. **Where should you store database credentials?**
   - Answer: _______

9. **What's the benefit of FastAPI's automatic documentation?**
   - Answer: _______

10. **How do you handle database sessions properly?**
    - Answer: _______

---

## 🎓 CourseDB-AI Implementation Guide

### **Step 1: Models from Week 3 ER Diagram**

Map your Week 3 ER design to SQLAlchemy:

**Course Model:**
```python
class Course(Base):
    __tablename__ = "courses"

    course_id = Column(Integer, primary_key=True)
    course_code = Column(String(20), unique=True, nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    credits = Column(Integer)

    # Relationships
    topics = relationship("Topic", back_populates="course", cascade="all, delete-orphan")
    questions = relationship("Question", back_populates="course")
```

**Topic Model:**
```python
class Topic(Base):
    __tablename__ = "topics"

    topic_id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.course_id", ondelete="CASCADE"), nullable=False)
    topic_name = Column(String(255), nullable=False)
    order_index = Column(Integer)

    # Relationships
    course = relationship("Course", back_populates="topics")
    questions = relationship("Question", back_populates="topic")
```

**Question Model:**
```python
class Question(Base):
    __tablename__ = "questions"

    question_id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.course_id"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.topic_id"), nullable=False)
    question_text = Column(Text, nullable=False)
    difficulty = Column(String(20))
    marks = Column(Integer)
    year = Column(Integer)

    # Relationships
    course = relationship("Course", back_populates="questions")
    topic = relationship("Topic", back_populates="questions")
```

### **Step 2: API Endpoints**

**Course CRUD:**
```python
@router.post("/courses", response_model=CourseRead)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    db_course = Course(**course.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

@router.get("/courses", response_model=List[CourseRead])
def list_courses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    courses = db.query(Course).offset(skip).limit(limit).all()
    return courses

@router.get("/courses/{course_id}", response_model=CourseRead)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.course_id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course
```

---

## 🔗 Additional Resources

### **PostgreSQL:**
- [Official PostgreSQL Tutorial](https://www.postgresql.org/docs/current/tutorial.html)
- [PostgreSQL Exercises](https://pgexercises.com/)

### **FastAPI:**
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)

### **SQLAlchemy:**
- [SQLAlchemy ORM Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/)
- [SQLAlchemy Relationship Patterns](https://docs.sqlalchemy.org/en/20/orm/relationships.html)

### **Alembic:**
- [Alembic Tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html)

---

## 📝 Study Tips

1. **Start with PostgreSQL setup** - Get database running first
2. **Test each component** - Don't build everything at once
3. **Use Swagger UI extensively** - FastAPI's auto docs are powerful
4. **Understand relationships** - Foreign keys and backrefs are crucial
5. **Read error messages** - SQLAlchemy errors are descriptive
6. **Check migrations** - Always review auto-generated migrations
7. **Use print statements** - Debug SQL queries with echo=True

---

## 🚀 Connection to Later Weeks

**Week 6: Advanced SQL**
- Add complex queries to your CRUD endpoints
- Implement filtering, sorting, pagination
- Use views and stored procedures

**Week 7: Indexing**
- Optimize your models with indexes
- Measure query performance
- Add composite indexes for common queries

**Week 8: Query Optimization**
- Analyze slow endpoints
- Optimize N+1 query problems
- Use eager loading with joinedload()

**Week 10: Semantic Search**
- Add pgvector extension
- Store embeddings in ResourceChunk model
- Build semantic search endpoints

---

## 🎯 Week 5 Success Criteria

You've successfully completed Week 5 if you can:

✅ Install and configure PostgreSQL from scratch
✅ Create and connect to a database
✅ Set up a FastAPI project with proper structure
✅ Define SQLAlchemy models for CourseDB-AI
✅ Create and run database migrations
✅ Build CRUD endpoints for at least one resource
✅ Test APIs using Swagger UI
✅ Understand how to manage database sessions
✅ Handle errors properly (404, validation errors)
✅ Store configuration in environment variables

**Ready to begin?** Start with Day 1 in `implementation_plan.md`!

**Questions?** Review `theory_notes.md` and `mistakes_to_expect.md`

---

## 🧭 Navigation

**[← Previous: Week 4](../week_04_normalization/reflection.md)** | **[Back to Week 5 Overview](README.md)** | **[Next: Theory Notes →](theory_notes.md)**

---

## 📋 Week 5 File Sequence

1. **[Week 5 README](README.md)** ← You are here
2. **[Theory Notes](theory_notes.md)** - Core concepts
3. **[Exercises](exercises.md)** - Practice
4. **[Implementation Plan](implementation_plan.md)** - Apply concepts
5. **[Checkpoints](checkpoints.md)** - Track progress
6. **[Mistakes to Expect](mistakes_to_expect.md)** - Common pitfalls
7. **[Reflection](reflection.md)** - Weekly reflection
8. **[→ Week 6](../week_06_advanced_sql/README.md)** - Continue journey

---

**Next Week**: Week 6 - Advanced SQL (Views, Triggers, Constraints, Stored Procedures) - Level up your SQL skills!

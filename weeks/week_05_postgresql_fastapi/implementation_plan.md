# Week 5: PostgreSQL + FastAPI Implementation Plan

## 📋 7-Day Learning Path

This plan guides you through building a production-ready FastAPI backend with PostgreSQL.

---

## Day 1: PostgreSQL Setup + Environment Configuration

### Morning: Install PostgreSQL (2-3 hours)

**Step 1: Install PostgreSQL**
- macOS: `brew install postgresql@15 && brew services start postgresql@15`
- Ubuntu: `sudo apt install postgresql-15 && sudo systemctl start postgresql`
- Windows: Download from postgresql.org

**Step 2: Create Database**
```bash
psql postgres
CREATE DATABASE coursedb_dev;
CREATE USER coursedb_user WITH PASSWORD 'secure_password123';
GRANT ALL PRIVILEGES ON DATABASE coursedb_dev TO coursedb_user;
\q
```

**Step 3: Verify Connection**
```bash
psql -U coursedb_user -d coursedb_dev -h localhost
```

### Afternoon: Project Setup (2-3 hours)

**Step 1: Create Project**
```bash
mkdir coursedb-backend && cd coursedb-backend
python -m venv venv
source venv/bin/activate
```

**Step 2: Install Dependencies**
```bash
pip install fastapi uvicorn[standard] sqlalchemy psycopg2-binary \
            alembic python-dotenv pydantic-settings python-multipart
pip freeze > requirements.txt
```

**Step 3: Create `.env`**
```env
DATABASE_URL=postgresql://coursedb_user:secure_password123@localhost:5432/coursedb_dev
SECRET_KEY=your-secret-key-change-in-production
DEBUG=True
```

**Step 4: Create `database.py`**
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**Deliverable:**
- PostgreSQL running
- Database created
- Project structure initialized
- Dependencies installed

**Time spent**: _____ hours

---

## Day 2: FastAPI Hello World + First Model

### Morning: Basic FastAPI App (2-3 hours)

**Step 1: Create `main.py`**
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="CourseDB API",
    description="Database learning platform API",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to CourseDB API"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "database": "connected"}
```

**Step 2: Run Server**
```bash
uvicorn main:app --reload
```

**Step 3: Test**
- Visit: http://localhost:8000
- Swagger: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Afternoon: First SQLAlchemy Model (2-3 hours)

**Step 1: Create `models.py`**
```python
from sqlalchemy import Column, Integer, String, Text
from database import Base

class Course(Base):
    __tablename__ = "courses"

    course_id = Column(Integer, primary_key=True, index=True)
    course_code = Column(String(20), unique=True, nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    credits = Column(Integer)
```

**Step 2: Create Tables**
```python
from database import engine, Base
from models import Course

Base.metadata.create_all(bind=engine)
```

**Step 3: Test in psql**
```sql
psql -U coursedb_user -d coursedb_dev
\dt
\d courses
```

**Deliverable:**
- FastAPI app running
- Course model defined
- Table created in PostgreSQL

**Time spent**: _____ hours

---

## Day 3: Pydantic Schemas + First CRUD Endpoint

### Morning: Define Schemas (2-3 hours)

**Step 1: Create `schemas.py`**
```python
from pydantic import BaseModel, Field
from typing import Optional

class CourseBase(BaseModel):
    course_code: str = Field(..., max_length=20)
    title: str = Field(..., max_length=255)
    description: Optional[str] = None
    credits: Optional[int] = Field(None, ge=0, le=10)

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    course_code: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    credits: Optional[int] = None

class CourseRead(CourseBase):
    course_id: int

    class Config:
        from_attributes = True
```

### Afternoon: Implement CRUD (2-3 hours)

**Step 1: Create `crud.py`**
```python
from sqlalchemy.orm import Session
from models import Course
from schemas import CourseCreate, CourseUpdate

def get_course(db: Session, course_id: int):
    return db.query(Course).filter(Course.course_id == course_id).first()

def get_courses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Course).offset(skip).limit(limit).all()

def create_course(db: Session, course: CourseCreate):
    db_course = Course(**course.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

def update_course(db: Session, course_id: int, course_update: CourseUpdate):
    course = get_course(db, course_id)
    if course:
        for key, value in course_update.dict(exclude_unset=True).items():
            setattr(course, key, value)
        db.commit()
        db.refresh(course)
    return course

def delete_course(db: Session, course_id: int):
    course = get_course(db, course_id)
    if course:
        db.delete(course)
        db.commit()
    return course
```

**Step 2: Add Endpoint to `main.py`**
```python
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from schemas import CourseCreate, CourseRead
import crud

@app.post("/courses", response_model=CourseRead, status_code=201)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    return crud.create_course(db, course)

@app.get("/courses", response_model=List[CourseRead])
def list_courses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_courses(db, skip, limit)

@app.get("/courses/{course_id}", response_model=CourseRead)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = crud.get_course(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course
```

**Step 3: Test with Swagger UI**

**Deliverable:**
- Schemas defined
- CRUD functions implemented
- 3 endpoints working (POST, GET list, GET detail)

**Time spent**: _____ hours

---

## Day 4: Alembic Migrations + More Models

### Morning: Set up Alembic (2-3 hours)

**Step 1: Initialize Alembic**
```bash
alembic init alembic
```

**Step 2: Configure `alembic/env.py`**
```python
from database import Base
from models import Course  # Import models

target_metadata = Base.metadata
```

**Step 3: Configure Database URL**
In `alembic.ini`, comment out:
```ini
# sqlalchemy.url = driver://user:pass@localhost/dbname
```

In `alembic/env.py`:
```python
from database import DATABASE_URL
config.set_main_option("sqlalchemy.url", DATABASE_URL)
```

**Step 4: Create Migration**
```bash
alembic revision --autogenerate -m "create courses table"
alembic upgrade head
```

### Afternoon: Add Topic and Question Models (2-3 hours)

**Step 1: Update `models.py`**
```python
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Topic(Base):
    __tablename__ = "topics"
    
    topic_id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.course_id", ondelete="CASCADE"))
    topic_name = Column(String(255), nullable=False)
    order_index = Column(Integer)
    
    course = relationship("Course", back_populates="topics")
    questions = relationship("Question", back_populates="topic")

class Question(Base):
    __tablename__ = "questions"
    
    question_id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.course_id"))
    topic_id = Column(Integer, ForeignKey("topics.topic_id"))
    question_text = Column(Text, nullable=False)
    difficulty = Column(String(20))
    marks = Column(Integer)
    year = Column(Integer)
    
    course = relationship("Course", back_populates="questions")
    topic = relationship("Topic", back_populates="questions")

# Update Course
Course.topics = relationship("Topic", back_populates="course")
Course.questions = relationship("Question", back_populates="course")
```

**Step 2: Create Migration**
```bash
alembic revision --autogenerate -m "add topics and questions tables"
alembic upgrade head
```

**Deliverable:**
- Alembic configured
- Migrations working
- 3 tables created

**Time spent**: _____ hours

---

## Day 5: Complete CRUD for All Resources

### All Day: Build Remaining Endpoints (6-8 hours)

**Step 1: Topics CRUD**
- Create `schemas.py` entries for Topic
- Create `crud.py` functions for Topic
- Add endpoints to `main.py`

**Step 2: Questions CRUD**
- Create schemas for Question
- Create CRUD functions
- Add endpoints

**Step 3: Test Everything**
- Use Swagger UI
- Test all CRUD operations
- Test error cases (404, validation errors)

**Step 4: Advanced Queries**
```python
@app.get("/courses/{course_id}/topics")
def get_course_topics(course_id: int, db: Session = Depends(get_db)):
    course = crud.get_course(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course.topics
```

**Deliverable:**
- Full CRUD for courses, topics, questions
- Relationship queries working
- All endpoints tested

**Time spent**: _____ hours

---

## Day 6: Remaining Models + Error Handling

### Morning: Add Resource Models (3-4 hours)

**Step 1: Add to `models.py`**
```python
class Resource(Base):
    __tablename__ = "resources"
    
    resource_id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.course_id"))
    title = Column(String(255), nullable=False)
    resource_type = Column(String(50))
    url = Column(Text)
    
    course = relationship("Course", back_populates="resources")
    chunks = relationship("ResourceChunk", back_populates="resource")

class ResourceChunk(Base):
    __tablename__ = "resource_chunks"
    
    chunk_id = Column(Integer, primary_key=True)
    resource_id = Column(Integer, ForeignKey("resources.resource_id"))
    chunk_number = Column(Integer, nullable=False)
    chunk_text = Column(Text, nullable=False)
    
    resource = relationship("Resource", back_populates="chunks")
```

**Step 2: Migrate**
```bash
alembic revision --autogenerate -m "add resources and chunks"
alembic upgrade head
```

### Afternoon: Error Handling (2-3 hours)

**Step 1: Custom Exception Handlers**
```python
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={"detail": "Resource not found"}
    )
```

**Step 2: Input Validation**
Pydantic handles this automatically!

**Deliverable:**
- All models complete
- Error handling improved

**Time spent**: _____ hours

---

## Day 7: Testing + Documentation

### Morning: Integration Testing (3-4 hours)

**Step 1: Create Test Data**
```python
# seed_db.py
from database import SessionLocal
from models import Course, Topic, Question

db = SessionLocal()

# Create courses
cs201 = Course(course_code="CS201", title="Database Systems", credits=3)
cs202 = Course(course_code="CS202", title="Data Structures", credits=3)
db.add_all([cs201, cs202])
db.commit()

# Create topics
topic1 = Topic(course_id=cs201.course_id, topic_name="SQL", order_index=1)
topic2 = Topic(course_id=cs201.course_id, topic_name="ER Model", order_index=2)
db.add_all([topic1, topic2])
db.commit()

# Create questions
q1 = Question(
    course_id=cs201.course_id,
    topic_id=topic1.topic_id,
    question_text="What is SQL?",
    difficulty="easy",
    marks=5
)
db.add(q1)
db.commit()

db.close()
```

**Step 2: Test All Endpoints**
- Use Postman or curl
- Test happy paths
- Test error cases

### Afternoon: Documentation (2-3 hours)

**Step 1: Update README.md**
Document:
- Installation steps
- Database setup
- Running the app
- API endpoints

**Step 2: API Documentation**
FastAPI auto-generates docs, but add descriptions:
```python
@app.post(
    "/courses",
    response_model=CourseRead,
    summary="Create a new course",
    description="Create a new course with course code, title, and credits"
)
```

**Deliverable:**
- Test data seeded
- All endpoints verified
- Documentation complete

**Time spent**: _____ hours

---

## Week 5 Deliverables Checklist

- [ ] PostgreSQL installed and configured
- [ ] Database and user created
- [ ] FastAPI project structure set up
- [ ] All models defined (Course, Topic, Question, Resource, ResourceChunk)
- [ ] Relationships configured
- [ ] Alembic migrations working
- [ ] CRUD endpoints for all resources
- [ ] Error handling implemented
- [ ] Swagger UI documentation accessible
- [ ] Test data seeded
- [ ] README with setup instructions

---

**Next Week**: Week 6 - Advanced SQL (Views, Triggers, Stored Procedures)

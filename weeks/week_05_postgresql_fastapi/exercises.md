# Week 5: PostgreSQL + FastAPI Exercises

## 🎯 Exercise Goals

These exercises bridge database theory to backend implementation:
- Install and configure PostgreSQL
- Build FastAPI applications
- Define SQLAlchemy ORM models
- Create database migrations
- Implement CRUD API endpoints
- Test with real HTTP requests

---

## Exercise Set 1: PostgreSQL Setup

### Exercise 1.1: Install PostgreSQL

**Tasks:**
1. Install PostgreSQL on your system
   - **macOS**: `brew install postgresql@15`
   - **Ubuntu**: `sudo apt install postgresql-15`
   - **Windows**: Download installer from postgresql.org

2. Verify installation:
```bash
psql --version
# Should output: psql (PostgreSQL) 15.x
```

3. Start PostgreSQL service:
```bash
# macOS (Homebrew)
brew services start postgresql@15

# Ubuntu
sudo systemctl start postgresql

# Windows
# Service starts automatically
```

### Exercise 1.2: Create Database and User

**Tasks:**
1. Connect to PostgreSQL as superuser:
```bash
psql postgres
```

2. Create database:
```sql
CREATE DATABASE coursedb_dev;
\l  -- List databases (verify creation)
```

3. Create user with password:
```sql
CREATE USER coursedb_user WITH PASSWORD 'secure_password123';
```

4. Grant privileges:
```sql
GRANT ALL PRIVILEGES ON DATABASE coursedb_dev TO coursedb_user;
\q  -- Quit
```

5. Test connection as new user:
```bash
psql -U coursedb_user -d coursedb_dev -h localhost
# Enter password when prompted
```

**Validation:**
- [ ] PostgreSQL installed
- [ ] Database `coursedb_dev` exists
- [ ] User `coursedb_user` can connect
- [ ] User has proper permissions

---

## Exercise Set 2: FastAPI Hello World

### Exercise 2.1: Project Setup

**Tasks:**
1. Create project directory:
```bash
mkdir coursedb-backend
cd coursedb-backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Install FastAPI and dependencies:
```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv pydantic-settings
```

4. Create `main.py`:
```python
from fastapi import FastAPI

app = FastAPI(title="CourseDB API")

@app.get("/")
def read_root():
    return {"message": "Welcome to CourseDB API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
```

5. Run the server:
```bash
uvicorn main:app --reload
```

6. Test endpoints:
   - Open browser: http://localhost:8000
   - View docs: http://localhost:8000/docs

**Validation:**
- [ ] Project created
- [ ] Dependencies installed
- [ ] Server runs without errors
- [ ] Swagger UI accessible
- [ ] Endpoints respond correctly

### Exercise 2.2: Path and Query Parameters

**Add to main.py:**
```python
@app.get("/courses/{course_id}")
def get_course(course_id: int):
    return {"course_id": course_id, "message": f"Fetching course {course_id}"}

@app.get("/courses")
def list_courses(skip: int = 0, limit: int = 10):
    return {
        "skip": skip,
        "limit": limit,
        "message": f"Listing courses from {skip} with limit {limit}"
    }
```

**Test:**
- Visit: http://localhost:8000/courses/5
- Visit: http://localhost:8000/courses?skip=10&limit=20
- Use Swagger UI to test with different values

---

## Exercise Set 3: SQLAlchemy Models

### Exercise 3.1: Database Connection

**Create `database.py`:**
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://coursedb_user:secure_password123@localhost:5432/coursedb_dev"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**Test connection:**
```python
# test_connection.py
from database import engine
from sqlalchemy import text

with engine.connect() as conn:
    result = conn.execute(text("SELECT version()"))
    print(result.fetchone())
```

### Exercise 3.2: Define Course Model

**Create `models.py`:**
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

    def __repr__(self):
        return f"<Course(id={self.course_id}, code='{self.course_code}')>"
```

**Create tables:**
```python
# In Python shell or script
from database import engine, Base
from models import Course

Base.metadata.create_all(bind=engine)
```

**Verify in PostgreSQL:**
```sql
psql -U coursedb_user -d coursedb_dev
\dt  -- List tables
\d courses  -- Describe courses table
```

### Exercise 3.3: CRUD Operations with ORM

**Create `crud.py`:**
```python
from sqlalchemy.orm import Session
from models import Course

def create_course(db: Session, course_code: str, title: str, credits: int):
    course = Course(course_code=course_code, title=title, credits=credits)
    db.add(course)
    db.commit()
    db.refresh(course)
    return course

def get_course(db: Session, course_id: int):
    return db.query(Course).filter(Course.course_id == course_id).first()

def list_courses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Course).offset(skip).limit(limit).all()

def update_course(db: Session, course_id: int, title: str):
    course = db.query(Course).filter(Course.course_id == course_id).first()
    if course:
        course.title = title
        db.commit()
        db.refresh(course)
    return course

def delete_course(db: Session, course_id: int):
    course = db.query(Course).filter(Course.course_id == course_id).first()
    if course:
        db.delete(course)
        db.commit()
    return course
```

**Test CRUD:**
```python
from database import SessionLocal
from crud import *

db = SessionLocal()

# Create
course = create_course(db, "CS201", "Database Systems", 3)
print(f"Created: {course}")

# Read
course = get_course(db, 1)
print(f"Retrieved: {course}")

# Update
course = update_course(db, 1, "Database Management Systems")
print(f"Updated: {course}")

# List
courses = list_courses(db)
print(f"All courses: {courses}")

# Delete
delete_course(db, 1)
print("Deleted")

db.close()
```

---

## Exercise Set 4: Pydantic Schemas

### Exercise 4.1: Define Schemas

**Create `schemas.py`:**
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
    course_code: Optional[str] = Field(None, max_length=20)
    title: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    credits: Optional[int] = Field(None, ge=0, le=10)

class CourseRead(CourseBase):
    course_id: int

    class Config:
        from_attributes = True  # Allows reading from ORM models
```

**Why Pydantic?**
- Automatic validation
- Type checking
- JSON serialization
- Clear API documentation

---

## Exercise Set 5: CRUD API Endpoints

### Exercise 5.1: Course API

**Update `main.py`:**
```python
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import Course
from schemas import CourseCreate, CourseRead, CourseUpdate

app = FastAPI(title="CourseDB API")

@app.post("/courses", response_model=CourseRead, status_code=201)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    # Check if course_code already exists
    existing = db.query(Course).filter(Course.course_code == course.course_code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Course code already exists")
    
    db_course = Course(**course.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

@app.get("/courses", response_model=List[CourseRead])
def list_courses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    courses = db.query(Course).offset(skip).limit(limit).all()
    return courses

@app.get("/courses/{course_id}", response_model=CourseRead)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.course_id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@app.put("/courses/{course_id}", response_model=CourseRead)
def update_course(course_id: int, course_update: CourseUpdate, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.course_id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    for field, value in course_update.dict(exclude_unset=True).items():
        setattr(course, field, value)
    
    db.commit()
    db.refresh(course)
    return course

@app.delete("/courses/{course_id}", status_code=204)
def delete_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.course_id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    db.delete(course)
    db.commit()
    return None
```

**Test with Swagger UI:**
1. Go to http://localhost:8000/docs
2. Test POST /courses (create a course)
3. Test GET /courses (list all courses)
4. Test GET /courses/{id} (get specific course)
5. Test PUT /courses/{id} (update course)
6. Test DELETE /courses/{id} (delete course)

---

## Exercise Set 6: Relationships

### Exercise 6.1: Add Topic Model

**Add to `models.py`:**
```python
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Topic(Base):
    __tablename__ = "topics"

    topic_id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.course_id", ondelete="CASCADE"), nullable=False)
    topic_name = Column(String(255), nullable=False)
    order_index = Column(Integer)

    # Relationships
    course = relationship("Course", back_populates="topics")

# Update Course model
Course.topics = relationship("Topic", back_populates="course", cascade="all, delete-orphan")
```

**Create tables:**
```python
Base.metadata.create_all(bind=engine)
```

### Exercise 6.2: Test Relationships

**Create topic with course:**
```python
from models import Course, Topic

db = SessionLocal()

# Create course
course = Course(course_code="CS201", title="DBMS", credits=3)
db.add(course)
db.commit()

# Create topics
topic1 = Topic(course_id=course.course_id, topic_name="SQL Basics", order_index=1)
topic2 = Topic(course_id=course.course_id, topic_name="ER Modeling", order_index=2)

db.add_all([topic1, topic2])
db.commit()

# Query with relationship
course = db.query(Course).filter(Course.course_id == 1).first()
print(f"Course: {course.title}")
print(f"Topics: {[t.topic_name for t in course.topics]}")

db.close()
```

---

## Exercise Set 7: Alembic Migrations

### Exercise 7.1: Initialize Alembic

**Install Alembic:**
```bash
pip install alembic
```

**Initialize:**
```bash
alembic init alembic
```

**Configure `alembic.ini`:**
```ini
# Comment out this line:
# sqlalchemy.url = driver://user:pass@localhost/dbname

# We'll use env.py instead
```

**Configure `alembic/env.py`:**
```python
from database import Base
from models import Course, Topic  # Import all models

# Add to target_metadata
target_metadata = Base.metadata
```

### Exercise 7.2: Create Migration

**Generate migration:**
```bash
alembic revision --autogenerate -m "create courses and topics tables"
```

**Review the migration file** in `alembic/versions/`

**Apply migration:**
```bash
alembic upgrade head
```

**Verify:**
```sql
psql -U coursedb_user -d coursedb_dev
\dt  -- Should show courses and topics tables
```

### Exercise 7.3: Modify Schema

**Add column to Course model:**
```python
class Course(Base):
    # ... existing columns ...
    semester = Column(String(20))  # New column
```

**Create migration:**
```bash
alembic revision --autogenerate -m "add semester to courses"
```

**Apply:**
```bash
alembic upgrade head
```

**Rollback:**
```bash
alembic downgrade -1
```

---

## Challenge Problems

### Challenge 1: Complete CourseDB-AI Models

**Tasks:**
1. Define all models (Course, Topic, Question, Resource, ResourceChunk, User, SearchLog)
2. Configure all relationships
3. Create migrations
4. Verify all tables created

### Challenge 2: Full CRUD for All Resources

**Tasks:**
1. Create Pydantic schemas for all models
2. Implement CRUD endpoints for topics
3. Implement CRUD endpoints for questions
4. Test all endpoints with Swagger UI

### Challenge 3: Advanced Queries

**Tasks:**
1. Get all topics for a specific course
2. Get all questions for a specific topic
3. Search questions by difficulty level
4. Count questions per course
5. Get courses with topic count

**Example:**
```python
@app.get("/courses/{course_id}/topics")
def get_course_topics(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.course_id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course.topics
```

---

## Self-Assessment Checklist

After completing these exercises, verify you can:

- [ ] Install and configure PostgreSQL
- [ ] Create databases and users
- [ ] Set up FastAPI project structure
- [ ] Define SQLAlchemy models
- [ ] Configure database connections
- [ ] Create database migrations
- [ ] Implement CRUD operations
- [ ] Define Pydantic schemas for validation
- [ ] Build API endpoints with proper error handling
- [ ] Test APIs with Swagger UI
- [ ] Handle database sessions correctly
- [ ] Configure foreign keys and relationships
- [ ] Use dependency injection

---

## Tips and Best Practices

1. **Always use environment variables** for database credentials
2. **Review auto-generated migrations** before applying
3. **Use database sessions properly** with try/finally
4. **Handle errors gracefully** with appropriate HTTP status codes
5. **Test endpoints incrementally** - don't build everything at once
6. **Use Swagger UI** for interactive testing
7. **Check PostgreSQL logs** when debugging connection issues

---

**Next Steps:** After completing exercises, move to `implementation_plan.md` for the 7-day guided implementation!

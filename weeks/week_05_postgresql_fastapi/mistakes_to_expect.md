# Week 5: Common PostgreSQL + FastAPI Mistakes

## 🎯 Purpose

Backend development involves many new tools and concepts. This guide documents common mistakes and how to fix them quickly.

---

## Mistake Category 1: PostgreSQL Setup Errors

### ❌ Mistake 1.1: PostgreSQL Not Running

**Error:**
```
psql: error: connection to server on socket "/tmp/.s.PGSQL.5432" failed: No such file or directory
```

**Cause:** PostgreSQL service not started

**Fix:**
```bash
# macOS
brew services start postgresql@15

# Ubuntu
sudo systemctl start postgresql
sudo systemctl status postgresql

# Check if running
psql postgres
```

---

### ❌ Mistake 1.2: Permission Denied

**Error:**
```
FATAL: permission denied for database "coursedb_dev"
```

**Cause:** User lacks privileges

**Fix:**
```sql
psql postgres
GRANT ALL PRIVILEGES ON DATABASE coursedb_dev TO coursedb_user;
GRANT ALL ON SCHEMA public TO coursedb_user;
```

---

### ❌ Mistake 1.3: Wrong Connection String

**Error:**
```
sqlalchemy.exc.OperationalError: could not connect to server
```

**Common mistakes:**
```python
# WRONG formats:
"postgres://..."  # Should be postgresql://
"postgresql://user@host/db"  # Missing password
"postgresql://user:pass@host:5432"  # Missing database name
"postgresql://user:pass@localhost/db"  # Missing port

# CORRECT:
"postgresql://user:password@host:5432/database"
"postgresql://coursedb_user:pass123@localhost:5432/coursedb_dev"
```

---

## Mistake Category 2: FastAPI Application Errors

### ❌ Mistake 2.1: Import Errors

**Error:**
```
ImportError: cannot import name 'FastAPI' from 'fastapi'
```

**Cause:** FastAPI not installed or wrong virtual environment

**Fix:**
```bash
# Activate venv
source venv/bin/activate

# Install
pip install fastapi uvicorn

# Verify
pip list | grep fastapi
```

---

### ❌ Mistake 2.2: Uvicorn Can't Find App

**Error:**
```
Error loading ASGI app. Could not import module "main".
```

**Cause:** Running uvicorn from wrong directory or wrong app path

**Fix:**
```bash
# Ensure you're in project directory
cd /path/to/project

# Correct syntax: module:app_variable
uvicorn main:app --reload

# If app is in subdirectory:
uvicorn app.main:app --reload
```

---

### ❌ Mistake 2.3: Port Already in Use

**Error:**
```
ERROR: [Errno 48] Address already in use
```

**Fix:**
```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>

# Or use different port
uvicorn main:app --port 8001
```

---

## Mistake Category 3: SQLAlchemy Model Errors

### ❌ Mistake 3.1: Missing `__tablename__`

**Error:**
```
sqlalchemy.exc.InvalidRequestError: Class <Course> does not have a __table__ or __tablename__ specified
```

**Wrong:**
```python
class Course(Base):
    course_id = Column(Integer, primary_key=True)
```

**Correct:**
```python
class Course(Base):
    __tablename__ = "courses"  # REQUIRED
    course_id = Column(Integer, primary_key=True)
```

---

### ❌ Mistake 3.2: Circular Import with Relationships

**Error:**
```
NameError: name 'Topic' is not defined
```

**Cause:** Models import each other

**Fix:**
Use string references in relationships:
```python
class Course(Base):
    topics = relationship("Topic", back_populates="course")  # String!

class Topic(Base):
    course = relationship("Course", back_populates="topics")
```

---

### ❌ Mistake 3.3: Forgetting to Import Models

**Error:**
Tables not created even after `Base.metadata.create_all()`

**Cause:** Models not imported before creating tables

**Fix:**
```python
from database import engine, Base
from models import Course, Topic, Question  # Import ALL models

Base.metadata.create_all(bind=engine)
```

---

## Mistake Category 4: Database Session Errors

### ❌ Mistake 4.1: Session Not Closed

**Problem:** Database connections leak, eventually exhausting connection pool

**Wrong:**
```python
def get_courses():
    db = SessionLocal()
    courses = db.query(Course).all()
    return courses  # Session never closed!
```

**Correct:**
```python
def get_courses(db: Session = Depends(get_db)):
    return db.query(Course).all()
    # Dependency handles closing

# Or manually:
db = SessionLocal()
try:
    courses = db.query(Course).all()
finally:
    db.close()
```

---

### ❌ Mistake 4.2: Using Closed Session

**Error:**
```
sqlalchemy.exc.InvalidRequestError: This Session's transaction has been rolled back
```

**Cause:** Trying to access object after session closed

**Fix:**
```python
# WRONG
course = db.query(Course).first()
db.close()
print(course.title)  # ERROR! Session closed

# CORRECT
course = db.query(Course).first()
title = course.title  # Access while session open
db.close()
print(title)  # OK
```

---

### ❌ Mistake 4.3: Forgetting `db.commit()`

**Problem:** Changes not persisted to database

**Wrong:**
```python
def create_course(db: Session, course: CourseCreate):
    db_course = Course(**course.dict())
    db.add(db_course)
    # Missing commit!
    return db_course
```

**Correct:**
```python
def create_course(db: Session, course: CourseCreate):
    db_course = Course(**course.dict())
    db.add(db_course)
    db.commit()  # REQUIRED
    db.refresh(db_course)  # Get auto-generated ID
    return db_course
```

---

## Mistake Category 5: Pydantic Schema Errors

### ❌ Mistake 5.1: Missing `from_attributes`

**Error:**
```
pydantic.error_wrappers.ValidationError: value is not a valid dict
```

**Cause:** Returning SQLAlchemy model without config

**Fix:**
```python
class CourseRead(BaseModel):
    course_id: int
    title: str

    class Config:
        from_attributes = True  # REQUIRED for ORM models
```

---

### ❌ Mistake 5.2: Wrong Field Types

**Error:**
```
pydantic.error_wrappers.ValidationError: value is not a valid integer
```

**Cause:** Type mismatch between schema and data

**Fix:**
```python
# Schema says int, but data is string
class CourseCreate(BaseModel):
    credits: int  # But form sends "3" (string)

# Solution: Pydantic coerces automatically, but be explicit:
from pydantic import validator

@validator('credits', pre=True)
def coerce_credits(cls, v):
    if isinstance(v, str):
        return int(v)
    return v
```

---

## Mistake Category 6: API Endpoint Errors

### ❌ Mistake 6.1: Missing `response_model`

**Problem:** API returns SQLAlchemy model with extra fields

**Wrong:**
```python
@app.get("/courses/{course_id}")
def get_course(course_id: int, db: Session = Depends(get_db)):
    return db.query(Course).first()  # Returns extra fields!
```

**Correct:**
```python
@app.get("/courses/{course_id}", response_model=CourseRead)
def get_course(course_id: int, db: Session = Depends(get_db)):
    return db.query(Course).first()  # Filtered by schema
```

---

### ❌ Mistake 6.2: Not Handling 404

**Problem:** Returns None instead of 404 error

**Wrong:**
```python
@app.get("/courses/{course_id}")
def get_course(course_id: int, db: Session = Depends(get_db)):
    return db.query(Course).first()  # Returns None if not found
```

**Correct:**
```python
from fastapi import HTTPException

@app.get("/courses/{course_id}")
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course
```

---

### ❌ Mistake 6.3: Wrong HTTP Methods

**Wrong:**
```python
@app.get("/courses")  # Should be POST
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    # ...
```

**Correct:**
```python
@app.post("/courses", status_code=201)  # POST for creation
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    # ...

@app.put("/courses/{id}")  # PUT for update
def update_course(id: int, course: CourseUpdate, db: Session = Depends(get_db)):
    # ...

@app.delete("/courses/{id}", status_code=204)  # DELETE for removal
def delete_course(id: int, db: Session = Depends(get_db)):
    # ...
```

---

## Mistake Category 7: Foreign Key Errors

### ❌ Mistake 7.1: Violating Foreign Key Constraint

**Error:**
```
sqlalchemy.exc.IntegrityError: FOREIGN KEY constraint failed
```

**Cause:** Trying to insert topic with non-existent course_id

**Fix:**
```python
# Check if course exists first
def create_topic(db: Session, topic: TopicCreate):
    course = db.query(Course).filter(Course.course_id == topic.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    db_topic = Topic(**topic.dict())
    db.add(db_topic)
    db.commit()
    return db_topic
```

---

### ❌ Mistake 7.2: Cascade Delete Issues

**Problem:** Deleting course fails because topics exist

**Fix:**
```python
class Topic(Base):
    course_id = Column(
        Integer,
        ForeignKey("courses.course_id", ondelete="CASCADE"),  # Add CASCADE
        nullable=False
    )
```

---

## Mistake Category 8: Alembic Migration Errors

### ❌ Mistake 8.1: Migration Not Detected

**Problem:** `alembic revision --autogenerate` finds no changes

**Causes:**
1. Models not imported in `alembic/env.py`
2. `target_metadata` not set

**Fix:**
```python
# alembic/env.py
from database import Base
from models import Course, Topic, Question  # Import all models

target_metadata = Base.metadata  # Set metadata
```

---

### ❌ Mistake 8.2: Migration Fails to Apply

**Error:**
```
sqlalchemy.exc.ProgrammingError: (psycopg2.errors.DuplicateTable) relation "courses" already exists
```

**Cause:** Table already exists from manual `create_all()`

**Fix:**
```bash
# Drop all tables and start fresh
psql -U coursedb_user -d coursedb_dev
DROP TABLE IF EXISTS questions, topics, courses CASCADE;

# Run migrations
alembic upgrade head
```

---

## Debugging Checklist

When something goes wrong:

### ✅ PostgreSQL Issues:
- [ ] Is PostgreSQL running? (`psql postgres`)
- [ ] Does database exist? (`\l`)
- [ ] Does user have permissions? (`\du`)
- [ ] Is connection string correct?

### ✅ FastAPI Issues:
- [ ] Is virtual environment activated?
- [ ] Are all dependencies installed?
- [ ] Is the server running? (check terminal)
- [ ] Is the correct port open?

### ✅ SQLAlchemy Issues:
- [ ] Are all models imported?
- [ ] Is `__tablename__` defined?
- [ ] Are sessions closed properly?
- [ ] Is `db.commit()` called?

### ✅ API Issues:
- [ ] Is `response_model` set?
- [ ] Are 404 errors handled?
- [ ] Are HTTP methods correct?
- [ ] Is input validation working?

---

## Quick Fixes

**Can't connect to PostgreSQL:**
```bash
brew services restart postgresql@15  # macOS
sudo systemctl restart postgresql    # Ubuntu
```

**Tables not appearing:**
```python
Base.metadata.create_all(bind=engine)
# Or use Alembic migrations
```

**API returning too much data:**
```python
# Add response_model
@app.get("/courses", response_model=List[CourseRead])
```

**Changes not saving:**
```python
# Add commit
db.commit()
```

---

**Next:** Complete `checkpoints.md` to track your progress!

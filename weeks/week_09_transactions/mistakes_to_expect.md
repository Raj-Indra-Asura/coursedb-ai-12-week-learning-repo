# Week 9: Transactions & Concurrency - Common Mistakes and How to Fix Them

## 🎯 Purpose

Week 9 teaches transactions and concurrency control. This guide prepares you for common mistakes with:
- ACID misunderstandings
- Concurrency bugs
- Wrong isolation levels
- Deadlock issues
- Transaction misuse in code
- Performance problems

---

## Mistake Category 1: ACID Misunderstandings

### Mistake 1.1: Forgetting to BEGIN Transaction

**What happens:**
```sql
-- Developer thinks this is atomic but it's NOT!
INSERT INTO courses VALUES (1, 'CS301', 'DBMS', 3);
INSERT INTO topics VALUES (1, 1, 'SQL', 1);

-- If second INSERT fails, first INSERT is already committed!
-- Course without topics = inconsistent data
```

**Why it's wrong:**
Each statement is auto-committed separately. No atomicity!

**How to fix:**
```sql
-- Explicit transaction
BEGIN;
    INSERT INTO courses VALUES (1, 'CS301', 'DBMS', 3);
    INSERT INTO topics VALUES (1, 1, 'SQL', 1);
COMMIT;

-- Both succeed or both fail
```

**How to avoid:**
- Always use BEGIN/COMMIT for multi-statement operations
- In SQLAlchemy, use session context manager
- Never rely on auto-commit for related operations

---

### Mistake 1.2: Confusing Isolation with Locking

**What happens:**
```python
# Developer thinks SERIALIZABLE prevents race conditions
with Session(engine) as session:
    session.connection(execution_options={"isolation_level": "SERIALIZABLE"})
    
    course = session.query(Course).filter_by(course_id=1).one()
    if course.enrolled_count < course.max_capacity:
        course.enrolled_count += 1
    session.commit()

# But two transactions can still both pass the check!
# Result: Over-enrollment (race condition)
```

**Why it's wrong:**
Isolation level doesn't lock rows. Both transactions read the same value, both pass check, both increment.

**How to fix:**
```python
# Use SELECT FOR UPDATE (explicit lock)
with Session(engine) as session:
    course = session.query(Course).filter_by(
        course_id=1
    ).with_for_update().one()  # Lock row
    
    if course.enrolled_count < course.max_capacity:
        course.enrolled_count += 1
        session.commit()
    else:
        raise CapacityExceeded()
```

**How to avoid:**
- Isolation level != locking
- Use `FOR UPDATE` for read-modify-write operations
- Understand difference between consistency and concurrency control

---

### Mistake 1.3: Assuming Durability Means No Data Loss Ever

**What happens:**
```sql
BEGIN;
    INSERT INTO courses VALUES (...);
COMMIT;

-- Developer assumes data is 100% safe forever
-- But doesn't have backups!
```

**Why it's wrong:**
Durability protects against crashes, not:
- Disk failure
- Accidental DELETE
- DROP TABLE
- Hardware destruction
- Ransomware

**How to fix:**
```sql
-- Durability provides:
-- ✅ Survives crashes
-- ✅ Survives power failure
-- ✅ Survives process kill

-- Durability does NOT provide:
-- ❌ Protection from DROP TABLE
-- ❌ Protection from disk failure
-- ❌ Protection from malicious deletion

-- You need:
-- 1. Regular backups
-- 2. Replication
-- 3. Monitoring
-- 4. Access control
```

**How to avoid:**
- Don't rely solely on durability
- Implement backup strategy
- Test disaster recovery
- Monitor disk health

---

## Mistake Category 2: Concurrency Bugs

### Mistake 2.1: Lost Update in Counter Increment

**What happens:**
```python
# Two API requests simultaneously
# Request 1:
course = session.query(Course).filter_by(course_id=1).one()
count = course.enrolled_count  # Reads 100
# Request 2 also reads 100 here!
course.enrolled_count = count + 1  # Sets to 101
session.commit()

# Request 2:
course.enrolled_count = count + 1  # Also sets to 101 (lost Request 1's increment!)
session.commit()

# Result: enrolled_count = 101 (should be 102)
```

**Why it happens:**
Both transactions read the same value before either writes.

**How to fix:**

**Solution 1: Database-level increment**
```python
# Let database handle increment atomically
session.query(Course).filter_by(course_id=1).update({
    'enrolled_count': Course.enrolled_count + 1
})
session.commit()
```

**Solution 2: SELECT FOR UPDATE**
```python
course = session.query(Course).filter_by(
    course_id=1
).with_for_update().one()  # Lock row

course.enrolled_count += 1  # Safe now
session.commit()
```

**How to avoid:**
- Never do read-modify-write without locking
- Use database expressions for counters
- Test concurrent scenarios

---

### Mistake 2.2: Not Detecting Dirty Reads

**What happens:**
```python
# Terminal 1:
session1.begin()
course.course_title = "TEMPORARY NAME"  # Not committed

# Terminal 2:
session2.begin()
course = session2.query(Course).filter_by(course_id=1).one()
print(course.course_title)  # Sees "TEMPORARY NAME" in some databases!

# Terminal 1:
session1.rollback()  # Abort

# Terminal 2 used invalid data!
```

**Why it's dangerous:**
Making decisions based on uncommitted (possibly invalid) data.

**How to fix:**
```python
# PostgreSQL prevents dirty reads by default (Read Committed)
# But be aware if using other databases or Read Uncommitted

# Explicit isolation level:
with Session(engine) as session:
    session.connection(execution_options={
        "isolation_level": "READ COMMITTED"  # Minimum!
    })
    # Now safe from dirty reads
```

**How to avoid:**
- Never use Read Uncommitted
- Understand default isolation level
- Test with multiple transactions

---

### Mistake 2.3: Unrepeatable Reads in Reports

**What happens:**
```python
# Generate monthly report
def generate_report(session):
    # First query: Get course count
    course_count = session.query(Course).count()  # Returns 100
    
    # Another user adds 10 courses here!
    
    # Second query: Get average enrollment
    avg_enrollment = session.query(
        func.avg(Course.enrolled_count)
    ).scalar()  # Now calculated with 110 courses!
    
    # Report inconsistent: count shows 100 but average uses 110
    return {
        'course_count': course_count,
        'avg_enrollment': avg_enrollment
    }
```

**Why it's wrong:**
Report uses inconsistent snapshot of data.

**How to fix:**
```python
def generate_report(session):
    # Use REPEATABLE READ for consistent snapshot
    session.connection(execution_options={
        "isolation_level": "REPEATABLE READ"
    })
    
    # All queries see same snapshot
    course_count = session.query(Course).count()
    avg_enrollment = session.query(func.avg(Course.enrolled_count)).scalar()
    
    return {
        'course_count': course_count,  # Consistent!
        'avg_enrollment': avg_enrollment
    }
```

**How to avoid:**
- Use REPEATABLE READ for reports and analytics
- Be aware that reports can be inconsistent with READ COMMITTED
- Document isolation level requirements

---

## Mistake Category 3: Wrong Isolation Levels

### Mistake 3.1: Using SERIALIZABLE for Everything

**What happens:**
```python
# Developer wants maximum safety
engine = create_engine(
    DATABASE_URL,
    isolation_level="SERIALIZABLE"  # For ALL transactions!
)

# Results:
# - 10x slower queries
# - Frequent serialization failures
# - Retries everywhere
# - Users complaining about performance
```

**Why it's wrong:**
SERIALIZABLE has high overhead. Most operations don't need it.

**How to fix:**
```python
# Default: READ COMMITTED (good for most operations)
engine = create_engine(DATABASE_URL)

# Use SERIALIZABLE only when needed
def critical_operation(session):
    session.connection(execution_options={
        "isolation_level": "SERIALIZABLE"
    })
    # Complex multi-step transaction
    
# Most operations use default (fast)
```

**Rule of thumb:**
- READ COMMITTED: 95% of operations
- REPEATABLE READ: Reports, analytics
- SERIALIZABLE: Critical business logic (inventory, money)

---

### Mistake 3.2: Using READ COMMITTED for Analytics

**What happens:**
```python
# Generate analytics dashboard
def get_dashboard_data(session):
    # Query 1: Total courses
    total = session.query(Course).count()  # Returns 100
    
    # New courses added here!
    
    # Query 2: Courses by department
    by_dept = session.query(
        Course.department,
        func.count(Course.course_id)
    ).group_by(Course.department).all()
    # Returns counts that sum to 105!
    
    # Dashboard shows: "Total: 100" but department counts sum to 105
    # Confusing for users!
```

**Why it's wrong:**
Analytics needs consistent snapshot.

**How to fix:**
```python
def get_dashboard_data(session):
    # Use REPEATABLE READ for consistent snapshot
    session.connection(execution_options={
        "isolation_level": "REPEATABLE READ"
    })
    
    total = session.query(Course).count()
    by_dept = session.query(
        Course.department,
        func.count(Course.course_id)
    ).group_by(Course.department).all()
    
    # Both queries see same snapshot - counts match!
```

**How to avoid:**
- Use REPEATABLE READ for any multi-query analytics
- Document why isolation level chosen
- Test with concurrent updates

---

## Mistake Category 4: Deadlock Issues

### Mistake 4.1: Not Handling Deadlocks

**What happens:**
```python
def transfer_enrollment(from_course_id, to_course_id):
    with Session(engine) as session:
        # Lock in unpredictable order
        from_course = session.query(Course).filter_by(
            course_id=from_course_id
        ).with_for_update().one()
        
        to_course = session.query(Course).filter_by(
            course_id=to_course_id
        ).with_for_update().one()
        
        # Transfer
        from_course.enrolled_count -= 1
        to_course.enrolled_count += 1
        
        session.commit()
        # ERROR: deadlock detected (if two transfers run simultaneously)
        # Application crashes!
```

**Why it's wrong:**
No retry logic. Deadlocks cause failures.

**How to fix:**
```python
import time
from sqlalchemy.exc import DBAPIError

def transfer_enrollment(from_course_id, to_course_id, max_retries=3):
    for attempt in range(max_retries):
        try:
            with Session(engine) as session:
                # Lock in consistent order (by ID)
                ids = sorted([from_course_id, to_course_id])
                courses = session.query(Course).filter(
                    Course.course_id.in_(ids)
                ).with_for_update().all()
                
                course_map = {c.course_id: c for c in courses}
                from_course = course_map[from_course_id]
                to_course = course_map[to_course_id]
                
                from_course.enrolled_count -= 1
                to_course.enrolled_count += 1
                
                session.commit()
                return True
                
        except DBAPIError as e:
            if 'deadlock' in str(e).lower():
                if attempt < max_retries - 1:
                    wait = 0.1 * (2 ** attempt)  # Exponential backoff
                    time.sleep(wait)
                    continue
            raise
    
    return False
```

**How to avoid:**
- Always handle deadlock exceptions
- Implement retry with exponential backoff
- Lock resources in consistent order
- Log deadlocks for analysis

---

### Mistake 4.2: Creating Deadlocks with Inconsistent Lock Order

**What happens:**
```python
# Function 1: Transfer from A to B
def transfer_a_to_b():
    lock(course_a)  # Lock A first
    lock(course_b)  # Then B
    # Transfer

# Function 2: Transfer from B to A
def transfer_b_to_a():
    lock(course_b)  # Lock B first
    lock(course_a)  # Then A
    # Transfer

# Called simultaneously = DEADLOCK!
```

**Why it happens:**
Transactions lock resources in different order.

**How to fix:**
```python
def transfer(from_id, to_id):
    # ALWAYS lock in same order (e.g., by ID)
    ids = sorted([from_id, to_id])
    
    courses = session.query(Course).filter(
        Course.course_id.in_(ids)
    ).order_by(Course.course_id).with_for_update().all()
    
    # Now safe - always lock lower ID first
```

**How to avoid:**
- Document lock ordering convention
- Always lock in consistent order (by ID, by name, etc.)
- Use a helper function for multi-resource locking
- Code review for lock order

---

### Mistake 4.3: Holding Locks Too Long

**What happens:**
```python
@app.post("/api/courses/{course_id}/enroll")
def enroll_student(course_id: int, student: Student):
    with Session(engine) as session:
        # Lock course
        course = session.query(Course).filter_by(
            course_id=course_id
        ).with_for_update().one()
        
        # Send confirmation email (takes 5 seconds!)
        send_email(student.email, f"Enrolled in {course.course_title}")
        
        # Update enrollment
        course.enrolled_count += 1
        session.commit()
        
    # Course was locked for 5 seconds!
    # Other enrollments waited 5 seconds!
```

**Why it's wrong:**
Long transactions hold locks, blocking other transactions.

**How to fix:**
```python
@app.post("/api/courses/{course_id}/enroll")
def enroll_student(course_id: int, student: Student):
    # Separate transaction from external calls
    with Session(engine) as session:
        course = session.query(Course).filter_by(
            course_id=course_id
        ).with_for_update().one()
        
        course.enrolled_count += 1
        course_title = course.course_title
        session.commit()
    
    # Release lock before external call
    send_email(student.email, f"Enrolled in {course_title}")
```

**How to avoid:**
- Keep transactions short
- Never do I/O during transaction (email, HTTP calls, file ops)
- Don't wait for user input during transaction
- Monitor transaction duration

---

## Mistake Category 5: Transaction Misuse in Code

### Mistake 5.1: Not Rolling Back on Error

**What happens:**
```python
def create_course_with_topics(course_data, topics):
    session = Session(engine)
    
    # Create course
    course = Course(**course_data)
    session.add(course)
    session.flush()
    
    # Create topics
    for topic in topics:
        t = Topic(course_id=course.course_id, **topic)
        session.add(t)
    
    session.commit()
    # If error occurs, session is left in invalid state!
    # No rollback!
```

**Why it's wrong:**
If exception occurs, transaction is not rolled back. Session is corrupted.

**How to fix:**
```python
def create_course_with_topics(course_data, topics):
    session = Session(engine)
    try:
        course = Course(**course_data)
        session.add(course)
        session.flush()
        
        for topic in topics:
            t = Topic(course_id=course.course_id, **topic)
            session.add(t)
        
        session.commit()
    except Exception:
        session.rollback()  # Always rollback on error
        raise
    finally:
        session.close()

# Or use context manager (automatic!)
with Session(engine) as session:
    # Auto-rollback on exception
    # Auto-close on exit
```

**How to avoid:**
- Always use try/except with rollback
- Or use context manager (automatic cleanup)
- Never leave session in invalid state

---

### Mistake 5.2: Mixing Business Logic with Transactions

**What happens:**
```python
def enroll_student(course_id, student_id):
    with Session(engine) as session:
        course = session.query(Course).filter_by(
            course_id=course_id
        ).with_for_update().one()
        
        # Complex business logic inside transaction
        if course.enrolled_count >= course.max_capacity:
            raise CapacityExceeded()
        
        # Check prerequisites (queries other tables)
        student = session.query(Student).filter_by(id=student_id).one()
        prereqs = get_prerequisites(course_id)  # Complex function
        completed = get_completed_courses(student_id)  # Another complex function
        
        if not all(p in completed for p in prereqs):
            raise PrerequisiteNotMet()
        
        # Validate schedule conflicts
        conflicts = check_schedule_conflicts(student_id, course.schedule)
        if conflicts:
            raise ScheduleConflict()
        
        # Finally enroll
        course.enrolled_count += 1
        session.commit()
    
    # Transaction held lock for entire validation process!
```

**Why it's wrong:**
Long transaction holds locks while doing complex validation.

**How to fix:**
```python
def enroll_student(course_id, student_id):
    # Validation first (no locks)
    with Session(engine) as session:
        course = session.query(Course).filter_by(course_id=course_id).one()
        student = session.query(Student).filter_by(id=student_id).one()
        
        # All validations (no locks held)
        if course.enrolled_count >= course.max_capacity:
            raise CapacityExceeded()
        
        prereqs = get_prerequisites(course_id)
        completed = get_completed_courses(student_id)
        if not all(p in completed for p in prereqs):
            raise PrerequisiteNotMet()
        
        conflicts = check_schedule_conflicts(student_id, course.schedule)
        if conflicts:
            raise ScheduleConflict()
    
    # Quick transaction with lock
    with Session(engine) as session:
        course = session.query(Course).filter_by(
            course_id=course_id
        ).with_for_update().one()
        
        # Double-check capacity (might have changed)
        if course.enrolled_count >= course.max_capacity:
            raise CapacityExceeded()
        
        course.enrolled_count += 1
        session.commit()
```

**How to avoid:**
- Validate before locking
- Keep locked section minimal
- Separate read-only checks from updates
- Re-check conditions after locking

---

### Mistake 5.3: Forgetting to Close Sessions

**What happens:**
```python
def get_course(course_id):
    session = Session(engine)
    course = session.query(Course).filter_by(course_id=course_id).one()
    return course
    # Session never closed!
    # Connection leak!

# After 100 requests:
# ERROR: Too many connections
```

**Why it's wrong:**
Unclosed sessions leak database connections. Pool exhausted.

**How to fix:**
```python
# Option 1: Context manager (recommended)
def get_course(course_id):
    with Session(engine) as session:
        course = session.query(Course).filter_by(course_id=course_id).one()
        # Make sure to access needed attributes before session closes
        course_data = {
            'id': course.course_id,
            'title': course.course_title
        }
        return course_data
    # Session automatically closed

# Option 2: try/finally
def get_course(course_id):
    session = Session(engine)
    try:
        course = session.query(Course).filter_by(course_id=course_id).one()
        return course
    finally:
        session.close()  # Always closes

# Option 3: FastAPI dependency
def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()

@app.get("/courses/{course_id}")
def read_course(course_id: int, db: Session = Depends(get_db)):
    return db.query(Course).filter_by(course_id=course_id).one()
```

**How to avoid:**
- Always use context manager or try/finally
- Use FastAPI dependency injection
- Monitor connection pool usage
- Set pool size limits

---

## Mistake Category 6: Performance Problems

### Mistake 6.1: Too Many Small Transactions

**What happens:**
```python
# Inserting 1000 questions
for question_data in questions:
    with Session(engine) as session:
        question = Question(**question_data)
        session.add(question)
        session.commit()  # 1000 commits!
        
# Extremely slow: Each commit flushes to disk
# 1000 questions take 10 seconds
```

**Why it's wrong:**
Each commit is expensive (disk write). Too much overhead.

**How to fix:**
```python
# Batch commits
with Session(engine) as session:
    for question_data in questions:
        question = Question(**question_data)
        session.add(question)
    
    session.commit()  # Single commit
    # 1000 questions in 0.5 seconds

# Or use bulk operations
with Session(engine) as session:
    session.bulk_insert_mappings(Question, questions)
    session.commit()
    # Even faster!
```

**How to avoid:**
- Batch related operations in single transaction
- Use bulk operations for large inserts
- Don't commit after every row
- Balance batch size (too large = memory issues)

---

### Mistake 6.2: Querying Inside Transaction Loop

**What happens:**
```python
with Session(engine) as session:
    courses = session.query(Course).all()
    
    for course in courses:
        # Query inside transaction loop!
        topic_count = session.query(Topic).filter_by(
            course_id=course.course_id
        ).count()
        
        course.topic_count = topic_count
    
    session.commit()
    # N+1 queries inside transaction!
```

**Why it's wrong:**
N+1 queries during transaction. Long transaction duration.

**How to fix:**
```python
# Eager load outside transaction if possible
with Session(engine) as session:
    # Single query with join
    courses = session.query(
        Course.course_id,
        Course.course_title,
        func.count(Topic.topic_id).label('topic_count')
    ).outerjoin(Topic).group_by(Course.course_id).all()
    
    # Or use subquery
    topic_counts = session.query(
        Topic.course_id,
        func.count(Topic.topic_id).label('count')
    ).group_by(Topic.course_id).subquery()
    
    courses = session.query(Course, topic_counts.c.count).outerjoin(
        topic_counts, Course.course_id == topic_counts.c.course_id
    ).all()
```

**How to avoid:**
- Avoid queries inside loops
- Use eager loading (joinedload, selectinload)
- Aggregate in database, not application
- Keep transactions focused

---

## Quick Reference: Common Error Patterns

| Symptom | Likely Cause | Solution |
|---------|--------------|----------|
| Data inconsistency | No transaction / partial rollback | Wrap in BEGIN/COMMIT |
| Lost updates | Read-modify-write without lock | Use FOR UPDATE |
| Deadlock errors | Inconsistent lock order | Lock in sorted order |
| Slow queries during high traffic | Wrong isolation level | Use READ COMMITTED by default |
| Connection pool exhausted | Sessions not closed | Use context manager |
| Serialization failures | Unnecessary SERIALIZABLE | Downgrade to REPEATABLE READ |
| Long wait times | Locks held too long | Minimize transaction scope |
| N+1 queries in transaction | Queries in loop | Eager load or aggregate |

---

## Best Practices Summary

1. **Always use transactions** for related operations
2. **Keep transactions short** - minimize lock duration
3. **Choose appropriate isolation level** - READ COMMITTED by default
4. **Always handle deadlocks** - retry with backoff
5. **Lock in consistent order** - prevent deadlocks
6. **Use SELECT FOR UPDATE** for read-modify-write
7. **Always close sessions** - use context manager
8. **Batch operations** - don't commit after every row
9. **Separate validation from updates** - validate before locking
10. **Test concurrency** - simulate multiple users

---

**Remember:** Transactions are powerful but require careful handling. Most bugs come from not understanding isolation levels, forgetting to lock, or holding locks too long. Always test with concurrent users!

**Next steps:**
- Review exercises.md for hands-on practice
- Complete checkpoints.md to verify understanding
- Apply these lessons to CourseDB-AI

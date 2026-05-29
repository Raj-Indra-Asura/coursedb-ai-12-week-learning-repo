# Week 9: Transactions & Concurrency - Exercises

## 🎯 Exercise Overview

These exercises build your transaction and concurrency skills through hands-on practice:

1. **ACID Properties** - Test atomicity, consistency, isolation, durability
2. **Concurrency Problems** - Simulate lost updates, dirty reads, phantoms
3. **Isolation Levels** - Compare behavior at different levels
4. **Locking** - Practice shared and exclusive locks
5. **Deadlocks** - Create, detect, and resolve deadlocks
6. **SQLAlchemy Transactions** - Implement in Python/FastAPI

**Setup Required:**
- PostgreSQL with CourseDB-AI schema
- Two terminal windows (for concurrency tests)
- Python with SQLAlchemy

---

## Exercise Set 1: ACID Properties

### Exercise 1.1: Test Atomicity

**Goal:** Verify all-or-nothing behavior.

```sql
-- Test 1: Successful transaction
BEGIN;
    INSERT INTO courses (course_id, course_code, course_title, credit)
    VALUES (100, 'TEST100', 'Test Course', 3);
    
    INSERT INTO topics (topic_id, course_id, topic_name, week_number)
    VALUES (100, 100, 'Test Topic', 1);
COMMIT;

-- Check: Both inserted?
SELECT * FROM courses WHERE course_id = 100;
SELECT * FROM topics WHERE topic_id = 100;

-- Clean up
DELETE FROM topics WHERE topic_id = 100;
DELETE FROM courses WHERE course_id = 100;
```

```sql
-- Test 2: Failed transaction (atomicity)
BEGIN;
    INSERT INTO courses (course_id, course_code, course_title, credit)
    VALUES (101, 'TEST101', 'Test Course 2', 3);
    
    -- This will fail (FK violation: course_id 999 doesn't exist)
    INSERT INTO topics (topic_id, course_id, topic_name, week_number)
    VALUES (101, 999, 'Test Topic', 1);
COMMIT;

-- Check: Was course inserted? (Should be NO due to atomicity)
SELECT * FROM courses WHERE course_id = 101;
-- Result: No rows (entire transaction rolled back)
```

**Questions:**
1. What happened to the course insert when topic insert failed?
2. Why is this behavior important?
3. What would happen without transactions?

---

### Exercise 1.2: Test Consistency

**Goal:** Verify constraints are enforced.

```sql
-- Test foreign key constraint
BEGIN;
    INSERT INTO questions (
        question_id,
        course_id,  -- FK to courses
        question_text,
        marks
    ) VALUES (1000, 999, 'Test question', 10);
    -- course_id 999 doesn't exist
COMMIT;
-- ERROR: Foreign key violation

-- Test check constraint
BEGIN;
    INSERT INTO questions (
        question_id,
        course_id,
        question_text,
        marks
    ) VALUES (1001, 1, 'Test question', -5);  -- Negative marks!
COMMIT;
-- ERROR: Check constraint violation (if defined)
```

**Questions:**
1. When are constraints checked - during or after transaction?
2. Can you commit a transaction that violates constraints?
3. How do constraints help maintain consistency?

---

### Exercise 1.3: Test Isolation

**Goal:** Verify transactions don't see each other's uncommitted changes.

**Terminal 1:**
```sql
BEGIN;
    UPDATE courses SET course_title = 'MODIFIED' WHERE course_id = 1;
    -- Don't commit yet, leave transaction open
    -- Go to Terminal 2
```

**Terminal 2:**
```sql
-- Try to read the modified row
SELECT course_title FROM courses WHERE course_id = 1;
-- Should still see original title, not 'MODIFIED'
```

**Terminal 1:**
```sql
    COMMIT;  -- Now commit
```

**Terminal 2:**
```sql
-- Read again
SELECT course_title FROM courses WHERE course_id = 1;
-- Now you see 'MODIFIED'
```

**Questions:**
1. Why didn't Terminal 2 see the update before commit?
2. What isolation level is this demonstrating?
3. What would happen with Read Uncommitted?

---

### Exercise 1.4: Test Durability

**Goal:** Verify committed changes persist.

```sql
-- Insert data and commit
BEGIN;
    INSERT INTO courses (course_id, course_code, course_title, credit)
    VALUES (200, 'DURABLE', 'Durability Test', 3);
COMMIT;

-- Simulate crash: Close connection and reconnect
-- (In psql: \q then reconnect)

-- After reconnect, check data
SELECT * FROM courses WHERE course_id = 200;
-- Should still be there!

-- Clean up
DELETE FROM courses WHERE course_id = 200;
```

**Questions:**
1. How does PostgreSQL ensure durability?
2. What is Write-Ahead Logging (WAL)?
3. Would data survive if you crashed before COMMIT?

---

## Exercise Set 2: Concurrency Problems

### Exercise 2.1: Lost Update

**Goal:** Demonstrate and fix lost update problem.

**Problem Demonstration:**

**Terminal 1:**
```sql
BEGIN;
    -- Read balance
    SELECT enrolled_count FROM courses WHERE course_id = 1;
    -- Let's say it returns 100
    
    -- Wait here... (go to Terminal 2)
```

**Terminal 2:**
```sql
BEGIN;
    -- Read same balance
    SELECT enrolled_count FROM courses WHERE course_id = 1;
    -- Also sees 100
    
    -- Increment by 5
    UPDATE courses SET enrolled_count = 100 + 5 WHERE course_id = 1;
COMMIT;
```

**Terminal 1:**
```sql
    -- Increment by 10 (based on old value 100)
    UPDATE courses SET enrolled_count = 100 + 10 WHERE course_id = 1;
COMMIT;

-- Check final value
SELECT enrolled_count FROM courses WHERE course_id = 1;
-- Result: 110 (lost the +5 update!)
-- Should be 115
```

**Solution: Use SELECT FOR UPDATE:**

**Terminal 1:**
```sql
BEGIN;
    -- Lock the row
    SELECT enrolled_count FROM courses WHERE course_id = 1 FOR UPDATE;
    -- Returns 110 (from previous test)
```

**Terminal 2:**
```sql
BEGIN;
    -- Try to lock same row
    SELECT enrolled_count FROM courses WHERE course_id = 1 FOR UPDATE;
    -- Waits for Terminal 1 to finish
```

**Terminal 1:**
```sql
    UPDATE courses SET enrolled_count = enrolled_count + 10 WHERE course_id = 1;
COMMIT;
```

**Terminal 2:**
```sql
    -- Now Terminal 2 proceeds with updated value
    UPDATE courses SET enrolled_count = enrolled_count + 5 WHERE course_id = 1;
COMMIT;

-- Check final value
SELECT enrolled_count FROM courses WHERE course_id = 1;
-- Result: 125 (correct! Both updates applied)
```

**Questions:**
1. Why did the lost update occur?
2. How does SELECT FOR UPDATE prevent it?
3. When should you use SELECT FOR UPDATE?

---

### Exercise 2.2: Dirty Read

**Goal:** Demonstrate dirty read (if possible in your isolation level).

**Terminal 1:**
```sql
BEGIN TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
    UPDATE courses SET course_title = 'DIRTY' WHERE course_id = 1;
    -- Don't commit yet
```

**Terminal 2:**
```sql
BEGIN TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
    -- Try to read uncommitted change
    SELECT course_title FROM courses WHERE course_id = 1;
    -- In PostgreSQL, you still won't see 'DIRTY' (PostgreSQL treats Read Uncommitted as Read Committed)
COMMIT;
```

**Terminal 1:**
```sql
    ROLLBACK;  -- Abort transaction
```

**Note:** PostgreSQL doesn't allow true dirty reads. Try with MySQL if available.

**Questions:**
1. Why are dirty reads dangerous?
2. What isolation level prevents dirty reads?
3. Is there ever a valid use case for dirty reads?

---

### Exercise 2.3: Unrepeatable Read

**Goal:** Demonstrate unrepeatable read problem.

**Terminal 1:**
```sql
BEGIN TRANSACTION ISOLATION LEVEL READ COMMITTED;
    -- First read
    SELECT course_title FROM courses WHERE course_id = 1;
    -- Returns: 'Database Systems'
    
    -- Wait here... (go to Terminal 2)
```

**Terminal 2:**
```sql
BEGIN;
    UPDATE courses SET course_title = 'Advanced DBMS' WHERE course_id = 1;
COMMIT;
```

**Terminal 1:**
```sql
    -- Second read (same transaction)
    SELECT course_title FROM courses WHERE course_id = 1;
    -- Returns: 'Advanced DBMS' (different value!)
COMMIT;
```

**Solution: Use REPEATABLE READ:**

**Terminal 1:**
```sql
BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;
    -- First read
    SELECT course_title FROM courses WHERE course_id = 1;
    -- Returns: 'Advanced DBMS'
```

**Terminal 2:**
```sql
BEGIN;
    UPDATE courses SET course_title = 'Database Systems' WHERE course_id = 1;
COMMIT;
```

**Terminal 1:**
```sql
    -- Second read (same transaction)
    SELECT course_title FROM courses WHERE course_id = 1;
    -- Still returns: 'Advanced DBMS' (consistent!)
COMMIT;
```

**Questions:**
1. When is unrepeatable read a problem?
2. What isolation level prevents it?
3. What's the performance cost of Repeatable Read?

---

### Exercise 2.4: Phantom Read

**Goal:** Demonstrate phantom reads.

**Terminal 1:**
```sql
BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;
    -- Count questions for 2023
    SELECT COUNT(*) FROM questions WHERE year = 2023;
    -- Returns: 50
    
    -- Wait here... (go to Terminal 2)
```

**Terminal 2:**
```sql
BEGIN;
    -- Insert new question for 2023
    INSERT INTO questions (course_id, topic_id, question_text, year, marks)
    VALUES (1, 1, 'New question', 2023, 10);
COMMIT;
```

**Terminal 1:**
```sql
    -- Count again (same transaction)
    SELECT COUNT(*) FROM questions WHERE year = 2023;
    -- In PostgreSQL Repeatable Read: Still returns 50 (no phantom!)
    -- In other databases with true Repeatable Read: Returns 51 (phantom!)
COMMIT;
```

**Note:** PostgreSQL's Repeatable Read actually prevents phantoms. Use Serializable for guaranteed prevention.

**Questions:**
1. What's the difference between phantom and unrepeatable read?
2. When are phantoms a problem?
3. What's the cost of Serializable isolation?

---

## Exercise Set 3: Isolation Levels

### Exercise 3.1: Compare All Isolation Levels

**Goal:** See behavior differences across isolation levels.

Create test table:
```sql
CREATE TABLE test_isolation (
    id INT PRIMARY KEY,
    value TEXT
);

INSERT INTO test_isolation VALUES (1, 'initial');
```

**Test 1: Read Committed**

**Terminal 1:**
```sql
BEGIN TRANSACTION ISOLATION LEVEL READ COMMITTED;
    SELECT value FROM test_isolation WHERE id = 1;
    -- Returns: 'initial'
```

**Terminal 2:**
```sql
UPDATE test_isolation SET value = 'updated' WHERE id = 1;
```

**Terminal 1:**
```sql
    SELECT value FROM test_isolation WHERE id = 1;
    -- Returns: 'updated' (sees committed change)
COMMIT;
```

**Test 2: Repeatable Read**

**Terminal 1:**
```sql
BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;
    SELECT value FROM test_isolation WHERE id = 1;
    -- Returns: 'updated'
```

**Terminal 2:**
```sql
UPDATE test_isolation SET value = 'changed' WHERE id = 1;
```

**Terminal 1:**
```sql
    SELECT value FROM test_isolation WHERE id = 1;
    -- Returns: 'updated' (doesn't see change)
COMMIT;
```

**Test 3: Serializable**

**Terminal 1:**
```sql
BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;
    SELECT SUM(marks) FROM questions WHERE year = 2023;
    -- Returns: 500
```

**Terminal 2:**
```sql
BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;
    SELECT SUM(marks) FROM questions WHERE year = 2023;
    -- Returns: 500
    
    INSERT INTO questions (course_id, topic_id, question_text, year, marks)
    VALUES (1, 1, 'Extra', 2023, 50);
COMMIT;
```

**Terminal 1:**
```sql
    INSERT INTO questions (course_id, topic_id, question_text, year, marks)
    VALUES (1, 1, 'Another', 2023, 50);
COMMIT;
-- ERROR: Serialization failure!
-- Must retry transaction
```

**Questions:**
1. Which isolation level is fastest? Slowest?
2. When would you use each level?
3. What's serialization failure?

---

## Exercise Set 4: Locking

### Exercise 4.1: Shared vs Exclusive Locks

**Goal:** Understand lock compatibility.

**Test 1: Shared lock compatibility**

**Terminal 1:**
```sql
BEGIN;
    SELECT * FROM courses WHERE course_id = 1 FOR SHARE;
    -- Acquires shared lock
```

**Terminal 2:**
```sql
BEGIN;
    SELECT * FROM courses WHERE course_id = 1 FOR SHARE;
    -- Also gets shared lock (compatible!)
    -- Doesn't wait
COMMIT;
```

**Terminal 1:**
```sql
COMMIT;
```

**Test 2: Exclusive lock conflict**

**Terminal 1:**
```sql
BEGIN;
    SELECT * FROM courses WHERE course_id = 1 FOR UPDATE;
    -- Acquires exclusive lock
```

**Terminal 2:**
```sql
BEGIN;
    SELECT * FROM courses WHERE course_id = 1 FOR SHARE;
    -- Waits (conflict with exclusive lock)
```

**Terminal 1:**
```sql
COMMIT;  -- Release lock
```

**Terminal 2:**
```sql
    -- Now proceeds
COMMIT;
```

**Questions:**
1. When do you need FOR SHARE vs FOR UPDATE?
2. What happens if you SELECT without FOR SHARE/UPDATE?
3. Can two transactions both hold FOR UPDATE on same row?

---

### Exercise 4.2: Lock Timeout

**Goal:** Handle lock wait timeout.

**Terminal 1:**
```sql
BEGIN;
    SELECT * FROM courses WHERE course_id = 1 FOR UPDATE;
    -- Hold lock (don't commit)
```

**Terminal 2:**
```sql
-- Set timeout
SET statement_timeout = '3s';

BEGIN;
    -- Try to acquire lock
    SELECT * FROM courses WHERE course_id = 1 FOR UPDATE;
    -- Waits... then after 3 seconds:
    -- ERROR: canceling statement due to statement timeout
ROLLBACK;
```

**Terminal 1:**
```sql
COMMIT;
```

**Questions:**
1. Why is lock timeout important?
2. What timeout value is appropriate?
3. Should application retry after timeout?

---

## Exercise Set 5: Deadlocks

### Exercise 5.1: Create a Deadlock

**Goal:** Experience and understand deadlocks.

**Terminal 1:**
```sql
BEGIN;
    UPDATE courses SET course_title = 'T1' WHERE course_id = 1;
    -- Acquired lock on course 1
    
    -- Wait 10 seconds... (go to Terminal 2)
```

**Terminal 2:**
```sql
BEGIN;
    UPDATE courses SET course_title = 'T2' WHERE course_id = 2;
    -- Acquired lock on course 2
    
    -- Now try to get course 1
    UPDATE courses SET course_title = 'T2' WHERE course_id = 1;
    -- Waits for Terminal 1...
```

**Terminal 1:**
```sql
    -- Try to get course 2
    UPDATE courses SET course_title = 'T1' WHERE course_id = 2;
    -- Deadlock detected!
    -- ERROR: deadlock detected
ROLLBACK;
```

**Terminal 2:**
```sql
    -- Terminal 2 proceeds after Terminal 1 rolled back
COMMIT;
```

**Questions:**
1. Why did deadlock occur?
2. Which transaction was aborted?
3. How could this be prevented?

---

### Exercise 5.2: Prevent Deadlock with Lock Ordering

**Goal:** Prevent deadlock by locking in order.

**Solution:**

**Terminal 1:**
```sql
BEGIN;
    -- Lock in order: course 1, then course 2
    UPDATE courses SET course_title = 'T1' WHERE course_id = 1;
    
    -- Wait here...
```

**Terminal 2:**
```sql
BEGIN;
    -- Same order: course 1, then course 2
    UPDATE courses SET course_title = 'T2' WHERE course_id = 1;
    -- Waits for Terminal 1 (no deadlock!)
```

**Terminal 1:**
```sql
    UPDATE courses SET course_title = 'T1' WHERE course_id = 2;
COMMIT;
```

**Terminal 2:**
```sql
    -- Now proceeds
    UPDATE courses SET course_title = 'T2' WHERE course_id = 2;
COMMIT;
-- No deadlock!
```

**Questions:**
1. How does lock ordering prevent deadlock?
2. What if you can't predict lock order?
3. Are there other prevention strategies?

---

### Exercise 5.3: Deadlock Detection Query

**Goal:** Monitor for deadlocks.

```sql
-- Enable logging of deadlocks
ALTER SYSTEM SET log_lock_waits = on;
ALTER SYSTEM SET deadlock_timeout = '1s';
SELECT pg_reload_conf();

-- Create deadlock (from Exercise 5.1)

-- Check PostgreSQL log
-- Shows deadlock details with wait-for graph

-- Query to see lock waits
SELECT
    blocked_locks.pid AS blocked_pid,
    blocked_activity.usename AS blocked_user,
    blocking_locks.pid AS blocking_pid,
    blocking_activity.usename AS blocking_user,
    blocked_activity.query AS blocked_query,
    blocking_activity.query AS blocking_query
FROM pg_catalog.pg_locks blocked_locks
JOIN pg_catalog.pg_stat_activity blocked_activity ON blocked_activity.pid = blocked_locks.pid
JOIN pg_catalog.pg_locks blocking_locks 
    ON blocking_locks.locktype = blocked_locks.locktype
    AND blocking_locks.database IS NOT DISTINCT FROM blocked_locks.database
    AND blocking_locks.relation IS NOT DISTINCT FROM blocked_locks.relation
    AND blocking_locks.page IS NOT DISTINCT FROM blocked_locks.page
    AND blocking_locks.tuple IS NOT DISTINCT FROM blocked_locks.tuple
    AND blocking_locks.virtualxid IS NOT DISTINCT FROM blocked_locks.virtualxid
    AND blocking_locks.transactionid IS NOT DISTINCT FROM blocked_locks.transactionid
    AND blocking_locks.classid IS NOT DISTINCT FROM blocked_locks.classid
    AND blocking_locks.objid IS NOT DISTINCT FROM blocked_locks.objid
    AND blocking_locks.objsubid IS NOT DISTINCT FROM blocked_locks.objsubid
    AND blocking_locks.pid != blocked_locks.pid
JOIN pg_catalog.pg_stat_activity blocking_activity ON blocking_activity.pid = blocking_locks.pid
WHERE NOT blocked_locks.granted;
```

---

## Exercise Set 6: SQLAlchemy Transactions

### Exercise 6.1: Basic Transaction

**Goal:** Implement transaction in Python.

```python
from sqlalchemy.orm import Session
from app.db.database import get_session
from app.db.models import Course, Topic

def create_course_with_topics(
    course_code: str,
    course_title: str,
    credit: int,
    topics: list[str]
):
    """Create course and topics in a transaction."""
    with Session(engine) as session:
        try:
            # Create course
            new_course = Course(
                course_code=course_code,
                course_title=course_title,
                credit=credit
            )
            session.add(new_course)
            session.flush()  # Get course_id
            
            # Create topics
            for i, topic_name in enumerate(topics, start=1):
                new_topic = Topic(
                    course_id=new_course.course_id,
                    topic_name=topic_name,
                    week_number=i
                )
                session.add(new_topic)
            
            session.commit()
            return new_course.course_id
            
        except Exception as e:
            session.rollback()
            raise

# Test
course_id = create_course_with_topics(
    'CS401',
    'Transaction Processing',
    3,
    ['ACID', 'Concurrency', 'Recovery']
)
print(f"Created course {course_id}")
```

**Questions:**
1. What happens if topic creation fails?
2. Why use session.flush()?
3. Is try/except necessary with context manager?

---

### Exercise 6.2: Nested Transaction (Savepoint)

**Goal:** Implement partial rollback.

```python
def create_course_with_optional_topics(
    course_code: str,
    course_title: str,
    credit: int,
    topics: list[str]
):
    """Create course, skip invalid topics."""
    with Session(engine) as session:
        # Outer transaction
        new_course = Course(
            course_code=course_code,
            course_title=course_title,
            credit=credit
        )
        session.add(new_course)
        session.flush()
        
        created_topics = []
        for topic_name in topics:
            # Nested transaction (savepoint)
            session.begin_nested()
            try:
                new_topic = Topic(
                    course_id=new_course.course_id,
                    topic_name=topic_name,
                    week_number=len(created_topics) + 1
                )
                session.add(new_topic)
                session.commit()  # Commit nested
                created_topics.append(topic_name)
            except Exception as e:
                session.rollback()  # Rollback only nested
                print(f"Skipped topic {topic_name}: {e}")
        
        session.commit()  # Commit outer
        return new_course.course_id, created_topics

# Test with some invalid topics
course_id, topics = create_course_with_optional_topics(
    'CS402',
    'Advanced Topics',
    3,
    ['Valid Topic', None, 'Another Topic']  # None will fail
)
print(f"Created course {course_id} with topics: {topics}")
```

**Questions:**
1. When is nested transaction useful?
2. What's the difference between nested and outer commit?
3. Can you nest multiple levels?

---

### Exercise 6.3: Retry on Deadlock

**Goal:** Handle deadlock with retry logic.

```python
import time
from sqlalchemy.exc import DBAPIError

def transfer_enrollment(
    from_course_id: int,
    to_course_id: int,
    max_retries: int = 3
):
    """Transfer enrollment between courses with deadlock retry."""
    for attempt in range(max_retries):
        try:
            with Session(engine) as session:
                # Lock courses in consistent order (by ID)
                course_ids = sorted([from_course_id, to_course_id])
                
                course1 = session.query(Course).filter_by(
                    course_id=course_ids[0]
                ).with_for_update().one()
                
                course2 = session.query(Course).filter_by(
                    course_id=course_ids[1]
                ).with_for_update().one()
                
                # Identify which is from/to
                if course1.course_id == from_course_id:
                    from_course, to_course = course1, course2
                else:
                    from_course, to_course = course2, course1
                
                # Transfer
                from_course.enrolled_count -= 1
                to_course.enrolled_count += 1
                
                session.commit()
                return True
                
        except DBAPIError as e:
            if 'deadlock' in str(e).lower():
                if attempt < max_retries - 1:
                    # Exponential backoff
                    wait_time = 0.1 * (2 ** attempt)
                    print(f"Deadlock detected, retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    print("Max retries exceeded")
                    raise
            else:
                raise
    
    return False

# Test
success = transfer_enrollment(from_course_id=1, to_course_id=2)
print(f"Transfer {'succeeded' if success else 'failed'}")
```

**Questions:**
1. Why use exponential backoff?
2. Is lock ordering sufficient to prevent all deadlocks?
3. What's appropriate max_retries value?

---

## Challenge Exercises

### Challenge 1: Implement Optimistic Locking

Add version-based optimistic locking to Course model.

```python
# 1. Add version column to Course model
# 2. Implement update function that checks version
# 3. Raise ConcurrentModificationError if version changed
# 4. Test with two concurrent updates
```

### Challenge 2: Build Wait-For Graph

Create a function that builds and visualizes wait-for graph from pg_locks.

```python
# 1. Query pg_locks and pg_stat_activity
# 2. Build graph of which transactions wait for which
# 3. Detect cycles (deadlocks)
# 4. Visualize with networkx or similar
```

---

## Summary

After completing these exercises, you should be able to:

✅ Verify ACID properties with tests  
✅ Identify and fix concurrency problems  
✅ Choose appropriate isolation levels  
✅ Use locking correctly  
✅ Create, detect, and prevent deadlocks  
✅ Implement transactions in SQLAlchemy  
✅ Handle deadlocks with retry logic  

**Next Steps:**
- Follow implementation_plan.md for structured learning
- Review mistakes_to_expect.md to avoid common errors
- Apply transactions to CourseDB-AI endpoints
- Complete reflection.md to solidify understanding

# Week 9: Transactions & Concurrency Control

## 🧭 Navigation

**[← Previous: Week 8](../week_08_query_optimization/reflection.md)** | **[View Learning Path](../../LEARNING_PATH.md)** | **[Next: Theory Notes →](theory_notes.md)**

---

## 📋 Overview

Week 9 focuses on **transactions** and **concurrency control** - critical concepts for building reliable multi-user database applications. You'll learn how databases ensure data consistency when multiple users access data simultaneously, and how to handle the inevitable conflicts that arise.

**What you'll master:**
- ACID properties and why they matter
- Transaction lifecycle and commands
- Concurrency problems (lost updates, dirty reads, phantoms)
- Isolation levels and their trade-offs
- Locking mechanisms (shared, exclusive, two-phase)
- Deadlock detection and prevention
- Practical transaction patterns in SQLAlchemy
- Real-world concurrency scenarios in CourseDB-AI

**Why this matters:**
- Multi-user applications need transactions
- Race conditions can corrupt data silently
- Understanding isolation prevents bugs
- Deadlocks can bring systems down
- Wrong isolation level = performance or correctness issues

---

## 1. What is a Transaction?

A **transaction** is a sequence of one or more database operations executed as a single logical unit of work.

### Core Idea

Either **all operations succeed** (commit) or **all fail** (rollback). No partial execution.

### Example: Bank Transfer

```sql
-- WITHOUT transaction (dangerous!)
UPDATE accounts SET balance = balance - 100 WHERE account_id = 1;
-- Power fails here!
UPDATE accounts SET balance = balance + 100 WHERE account_id = 2;
-- Second update never happens - money lost!

-- WITH transaction (safe!)
BEGIN TRANSACTION;
    UPDATE accounts SET balance = balance - 100 WHERE account_id = 1;
    UPDATE accounts SET balance = balance + 100 WHERE account_id = 2;
COMMIT;
-- Both happen or neither happens
```

### CourseDB-AI Example

```sql
-- Create course with topics atomically
BEGIN;
    INSERT INTO courses (course_code, course_title, credit)
    VALUES ('CS301', 'Advanced DBMS', 3)
    RETURNING course_id;  -- Returns: 101

    INSERT INTO topics (course_id, topic_name, week_number)
    VALUES (101, 'Query Optimization', 1);

    INSERT INTO topics (course_id, topic_name, week_number)
    VALUES (101, 'Transactions', 2);
COMMIT;

-- All succeed together or all fail together
```

---

## 2. ACID Properties

ACID = **Atomicity, Consistency, Isolation, Durability**

### A - Atomicity

**All or nothing.** Transaction either completes fully or not at all.

```sql
BEGIN;
    INSERT INTO courses VALUES (1, 'CS201', 'DBMS', 4);
    INSERT INTO topics VALUES (1, 1, 'Normalization', 4);
    -- If INSERT into topics fails (e.g., FK violation)
    -- Then INSERT into courses is also rolled back
COMMIT;
```

**Implementation:** Write-ahead logging (WAL). Database logs operations before executing them, so it can undo if needed.

### C - Consistency

**Valid states only.** Database moves from one consistent state to another. All constraints (PK, FK, CHECK) must be satisfied.

```sql
-- Constraint enforced
CREATE TABLE questions (
    course_id INT REFERENCES courses(course_id),  -- FK constraint
    marks INT CHECK (marks > 0)  -- Check constraint
);

-- Consistency violation prevented
INSERT INTO questions (course_id, marks) VALUES (999, -5);
-- ERROR: Foreign key violation (course 999 doesn't exist)
-- ERROR: Check constraint violation (marks must be > 0)
```

**Implementation:** Database validates constraints before commit.

### I - Isolation

**Transactions don't interfere.** Concurrent transactions appear to execute sequentially.

```sql
-- Transaction 1
BEGIN;
SELECT balance FROM accounts WHERE id = 1;  -- Sees 1000
-- Transaction 2 updates balance to 500 here
SELECT balance FROM accounts WHERE id = 1;  -- Still sees 1000 (isolation!)
COMMIT;
```

**Implementation:** Locking, MVCC (Multi-Version Concurrency Control).

### D - Durability

**Committed = permanent.** Once committed, changes survive crashes, power failures, etc.

```sql
BEGIN;
    UPDATE accounts SET balance = 900 WHERE id = 1;
COMMIT;  -- Changes written to disk
-- Even if power fails now, balance is still 900 after restart
```

**Implementation:** Write-ahead log (WAL) on disk.

---

## 3. Transaction Lifecycle

```
START → ACTIVE → PARTIALLY COMMITTED → COMMITTED
          ↓
        FAILED → ABORTED
```

**States:**
- **Active**: Transaction is executing operations
- **Partially Committed**: Last operation executed, waiting to commit
- **Committed**: All changes written to disk, transaction complete
- **Failed**: Error occurred during execution
- **Aborted**: Transaction rolled back, all changes undone

**Commands:**

```sql
-- Start transaction
BEGIN;  -- or START TRANSACTION;

-- Do work
INSERT INTO courses VALUES (...);
UPDATE topics SET ...;

-- Success: Make permanent
COMMIT;

-- OR Failure: Undo everything
ROLLBACK;
```

---

## 4. Concurrency Problems

When multiple transactions run simultaneously, issues arise:

### Problem 1: Lost Update

Two transactions update the same data; one update is lost.

```sql
-- Time  Transaction 1             Transaction 2
-- T1    READ balance = 1000
-- T2                              READ balance = 1000
-- T3    balance = 1000 - 100
-- T4                              balance = 1000 + 200
-- T5    WRITE balance = 900
-- T6                              WRITE balance = 1200
-- Result: Lost the -100 update! Should be 1100, not 1200
```

**Solution:** Use locking or higher isolation level.

### Problem 2: Dirty Read

Reading uncommitted (potentially invalid) data from another transaction.

```sql
-- Time  Transaction 1             Transaction 2
-- T1    UPDATE balance = 900
-- T2                              READ balance = 900  ← Dirty read!
-- T3    ROLLBACK  ← T1 aborts
-- T4                              Uses 900 (wrong! Should be 1000)
```

**Solution:** Use Read Committed or higher isolation level.

### Problem 3: Unrepeatable Read

Reading the same data twice in a transaction gives different results.

```sql
-- Time  Transaction 1             Transaction 2
-- T1    READ balance = 1000
-- T2                              UPDATE balance = 900
-- T3                              COMMIT
-- T4    READ balance = 900  ← Different value!
-- Same transaction, different values for same row
```

**Solution:** Use Repeatable Read or Serializable isolation.

### Problem 4: Phantom Read

A query returns different rows when repeated in the same transaction.

```sql
-- Time  Transaction 1                    Transaction 2
-- T1    SELECT COUNT(*) FROM questions
--       WHERE year = 2023;  -- Returns 10
-- T2                                     INSERT new question (year=2023)
-- T3                                     COMMIT
-- T4    SELECT COUNT(*) FROM questions
--       WHERE year = 2023;  -- Returns 11  ← Phantom row!
```

**Solution:** Use Serializable isolation level.

---

## 5. Isolation Levels

PostgreSQL provides 4 isolation levels to control transaction visibility:

| Isolation Level | Dirty Read | Unrepeatable Read | Phantom Read | Performance |
|----------------|------------|-------------------|--------------|-------------|
| **Read Uncommitted** | ❌ Possible | ❌ Possible | ❌ Possible | Fastest |
| **Read Committed** | ✅ Prevented | ❌ Possible | ❌ Possible | Fast |
| **Repeatable Read** | ✅ Prevented | ✅ Prevented | ❌ Possible | Slower |
| **Serializable** | ✅ Prevented | ✅ Prevented | ✅ Prevented | Slowest |

**Default in PostgreSQL: Read Committed**

### Setting Isolation Level

```sql
-- For single transaction
BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;
    SELECT * FROM accounts WHERE id = 1;
    UPDATE accounts SET balance = balance - 100 WHERE id = 1;
COMMIT;

-- For session
SET SESSION CHARACTERISTICS AS TRANSACTION ISOLATION LEVEL REPEATABLE READ;
```

### Choosing the Right Level

**Use Read Committed when:**
- Default for most applications
- Acceptable if reads can change between queries
- Example: Viewing list of courses (it's OK if new courses appear)

**Use Repeatable Read when:**
- Need consistent snapshot of data
- Generating reports or analytics
- Example: Monthly revenue report (data shouldn't change mid-report)

**Use Serializable when:**
- Need maximum consistency
- Complex multi-step transactions
- Example: Inventory management (prevent overselling)

---

## 6. Locking Mechanisms

Locks control concurrent access to data.

### Lock Types

**Shared Lock (S-Lock)** - "Read lock"
- Multiple transactions can read
- No transaction can write
- Compatible with other shared locks

**Exclusive Lock (X-Lock)** - "Write lock"
- Only one transaction can write
- No other transaction can read or write
- Not compatible with any other lock

### Lock Compatibility Table

|   | S-Lock | X-Lock |
|---|--------|--------|
| **S-Lock** | ✅ Compatible | ❌ Conflict |
| **X-Lock** | ❌ Conflict | ❌ Conflict |

### Explicit Locking in PostgreSQL

```sql
-- Shared lock (reading)
BEGIN;
SELECT * FROM courses WHERE course_id = 1 FOR SHARE;
-- Other transactions can also SELECT FOR SHARE
-- But cannot UPDATE/DELETE
COMMIT;

-- Exclusive lock (writing)
BEGIN;
SELECT * FROM courses WHERE course_id = 1 FOR UPDATE;
-- No other transaction can read or write
UPDATE courses SET course_title = 'New Title' WHERE course_id = 1;
COMMIT;
```

### CourseDB-AI Example

```sql
-- Prevent race condition when enrolling students
BEGIN;
    -- Lock course to check capacity
    SELECT enrolled_count, max_capacity
    FROM courses
    WHERE course_id = 1
    FOR UPDATE;  -- Exclusive lock

    -- Safe to enroll (other transactions wait)
    UPDATE courses
    SET enrolled_count = enrolled_count + 1
    WHERE course_id = 1 AND enrolled_count < max_capacity;

COMMIT;
```

---

## 7. Two-Phase Locking (2PL)

Protocol to ensure **serializability** (transactions behave as if executed sequentially).

### Two Phases

**Phase 1: Growing Phase**
- Acquire locks as needed
- Cannot release any lock

**Phase 2: Shrinking Phase**
- Release locks as finished
- Cannot acquire any lock

### Example

```sql
BEGIN;
    -- Growing Phase: Acquire locks
    LOCK accounts WHERE id = 1;  -- Acquire lock 1
    LOCK accounts WHERE id = 2;  -- Acquire lock 2

    -- Perform operations
    UPDATE accounts SET balance = balance - 100 WHERE id = 1;
    UPDATE accounts SET balance = balance + 100 WHERE id = 2;

    -- Shrinking Phase: Release locks
COMMIT;  -- All locks released
```

**Rule:** Once you release any lock, you cannot acquire new locks.

**Why it works:** Prevents interleaving that causes inconsistencies.

---

## 8. Deadlock

**Deadlock:** Two or more transactions wait for each other indefinitely.

### Classic Deadlock Example

```sql
-- Time  Transaction 1             Transaction 2
-- T1    LOCK account 1            
-- T2                              LOCK account 2
-- T3    Wait for account 2 →
-- T4                          ←   Wait for account 1
-- Deadlock! Both wait forever
```

### Detection: Wait-For Graph

```
Transaction 1 → Transaction 2  (T1 waits for T2)
Transaction 2 → Transaction 1  (T2 waits for T1)

Cycle detected! Deadlock exists.
```

### Prevention Strategies

**1. Lock Ordering**
```sql
-- Always lock in same order (e.g., by ID)
BEGIN;
    LOCK accounts WHERE id IN (1, 2) ORDER BY id;  -- Always lock lower ID first
    -- Operations
COMMIT;
```

**2. Timeout**
```sql
-- PostgreSQL: Set statement timeout
SET statement_timeout = '5s';
BEGIN;
    -- If lock wait exceeds 5s, transaction aborts
COMMIT;
```

**3. Lock All at Once**
```sql
BEGIN;
    LOCK accounts WHERE id IN (1, 2);  -- Lock all needed resources upfront
    -- Operations
COMMIT;
```

### Resolution

When deadlock detected, PostgreSQL:
1. **Aborts one transaction** (victim selection)
2. **Rolls back the victim**
3. **Lets other transaction proceed**
4. **Returns error** to aborted transaction

Application should retry:

```python
max_retries = 3
for attempt in range(max_retries):
    try:
        db.begin()
        # Transaction operations
        db.commit()
        break  # Success
    except DeadlockDetected:
        db.rollback()
        if attempt == max_retries - 1:
            raise  # Give up after retries
        time.sleep(0.1 * (2 ** attempt))  # Exponential backoff
```

---

## 9. Transaction Commands

### BEGIN / START TRANSACTION

```sql
BEGIN;  -- Start transaction
-- OR
START TRANSACTION;
```

### COMMIT

```sql
COMMIT;  -- Make all changes permanent
```

### ROLLBACK

```sql
ROLLBACK;  -- Undo all changes since BEGIN
```

### SAVEPOINT

Partial rollback within transaction:

```sql
BEGIN;
    INSERT INTO courses VALUES (1, 'CS201', 'DBMS', 4);
    SAVEPOINT sp1;

    INSERT INTO topics VALUES (1, 1, 'SQL', 1);
    -- Error occurs

    ROLLBACK TO sp1;  -- Undo only after savepoint
    -- courses insert still valid

    INSERT INTO topics VALUES (1, 1, 'Normalization', 1);  -- Try again
COMMIT;
```

---

## 10. Transactions in SQLAlchemy (Python)

### Basic Transaction

```python
from sqlalchemy.orm import Session

# Automatic transaction management
with Session(engine) as session:
    try:
        # Operations
        new_course = Course(course_code='CS301', course_title='DBMS', credit=3)
        session.add(new_course)
        
        new_topic = Topic(course_id=new_course.id, topic_name='Transactions')
        session.add(new_topic)
        
        session.commit()  # Commit if all succeed
    except Exception:
        session.rollback()  # Rollback on error
        raise
```

### Explicit Transaction Control

```python
# Manual transaction
session.begin()
try:
    session.add(new_course)
    session.add(new_topic)
    session.commit()
except:
    session.rollback()
    raise
```

### Nested Transactions (Savepoints)

```python
session.begin()
try:
    session.add(course)
    
    session.begin_nested()  # Savepoint
    try:
        session.add(topic)
        session.commit()  # Commit nested
    except:
        session.rollback()  # Rollback only nested
    
    session.commit()  # Commit outer
except:
    session.rollback()
    raise
```

### Isolation Level in SQLAlchemy

```python
from sqlalchemy import create_engine

# Set for all connections
engine = create_engine(
    DATABASE_URL,
    isolation_level="REPEATABLE READ"
)

# Or per-transaction
with session.begin():
    session.connection(execution_options={"isolation_level": "SERIALIZABLE"})
    # Operations
```

---

## 11. Real-World Patterns

### Pattern 1: Optimistic Locking with Version Column

```python
# Add version column to model
class Course(Base):
    __tablename__ = 'courses'
    course_id = Column(Integer, primary_key=True)
    course_title = Column(String)
    version = Column(Integer, default=0)  # Version tracking

# Update with version check
def update_course(session, course_id, new_title):
    course = session.query(Course).filter_by(course_id=course_id).one()
    old_version = course.version
    
    course.course_title = new_title
    course.version += 1
    
    # Only update if version unchanged
    result = session.query(Course).filter_by(
        course_id=course_id,
        version=old_version
    ).update({
        'course_title': new_title,
        'version': old_version + 1
    }, synchronize_session=False)
    
    if result == 0:
        raise ConcurrentModificationError("Course was modified by another transaction")
    
    session.commit()
```

### Pattern 2: SELECT FOR UPDATE

```python
# Pessimistic locking
with session.begin():
    # Lock row for update
    course = session.query(Course).filter_by(
        course_id=1
    ).with_for_update().one()
    
    # Safe to modify (other transactions wait)
    course.enrolled_count += 1
    session.commit()
```

### Pattern 3: Idempotent Operations

```python
# Safe to retry without side effects
def enroll_student(session, student_id, course_id):
    # Check if already enrolled
    exists = session.query(Enrollment).filter_by(
        student_id=student_id,
        course_id=course_id
    ).first()
    
    if exists:
        return  # Already enrolled, idempotent
    
    enrollment = Enrollment(student_id=student_id, course_id=course_id)
    session.add(enrollment)
    session.commit()
```

---

## 12. Best Practices

### ✅ DO

1. **Keep transactions short** - Long transactions hold locks longer
2. **Handle errors gracefully** - Always rollback on error
3. **Use appropriate isolation level** - Balance consistency and performance
4. **Lock in consistent order** - Prevent deadlocks
5. **Retry on deadlock** - Deadlocks are normal, retry with backoff
6. **Use database constraints** - Let database enforce consistency
7. **Test concurrent scenarios** - Simulate multiple users

### ❌ DON'T

1. **Don't hold transactions during user input** - Never wait for user in transaction
2. **Don't use Serializable by default** - Too slow for most cases
3. **Don't ignore deadlock errors** - Implement retry logic
4. **Don't update without WHERE clause** - Locks entire table
5. **Don't mix business logic with transactions** - Keep transactions focused
6. **Don't nest transactions unnecessarily** - Use savepoints sparingly
7. **Don't forget to close sessions** - Leaks connections

---

## 13. Debugging Transactions

### View Active Transactions

```sql
-- PostgreSQL: See active transactions
SELECT
    pid,
    usename,
    state,
    query_start,
    state_change,
    query
FROM pg_stat_activity
WHERE state != 'idle'
ORDER BY query_start;
```

### View Locks

```sql
-- See current locks
SELECT
    locktype,
    relation::regclass,
    mode,
    transactionid AS tid,
    virtualtransaction AS vtid,
    pid,
    granted
FROM pg_locks
ORDER BY pid;
```

### Kill Blocking Transaction

```sql
-- Find blocking transaction
SELECT
    blocked_locks.pid AS blocked_pid,
    blocking_locks.pid AS blocking_pid,
    blocked_activity.query AS blocked_query,
    blocking_activity.query AS blocking_query
FROM pg_locks AS blocked_locks
JOIN pg_stat_activity AS blocked_activity ON blocked_activity.pid = blocked_locks.pid
JOIN pg_locks AS blocking_locks ON blocking_locks.locktype = blocked_locks.locktype
JOIN pg_stat_activity AS blocking_activity ON blocking_activity.pid = blocking_locks.pid
WHERE NOT blocked_locks.granted AND blocking_locks.granted;

-- Kill blocking transaction (use with caution!)
SELECT pg_terminate_backend(blocking_pid);
```

---

## 14. Summary

**Key Takeaways:**

1. **Transactions ensure ACID** - Atomicity, Consistency, Isolation, Durability
2. **Isolation levels trade consistency for performance** - Choose based on needs
3. **Locking prevents conflicts** - But can cause deadlocks
4. **Deadlocks are normal** - Detect and retry with backoff
5. **Keep transactions short** - Minimize lock duration
6. **Test concurrency** - Race conditions are subtle

**Next Steps:**
- Complete exercises.md for hands-on practice
- Follow implementation_plan.md for 7-day learning path
- Review mistakes_to_expect.md to avoid common pitfalls
- Apply transactions to CourseDB-AI API endpoints

**Week 10 Preview:** Semantic search with embeddings and pgvector!

---

## Resources

- [PostgreSQL Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html)
- [SQLAlchemy Transactions](https://docs.sqlalchemy.org/en/20/orm/session_transaction.html)
- [ACID Properties Explained](https://en.wikipedia.org/wiki/ACID)
- [Two-Phase Locking](https://en.wikipedia.org/wiki/Two-phase_locking)

---

## 🧭 Navigation

**[← Previous: Week 8](../week_08_query_optimization/reflection.md)** | **[Back to Week 9 Overview](README.md)** | **[Next: Theory Notes →](theory_notes.md)**

---

## 📋 Week 9 File Sequence

1. **[Week 9 README](README.md)** ← You are here
2. **[Theory Notes](theory_notes.md)** - Core concepts
3. **[Exercises](exercises.md)** - Practice
4. **[Implementation Plan](implementation_plan.md)** - Apply concepts
5. **[Checkpoints](checkpoints.md)** - Track progress
6. **[Mistakes to Expect](mistakes_to_expect.md)** - Common pitfalls
7. **[Reflection](reflection.md)** - Weekly reflection
8. **[→ Week 10](../week_10_semantic_search/README.md)** - Continue journey

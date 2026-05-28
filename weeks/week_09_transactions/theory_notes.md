# Week 9: Transactions & Concurrency - Theory Notes

## 📚 Core Concepts

### 1. What is a Transaction?

**Transaction**: A sequence of database operations executed as a single unit.

**Example:**
```sql
BEGIN TRANSACTION;
    UPDATE accounts SET balance = balance - 100 WHERE account_id = 1;
    UPDATE accounts SET balance = balance + 100 WHERE account_id = 2;
COMMIT;
```

**Properties:**
- All operations succeed together (commit)
- OR all fail together (rollback)
- No partial execution

---

### 2. ACID Properties

#### **A - Atomicity**
All or nothing. Transaction either completes fully or not at all.

```sql
BEGIN;
    INSERT INTO courses VALUES (1, 'CS201', 'DBMS', 4);
    INSERT INTO topics VALUES (1, 1, 'Normalization', 4);
COMMIT;  -- Both succeed or both fail
```

#### **C - Consistency**
Database moves from one valid state to another. Constraints always satisfied.

```sql
-- Consistency enforced by constraints
INSERT INTO questions (course_id, ...) VALUES (999, ...);
-- ERROR: Foreign key violation (course 999 doesn't exist)
```

#### **I - Isolation**
Concurrent transactions don't interfere with each other.

```sql
-- Transaction 1
BEGIN;
SELECT balance FROM accounts WHERE id = 1;  -- Sees 1000
-- Transaction 2 updates balance here
SELECT balance FROM accounts WHERE id = 1;  -- Still sees 1000 (isolation)
COMMIT;
```

#### **D - Durability**
Committed changes persist even after system crash.

```sql
COMMIT;  -- Once committed, changes are permanent
-- Even if power fails, changes are saved
```

---

### 3. Transaction States

```
Active → Partially Committed → Committed
  ↓
Failed → Aborted
```

- **Active**: Transaction executing
- **Partially Committed**: Last operation executed
- **Committed**: Changes written to disk
- **Failed**: Error occurred
- **Aborted**: Rolled back

---

### 4. Concurrency Problems

#### **Lost Update**
Two transactions update same data; one update is lost.

```sql
-- Time  Transaction 1             Transaction 2
-- T1    READ balance = 1000
-- T2                              READ balance = 1000
-- T3    balance = 1000 - 100
-- T4                              balance = 1000 + 200
-- T5    WRITE balance = 900
-- T6                              WRITE balance = 1200
-- Result: Lost the -100 update!
```

#### **Dirty Read**
Reading uncommitted data from another transaction.

```sql
-- Time  Transaction 1             Transaction 2
-- T1    UPDATE balance = 900
-- T2                              READ balance = 900 (dirty!)
-- T3    ROLLBACK
-- T4                              Uses 900 (wrong!)
```

#### **Unrepeatable Read**
Reading same data twice gives different results.

```sql
-- Time  Transaction 1             Transaction 2
-- T1    READ balance = 1000
-- T2                              UPDATE balance = 900
-- T3                              COMMIT
-- T4    READ balance = 900
-- Same transaction, different values!
```

#### **Phantom Read**
Query returns different rows when repeated.

```sql
-- Time  Transaction 1                    Transaction 2
-- T1    SELECT COUNT(*) FROM questions
--       WHERE year = 2023;  -- Returns 10
-- T2                                     INSERT new question (year=2023)
-- T3                                     COMMIT
-- T4    SELECT COUNT(*) FROM questions
--       WHERE year = 2023;  -- Returns 11 (phantom!)
```

---

### 5. Isolation Levels

PostgreSQL supports 4 isolation levels:

| Level | Dirty Read | Unrepeatable Read | Phantom Read |
|-------|------------|-------------------|--------------|
| **Read Uncommitted** | ❌ Possible | ❌ Possible | ❌ Possible |
| **Read Committed** | ✅ Prevented | ❌ Possible | ❌ Possible |
| **Repeatable Read** | ✅ Prevented | ✅ Prevented | ❌ Possible |
| **Serializable** | ✅ Prevented | ✅ Prevented | ✅ Prevented |

**Default in PostgreSQL: Read Committed**

```sql
-- Set isolation level
BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;
    -- Your queries here
COMMIT;
```

---

### 6. Locking

**Lock**: Mechanism to control concurrent access to data.

#### **Shared Lock (S-Lock)**
- Multiple transactions can read
- No transaction can write
- "Read lock"

#### **Exclusive Lock (X-Lock)**
- Only one transaction can write
- No other transaction can read or write
- "Write lock"

**Lock Compatibility:**
|   | S-Lock | X-Lock |
|---|--------|--------|
| **S-Lock** | ✅ Compatible | ❌ Conflict |
| **X-Lock** | ❌ Conflict | ❌ Conflict |

---

### 7. Two-Phase Locking (2PL)

**Protocol to ensure serializability.**

**Two Phases:**
1. **Growing Phase**: Acquire locks, cannot release any lock
2. **Shrinking Phase**: Release locks, cannot acquire any lock

```sql
-- Growing Phase
BEGIN;
    LOCK accounts WHERE id = 1;  -- Acquire
    LOCK accounts WHERE id = 2;  -- Acquire

    -- Perform operations
    UPDATE accounts SET balance = balance - 100 WHERE id = 1;
    UPDATE accounts SET balance = balance + 100 WHERE id = 2;

-- Shrinking Phase
COMMIT;  -- Release all locks
```

---

### 8. Deadlock

**Deadlock**: Two transactions wait for each other indefinitely.

```sql
-- Time  Transaction 1             Transaction 2
-- T1    LOCK account 1
-- T2                              LOCK account 2
-- T3    Wait for account 2
-- T4                              Wait for account 1
-- Deadlock! Both wait forever
```

**Deadlock Detection:**
- Use wait-for graph
- Find cycles in graph
- If cycle exists → deadlock

**Deadlock Prevention:**
- Lock all resources at once
- Use timeout
- Lock in same order

**Deadlock Resolution:**
- Abort one transaction (victim selection)
- Let other proceed

---

### 9. Transaction Commands

#### **BEGIN/START TRANSACTION**
```sql
BEGIN;
-- OR
START TRANSACTION;
```

#### **COMMIT**
```sql
COMMIT;  -- Make changes permanent
```

#### **ROLLBACK**
```sql
ROLLBACK;  -- Undo all changes
```

#### **SAVEPOINT**
```sql
BEGIN;
    INSERT INTO courses VALUES (...);
    SAVEPOINT sp1;

    INSERT INTO topics VALUES (...);
    -- Error occurs

    ROLLBACK TO sp1;  -- Undo only after savepoint
    -- courses insert still valid
COMMIT;
```

---

## 🎯 CourseDB-AI Transaction Examples

### Example 1: Create Course with Topics
```sql
BEGIN;
    INSERT INTO courses (course_code, course_title, credit)
    VALUES ('CS301', 'Advanced DBMS', 3)
    RETURNING course_id;  -- Get generated ID

    INSERT INTO topics (course_id, topic_name, week_number)
    VALUES (LASTVAL(), 'Query Optimization', 1);

    INSERT INTO topics (course_id, topic_name, week_number)
    VALUES (LASTVAL(), 'Transactions', 2);
COMMIT;
-- All succeed or all fail (atomicity)
```

### Example 2: Update with Validation
```sql
BEGIN;
    -- Check if course exists
    SELECT course_id FROM courses WHERE course_code = 'CS201';

    -- Update questions
    UPDATE questions
    SET difficulty = 'hard'
    WHERE course_id = 1 AND year = 2023;

    -- Verify update
    SELECT COUNT(*) FROM questions
    WHERE course_id = 1 AND difficulty = 'hard';

COMMIT;
```

### Example 3: Error Handling
```python
# Python with SQLAlchemy
from sqlalchemy.exc import IntegrityError

try:
    db.begin()
    db.add(new_course)
    db.add(new_topic)
    db.commit()
except IntegrityError:
    db.rollback()  # Undo changes on error
    raise HTTPException(status_code=400, detail="Constraint violation")
```

---

## ✅ Self-Check Questions

1. What are the four ACID properties?
2. What's the difference between dirty read and unrepeatable read?
3. Which isolation level prevents phantom reads?
4. What's a deadlock? How is it detected?
5. What's the difference between shared and exclusive locks?
6. What are the two phases in Two-Phase Locking?
7. When would you use SAVEPOINT?
8. What's the default isolation level in PostgreSQL?

---

## 🔬 Hands-On Exercises

### Exercise 1: Test Atomicity
```sql
BEGIN;
    INSERT INTO courses VALUES (100, 'TEST', 'Test Course', 3);
    INSERT INTO topics VALUES (1, 999, 'Test', 1);  -- Error: FK violation
COMMIT;

-- Check: Was course inserted? (No - atomicity!)
SELECT * FROM courses WHERE course_id = 100;
```

### Exercise 2: Simulate Deadlock
```sql
-- Terminal 1
BEGIN;
UPDATE accounts SET balance = balance - 10 WHERE id = 1;
-- Wait here...
UPDATE accounts SET balance = balance + 10 WHERE id = 2;
COMMIT;

-- Terminal 2 (run while Terminal 1 is waiting)
BEGIN;
UPDATE accounts SET balance = balance - 10 WHERE id = 2;
UPDATE accounts SET balance = balance + 10 WHERE id = 1;  -- Deadlock!
COMMIT;
```

---

**Next Week (Week 10):** Semantic search with embeddings and pgvector!

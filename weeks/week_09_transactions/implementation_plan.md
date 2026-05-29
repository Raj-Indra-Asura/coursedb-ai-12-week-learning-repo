# Week 9: Transactions & Concurrency - 7-Day Implementation Plan

## 📅 Overview

This 7-day plan guides you through mastering transactions and concurrency control. Each day builds on the previous, with hands-on exercises and clear checkpoints.

**Time commitment:** 4-6 hours per day  
**Prerequisites:** Week 8 (Query Optimization) completed  
**Tools needed:** PostgreSQL, two terminal windows, Python/SQLAlchemy

---

## Day 1: ACID Properties & Transaction Basics

### Morning (2-3 hours): Understanding ACID

**Reading:**
- README.md Sections 1-3 (What is a Transaction, ACID, Lifecycle)
- theory_notes.md Sections 1-2

**Hands-On:**
1. Complete Exercise 1.1 (Test Atomicity)
   ```sql
   -- Test successful and failed transactions
   -- Verify all-or-nothing behavior
   ```

2. Complete Exercise 1.2 (Test Consistency)
   ```sql
   -- Test FK and check constraints
   -- Verify constraints enforced
   ```

3. Complete Exercise 1.3 (Test Isolation)
   ```sql
   -- Two terminals
   -- Verify uncommitted changes not visible
   ```

4. Complete Exercise 1.4 (Test Durability)
   ```sql
   -- Commit and reconnect
   -- Verify changes persist
   ```

**Deliverable:** Notes on each ACID property with examples

### Afternoon (2-3 hours): Transaction Commands

**Reading:**
- README.md Section 9 (Transaction Commands)

**Hands-On:**
1. Practice BEGIN/COMMIT/ROLLBACK
   ```sql
   BEGIN;
   -- Operations
   COMMIT;  -- or ROLLBACK;
   ```

2. Test SAVEPOINT
   ```sql
   BEGIN;
   -- Operation 1
   SAVEPOINT sp1;
   -- Operation 2 (might fail)
   ROLLBACK TO sp1;  -- Undo only Operation 2
   COMMIT;
   ```

3. Create CourseDB-AI transaction examples:
   ```sql
   -- Create course with topics atomically
   -- Update with validation
   -- Batch operations
   ```

**Deliverable:** SQL scripts for common transaction patterns

### Checkpoint Questions

- [ ] Can you explain all 4 ACID properties?
- [ ] Do you understand transaction lifecycle?
- [ ] Can you use BEGIN/COMMIT/ROLLBACK?
- [ ] When would you use SAVEPOINT?
- [ ] Confidence rating: _____ / 5

---

## Day 2: Concurrency Problems

### Morning (2-3 hours): Understanding Problems

**Reading:**
- README.md Section 4 (Concurrency Problems)
- theory_notes.md Section 4

**Study each problem:**
1. **Lost Update**
   - Why it happens
   - Real-world impact
   - How to prevent

2. **Dirty Read**
   - Reading uncommitted data
   - Why dangerous
   - Prevention

3. **Unrepeatable Read**
   - Same query, different results
   - When problematic
   - Solutions

4. **Phantom Read**
   - Different rows appear
   - Distinction from unrepeatable
   - Prevention

**Deliverable:** Summary table comparing all 4 problems

### Afternoon (2-3 hours): Simulate Problems

**Hands-On:**
1. Complete Exercise 2.1 (Lost Update)
   ```sql
   -- Two terminals
   -- Demonstrate problem
   -- Fix with SELECT FOR UPDATE
   ```

2. Complete Exercise 2.2 (Dirty Read)
   ```sql
   -- Try with READ UNCOMMITTED
   -- Note: PostgreSQL treats as READ COMMITTED
   ```

3. Complete Exercise 2.3 (Unrepeatable Read)
   ```sql
   -- Two terminals
   -- Show different reads in same transaction
   ```

4. Complete Exercise 2.4 (Phantom Read)
   ```sql
   -- INSERT during transaction
   -- See phantom row appear
   ```

**Deliverable:** Working examples of each concurrency problem

### Checkpoint Questions

- [ ] Can you explain each concurrency problem?
- [ ] Can you simulate lost update?
- [ ] Do you understand why dirty reads are dangerous?
- [ ] What's difference between unrepeatable and phantom read?
- [ ] Confidence rating: _____ / 5

---

## Day 3: Isolation Levels

### Morning (2-3 hours): Understanding Levels

**Reading:**
- README.md Section 5 (Isolation Levels)
- theory_notes.md Section 5

**Create comparison table:**

| Level | Prevents | Performance | Use When |
|-------|----------|-------------|----------|
| Read Uncommitted | Nothing | Fastest | ? |
| Read Committed | Dirty reads | Fast | ? |
| Repeatable Read | Dirty + Unrepeatable | Slower | ? |
| Serializable | All | Slowest | ? |

**For each level, understand:**
- What problems it prevents
- What problems it allows
- Performance impact
- Real-world use cases

**Deliverable:** Completed comparison table with use cases

### Afternoon (2-3 hours): Test All Levels

**Hands-On:**
1. Complete Exercise 3.1 (Compare All Levels)
   ```sql
   -- Test each isolation level
   -- Document behavior differences
   ```

2. Test with CourseDB-AI queries:
   ```sql
   -- Read Committed: View courses list
   -- Repeatable Read: Generate analytics report
   -- Serializable: Process enrollments
   ```

3. Measure performance impact:
   ```sql
   -- Same query at different isolation levels
   -- Use EXPLAIN ANALYZE
   -- Record execution times
   ```

**Deliverable:** Performance comparison and use case guide

### Checkpoint Questions

- [ ] Can you explain all 4 isolation levels?
- [ ] Which level is default in PostgreSQL?
- [ ] Can you choose appropriate level for a scenario?
- [ ] Do you understand the performance trade-offs?
- [ ] Confidence rating: _____ / 5

---

## Day 4: Locking Mechanisms

### Morning (2-3 hours): Understanding Locks

**Reading:**
- README.md Sections 6-7 (Locking, Two-Phase Locking)
- theory_notes.md Sections 6-7

**Study:**
1. **Shared Lock (S-Lock)**
   - When acquired
   - What it allows/prevents
   - Compatibility

2. **Exclusive Lock (X-Lock)**
   - When acquired
   - What it allows/prevents
   - Compatibility

3. **Two-Phase Locking (2PL)**
   - Growing phase
   - Shrinking phase
   - Why it ensures serializability

**Deliverable:** Lock compatibility table and 2PL diagram

### Afternoon (2-3 hours): Practice Locking

**Hands-On:**
1. Complete Exercise 4.1 (Shared vs Exclusive)
   ```sql
   -- Test FOR SHARE (shared lock)
   -- Test FOR UPDATE (exclusive lock)
   -- Test compatibility
   ```

2. Complete Exercise 4.2 (Lock Timeout)
   ```sql
   -- Set statement_timeout
   -- Test timeout behavior
   ```

3. Implement safe enrollment:
   ```sql
   BEGIN;
   -- Lock course
   SELECT * FROM courses 
   WHERE course_id = 1 
   FOR UPDATE;
   
   -- Check capacity
   -- Enroll if available
   COMMIT;
   ```

**Deliverable:** Safe concurrent operation patterns

### Checkpoint Questions

- [ ] Can you explain shared vs exclusive locks?
- [ ] When do you use FOR SHARE vs FOR UPDATE?
- [ ] What is Two-Phase Locking?
- [ ] Why are lock timeouts important?
- [ ] Confidence rating: _____ / 5

---

## Day 5: Deadlocks

### Morning (2-3 hours): Understanding Deadlocks

**Reading:**
- README.md Section 8 (Deadlock)
- theory_notes.md Section 8

**Study:**
1. **What is deadlock?**
   - Two transactions wait forever
   - Circular wait condition
   - Real-world examples

2. **Detection**
   - Wait-for graph
   - Cycle detection
   - PostgreSQL's deadlock_timeout

3. **Prevention**
   - Lock ordering
   - Timeout
   - Lock all at once

4. **Resolution**
   - Victim selection
   - Automatic rollback
   - Retry strategy

**Deliverable:** Deadlock prevention checklist

### Afternoon (2-3 hours): Deadlock Lab

**Hands-On:**
1. Complete Exercise 5.1 (Create Deadlock)
   ```sql
   -- Two terminals
   -- Lock resources in opposite order
   -- Trigger deadlock
   ```

2. Complete Exercise 5.2 (Prevent with Ordering)
   ```sql
   -- Lock in consistent order
   -- Verify no deadlock
   ```

3. Complete Exercise 5.3 (Detection Query)
   ```sql
   -- Enable lock logging
   -- Query pg_locks
   -- Find blocking transactions
   ```

4. Document deadlock in CourseDB-AI:
   - Where could deadlocks occur?
   - Prevention strategies for each
   - Monitoring approach

**Deliverable:** Deadlock scenarios and prevention for CourseDB-AI

### Checkpoint Questions

- [ ] Can you explain what causes deadlock?
- [ ] Can you create a deadlock intentionally?
- [ ] How do you prevent deadlocks?
- [ ] What happens when deadlock detected?
- [ ] Confidence rating: _____ / 5

---

## Day 6: SQLAlchemy Transactions

### Morning (2-3 hours): Python Transactions

**Reading:**
- README.md Section 10 (Transactions in SQLAlchemy)

**Study:**
1. Session management
   ```python
   with Session(engine) as session:
       # Auto-commit/rollback
   ```

2. Explicit control
   ```python
   session.begin()
   session.commit()
   session.rollback()
   ```

3. Nested transactions
   ```python
   session.begin_nested()  # Savepoint
   ```

4. Isolation levels
   ```python
   session.connection(
       execution_options={"isolation_level": "SERIALIZABLE"}
   )
   ```

**Deliverable:** Python transaction patterns guide

### Afternoon (2-3 hours): Implement in Code

**Hands-On:**
1. Complete Exercise 6.1 (Basic Transaction)
   ```python
   def create_course_with_topics():
       # Implement atomic creation
   ```

2. Complete Exercise 6.2 (Nested Transaction)
   ```python
   def create_with_optional_topics():
       # Use savepoints for partial rollback
   ```

3. Complete Exercise 6.3 (Retry on Deadlock)
   ```python
   def transfer_with_retry():
       # Exponential backoff
   ```

4. Add transactions to CourseDB-AI API:
   ```python
   # POST /api/courses (create with topics)
   # PUT /api/courses/{id}/enroll (safe enrollment)
   # POST /api/bulk-import (batch operations)
   ```

**Deliverable:** Updated API endpoints with proper transactions

### Checkpoint Questions

- [ ] Can you implement transactions in SQLAlchemy?
- [ ] Do you understand session management?
- [ ] Can you use nested transactions?
- [ ] Can you handle deadlocks with retry logic?
- [ ] Confidence rating: _____ / 5

---

## Day 7: Real-World Patterns & Review

### Morning (2-3 hours): Advanced Patterns

**Reading:**
- README.md Sections 11-13 (Patterns, Best Practices, Debugging)

**Study patterns:**
1. **Optimistic Locking**
   ```python
   # Version-based concurrency control
   class Course:
       version = Column(Integer, default=0)
   
   # Check version on update
   ```

2. **SELECT FOR UPDATE patterns**
   ```python
   # Lock specific rows
   course = session.query(Course).filter_by(
       course_id=1
   ).with_for_update().one()
   ```

3. **Idempotent operations**
   ```python
   # Safe to retry without side effects
   def enroll_student(student_id, course_id):
       # Check if already enrolled
       # Insert only if not exists
   ```

**Deliverable:** Pattern library for common scenarios

### Afternoon (2-3 hours): Review & Testing

**1. Complete challenge exercises**
   - Challenge 1: Implement optimistic locking
   - Challenge 2: Build wait-for graph

**2. Review all checkpoints**
   - Go through Days 1-6 checkpoint questions
   - Fill any knowledge gaps

**3. Test CourseDB-API transactions**
   ```python
   # Test concurrent enrollments
   # Test bulk operations
   # Test deadlock handling
   # Test rollback on error
   ```

**4. Document learnings**
   - What surprised you?
   - What's still confusing?
   - What patterns will you use?

**Deliverable:** Complete Week 9 reflection.md

### Final Checkpoint

- [ ] Can you explain all ACID properties?
- [ ] Can you identify and fix concurrency problems?
- [ ] Can you choose appropriate isolation levels?
- [ ] Do you understand locking mechanisms?
- [ ] Can you prevent and handle deadlocks?
- [ ] Can you implement transactions in SQLAlchemy?
- [ ] Have you applied transactions to CourseDB-AI?
- [ ] Overall confidence rating: _____ / 5

---

## Week Completion Checklist

**Theory Understanding:**
- [ ] ACID properties clear
- [ ] Concurrency problems understood
- [ ] Isolation levels compared
- [ ] Locking mechanisms explained
- [ ] Deadlock causes and prevention
- [ ] Two-Phase Locking understood

**Practical Skills:**
- [ ] Can write SQL transactions
- [ ] Can simulate concurrency problems
- [ ] Can test different isolation levels
- [ ] Can create and prevent deadlocks
- [ ] Can implement in SQLAlchemy
- [ ] Can handle deadlocks with retry

**Applied to CourseDB-AI:**
- [ ] API endpoints use transactions
- [ ] Appropriate isolation levels chosen
- [ ] Deadlock prevention implemented
- [ ] Error handling with rollback
- [ ] Testing concurrent scenarios

**Documentation:**
- [ ] All exercises completed
- [ ] Checkpoints answered
- [ ] Reflection.md filled out
- [ ] Pattern library created

---

## Common Pitfalls to Avoid

1. **Long transactions** - Keep transactions short
2. **Blocking user input** - Never wait for user during transaction
3. **Wrong isolation level** - Don't use Serializable by default
4. **Ignoring deadlocks** - Always implement retry logic
5. **No error handling** - Always catch and rollback on error
6. **Inconsistent lock order** - Document locking order
7. **Testing only happy path** - Test concurrent scenarios

---

## Additional Resources

**PostgreSQL Documentation:**
- [Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html)
- [Explicit Locking](https://www.postgresql.org/docs/current/explicit-locking.html)
- [Lock Monitoring](https://www.postgresql.org/docs/current/monitoring-locks.html)

**SQLAlchemy Documentation:**
- [Session Basics](https://docs.sqlalchemy.org/en/20/orm/session_basics.html)
- [Session Transaction](https://docs.sqlalchemy.org/en/20/orm/session_transaction.html)

**Next Week:** Week 10 - Semantic Search with Embeddings and pgvector!

---

## Progress Tracking

**Daily Time Log:**
```
Day 1: ____ hours - ACID & Basics
Day 2: ____ hours - Concurrency Problems
Day 3: ____ hours - Isolation Levels
Day 4: ____ hours - Locking
Day 5: ____ hours - Deadlocks
Day 6: ____ hours - SQLAlchemy
Day 7: ____ hours - Review & Apply

Total: ____ hours
```

**Confidence Growth:**
```
Day 1: ____ / 5
Day 2: ____ / 5
Day 3: ____ / 5
Day 4: ____ / 5
Day 5: ____ / 5
Day 6: ____ / 5
Day 7: ____ / 5
```

**Key Takeaways:**
1. _________________________________________________
2. _________________________________________________
3. _________________________________________________
4. _________________________________________________
5. _________________________________________________

**Questions for Further Study:**
1. _________________________________________________
2. _________________________________________________
3. _________________________________________________

---

**Remember:** Transactions are critical for data integrity. Take time to understand deeply - the patterns you learn this week apply to every database application you'll build!

# Week 9: Transactions & Concurrency - Daily Checkpoints

## 🎯 Purpose

Track your progress through Week 9 with concrete, measurable checkpoints. Use these to verify understanding before moving forward.

**How to use:**
- Complete checkpoints at end of each day
- Be honest - gaps in understanding compound
- Revisit earlier days if needed
- Aim for 4/5 or 5/5 confidence before proceeding

---

## Day 1: ACID Properties & Transaction Basics

### Knowledge Checkpoints

**ACID Properties:**
- [ ] I can explain Atomicity with a real example
- [ ] I can explain Consistency and give an example constraint
- [ ] I can explain Isolation and why it matters
- [ ] I can explain Durability and how PostgreSQL ensures it
- [ ] I can describe when each property might be violated

**Transaction Lifecycle:**
- [ ] I can draw the transaction state diagram
- [ ] I can explain what happens in each state
- [ ] I understand difference between PARTIALLY COMMITTED and COMMITTED
- [ ] I know what causes FAILED → ABORTED transition

**Transaction Commands:**
- [ ] I can write a transaction with BEGIN/COMMIT
- [ ] I know when to use ROLLBACK
- [ ] I understand what SAVEPOINT does
- [ ] I can use ROLLBACK TO SAVEPOINT

### Practical Checkpoints

**Exercises Completed:**
- [ ] Exercise 1.1: Test Atomicity (success and failure cases)
- [ ] Exercise 1.2: Test Consistency (FK and CHECK constraints)
- [ ] Exercise 1.3: Test Isolation (two terminals)
- [ ] Exercise 1.4: Test Durability (reconnect test)

**Can I Do This:**
```sql
-- Write a transaction that creates course with topics
-- If any topic fails, entire transaction rolls back

[ ] Yes, confidently
[ ] Yes, with reference
[ ] Not yet
```

### Self-Assessment

**Understanding (rate 1-5):**
- Atomicity: _____ / 5
- Consistency: _____ / 5
- Isolation: _____ / 5
- Durability: _____ / 5
- Transaction commands: _____ / 5

**Overall Day 1 confidence: _____ / 5**

**What I learned today:**
```
_________________________________________________________________
_________________________________________________________________
```

**What's still unclear:**
```
_________________________________________________________________
_________________________________________________________________
```

---

## Day 2: Concurrency Problems

### Knowledge Checkpoints

**Lost Update:**
- [ ] I can explain what lost update is
- [ ] I can describe a scenario where it causes real harm
- [ ] I know how to prevent it (SELECT FOR UPDATE)
- [ ] I understand why simple reads aren't enough

**Dirty Read:**
- [ ] I can explain what dirty read is
- [ ] I understand why it's dangerous
- [ ] I know which isolation level prevents it
- [ ] I understand PostgreSQL's behavior (no true dirty reads)

**Unrepeatable Read:**
- [ ] I can explain unrepeatable read
- [ ] I can distinguish it from lost update
- [ ] I know when it's actually a problem
- [ ] I know which isolation level prevents it

**Phantom Read:**
- [ ] I can explain phantom read
- [ ] I can distinguish it from unrepeatable read
- [ ] I understand when phantoms matter
- [ ] I know which isolation level prevents it

### Practical Checkpoints

**Exercises Completed:**
- [ ] Exercise 2.1: Lost Update (demonstrated and fixed)
- [ ] Exercise 2.2: Dirty Read (attempted)
- [ ] Exercise 2.3: Unrepeatable Read (demonstrated)
- [ ] Exercise 2.4: Phantom Read (demonstrated)

**Can I Do This:**
```
Explain to someone else the difference between:
- Lost update vs unrepeatable read
- Unrepeatable read vs phantom read

[ ] Yes, clearly
[ ] Somewhat
[ ] Not yet
```

### Comparison Table

Fill out this table from memory:

| Problem | What Happens | Example Scenario | How to Prevent |
|---------|-------------|------------------|----------------|
| Lost Update | _____________ | _____________ | _____________ |
| Dirty Read | _____________ | _____________ | _____________ |
| Unrepeatable Read | _____________ | _____________ | _____________ |
| Phantom Read | _____________ | _____________ | _____________ |

### Self-Assessment

**Understanding (rate 1-5):**
- Lost Update: _____ / 5
- Dirty Read: _____ / 5
- Unrepeatable Read: _____ / 5
- Phantom Read: _____ / 5
- Overall concurrency: _____ / 5

**Overall Day 2 confidence: _____ / 5**

**Most important lesson today:**
```
_________________________________________________________________
_________________________________________________________________
```

---

## Day 3: Isolation Levels

### Knowledge Checkpoints

**Isolation Levels:**
- [ ] I can name all 4 isolation levels
- [ ] I can explain what each level prevents
- [ ] I understand the performance trade-offs
- [ ] I know PostgreSQL's default (READ COMMITTED)
- [ ] I can choose appropriate level for a scenario

**Read Uncommitted:**
- [ ] I know what it prevents (nothing)
- [ ] I know PostgreSQL treats it as READ COMMITTED
- [ ] I understand when (never!) to use it

**Read Committed:**
- [ ] I know what it prevents (dirty reads)
- [ ] I know what it allows (unrepeatable, phantom)
- [ ] I understand when to use it (default for most operations)

**Repeatable Read:**
- [ ] I know what it prevents (dirty, unrepeatable)
- [ ] I know what it allows (phantoms in some DBs)
- [ ] I understand when to use it (reports, analytics)

**Serializable:**
- [ ] I know what it prevents (all concurrency issues)
- [ ] I understand the performance cost
- [ ] I know when to use it (critical operations only)

### Practical Checkpoints

**Exercises Completed:**
- [ ] Exercise 3.1: Compared all isolation levels
- [ ] Tested with CourseDB-AI queries
- [ ] Measured performance impact

**Can I Do This:**
```sql
-- Choose isolation level for:
1. Viewing course list: _______________________
2. Enrolling in course: _______________________
3. Generating monthly report: _______________________
4. Processing payments: _______________________

[ ] All correct
[ ] Mostly correct
[ ] Need review
```

### Comparison Table

Complete from memory:

| Level | Prevents | Allows | Performance | Use When |
|-------|----------|--------|-------------|----------|
| Read Uncommitted | _______ | _______ | _______ | _______ |
| Read Committed | _______ | _______ | _______ | _______ |
| Repeatable Read | _______ | _______ | _______ | _______ |
| Serializable | _______ | _______ | _______ | _______ |

### Self-Assessment

**Understanding (rate 1-5):**
- Isolation level concepts: _____ / 5
- Choosing right level: _____ / 5
- Performance trade-offs: _____ / 5
- PostgreSQL specifics: _____ / 5

**Overall Day 3 confidence: _____ / 5**

**Key insight today:**
```
_________________________________________________________________
_________________________________________________________________
```

---

## Day 4: Locking Mechanisms

### Knowledge Checkpoints

**Lock Types:**
- [ ] I can explain shared lock (S-Lock)
- [ ] I can explain exclusive lock (X-Lock)
- [ ] I know the compatibility rules
- [ ] I understand when each is acquired

**SQL Locking:**
- [ ] I can use SELECT ... FOR SHARE
- [ ] I can use SELECT ... FOR UPDATE
- [ ] I know when to use each
- [ ] I understand implicit vs explicit locking

**Two-Phase Locking:**
- [ ] I can explain the growing phase
- [ ] I can explain the shrinking phase
- [ ] I understand why it ensures serializability
- [ ] I know the limitations

### Practical Checkpoints

**Exercises Completed:**
- [ ] Exercise 4.1: Shared vs Exclusive locks
- [ ] Exercise 4.2: Lock timeout
- [ ] Implemented safe enrollment with locking

**Lock Compatibility Table**

Fill from memory:

|   | Shared | Exclusive |
|---|--------|-----------|
| **Shared** | _______ | _______ |
| **Exclusive** | _______ | _______ |

**Can I Do This:**
```sql
-- Write query that:
1. Locks course for reading (others can read too)
2. Locks course for writing (exclusive)
3. Checks capacity and enrolls atomically

[ ] All correct
[ ] Need hints
[ ] Not yet
```

### Self-Assessment

**Understanding (rate 1-5):**
- Lock types: _____ / 5
- FOR SHARE vs FOR UPDATE: _____ / 5
- Two-Phase Locking: _____ / 5
- When to use locking: _____ / 5

**Overall Day 4 confidence: _____ / 5**

**Most useful technique learned:**
```
_________________________________________________________________
_________________________________________________________________
```

---

## Day 5: Deadlocks

### Knowledge Checkpoints

**Understanding Deadlocks:**
- [ ] I can explain what deadlock is
- [ ] I can describe how deadlocks form
- [ ] I can draw a wait-for graph
- [ ] I understand cycle detection

**Prevention:**
- [ ] I know lock ordering strategy
- [ ] I understand timeout approach
- [ ] I know "lock all at once" pattern
- [ ] I can choose appropriate strategy

**Detection & Resolution:**
- [ ] I understand PostgreSQL's deadlock detection
- [ ] I know what happens to victim transaction
- [ ] I can write retry logic
- [ ] I understand exponential backoff

### Practical Checkpoints

**Exercises Completed:**
- [ ] Exercise 5.1: Created deadlock
- [ ] Exercise 5.2: Prevented with ordering
- [ ] Exercise 5.3: Deadlock detection query

**Can I Do This:**
```
1. Explain why this code deadlocks:
   Transaction 1: Lock A, then B
   Transaction 2: Lock B, then A

2. Fix it with lock ordering

3. Write retry logic with backoff

[ ] All correct
[ ] Partially
[ ] Need review
```

### Wait-For Graph

Draw a wait-for graph for the classic deadlock:

```
Transaction 1: Holds ___, Waits for ___
Transaction 2: Holds ___, Waits for ___

Cycle: ___________________________
```

### Self-Assessment

**Understanding (rate 1-5):**
- What causes deadlocks: _____ / 5
- Prevention strategies: _____ / 5
- Detection & resolution: _____ / 5
- Implementing retry logic: _____ / 5

**Overall Day 5 confidence: _____ / 5**

**Most important lesson:**
```
_________________________________________________________________
_________________________________________________________________
```

---

## Day 6: SQLAlchemy Transactions

### Knowledge Checkpoints

**Session Management:**
- [ ] I understand Session lifecycle
- [ ] I can use context manager (with Session)
- [ ] I know when to use begin/commit explicitly
- [ ] I always handle exceptions with rollback

**Transaction Patterns:**
- [ ] I can implement basic transaction
- [ ] I can use nested transactions (savepoints)
- [ ] I can set isolation level
- [ ] I can implement retry logic for deadlocks

**Best Practices:**
- [ ] I always close sessions
- [ ] I keep transactions short
- [ ] I separate validation from updates
- [ ] I handle errors gracefully

### Practical Checkpoints

**Exercises Completed:**
- [ ] Exercise 6.1: Basic transaction
- [ ] Exercise 6.2: Nested transaction
- [ ] Exercise 6.3: Retry on deadlock
- [ ] Applied transactions to CourseDB-AI API

**Can I Do This:**
```python
# Write a function that:
1. Creates course with topics (atomic)
2. Uses savepoint for optional operations
3. Handles deadlocks with retry
4. Properly closes session

[ ] Yes, confidently
[ ] With reference
[ ] Not yet
```

### Code Review

Review this code - what's wrong?

```python
def update_course(course_id, new_title):
    session = Session(engine)
    course = session.query(Course).filter_by(course_id=course_id).one()
    course.course_title = new_title
    session.commit()
    return course

Issues found:
1. _________________________________________________________________
2. _________________________________________________________________
3. _________________________________________________________________
```

### Self-Assessment

**Understanding (rate 1-5):**
- Session management: _____ / 5
- Transaction patterns: _____ / 5
- Error handling: _____ / 5
- Best practices: _____ / 5

**Overall Day 6 confidence: _____ / 5**

**Pattern I'll use most:**
```
_________________________________________________________________
_________________________________________________________________
```

---

## Day 7: Review & Real-World Patterns

### Knowledge Checkpoints

**Advanced Patterns:**
- [ ] I understand optimistic locking
- [ ] I can implement version-based concurrency control
- [ ] I understand idempotent operations
- [ ] I know when to use each pattern

**Best Practices:**
- [ ] I can list 5+ transaction best practices
- [ ] I know common mistakes to avoid
- [ ] I understand when to optimize
- [ ] I can debug transaction issues

**Debugging:**
- [ ] I can query pg_locks
- [ ] I can find blocking transactions
- [ ] I can identify deadlock causes
- [ ] I know how to monitor transactions

### Practical Checkpoints

**Challenge Exercises:**
- [ ] Challenge 1: Optimistic locking (completed or attempted)
- [ ] Challenge 2: Wait-for graph (completed or attempted)

**Applied to CourseDB-AI:**
- [ ] API endpoints use transactions
- [ ] Appropriate isolation levels chosen
- [ ] Error handling implemented
- [ ] Deadlock retry logic added
- [ ] Tested concurrent scenarios

### Comprehensive Self-Test

Answer without reference:

1. **Four ACID properties:**
   ```
   A: _________________________________________________________________
   C: _________________________________________________________________
   I: _________________________________________________________________
   D: _________________________________________________________________
   ```

2. **Four concurrency problems:**
   ```
   1. _________________________________________________________________
   2. _________________________________________________________________
   3. _________________________________________________________________
   4. _________________________________________________________________
   ```

3. **When to use each isolation level:**
   ```
   Read Committed: ____________________________________________________
   Repeatable Read: ___________________________________________________
   Serializable: ______________________________________________________
   ```

4. **Deadlock prevention strategies:**
   ```
   1. _________________________________________________________________
   2. _________________________________________________________________
   3. _________________________________________________________________
   ```

5. **Transaction best practices:**
   ```
   1. _________________________________________________________________
   2. _________________________________________________________________
   3. _________________________________________________________________
   4. _________________________________________________________________
   5. _________________________________________________________________
   ```

### Self-Assessment

**Overall Week 9 Understanding:**
- ACID properties: _____ / 5
- Concurrency problems: _____ / 5
- Isolation levels: _____ / 5
- Locking: _____ / 5
- Deadlocks: _____ / 5
- SQLAlchemy: _____ / 5
- Real-world application: _____ / 5

**Overall Week 9 confidence: _____ / 5**

---

## Week 9 Completion Checklist

### Theory Mastery

- [ ] Can explain all ACID properties
- [ ] Can describe all concurrency problems
- [ ] Can compare all isolation levels
- [ ] Understand locking mechanisms
- [ ] Know deadlock causes and prevention
- [ ] Understand Two-Phase Locking

### Practical Skills

- [ ] Can write SQL transactions
- [ ] Can simulate concurrency problems
- [ ] Can test different isolation levels
- [ ] Can create and prevent deadlocks
- [ ] Can implement in SQLAlchemy
- [ ] Can handle deadlocks with retry

### Applied Knowledge

- [ ] API endpoints use transactions appropriately
- [ ] Chose appropriate isolation levels
- [ ] Implemented proper error handling
- [ ] Added deadlock retry logic
- [ ] Tested concurrent scenarios
- [ ] Documented transaction strategy

### Documentation

- [ ] All exercises completed (or attempted)
- [ ] All daily checkpoints filled
- [ ] Reflection.md completed
- [ ] Implementation plan followed
- [ ] Mistakes reviewed

---

## Final Reflection

**Most valuable lesson from Week 9:**
```
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
```

**Biggest challenge overcome:**
```
_________________________________________________________________
_________________________________________________________________
```

**How I'll apply this in real projects:**
```
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
```

**What I'll continue studying:**
```
_________________________________________________________________
_________________________________________________________________
```

**Ready for Week 10? (Yes/Not Yet): __________**

If "Not Yet", what needs review:
```
_________________________________________________________________
_________________________________________________________________
```

---

## Progress Metrics

**Time Invested:**
```
Day 1: _____ hours
Day 2: _____ hours
Day 3: _____ hours
Day 4: _____ hours
Day 5: _____ hours
Day 6: _____ hours
Day 7: _____ hours

Total: _____ hours
```

**Exercises Completed:**
```
Total exercises: 21 (6 sets × 3-4 exercises each)
Completed: _____ / 21
Completion rate: _____ %
```

**Confidence Growth:**
```
Day 1: _____ / 5
Day 2: _____ / 5
Day 3: _____ / 5
Day 4: _____ / 5
Day 5: _____ / 5
Day 6: _____ / 5
Day 7: _____ / 5

Growth: _____ points
```

---

**Congratulations on completing Week 9! You now understand one of the most critical aspects of database systems - ensuring data integrity in multi-user environments. These skills will serve you throughout your career!**

**Next:** Week 10 - Semantic Search with Embeddings and pgvector!

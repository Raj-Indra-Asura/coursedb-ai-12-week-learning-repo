# Week 8: Query Optimization & Performance Tuning - Common Mistakes and How to Fix Them

## 🎯 Purpose

Week 8 teaches systematic query optimization. This guide prepares you for common mistakes with:
- EXPLAIN interpretation errors
- Optimization gone wrong
- Measurement pitfalls
- Over-optimization
- Statistics and maintenance issues

---

## Mistake Category 1: EXPLAIN Interpretation Errors

### Mistake 1.1: Confusing Cost with Time

**What happens:**
```sql
EXPLAIN SELECT * FROM questions WHERE year = 2023;

-- Output:
-- Seq Scan on questions  (cost=0.00..35.50 rows=50 width=200)

-- Developer thinks: "Cost 35.50 means 35.50 milliseconds"
```

**Why it's wrong:**
Cost is arbitrary units for comparing plans, NOT execution time!

**How to fix:**
```sql
-- Always use EXPLAIN ANALYZE for actual time
EXPLAIN ANALYZE SELECT * FROM questions WHERE year = 2023;

-- Output:
-- Seq Scan on questions  (cost=0.00..35.50 rows=50 width=200)
--                        (actual time=0.015..2.456 rows=48 loops=1)
-- Execution Time: 2.489 ms  ← REAL time!

-- Cost (35.50) is just for comparison
-- Execution Time (2.489ms) is what matters
```

**How to avoid:**
- Use EXPLAIN ANALYZE, not EXPLAIN
- Focus on "Execution Time" and "actual time"
- Use cost only to compare alternative plans

---

### Mistake 1.2: Ignoring Estimated vs Actual Rows

**What happens:**
```sql
EXPLAIN ANALYZE SELECT * FROM questions WHERE year = 2023;

-- Output:
-- (cost=... rows=50 width=200)       ← Estimated 50 rows
-- (actual time=... rows=5000 loops=1) ← Actually 5000 rows!

-- Developer doesn't notice 100x discrepancy!
```

**Why it matters:**
Large discrepancy → stale statistics → optimizer makes bad decisions → slow queries

**How to fix:**
```sql
-- Update statistics
ANALYZE questions;

-- Run query again
EXPLAIN ANALYZE SELECT * FROM questions WHERE year = 2023;

-- Output now shows:
-- (cost=... rows=5000 width=200)      ← Accurate estimate
-- (actual time=... rows=5000 loops=1) ← Matches actual
```

**How to avoid:**
- Always compare estimated vs actual rows
- Run ANALYZE after bulk data changes
- Set up autovacuum (usually enabled by default)
- Alert if estimates are >10x off

---

### Mistake 1.3: Not Looking at the Full Execution Plan

**What happens:**
```sql
EXPLAIN ANALYZE
SELECT c.*, COUNT(q.question_id)
FROM courses c
LEFT JOIN questions q ON c.course_id = q.course_id
GROUP BY c.course_id;

-- Developer only looks at top line:
-- "Hash Join (cost=15.00..50.00 rows=10 width=200)"
-- "Execution Time: 5.123 ms"

-- Misses that 95% of time is in one node deep in the plan!
```

**How to fix:**
```sql
-- Read the ENTIRE plan, especially high-cost nodes:

HashAggregate (cost=50.00..52.00 rows=10 width=200)
  (actual time=5.100..5.110 rows=10 loops=1)
  -> Hash Left Join (cost=15.00..45.00 rows=1000 width=200)
       (actual time=0.050..0.200 rows=1000 loops=1)
       -> Seq Scan on courses c (cost=0.00..10.00 rows=10 width=200)
            (actual time=0.010..0.015 rows=10 loops=1)
       -> Hash (cost=10.00..10.00 rows=1000 width=4)
            (actual time=0.030..0.030 rows=1000 loops=1)
            -> Seq Scan on questions q (cost=0.00..10.00 rows=1000 width=4)
                 (actual time=0.005..0.020 rows=1000 loops=1)  ← Bottleneck!

-- The HashAggregate takes 5.1ms of the total 5.123ms!
-- That's the real bottleneck, not the join
```

**How to avoid:**
- Read plan from bottom to top (execution order)
- Look for nodes with high "actual time"
- Check "loops" column (loops > 1 = repeated execution)
- Identify the slowest node

---

## Mistake Category 2: Premature or Wrong Optimization

### Mistake 2.1: Optimizing Before Measuring

**What happens:**
```sql
-- Developer thinks: "This query looks slow, I'll add an index"

CREATE INDEX idx_questions_difficulty ON questions(difficulty);

-- Query is still slow!
-- Index wasn't the problem
-- Now you have unused index eating space and slowing down writes
```

**How to fix:**
```sql
-- ALWAYS measure first
EXPLAIN ANALYZE SELECT * FROM questions WHERE difficulty = 'medium';

-- Output shows:
-- Seq Scan (cost=0..100 rows=333 width=200)
-- Execution Time: 1.5ms

-- Wait, 1.5ms is already fast!
-- Optimization not needed
-- Low selectivity (333 out of 1000 rows = 33%)
-- Seq Scan is correct choice
```

**How to avoid:**
- Always run EXPLAIN ANALYZE before optimizing
- Know your performance targets (is 10ms slow? 100ms? 1000ms?)
- Trust the optimizer when it chooses Seq Scan
- Remember: not every query needs to be fast, only user-facing ones

---

### Mistake 2.2: Creating Indexes on Low-Selectivity Columns

**What happens:**
```sql
-- Boolean column (true/false)
CREATE INDEX idx_questions_active ON questions(is_active);

-- Query:
SELECT * FROM questions WHERE is_active = true;

-- EXPLAIN shows: Seq Scan (index exists but not used!)
```

**Why it happens:**
If 50% of rows match, Seq Scan is faster than index (avoids random I/O)

**How to fix:**
```sql
-- Option 1: Accept Seq Scan (it's correct!)
-- If 50% of rows match, don't create index

-- Option 2: Partial index if one value is rare
CREATE INDEX idx_questions_inactive ON questions(question_id)
WHERE is_active = false;  -- Only 5% of rows

-- Now queries for inactive questions use index
SELECT * FROM questions WHERE is_active = false;
```

**Rule of thumb**: Only index if selectivity < 5-10%

---

### Mistake 2.3: Over-Indexing

**What happens:**
```sql
-- Developer creates index for every column
CREATE INDEX idx_q1 ON questions(year);
CREATE INDEX idx_q2 ON questions(difficulty);
CREATE INDEX idx_q3 ON questions(marks);
CREATE INDEX idx_q4 ON questions(course_id);
CREATE INDEX idx_q5 ON questions(topic_id);
CREATE INDEX idx_q6 ON questions(created_at);
CREATE INDEX idx_q7 ON questions(updated_at);

-- Result:
-- - 7 indexes eating 500KB+ disk
-- - INSERT takes 5x longer (must update 7 indexes!)
-- - Most indexes never used
```

**How to fix:**
```sql
-- Check index usage
SELECT
    indexname,
    idx_scan,
    pg_size_pretty(pg_relation_size(indexrelid)) as size
FROM pg_stat_user_indexes
WHERE tablename = 'questions'
ORDER BY idx_scan ASC;

-- Drop unused indexes (idx_scan = 0)
DROP INDEX idx_q3;  -- marks: never used
DROP INDEX idx_q6;  -- created_at: never used
DROP INDEX idx_q7;  -- updated_at: never used

-- Create composite indexes for common query patterns
CREATE INDEX idx_questions_search
ON questions(course_id, year, difficulty);  -- Covers multiple queries!
```

**How to avoid:**
- Start with fewer indexes
- Create based on actual query patterns
- Monitor usage with pg_stat_user_indexes
- Drop unused indexes

---

## Mistake Category 3: Query Rewriting Errors

### Mistake 3.1: Rewriting Query to Be Incorrect

**What happens:**
```sql
-- Original (correct but slow):
SELECT * FROM courses
WHERE course_id IN (SELECT course_id FROM questions WHERE year = 2023);

-- Developer rewrites to EXISTS:
SELECT * FROM courses c
WHERE EXISTS (
    SELECT 1 FROM questions q WHERE q.course_id = c.course_id
);

-- But forgot the WHERE year = 2023!
-- Now returns courses with ANY questions, not just 2023 questions
-- Query is faster but WRONG!
```

**How to fix:**
```sql
-- Correct rewrite:
SELECT * FROM courses c
WHERE EXISTS (
    SELECT 1 FROM questions q
    WHERE q.course_id = c.course_id AND q.year = 2023  ← Don't forget condition!
);

-- Verify correctness:
-- 1. Run both queries
-- 2. Compare row counts
-- 3. Spot check results
```

**How to avoid:**
- Test rewritten query returns same results
- Use EXCEPT to find differences:
  ```sql
  (SELECT * FROM original_query)
  EXCEPT
  (SELECT * FROM rewritten_query);
  -- Should return 0 rows
  ```
- Add assertion tests in code

---

### Mistake 3.2: Making Query Unreadable for Marginal Gain

**What happens:**
```sql
-- Original (clear, 50ms):
SELECT
    c.course_code,
    (SELECT COUNT(*) FROM questions WHERE course_id = c.course_id) as q_count
FROM courses c;

-- Optimized (obscure, 45ms):
SELECT
    c.course_code,
    COALESCE(q_agg.q_count, 0)
FROM courses c
LEFT JOIN LATERAL (
    SELECT COUNT(*) as q_count
    FROM questions
    WHERE course_id = c.course_id
) q_agg ON true;

-- 5ms faster but much harder to understand
-- Not worth it for non-critical query!
```

**How to fix:**
- Keep original if:
  - < 100ms execution time
  - Runs infrequently
  - Not user-facing
  - Marginal improvement (< 2x)

- Optimize if:
  - > 1000ms execution time
  - Called frequently
  - User-facing (impacts UX)
  - Big improvement (> 5x)

**Balance**: Maintainability vs performance

---

### Mistake 3.3: SELECT * When You Don't Need All Columns

**What happens:**
```sql
-- Bad: Fetches all 20 columns (200 bytes per row)
SELECT * FROM questions WHERE year = 2023;
-- Returns: 1000 rows × 200 bytes = 200KB

-- API only needs: question_id, question_text
-- Wasted: 150KB of network transfer and parsing
```

**How to fix:**
```sql
-- Good: Only fetch needed columns
SELECT question_id, question_text FROM questions WHERE year = 2023;
-- Returns: 1000 rows × 50 bytes = 50KB
-- 4x less data!

-- Benefits:
-- - Less I/O
-- - Less network transfer
-- - Enables covering indexes
-- - Faster JSON serialization
```

**How to avoid:**
- Never use SELECT * in production code
- Specify exact columns needed
- Review API responses - are you returning unused data?
- Use TypeScript/Pydantic to enforce contract

---

## Mistake Category 4: N+1 Query Pitfalls

### Mistake 4.1: Not Recognizing N+1 Pattern

**What happens:**
```python
# Looks innocent but is N+1!
courses = db.query(Course).all()  # 1 query
for course in courses:
    # Accessing relationship without eager loading
    topic_count = len(course.topics)  # N queries!
    # This triggers separate query for EACH course
```

**How to fix:**
```python
# Enable SQL logging to see the problem
engine = create_engine(DATABASE_URL, echo=True)

# Run the code
# See in logs:
# SELECT * FROM courses;
# SELECT * FROM topics WHERE course_id = 1;
# SELECT * FROM topics WHERE course_id = 2;
# SELECT * FROM topics WHERE course_id = 3;
# ...
# SELECT * FROM topics WHERE course_id = 100;
# 101 queries total!

# Fix with eager loading:
courses = db.query(Course).options(joinedload(Course.topics)).all()
# 1 query with JOIN
```

**How to avoid:**
- Enable SQL logging in development
- Count queries per endpoint
- Use database query profilers
- Code review for relationship access in loops

---

### Mistake 4.2: Using Wrong Eager Loading Strategy

**What happens:**
```python
# joinedload creates LEFT JOIN
courses = db.query(Course).options(
    joinedload(Course.topics),
    joinedload(Course.questions)  # Another relationship
).all()

# Generates:
# SELECT * FROM courses
# LEFT JOIN topics ON ...
# LEFT JOIN questions ON ...

# Problem: Cartesian product!
# 10 courses × 5 topics × 100 questions = 5000 rows returned
# When you only have 10 courses!
```

**How to fix:**
```python
# Use selectinload for one-to-many relationships
courses = db.query(Course).options(
    selectinload(Course.topics),
    selectinload(Course.questions)
).all()

# Generates 3 queries:
# SELECT * FROM courses;
# SELECT * FROM topics WHERE course_id IN (1,2,3,...);
# SELECT * FROM questions WHERE course_id IN (1,2,3,...);

# Total 3 queries (not 101!) and no cartesian product
```

**Rules:**
- `joinedload`: For one-to-one or small one-to-many
- `selectinload`: For larger one-to-many
- `subqueryload`: For complex filtering

---

## Mistake Category 5: Statistics and Maintenance

### Mistake 5.1: Never Running ANALYZE

**What happens:**
```sql
-- After inserting 50,000 new rows:
INSERT INTO questions SELECT ... FROM generate_series(1, 50000);

-- Statistics still think there are 1,000 rows
-- Query plan is completely wrong:

EXPLAIN SELECT * FROM questions WHERE year = 2023;
-- Shows: (cost=... rows=50 width=200)  ← Thinks only 50 match
-- Actually: 5,000 match!

-- Optimizer chooses Nested Loop Join thinking table is small
-- Actually table is huge now → very slow
```

**How to fix:**
```sql
-- Update statistics after bulk changes
ANALYZE questions;

-- Verify estimates improved:
EXPLAIN SELECT * FROM questions WHERE year = 2023;
-- Shows: (cost=... rows=5000 width=200)  ← Accurate now!

-- Optimizer now chooses Hash Join (correct for large table)
```

**How to avoid:**
- Run ANALYZE after bulk INSERT/UPDATE/DELETE
- Enable autovacuum (default in PostgreSQL)
- Check last_analyze time:
  ```sql
  SELECT schemaname, tablename, last_analyze, last_autoanalyze
  FROM pg_stat_user_tables;
  ```

---

### Mistake 5.2: Running VACUUM FULL on Production

**What happens:**
```sql
-- Developer sees dead tuples, runs:
VACUUM FULL questions;

-- Table is LOCKED for duration!
-- All queries blocked
-- Application down!
-- Users angry!
```

**Why it's bad:**
`VACUUM FULL` requires exclusive lock (blocks reads AND writes)

**How to fix:**
```sql
-- Use regular VACUUM (doesn't lock table)
VACUUM questions;

-- Or VACUUM ANALYZE
VACUUM ANALYZE questions;

-- Regular VACUUM can run concurrently with queries
-- Only use VACUUM FULL during maintenance window
```

**How to avoid:**
- Use `VACUUM` not `VACUUM FULL` in production
- Schedule VACUUM FULL during downtime
- Let autovacuum handle regular maintenance
- Monitor dead tuples:
  ```sql
  SELECT n_dead_tup, n_live_tup
  FROM pg_stat_user_tables
  WHERE tablename = 'questions';
  ```

---

## Mistake Category 6: Measurement and Monitoring

### Mistake 6.1: Testing on Empty Database

**What happens:**
```sql
-- Developer tests on local database with 10 rows
EXPLAIN ANALYZE SELECT * FROM questions WHERE year = 2023;
-- Execution Time: 0.05ms  ← Super fast!

-- Deploy to production (10 million rows)
-- User reports: takes 30 seconds!
-- Index that worked on 10 rows doesn't help with 10M rows
```

**How to fix:**
```sql
-- Test with realistic data volume
-- Generate test data:
INSERT INTO questions
SELECT
    (random() * 100 + 1)::int as course_id,
    (random() * 500 + 1)::int as topic_id,
    'Question ' || i as question_text,
    CASE (random() * 3)::int
        WHEN 0 THEN 'easy'
        WHEN 1 THEN 'medium'
        ELSE 'hard'
    END as difficulty,
    (random() * 90 + 10)::int as marks,
    2000 + (random() * 24)::int as year
FROM generate_series(1, 100000) i;

-- Now test with realistic volume
EXPLAIN ANALYZE SELECT * FROM questions WHERE year = 2023;
```

**How to avoid:**
- Use production-like data volume in testing
- Test with realistic data distribution
- Consider worst-case scenarios
- Load test before deployment

---

### Mistake 6.2: Not Monitoring in Production

**What happens:**
```sql
-- Developer optimizes queries in development
-- Deploys to production
-- Never checks if optimizations actually helped
-- Regressions go unnoticed
```

**How to fix:**
```sql
-- Set up pg_stat_statements
CREATE EXTENSION pg_stat_statements;

-- Monitor slow queries
SELECT
    calls,
    mean_exec_time,
    max_exec_time,
    query
FROM pg_stat_statements
WHERE mean_exec_time > 100  -- > 100ms
ORDER BY mean_exec_time DESC
LIMIT 10;

-- Set up alerts:
-- - Any query > 1000ms
-- - Mean exec time increasing over time
-- - Query call count spike
```

**How to avoid:**
- Enable pg_stat_statements in production
- Set up monitoring dashboard
- Alert on slow query trends
- Regular slow query review

---

## Mistake Category 7: Join Optimization

### Mistake 7.1: Missing Index on Foreign Key

**What happens:**
```sql
-- Tables:
-- courses (50 rows)
-- topics (500 rows)
-- questions (10,000 rows)

-- No index on questions.topic_id!

SELECT * FROM questions q
JOIN topics t ON q.topic_id = t.topic_id
WHERE t.course_id = 1;

-- EXPLAIN shows:
-- Nested Loop  ← Bad! For each topic, scan all questions
--   -> Seq Scan on topics (filter: course_id = 1)
--   -> Seq Scan on questions  ← Scans 10,000 rows per topic!
-- Execution Time: 5000ms
```

**How to fix:**
```sql
-- Index foreign key columns!
CREATE INDEX idx_questions_topic ON questions(topic_id);

-- EXPLAIN now shows:
-- Nested Loop
--   -> Seq Scan on topics (filter: course_id = 1)
--   -> Index Scan using idx_questions_topic on questions
-- Execution Time: 50ms  ← 100x faster!
```

**Rule**: Always index foreign key columns!

---

## Quick Reference: Common Error Patterns

| Symptom | Likely Cause | Solution |
|---------|--------------|----------|
| Seq Scan when index exists | Function on column, low selectivity | Remove function or accept Seq Scan |
| Estimates way off (>10x) | Stale statistics | Run ANALYZE |
| Nested Loop on large tables | Missing foreign key index | CREATE INDEX |
| High "Rows Removed" | Filter too late | Add WHERE earlier or use better index |
| "Loops: 1000" | Nested query executed many times | Rewrite or add index |
| Query slow in production, fast in dev | Data volume difference | Test with realistic data |

---

## Best Practices Summary

1. **Always measure before optimizing** - EXPLAIN ANALYZE first
2. **Test with realistic data** - Volume matters
3. **Trust the optimizer** - Seq Scan sometimes correct
4. **Monitor in production** - Ensure optimizations help
5. **Keep queries readable** - Balance performance and maintainability
6. **Update statistics** - ANALYZE after bulk changes
7. **Index foreign keys** - Always
8. **Watch for N+1** - Enable SQL logging in development

---

**Remember**: The goal is fast enough, not fastest possible. Optimize what matters, maintain readability, and always measure the impact!

**Next steps:**
- Review exercises.md for hands-on practice
- Complete checkpoints.md to verify understanding
- Apply these lessons to CourseDB-AI

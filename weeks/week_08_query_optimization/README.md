# Week 8: Query Optimization & Performance Tuning

## 🎯 Learning Objectives

By the end of this week, you will:
- Master EXPLAIN ANALYZE for query performance analysis
- Understand query execution plans and optimizer behavior
- Optimize slow queries systematically
- Learn join algorithms and when each is used
- Identify and fix common performance bottlenecks
- Apply query optimization to CourseDB-AI
- Balance query performance with code maintainability
- Use PostgreSQL statistics and vacuum for optimal performance

---

## 📋 Week Overview

**Theme**: From analysis to action - systematically transform slow queries into fast ones

**The Journey**:
- Week 7: Created indexes (the tools)
- Week 8: Use indexes effectively (the skill)

**Real-world scenario**: 
Your CourseDB-AI analytics dashboard loads slowly (5 seconds). Users complain. You use EXPLAIN ANALYZE to discover the problem, create appropriate indexes, and reduce load time to 50ms - **100x faster**!

---

## 1. Query Optimization Overview

### What is Query Optimization?

**Query Optimizer**: The "brain" of the database that decides HOW to execute your query.

**Your role**: Write SQL (WHAT you want)
**Optimizer's role**: Determine execution strategy (HOW to get it)

**Example:**
```sql
SELECT * FROM questions WHERE year = 2023 AND difficulty = 'hard';
```

**Possible execution strategies:**
1. Sequential scan → filter year → filter difficulty
2. Use idx_year → fetch rows → filter difficulty
3. Use idx_difficulty → fetch rows → filter year
4. Use idx_year_difficulty → fetch rows directly (best!)

**Optimizer chooses #4** (lowest cost)

### The Query Execution Pipeline

```
┌─────────────┐
│  SQL Query  │
└──────┬──────┘
       │
       v
┌─────────────┐
│   Parser    │ ← Syntax check
└──────┬──────┘
       │
       v
┌─────────────┐
│  Rewriter   │ ← Apply rules (views, etc.)
└──────┬──────┘
       │
       v
┌─────────────┐
│  Optimizer  │ ← Generate plans, choose best
└──────┬──────┘
       │
       v
┌─────────────┐
│  Executor   │ ← Run chosen plan
└──────┬──────┘
       │
       v
┌─────────────┐
│   Results   │
└─────────────┘
```

### Cost-Based Optimization

**How optimizer chooses plan:**

1. **Generate alternative plans**:
   - Sequential scan
   - Index scan on year
   - Index scan on difficulty
   - Index scan on composite index

2. **Estimate cost of each plan**:
   - Seq Scan: 1000 units
   - Index on year: 100 units
   - Index on difficulty: 200 units
   - Composite index: 10 units ← **Winner!**

3. **Choose lowest cost plan**

4. **Execute chosen plan**

**Cost factors:**
- Disk I/O (biggest factor)
- CPU processing
- Memory usage
- Network (for distributed databases)

---

## 2. Understanding EXPLAIN and EXPLAIN ANALYZE

### EXPLAIN: The Execution Plan

**EXPLAIN** shows the plan WITHOUT executing:

```sql
EXPLAIN
SELECT * FROM questions WHERE year = 2023;
```

**Output:**
```
Seq Scan on questions  (cost=0.00..35.50 rows=50 width=200)
  Filter: (year = 2023)
```

**What each field means:**

| Field | Meaning | Example |
|-------|---------|---------|
| Scan type | How data is accessed | Seq Scan, Index Scan |
| cost | Estimated cost (start..total) | 0.00..35.50 |
| rows | Estimated rows returned | 50 |
| width | Average row size (bytes) | 200 |

### EXPLAIN ANALYZE: Actual Execution

**EXPLAIN ANALYZE** executes the query and shows REAL metrics:

```sql
EXPLAIN ANALYZE
SELECT * FROM questions WHERE year = 2023;
```

**Output:**
```
Seq Scan on questions  (cost=0.00..35.50 rows=50 width=200)
                       (actual time=0.015..2.456 rows=48 loops=1)
  Filter: (year = 2023)
  Rows Removed by Filter: 952
Planning Time: 0.123 ms
Execution Time: 2.489 ms
```

**Additional fields:**

| Field | Meaning |
|-------|---------|
| actual time | Real start..end time (ms) |
| rows (actual) | Actual rows returned |
| loops | How many times node executed |
| Rows Removed | Rows filtered out |
| Planning Time | Time to create plan |
| Execution Time | Time to execute query |

### EXPLAIN Options

```sql
-- Basic plan
EXPLAIN SELECT ...;

-- With actual execution
EXPLAIN ANALYZE SELECT ...;

-- Detailed output (buffers, I/O)
EXPLAIN (ANALYZE, BUFFERS) SELECT ...;

-- JSON format (for tools)
EXPLAIN (FORMAT JSON) SELECT ...;

-- All details
EXPLAIN (ANALYZE, BUFFERS, VERBOSE, COSTS, TIMING) SELECT ...;
```

---

## 3. Scan Types and When Each is Used

### 3.1 Sequential Scan (Seq Scan)

**What it is**: Read every row from start to finish

**When used:**
- No index available
- Index not helpful (low selectivity)
- Table is small (< 1000 rows)

**Performance**: O(n) - proportional to table size

**Example:**
```sql
-- No index on difficulty
SELECT * FROM questions WHERE difficulty = 'medium';

-- EXPLAIN shows:
Seq Scan on questions (cost=0.00..180.00 rows=333 width=200)
  Filter: (difficulty = 'medium')
```

**When it's actually fast:**
- Small tables
- Returning large percentage of rows (> 10%)
- Data fits in memory (cached)

### 3.2 Index Scan

**What it is**: Use index to find rows, then fetch from table

**When used:**
- Index exists on WHERE column
- Good selectivity (< 5% of rows)
- Index matches query

**Performance**: O(log n) + k (k = rows fetched)

**Example:**
```sql
CREATE INDEX idx_year ON questions(year);

SELECT * FROM questions WHERE year = 2023;

-- EXPLAIN shows:
Index Scan using idx_year on questions (cost=0.29..10.50 rows=50 width=200)
  Index Cond: (year = 2023)
```

**Two steps:**
1. Search index (log n)
2. Fetch rows from table (k random I/Os)

### 3.3 Index Only Scan

**What it is**: Get all data from index, no table access

**When used:**
- Covering index (index contains all needed columns)
- VACUUM has run recently (visibility map updated)

**Performance**: O(log n) - fastest!

**Example:**
```sql
CREATE INDEX idx_year_marks ON questions(year, marks);

SELECT year, marks FROM questions WHERE year = 2023;

-- EXPLAIN shows:
Index Only Scan using idx_year_marks on questions (cost=0.29..5.50 rows=50 width=8)
  Index Cond: (year = 2023)
  Heap Fetches: 0  ← Perfect!
```

**Key metric**: `Heap Fetches: 0` means no table access!

### 3.4 Bitmap Index Scan

**What it is**: Build bitmap of matching rows, then fetch in one pass

**When used:**
- Multiple index conditions (OR)
- Moderate selectivity
- Better than multiple Index Scans

**Performance**: O(log n) + O(m) where m = matching rows

**Example:**
```sql
SELECT * FROM questions
WHERE year = 2023 OR difficulty = 'hard';

-- EXPLAIN shows:
Bitmap Heap Scan on questions (cost=10.15..45.50 rows=150 width=200)
  Recheck Cond: ((year = 2023) OR (difficulty = 'hard'))
  ->  BitmapOr (cost=10.15..10.15 rows=150 width=0)
        ->  Bitmap Index Scan on idx_year (cost=0.00..5.00 rows=50 width=0)
              Index Cond: (year = 2023)
        ->  Bitmap Index Scan on idx_difficulty (cost=0.00..5.00 rows=100 width=0)
              Index Cond: (difficulty = 'hard')
```

**Why bitmap?** Combines multiple indexes efficiently, fetches rows in physical order (faster I/O)

---

## 4. Join Algorithms

### 4.1 Nested Loop Join

**Algorithm:**
```
for each row in table1:
    for each row in table2:
        if join condition matches:
            return combined row
```

**Cost**: O(n × m) - expensive!

**When used:**
- Small tables
- Good index on inner table
- Few rows in outer table

**Example:**
```sql
SELECT * FROM courses c
JOIN topics t ON c.course_id = t.course_id
WHERE c.course_code = 'CS201';

-- courses: 1 row (after WHERE)
-- topics: indexed on course_id

-- EXPLAIN shows:
Nested Loop (cost=0.29..10.50 rows=5 width=400)
  ->  Seq Scan on courses c (cost=0.00..1.50 rows=1 width=200)
        Filter: (course_code = 'CS201')
  ->  Index Scan using idx_topics_course on topics t (cost=0.29..8.50 rows=5 width=200)
        Index Cond: (course_id = c.course_id)
```

**Good**: Stops early if outer table has few rows
**Bad**: Exponential with table size

### 4.2 Hash Join

**Algorithm:**
```
1. Build hash table on smaller table
2. For each row in larger table:
     - Hash join key
     - Lookup in hash table
     - If match, return combined row
```

**Cost**: O(n + m) - linear!

**When used:**
- Large tables
- Equality joins (=)
- Enough memory for hash table

**Example:**
```sql
SELECT * FROM questions q
JOIN courses c ON q.course_id = c.course_id;

-- Both tables large
-- Equality join on course_id

-- EXPLAIN shows:
Hash Join (cost=15.00..250.00 rows=1000 width=400)
  Hash Cond: (q.course_id = c.course_id)
  ->  Seq Scan on questions q (cost=0.00..180.00 rows=1000 width=200)
  ->  Hash (cost=10.00..10.00 rows=50 width=200)
        ->  Seq Scan on courses c (cost=0.00..10.00 rows=50 width=200)
```

**Good**: Efficient for large tables
**Bad**: Requires memory for hash table

### 4.3 Merge Join

**Algorithm:**
```
1. Sort both tables on join key
2. Merge sorted lists (like merge sort)
```

**Cost**: O(n log n + m log m) + O(n + m)

**When used:**
- Already sorted (indexed columns)
- Non-equality joins (>, <, BETWEEN)
- Very large tables (can't fit in hash)

**Example:**
```sql
SELECT * FROM courses c
JOIN topics t ON c.course_id = t.course_id
ORDER BY c.course_code;

-- Both tables small, already sorted

-- EXPLAIN shows:
Merge Join (cost=5.00..30.00 rows=100 width=400)
  Merge Cond: (c.course_id = t.course_id)
  ->  Index Scan using idx_courses_code on courses c (cost=0.00..10.00 rows=50 width=200)
  ->  Index Scan using idx_topics_course on topics t (cost=0.00..15.00 rows=100 width=200)
```

**Good**: Efficient when pre-sorted, produces sorted output
**Bad**: Sorting overhead if not pre-sorted

### Join Algorithm Selection

| Scenario | Best Join Algorithm |
|----------|-------------------|
| Small × Small | Nested Loop |
| Small × Large (with index) | Nested Loop |
| Large × Large (equality) | Hash Join |
| Large × Large (sorted) | Merge Join |
| Large × Large (non-equality) | Merge Join |

---

## 5. Query Optimization Techniques

### Technique 1: Avoid SELECT *

**Problem**: Fetches unnecessary data

```sql
-- ❌ Bad: Returns all 20 columns (200 bytes per row)
SELECT * FROM questions WHERE year = 2023;
-- 1000 rows × 200 bytes = 200KB transferred

-- ✅ Good: Returns only needed columns (50 bytes per row)
SELECT question_id, question_text, marks
FROM questions WHERE year = 2023;
-- 1000 rows × 50 bytes = 50KB transferred
-- 4x less data!
```

**Benefits:**
- Less disk I/O
- Less network transfer
- Enables covering indexes
- Faster parsing

### Technique 2: Use Indexes Effectively

**Problem**: Index exists but not used

```sql
-- ❌ Bad: Function on column prevents index usage
SELECT * FROM questions WHERE YEAR(created_at) = 2023;
-- Seq Scan (index on created_at not used)

-- ✅ Good: Sargable query (index can be used)
SELECT * FROM questions
WHERE created_at >= '2023-01-01'
  AND created_at < '2024-01-01';
-- Index Scan using idx_created_at
```

**SARGABLE**: Search ARGument ABLE (optimizer can use index)

### Technique 3: Use LIMIT for Pagination

**Problem**: Fetching millions of rows

```sql
-- ❌ Bad: Returns all rows (slow, memory intensive)
SELECT * FROM questions ORDER BY year DESC;
-- Returns 100,000 rows

-- ✅ Good: Pagination with LIMIT
SELECT * FROM questions
ORDER BY year DESC
LIMIT 20 OFFSET 0;
-- Returns 20 rows (5000x less!)
```

**For APIs**: Always use LIMIT

### Technique 4: Optimize Subqueries with EXISTS

**Problem**: IN with large subquery

```sql
-- ❌ Slower: IN materializes entire subquery
SELECT * FROM courses
WHERE course_id IN (
    SELECT course_id FROM questions WHERE year = 2023
);
-- Evaluates subquery fully

-- ✅ Faster: EXISTS short-circuits
SELECT * FROM courses c
WHERE EXISTS (
    SELECT 1 FROM questions q
    WHERE q.course_id = c.course_id AND q.year = 2023
);
-- Stops at first match per course
```

**Rule**: Use EXISTS for large subqueries, IN for small lists

### Technique 5: Avoid N+1 Queries

**Problem**: One query per row (N+1 total)

```python
# ❌ Bad: N+1 queries
courses = db.query(Course).all()  # 1 query
for course in courses:
    topics = db.query(Topic).filter(
        Topic.course_id == course.id
    ).all()  # N queries (1 per course)
# Total: 1 + N queries

# ✅ Good: Single query with JOIN
courses = db.query(Course).options(
    joinedload(Course.topics)
).all()  # 1 query with JOIN
# Total: 1 query!
```

**FastAPI/SQLAlchemy**: Use `joinedload` or `selectinload`

### Technique 6: Use CTEs for Readability (Sometimes)

**Balance**: Readability vs performance

```sql
-- ✅ Readable but may be slower (CTE materialized)
WITH recent_questions AS (
    SELECT * FROM questions WHERE year >= 2020
)
SELECT course_id, COUNT(*)
FROM recent_questions
GROUP BY course_id;

-- ✅ Faster but less readable
SELECT course_id, COUNT(*)
FROM questions
WHERE year >= 2020
GROUP BY course_id;
```

**PostgreSQL 12+**: CTEs are often optimized away (not materialized)

### Technique 7: Batch Operations

**Problem**: Row-by-row operations

```sql
-- ❌ Bad: 1000 individual INSERTs
INSERT INTO questions VALUES (...);  -- x1000

-- ✅ Good: Batch INSERT
INSERT INTO questions VALUES
    (...),
    (...),
    (...);  -- All at once
-- 100x faster!
```

---

## 6. Statistics and Maintenance

### ANALYZE: Update Statistics

**Why**: Optimizer uses statistics to estimate costs

```sql
-- Update statistics for one table
ANALYZE questions;

-- Update statistics for all tables
ANALYZE;
```

**When to run:**
- After bulk INSERT/UPDATE/DELETE
- If EXPLAIN estimates are way off
- After data distribution changes

**Example:**
```sql
-- Bad estimates
EXPLAIN SELECT * FROM questions WHERE year = 2023;
-- Shows: rows=50 (estimate)
-- Actually: 5000 rows!

-- Update statistics
ANALYZE questions;

-- Good estimates now
EXPLAIN SELECT * FROM questions WHERE year = 2023;
-- Shows: rows=5000 (accurate!)
```

### VACUUM: Clean Up Dead Rows

**Why**: UPDATE/DELETE leaves "dead" rows

```sql
-- Manual vacuum
VACUUM questions;

-- Vacuum + update statistics
VACUUM ANALYZE questions;

-- Aggressive vacuum (reclaim more space)
VACUUM FULL questions;  -- Locks table!
```

**When to run:**
- Regular maintenance (weekly/monthly)
- After bulk operations
- When table is bloated

**Autovacuum**: PostgreSQL usually handles this automatically

### Statistics Views

**Check statistics:**
```sql
-- Last analyze time
SELECT schemaname, tablename, last_analyze, last_autoanalyze
FROM pg_stat_user_tables
WHERE tablename = 'questions';

-- Dead tuples (need vacuum)
SELECT n_dead_tup, n_live_tup
FROM pg_stat_user_tables
WHERE tablename = 'questions';
```

---

## 7. Common Performance Bottlenecks

### Bottleneck 1: Missing Index

**Symptom**: Seq Scan on large table

**Fix**:
```sql
-- Identify from EXPLAIN
EXPLAIN ANALYZE SELECT * FROM questions WHERE year = 2023;
-- Shows: Seq Scan on questions (cost=0..1000)

-- Create index
CREATE INDEX idx_questions_year ON questions(year);

-- Verify improvement
EXPLAIN ANALYZE SELECT * FROM questions WHERE year = 2023;
-- Shows: Index Scan using idx_questions_year (cost=0..50)
-- 20x faster!
```

### Bottleneck 2: Poor Join Order

**Symptom**: Large intermediate results

**Fix**: Let optimizer choose, or use explicit JOIN order

```sql
-- Optimizer chooses join order automatically
SELECT * FROM courses c
JOIN topics t ON c.course_id = t.course_id
JOIN questions q ON t.topic_id = q.topic_id
WHERE c.course_code = 'CS201';

-- Filter early: c.course_code = 'CS201' → 1 course → 5 topics → 50 questions
-- Not: all courses → all topics → all questions → filter
```

### Bottleneck 3: Unindexed Foreign Keys

**Symptom**: Slow JOINs

**Fix**: Index foreign key columns

```sql
-- Slow JOIN
SELECT * FROM questions q
JOIN topics t ON q.topic_id = t.topic_id;
-- Nested loop without index on topic_id

-- Create index
CREATE INDEX idx_questions_topic ON questions(topic_id);

-- Fast JOIN now
-- Uses index on topic_id
```

### Bottleneck 4: Large Result Sets

**Symptom**: Running out of memory

**Fix**: Use cursor or streaming

```python
# ❌ Bad: Load all rows into memory
questions = db.query(Question).all()  # 1M rows!

# ✅ Good: Stream with yield_per
for questions_batch in db.query(Question).yield_per(1000):
    process(questions_batch)
```

### Bottleneck 5: Lock Contention

**Symptom**: Queries waiting for locks

**Fix**: Optimize transactions, use appropriate isolation level

```sql
-- Check blocked queries
SELECT pid, wait_event_type, wait_event, query
FROM pg_stat_activity
WHERE wait_event IS NOT NULL;
```

---

## 8. Practical Optimization Workflow

### Step 1: Identify Slow Query

**Methods:**
- Application logs (response times)
- User complaints
- Monitoring tools
- `pg_stat_statements` (PostgreSQL extension)

```sql
-- Enable pg_stat_statements
CREATE EXTENSION pg_stat_statements;

-- Find slowest queries
SELECT
    calls,
    mean_exec_time,
    max_exec_time,
    query
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;
```

### Step 2: Analyze with EXPLAIN ANALYZE

```sql
EXPLAIN (ANALYZE, BUFFERS)
[YOUR SLOW QUERY];
```

**Look for:**
- Seq Scan on large tables → need index
- High actual time → bottleneck
- High "Rows Removed" → inefficient filter
- Many "Buffers" → excessive I/O

### Step 3: Identify Root Cause

**Common causes:**
1. Missing index
2. Wrong index used
3. Poor statistics
4. Inefficient join order
5. Too many rows returned

### Step 4: Apply Fix

**Fixes by cause:**
1. Missing index → CREATE INDEX
2. Wrong index → Fix query or create better index
3. Poor statistics → ANALYZE
4. Inefficient join → Rewrite query
5. Too many rows → Add LIMIT or filters

### Step 5: Verify Improvement

```sql
EXPLAIN ANALYZE [YOUR FIXED QUERY];
```

**Compare metrics:**
- Execution time: Before vs After
- Scan types: Seq Scan → Index Scan
- Rows processed: Higher → Lower
- Cost: Higher → Lower

### Step 6: Monitor in Production

- Deploy change
- Monitor query performance
- Verify no regressions
- Document optimization

---

## 9. CourseDB-AI Optimization Examples

### Example 1: Analytics Dashboard

**Slow query** (5000ms):
```sql
SELECT
    c.course_code,
    COUNT(q.question_id) as question_count,
    AVG(q.marks) as avg_marks
FROM courses c
LEFT JOIN questions q ON c.course_id = q.course_id
WHERE q.year >= 2020
GROUP BY c.course_code
ORDER BY question_count DESC;
```

**EXPLAIN shows:**
- Seq Scan on questions (cost=0..10000)
- Hash Join
- Sort

**Optimizations:**
```sql
-- 1. Index on year
CREATE INDEX idx_questions_year ON questions(year);

-- 2. Index on course_id (for JOIN)
CREATE INDEX idx_questions_course ON questions(course_id);

-- 3. Covering index (best!)
CREATE INDEX idx_questions_analytics
ON questions(course_id, year, marks);
```

**Result**: 5000ms → 50ms (100x faster!)

### Example 2: Question Search

**Slow query** (2000ms):
```sql
SELECT * FROM questions
WHERE year BETWEEN 2020 AND 2023
  AND difficulty = 'hard'
  AND topic_id = 5
ORDER BY year DESC
LIMIT 20;
```

**EXPLAIN shows:**
- Multiple Seq Scans or bitmap scans
- Filter applied late

**Optimization:**
```sql
-- Composite index (query order matters!)
CREATE INDEX idx_questions_search
ON questions(topic_id, year, difficulty);
-- Ordered by selectivity: topic_id (most selective) first
```

**Result**: 2000ms → 20ms (100x faster!)

### Example 3: N+1 Query Problem

**Slow code** (5000ms for 100 courses):
```python
# ❌ 1 + 100 queries
courses = db.query(Course).all()  # 1 query
for course in courses:  # 100 iterations
    topics = db.query(Topic).filter(
        Topic.course_id == course.id
    ).all()  # 100 queries!
```

**Optimization:**
```python
# ✅ 1 query with JOIN
courses = db.query(Course).options(
    joinedload(Course.topics)
).all()
```

**Result**: 5000ms → 50ms (100x faster!)

---

## Summary

**Key Takeaways:**

1. **EXPLAIN ANALYZE is your best friend** - Use it for every slow query
2. **Index strategically** - Not every column needs an index
3. **Trust the optimizer** - But verify with EXPLAIN
4. **Measure everything** - Before/after metrics prove value
5. **Balance readability and performance** - Sometimes slower query is clearer
6. **Keep statistics updated** - ANALYZE after bulk changes
7. **Watch for N+1 queries** - Use joins or eager loading
8. **Start simple** - Add complexity only when needed

**Week 8 gives you:**
- Skills to analyze any slow query
- Tools to optimize systematically
- Understanding of database internals
- Confidence to tune production systems

**Next steps:**
- Complete exercises.md (hands-on optimization)
- Follow implementation_plan.md (7-day practice)
- Review mistakes_to_expect.md (avoid pitfalls)
- Track progress with checkpoints.md

---

**Ready to make your queries fly? Let's optimize! 🚀**

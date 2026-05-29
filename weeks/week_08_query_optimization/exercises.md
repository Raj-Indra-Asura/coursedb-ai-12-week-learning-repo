# Week 8: Query Optimization & Performance Tuning - Exercises

## 🎯 Exercise Overview

This week focuses on **systematically analyzing and optimizing slow queries**. You'll:
- Use EXPLAIN ANALYZE to diagnose performance problems
- Identify bottlenecks and apply appropriate fixes
- Measure performance improvements
- Optimize real CourseDB-AI queries
- Learn through experimentation and data

**Time estimate**: 6-8 hours total

---

## Exercise Set 1: EXPLAIN Mastery

### Exercise 1.1: Reading EXPLAIN Output (45 minutes)

**Goal**: Become fluent in reading and interpreting EXPLAIN output

**Step 1: Basic EXPLAIN**

```sql
-- Connect to database
psql -U coursedb_user -d coursedb_dev

-- Run EXPLAIN (no execution)
EXPLAIN
SELECT * FROM questions WHERE year = 2023;
```

**Record the output and answer:**
1. What is the scan type? _____
2. What is the estimated cost? _____
3. How many rows are estimated? _____
4. What is the average row width? _____

**Step 2: EXPLAIN ANALYZE**

```sql
-- Run with actual execution
EXPLAIN ANALYZE
SELECT * FROM questions WHERE year = 2023;
```

**Record and compare:**
| Metric | Estimated | Actual |
|--------|-----------|--------|
| Rows | _____ | _____ |
| Start time | _____ | _____ |
| Total time | _____ | _____ |

**Step 3: Compare estimates**

```sql
-- If estimates are very different from actuals, update statistics
ANALYZE questions;

-- Run EXPLAIN ANALYZE again
EXPLAIN ANALYZE
SELECT * FROM questions WHERE year = 2023;
```

**Questions to answer:**
1. Why might estimates differ from actuals? _____
2. When should you run ANALYZE? _____
3. What's the difference between "cost" and "actual time"? _____

---

### Exercise 1.2: Scan Type Recognition (30 minutes)

**Goal**: Identify different scan types and understand when each is used

**Test Case 1: Sequential Scan**

```sql
-- Drop all indexes on questions temporarily
DROP INDEX IF EXISTS idx_questions_year;
DROP INDEX IF EXISTS idx_questions_difficulty;

-- Query without index
EXPLAIN ANALYZE
SELECT * FROM questions WHERE year = 2023;

-- Record:
-- Scan type: _____
-- Execution time: _____ ms
```

**Test Case 2: Index Scan**

```sql
-- Create index
CREATE INDEX idx_questions_year ON questions(year);

-- Same query with index
EXPLAIN ANALYZE
SELECT * FROM questions WHERE year = 2023;

-- Record:
-- Scan type: _____
-- Execution time: _____ ms
-- Speedup: _____x
```

**Test Case 3: Index Only Scan**

```sql
-- Create covering index
CREATE INDEX idx_questions_year_marks ON questions(year, marks);

-- Query only indexed columns
EXPLAIN ANALYZE
SELECT year, marks FROM questions WHERE year = 2023;

-- Record:
-- Scan type: _____
-- Heap Fetches: _____
-- Execution time: _____ ms
```

**Test Case 4: Bitmap Scan**

```sql
-- Create second index
CREATE INDEX idx_questions_difficulty ON questions(difficulty);

-- Query with OR
EXPLAIN ANALYZE
SELECT * FROM questions
WHERE year = 2023 OR difficulty = 'hard';

-- Record:
-- Scan type: _____
-- How many indexes used: _____
-- Execution time: _____ ms
```

**Summary table:**

| Scan Type | When Used | Speed |
|-----------|-----------|-------|
| Seq Scan | _____ | _____ |
| Index Scan | _____ | _____ |
| Index Only Scan | _____ | _____ |
| Bitmap Scan | _____ | _____ |

---

### Exercise 1.3: Cost Estimation Analysis (30 minutes)

**Goal**: Understand how cost estimates guide optimizer decisions

```sql
-- Disable seq scan to force index usage
SET enable_seqscan = OFF;

EXPLAIN ANALYZE
SELECT * FROM questions WHERE difficulty = 'medium';

-- Record forced index scan cost: _____

-- Re-enable seq scan
SET enable_seqscan = ON;

EXPLAIN ANALYZE
SELECT * FROM questions WHERE difficulty = 'medium';

-- Record chosen scan cost: _____
```

**Questions:**
1. Which scan did optimizer choose when allowed? _____
2. Why did it choose that scan? _____
3. Is the chosen plan actually faster? (Check execution time) _____

**Key insight**: Sometimes Seq Scan is faster (low selectivity)!

---

## Exercise Set 2: Join Optimization

### Exercise 2.1: Join Algorithm Comparison (60 minutes)

**Goal**: Understand different join algorithms and when each is used

**Setup: Create test tables**

```sql
-- Small table (50 rows)
CREATE TABLE small_table AS
SELECT id, 'Small ' || id as name
FROM generate_series(1, 50) as id;

-- Medium table (1000 rows)
CREATE TABLE medium_table AS
SELECT id, 'Medium ' || id as name
FROM generate_series(1, 1000) as id;

-- Large table (10000 rows)
CREATE TABLE large_table AS
SELECT id, 'Large ' || id as name
FROM generate_series(1, 10000) as id;

-- Create indexes
CREATE INDEX idx_medium_id ON medium_table(id);
CREATE INDEX idx_large_id ON large_table(id);
```

**Test Case 1: Nested Loop Join**

```sql
-- Small × Small
EXPLAIN ANALYZE
SELECT * FROM small_table s1
JOIN small_table s2 ON s1.id = s2.id;

-- Record:
-- Join algorithm: _____
-- Execution time: _____ ms
```

**Test Case 2: Hash Join**

```sql
-- Large × Large with equality
EXPLAIN ANALYZE
SELECT * FROM large_table l1
JOIN large_table l2 ON l1.id = l2.id;

-- Record:
-- Join algorithm: _____
-- Execution time: _____ ms
```

**Test Case 3: Merge Join**

```sql
-- Pre-sorted tables
EXPLAIN ANALYZE
SELECT * FROM small_table s
JOIN medium_table m ON s.id = m.id
ORDER BY s.id;

-- Record:
-- Join algorithm: _____
-- Execution time: _____ ms
```

**Cleanup:**
```sql
DROP TABLE small_table, medium_table, large_table;
```

**Summary:**

| Join Type | Best For | Example |
|-----------|----------|---------|
| Nested Loop | _____ | _____ |
| Hash Join | _____ | _____ |
| Merge Join | _____ | _____ |

---

### Exercise 2.2: Optimizing JOIN Order (45 minutes)

**Goal**: Understand how join order affects performance

**Scenario**: Dashboard showing courses → topics → questions

```sql
-- Unoptimized query
EXPLAIN ANALYZE
SELECT c.course_code, COUNT(q.question_id)
FROM courses c
JOIN topics t ON c.course_id = t.course_id
JOIN questions q ON t.topic_id = q.topic_id
GROUP BY c.course_code;

-- Record execution time: _____ ms
```

**Now add WHERE to filter early:**

```sql
-- Optimized with early filtering
EXPLAIN ANALYZE
SELECT c.course_code, COUNT(q.question_id)
FROM courses c
JOIN topics t ON c.course_id = t.course_id
JOIN questions q ON t.topic_id = q.topic_id
WHERE c.course_code = 'CS201'  -- Filter early!
GROUP BY c.course_code;

-- Record execution time: _____ ms
-- Speedup: _____x
```

**Key insight**: Filter as early as possible to reduce intermediate results!

---

### Exercise 2.3: Index Usage in JOINs (30 minutes)

**Goal**: Verify indexes speed up JOIN operations

**Test without indexes:**

```sql
-- Drop foreign key indexes
DROP INDEX IF EXISTS idx_questions_course;
DROP INDEX IF EXISTS idx_questions_topic;

-- JOIN without indexes
EXPLAIN ANALYZE
SELECT c.course_code, COUNT(q.question_id)
FROM courses c
LEFT JOIN questions q ON c.course_id = q.course_id
GROUP BY c.course_code;

-- Record execution time: _____ ms
-- Join algorithm: _____
```

**Test with indexes:**

```sql
-- Create indexes on foreign keys
CREATE INDEX idx_questions_course ON questions(course_id);
CREATE INDEX idx_questions_topic ON questions(topic_id);

-- Same JOIN with indexes
EXPLAIN ANALYZE
SELECT c.course_code, COUNT(q.question_id)
FROM courses c
LEFT JOIN questions q ON c.course_id = q.course_id
GROUP BY c.course_code;

-- Record execution time: _____ ms
-- Join algorithm: _____
-- Speedup: _____x
```

**Rule**: Always index foreign key columns!

---

## Exercise Set 3: Query Rewriting for Performance

### Exercise 3.1: SELECT * vs Specific Columns (20 minutes)

**Goal**: Measure impact of selecting only needed columns

**Test Case 1: SELECT ***

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM questions WHERE year = 2023;

-- Record:
-- Buffers read: _____ (disk pages)
-- Data transferred: _____ bytes (rows × width)
-- Execution time: _____ ms
```

**Test Case 2: Specific columns**

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT question_id, question_text, marks
FROM questions WHERE year = 2023;

-- Record:
-- Buffers read: _____
-- Data transferred: _____
-- Execution time: _____ ms
-- Data reduction: _____x
```

**Key benefit**: Smaller data = less I/O = faster query

---

### Exercise 3.2: Avoiding Functions on Indexed Columns (30 minutes)

**Goal**: Learn to write SARGABLE queries

**Bad query (not SARGABLE):**

```sql
-- Function prevents index usage
EXPLAIN ANALYZE
SELECT * FROM questions
WHERE EXTRACT(YEAR FROM created_at) = 2023;

-- Record:
-- Scan type: _____ (likely Seq Scan)
-- Execution time: _____ ms
```

**Good query (SARGABLE):**

```sql
-- Index can be used
EXPLAIN ANALYZE
SELECT * FROM questions
WHERE created_at >= '2023-01-01'
  AND created_at < '2024-01-01';

-- Record:
-- Scan type: _____ (likely Index Scan)
-- Execution time: _____ ms
-- Speedup: _____x
```

**Other examples to test:**

```sql
-- Bad: LOWER() on indexed column
SELECT * FROM questions WHERE LOWER(difficulty) = 'hard';

-- Good: Store normalized or create expression index
CREATE INDEX idx_difficulty_lower ON questions(LOWER(difficulty));
SELECT * FROM questions WHERE LOWER(difficulty) = 'hard';
```

---

### Exercise 3.3: EXISTS vs IN Performance (45 minutes)

**Goal**: Compare EXISTS and IN for subqueries

**Setup:**

```sql
-- Ensure indexes exist
CREATE INDEX IF NOT EXISTS idx_questions_year ON questions(year);
CREATE INDEX IF NOT EXISTS idx_questions_course ON questions(course_id);
```

**Test Case 1: Using IN**

```sql
EXPLAIN ANALYZE
SELECT * FROM courses
WHERE course_id IN (
    SELECT course_id FROM questions WHERE year = 2023
);

-- Record:
-- Execution time: _____ ms
-- Subquery execution: _____
```

**Test Case 2: Using EXISTS**

```sql
EXPLAIN ANALYZE
SELECT * FROM courses c
WHERE EXISTS (
    SELECT 1 FROM questions q
    WHERE q.course_id = c.course_id AND q.year = 2023
);

-- Record:
-- Execution time: _____ ms
-- Short-circuit behavior: _____
```

**Test Case 3: Using JOIN**

```sql
EXPLAIN ANALYZE
SELECT DISTINCT c.*
FROM courses c
JOIN questions q ON c.course_id = q.course_id
WHERE q.year = 2023;

-- Record:
-- Execution time: _____ ms
```

**Comparison:**

| Method | Time | Best For |
|--------|------|----------|
| IN | _____ ms | Small subquery results |
| EXISTS | _____ ms | Large tables, early termination |
| JOIN | _____ ms | Need subquery columns |

---

### Exercise 3.4: LIMIT for Pagination (20 minutes)

**Goal**: Understand LIMIT optimization

**Without LIMIT (bad):**

```sql
EXPLAIN ANALYZE
SELECT * FROM questions
ORDER BY year DESC, question_id;

-- Returns ALL rows
-- Execution time: _____ ms
```

**With LIMIT (good):**

```sql
EXPLAIN ANALYZE
SELECT * FROM questions
ORDER BY year DESC, question_id
LIMIT 20;

-- Returns only 20 rows
-- Execution time: _____ ms
-- Speedup: _____x
```

**With LIMIT + index (best):**

```sql
CREATE INDEX idx_questions_order ON questions(year DESC, question_id);

EXPLAIN ANALYZE
SELECT * FROM questions
ORDER BY year DESC, question_id
LIMIT 20;

-- Uses index to avoid full sort
-- Execution time: _____ ms
```

---

## Exercise Set 4: Real-World Optimization

### Exercise 4.1: Optimize Analytics Dashboard Query (90 minutes)

**Goal**: End-to-end optimization of a realistic slow query

**The slow query:**

```sql
-- Dashboard showing course statistics
SELECT
    c.course_code,
    c.title,
    COUNT(q.question_id) as question_count,
    COUNT(DISTINCT t.topic_id) as topic_count,
    AVG(q.marks) as avg_marks,
    COUNT(CASE WHEN q.difficulty = 'easy' THEN 1 END) as easy_count,
    COUNT(CASE WHEN q.difficulty = 'medium' THEN 1 END) as medium_count,
    COUNT(CASE WHEN q.difficulty = 'hard' THEN 1 END) as hard_count,
    MIN(q.year) as earliest_year,
    MAX(q.year) as latest_year
FROM courses c
LEFT JOIN topics t ON c.course_id = t.course_id
LEFT JOIN questions q ON t.topic_id = q.topic_id
GROUP BY c.course_id, c.course_code, c.title
ORDER BY question_count DESC;
```

**Step 1: Baseline measurement**

```sql
EXPLAIN (ANALYZE, BUFFERS)
[query above];

-- Record:
-- Execution time: _____ ms
-- Scan types: _____
-- Buffers: _____
-- Bottlenecks identified: _____
```

**Step 2: Identify optimization opportunities**

Look for:
- [ ] Seq Scans on large tables
- [ ] Missing indexes on join columns
- [ ] High buffer usage
- [ ] Expensive sorts

**Step 3: Apply optimizations**

```sql
-- Example optimizations:
CREATE INDEX idx_topics_course ON topics(course_id);
CREATE INDEX idx_questions_topic ON questions(topic_id);
CREATE INDEX idx_questions_analytics ON questions(topic_id, year, difficulty, marks);
```

**Step 4: Remeasure**

```sql
EXPLAIN (ANALYZE, BUFFERS)
[query above];

-- Record:
-- Execution time: _____ ms
-- Improvement: _____x faster
```

**Step 5: Document your work**

```
Original time: _____ ms
Optimized time: _____ ms
Speedup: _____x

Indexes created:
1. _____
2. _____
3. _____

Rationale:
_____
```

---

### Exercise 4.2: Optimize Question Search (60 minutes)

**Goal**: Optimize a complex search query with multiple filters

**The slow query:**

```sql
SELECT
    q.question_id,
    q.question_text,
    q.year,
    q.difficulty,
    q.marks,
    t.topic_name,
    c.course_code
FROM questions q
JOIN topics t ON q.topic_id = t.topic_id
JOIN courses c ON t.course_id = c.course_id
WHERE q.year BETWEEN 2020 AND 2023
  AND q.difficulty = 'hard'
  AND c.course_code = 'CS201'
ORDER BY q.year DESC, q.marks DESC
LIMIT 50;
```

**Your task:**

1. **Measure baseline** with EXPLAIN ANALYZE
2. **Identify bottlenecks** (what's slow?)
3. **Create appropriate indexes**
4. **Verify improvement**
5. **Calculate speedup**

**Deliverable:**

```
Baseline: _____ ms

Bottlenecks:
1. _____
2. _____

Indexes created:
1. CREATE INDEX _____ ON _____(_____);
   Rationale: _____

2. CREATE INDEX _____ ON _____(_____);
   Rationale: _____

Optimized: _____ ms
Speedup: _____x
```

---

### Exercise 4.3: Fix N+1 Query Problem (45 minutes)

**Goal**: Eliminate N+1 queries in application code

**The N+1 problem (Python/FastAPI):**

```python
# Slow code
def get_courses_with_topics():
    courses = db.query(Course).all()  # 1 query
    result = []
    for course in courses:  # N iterations
        topics = db.query(Topic).filter(
            Topic.course_id == course.id
        ).all()  # N queries!
        
        result.append({
            "course": course,
            "topics": topics
        })
    return result

# Total queries: 1 + N
```

**Your task: Rewrite to use 1 query**

```python
# Optimized code
def get_courses_with_topics():
    # Your code here
    # Use joinedload or selectinload
    courses = db.query(Course).options(
        # TODO: Add eager loading
    ).all()
    
    # Total queries: 1
```

**Test with SQL logging enabled:**

```python
# Enable SQL echo
engine = create_engine(DATABASE_URL, echo=True)

# Run both versions, count queries
# N+1 version: _____ queries
# Optimized version: _____ queries
```

---

## Exercise Set 5: Statistics and Maintenance

### Exercise 5.1: Statistics Impact (30 minutes)

**Goal**: See how statistics affect query plans

**Step 1: Outdated statistics**

```sql
-- Insert lots of new data
INSERT INTO questions (course_id, topic_id, question_text, difficulty, marks, year)
SELECT
    (random() * 10 + 1)::int,
    (random() * 50 + 1)::int,
    'Generated question ' || i,
    CASE (random() * 3)::int
        WHEN 0 THEN 'easy'
        WHEN 1 THEN 'medium'
        ELSE 'hard'
    END,
    (random() * 90 + 10)::int,
    2020 + (random() * 4)::int
FROM generate_series(1, 5000) i;

-- Query with outdated statistics
EXPLAIN ANALYZE
SELECT * FROM questions WHERE year = 2023;

-- Record:
-- Estimated rows: _____
-- Actual rows: _____
-- Difference: _____x
```

**Step 2: Updated statistics**

```sql
-- Update statistics
ANALYZE questions;

-- Same query with updated statistics
EXPLAIN ANALYZE
SELECT * FROM questions WHERE year = 2023;

-- Record:
-- Estimated rows: _____
-- Actual rows: _____
-- Accuracy improved: Yes / No
```

**Key insight**: Accurate statistics = better query plans!

---

### Exercise 5.2: VACUUM Impact (20 minutes)

**Goal**: Understand when VACUUM helps

```sql
-- Check dead tuples
SELECT n_live_tup, n_dead_tup
FROM pg_stat_user_tables
WHERE tablename = 'questions';

-- If many dead tuples, VACUUM
VACUUM ANALYZE questions;

-- Check again
SELECT n_live_tup, n_dead_tup
FROM pg_stat_user_tables
WHERE tablename = 'questions';

-- Dead tuples removed: _____
```

---

## Challenge Exercises

### Challenge 1: Complete CourseDB-AI Optimization (120 minutes)

**Goal**: Optimize all major queries in CourseDB-AI

**Your task:**

1. **Identify all slow endpoints** (> 100ms)
2. **Profile each query** with EXPLAIN ANALYZE
3. **Create optimization plan**
4. **Implement indexes and rewrites**
5. **Verify improvements**
6. **Document everything**

**Deliverable**: optimization_report.md with:
- List of optimized queries
- Before/after metrics
- Indexes created
- Overall improvement

---

### Challenge 2: Query Optimization Competition (90 minutes)

**Goal**: Optimize this monster query as fast as possible

```sql
-- Ultra-complex analytics query
SELECT
    c.course_code,
    t.topic_name,
    q.year,
    q.difficulty,
    COUNT(*) as question_count,
    AVG(q.marks) as avg_marks,
    MIN(q.marks) as min_marks,
    MAX(q.marks) as max_marks,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY q.marks) as median_marks
FROM courses c
JOIN topics t ON c.course_id = t.course_id
JOIN questions q ON t.topic_id = q.topic_id
WHERE q.year >= 2020
  AND q.difficulty IN ('medium', 'hard')
GROUP BY c.course_code, t.topic_name, q.year, q.difficulty
HAVING COUNT(*) >= 5
ORDER BY question_count DESC, avg_marks DESC
LIMIT 100;
```

**Your challenge:**
- Get execution time as low as possible
- Use any optimization techniques learned
- Document your approach

**Winner**: Lowest execution time!

---

## Summary Checklist

After completing these exercises, you should be able to:

- [ ] Read and interpret EXPLAIN output fluently
- [ ] Identify different scan types and when each is used
- [ ] Understand join algorithms and their trade-offs
- [ ] Rewrite queries for better performance
- [ ] Avoid common anti-patterns (N+1, SELECT *, functions on indexes)
- [ ] Create appropriate indexes for specific queries
- [ ] Use ANALYZE to update statistics
- [ ] Measure and verify performance improvements
- [ ] Optimize real-world queries systematically

**Next steps:**
- Complete implementation_plan.md for 7-day practice
- Review mistakes_to_expect.md for common pitfalls
- Track progress with checkpoints.md

**Excellent work! You now have the skills to optimize any database query! ⚡🚀**

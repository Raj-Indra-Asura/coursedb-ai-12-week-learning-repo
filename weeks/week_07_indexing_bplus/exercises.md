# Week 7: Indexing & B+ Trees - Exercises

## 🎯 Exercise Overview

This week focuses on **hands-on index creation and performance analysis**. You'll:
- Create indexes and measure performance improvements
- Use EXPLAIN ANALYZE to understand query execution
- Experiment with different index types
- Optimize real CourseDB-AI queries
- Learn through experimentation and measurement

**Time estimate**: 6-8 hours total

---

## Exercise Set 1: Index Basics and Performance Measurement

### Exercise 1.1: Your First Index (30 minutes)

**Goal**: Create an index and measure the performance improvement

**Scenario**: You need to frequently search questions by year

**Step 1: Setup and baseline measurement**

```sql
-- Connect to your database
psql -U coursedb_user -d coursedb_dev

-- Check current data size
SELECT COUNT(*) FROM questions;

-- Measure query without index
EXPLAIN ANALYZE
SELECT * FROM questions WHERE year = 2023;

-- Record the output:
-- Execution Time: _____ ms
-- Scan type: _____
```

**Expected output (without index):**
```
Seq Scan on questions  (cost=0.00..25.00 rows=5 width=500)
  Filter: (year = 2023)
Planning Time: 0.123 ms
Execution Time: 2.456 ms
```

**Step 2: Create index**

```sql
-- Create index on year column
CREATE INDEX idx_questions_year_test ON questions(year);

-- Verify index was created
\d questions

-- Should see:
-- Indexes:
--     "idx_questions_year_test" btree (year)
```

**Step 3: Measure with index**

```sql
-- Same query, now with index
EXPLAIN ANALYZE
SELECT * FROM questions WHERE year = 2023;

-- Record the output:
-- Execution Time: _____ ms
-- Scan type: _____
```

**Expected output (with index):**
```
Index Scan using idx_questions_year_test on questions
  (cost=0.14..8.16 rows=5 width=500)
  Index Cond: (year = 2023)
Planning Time: 0.234 ms
Execution Time: 0.123 ms
```

**Step 4: Calculate speedup**

```
Speedup = Time_without_index / Time_with_index
Speedup = 2.456ms / 0.123ms = 20x faster!
```

**Questions to answer:**
1. What was your execution time without index? _____ms
2. What was your execution time with index? _____ms
3. What was the speedup factor? _____x
4. What changed in the EXPLAIN output? (Seq Scan → Index Scan)

**Step 5: Cleanup**

```sql
-- Drop the test index (we'll create better ones later)
DROP INDEX idx_questions_year_test;
```

---

### Exercise 1.2: Index Size and Storage (20 minutes)

**Goal**: Understand how much space indexes consume

**Step 1: Check table size**

```sql
-- Table size
SELECT
    pg_size_pretty(pg_total_relation_size('questions')) as total_size,
    pg_size_pretty(pg_relation_size('questions')) as table_size,
    pg_size_pretty(pg_total_relation_size('questions') - pg_relation_size('questions')) as indexes_size;
```

**Expected output:**
```
 total_size | table_size | indexes_size
------------+------------+--------------
 120 kB     | 48 kB      | 72 kB
```

**Step 2: Create index and remeasure**

```sql
-- Create index
CREATE INDEX idx_test ON questions(year, difficulty, marks);

-- Remeasure sizes
SELECT
    pg_size_pretty(pg_total_relation_size('questions')) as total_size,
    pg_size_pretty(pg_relation_size('questions')) as table_size,
    pg_size_pretty(pg_total_relation_size('questions') - pg_relation_size('questions')) as indexes_size;
```

**Step 3: View individual index sizes**

```sql
SELECT
    indexname,
    pg_size_pretty(pg_relation_size(indexrelid)) AS index_size
FROM pg_stat_user_indexes
WHERE tablename = 'questions'
ORDER BY pg_relation_size(indexrelid) DESC;
```

**Expected output:**
```
        indexname         | index_size
--------------------------+------------
 questions_pkey           | 16 kB
 idx_test                 | 24 kB
 idx_questions_course     | 16 kB
```

**Questions to answer:**
1. How much space do indexes take compared to table data? _____
2. Which index is largest? Why? _____
3. Is the storage overhead acceptable? (Usually yes for performance gain)

**Cleanup:**
```sql
DROP INDEX idx_test;
```

---

### Exercise 1.3: Comparing Scan Types (30 minutes)

**Goal**: Understand when PostgreSQL uses different scan types

**Step 1: Sequential scan (no index, or low selectivity)**

```sql
-- Query returning many rows (poor selectivity)
EXPLAIN ANALYZE
SELECT * FROM questions WHERE marks >= 5;

-- Expected: Seq Scan (because many rows match)
```

**Step 2: Index scan (index exists, good selectivity)**

```sql
CREATE INDEX idx_questions_year ON questions(year);

-- Query returning few rows (good selectivity)
EXPLAIN ANALYZE
SELECT * FROM questions WHERE year = 2020;

-- Expected: Index Scan
```

**Step 3: Index Only Scan (covering index)**

```sql
CREATE INDEX idx_questions_covering ON questions(year, difficulty, marks);

-- Query only accessing indexed columns
EXPLAIN ANALYZE
SELECT year, difficulty, marks
FROM questions
WHERE year = 2023;

-- Expected: Index Only Scan
-- Heap Fetches: 0 (perfect!)
```

**Step 4: Bitmap Index Scan (multiple index conditions)**

```sql
CREATE INDEX idx_difficulty ON questions(difficulty);

-- Query with OR condition
EXPLAIN ANALYZE
SELECT * FROM questions
WHERE year = 2023 OR difficulty = 'hard';

-- Expected: Bitmap Heap Scan + Bitmap Index Scan
```

**Summary table to fill:**

| Query | Scan Type | Execution Time |
|-------|-----------|----------------|
| marks >= 5 | _____ | _____ ms |
| year = 2020 | _____ | _____ ms |
| year = 2023 (covering) | _____ | _____ ms |
| year = 2023 OR difficulty = 'hard' | _____ | _____ ms |

**Cleanup:**
```sql
DROP INDEX idx_questions_year;
DROP INDEX idx_questions_covering;
DROP INDEX idx_difficulty;
```

---

## Exercise Set 2: Composite Indexes and Leftmost Prefix

### Exercise 2.1: Understanding Leftmost Prefix (45 minutes)

**Goal**: Master the leftmost prefix rule for composite indexes

**Step 1: Create composite index**

```sql
CREATE INDEX idx_year_diff_marks ON questions(year, difficulty, marks);
```

**Step 2: Test different query patterns**

```sql
-- Test 1: Uses all columns (full index)
EXPLAIN ANALYZE
SELECT * FROM questions
WHERE year = 2023 AND difficulty = 'hard' AND marks = 10;

-- Expected: Index Scan using idx_year_diff_marks
-- Note the execution time: _____ ms

-- Test 2: Uses first two columns (partial index)
EXPLAIN ANALYZE
SELECT * FROM questions
WHERE year = 2023 AND difficulty = 'hard';

-- Expected: Index Scan using idx_year_diff_marks
-- Note the execution time: _____ ms

-- Test 3: Uses first column only
EXPLAIN ANALYZE
SELECT * FROM questions
WHERE year = 2023;

-- Expected: Index Scan using idx_year_diff_marks
-- Note the execution time: _____ ms

-- Test 4: Skips first column (CANNOT use index)
EXPLAIN ANALYZE
SELECT * FROM questions
WHERE difficulty = 'hard';

-- Expected: Seq Scan (index not used!)
-- Note the execution time: _____ ms

-- Test 5: Skips middle column (uses first column only)
EXPLAIN ANALYZE
SELECT * FROM questions
WHERE year = 2023 AND marks = 10;

-- Expected: Index Scan using idx_year_diff_marks
-- But only 'year' condition used by index
-- 'marks' condition applied as filter

-- Test 6: Out-of-order columns (ORDER DOESN'T MATTER in WHERE!)
EXPLAIN ANALYZE
SELECT * FROM questions
WHERE difficulty = 'hard' AND year = 2023;

-- Expected: Index Scan (PostgreSQL reorders conditions)
```

**Summary: Which queries use the index?**

| Query Columns | Uses Index? | Index Columns Used |
|---------------|-------------|-------------------|
| year, difficulty, marks | ✅ Yes | All 3 |
| year, difficulty | ✅ Yes | First 2 |
| year | ✅ Yes | First 1 |
| difficulty | ❌ No | None (skips leftmost) |
| year, marks | ✅ Yes | year only (skips middle) |
| difficulty, year | ✅ Yes | All (order in WHERE doesn't matter) |

**Key insight**: Index can be used if leftmost column(s) appear in WHERE clause. Order of columns in WHERE doesn't matter.

**Cleanup:**
```sql
DROP INDEX idx_year_diff_marks;
```

---

### Exercise 2.2: Choosing Index Column Order (30 minutes)

**Goal**: Learn to order composite index columns for maximum efficiency

**Scenario**: You have these common queries:
- `WHERE year = 2023` (80% of queries)
- `WHERE year = 2023 AND difficulty = 'hard'` (15% of queries)
- `WHERE difficulty = 'hard'` (5% of queries)

**Question**: Should you create `idx(year, difficulty)` or `idx(difficulty, year)`?

**Step 1: Option A - Index on (year, difficulty)**

```sql
CREATE INDEX idx_year_difficulty ON questions(year, difficulty);

-- Test query 1 (80% of queries)
EXPLAIN ANALYZE
SELECT * FROM questions WHERE year = 2023;
-- Record time: _____ ms

-- Test query 2 (15% of queries)
EXPLAIN ANALYZE
SELECT * FROM questions WHERE year = 2023 AND difficulty = 'hard';
-- Record time: _____ ms

-- Test query 3 (5% of queries)
EXPLAIN ANALYZE
SELECT * FROM questions WHERE difficulty = 'hard';
-- Record time: _____ ms

DROP INDEX idx_year_difficulty;
```

**Step 2: Option B - Index on (difficulty, year)**

```sql
CREATE INDEX idx_difficulty_year ON questions(difficulty, year);

-- Test query 1 (80% of queries)
EXPLAIN ANALYZE
SELECT * FROM questions WHERE year = 2023;
-- Record time: _____ ms

-- Test query 2 (15% of queries)
EXPLAIN ANALYZE
SELECT * FROM questions WHERE year = 2023 AND difficulty = 'hard';
-- Record time: _____ ms

-- Test query 3 (5% of queries)
EXPLAIN ANALYZE
SELECT * FROM questions WHERE difficulty = 'hard';
-- Record time: _____ ms

DROP INDEX idx_difficulty_year;
```

**Step 3: Compare results**

| Index Order | Query 1 Time | Query 2 Time | Query 3 Time | Overall Score |
|-------------|--------------|--------------|--------------|---------------|
| (year, difficulty) | _____ | _____ | _____ | (Q1×80% + Q2×15% + Q3×5%) |
| (difficulty, year) | _____ | _____ | _____ | (Q1×80% + Q2×15% + Q3×5%) |

**Winner**: _____ because _____

**General rule**: Put most selective columns first, OR columns used in most queries first.

---

### Exercise 2.3: Multiple Indexes vs Composite Index (30 minutes)

**Goal**: Understand when to use multiple single-column indexes vs one composite index

**Option A: Two separate indexes**

```sql
CREATE INDEX idx_year ON questions(year);
CREATE INDEX idx_difficulty ON questions(difficulty);

-- Test combined query
EXPLAIN ANALYZE
SELECT * FROM questions
WHERE year = 2023 AND difficulty = 'hard';

-- Record:
-- Scan type: _____
-- Execution time: _____ ms

-- View index usage
SELECT indexname, idx_scan
FROM pg_stat_user_indexes
WHERE tablename = 'questions';

DROP INDEX idx_year;
DROP INDEX idx_difficulty;
```

**Option B: One composite index**

```sql
CREATE INDEX idx_year_difficulty ON questions(year, difficulty);

-- Test combined query
EXPLAIN ANALYZE
SELECT * FROM questions
WHERE year = 2023 AND difficulty = 'hard';

-- Record:
-- Scan type: _____
-- Execution time: _____ ms

DROP INDEX idx_year_difficulty;
```

**Comparison:**

| Approach | Index Size | Combined Query Time | Individual Query Support |
|----------|------------|---------------------|-------------------------|
| Two separate | _____ | _____ | Both year and difficulty alone |
| One composite | _____ | _____ | Only year alone (leftmost) |

**Decision guide:**
- If you query both columns together often → composite index
- If you query columns individually often → separate indexes
- If in doubt → composite index (more efficient for combined queries)

---

## Exercise Set 3: Covering Indexes and Index-Only Scans

### Exercise 3.1: Creating a Covering Index (30 minutes)

**Goal**: Achieve Index Only Scan for maximum performance

**Scenario**: Analytics dashboard frequently runs this query:

```sql
SELECT year, difficulty, COUNT(*), AVG(marks)
FROM questions
GROUP BY year, difficulty;
```

**Step 1: Without covering index**

```sql
-- Run query
EXPLAIN ANALYZE
SELECT year, difficulty, COUNT(*), AVG(marks)
FROM questions
GROUP BY year, difficulty;

-- Expected: Seq Scan or Index Scan + table lookup
-- Record execution time: _____ ms
```

**Step 2: Create covering index**

```sql
-- Index includes all columns needed by query
CREATE INDEX idx_questions_analytics
ON questions(year, difficulty, marks);

-- Run query again
EXPLAIN ANALYZE
SELECT year, difficulty, COUNT(*), AVG(marks)
FROM questions
GROUP BY year, difficulty;

-- Expected: Index Only Scan
-- Heap Fetches: 0 (no table access!)
-- Record execution time: _____ ms
```

**Step 3: Calculate improvement**

```
Speedup = Time_without / Time_with
Speedup = _____ ms / _____ ms = _____x faster
```

**Step 4: Verify Index Only Scan**

```sql
-- Query that accesses non-indexed column (must access table)
EXPLAIN ANALYZE
SELECT year, difficulty, question_text
FROM questions
WHERE year = 2023;

-- Expected: Index Scan (not Index Only Scan)
-- Because question_text not in index

-- Query with only indexed columns
EXPLAIN ANALYZE
SELECT year, difficulty, marks
FROM questions
WHERE year = 2023;

-- Expected: Index Only Scan
-- Heap Fetches: 0
```

**Key insight**: Covering index = query accesses only indexed columns = no table lookup = fastest!

**Cleanup:**
```sql
DROP INDEX idx_questions_analytics;
```

---

### Exercise 3.2: Include Columns (PostgreSQL 11+) (20 minutes)

**Goal**: Use INCLUDE to add non-key columns to index

**Scenario**: You want index on (year), but also want to cover (marks) without making marks part of the key

**Step 1: Regular index (marks not included)**

```sql
CREATE INDEX idx_year_only ON questions(year);

EXPLAIN ANALYZE
SELECT year, marks FROM questions WHERE year = 2023;

-- Expected: Index Scan (not Index Only)
-- Must fetch marks from table

DROP INDEX idx_year_only;
```

**Step 2: Index with INCLUDE**

```sql
-- Create index with included columns
CREATE INDEX idx_year_include_marks ON questions(year) INCLUDE (marks);

EXPLAIN ANALYZE
SELECT year, marks FROM questions WHERE year = 2023;

-- Expected: Index Only Scan
-- marks included but not part of key

-- Verify: can still filter on year
EXPLAIN ANALYZE
SELECT year, marks FROM questions WHERE year BETWEEN 2020 AND 2023;

-- Expected: Index Only Scan with range
```

**Benefit**: marks not part of key → smaller internal nodes → more keys per node → shallower tree

**Cleanup:**
```sql
DROP INDEX idx_year_include_marks;
```

---

## Exercise Set 4: Partial Indexes

### Exercise 4.1: Creating Partial Indexes (30 minutes)

**Goal**: Create smaller, faster indexes for specific queries

**Scenario**: 90% of your queries search for recent questions (year >= 2020)

**Step 1: Full index**

```sql
CREATE INDEX idx_year_full ON questions(year);

-- Check index size
SELECT pg_size_pretty(pg_relation_size('idx_year_full'));
-- Size: _____ kB
```

**Step 2: Partial index (only recent years)**

```sql
CREATE INDEX idx_year_recent ON questions(year)
WHERE year >= 2020;

-- Check index size
SELECT pg_size_pretty(pg_relation_size('idx_year_recent'));
-- Size: _____ kB (should be smaller)
```

**Step 3: Test queries**

```sql
-- Query matches partial index condition
EXPLAIN ANALYZE
SELECT * FROM questions WHERE year = 2023;
-- Uses: idx_year_recent ✅

-- Query matches partial index condition (range)
EXPLAIN ANALYZE
SELECT * FROM questions WHERE year >= 2022;
-- Uses: idx_year_recent ✅

-- Query does NOT match partial index condition
EXPLAIN ANALYZE
SELECT * FROM questions WHERE year = 2015;
-- Uses: idx_year_full (or Seq Scan if full index dropped)
```

**Step 4: Compare sizes and performance**

| Index | Size | Query (year=2023) Time | Query (year=2015) Time |
|-------|------|----------------------|----------------------|
| Full index | _____ kB | _____ ms | _____ ms |
| Partial index | _____ kB | _____ ms | N/A (can't use) |

**Benefits of partial index:**
- Smaller size (faster to scan)
- Faster to maintain (fewer entries to update)
- More cache-friendly

**Cleanup:**
```sql
DROP INDEX idx_year_full;
DROP INDEX idx_year_recent;
```

---

### Exercise 4.2: Partial Index for Common Filters (20 minutes)

**Goal**: Optimize queries with common WHERE conditions

**Scenario**: Dashboard frequently shows hard questions

```sql
SELECT * FROM questions WHERE difficulty = 'hard';
```

**Step 1: Full index on difficulty**

```sql
CREATE INDEX idx_difficulty_full ON questions(difficulty);

-- Check size
SELECT pg_size_pretty(pg_relation_size('idx_difficulty_full'));
-- Size: _____ kB
```

**Step 2: Partial index for hard questions only**

```sql
CREATE INDEX idx_hard_questions ON questions(question_id)
WHERE difficulty = 'hard';

-- Check size
SELECT pg_size_pretty(pg_relation_size('idx_hard_questions'));
-- Size: _____ kB (much smaller!)
```

**Step 3: Test**

```sql
-- Query for hard questions
EXPLAIN ANALYZE
SELECT * FROM questions WHERE difficulty = 'hard';
-- Uses: idx_hard_questions ✅

-- Query for easy questions
EXPLAIN ANALYZE
SELECT * FROM questions WHERE difficulty = 'easy';
-- Uses: idx_difficulty_full (or Seq Scan)
```

**Use case**: Partial indexes perfect for:
- Status filters (`WHERE status = 'active'`)
- Date ranges (`WHERE created_at > '2023-01-01'`)
- Boolean flags (`WHERE is_published = true`)

**Cleanup:**
```sql
DROP INDEX idx_difficulty_full;
DROP INDEX idx_hard_questions;
```

---

## Exercise Set 5: Real-World Optimization

### Exercise 5.1: Optimize a Slow Query (60 minutes)

**Goal**: End-to-end optimization of a real query

**Scenario**: Course analytics query is slow

```sql
-- Slow analytics query
SELECT
    c.course_code,
    c.title,
    COUNT(q.question_id) as question_count,
    AVG(q.marks) as avg_marks,
    COUNT(CASE WHEN q.difficulty = 'easy' THEN 1 END) as easy_count,
    COUNT(CASE WHEN q.difficulty = 'medium' THEN 1 END) as medium_count,
    COUNT(CASE WHEN q.difficulty = 'hard' THEN 1 END) as hard_count
FROM courses c
LEFT JOIN questions q ON c.course_id = q.course_id
WHERE q.year >= 2020
GROUP BY c.course_id, c.course_code, c.title
ORDER BY question_count DESC;
```

**Step 1: Baseline measurement**

```sql
EXPLAIN ANALYZE [query above];

-- Record:
-- Execution time: _____ ms
-- Scan types: _____
-- Bottlenecks: _____
```

**Step 2: Identify optimization opportunities**

```sql
-- Look for:
-- 1. Seq Scan (needs index)
-- 2. High cost operations
-- 3. Large row estimates vs actual

-- Common issues:
-- - No index on questions(year)
-- - No index on questions(course_id)
-- - JOIN without index
```

**Step 3: Create indexes**

```sql
-- Index for WHERE clause
CREATE INDEX idx_questions_year_opt ON questions(year);

-- Index for JOIN
CREATE INDEX idx_questions_course_opt ON questions(course_id);

-- Composite for better performance
CREATE INDEX idx_questions_year_course_opt
ON questions(year, course_id, difficulty, marks);
```

**Step 4: Remeasure**

```sql
EXPLAIN ANALYZE [query above];

-- Record:
-- Execution time: _____ ms
-- Improvement: _____x faster
```

**Step 5: Further optimization (covering index)**

```sql
-- Create covering index for entire query
CREATE INDEX idx_questions_analytics_full
ON questions(course_id, year, difficulty, marks);

EXPLAIN ANALYZE [query above];

-- Record:
-- Execution time: _____ ms
-- Total improvement: _____x faster
```

**Step 6: Document your findings**

```
Original query time: _____ ms
With indexes: _____ ms
Speedup: _____x

Indexes created:
1. idx_questions_year_opt
2. idx_questions_course_opt
3. idx_questions_analytics_full

Best index: _____ (provides _____x speedup)

Recommendation: Keep only the best index to save space
```

**Cleanup:**
```sql
-- Keep the best one, drop others
DROP INDEX idx_questions_year_opt;
DROP INDEX idx_questions_course_opt;
-- Keep: idx_questions_analytics_full
```

---

### Exercise 5.2: Finding Unused Indexes (20 minutes)

**Goal**: Identify and remove indexes that aren't being used

**Step 1: Create some test indexes**

```sql
CREATE INDEX idx_test_1 ON questions(marks);
CREATE INDEX idx_test_2 ON questions(question_text);
CREATE INDEX idx_test_3 ON questions(year, marks);
```

**Step 2: Run some queries**

```sql
-- This uses idx_test_3
SELECT * FROM questions WHERE year = 2023 AND marks > 10;

-- This uses idx_test_1
SELECT * FROM questions WHERE marks = 15;

-- idx_test_2 not used by any query
```

**Step 3: Check index usage statistics**

```sql
-- View index scan counts
SELECT
    schemaname,
    tablename,
    indexname,
    idx_scan as scans,
    idx_tup_read as tuples_read,
    idx_tup_fetch as tuples_fetched,
    pg_size_pretty(pg_relation_size(indexrelid)) as size
FROM pg_stat_user_indexes
WHERE tablename = 'questions'
ORDER BY idx_scan ASC;
```

**Expected output:**
```
 indexname   | scans | tuples_read | tuples_fetched | size
-------------+-------+-------------+----------------+------
 idx_test_2  |     0 |           0 |              0 | 24 kB  ← UNUSED!
 idx_test_1  |     1 |          10 |             10 | 16 kB
 idx_test_3  |     1 |           5 |              5 | 20 kB
```

**Step 4: Find all unused indexes**

```sql
SELECT
    schemaname,
    tablename,
    indexname,
    pg_size_pretty(pg_relation_size(indexrelid)) as size
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
  AND idx_scan = 0
  AND indexrelid NOT IN (
      -- Exclude primary keys and unique constraints
      SELECT conindid FROM pg_constraint WHERE contype IN ('p', 'u')
  )
ORDER BY pg_relation_size(indexrelid) DESC;
```

**Step 5: Drop unused indexes**

```sql
-- Safe to drop (not used)
DROP INDEX idx_test_2;

-- Keep these (being used)
-- idx_test_1, idx_test_3
```

**Cleanup:**
```sql
DROP INDEX idx_test_1;
DROP INDEX idx_test_3;
```

---

## Exercise Set 6: Hash Indexes

### Exercise 6.1: Hash Index vs B+ Tree (30 minutes)

**Goal**: Compare hash and B+ tree indexes for equality queries

**Step 1: B+ tree index (default)**

```sql
CREATE INDEX idx_course_code_btree ON courses(course_code);

-- Test equality
EXPLAIN ANALYZE
SELECT * FROM courses WHERE course_code = 'CS201';
-- Record time: _____ ms

-- Test range (works with B+ tree)
EXPLAIN ANALYZE
SELECT * FROM courses WHERE course_code > 'CS200' AND course_code < 'CS300';
-- Record time: _____ ms

DROP INDEX idx_course_code_btree;
```

**Step 2: Hash index**

```sql
CREATE INDEX idx_course_code_hash ON courses USING HASH (course_code);

-- Test equality
EXPLAIN ANALYZE
SELECT * FROM courses WHERE course_code = 'CS201';
-- Record time: _____ ms

-- Test range (CANNOT use hash index)
EXPLAIN ANALYZE
SELECT * FROM courses WHERE course_code > 'CS200' AND course_code < 'CS300';
-- Expected: Seq Scan (hash index not used)
-- Record time: _____ ms

DROP INDEX idx_course_code_hash;
```

**Step 3: Compare results**

| Index Type | Equality Time | Range Query Time | Range Query Works? |
|------------|---------------|------------------|-------------------|
| B+ tree    | _____ ms      | _____ ms         | ✅ Yes            |
| Hash       | _____ ms      | _____ ms         | ❌ No (Seq Scan)  |

**Conclusion:**
- Hash: Slightly faster for equality (usually negligible difference)
- B+ tree: Works for everything (equality + range + sort)
- **Recommendation**: Use B+ tree (default) unless you have specific hash needs

---

## Challenge Exercises

### Challenge 1: Full CourseDB-AI Index Strategy (90 minutes)

**Goal**: Design complete indexing strategy for CourseDB-AI

**Your task:**

1. **Analyze all queries** in your application:
   - API endpoints in app/api/
   - Common WHERE conditions
   - JOIN conditions
   - ORDER BY columns

2. **Design indexes** for:
   - courses table
   - topics table
   - questions table
   - resources table (if exists)

3. **Document your strategy:**
   ```sql
   -- courses table indexes
   CREATE INDEX idx_courses_code ON courses(course_code);
   -- Rationale: Unique lookups, primary search field
   
   -- questions table indexes
   CREATE INDEX idx_questions_year_difficulty ON questions(year, difficulty);
   -- Rationale: Most common filter combination (80% of queries)
   
   -- Add more...
   ```

4. **Implement and test:**
   - Create all indexes
   - Run EXPLAIN ANALYZE on key queries
   - Measure improvements
   - Document results

5. **Review for over-indexing:**
   - Check index usage statistics
   - Remove unused indexes
   - Keep only beneficial indexes

**Deliverable**: `indexing_strategy.sql` file with all index definitions and rationale

---

### Challenge 2: Query Optimization Competition (60 minutes)

**Goal**: Optimize this complex query to be as fast as possible

**The query:**
```sql
-- Find courses with most hard questions in recent years
SELECT
    c.course_code,
    c.title,
    COUNT(q.question_id) as hard_question_count,
    AVG(q.marks) as avg_marks,
    MAX(q.year) as latest_year,
    STRING_AGG(DISTINCT t.topic_name, ', ' ORDER BY t.topic_name) as topics
FROM courses c
JOIN questions q ON c.course_id = q.course_id
JOIN topics t ON q.topic_id = t.topic_id
WHERE q.difficulty = 'hard'
  AND q.year >= 2020
  AND q.marks >= 10
GROUP BY c.course_id, c.course_code, c.title
HAVING COUNT(q.question_id) >= 5
ORDER BY hard_question_count DESC, avg_marks DESC
LIMIT 10;
```

**Your challenge:**
1. Measure baseline (no indexes beyond primary keys)
2. Create indexes to optimize this query
3. Get execution time as low as possible
4. Document your approach

**Rules:**
- Can create any indexes
- Can create covering indexes
- Can create partial indexes
- Cannot modify the query itself

**Winner**: Lowest execution time!

**Share your solution:**
- Indexes created: _____
- Original time: _____ ms
- Optimized time: _____ ms
- Speedup: _____x

---

## Summary Checklist

After completing these exercises, you should be able to:

- [ ] Create single-column indexes
- [ ] Create composite (multi-column) indexes
- [ ] Understand and apply leftmost prefix rule
- [ ] Create covering indexes for Index Only Scans
- [ ] Create partial indexes for common filters
- [ ] Use EXPLAIN ANALYZE to measure query performance
- [ ] Identify when indexes are and aren't used
- [ ] Calculate query speedup from indexes
- [ ] Find and remove unused indexes
- [ ] Design comprehensive indexing strategy
- [ ] Optimize real-world queries with indexes

**Next steps:**
- Complete implementation_plan.md for 7-day guided practice
- Review mistakes_to_expect.md to avoid common pitfalls
- Track progress with checkpoints.md

**Great work! You're now equipped to make databases blazingly fast! 🚀**

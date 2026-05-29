# Week 7: Indexing & B+ Trees - Common Mistakes and How to Fix Them

## 🎯 Purpose

Week 7 introduces database indexing for performance optimization. This guide prepares you for common mistakes with:
- Index creation and usage
- EXPLAIN ANALYZE interpretation
- Composite index design
- Performance measurement
- Over-indexing and under-indexing

---

## Mistake Category 1: Index Not Being Used

### Mistake 1.1: Function on Indexed Column

**What happens:**
```sql
CREATE INDEX idx_difficulty ON questions(difficulty);

-- This query CANNOT use the index!
SELECT * FROM questions WHERE LOWER(difficulty) = 'hard';

EXPLAIN ANALYZE shows: Seq Scan on questions
```

**Why it happens:**
Index is on `difficulty`, but query uses `LOWER(difficulty)`. PostgreSQL can't use the index because it's a different value.

**How to fix:**
```sql
-- Option 1: Remove function from query (if possible)
SELECT * FROM questions WHERE difficulty = 'HARD';
-- Now uses index ✅

-- Option 2: Create expression index
CREATE INDEX idx_difficulty_lower ON questions(LOWER(difficulty));
SELECT * FROM questions WHERE LOWER(difficulty) = 'hard';
-- Now uses expression index ✅

-- Option 3: Store normalized data
-- ALTER TABLE questions ADD COLUMN difficulty_lower VARCHAR(20);
-- UPDATE questions SET difficulty_lower = LOWER(difficulty);
-- CREATE INDEX idx_difficulty_lower ON questions(difficulty_lower);
```

**How to avoid:**
- Don't apply functions to indexed columns in WHERE
- Create expression indexes when functions are necessary
- Normalize data at write time, not read time

---

### Mistake 1.2: Leading Wildcard in LIKE Query

**What happens:**
```sql
CREATE INDEX idx_question_text ON questions(question_text);

-- This CANNOT use B+ tree index!
SELECT * FROM questions WHERE question_text LIKE '%normalization%';

-- EXPLAIN shows: Seq Scan
```

**Why it happens:**
B+ tree indexes are sorted by prefix. `%normalization%` means "normalization anywhere in the text" - index can't help because it doesn't know where to start.

**How to fix:**
```sql
-- Option 1: Remove leading wildcard (if possible)
SELECT * FROM questions WHERE question_text LIKE 'What is%';
-- Uses index ✅

-- Option 2: Use full-text search
CREATE INDEX idx_question_text_fts ON questions
USING GIN (to_tsvector('english', question_text));

SELECT * FROM questions
WHERE to_tsvector('english', question_text) @@ to_tsquery('normalization');
-- Uses GIN index ✅

-- Option 3: Use trigram index (pg_trgm extension)
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE INDEX idx_question_text_trgm ON questions
USING GIN (question_text gin_trgm_ops);

SELECT * FROM questions WHERE question_text LIKE '%normalization%';
-- Uses trigram index ✅
```

**How to avoid:**
- Avoid leading wildcards when possible
- Use full-text search for text searching
- Use trigram indexes for partial matching

---

### Mistake 1.3: Skipping Leftmost Column in Composite Index

**What happens:**
```sql
CREATE INDEX idx_year_difficulty ON questions(year, difficulty);

-- This CANNOT use the index!
SELECT * FROM questions WHERE difficulty = 'hard';

-- EXPLAIN shows: Seq Scan (index not used)
```

**Why it happens:**
Composite index `(year, difficulty)` is like a phone book sorted by (last name, first name). You can't efficiently find all "John"s without knowing the last name.

**How to fix:**
```sql
-- Option 1: Include leftmost column in query
SELECT * FROM questions WHERE year = 2023 AND difficulty = 'hard';
-- Uses index ✅

-- Option 2: Create separate index for difficulty
CREATE INDEX idx_difficulty ON questions(difficulty);
SELECT * FROM questions WHERE difficulty = 'hard';
-- Uses new index ✅

-- Option 3: Reorder composite index
DROP INDEX idx_year_difficulty;
CREATE INDEX idx_difficulty_year ON questions(difficulty, year);
-- Now queries on difficulty alone can use index
```

**How to avoid:**
- Remember leftmost prefix rule
- Order composite index columns by query frequency
- Create separate indexes if needed

---

### Mistake 1.4: Low Selectivity Query

**What happens:**
```sql
CREATE INDEX idx_difficulty ON questions(difficulty);

-- Query returns 40% of rows
SELECT * FROM questions WHERE difficulty = 'medium';

-- EXPLAIN shows: Seq Scan (index exists but not used!)
```

**Why it happens:**
PostgreSQL's query planner decides: "Index would find 4,000 rows, then fetch 4,000 pages from disk. Sequential scan of entire table is faster!"

**How to fix:**
```sql
-- Option 1: Accept that index won't help (this is correct behavior)
-- Sequential scan is actually faster for low selectivity

-- Option 2: Add more selective conditions
SELECT * FROM questions
WHERE difficulty = 'medium' AND year = 2023;
-- Now more selective, index might help

-- Option 3: Create partial index for common specific case
CREATE INDEX idx_hard_questions ON questions(question_id)
WHERE difficulty = 'hard';
-- Only indexes 20% of rows
```

**How to avoid:**
- Don't create indexes for low-selectivity columns (e.g., boolean, gender, status with few values)
- Trust PostgreSQL's query planner
- Use EXPLAIN to verify actual behavior

---

## Mistake Category 2: Composite Index Design

### Mistake 2.1: Wrong Column Order

**What happens:**
```sql
-- 80% of queries: WHERE year = X
-- 20% of queries: WHERE difficulty = Y

CREATE INDEX idx_difficulty_year ON questions(difficulty, year);

-- Most common query
SELECT * FROM questions WHERE year = 2023;
-- Cannot use index! ❌
```

**Why it happens:**
Index column order matters. Most common query column should be leftmost.

**How to fix:**
```sql
-- Correct order: most common column first
DROP INDEX idx_difficulty_year;
CREATE INDEX idx_year_difficulty ON questions(year, difficulty);

-- Now most common query uses index
SELECT * FROM questions WHERE year = 2023;
-- Uses index ✅

-- And combined query also uses index
SELECT * FROM questions WHERE year = 2023 AND difficulty = 'hard';
-- Uses index ✅
```

**How to avoid:**
- Analyze query patterns before creating index
- Put most frequently queried columns first
- Put most selective columns first (if frequency equal)

---

### Mistake 2.2: Creating Too Many Composite Indexes

**What happens:**
```sql
-- Trying to optimize every possible query combination
CREATE INDEX idx_year_difficulty ON questions(year, difficulty);
CREATE INDEX idx_year_marks ON questions(year, marks);
CREATE INDEX idx_difficulty_marks ON questions(difficulty, marks);
CREATE INDEX idx_year_difficulty_marks ON questions(year, difficulty, marks);

-- Result: 4 indexes eating disk space, slowing down writes
```

**Why it happens:**
Desire to optimize every query without considering costs.

**How to fix:**
```sql
-- Drop all indexes
DROP INDEX idx_year_difficulty;
DROP INDEX idx_year_marks;
DROP INDEX idx_difficulty_marks;
DROP INDEX idx_year_difficulty_marks;

-- Create ONE comprehensive index
CREATE INDEX idx_year_difficulty_marks ON questions(year, difficulty, marks);

-- This single index can handle:
-- - WHERE year = X  ✅
-- - WHERE year = X AND difficulty = Y  ✅
-- - WHERE year = X AND difficulty = Y AND marks = Z  ✅
-- - WHERE year = X AND marks = Z  ✅ (uses year, filters marks)
```

**How to avoid:**
- Start with one well-designed composite index
- Use EXPLAIN to verify it's used
- Add more indexes only if proven necessary
- Monitor index usage statistics

---

### Mistake 2.3: Ignoring Column Order in WHERE Clause

**What happens:**
```sql
CREATE INDEX idx_year_difficulty ON questions(year, difficulty);

-- Developer thinks: "I need to write WHERE in same order as index"
SELECT * FROM questions WHERE year = 2023 AND difficulty = 'hard';  -- Works
SELECT * FROM questions WHERE difficulty = 'hard' AND year = 2023;  -- Thinks this won't work
```

**Why this is a misconception:**
PostgreSQL query planner automatically reorders WHERE conditions! Column order in WHERE doesn't matter.

**How to fix:**
```sql
-- Both queries use index identically
SELECT * FROM questions WHERE year = 2023 AND difficulty = 'hard';
-- Uses index ✅

SELECT * FROM questions WHERE difficulty = 'hard' AND year = 2023;
-- Also uses index ✅ (planner reorders internally)

EXPLAIN shows same plan for both
```

**Key insight:**
- Column order in INDEX definition matters
- Column order in WHERE clause doesn't matter (planner reorders)

---

## Mistake Category 3: EXPLAIN Misinterpretation

### Mistake 3.1: Confusing Cost with Time

**What happens:**
```sql
EXPLAIN SELECT * FROM questions WHERE year = 2023;

-- Output:
-- Index Scan ... (cost=0.29..8.16 rows=1 width=500)

-- Developer thinks: "Cost 8.16 means 8.16 milliseconds"
```

**Why it's wrong:**
Cost is abstract units, NOT time. Cost units are relative for comparison, not absolute time.

**How to fix:**
```sql
-- Use EXPLAIN ANALYZE for actual time
EXPLAIN ANALYZE SELECT * FROM questions WHERE year = 2023;

-- Output:
-- Index Scan ... (cost=0.29..8.16 rows=1 width=500)
--                (actual time=0.015..0.015 rows=1 loops=1)
-- Execution Time: 0.025 ms

-- Actual time: 0.025ms (this is real time!)
-- Cost: 8.16 (just for comparison with other plans)
```

**How to avoid:**
- Always use EXPLAIN ANALYZE, not just EXPLAIN
- Focus on "actual time" and "Execution Time"
- Use cost only for comparing alternative plans

---

### Mistake 3.2: Not Recognizing When Index Isn't Used

**What happens:**
```sql
CREATE INDEX idx_year ON questions(year);

EXPLAIN ANALYZE SELECT * FROM questions WHERE year = 2023;

-- Developer sees "Seq Scan" but thinks:
-- "I created an index, so it must be using it!"
```

**Why it happens:**
Not carefully reading EXPLAIN output.

**How to fix:**
```sql
-- Look for these keywords in EXPLAIN:
-- ✅ "Index Scan using idx_year" = index used
-- ✅ "Index Only Scan using idx_year" = index used (best!)
-- ❌ "Seq Scan" = index NOT used
-- ⚠️ "Bitmap Index Scan" = index used (special case)

-- If you see Seq Scan:
-- 1. Check if index exists: \d questions
-- 2. Check if query matches index
-- 3. Check selectivity (maybe Seq Scan is correct choice)
-- 4. Force index temporarily to test:
SET enable_seqscan = off;
EXPLAIN ANALYZE [your query];
SET enable_seqscan = on;
```

**How to avoid:**
- Always read EXPLAIN output carefully
- Look for index name in output
- Understand when Seq Scan is correct choice

---

### Mistake 3.3: Not Checking Actual Rows vs Estimated

**What happens:**
```sql
EXPLAIN ANALYZE SELECT * FROM questions WHERE year = 2023;

-- Output:
-- (cost=... rows=50 width=500)
-- (actual time=... rows=5000 loops=1)

-- Developer doesn't notice: estimated 50, actual 5000!
```

**Why it matters:**
Large discrepancy means statistics are stale → planner makes bad decisions → slow queries.

**How to fix:**
```sql
-- Update table statistics
ANALYZE questions;

-- Run query again
EXPLAIN ANALYZE SELECT * FROM questions WHERE year = 2023;

-- Output now shows:
-- (cost=... rows=5000 width=500)
-- (actual time=... rows=5000 loops=1)
-- Much better!

-- Set up auto-analyze (usually enabled by default)
-- Check: SHOW autovacuum;
```

**How to avoid:**
- Always compare estimated vs actual rows
- Run ANALYZE after bulk data changes
- Enable autovacuum
- Re-ANALYZE if estimates are way off

---

## Mistake Category 4: Over-Indexing

### Mistake 4.1: Index on Every Column

**What happens:**
```sql
-- "More indexes = better performance, right?"
CREATE INDEX idx_q1 ON questions(year);
CREATE INDEX idx_q2 ON questions(difficulty);
CREATE INDEX idx_q3 ON questions(marks);
CREATE INDEX idx_q4 ON questions(question_text);
CREATE INDEX idx_q5 ON questions(course_id);
CREATE INDEX idx_q6 ON questions(topic_id);
CREATE INDEX idx_q7 ON questions(created_at);
CREATE INDEX idx_q8 ON questions(updated_at);

-- Result:
-- - 8 indexes eating 500KB+ disk
-- - INSERT takes 5x longer
-- - UPDATE takes 3x longer
-- - Most indexes never used
```

**Why it's bad:**
Each index must be updated on INSERT/UPDATE/DELETE. Too many indexes = slow writes.

**How to fix:**
```sql
-- Check which indexes are actually used
SELECT
    indexname,
    idx_scan,
    pg_size_pretty(pg_relation_size(indexrelid)) as size
FROM pg_stat_user_indexes
WHERE tablename = 'questions'
ORDER BY idx_scan ASC;

-- Output shows:
-- idx_q4: 0 scans (never used!) - DROP IT
-- idx_q7: 1 scan (rarely used) - DROP IT
-- idx_q8: 0 scans (never used!) - DROP IT

DROP INDEX idx_q4;
DROP INDEX idx_q7;
DROP INDEX idx_q8;

-- Keep only frequently used indexes
```

**How to avoid:**
- Create indexes based on query analysis, not guessing
- Monitor index usage with pg_stat_user_indexes
- Remove unused indexes
- Start with fewer indexes, add more as needed

---

### Mistake 4.2: Not Measuring Write Performance Impact

**What happens:**
```sql
-- Developer adds 5 indexes
-- Reads get faster ✅
-- But never tests INSERT/UPDATE speed ❌

-- Later: Users complain forms are slow
-- Reason: Every form submission now updates 5 indexes
```

**How to fix:**
```sql
-- Benchmark BEFORE adding indexes
\timing on

-- Test INSERT (run 10 times, average)
INSERT INTO questions (course_id, topic_id, question_text, difficulty, marks, year)
VALUES (1, 1, 'Test question', 'easy', 10, 2023);
-- Time: 5ms average

-- Now add indexes
CREATE INDEX idx1 ON questions(year);
CREATE INDEX idx2 ON questions(difficulty);
CREATE INDEX idx3 ON questions(year, difficulty, marks);

-- Test INSERT again (run 10 times, average)
INSERT INTO questions (course_id, topic_id, question_text, difficulty, marks, year)
VALUES (1, 1, 'Test question', 'easy', 10, 2023);
-- Time: 15ms average (3x slower!)

-- Evaluate trade-off: Is 3x slower writes worth faster reads?
```

**How to avoid:**
- Always measure write performance before/after indexes
- Consider your workload: read-heavy or write-heavy?
- Document the trade-off
- Drop indexes during bulk imports

---

## Mistake Category 5: Covering Index Mistakes

### Mistake 5.1: Expecting Index Only Scan with Non-Indexed Columns

**What happens:**
```sql
CREATE INDEX idx_year ON questions(year);

SELECT year, difficulty, marks FROM questions WHERE year = 2023;

-- Expected: Index Only Scan
-- Actual: Index Scan (not Index Only!)
-- Heap Fetches: 50 (had to access table!)
```

**Why it happens:**
Index only contains `year`, but query needs `difficulty` and `marks` too. Must access table.

**How to fix:**
```sql
-- Create covering index with all needed columns
CREATE INDEX idx_year_covering ON questions(year, difficulty, marks);

SELECT year, difficulty, marks FROM questions WHERE year = 2023;

-- Now: Index Only Scan ✅
-- Heap Fetches: 0 ✅
```

**How to avoid:**
- For Index Only Scan, index must contain ALL columns in SELECT
- Check "Heap Fetches" in EXPLAIN output
- Create covering indexes for frequently run queries

---

### Mistake 5.2: Including Too Many Columns in Covering Index

**What happens:**
```sql
-- "Let's make this index cover EVERYTHING!"
CREATE INDEX idx_covering_huge ON questions(
    year, difficulty, marks, course_id, topic_id,
    question_text, answer_text, explanation, created_at, updated_at
);

-- Result:
-- - Index size: 5MB (larger than table!)
-- - INSERT performance: 10x slower
-- - Rarely gives benefit
```

**How to fix:**
```sql
-- Only include columns frequently accessed together
DROP INDEX idx_covering_huge;

CREATE INDEX idx_covering_reasonable ON questions(year, difficulty, marks);
-- Much smaller, still covers 80% of queries

-- For the 20% needing more columns: table access is OK
```

**How to avoid:**
- Include only columns that appear together in common queries
- Balance index size vs query benefit
- Don't try to cover every possible query

---

## Mistake Category 6: Maintenance Mistakes

### Mistake 6.1: Never Dropping Unused Indexes

**What happens:**
```sql
-- Indexes created 6 months ago
-- App evolved, queries changed
-- But indexes still exist, unused

-- Check usage:
SELECT indexname, idx_scan
FROM pg_stat_user_indexes
WHERE tablename = 'questions';

-- Output:
-- idx_old_feature: 0 scans (feature removed 3 months ago!)
-- idx_experiment: 0 scans (experiment abandoned)
-- idx_temporary: 0 scans (was for one-time migration)

-- These waste: disk space, insert performance, backup time
```

**How to fix:**
```sql
-- Find unused indexes
SELECT
    schemaname,
    tablename,
    indexname,
    pg_size_pretty(pg_relation_size(indexrelid)) as size,
    idx_scan
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
  AND idx_scan = 0
  AND indexrelid NOT IN (
      SELECT conindid FROM pg_constraint WHERE contype IN ('p', 'u')
  )
ORDER BY pg_relation_size(indexrelid) DESC;

-- Drop unused indexes
DROP INDEX idx_old_feature;
DROP INDEX idx_experiment;
DROP INDEX idx_temporary;
```

**How to avoid:**
- Review index usage quarterly
- Document why each index exists
- Remove indexes when features are removed
- Set up monitoring alerts for unused indexes

---

### Mistake 6.2: Not Rebuilding Bloated Indexes

**What happens:**
```sql
-- After millions of UPDATEs/DELETEs over months
-- Indexes get "bloated" (wasted space)
-- Performance slowly degrades
-- Developer doesn't notice gradual slowdown
```

**How to fix:**
```sql
-- Check index bloat
SELECT
    indexname,
    pg_size_pretty(pg_relation_size(indexrelid)) as size
FROM pg_stat_user_indexes
WHERE tablename = 'questions';

-- If indexes are suspiciously large, rebuild:
REINDEX INDEX idx_questions_year;

-- Or rebuild all indexes on table:
REINDEX TABLE questions;

-- Or rebuild entire database (during maintenance window):
REINDEX DATABASE coursedb_dev;
```

**How to avoid:**
- Schedule quarterly index rebuilds
- Monitor index size growth
- REINDEX after major data changes
- Set up autovacuum (handles some bloat)

---

## Quick Reference: Common Error Messages

| Error/Issue | Cause | Solution |
|------------|-------|----------|
| "Index not used (Seq Scan)" | Function on column, low selectivity, or small table | Check EXPLAIN, verify index matches query |
| "Heap Fetches > 0" | Index doesn't cover all columns | Add columns to index for Index Only Scan |
| "ERROR: could not create unique index" | Duplicate values exist | Find and fix duplicates, then create index |
| Query still slow after index | Wrong index, stale statistics, or complex query | Run ANALYZE, check EXPLAIN, consider covering index |
| INSERT suddenly slow | Too many indexes | Audit indexes, drop unused ones |
| "rows estimated: 100, actual: 10000" | Stale statistics | Run ANALYZE table |

---

## Best Practices Summary

1. **Always use EXPLAIN ANALYZE** - Don't guess, measure
2. **Create indexes based on queries** - Not every column needs an index
3. **Follow leftmost prefix rule** - Order matters in composite indexes
4. **Monitor index usage** - Drop unused indexes
5. **Measure write performance** - Indexes slow down writes
6. **Trust the query planner** - It's usually right about Seq Scan
7. **Keep statistics updated** - Run ANALYZE after bulk changes
8. **Document your indexes** - Why does each exist?

---

**Remember**: Index mistakes are learning opportunities! Use EXPLAIN ANALYZE, monitor statistics, and iterate. The best indexing strategy emerges from measuring real queries on real data.

**Next steps:**
- Review exercises.md for hands-on practice
- Complete checkpoints.md to verify understanding
- Apply these lessons to CourseDB-AI

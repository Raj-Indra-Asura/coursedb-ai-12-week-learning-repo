# Week 7: Indexing & B+ Trees

## 🎯 Learning Objectives

By the end of this week, you will:
- Understand what indexes are and why they're critical for database performance
- Master B+ tree structure and operations (insert, search, range queries)
- Learn when and how to create effective indexes
- Use EXPLAIN ANALYZE to measure query performance
- Apply indexing strategies to CourseDB-AI
- Understand trade-offs between query speed and write performance
- Create composite and covering indexes
- Analyze and optimize slow queries

---

## 📋 Week Overview

**Theme**: From slow to fast - transform your database performance with indexing

**The Problem**: Your CourseDB-AI has thousands of questions. Searching by year takes seconds because PostgreSQL scans every row.

**The Solution**: Indexes! Data structures that allow fast lookups, like a book's index lets you jump to specific pages.

**Real-world impact**: 
- Without indexes: Query takes 2 seconds (sequential scan of 10,000 rows)
- With indexes: Same query takes 5ms (index scan of 50 rows)
- **400x faster!**

---

## 1. What is an Index?

### The Book Analogy

**Scenario**: Find all mentions of "normalization" in a 500-page textbook.

**Without index:**
- Read every page (500 pages)
- Takes hours
- Inefficient

**With index:**
- Look in book index: "normalization - pages 42, 87, 156"
- Jump directly to those pages
- Takes minutes
- Efficient!

**Database equivalent:**

```sql
-- Without index: Sequential scan (slow)
SELECT * FROM questions WHERE year = 2023;
-- PostgreSQL reads EVERY row: 1, 2, 3, 4, 5, ..., 10000

-- With index: Index scan (fast)
CREATE INDEX idx_questions_year ON questions(year);
SELECT * FROM questions WHERE year = 2023;
-- PostgreSQL jumps directly to rows with year=2023
```

### Index Definition

**Index**: A data structure that maintains pointers to table rows, organized for fast lookup.

**Key concepts:**
- **Search key**: Column(s) you want to search by (e.g., `year`)
- **Index entry**: (search key value → pointer to table row)
- **Index structure**: How entries are organized (B+ tree, hash table, etc.)

### Time Complexity

| Operation | Without Index | With B+ Tree Index |
|-----------|---------------|-------------------|
| Find one row | O(n) - sequential scan | O(log n) - tree traversal |
| Find range | O(n) - sequential scan | O(log n + k) - k = results |
| Insert | O(1) - append | O(log n) - tree insert |
| Delete | O(n) - find + delete | O(log n) - tree delete |

**Example**: Table with 1,000,000 rows
- Sequential scan: 1,000,000 comparisons
- B+ tree (order 100): log₁₀₀(1,000,000) = ~3 disk reads
- **333,333x faster!**

---

## 2. Types of Indexes

### 2.1 B+ Tree Index (Default in PostgreSQL)

**Best for**: 
- Range queries (`WHERE year BETWEEN 2020 AND 2023`)
- Sorted access (`ORDER BY year`)
- Equality queries (`WHERE year = 2023`)

**Structure:**
```
           [50]
          /    \
      [20, 35]  [65, 80]
     /   |   \   /  |  \
   [10] [20] [35] [50] [65] [80]
    ↓    ↓    ↓    ↓    ↓    ↓
  (rows)(rows)(rows)(rows)(rows)(rows)
  
All leaf nodes linked: enables efficient range scans
```

**Properties:**
- Self-balancing (all paths same height)
- High fanout (many children per node)
- All data in leaf nodes
- Internal nodes only store keys for navigation

**Example usage:**
```sql
CREATE INDEX idx_questions_year ON questions(year);

-- Uses index efficiently
SELECT * FROM questions WHERE year = 2023;
SELECT * FROM questions WHERE year BETWEEN 2020 AND 2023;
SELECT * FROM questions ORDER BY year;
```

### 2.2 Hash Index

**Best for**:
- Exact equality queries (`WHERE course_code = 'CS201'`)

**Cannot handle**:
- Range queries
- Sorting
- Pattern matching

**Structure:**
```
Hash Function: f(key) → bucket number

course_code = 'CS201' → hash('CS201') = 42 → bucket[42] → row pointer
course_code = 'CS305' → hash('CS305') = 17 → bucket[17] → row pointer
```

**Example usage:**
```sql
CREATE INDEX idx_courses_code_hash ON courses USING HASH (course_code);

-- ✅ Uses hash index (O(1))
SELECT * FROM courses WHERE course_code = 'CS201';

-- ❌ Cannot use hash index
SELECT * FROM courses WHERE course_code > 'CS200';
```

**When to use hash vs B+ tree:**
- Hash: Only equality lookups, need fastest possible access
- B+ tree: Everything else (range, sort, default choice)

### 2.3 Other Index Types (Advanced)

**GiST (Generalized Search Tree)**:
- Full-text search
- Geometric data (points, polygons)
- Custom data types

**GIN (Generalized Inverted Index)**:
- Array columns (`tags TEXT[]`)
- JSONB data
- Full-text search

**BRIN (Block Range Index)**:
- Very large tables (billions of rows)
- Naturally ordered data (timestamps, IDs)
- Small index size

**Example:**
```sql
-- GIN for JSONB
CREATE INDEX idx_metadata_gin ON questions USING GIN (metadata);
SELECT * FROM questions WHERE metadata @> '{"difficulty": "hard"}';

-- BRIN for timestamps
CREATE INDEX idx_created_brin ON questions USING BRIN (created_at);
SELECT * FROM questions WHERE created_at > '2023-01-01';
```

---

## 3. B+ Tree Structure Deep Dive

### Why B+ Trees for Databases?

**Key insight**: Databases store data on disk, and **disk I/O is the bottleneck** (1000x slower than RAM).

**B+ tree advantages:**
1. **Minimize disk reads**: Each node = one disk page (4KB)
2. **High fanout**: Order 100-200 means 100-200 children per node
3. **Shallow trees**: Fewer levels = fewer disk reads
4. **Sequential leaf access**: Linked leaves allow range scans without tree traversal

### B+ Tree Properties

**Order (m)**: Maximum number of children per node

**Internal nodes**:
- Store m-1 keys
- Store m child pointers
- Keys guide search (which subtree to descend)
- **Do NOT store actual data**

**Leaf nodes**:
- Store actual data (or pointers to rows)
- All leaves at same level
- Linked together (left to right)

**Example B+ Tree (order=4, max 3 keys per node):**

```
                    [30]
                   /    \
              [10, 20]   [40, 50]
             /   |   \    /   |  \
        [5,7] [10,12] [20,25] [30,35] [40,45] [50,55]
          ↓      ↓       ↓       ↓       ↓       ↓
        data   data    data    data    data    data
         ←―――――――――――――――――――――――――――――――――――→
                  (linked list)
```

### B+ Tree Operations

#### **Search (Single Value)**

```
Find year = 35 in tree above:

1. Start at root [30]
   - 35 > 30, go right

2. Internal node [40, 50]
   - 35 < 40, go left

3. Leaf node [30, 35]
   - Found 35! Return data pointer
   
Time: O(log_m n) = 3 comparisons for millions of rows
```

#### **Range Query**

```
Find year BETWEEN 20 AND 45:

1. Search for 20 (start of range)
   - Navigate to leaf [20, 25]

2. Follow leaf links
   - [20, 25] → [30, 35] → [40, 45]
   - Collect all values in range

3. Stop at first value > 45

Time: O(log n + k) where k = number of results
```

#### **Insert**

```
Insert year = 22:

1. Find correct leaf (navigate tree)
2. Insert in sorted order in leaf
3. If leaf overflows (> max keys):
   - Split leaf into two
   - Promote middle key to parent
4. If parent overflows, split recursively

Example:
[20, 25] → insert 22 → [20, 22, 25] (no overflow, done)
```

#### **Delete**

```
Delete year = 10:

1. Find and remove from leaf
2. If leaf underflows (< min keys):
   - Borrow from sibling, OR
   - Merge with sibling
3. Update parent keys if needed
```

### Why All Data in Leaves?

**Alternative: B-tree (data in all nodes)**
- Pro: Faster search (might find in internal node)
- Con: Range scans require tree traversal

**B+ tree (data only in leaves)**
- Pro: Range scans just follow leaf links (sequential disk reads)
- Pro: More keys fit in internal nodes (higher fanout, shallower tree)
- Con: Must always traverse to leaves

**For databases: B+ tree wins** because range queries are common and sequential disk I/O is fast.

---

## 4. Creating and Using Indexes

### Basic Index Creation

```sql
-- Single column index
CREATE INDEX idx_questions_year ON questions(year);

-- View indexes
\d questions
-- Shows: "idx_questions_year" btree (year)

-- Drop index
DROP INDEX idx_questions_year;
```

### Index Types Syntax

```sql
-- B+ tree (default)
CREATE INDEX idx_year_btree ON questions(year);
CREATE INDEX idx_year ON questions(year);  -- same as above

-- Hash index
CREATE INDEX idx_code_hash ON courses USING HASH (course_code);

-- GIN index (for JSONB)
CREATE INDEX idx_metadata_gin ON questions USING GIN (metadata);
```

### Unique Indexes

```sql
-- Enforce uniqueness
CREATE UNIQUE INDEX idx_courses_code_unique ON courses(course_code);

-- Equivalent to UNIQUE constraint
ALTER TABLE courses ADD CONSTRAINT unique_course_code UNIQUE (course_code);
-- PostgreSQL automatically creates unique index
```

### Composite Indexes (Multi-Column)

```sql
-- Index on multiple columns
CREATE INDEX idx_year_difficulty ON questions(year, difficulty);

-- Order matters! (leftmost prefix rule)
-- ✅ Uses index
SELECT * FROM questions WHERE year = 2023;
SELECT * FROM questions WHERE year = 2023 AND difficulty = 'hard';

-- ❌ Cannot use index (skips leftmost column)
SELECT * FROM questions WHERE difficulty = 'hard';
```

**Leftmost prefix rule**: Index can be used if query includes leftmost column(s).

**Example:**
```sql
CREATE INDEX idx_abc ON table(a, b, c);

Uses index:
- WHERE a = 1
- WHERE a = 1 AND b = 2
- WHERE a = 1 AND b = 2 AND c = 3
- WHERE a = 1 AND c = 3  (uses 'a' only)

Cannot use index:
- WHERE b = 2
- WHERE c = 3
- WHERE b = 2 AND c = 3
```

### Partial Indexes

```sql
-- Index only rows matching condition
CREATE INDEX idx_hard_questions ON questions(question_id)
WHERE difficulty = 'hard';

-- Smaller index, faster for specific queries
SELECT * FROM questions WHERE difficulty = 'hard' AND year = 2023;
```

### Covering Indexes (Include Columns)

```sql
-- Index includes all columns needed by query
CREATE INDEX idx_questions_covering ON questions(year, difficulty, marks);

-- Query uses ONLY index (no table lookup!)
SELECT year, difficulty, marks
FROM questions
WHERE year = 2023;

-- EXPLAIN shows: Index Only Scan (fastest!)
```

---

## 5. Query Performance Analysis with EXPLAIN

### EXPLAIN Basics

```sql
-- Show execution plan (no execution)
EXPLAIN
SELECT * FROM questions WHERE year = 2023;

-- Show execution plan + actual runtime
EXPLAIN ANALYZE
SELECT * FROM questions WHERE year = 2023;
```

### Understanding EXPLAIN Output

**Without index:**
```
Seq Scan on questions  (cost=0.00..180.00 rows=50 width=200)
  Filter: (year = 2023)
  
- Seq Scan: Sequential scan (reads every row)
- cost: 0.00 (startup) .. 180.00 (total)
- rows: Estimated 50 rows returned
- width: Average row size (200 bytes)
```

**With index:**
```
Index Scan using idx_questions_year on questions
  (cost=0.29..10.50 rows=50 width=200)
  Index Cond: (year = 2023)
  
- Index Scan: Uses index
- cost: Lower (0.29..10.50 vs 0..180)
- Index Cond: Condition used by index
```

**Index Only Scan (best):**
```
Index Only Scan using idx_questions_covering on questions
  (cost=0.29..5.50 rows=50 width=12)
  Index Cond: (year = 2023)
  Heap Fetches: 0
  
- Index Only Scan: No table access needed
- Heap Fetches: 0 (perfect!)
```

### EXPLAIN ANALYZE Output

```sql
EXPLAIN ANALYZE
SELECT * FROM questions WHERE year = 2023;

-- Output:
Index Scan using idx_questions_year on questions
  (cost=0.29..10.50 rows=50 width=200)
  (actual time=0.015..0.125 rows=48 loops=1)
  Index Cond: (year = 2023)
Planning Time: 0.132 ms
Execution Time: 0.158 ms
```

**Key metrics:**
- **cost**: Estimated cost (arbitrary units)
- **rows**: Estimated rows (50 estimated vs 48 actual)
- **actual time**: Real time (0.015ms startup, 0.125ms total)
- **Planning Time**: Query planning overhead
- **Execution Time**: Actual query execution

### Common Scan Types (Slowest to Fastest)

1. **Seq Scan**: Full table scan, no index
2. **Index Scan**: Use index, then fetch rows from table
3. **Index Only Scan**: Use index only, no table access
4. **Bitmap Index Scan**: Multiple indexes combined
5. **Index Scan + Filter**: Index narrows, then filter remaining

---

## 6. Indexing Strategies

### When to Create Indexes

**✅ Create index if:**
- Column frequently in WHERE clause
- Column in JOIN condition
- Column in ORDER BY
- Large table (> 1000 rows)
- Queries are slow (identified with EXPLAIN)
- Read-heavy workload

**❌ Avoid index if:**
- Small table (< 1000 rows) - sequential scan is fast enough
- Column rarely queried
- Low cardinality (few distinct values, e.g., boolean)
- Write-heavy workload (indexes slow down INSERT/UPDATE/DELETE)
- Column values change frequently

### Index Selectivity

**Selectivity**: Percentage of rows matching a condition

```sql
-- High selectivity (good for index)
SELECT * FROM questions WHERE question_id = 12345;
-- Returns 1 row out of 10,000 (0.01% selectivity)

-- Low selectivity (bad for index)
SELECT * FROM questions WHERE difficulty = 'medium';
-- Returns 3,333 rows out of 10,000 (33% selectivity)
-- Sequential scan might be faster!
```

**Rule of thumb**: Index useful if selectivity < 5-10%

### Composite Index Strategy

**Question**: Should you create separate indexes or one composite?

```sql
-- Option A: Two separate indexes
CREATE INDEX idx_year ON questions(year);
CREATE INDEX idx_difficulty ON questions(difficulty);

-- Option B: One composite index
CREATE INDEX idx_year_difficulty ON questions(year, difficulty);
```

**Decision guide:**

| Query Pattern | Best Choice |
|--------------|-------------|
| `WHERE year = 2023` only | Option A (idx_year) |
| `WHERE difficulty = 'hard'` only | Option A (idx_difficulty) |
| `WHERE year = 2023 AND difficulty = 'hard'` | Option B (composite) |
| All of the above | Option A + B (3 indexes total) |

**Trade-off**: More indexes = faster reads but slower writes

### CourseDB-AI Indexing Strategy

**Current queries:**
```sql
-- Q1: Search by year
SELECT * FROM questions WHERE year = 2023;

-- Q2: Search by year and difficulty
SELECT * FROM questions WHERE year = 2023 AND difficulty = 'hard';

-- Q3: Search by course
SELECT * FROM questions WHERE course_id = 1;

-- Q4: Search by topic
SELECT * FROM questions WHERE topic_id = 5;

-- Q5: Questions per course (analytics)
SELECT course_id, COUNT(*) FROM questions GROUP BY course_id;
```

**Recommended indexes:**
```sql
-- For Q1, Q2
CREATE INDEX idx_questions_year_difficulty ON questions(year, difficulty);

-- For Q3, Q5
CREATE INDEX idx_questions_course ON questions(course_id);

-- For Q4
CREATE INDEX idx_questions_topic ON questions(topic_id);

-- For course code lookups
CREATE UNIQUE INDEX idx_courses_code ON courses(course_code);
```

---

## 7. Index Maintenance

### Viewing Indexes

```sql
-- List all indexes on table
\d questions

-- Detailed index information
SELECT
    tablename,
    indexname,
    indexdef
FROM pg_indexes
WHERE schemaname = 'public'
ORDER BY tablename, indexname;

-- Index size
SELECT
    indexname,
    pg_size_pretty(pg_relation_size(indexrelid)) AS size
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
ORDER BY pg_relation_size(indexrelid) DESC;
```

### Index Statistics

```sql
-- Index usage statistics
SELECT
    schemaname,
    tablename,
    indexname,
    idx_scan,        -- Number of index scans
    idx_tup_read,    -- Tuples read from index
    idx_tup_fetch    -- Tuples fetched from table
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
ORDER BY idx_scan DESC;

-- Unused indexes (idx_scan = 0)
SELECT
    schemaname,
    tablename,
    indexname,
    pg_size_pretty(pg_relation_size(indexrelid)) AS size
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
  AND idx_scan = 0
  AND indexrelid NOT IN (
      SELECT conindid FROM pg_constraint WHERE contype IN ('p', 'u')
  );
```

### Rebuilding Indexes

```sql
-- Rebuild index (removes bloat)
REINDEX INDEX idx_questions_year;

-- Rebuild all indexes on table
REINDEX TABLE questions;

-- Rebuild all indexes in database
REINDEX DATABASE coursedb_dev;
```

**When to rebuild:**
- After bulk data changes
- Index bloat (wasted space from updates/deletes)
- Performance degradation over time

---

## 8. Common Indexing Mistakes

### Mistake 1: Function on Indexed Column

```sql
CREATE INDEX idx_difficulty ON questions(difficulty);

-- ❌ Cannot use index (function on column)
SELECT * FROM questions WHERE LOWER(difficulty) = 'hard';

-- ✅ Uses index
SELECT * FROM questions WHERE difficulty = 'HARD';

-- ✅ Or create expression index
CREATE INDEX idx_difficulty_lower ON questions(LOWER(difficulty));
SELECT * FROM questions WHERE LOWER(difficulty) = 'hard';
```

### Mistake 2: Leading Wildcards

```sql
CREATE INDEX idx_question_text ON questions(question_text);

-- ❌ Cannot use B+ tree index
SELECT * FROM questions WHERE question_text LIKE '%normalization%';

-- ✅ Can use index (no leading wildcard)
SELECT * FROM questions WHERE question_text LIKE 'What is%';

-- ✅ Use full-text search instead
CREATE INDEX idx_question_text_fts ON questions
USING GIN (to_tsvector('english', question_text));

SELECT * FROM questions
WHERE to_tsvector('english', question_text) @@ to_tsquery('normalization');
```

### Mistake 3: OR Conditions on Different Columns

```sql
-- ❌ May not use indexes efficiently
SELECT * FROM questions
WHERE year = 2023 OR difficulty = 'hard';

-- ✅ Rewrite as UNION
SELECT * FROM questions WHERE year = 2023
UNION
SELECT * FROM questions WHERE difficulty = 'hard';
```

### Mistake 4: Too Many Indexes

```sql
-- ❌ Over-indexing (slows down writes)
CREATE INDEX idx_q1 ON questions(year);
CREATE INDEX idx_q2 ON questions(difficulty);
CREATE INDEX idx_q3 ON questions(marks);
CREATE INDEX idx_q4 ON questions(year, difficulty);
CREATE INDEX idx_q5 ON questions(year, marks);
CREATE INDEX idx_q6 ON questions(difficulty, marks);
CREATE INDEX idx_q7 ON questions(year, difficulty, marks);

-- ✅ Analyze query patterns, create only needed indexes
CREATE INDEX idx_year_difficulty ON questions(year, difficulty);
CREATE INDEX idx_marks ON questions(marks);
-- That's enough for most queries!
```

---

## 9. Practical Example: Optimizing CourseDB-AI

### Scenario: Slow Analytics Query

**Problem**: Course analytics dashboard is slow (5 seconds)

```sql
-- Slow query
SELECT
    c.course_code,
    c.title,
    COUNT(q.question_id) as question_count,
    AVG(q.marks) as avg_marks
FROM courses c
LEFT JOIN questions q ON c.course_id = q.course_id
WHERE q.year = 2023
GROUP BY c.course_id, c.course_code, c.title
ORDER BY question_count DESC;
```

**Step 1: Analyze with EXPLAIN**
```sql
EXPLAIN ANALYZE [query above];

-- Output shows:
-- Seq Scan on questions (cost=0..10000, time=4500ms)
-- Filter: (year = 2023)
```

**Problem identified**: Sequential scan on questions table

**Step 2: Create index**
```sql
CREATE INDEX idx_questions_year ON questions(year);
```

**Step 3: Verify improvement**
```sql
EXPLAIN ANALYZE [query above];

-- Output now shows:
-- Index Scan using idx_questions_year (cost=0..100, time=50ms)
-- Index Cond: (year = 2023)

-- Result: 90x faster! (4500ms → 50ms)
```

**Step 4: Further optimization (composite index)**
```sql
-- Also create index on join column
CREATE INDEX idx_questions_course ON questions(course_id);

-- Now down to 20ms (225x faster than original!)
```

---

## Summary

**Key Takeaways:**

1. **Indexes are essential** for fast database queries in large tables
2. **B+ trees** are the default and best general-purpose index structure
3. **EXPLAIN ANALYZE** is your best friend for identifying slow queries
4. **Trade-offs exist**: Indexes speed up reads but slow down writes
5. **Composite indexes** follow leftmost prefix rule
6. **Covering indexes** eliminate table lookups for maximum speed
7. **Index strategically**: Not every column needs an index

**Week 7 gives you the tools to:**
- Transform slow queries into fast ones
- Understand database internals
- Make informed indexing decisions
- Debug performance problems systematically

**Next steps:**
- Complete exercises.md (hands-on index creation and analysis)
- Follow implementation_plan.md (7-day guided practice)
- Read mistakes_to_expect.md (avoid common pitfalls)
- Track progress with checkpoints.md

---

**Ready to make your database blazingly fast? Let's go! 🚀**

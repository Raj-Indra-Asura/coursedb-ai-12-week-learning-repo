# Week 7: Indexing & B+ Trees - Theory Notes

## 📚 Core Concepts

### 1. What is an Index?

**Index**: Data structure that improves the speed of data retrieval operations.

**Analogy**: Like a book index - instead of reading every page to find "B+ tree", you look in the index to find the page number.

**Without Index:**
```sql
SELECT * FROM questions WHERE year = 2023;
-- Scans ALL rows (sequential scan) - O(n)
```

**With Index:**
```sql
CREATE INDEX idx_questions_year ON questions(year);
SELECT * FROM questions WHERE year = 2023;
-- Uses index to find rows directly - O(log n)
```

---

### 2. Types of Indexes

#### **B+ Tree Index** (Default in PostgreSQL)
- Best for range queries
- Maintains sorted order
- Self-balancing
- All data in leaf nodes

#### **Hash Index**
- Best for equality checks (=)
- Fast lookups: O(1)
- Cannot handle range queries
- No ordering

#### **GiST (Generalized Search Tree)**
- Full-text search
- Geometric data
- Custom types

#### **GIN (Generalized Inverted Index)**
- Array data
- JSON data
- Full-text search

---

### 3. B+ Tree Structure

**Properties:**
- Order (m): Maximum children per node
- Internal nodes: Keys for navigation
- Leaf nodes: Actual data (or pointers to data)
- Leaves linked: Enables efficient range scans

**Example B+ Tree (order=3):**
```
           [15]
          /    \
      [10]      [20, 30]
     /  \       /   |   \
  [5,7] [10,12] [15,18] [20,25] [30,35]
    ↓     ↓       ↓       ↓       ↓
  (data) (data)  (data)  (data)  (data)
```

**Why B+ Trees for Databases?**
1. **Minimize disk I/O**: Each node = one disk page
2. **Range queries**: Linked leaves allow sequential scan
3. **Balanced**: All paths same length (predictable performance)
4. **High fanout**: Fewer levels = fewer disk reads

---

### 4. Index Operations

#### **Creating Indexes**
```sql
-- Single column
CREATE INDEX idx_questions_year ON questions(year);

-- Composite index (multi-column)
CREATE INDEX idx_questions_year_difficulty
ON questions(year, difficulty);

-- Unique index
CREATE UNIQUE INDEX idx_courses_code ON courses(course_code);

-- Partial index (with WHERE clause)
CREATE INDEX idx_hard_questions
ON questions(difficulty)
WHERE difficulty = 'hard';
```

#### **Using Indexes**
```sql
-- Good: Uses index
SELECT * FROM questions WHERE year = 2023;

-- Bad: Cannot use index (function on column)
SELECT * FROM questions WHERE LOWER(difficulty) = 'hard';

-- Good: Composite index usage
SELECT * FROM questions
WHERE year = 2023 AND difficulty = 'hard';
```

---

### 5. Index Performance

**EXPLAIN ANALYZE**: Shows query execution plan

```sql
-- Without index
EXPLAIN ANALYZE
SELECT * FROM questions WHERE year = 2023;
-- Result: Seq Scan on questions (cost=0..100 rows=1000)

-- With index
CREATE INDEX idx_questions_year ON questions(year);
EXPLAIN ANALYZE
SELECT * FROM questions WHERE year = 2023;
-- Result: Index Scan using idx_questions_year (cost=0..10 rows=50)
```

**Metrics to understand:**
- **cost**: Estimated query cost
- **rows**: Estimated rows returned
- **actual time**: Real execution time
- **Seq Scan**: Full table scan (slow)
- **Index Scan**: Uses index (fast)

---

### 6. Index Trade-offs

**Benefits:**
- ✅ Faster SELECT queries
- ✅ Faster WHERE filtering
- ✅ Faster ORDER BY
- ✅ Faster JOINs

**Costs:**
- ❌ Slower INSERT (must update index)
- ❌ Slower UPDATE (if indexed column changes)
- ❌ Slower DELETE (must update index)
- ❌ Extra disk space

**When to use indexes:**
- Columns frequently in WHERE
- Columns in JOIN conditions
- Columns in ORDER BY
- Large tables with selective queries

**When NOT to use indexes:**
- Small tables (< 1000 rows)
- Columns rarely queried
- Columns with low cardinality (e.g., boolean)
- Heavy INSERT/UPDATE workloads

---

### 7. Composite Indexes

**Order matters!**

```sql
CREATE INDEX idx_year_difficulty ON questions(year, difficulty);

-- ✅ Uses index (leftmost prefix)
SELECT * FROM questions WHERE year = 2023;

-- ✅ Uses index fully
SELECT * FROM questions WHERE year = 2023 AND difficulty = 'hard';

-- ❌ Cannot use index (skips leftmost column)
SELECT * FROM questions WHERE difficulty = 'hard';
```

**Rule**: Index can be used if query includes leftmost columns.

---

### 8. Covering Indexes

**Covering Index**: Index contains all columns needed for query.

```sql
-- Create covering index
CREATE INDEX idx_questions_cover
ON questions(year, difficulty, marks);

-- Query uses ONLY index (no table lookup needed!)
SELECT year, difficulty, marks
FROM questions
WHERE year = 2023;
-- Result: Index Only Scan (fastest!)
```

---

## 🎯 CourseDB-AI Indexing Strategy

### Current Indexes (from models.py):
1. `idx_questions_year` - year column
2. `idx_questions_difficulty` - difficulty column
3. `idx_questions_year_difficulty` - composite
4. `idx_questions_course_topic` - composite FK
5. `idx_courses_code` - unique on course_code
6. `idx_topics_name` - topic_name

### Query Patterns to Optimize:
```sql
-- Common query 1: Filter by year and difficulty
SELECT * FROM questions WHERE year = 2023 AND difficulty = 'hard';
-- Uses: idx_questions_year_difficulty ✅

-- Common query 2: Find questions by topic
SELECT * FROM questions WHERE topic_id = 5;
-- Uses: idx_questions_course_topic ✅

-- Common query 3: Search by text (needs full-text search)
SELECT * FROM questions WHERE question_text ILIKE '%normalization%';
-- No index helps here ❌ (consider full-text search in Week 11)
```

---

## ✅ Self-Check Questions

1. What's the difference between B+ tree and hash index?
2. Why do B+ trees have all data in leaf nodes?
3. What's the cost of adding an index?
4. When would you use a composite index?
5. What does EXPLAIN ANALYZE show?
6. Why is leftmost prefix important for composite indexes?
7. What's a covering index?
8. When should you NOT create an index?

---

## 🔬 Hands-On Exercises

### Exercise 1: Create and Compare
```sql
-- 1. Run query without index
EXPLAIN ANALYZE SELECT * FROM questions WHERE year = 2023;

-- 2. Create index
CREATE INDEX idx_test_year ON questions(year);

-- 3. Run query with index
EXPLAIN ANALYZE SELECT * FROM questions WHERE year = 2023;

-- 4. Compare: cost, time, scan type
```

### Exercise 2: Composite Index Testing
```sql
CREATE INDEX idx_test ON questions(year, difficulty);

-- Which queries use the index?
-- A: WHERE year = 2023
-- B: WHERE difficulty = 'hard'
-- C: WHERE year = 2023 AND difficulty = 'hard'
-- D: WHERE difficulty = 'hard' AND year = 2023
```

---

**Next Week (Week 8):** Query optimization and performance tuning!

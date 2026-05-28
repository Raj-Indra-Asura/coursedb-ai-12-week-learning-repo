# Week 8: Query Optimization - Theory Notes

## 📚 Core Concepts

### 1. Query Optimization Overview

**Query Optimizer**: Component of DBMS that finds the most efficient way to execute a query.

**Goal**: Minimize cost (disk I/O, CPU, memory)

**Process:**
1. Parse SQL query
2. Generate multiple execution plans
3. Estimate cost of each plan
4. Choose plan with lowest cost
5. Execute chosen plan

---

### 2. Query Execution Plans

**Execution Plan**: Step-by-step strategy for executing a query.

**Reading EXPLAIN Output:**
```sql
EXPLAIN SELECT * FROM questions WHERE year = 2023;

Seq Scan on questions  (cost=0.00..35.00 rows=50 width=200)
  Filter: (year = 2023)
```

**Key metrics:**
- **cost=0.00..35.00**: Start cost..total cost
- **rows=50**: Estimated rows returned
- **width=200**: Average row size (bytes)
- **Seq Scan**: Full table scan (slow)
- **Index Scan**: Uses index (fast)

---

### 3. Types of Scans

#### **Sequential Scan (Seq Scan)**
- Reads entire table row by row
- Used when no index or index not helpful
- Cost proportional to table size: O(n)

```sql
SELECT * FROM questions WHERE difficulty = 'medium';
-- If no index on difficulty → Seq Scan
```

#### **Index Scan**
- Uses index to find rows
- Faster than Seq Scan
- Cost proportional to log(n)

```sql
CREATE INDEX idx_year ON questions(year);
SELECT * FROM questions WHERE year = 2023;
-- Uses Index Scan
```

#### **Index Only Scan**
- All needed columns in index
- No table lookup needed
- Fastest scan type

```sql
CREATE INDEX idx_cover ON questions(year, marks);
SELECT year, marks FROM questions WHERE year = 2023;
-- Uses Index Only Scan (fastest!)
```

#### **Bitmap Scan**
- Combines multiple indexes
- Used for OR conditions

```sql
SELECT * FROM questions
WHERE year = 2023 OR difficulty = 'hard';
-- May use Bitmap Scan with both indexes
```

---

### 4. Join Algorithms

#### **Nested Loop Join**
- For each row in table A, scan table B
- Cost: O(n * m)
- Good for small tables

```sql
SELECT * FROM courses c
JOIN topics t ON c.course_id = t.course_id;
-- Small tables → Nested Loop Join
```

#### **Hash Join**
- Build hash table on smaller table
- Probe with larger table
- Cost: O(n + m)
- Good for equi-joins (=)

```sql
SELECT * FROM questions q
JOIN courses c ON q.course_id = c.course_id;
-- Large tables + equality → Hash Join
```

#### **Merge Join**
- Both tables sorted on join key
- Merge sorted lists
- Cost: O(n log n + m log m)
- Good when already sorted

---

### 5. Query Optimization Techniques

#### **1. Use Indexes Effectively**
```sql
-- ❌ Bad: Function on indexed column
SELECT * FROM questions WHERE YEAR(created_at) = 2023;

-- ✅ Good: Preserve index usage
SELECT * FROM questions
WHERE created_at >= '2023-01-01' AND created_at < '2024-01-01';
```

#### **2. Avoid SELECT ***
```sql
-- ❌ Bad: Retrieves all columns
SELECT * FROM questions WHERE year = 2023;

-- ✅ Good: Only needed columns
SELECT question_id, question_text FROM questions WHERE year = 2023;
```

#### **3. Use LIMIT for Pagination**
```sql
-- ❌ Bad: Returns all rows
SELECT * FROM questions ORDER BY year DESC;

-- ✅ Good: Limits results
SELECT * FROM questions ORDER BY year DESC LIMIT 10 OFFSET 20;
```

#### **4. Optimize JOINs**
```sql
-- ❌ Bad: Cartesian product then filter
SELECT * FROM courses, topics
WHERE courses.course_id = topics.course_id;

-- ✅ Good: Explicit JOIN
SELECT * FROM courses
INNER JOIN topics ON courses.course_id = topics.course_id;
```

#### **5. Use EXISTS Instead of IN (for large subqueries)**
```sql
-- ❌ Slower: IN with subquery
SELECT * FROM courses
WHERE course_id IN (SELECT course_id FROM questions WHERE year = 2023);

-- ✅ Faster: EXISTS
SELECT * FROM courses c
WHERE EXISTS (
    SELECT 1 FROM questions q
    WHERE q.course_id = c.course_id AND q.year = 2023
);
```

---

### 6. Analyzing Query Performance

#### **EXPLAIN ANALYZE**
Shows actual execution time (not just estimates).

```sql
EXPLAIN ANALYZE
SELECT * FROM questions
WHERE year = 2023 AND difficulty = 'hard';

-- Output:
-- Planning Time: 0.123 ms
-- Execution Time: 1.456 ms
-- Index Scan using idx_questions_year_difficulty
--   (cost=0.15..8.17 rows=5 width=200)
--   (actual time=0.012..0.089 rows=5 loops=1)
```

**Key metrics:**
- **Planning Time**: Time to create plan
- **Execution Time**: Actual query execution
- **actual time**: Real start..end time
- **rows**: Actual rows returned (vs estimated)

---

### 7. Common Performance Issues

#### **Problem 1: Missing Index**
```sql
-- Slow query
SELECT * FROM questions WHERE year = 2023;
-- Shows: Seq Scan (cost=0..1000)

-- Solution: Add index
CREATE INDEX idx_questions_year ON questions(year);
-- Now: Index Scan (cost=0..50)
```

#### **Problem 2: Index Not Used**
```sql
-- Index exists but not used
SELECT * FROM questions WHERE LOWER(difficulty) = 'hard';

-- Solution: Remove function from column
SELECT * FROM questions WHERE difficulty = 'hard';
-- Or create functional index:
CREATE INDEX idx_difficulty_lower ON questions(LOWER(difficulty));
```

#### **Problem 3: Too Many Rows**
```sql
-- Returns millions of rows
SELECT * FROM questions WHERE year >= 2020;

-- Solution: Add LIMIT or more filters
SELECT * FROM questions
WHERE year >= 2020 AND difficulty = 'hard'
LIMIT 100;
```

#### **Problem 4: N+1 Query Problem**
```python
# ❌ Bad: N+1 queries
courses = session.query(Course).all()
for course in courses:
    topics = session.query(Topic).filter(Topic.course_id == course.id).all()
    # 1 query for courses + N queries for topics = N+1 queries

# ✅ Good: Single query with JOIN
courses = session.query(Course).options(joinedload(Course.topics)).all()
# 1 query total (with JOIN)
```

---

### 8. Statistics and Vacuum

**ANALYZE**: Update table statistics for optimizer

```sql
ANALYZE questions;
-- Updates row count, data distribution
-- Helps optimizer make better decisions
```

**VACUUM**: Clean up dead rows

```sql
VACUUM ANALYZE questions;
-- Reclaim storage + update statistics
```

---

## 🎯 CourseDB-AI Query Optimization

### Common Queries to Optimize:

**1. Dashboard: Topic frequency**
```sql
-- Optimized query
SELECT
    topic_name,
    COUNT(*) as question_count,
    AVG(marks) as avg_marks
FROM questions
WHERE year >= 2020
GROUP BY topic_name
HAVING COUNT(*) >= 3
ORDER BY question_count DESC
LIMIT 10;

-- Needs: index on (year, topic_name) or (year) + (topic_name)
```

**2. Search: Questions by filters**
```sql
-- Optimized query
SELECT question_id, question_text, year, difficulty
FROM questions
WHERE year BETWEEN 2020 AND 2023
  AND difficulty = 'hard'
  AND topic_id = 5
ORDER BY year DESC
LIMIT 20;

-- Needs: composite index on (topic_id, year, difficulty)
```

---

## ✅ Self-Check Questions

1. What's the difference between EXPLAIN and EXPLAIN ANALYZE?
2. Which is faster: Seq Scan or Index Scan?
3. When would you use Hash Join vs Nested Loop Join?
4. Why is SELECT * bad for performance?
5. What's the N+1 query problem?
6. When does the optimizer choose NOT to use an index?
7. What does VACUUM do?
8. How do you optimize a slow JOIN query?

---

## 🔬 Performance Testing Exercise

```sql
-- 1. Create test table with 100k rows
CREATE TABLE test_questions AS
SELECT
    id,
    'Question ' || id as question_text,
    2000 + (id % 25) as year,
    CASE (id % 3)
        WHEN 0 THEN 'easy'
        WHEN 1 THEN 'medium'
        ELSE 'hard'
    END as difficulty
FROM generate_series(1, 100000) as id;

-- 2. Test without index
EXPLAIN ANALYZE SELECT * FROM test_questions WHERE year = 2023;

-- 3. Add index
CREATE INDEX idx_test_year ON test_questions(year);

-- 4. Test with index
EXPLAIN ANALYZE SELECT * FROM test_questions WHERE year = 2023;

-- 5. Compare results
```

---

**Next Week (Week 9):** Transactions, ACID, and concurrency control!

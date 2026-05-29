# Week 6: Advanced SQL - Theory Notes

## 📚 Core Concepts

### 1. JOINs in SQL

**JOIN**: Combine rows from two or more tables based on a related column.

#### **INNER JOIN**
Returns only matching rows from both tables.

```sql
SELECT s.name, c.course_title
FROM students s
INNER JOIN enrollments e ON s.student_id = e.student_id
INNER JOIN courses c ON e.course_id = c.course_id;
```

#### **LEFT JOIN (LEFT OUTER JOIN)**
Returns all rows from left table, matching rows from right table (NULL if no match).

```sql
SELECT c.course_code, COUNT(q.question_id) as question_count
FROM courses c
LEFT JOIN questions q ON c.course_id = q.course_id
GROUP BY c.course_code;
```

Use case: Find courses with zero questions.

#### **RIGHT JOIN**
Returns all rows from right table, matching rows from left table.

#### **FULL OUTER JOIN**
Returns all rows from both tables, with NULLs where no match.

---

### 2. Subqueries

**Subquery**: Query nested inside another query.

#### **WHERE Subquery**
```sql
-- Find questions harder than average marks
SELECT question_text, marks
FROM questions
WHERE marks > (SELECT AVG(marks) FROM questions);
```

#### **FROM Subquery (Derived Table)**
```sql
-- Find topics with most questions
SELECT topic_stats.*
FROM (
    SELECT topic_name, COUNT(*) as q_count
    FROM questions
    GROUP BY topic_name
) as topic_stats
WHERE topic_stats.q_count > 5;
```

#### **IN Subquery**
```sql
-- Find students enrolled in CS courses
SELECT name FROM students
WHERE student_id IN (
    SELECT student_id FROM enrollments
    WHERE course_id IN (
        SELECT course_id FROM courses
        WHERE course_code LIKE 'CS%'
    )
);
```

---

### 3. Views

**View**: Virtual table based on a query.

```sql
-- Create view
CREATE VIEW hard_questions AS
SELECT question_id, question_text, year
FROM questions
WHERE difficulty = 'hard';

-- Use view like a table
SELECT * FROM hard_questions WHERE year = 2023;
```

**Benefits:**
- Simplify complex queries
- Security (hide sensitive columns)
- Abstraction layer

---

### 4. CTEs (Common Table Expressions)

**CTE**: Named temporary result set (WITH clause).

```sql
WITH topic_counts AS (
    SELECT topic_name, COUNT(*) as count
    FROM questions
    GROUP BY topic_name
)
SELECT topic_name, count
FROM topic_counts
WHERE count > 5
ORDER BY count DESC;
```

**Recursive CTE:**
```sql
-- Generate series
WITH RECURSIVE numbers AS (
    SELECT 1 as n
    UNION ALL
    SELECT n + 1 FROM numbers WHERE n < 10
)
SELECT * FROM numbers;
```

---

### 5. Window Functions

**Window Function**: Perform calculation across a set of rows related to current row.

#### **ROW_NUMBER()**
```sql
SELECT
    question_text,
    year,
    ROW_NUMBER() OVER (PARTITION BY year ORDER BY marks DESC) as rank
FROM questions;
```

#### **RANK() and DENSE_RANK()**
```sql
-- Find top 3 questions per year by marks
SELECT * FROM (
    SELECT
        question_text,
        year,
        marks,
        RANK() OVER (PARTITION BY year ORDER BY marks DESC) as rank
    FROM questions
) ranked
WHERE rank <= 3;
```

#### **LAG() and LEAD()**
```sql
-- Compare with previous year
SELECT
    year,
    COUNT(*) as question_count,
    LAG(COUNT(*)) OVER (ORDER BY year) as prev_year_count
FROM questions
GROUP BY year;
```

---

### 6. Aggregate Window Functions

```sql
SELECT
    question_id,
    marks,
    AVG(marks) OVER (PARTITION BY difficulty) as avg_marks_by_difficulty,
    SUM(marks) OVER (ORDER BY year) as cumulative_marks
FROM questions;
```

---

### 7. Transactions

**Transaction**: Group of SQL statements executed as a single unit.

**ACID Properties:**
- **Atomicity**: All or nothing
- **Consistency**: Database remains in valid state
- **Isolation**: Concurrent transactions don't interfere
- **Durability**: Committed changes persist

```sql
BEGIN TRANSACTION;

INSERT INTO courses (course_code, course_title, credit)
VALUES ('CS301', 'Advanced DBMS', 3);

INSERT INTO topics (course_id, topic_name, week_number)
VALUES (LASTVAL(), 'Query Optimization', 1);

COMMIT;  -- Or ROLLBACK if error
```

---

### 8. Indexes

**Index**: Data structure to speed up queries.

```sql
-- Create index
CREATE INDEX idx_questions_year ON questions(year);

-- Composite index
CREATE INDEX idx_questions_year_difficulty
ON questions(year, difficulty);

-- Unique index
CREATE UNIQUE INDEX idx_courses_code ON courses(course_code);
```

**When to use:**
- Columns frequently used in WHERE
- Columns in JOIN conditions
- Columns in ORDER BY

**Trade-offs:**
- Faster SELECT
- Slower INSERT/UPDATE/DELETE
- Extra storage space

---

### 9. Constraints

```sql
-- Primary Key
ALTER TABLE students ADD PRIMARY KEY (student_id);

-- Foreign Key
ALTER TABLE questions
ADD CONSTRAINT fk_course
FOREIGN KEY (course_id) REFERENCES courses(course_id);

-- CHECK constraint
ALTER TABLE questions
ADD CONSTRAINT chk_marks
CHECK (marks > 0 AND marks <= 100);

-- UNIQUE constraint
ALTER TABLE users ADD UNIQUE (email);

-- NOT NULL constraint
ALTER TABLE courses ALTER COLUMN course_title SET NOT NULL;
```

---

### 10. Triggers

**Trigger**: Automatically execute function when event occurs.

```sql
-- Create function
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger
CREATE TRIGGER questions_update_timestamp
BEFORE UPDATE ON questions
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();
```

---

## 🎯 CourseDB-AI Week 6 Implementation

### What to Build:

1. **CRUD Endpoints**
   - GET /api/courses (list)
   - GET /api/courses/{id} (detail)
   - POST /api/courses (create)
   - PUT /api/courses/{id} (update)
   - DELETE /api/courses/{id} (delete)

2. **Complex Queries**
   - Analytics endpoints using JOINs
   - Aggregations with GROUP BY
   - Filtering with subqueries

3. **Views**
   - Create views for common queries
   - Simplify frontend queries

---

## ✅ Self-Check Questions

1. What's the difference between INNER JOIN and LEFT JOIN?
2. When would you use a subquery vs a JOIN?
3. What's the difference between WHERE and HAVING?
4. What's a view and when should you use one?
5. What's the difference between RANK() and ROW_NUMBER()?
6. What are ACID properties?
7. When should you create an index?
8. What's the difference between a view and a CTE?

---

**Practice:** Implement the courses CRUD API using the theory from this week!

# Week 6: Advanced SQL (Views, Triggers, Constraints, Stored Procedures)

**Duration**: 7 days
**Status**: 🔄 Ready to Start

---

## 🎯 Why This Week Matters

You've built a functional FastAPI backend in Week 5. Now it's time to level up your SQL skills with **advanced database features** that make your application more powerful, maintainable, and efficient.

Week 6 teaches you to:
- Create **views** for complex queries
- Write **triggers** for automated database actions
- Implement **constraints** for data integrity
- Build **stored procedures** for business logic
- Use **CTEs** and **window functions** for advanced queries
- Optimize with **materialized views**

**Why these features matter:**
- **Views**: Simplify complex queries, provide security, abstract complexity
- **Triggers**: Automate auditing, enforce business rules, maintain data consistency
- **Constraints**: Prevent invalid data at database level (stronger than app validation)
- **Stored Procedures**: Encapsulate business logic, reduce network traffic, improve security
- **Advanced SQL**: Handle complex analytical queries efficiently

**Real-world impact:**
- Banking systems use triggers for audit trails
- E-commerce platforms use views for reporting dashboards
- SaaS applications use constraints to enforce multi-tenancy
- Data warehouses use CTEs and window functions for analytics

---

## 📚 Learning Objectives

By the end of this week, you will be able to:

✅ Create and manage database views (simple and complex)
✅ Implement materialized views for performance
✅ Write triggers for BEFORE and AFTER events
✅ Use triggers for auditing and data validation
✅ Define CHECK constraints for business rules
✅ Implement custom constraints with triggers
✅ Create stored procedures with parameters
✅ Use Common Table Expressions (CTEs)
✅ Apply window functions (ROW_NUMBER, RANK, LAG/LEAD)
✅ Build recursive queries
✅ Understand when to use each feature

---

## 📖 Concepts to Learn

### **1. Database Views**

**What is a View?**
A virtual table based on a SQL query. Views don't store data - they're saved queries.

**Simple View:**
```sql
CREATE VIEW course_summary AS
SELECT
    c.course_id,
    c.course_code,
    c.title,
    COUNT(q.question_id) as question_count
FROM courses c
LEFT JOIN questions q ON c.course_id = q.course_id
GROUP BY c.course_id, c.course_code, c.title;

-- Use like a table
SELECT * FROM course_summary WHERE question_count > 10;
```

**Benefits:**
- Simplify complex queries
- Provide security (hide sensitive columns)
- Abstract database structure
- Reusable query logic

**Updatable Views:**
```sql
-- Simple views CAN be updated
CREATE VIEW active_courses AS
SELECT * FROM courses WHERE status = 'active';

-- This works!
UPDATE active_courses SET credits = 4 WHERE course_id = 1;
```

**Complex Views (NOT updatable):**
```sql
-- Joins, aggregations = not updatable
CREATE VIEW course_stats AS
SELECT c.*, COUNT(q.question_id) as q_count
FROM courses c LEFT JOIN questions q ON c.course_id = q.course_id
GROUP BY c.course_id;

-- This fails!
-- UPDATE course_stats SET q_count = 10 WHERE course_id = 1;
```

### **2. Materialized Views**

**What's the difference?**
- **View**: Query executed every time (always current, but slow for complex queries)
- **Materialized View**: Query results stored (fast, but needs refresh)

**PostgreSQL Materialized View:**
```sql
CREATE MATERIALIZED VIEW course_analytics AS
SELECT
    c.course_code,
    c.title,
    COUNT(DISTINCT t.topic_id) as topic_count,
    COUNT(DISTINCT q.question_id) as question_count,
    AVG(q.marks) as avg_marks
FROM courses c
LEFT JOIN topics t ON c.course_id = t.course_id
LEFT JOIN questions q ON c.course_id = q.course_id
GROUP BY c.course_id, c.course_code, c.title;

-- Refresh when data changes
REFRESH MATERIALIZED VIEW course_analytics;

-- Concurrent refresh (doesn't lock)
REFRESH MATERIALIZED VIEW CONCURRENTLY course_analytics;
```

**When to use:**
- Expensive queries that don't need real-time data
- Reporting dashboards
- Analytics queries
- Data that changes infrequently

### **3. Database Triggers**

**What is a Trigger?**
Automatic action executed when specific database event occurs.

**Trigger Types:**
- **BEFORE**: Executes before INSERT/UPDATE/DELETE
- **AFTER**: Executes after INSERT/UPDATE/DELETE
- **INSTEAD OF**: For views (replaces the action)

**Basic Trigger:**
```sql
-- Audit table
CREATE TABLE question_audit (
    audit_id SERIAL PRIMARY KEY,
    question_id INTEGER,
    action VARCHAR(10),
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    changed_by VARCHAR(100)
);

-- Trigger function
CREATE OR REPLACE FUNCTION audit_question_changes()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO question_audit (question_id, action)
        VALUES (NEW.question_id, 'INSERT');
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO question_audit (question_id, action)
        VALUES (NEW.question_id, 'UPDATE');
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO question_audit (question_id, action)
        VALUES (OLD.question_id, 'DELETE');
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger
CREATE TRIGGER question_audit_trigger
AFTER INSERT OR UPDATE OR DELETE ON questions
FOR EACH ROW
EXECUTE FUNCTION audit_question_changes();
```

**Trigger Use Cases:**
- **Auditing**: Track who changed what and when
- **Validation**: Enforce complex business rules
- **Denormalization**: Update computed columns
- **Cascading**: Custom cascade behavior
- **Notifications**: Log or notify on changes

**BEFORE vs AFTER:**
```sql
-- BEFORE: Can modify NEW values
CREATE TRIGGER update_modified_timestamp
BEFORE UPDATE ON courses
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();

-- AFTER: Cannot modify, used for logging
CREATE TRIGGER log_course_changes
AFTER UPDATE ON courses
FOR EACH ROW
EXECUTE FUNCTION log_changes();
```

### **4. Constraints**

**CHECK Constraints:**
```sql
CREATE TABLE questions (
    question_id SERIAL PRIMARY KEY,
    question_text TEXT NOT NULL,
    difficulty VARCHAR(20) CHECK (difficulty IN ('easy', 'medium', 'hard')),
    marks INTEGER CHECK (marks BETWEEN 1 AND 100),
    year INTEGER CHECK (year >= 2000 AND year <= EXTRACT(YEAR FROM CURRENT_DATE))
);
```

**Named Constraints:**
```sql
ALTER TABLE questions
ADD CONSTRAINT valid_difficulty
CHECK (difficulty IN ('easy', 'medium', 'hard'));

-- Can drop by name
ALTER TABLE questions
DROP CONSTRAINT valid_difficulty;
```

**Table-level Constraints:**
```sql
CREATE TABLE enrollments (
    student_id INTEGER,
    course_id INTEGER,
    semester VARCHAR(10),
    grade VARCHAR(2),
    PRIMARY KEY (student_id, course_id, semester),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    CHECK (grade IN ('A', 'B', 'C', 'D', 'F', NULL))  -- NULL = in progress
);
```

**UNIQUE Constraints:**
```sql
-- Single column
ALTER TABLE courses ADD CONSTRAINT unique_course_code UNIQUE (course_code);

-- Multiple columns (composite unique)
ALTER TABLE topics ADD CONSTRAINT unique_topic_per_course
UNIQUE (course_id, topic_name);
```

### **5. Stored Procedures and Functions**

**Function (returns value):**
```sql
CREATE OR REPLACE FUNCTION get_course_question_count(p_course_id INTEGER)
RETURNS INTEGER AS $$
DECLARE
    question_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO question_count
    FROM questions
    WHERE course_id = p_course_id;

    RETURN question_count;
END;
$$ LANGUAGE plpgsql;

-- Usage
SELECT course_code, get_course_question_count(course_id)
FROM courses;
```

**Procedure (performs action):**
```sql
CREATE OR REPLACE PROCEDURE update_question_difficulty(
    p_question_id INTEGER,
    p_new_difficulty VARCHAR(20)
)
LANGUAGE plpgsql AS $$
BEGIN
    -- Validate difficulty
    IF p_new_difficulty NOT IN ('easy', 'medium', 'hard') THEN
        RAISE EXCEPTION 'Invalid difficulty: %', p_new_difficulty;
    END IF;

    -- Update
    UPDATE questions
    SET difficulty = p_new_difficulty
    WHERE question_id = p_question_id;

    -- Log change
    INSERT INTO change_log (table_name, record_id, action)
    VALUES ('questions', p_question_id, 'difficulty_update');
END;
$$;

-- Usage
CALL update_question_difficulty(1, 'hard');
```

**Functions with Return Tables:**
```sql
CREATE OR REPLACE FUNCTION get_course_topics(p_course_id INTEGER)
RETURNS TABLE (
    topic_id INTEGER,
    topic_name VARCHAR(255),
    question_count BIGINT
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        t.topic_id,
        t.topic_name,
        COUNT(q.question_id) as question_count
    FROM topics t
    LEFT JOIN questions q ON t.topic_id = q.topic_id
    WHERE t.course_id = p_course_id
    GROUP BY t.topic_id, t.topic_name;
END;
$$ LANGUAGE plpgsql;

-- Usage
SELECT * FROM get_course_topics(1);
```

### **6. Common Table Expressions (CTEs)**

**Basic CTE:**
```sql
WITH course_stats AS (
    SELECT
        course_id,
        COUNT(*) as question_count,
        AVG(marks) as avg_marks
    FROM questions
    GROUP BY course_id
)
SELECT
    c.course_code,
    c.title,
    cs.question_count,
    cs.avg_marks
FROM courses c
JOIN course_stats cs ON c.course_id = cs.course_id
WHERE cs.question_count > 10;
```

**Multiple CTEs:**
```sql
WITH easy_questions AS (
    SELECT course_id, COUNT(*) as easy_count
    FROM questions
    WHERE difficulty = 'easy'
    GROUP BY course_id
),
hard_questions AS (
    SELECT course_id, COUNT(*) as hard_count
    FROM questions
    WHERE difficulty = 'hard'
    GROUP BY course_id
)
SELECT
    c.title,
    COALESCE(e.easy_count, 0) as easy_count,
    COALESCE(h.hard_count, 0) as hard_count
FROM courses c
LEFT JOIN easy_questions e ON c.course_id = e.course_id
LEFT JOIN hard_questions h ON c.course_id = h.course_id;
```

**Recursive CTE:**
```sql
-- Prerequisite chain example
WITH RECURSIVE prerequisite_chain AS (
    -- Base case
    SELECT course_id, title, prerequisite_id, 1 as level
    FROM courses
    WHERE course_id = 5  -- Starting course

    UNION ALL

    -- Recursive case
    SELECT c.course_id, c.title, c.prerequisite_id, pc.level + 1
    FROM courses c
    JOIN prerequisite_chain pc ON c.course_id = pc.prerequisite_id
)
SELECT * FROM prerequisite_chain;
```

### **7. Window Functions**

**ROW_NUMBER():**
```sql
SELECT
    question_id,
    course_id,
    marks,
    ROW_NUMBER() OVER (PARTITION BY course_id ORDER BY marks DESC) as rank_in_course
FROM questions;
```

**RANK() and DENSE_RANK():**
```sql
SELECT
    course_code,
    question_count,
    RANK() OVER (ORDER BY question_count DESC) as rank,
    DENSE_RANK() OVER (ORDER BY question_count DESC) as dense_rank
FROM (
    SELECT c.course_code, COUNT(q.question_id) as question_count
    FROM courses c
    LEFT JOIN questions q ON c.course_id = q.course_id
    GROUP BY c.course_code
) stats;
```

**LAG() and LEAD():**
```sql
-- Compare with previous/next row
SELECT
    year,
    COUNT(*) as question_count,
    LAG(COUNT(*)) OVER (ORDER BY year) as prev_year_count,
    LEAD(COUNT(*)) OVER (ORDER BY year) as next_year_count
FROM questions
GROUP BY year
ORDER BY year;
```

**Running Totals:**
```sql
SELECT
    course_id,
    question_id,
    marks,
    SUM(marks) OVER (PARTITION BY course_id ORDER BY question_id) as running_total
FROM questions;
```

---

## 🛠️ This Week's Exercises

### **Exercise 1: Create Views**
- Simple view for active courses
- Complex view with joins and aggregations
- Updatable view for course management

### **Exercise 2: Implement Triggers**
- Audit trigger for question changes
- Validation trigger for data integrity
- Cascade trigger for computed columns

### **Exercise 3: Add Constraints**
- CHECK constraints for business rules
- UNIQUE constraints for data integrity
- Custom constraints with triggers

### **Exercise 4: Build Stored Procedures**
- Function to calculate course statistics
- Procedure to archive old questions
- Function returning table of results

### **Exercise 5: Advanced Queries**
- CTE for complex reporting
- Recursive CTE for hierarchies
- Window functions for analytics

---

## 📦 Deliverables

By the end of Week 6, you should have:

1. **5+ Database Views** for CourseDB-AI
2. **3+ Triggers** for auditing and validation
3. **10+ Constraints** enforcing business rules
4. **5+ Stored Procedures/Functions**
5. **Advanced SQL Queries** using CTEs and window functions
6. **Documentation** of all database objects

---

## ✅ Self-Check Quiz

1. **What's the difference between a view and a materialized view?**
2. **When should you use BEFORE vs AFTER triggers?**
3. **What's the difference between RANK() and DENSE_RANK()?**
4. **How do you create a recursive CTE?**
5. **What are the benefits of stored procedures?**
6. **How do CHECK constraints differ from application validation?**
7. **Can you update a view with JOIN and GROUP BY?**
8. **What is OLD and NEW in trigger functions?**
9. **How do you refresh a materialized view?**
10. **When should you use window functions vs GROUP BY?**

---

## 🚀 Connection to CourseDB-AI

Week 6 enhances your CourseDB-AI backend with:
- **Analytics views** for dashboard metrics
- **Audit triggers** to track all data changes
- **Data validation** at database level
- **Reporting functions** for complex queries
- **Performance optimization** with materialized views

---

**Next Week**: Week 7 - Indexing (B+ Tree, Hash Index) - Optimize query performance!

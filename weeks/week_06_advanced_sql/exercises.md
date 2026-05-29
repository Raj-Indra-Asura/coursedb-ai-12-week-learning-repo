# Week 6: Advanced SQL Exercises

## 🎯 Exercise Goals

Practice advanced SQL features: views, triggers, constraints, stored procedures, CTEs, and window functions.

---

## Exercise Set 1: Database Views

### Exercise 1.1: Simple View

**Create a view for active courses with question count:**
```sql
CREATE VIEW active_courses_with_questions AS
SELECT
    c.course_id,
    c.course_code,
    c.title,
    c.credits,
    COUNT(q.question_id) as question_count
FROM courses c
LEFT JOIN questions q ON c.course_id = q.course_id
GROUP BY c.course_id, c.course_code, c.title, c.credits;
```

**Test:**
```sql
SELECT * FROM active_courses_with_questions;
SELECT * FROM active_courses_with_questions WHERE question_count > 10;
```

### Exercise 1.2: Complex View with Multiple Joins

**Create comprehensive course analytics view:**
```sql
CREATE VIEW course_analytics AS
SELECT
    c.course_id,
    c.course_code,
    c.title,
    COUNT(DISTINCT t.topic_id) as topic_count,
    COUNT(DISTINCT q.question_id) as question_count,
    COUNT(DISTINCT CASE WHEN q.difficulty = 'easy' THEN q.question_id END) as easy_count,
    COUNT(DISTINCT CASE WHEN q.difficulty = 'medium' THEN q.question_id END) as medium_count,
    COUNT(DISTINCT CASE WHEN q.difficulty = 'hard' THEN q.question_id END) as hard_count,
    ROUND(AVG(q.marks), 2) as avg_marks
FROM courses c
LEFT JOIN topics t ON c.course_id = t.course_id
LEFT JOIN questions q ON c.course_id = q.course_id
GROUP BY c.course_id, c.course_code, c.title;
```

### Exercise 1.3: Materialized View

**Create materialized view for expensive queries:**
```sql
CREATE MATERIALIZED VIEW course_performance_stats AS
SELECT
    c.course_code,
    c.title,
    COUNT(DISTINCT q.question_id) as total_questions,
    ROUND(AVG(q.marks), 2) as avg_marks,
    MAX(q.year) as latest_year,
    MIN(q.year) as oldest_year
FROM courses c
JOIN questions q ON c.course_id = q.course_id
GROUP BY c.course_id, c.course_code, c.title;

-- Create unique index for concurrent refresh
CREATE UNIQUE INDEX ON course_performance_stats (course_code);

-- Refresh
REFRESH MATERIALIZED VIEW course_performance_stats;
REFRESH MATERIALIZED VIEW CONCURRENTLY course_performance_stats;
```

---

## Exercise Set 2: Database Triggers

### Exercise 2.1: Audit Trigger

**Step 1: Create audit table:**
```sql
CREATE TABLE audit_log (
    audit_id SERIAL PRIMARY KEY,
    table_name VARCHAR(50),
    record_id INTEGER,
    operation VARCHAR(10),
    old_data JSONB,
    new_data JSONB,
    changed_by VARCHAR(100),
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Step 2: Create trigger function:**
```sql
CREATE OR REPLACE FUNCTION audit_question_changes()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO audit_log (table_name, record_id, operation, new_data)
        VALUES ('questions', NEW.question_id, 'INSERT', row_to_json(NEW)::jsonb);
        RETURN NEW;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO audit_log (table_name, record_id, operation, old_data, new_data)
        VALUES ('questions', NEW.question_id, 'UPDATE',
                row_to_json(OLD)::jsonb, row_to_json(NEW)::jsonb);
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO audit_log (table_name, record_id, operation, old_data)
        VALUES ('questions', OLD.question_id, 'DELETE', row_to_json(OLD)::jsonb);
        RETURN OLD;
    END IF;
END;
$$ LANGUAGE plpgsql;
```

**Step 3: Create trigger:**
```sql
CREATE TRIGGER question_audit_trigger
AFTER INSERT OR UPDATE OR DELETE ON questions
FOR EACH ROW
EXECUTE FUNCTION audit_question_changes();
```

**Test:**
```sql
INSERT INTO questions (course_id, topic_id, question_text, difficulty, marks)
VALUES (1, 1, 'Test question', 'easy', 5);

UPDATE questions SET difficulty = 'medium' WHERE question_id = 1;

DELETE FROM questions WHERE question_id = 1;

-- View audit log
SELECT * FROM audit_log ORDER BY changed_at DESC;
```

### Exercise 2.2: Validation Trigger

**Prevent invalid data at database level:**
```sql
CREATE OR REPLACE FUNCTION validate_question_data()
RETURNS TRIGGER AS $$
BEGIN
    -- Validate marks
    IF NEW.marks < 1 OR NEW.marks > 100 THEN
        RAISE EXCEPTION 'Marks must be between 1 and 100, got %', NEW.marks;
    END IF;

    -- Validate difficulty
    IF NEW.difficulty NOT IN ('easy', 'medium', 'hard') THEN
        RAISE EXCEPTION 'Invalid difficulty: %', NEW.difficulty;
    END IF;

    -- Validate year
    IF NEW.year < 2000 OR NEW.year > EXTRACT(YEAR FROM CURRENT_DATE) + 1 THEN
        RAISE EXCEPTION 'Invalid year: %', NEW.year;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER validate_question_trigger
BEFORE INSERT OR UPDATE ON questions
FOR EACH ROW
EXECUTE FUNCTION validate_question_data();
```

### Exercise 2.3: Automatic Timestamp Update

**Update modified timestamp automatically:**
```sql
ALTER TABLE courses ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_course_timestamp
BEFORE UPDATE ON courses
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();
```

---

## Exercise Set 3: Constraints

### Exercise 3.1: CHECK Constraints

**Add business rule constraints:**
```sql
-- Difficulty constraint
ALTER TABLE questions
ADD CONSTRAINT valid_difficulty
CHECK (difficulty IN ('easy', 'medium', 'hard'));

-- Marks constraint
ALTER TABLE questions
ADD CONSTRAINT valid_marks
CHECK (marks BETWEEN 1 AND 100);

-- Year constraint
ALTER TABLE questions
ADD CONSTRAINT valid_year
CHECK (year >= 2000 AND year <= EXTRACT(YEAR FROM CURRENT_DATE) + 1);

-- Credits constraint
ALTER TABLE courses
ADD CONSTRAINT valid_credits
CHECK (credits BETWEEN 1 AND 10);
```

**Test:**
```sql
-- This should fail
INSERT INTO questions (course_id, topic_id, question_text, difficulty, marks)
VALUES (1, 1, 'Test', 'invalid', 5);

-- This should fail
INSERT INTO questions (course_id, topic_id, question_text, difficulty, marks)
VALUES (1, 1, 'Test', 'easy', 150);
```

### Exercise 3.2: UNIQUE Constraints

**Prevent duplicate data:**
```sql
-- Course code must be unique
ALTER TABLE courses
ADD CONSTRAINT unique_course_code UNIQUE (course_code);

-- Topic name must be unique per course
ALTER TABLE topics
ADD CONSTRAINT unique_topic_per_course UNIQUE (course_id, topic_name);

-- Question text should be unique (optional - depends on requirements)
-- ALTER TABLE questions
-- ADD CONSTRAINT unique_question_text UNIQUE (question_text);
```

### Exercise 3.3: Custom Domain Constraints

**Create custom data types:**
```sql
-- Custom difficulty type
CREATE DOMAIN difficulty_level AS VARCHAR(20)
CHECK (VALUE IN ('easy', 'medium', 'hard'));

-- Custom marks type
CREATE DOMAIN question_marks AS INTEGER
CHECK (VALUE BETWEEN 1 AND 100);

-- Use in table
CREATE TABLE new_questions (
    question_id SERIAL PRIMARY KEY,
    question_text TEXT NOT NULL,
    difficulty difficulty_level,
    marks question_marks
);
```

---

## Exercise Set 4: Stored Procedures and Functions

### Exercise 4.1: Function Returning Single Value

**Calculate course statistics:**
```sql
CREATE OR REPLACE FUNCTION get_course_question_count(p_course_id INTEGER)
RETURNS INTEGER AS $$
DECLARE
    v_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO v_count
    FROM questions
    WHERE course_id = p_course_id;

    RETURN v_count;
END;
$$ LANGUAGE plpgsql;

-- Usage
SELECT course_code, get_course_question_count(course_id) as q_count
FROM courses;
```

### Exercise 4.2: Function Returning Table

**Get course topics with stats:**
```sql
CREATE OR REPLACE FUNCTION get_course_topics_with_stats(p_course_id INTEGER)
RETURNS TABLE (
    topic_id INTEGER,
    topic_name VARCHAR(255),
    question_count BIGINT,
    avg_marks NUMERIC
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        t.topic_id,
        t.topic_name,
        COUNT(q.question_id) as question_count,
        ROUND(AVG(q.marks), 2) as avg_marks
    FROM topics t
    LEFT JOIN questions q ON t.topic_id = q.topic_id
    WHERE t.course_id = p_course_id
    GROUP BY t.topic_id, t.topic_name
    ORDER BY t.order_index;
END;
$$ LANGUAGE plpgsql;

-- Usage
SELECT * FROM get_course_topics_with_stats(1);
```

### Exercise 4.3: Procedure with Business Logic

**Archive old questions:**
```sql
CREATE TABLE archived_questions (
    LIKE questions INCLUDING ALL,
    archived_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE OR REPLACE PROCEDURE archive_old_questions(p_year_threshold INTEGER)
LANGUAGE plpgsql AS $$
DECLARE
    v_count INTEGER;
BEGIN
    -- Move old questions to archive
    INSERT INTO archived_questions
    SELECT *, CURRENT_TIMESTAMP
    FROM questions
    WHERE year < p_year_threshold;

    GET DIAGNOSTICS v_count = ROW_COUNT;

    -- Delete from main table
    DELETE FROM questions WHERE year < p_year_threshold;

    RAISE NOTICE 'Archived % questions older than %', v_count, p_year_threshold;
END;
$$;

-- Usage
CALL archive_old_questions(2015);
```

---

## Exercise Set 5: Common Table Expressions (CTEs)

### Exercise 5.1: Basic CTE

**Course difficulty distribution:**
```sql
WITH difficulty_stats AS (
    SELECT
        course_id,
        difficulty,
        COUNT(*) as count
    FROM questions
    GROUP BY course_id, difficulty
)
SELECT
    c.course_code,
    c.title,
    MAX(CASE WHEN ds.difficulty = 'easy' THEN ds.count ELSE 0 END) as easy_count,
    MAX(CASE WHEN ds.difficulty = 'medium' THEN ds.count ELSE 0 END) as medium_count,
    MAX(CASE WHEN ds.difficulty = 'hard' THEN ds.count ELSE 0 END) as hard_count
FROM courses c
LEFT JOIN difficulty_stats ds ON c.course_id = ds.course_id
GROUP BY c.course_id, c.course_code, c.title;
```

### Exercise 5.2: Multiple CTEs

**Complex reporting query:**
```sql
WITH course_question_counts AS (
    SELECT course_id, COUNT(*) as total_questions
    FROM questions
    GROUP BY course_id
),
course_topic_counts AS (
    SELECT course_id, COUNT(*) as total_topics
    FROM topics
    GROUP BY course_id
),
course_avg_marks AS (
    SELECT course_id, ROUND(AVG(marks), 2) as avg_marks
    FROM questions
    GROUP BY course_id
)
SELECT
    c.course_code,
    c.title,
    COALESCE(cqc.total_questions, 0) as questions,
    COALESCE(ctc.total_topics, 0) as topics,
    COALESCE(cam.avg_marks, 0) as avg_marks
FROM courses c
LEFT JOIN course_question_counts cqc ON c.course_id = cqc.course_id
LEFT JOIN course_topic_counts ctc ON c.course_id = ctc.course_id
LEFT JOIN course_avg_marks cam ON c.course_id = cam.course_id;
```

### Exercise 5.3: Recursive CTE

**Topic hierarchy (if topics have parent_topic_id):**
```sql
-- First add parent_topic_id if not exists
-- ALTER TABLE topics ADD COLUMN parent_topic_id INTEGER REFERENCES topics(topic_id);

WITH RECURSIVE topic_hierarchy AS (
    -- Base case: root topics
    SELECT
        topic_id,
        topic_name,
        parent_topic_id,
        1 as level,
        topic_name::TEXT as path
    FROM topics
    WHERE parent_topic_id IS NULL AND course_id = 1

    UNION ALL

    -- Recursive case: child topics
    SELECT
        t.topic_id,
        t.topic_name,
        t.parent_topic_id,
        th.level + 1,
        th.path || ' > ' || t.topic_name
    FROM topics t
    JOIN topic_hierarchy th ON t.parent_topic_id = th.topic_id
)
SELECT * FROM topic_hierarchy ORDER BY path;
```

---

## Exercise Set 6: Window Functions

### Exercise 6.1: ROW_NUMBER()

**Rank questions by marks within each course:**
```sql
SELECT
    c.course_code,
    q.question_id,
    q.question_text,
    q.marks,
    ROW_NUMBER() OVER (PARTITION BY c.course_id ORDER BY q.marks DESC) as rank_in_course
FROM questions q
JOIN courses c ON q.course_id = c.course_id
ORDER BY c.course_code, rank_in_course;
```

### Exercise 6.2: RANK() and DENSE_RANK()

**Rank courses by question count:**
```sql
WITH course_stats AS (
    SELECT
        c.course_code,
        c.title,
        COUNT(q.question_id) as question_count
    FROM courses c
    LEFT JOIN questions q ON c.course_id = q.course_id
    GROUP BY c.course_id, c.course_code, c.title
)
SELECT
    course_code,
    title,
    question_count,
    RANK() OVER (ORDER BY question_count DESC) as rank,
    DENSE_RANK() OVER (ORDER BY question_count DESC) as dense_rank,
    PERCENT_RANK() OVER (ORDER BY question_count DESC) as percent_rank
FROM course_stats;
```

### Exercise 6.3: LAG() and LEAD()

**Compare year-over-year question counts:**
```sql
WITH yearly_counts AS (
    SELECT
        year,
        COUNT(*) as question_count
    FROM questions
    WHERE year IS NOT NULL
    GROUP BY year
    ORDER BY year
)
SELECT
    year,
    question_count,
    LAG(question_count) OVER (ORDER BY year) as prev_year_count,
    LEAD(question_count) OVER (ORDER BY year) as next_year_count,
    question_count - LAG(question_count) OVER (ORDER BY year) as yoy_change
FROM yearly_counts;
```

### Exercise 6.4: Running Totals

**Cumulative question count:**
```sql
SELECT
    course_id,
    question_id,
    marks,
    SUM(marks) OVER (PARTITION BY course_id ORDER BY question_id) as running_total,
    AVG(marks) OVER (PARTITION BY course_id ORDER BY question_id
                     ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as running_avg
FROM questions;
```

---

## Challenge Problems

### Challenge 1: Build Complete Analytics System

Create views, functions, and CTEs for:
1. Course performance dashboard
2. Question difficulty analysis
3. Topic coverage report
4. Historical trends
5. Instructor dashboard (if you have instructor data)

### Challenge 2: Implement Complete Audit System

1. Audit table for all tables
2. Generic trigger function
3. Triggers on all tables
4. Query interface to view changes
5. Rollback procedure

### Challenge 3: Data Quality Framework

1. Validation triggers for all tables
2. Data quality constraints
3. Automated data cleanup procedures
4. Quality score calculation

---

## Self-Assessment

- [ ] Can create and use views
- [ ] Understand materialized views
- [ ] Can write triggers for auditing
- [ ] Can implement validation triggers
- [ ] Comfortable with CHECK constraints
- [ ] Can write stored procedures
- [ ] Understand CTEs
- [ ] Can use window functions
- [ ] Know when to use each feature

---

**Next:** Move to `implementation_plan.md` for 7-day guided implementation!

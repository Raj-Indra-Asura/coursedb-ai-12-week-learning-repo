# Week 6: Advanced SQL - Common Mistakes and How to Fix Them

## 🎯 Purpose

Week 6 introduces powerful but complex database features. This guide prepares you for common mistakes with:
- Database views (updatable vs non-updatable)
- Triggers (infinite loops, performance)
- Constraints (cascading effects, validation)
- Stored procedures (debugging, transaction management)
- CTEs (recursive termination)
- Window functions (PARTITION BY confusion)

---

## Mistake Category 1: Views and Materialized Views

### Mistake 1.1: Trying to Update Non-Updatable Views

**What happens:**
```sql
CREATE VIEW course_analytics AS
SELECT c.course_code, COUNT(q.question_id) as question_count
FROM courses c
LEFT JOIN questions q ON c.course_id = q.course_id
GROUP BY c.course_code;

-- This fails!
UPDATE course_analytics SET question_count = 100 WHERE course_code = 'CS201';
```

**Error message:**
```
ERROR:  cannot update view "course_analytics"
DETAIL:  Views containing GROUP BY are not automatically updatable.
```

**Why it happens:**
Views with JOINs, GROUP BY, DISTINCT, or aggregations are not updatable because PostgreSQL can't determine how to translate the update back to the underlying tables.

**How to fix:**
```sql
-- Option 1: Update the underlying table directly
UPDATE courses SET title = 'New Title' WHERE course_code = 'CS201';

-- Option 2: Create INSTEAD OF trigger for complex update logic
CREATE OR REPLACE FUNCTION update_course_analytics()
RETURNS TRIGGER AS $$
BEGIN
    -- Custom logic to handle the update
    UPDATE courses SET title = NEW.title WHERE course_code = NEW.course_code;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_course_analytics_trigger
INSTEAD OF UPDATE ON course_analytics
FOR EACH ROW EXECUTE FUNCTION update_course_analytics();

-- Option 3: Use simple view without aggregations
CREATE VIEW simple_courses AS
SELECT course_id, course_code, title FROM courses;

-- This works!
UPDATE simple_courses SET title = 'New Title' WHERE course_id = 1;
```

**How to avoid:**
- Understand which views are updatable (simple SELECT from single table)
- Use views for reading complex data, not updating
- Update underlying tables directly for data changes

---

### Mistake 1.2: Forgetting to Refresh Materialized Views

**What happens:**
```sql
CREATE MATERIALIZED VIEW course_stats AS
SELECT course_code, COUNT(*) as question_count
FROM courses c JOIN questions q ON c.course_id = q.course_id
GROUP BY course_code;

-- Insert new questions
INSERT INTO questions (course_id, topic_id, question_text, difficulty, marks)
VALUES (1, 1, 'New question', 'easy', 5);

-- View still shows old data!
SELECT * FROM course_stats WHERE course_code = 'CS201';
```

**Why it happens:**
Materialized views store query results. They don't automatically update when underlying data changes.

**How to fix:**
```sql
-- Manual refresh
REFRESH MATERIALIZED VIEW course_stats;

-- Or use concurrent refresh (doesn't lock the view)
REFRESH MATERIALIZED VIEW CONCURRENTLY course_stats;

-- Set up periodic refresh (via cron or application scheduler)
-- Example: Refresh every hour in application code
```

**How to avoid:**
- Document refresh requirements clearly
- Set up automated refresh schedules
- Consider using regular views for real-time data
- Use materialized views only when staleness is acceptable

---

### Mistake 1.3: Circular View Dependencies

**What happens:**
```sql
CREATE VIEW view_a AS SELECT * FROM view_b;
CREATE VIEW view_b AS SELECT * FROM view_a;
```

**Error message:**
```
ERROR:  infinite recursion detected in rules for relation "view_a"
```

**How to fix:**
- Design view dependencies as directed acyclic graph (DAG)
- Document view dependencies
- Refactor circular logic into single view or CTE

---

## Mistake Category 2: Triggers

### Mistake 2.1: Infinite Trigger Loops

**What happens:**
```sql
-- Trigger updates the same table it's attached to
CREATE OR REPLACE FUNCTION update_question_stats()
RETURNS TRIGGER AS $$
BEGIN
    -- This causes infinite loop!
    UPDATE questions SET updated_at = CURRENT_TIMESTAMP
    WHERE question_id = NEW.question_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER question_update_trigger
AFTER UPDATE ON questions
FOR EACH ROW EXECUTE FUNCTION update_question_stats();
```

**Why it happens:**
AFTER UPDATE trigger on `questions` table updates `questions` table, which fires the trigger again, creating infinite recursion.

**How to fix:**
```sql
-- Option 1: Use BEFORE trigger and modify NEW
CREATE OR REPLACE FUNCTION update_question_stats()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER question_update_trigger
BEFORE UPDATE ON questions
FOR EACH ROW EXECUTE FUNCTION update_question_stats();

-- Option 2: Update different table
CREATE OR REPLACE FUNCTION log_question_update()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO question_update_log (question_id, updated_at)
    VALUES (NEW.question_id, CURRENT_TIMESTAMP);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Option 3: Add condition to prevent recursion
CREATE OR REPLACE FUNCTION smart_update()
RETURNS TRIGGER AS $$
BEGIN
    IF OLD.some_field != NEW.some_field THEN
        -- Only update if specific field changed
        NEW.updated_at = CURRENT_TIMESTAMP;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

**How to avoid:**
- Use BEFORE triggers when modifying the same row
- Never UPDATE the same table in AFTER trigger
- Add conditions to prevent unnecessary trigger execution
- Test triggers with multiple updates

---

### Mistake 2.2: Trigger Not Returning Correct Value

**What happens:**
```sql
CREATE OR REPLACE FUNCTION validate_marks()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.marks < 1 OR NEW.marks > 100 THEN
        RAISE EXCEPTION 'Invalid marks';
    END IF;
    -- Forgot RETURN NEW!
END;
$$ LANGUAGE plpgsql;
```

**Error message:**
```
ERROR:  control reached end of trigger procedure without RETURN
```

**Why it happens:**
BEFORE triggers must return NEW (for INSERT/UPDATE) or OLD (for DELETE). Forgetting to return causes error.

**How to fix:**
```sql
CREATE OR REPLACE FUNCTION validate_marks()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.marks < 1 OR NEW.marks > 100 THEN
        RAISE EXCEPTION 'Invalid marks: %', NEW.marks;
    END IF;
    RETURN NEW;  -- Always return!
END;
$$ LANGUAGE plpgsql;

-- For DELETE triggers
CREATE OR REPLACE FUNCTION log_deletion()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO deletion_log (table_name, record_id)
    VALUES (TG_TABLE_NAME, OLD.question_id);
    RETURN OLD;  -- Return OLD for DELETE
END;
$$ LANGUAGE plpgsql;
```

**How to avoid:**
- Always end BEFORE trigger with `RETURN NEW` or `RETURN OLD`
- Use AFTER triggers when you don't need to modify data (return value doesn't matter)
- Test triggers immediately after creation

---

### Mistake 2.3: Using NEW in DELETE Trigger

**What happens:**
```sql
CREATE OR REPLACE FUNCTION audit_deletion()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO audit_log (record_id, action)
    VALUES (NEW.question_id, 'DELETE');  -- NEW doesn't exist in DELETE!
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;
```

**Error message:**
```
ERROR:  record "new" is not assigned yet
```

**Why it happens:**
In DELETE triggers, the row is being removed, so there's no NEW record. Use OLD instead.

**How to fix:**
```sql
CREATE OR REPLACE FUNCTION audit_deletion()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'DELETE' THEN
        INSERT INTO audit_log (record_id, action, old_data)
        VALUES (OLD.question_id, 'DELETE', row_to_json(OLD)::jsonb);
        RETURN OLD;
    ELSIF TG_OP = 'INSERT' THEN
        INSERT INTO audit_log (record_id, action, new_data)
        VALUES (NEW.question_id, 'INSERT', row_to_json(NEW)::jsonb);
        RETURN NEW;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO audit_log (record_id, action, old_data, new_data)
        VALUES (NEW.question_id, 'UPDATE', row_to_json(OLD)::jsonb, row_to_json(NEW)::jsonb);
        RETURN NEW;
    END IF;
END;
$$ LANGUAGE plpgsql;
```

**Remember:**
- INSERT: Only NEW exists
- UPDATE: Both OLD and NEW exist
- DELETE: Only OLD exists

---

### Mistake 2.4: Trigger Performance Issues

**What happens:**
```sql
-- Slow trigger on high-traffic table
CREATE OR REPLACE FUNCTION expensive_audit()
RETURNS TRIGGER AS $$
BEGIN
    -- Complex aggregation on every insert!
    INSERT INTO audit_log (stats)
    SELECT COUNT(*) FROM questions;  -- Scans entire table
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER expensive_trigger
AFTER INSERT ON questions
FOR EACH ROW EXECUTE FUNCTION expensive_audit();
```

**Why it's bad:**
Every INSERT on questions table now requires scanning the entire questions table for COUNT(*), making inserts 100x slower.

**How to fix:**
```sql
-- Option 1: Asynchronous processing (log to queue, process later)
CREATE OR REPLACE FUNCTION lightweight_audit()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO audit_queue (record_id, action, queued_at)
    VALUES (NEW.question_id, TG_OP, CURRENT_TIMESTAMP);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Option 2: Conditional execution (only for important records)
CREATE OR REPLACE FUNCTION conditional_audit()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.marks > 50 THEN  -- Only audit high-value questions
        INSERT INTO audit_log (record_id, action)
        VALUES (NEW.question_id, TG_OP);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Option 3: Batch processing (use STATEMENT-level trigger)
CREATE TRIGGER batch_audit_trigger
AFTER INSERT ON questions
FOR EACH STATEMENT  -- Fires once per statement, not per row
EXECUTE FUNCTION batch_audit();
```

**How to avoid:**
- Keep triggers lightweight
- Avoid complex queries in triggers
- Use FOR EACH STATEMENT when possible
- Consider application-level processing for complex logic
- Profile trigger performance

---

## Mistake Category 3: Constraints

### Mistake 3.1: Adding Constraint to Existing Invalid Data

**What happens:**
```sql
-- Table has existing data with marks = 150
ALTER TABLE questions
ADD CONSTRAINT valid_marks CHECK (marks BETWEEN 1 AND 100);
```

**Error message:**
```
ERROR:  check constraint "valid_marks" is violated by some row
```

**Why it happens:**
PostgreSQL validates ALL existing data when adding constraint. If any row violates constraint, the ALTER TABLE fails.

**How to fix:**
```sql
-- Option 1: Clean data first
UPDATE questions SET marks = 100 WHERE marks > 100;
UPDATE questions SET marks = 1 WHERE marks < 1;

-- Then add constraint
ALTER TABLE questions
ADD CONSTRAINT valid_marks CHECK (marks BETWEEN 1 AND 100);

-- Option 2: Find violating rows first
SELECT * FROM questions WHERE marks NOT BETWEEN 1 AND 100;

-- Option 3: Add constraint as NOT VALID (doesn't check existing data)
ALTER TABLE questions
ADD CONSTRAINT valid_marks CHECK (marks BETWEEN 1 AND 100) NOT VALID;

-- Then validate in separate transaction (can be done during low traffic)
ALTER TABLE questions VALIDATE CONSTRAINT valid_marks;
```

**How to avoid:**
- Add constraints early in development
- Clean data before adding constraints
- Use NOT VALID for large production tables
- Write migration scripts that fix data before adding constraints

---

### Mistake 3.2: Constraint Naming Conflicts

**What happens:**
```sql
ALTER TABLE questions ADD CHECK (marks > 0);
ALTER TABLE questions ADD CHECK (marks < 100);
```

**Result:**
Constraints get auto-generated names like `questions_check`, `questions_check1`, making them hard to manage.

**How to fix:**
```sql
-- Always name constraints
ALTER TABLE questions
ADD CONSTRAINT valid_marks_minimum CHECK (marks > 0);

ALTER TABLE questions
ADD CONSTRAINT valid_marks_maximum CHECK (marks < 100);

-- Drop by name
ALTER TABLE questions DROP CONSTRAINT valid_marks_minimum;

-- Or combine into single constraint
ALTER TABLE questions
ADD CONSTRAINT valid_marks CHECK (marks BETWEEN 1 AND 100);
```

**How to avoid:**
- Always use descriptive constraint names
- Follow naming convention: `{table}_{column}_{type}`
- Example: `questions_marks_check`, `courses_code_unique`

---

### Mistake 3.3: CHECK Constraint with Subquery

**What happens:**
```sql
-- Trying to validate against other rows
ALTER TABLE questions
ADD CONSTRAINT unique_difficulty_per_course
CHECK ((SELECT COUNT(*) FROM questions WHERE course_id = questions.course_id) > 0);
```

**Error message:**
```
ERROR:  cannot use subquery in check constraint
```

**Why it happens:**
CHECK constraints can only reference the current row. They can't query other rows.

**How to fix:**
```sql
-- Option 1: Use trigger for complex validation
CREATE OR REPLACE FUNCTION validate_course_questions()
RETURNS TRIGGER AS $$
DECLARE
    v_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO v_count
    FROM questions
    WHERE course_id = NEW.course_id;

    IF v_count > 100 THEN
        RAISE EXCEPTION 'Course % already has % questions (max 100)',
            NEW.course_id, v_count;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER validate_question_count
BEFORE INSERT ON questions
FOR EACH ROW EXECUTE FUNCTION validate_course_questions();

-- Option 2: Use unique index for uniqueness across rows
CREATE UNIQUE INDEX unique_question_text_per_course
ON questions(course_id, MD5(question_text));

-- Option 3: Use exclusion constraint (PostgreSQL advanced feature)
CREATE EXTENSION IF NOT EXISTS btree_gist;
ALTER TABLE questions
ADD CONSTRAINT no_overlapping_dates
EXCLUDE USING gist (course_id WITH =, year WITH &&);
```

**How to avoid:**
- Use CHECK constraints for single-row validation only
- Use triggers for multi-row validation
- Use unique indexes/constraints for cross-row uniqueness

---

## Mistake Category 4: Stored Procedures and Functions

### Mistake 4.1: Function vs Procedure Confusion

**What happens:**
```sql
-- Creating function but trying to use COMMIT (only in procedures)
CREATE OR REPLACE FUNCTION archive_questions(p_year INTEGER)
RETURNS INTEGER AS $$
BEGIN
    DELETE FROM questions WHERE year < p_year;
    COMMIT;  -- ERROR! Functions can't control transactions
    RETURN 1;
END;
$$ LANGUAGE plpgsql;
```

**Error message:**
```
ERROR:  cannot commit while a subtransaction is active
```

**How to fix:**
```sql
-- Use PROCEDURE for transaction control
CREATE OR REPLACE PROCEDURE archive_questions(p_year INTEGER)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM questions WHERE year < p_year;
    COMMIT;  -- OK in procedure
END;
$$;

-- Call procedure
CALL archive_questions(2015);

-- Use FUNCTION for computed values (no transaction control)
CREATE OR REPLACE FUNCTION count_questions(p_course_id INTEGER)
RETURNS INTEGER AS $$
DECLARE
    v_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO v_count FROM questions WHERE course_id = p_course_id;
    RETURN v_count;
END;
$$ LANGUAGE plpgsql;

-- Call function in query
SELECT course_code, count_questions(course_id) FROM courses;
```

**Key differences:**
- **Function**: Returns value, used in SELECT, can't control transactions
- **Procedure**: Performs action, called with CALL, can COMMIT/ROLLBACK

---

### Mistake 4.2: Not Handling NULL Returns

**What happens:**
```sql
CREATE OR REPLACE FUNCTION get_course_avg(p_course_id INTEGER)
RETURNS NUMERIC AS $$
DECLARE
    v_avg NUMERIC;
BEGIN
    SELECT AVG(marks) INTO v_avg
    FROM questions
    WHERE course_id = p_course_id;
    RETURN v_avg;  -- Returns NULL if no questions!
END;
$$ LANGUAGE plpgsql;

-- This breaks calculations
SELECT course_code, get_course_avg(course_id) * 2 FROM courses;
-- Result: NULL * 2 = NULL
```

**How to fix:**
```sql
CREATE OR REPLACE FUNCTION get_course_avg(p_course_id INTEGER)
RETURNS NUMERIC AS $$
DECLARE
    v_avg NUMERIC;
BEGIN
    SELECT COALESCE(AVG(marks), 0) INTO v_avg
    FROM questions
    WHERE course_id = p_course_id;
    RETURN v_avg;  -- Returns 0 instead of NULL
END;
$$ LANGUAGE plpgsql;

-- Or handle NULL at call site
SELECT course_code, COALESCE(get_course_avg(course_id), 0) * 2 FROM courses;
```

**How to avoid:**
- Always handle NULL returns explicitly
- Use COALESCE for default values
- Document return behavior in function comments

---

### Mistake 4.3: Debugging Stored Procedure Errors

**What happens:**
```sql
CREATE OR REPLACE FUNCTION complex_calculation(p_id INTEGER)
RETURNS INTEGER AS $$
DECLARE
    v_result INTEGER;
    v_temp INTEGER;
BEGIN
    -- Complex logic with multiple steps
    -- Error somewhere here, but where?
    SELECT some_value INTO v_temp FROM table1 WHERE id = p_id;
    SELECT other_value INTO v_result FROM table2 WHERE id = v_temp;
    RETURN v_result;
END;
$$ LANGUAGE plpgsql;
```

**Error message is unhelpful:**
```
ERROR:  query returned no rows
```

**How to fix:**
```sql
CREATE OR REPLACE FUNCTION complex_calculation(p_id INTEGER)
RETURNS INTEGER AS $$
DECLARE
    v_result INTEGER;
    v_temp INTEGER;
BEGIN
    -- Add logging
    RAISE NOTICE 'Starting calculation for id %', p_id;

    SELECT some_value INTO v_temp FROM table1 WHERE id = p_id;
    IF v_temp IS NULL THEN
        RAISE EXCEPTION 'No record found in table1 for id %', p_id;
    END IF;
    RAISE NOTICE 'v_temp = %', v_temp;

    SELECT other_value INTO v_result FROM table2 WHERE id = v_temp;
    IF v_result IS NULL THEN
        RAISE EXCEPTION 'No record found in table2 for id %', v_temp;
    END IF;
    RAISE NOTICE 'v_result = %', v_result;

    RETURN v_result;
END;
$$ LANGUAGE plpgsql;

-- Enable client_min_messages to see NOTICE
SET client_min_messages TO NOTICE;
```

**Debugging techniques:**
- Use RAISE NOTICE for debugging output
- Check for NULL explicitly
- Use RAISE EXCEPTION with descriptive messages
- Use ASSERT for internal invariants
- Test functions incrementally

---

## Mistake Category 5: Common Table Expressions (CTEs)

### Mistake 5.1: Recursive CTE Without Termination

**What happens:**
```sql
WITH RECURSIVE infinite AS (
    SELECT 1 as n
    UNION ALL
    SELECT n + 1 FROM infinite  -- No termination condition!
)
SELECT * FROM infinite;
```

**Error message:**
```
ERROR:  maximum recursion depth exceeded
```

**How to fix:**
```sql
-- Add termination condition
WITH RECURSIVE finite AS (
    SELECT 1 as n
    UNION ALL
    SELECT n + 1 FROM finite WHERE n < 100  -- Terminates at 100
)
SELECT * FROM finite;

-- For hierarchical data
WITH RECURSIVE topic_hierarchy AS (
    SELECT topic_id, topic_name, parent_topic_id, 1 as level
    FROM topics
    WHERE parent_topic_id IS NULL

    UNION ALL

    SELECT t.topic_id, t.topic_name, t.parent_topic_id, th.level + 1
    FROM topics t
    JOIN topic_hierarchy th ON t.parent_topic_id = th.topic_id
    WHERE th.level < 10  -- Prevent infinite loops in circular references
)
SELECT * FROM topic_hierarchy;
```

**How to avoid:**
- Always include termination condition in recursive CTE
- Add max depth limit for hierarchical data
- Detect cycles in data before using recursive CTE

---

### Mistake 5.2: CTE Optimization Fence

**What happens:**
```sql
-- CTE is evaluated once and materialized
WITH large_dataset AS (
    SELECT * FROM questions  -- 1 million rows
)
SELECT * FROM large_dataset WHERE course_id = 1;  -- Filters after materialization
```

**Why it's slow:**
PostgreSQL materializes the entire CTE before filtering, loading all 1M rows into memory.

**How to fix:**
```sql
-- Option 1: Add filter inside CTE
WITH filtered_dataset AS (
    SELECT * FROM questions WHERE course_id = 1  -- Filter early
)
SELECT * FROM filtered_dataset;

-- Option 2: Use subquery instead (PostgreSQL can optimize)
SELECT * FROM (
    SELECT * FROM questions
) sub WHERE course_id = 1;

-- Option 3: Use join instead of CTE if appropriate
SELECT q.* FROM questions q WHERE course_id = 1;
```

**When CTEs are materialized (PostgreSQL 12+):**
- NOT materialized: Simple CTEs used once
- Materialized: CTEs used multiple times or recursive CTEs

**Force materialization:**
```sql
WITH stats AS MATERIALIZED (
    SELECT course_id, AVG(marks) as avg_marks FROM questions GROUP BY course_id
)
SELECT * FROM stats;
```

---

## Mistake Category 6: Window Functions

### Mistake 6.1: Mixing Window Functions and GROUP BY

**What happens:**
```sql
SELECT
    course_id,
    AVG(marks) as avg_marks,  -- Aggregation
    marks,  -- Individual value - ERROR!
    ROW_NUMBER() OVER (PARTITION BY course_id ORDER BY marks) as rn
FROM questions
GROUP BY course_id;
```

**Error message:**
```
ERROR:  column "questions.marks" must appear in the GROUP BY clause or be used in an aggregate function
```

**Why it happens:**
GROUP BY aggregates rows, but window functions keep individual rows. You can't mix both without proper grouping.

**How to fix:**
```sql
-- Option 1: Remove GROUP BY (use window function for aggregation)
SELECT
    course_id,
    marks,
    AVG(marks) OVER (PARTITION BY course_id) as avg_marks,
    ROW_NUMBER() OVER (PARTITION BY course_id ORDER BY marks) as rn
FROM questions;

-- Option 2: Use subquery
WITH aggregated AS (
    SELECT course_id, AVG(marks) as avg_marks
    FROM questions
    GROUP BY course_id
)
SELECT
    q.course_id,
    q.marks,
    a.avg_marks,
    ROW_NUMBER() OVER (PARTITION BY q.course_id ORDER BY q.marks) as rn
FROM questions q
JOIN aggregated a ON q.course_id = a.course_id;
```

---

### Mistake 6.2: Wrong ORDER BY in Window Function

**What happens:**
```sql
-- Want to rank questions by highest marks first
SELECT
    question_id,
    marks,
    ROW_NUMBER() OVER (ORDER BY marks) as rank  -- ASC by default!
FROM questions;
```

**Result:**
Lowest marks get rank 1, not highest.

**How to fix:**
```sql
-- Explicit DESC for highest-to-lowest
SELECT
    question_id,
    marks,
    ROW_NUMBER() OVER (ORDER BY marks DESC) as rank
FROM questions;

-- With PARTITION
SELECT
    course_id,
    question_id,
    marks,
    ROW_NUMBER() OVER (PARTITION BY course_id ORDER BY marks DESC) as rank_in_course
FROM questions;
```

---

### Mistake 6.3: Using Window Function in WHERE Clause

**What happens:**
```sql
-- Want top 3 questions per course
SELECT
    course_id,
    question_id,
    marks,
    ROW_NUMBER() OVER (PARTITION BY course_id ORDER BY marks DESC) as rn
FROM questions
WHERE rn <= 3;  -- ERROR!
```

**Error message:**
```
ERROR:  window functions are not allowed in WHERE
```

**Why it happens:**
Window functions execute after WHERE clause. You can't filter on window function results in WHERE.

**How to fix:**
```sql
-- Use subquery or CTE
WITH ranked AS (
    SELECT
        course_id,
        question_id,
        marks,
        ROW_NUMBER() OVER (PARTITION BY course_id ORDER BY marks DESC) as rn
    FROM questions
)
SELECT * FROM ranked WHERE rn <= 3;
```

---

## General Best Practices

### 1. Testing Strategy
```sql
-- Always test in development first
BEGIN;
    -- Try your trigger/constraint/function
    INSERT INTO questions (course_id, topic_id, question_text, difficulty, marks)
    VALUES (1, 1, 'Test', 'easy', 5);
    
    SELECT * FROM audit_log;  -- Verify trigger worked
ROLLBACK;  -- Undo test changes
```

### 2. Error Handling in Functions
```sql
CREATE OR REPLACE FUNCTION safe_divide(a NUMERIC, b NUMERIC)
RETURNS NUMERIC AS $$
BEGIN
    IF b = 0 THEN
        RAISE EXCEPTION 'Division by zero';
    END IF;
    RETURN a / b;
EXCEPTION
    WHEN division_by_zero THEN
        RETURN NULL;
    WHEN OTHERS THEN
        RAISE NOTICE 'Unexpected error: %', SQLERRM;
        RETURN NULL;
END;
$$ LANGUAGE plpgsql;
```

### 3. Documentation
```sql
-- Document complex logic
CREATE OR REPLACE FUNCTION calculate_grade(p_marks INTEGER)
RETURNS VARCHAR AS $$
-- Calculates letter grade from marks
-- Input: marks (0-100)
-- Returns: 'A', 'B', 'C', 'D', or 'F'
-- Raises exception if marks out of range
BEGIN
    IF p_marks < 0 OR p_marks > 100 THEN
        RAISE EXCEPTION 'Invalid marks: %. Must be 0-100', p_marks;
    END IF;
    
    IF p_marks >= 90 THEN RETURN 'A';
    ELSIF p_marks >= 80 THEN RETURN 'B';
    ELSIF p_marks >= 70 THEN RETURN 'C';
    ELSIF p_marks >= 60 THEN RETURN 'D';
    ELSE RETURN 'F';
    END IF;
END;
$$ LANGUAGE plpgsql;
```

---

## Quick Reference: Common Error Messages

| Error | Likely Cause | Solution |
|-------|--------------|----------|
| "cannot update view" | View has JOIN/GROUP BY | Update underlying table or use INSTEAD OF trigger |
| "infinite recursion detected" | Circular view dependency | Redesign view relationships |
| "control reached end without RETURN" | Missing RETURN in function | Add `RETURN NEW/OLD` |
| "record 'new' is not assigned" | Using NEW in DELETE trigger | Use OLD instead |
| "check constraint violated" | Adding constraint to invalid data | Clean data first or use NOT VALID |
| "cannot use subquery in check constraint" | CHECK with SELECT | Use trigger instead |
| "cannot commit in subtransaction" | COMMIT in function | Use procedure instead |
| "maximum recursion depth exceeded" | Recursive CTE no termination | Add WHERE condition to stop recursion |
| "window functions not allowed in WHERE" | Filter on window function | Use subquery/CTE |

---

**Remember**: Mistakes are part of learning! Use this guide to troubleshoot, but don't let fear of mistakes prevent you from experimenting. Always test in a safe environment first!

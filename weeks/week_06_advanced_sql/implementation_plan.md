# Week 6: Advanced SQL - 7-Day Implementation Plan

**Goal**: Master advanced SQL features (views, triggers, constraints, stored procedures, CTEs, window functions) to enhance your CourseDB-AI backend.

**Prerequisites**:
- Week 5 completed (PostgreSQL + FastAPI backend running)
- CourseDB-AI database with courses, topics, questions tables
- PostgreSQL access (psql or pgAdmin)

---

## Day 1: Database Views (Monday)

### Morning: Theory and Simple Views (2-3 hours)

**Learning Objectives**:
- Understand view vs materialized view
- Create simple views
- Query views like tables
- Update updatable views

**Tasks**:

1. **Read README.md Section 1: Database Views** (30 min)

2. **Create your first view** (30 min):
```sql
-- Connect to your database
psql -U coursedb_user -d coursedb_dev

-- Create simple view
CREATE VIEW active_courses AS
SELECT course_id, course_code, title, credits
FROM courses
WHERE status = 'active';

-- Query the view
SELECT * FROM active_courses;

-- Test: This should work (updatable view)
UPDATE active_courses SET credits = 4 WHERE course_id = 1;
```

3. **Complete Exercise 1.1** from exercises.md (30 min):
- Create `active_courses_with_questions` view
- Test queries on the view
- Understand aggregation in views

4. **Complete Exercise 1.2** (45 min):
- Create `course_analytics` view with multiple joins
- Query difficulty distribution
- Calculate average marks per course

**Checkpoint**: Can you create a view and query it? ✅

### Afternoon: Complex Views and Materialized Views (2-3 hours)

**Tasks**:

1. **Create complex view with JOINs** (45 min):
```sql
-- Complex view with multiple aggregations
CREATE VIEW comprehensive_course_stats AS
SELECT
    c.course_id,
    c.course_code,
    c.title,
    COUNT(DISTINCT t.topic_id) as topic_count,
    COUNT(DISTINCT q.question_id) as question_count,
    COUNT(CASE WHEN q.difficulty = 'easy' THEN 1 END) as easy_questions,
    COUNT(CASE WHEN q.difficulty = 'medium' THEN 1 END) as medium_questions,
    COUNT(CASE WHEN q.difficulty = 'hard' THEN 1 END) as hard_questions,
    ROUND(AVG(q.marks), 2) as avg_marks,
    MAX(q.year) as latest_year,
    MIN(q.year) as earliest_year
FROM courses c
LEFT JOIN topics t ON c.course_id = t.course_id
LEFT JOIN questions q ON c.course_id = q.course_id
GROUP BY c.course_id, c.course_code, c.title;

-- Query the view
SELECT * FROM comprehensive_course_stats
WHERE question_count > 10
ORDER BY avg_marks DESC;
```

2. **Complete Exercise 1.3: Materialized Views** (60 min):
- Understand when to use materialized views
- Create materialized view with aggregations
- Refresh materialized view
- Create unique index for concurrent refresh

3. **Experiment with view updates** (30 min):
```sql
-- Try to update non-updatable view (should fail)
-- UPDATE course_analytics SET question_count = 100 WHERE course_id = 1;

-- Create updatable view
CREATE VIEW simple_courses AS
SELECT course_id, course_code, title, credits
FROM courses;

-- This works
UPDATE simple_courses SET credits = 4 WHERE course_id = 1;
```

**Day 1 Deliverable**:
- [ ] 3+ views created for CourseDB-AI
- [ ] 1 materialized view with refresh
- [ ] Understanding of updatable vs non-updatable views

**Evening Reflection** (30 min):
- What's the difference between view and materialized view?
- When would you use each?
- Document your views in a SQL file

---

## Day 2: Database Triggers (Tuesday)

### Morning: Audit Triggers (2-3 hours)

**Learning Objectives**:
- Understand trigger types (BEFORE, AFTER)
- Write trigger functions
- Implement audit logging
- Use TG_OP, OLD, NEW variables

**Tasks**:

1. **Read README.md Section 3: Database Triggers** (30 min)

2. **Complete Exercise 2.1: Audit Trigger** (90 min):

**Step 1: Create audit table**:
```sql
CREATE TABLE audit_log (
    audit_id SERIAL PRIMARY KEY,
    table_name VARCHAR(50),
    record_id INTEGER,
    operation VARCHAR(10),
    old_data JSONB,
    new_data JSONB,
    changed_by VARCHAR(100) DEFAULT CURRENT_USER,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Step 2: Create trigger function**:
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

**Step 3: Attach trigger**:
```sql
CREATE TRIGGER question_audit_trigger
AFTER INSERT OR UPDATE OR DELETE ON questions
FOR EACH ROW
EXECUTE FUNCTION audit_question_changes();
```

**Step 4: Test**:
```sql
-- Insert a question
INSERT INTO questions (course_id, topic_id, question_text, difficulty, marks)
VALUES (1, 1, 'What is normalization?', 'easy', 5);

-- Update the question
UPDATE questions SET difficulty = 'medium' WHERE question_id = 1;

-- View audit log
SELECT * FROM audit_log ORDER BY changed_at DESC;

-- Examine the JSONB data
SELECT
    audit_id,
    operation,
    old_data->>'difficulty' as old_difficulty,
    new_data->>'difficulty' as new_difficulty,
    changed_at
FROM audit_log
WHERE table_name = 'questions';
```

3. **Extend audit to other tables** (45 min):
- Create audit triggers for `courses` table
- Create audit triggers for `topics` table
- Test all triggers

**Checkpoint**: Do you have audit logging working for all tables? ✅

### Afternoon: Validation Triggers (2-3 hours)

**Tasks**:

1. **Complete Exercise 2.2: Validation Trigger** (90 min):
```sql
CREATE OR REPLACE FUNCTION validate_question_data()
RETURNS TRIGGER AS $$
BEGIN
    -- Validate marks range
    IF NEW.marks < 1 OR NEW.marks > 100 THEN
        RAISE EXCEPTION 'Marks must be between 1 and 100, got %', NEW.marks;
    END IF;

    -- Validate difficulty
    IF NEW.difficulty NOT IN ('easy', 'medium', 'hard') THEN
        RAISE EXCEPTION 'Invalid difficulty: %. Must be easy, medium, or hard', NEW.difficulty;
    END IF;

    -- Validate year range
    IF NEW.year < 2000 OR NEW.year > EXTRACT(YEAR FROM CURRENT_DATE) + 1 THEN
        RAISE EXCEPTION 'Invalid year: %. Must be between 2000 and %',
            NEW.year, EXTRACT(YEAR FROM CURRENT_DATE) + 1;
    END IF;

    -- Validate question text not empty
    IF LENGTH(TRIM(NEW.question_text)) < 10 THEN
        RAISE EXCEPTION 'Question text must be at least 10 characters';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER validate_question_trigger
BEFORE INSERT OR UPDATE ON questions
FOR EACH ROW
EXECUTE FUNCTION validate_question_data();
```

**Test validation**:
```sql
-- These should fail with descriptive errors
INSERT INTO questions (course_id, topic_id, question_text, difficulty, marks)
VALUES (1, 1, 'Test', 'invalid', 150);  -- Invalid difficulty and marks

INSERT INTO questions (course_id, topic_id, question_text, difficulty, marks)
VALUES (1, 1, 'Short', 'easy', 5);  -- Question text too short

-- This should succeed
INSERT INTO questions (course_id, topic_id, question_text, difficulty, marks)
VALUES (1, 1, 'What is the difference between 1NF and 2NF?', 'medium', 10);
```

2. **Complete Exercise 2.3: Automatic Timestamp** (45 min):
```sql
-- Add updated_at column to courses
ALTER TABLE courses ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- Create timestamp update function
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Attach trigger
CREATE TRIGGER update_course_timestamp
BEFORE UPDATE ON courses
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();

-- Test
UPDATE courses SET title = 'Database Management Systems' WHERE course_id = 1;
SELECT course_id, title, updated_at FROM courses WHERE course_id = 1;
```

**Day 2 Deliverable**:
- [ ] Audit triggers on all major tables
- [ ] Validation triggers for data integrity
- [ ] Automatic timestamp updates
- [ ] All triggers tested and working

**Evening Task**: Write reflection on triggers (see reflection.md)

---

## Day 3: Constraints (Wednesday)

### Morning: CHECK and UNIQUE Constraints (2-3 hours)

**Learning Objectives**:
- Add CHECK constraints for business rules
- Implement UNIQUE constraints
- Understand constraint violation errors
- Use named constraints

**Tasks**:

1. **Read README.md Section 4: Constraints** (20 min)

2. **Complete Exercise 3.1: CHECK Constraints** (90 min):
```sql
-- Add difficulty constraint
ALTER TABLE questions
ADD CONSTRAINT valid_difficulty
CHECK (difficulty IN ('easy', 'medium', 'hard'));

-- Add marks constraint
ALTER TABLE questions
ADD CONSTRAINT valid_marks
CHECK (marks BETWEEN 1 AND 100);

-- Add year constraint
ALTER TABLE questions
ADD CONSTRAINT valid_year
CHECK (year >= 2000 AND year <= EXTRACT(YEAR FROM CURRENT_DATE) + 1);

-- Add credits constraint for courses
ALTER TABLE courses
ADD CONSTRAINT valid_credits
CHECK (credits BETWEEN 1 AND 10);

-- Test constraints
-- This should fail
INSERT INTO questions (course_id, topic_id, question_text, difficulty, marks)
VALUES (1, 1, 'Test question', 'super_hard', 5);

-- This should fail
INSERT INTO questions (course_id, topic_id, question_text, difficulty, marks)
VALUES (1, 1, 'Test question', 'easy', 150);

-- This should succeed
INSERT INTO questions (course_id, topic_id, question_text, difficulty, marks)
VALUES (1, 1, 'What is ACID?', 'medium', 15);
```

3. **Complete Exercise 3.2: UNIQUE Constraints** (60 min):
```sql
-- Course code must be unique
ALTER TABLE courses
ADD CONSTRAINT unique_course_code UNIQUE (course_code);

-- Topic name must be unique per course (composite unique)
ALTER TABLE topics
ADD CONSTRAINT unique_topic_per_course UNIQUE (course_id, topic_name);

-- Test
-- This should fail if course code exists
INSERT INTO courses (course_code, title, credits)
VALUES ('CS201', 'Duplicate Course', 4);

-- This should fail if topic exists for course
INSERT INTO topics (course_id, topic_name, order_index)
VALUES (1, 'Normalization', 5);  -- Assuming this topic already exists for course 1
```

**Checkpoint**: Do all constraints prevent invalid data? ✅

### Afternoon: Custom Domains and Complex Constraints (2-3 hours)

**Tasks**:

1. **Complete Exercise 3.3: Custom Domain Constraints** (90 min):
```sql
-- Create custom difficulty type
CREATE DOMAIN difficulty_level AS VARCHAR(20)
CHECK (VALUE IN ('easy', 'medium', 'hard'));

-- Create custom marks type
CREATE DOMAIN question_marks AS INTEGER
CHECK (VALUE BETWEEN 1 AND 100);

-- Create custom year type
CREATE DOMAIN academic_year AS INTEGER
CHECK (VALUE >= 2000 AND VALUE <= EXTRACT(YEAR FROM CURRENT_DATE) + 1);

-- Create new table using custom domains
CREATE TABLE validated_questions (
    question_id SERIAL PRIMARY KEY,
    course_id INTEGER NOT NULL,
    topic_id INTEGER NOT NULL,
    question_text TEXT NOT NULL,
    difficulty difficulty_level,
    marks question_marks,
    year academic_year,
    CONSTRAINT fk_course FOREIGN KEY (course_id) REFERENCES courses(course_id),
    CONSTRAINT fk_topic FOREIGN KEY (topic_id) REFERENCES topics(topic_id)
);

-- Test domain constraints
INSERT INTO validated_questions (course_id, topic_id, question_text, difficulty, marks, year)
VALUES (1, 1, 'What is a database?', 'easy', 5, 2024);

-- This should fail (invalid difficulty)
-- INSERT INTO validated_questions (course_id, topic_id, question_text, difficulty, marks, year)
-- VALUES (1, 1, 'Test', 'super_easy', 5, 2024);
```

2. **Document all constraints** (45 min):
```sql
-- View all constraints
SELECT
    tc.constraint_name,
    tc.constraint_type,
    tc.table_name,
    cc.check_clause
FROM information_schema.table_constraints tc
LEFT JOIN information_schema.check_constraints cc
    ON tc.constraint_name = cc.constraint_name
WHERE tc.table_schema = 'public'
ORDER BY tc.table_name, tc.constraint_type;
```

3. **Create constraint documentation** (30 min):
- List all CHECK constraints and their purpose
- List all UNIQUE constraints
- Document custom domains
- Save as `constraints.sql`

**Day 3 Deliverable**:
- [ ] CHECK constraints on all appropriate columns
- [ ] UNIQUE constraints for business keys
- [ ] Custom domains created and used
- [ ] Constraint documentation file

---

## Day 4: Stored Procedures and Functions (Thursday)

### Morning: Functions Returning Values (2-3 hours)

**Learning Objectives**:
- Understand function vs procedure
- Write functions in plpgsql
- Return single values
- Return tables
- Use functions in queries

**Tasks**:

1. **Read README.md Section 5: Stored Procedures and Functions** (30 min)

2. **Complete Exercise 4.1: Function Returning Single Value** (60 min):
```sql
-- Function to count questions per course
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

-- Usage in query
SELECT
    course_id,
    course_code,
    title,
    get_course_question_count(course_id) as question_count
FROM courses;
```

3. **Create additional utility functions** (90 min):
```sql
-- Function to calculate average difficulty
CREATE OR REPLACE FUNCTION get_course_avg_marks(p_course_id INTEGER)
RETURNS NUMERIC AS $$
DECLARE
    v_avg NUMERIC;
BEGIN
    SELECT ROUND(AVG(marks), 2) INTO v_avg
    FROM questions
    WHERE course_id = p_course_id;

    RETURN COALESCE(v_avg, 0);
END;
$$ LANGUAGE plpgsql;

-- Function to get difficulty distribution
CREATE OR REPLACE FUNCTION get_difficulty_distribution(p_course_id INTEGER)
RETURNS TEXT AS $$
DECLARE
    v_easy INTEGER;
    v_medium INTEGER;
    v_hard INTEGER;
BEGIN
    SELECT
        COUNT(CASE WHEN difficulty = 'easy' THEN 1 END),
        COUNT(CASE WHEN difficulty = 'medium' THEN 1 END),
        COUNT(CASE WHEN difficulty = 'hard' THEN 1 END)
    INTO v_easy, v_medium, v_hard
    FROM questions
    WHERE course_id = p_course_id;

    RETURN FORMAT('Easy: %s, Medium: %s, Hard: %s', v_easy, v_medium, v_hard);
END;
$$ LANGUAGE plpgsql;

-- Test functions
SELECT
    course_code,
    get_course_question_count(course_id) as questions,
    get_course_avg_marks(course_id) as avg_marks,
    get_difficulty_distribution(course_id) as difficulty_dist
FROM courses;
```

**Checkpoint**: Can you write and use functions in queries? ✅

### Afternoon: Functions Returning Tables and Procedures (2-3 hours)

**Tasks**:

1. **Complete Exercise 4.2: Function Returning Table** (90 min):
```sql
CREATE OR REPLACE FUNCTION get_course_topics_with_stats(p_course_id INTEGER)
RETURNS TABLE (
    topic_id INTEGER,
    topic_name VARCHAR(255),
    question_count BIGINT,
    avg_marks NUMERIC,
    difficulty_dist TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        t.topic_id,
        t.topic_name,
        COUNT(q.question_id) as question_count,
        ROUND(AVG(q.marks), 2) as avg_marks,
        STRING_AGG(
            DISTINCT q.difficulty || ':' || COUNT(*) OVER (PARTITION BY t.topic_id, q.difficulty)::TEXT,
            ', '
        ) as difficulty_dist
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

2. **Complete Exercise 4.3: Procedure with Business Logic** (90 min):
```sql
-- Create archive table
CREATE TABLE archived_questions (
    LIKE questions INCLUDING ALL,
    archived_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    archived_by VARCHAR(100) DEFAULT CURRENT_USER
);

-- Archive procedure
CREATE OR REPLACE PROCEDURE archive_old_questions(
    p_year_threshold INTEGER,
    OUT p_archived_count INTEGER
)
LANGUAGE plpgsql AS $$
BEGIN
    -- Move old questions to archive
    INSERT INTO archived_questions
    SELECT *, CURRENT_TIMESTAMP, CURRENT_USER
    FROM questions
    WHERE year < p_year_threshold;

    GET DIAGNOSTICS p_archived_count = ROW_COUNT;

    -- Delete from main table
    DELETE FROM questions WHERE year < p_year_threshold;

    RAISE NOTICE 'Archived % questions older than %', p_archived_count, p_year_threshold;
END;
$$;

-- Usage
DO $$
DECLARE
    v_count INTEGER;
BEGIN
    CALL archive_old_questions(2015, v_count);
    RAISE NOTICE 'Total archived: %', v_count;
END $$;

-- Verify
SELECT COUNT(*) FROM archived_questions;
```

**Day 4 Deliverable**:
- [ ] 5+ functions for CourseDB-AI analytics
- [ ] 2+ procedures for business operations
- [ ] All functions tested and working
- [ ] Documentation of function signatures

---

## Day 5: Common Table Expressions (Friday)

### Morning: Basic and Multiple CTEs (2-3 hours)

**Learning Objectives**:
- Understand CTE syntax
- Write simple CTEs
- Chain multiple CTEs
- Use CTEs for complex queries

**Tasks**:

1. **Read README.md Section 6: CTEs** (20 min)

2. **Complete Exercise 5.1: Basic CTE** (60 min):
```sql
-- Course difficulty distribution
WITH difficulty_stats AS (
    SELECT
        course_id,
        difficulty,
        COUNT(*) as count,
        ROUND(AVG(marks), 2) as avg_marks
    FROM questions
    GROUP BY course_id, difficulty
)
SELECT
    c.course_code,
    c.title,
    MAX(CASE WHEN ds.difficulty = 'easy' THEN ds.count ELSE 0 END) as easy_count,
    MAX(CASE WHEN ds.difficulty = 'medium' THEN ds.count ELSE 0 END) as medium_count,
    MAX(CASE WHEN ds.difficulty = 'hard' THEN ds.count ELSE 0 END) as hard_count,
    MAX(CASE WHEN ds.difficulty = 'easy' THEN ds.avg_marks END) as easy_avg,
    MAX(CASE WHEN ds.difficulty = 'medium' THEN ds.avg_marks END) as medium_avg,
    MAX(CASE WHEN ds.difficulty = 'hard' THEN ds.avg_marks END) as hard_avg
FROM courses c
LEFT JOIN difficulty_stats ds ON c.course_id = ds.course_id
GROUP BY c.course_id, c.course_code, c.title
ORDER BY c.course_code;
```

3. **Complete Exercise 5.2: Multiple CTEs** (90 min):
```sql
WITH course_question_counts AS (
    SELECT
        course_id,
        COUNT(*) as total_questions,
        COUNT(CASE WHEN difficulty = 'easy' THEN 1 END) as easy_questions,
        COUNT(CASE WHEN difficulty = 'medium' THEN 1 END) as medium_questions,
        COUNT(CASE WHEN difficulty = 'hard' THEN 1 END) as hard_questions
    FROM questions
    GROUP BY course_id
),
course_topic_counts AS (
    SELECT course_id, COUNT(*) as total_topics
    FROM topics
    GROUP BY course_id
),
course_avg_marks AS (
    SELECT
        course_id,
        ROUND(AVG(marks), 2) as avg_marks,
        MIN(marks) as min_marks,
        MAX(marks) as max_marks
    FROM questions
    GROUP BY course_id
),
course_year_range AS (
    SELECT
        course_id,
        MIN(year) as earliest_year,
        MAX(year) as latest_year,
        COUNT(DISTINCT year) as year_span
    FROM questions
    WHERE year IS NOT NULL
    GROUP BY course_id
)
SELECT
    c.course_code,
    c.title,
    c.credits,
    COALESCE(cqc.total_questions, 0) as total_questions,
    COALESCE(cqc.easy_questions, 0) as easy_questions,
    COALESCE(cqc.medium_questions, 0) as medium_questions,
    COALESCE(cqc.hard_questions, 0) as hard_questions,
    COALESCE(ctc.total_topics, 0) as total_topics,
    COALESCE(cam.avg_marks, 0) as avg_marks,
    cam.min_marks,
    cam.max_marks,
    cyr.earliest_year,
    cyr.latest_year,
    cyr.year_span
FROM courses c
LEFT JOIN course_question_counts cqc ON c.course_id = cqc.course_id
LEFT JOIN course_topic_counts ctc ON c.course_id = ctc.course_id
LEFT JOIN course_avg_marks cam ON c.course_id = cam.course_id
LEFT JOIN course_year_range cyr ON c.course_id = cyr.course_id
ORDER BY total_questions DESC;
```

**Checkpoint**: Can you write complex analytical queries with CTEs? ✅

### Afternoon: Recursive CTEs (2-3 hours)

**Tasks**:

1. **Understand recursive CTE structure** (30 min):
```sql
-- General pattern
WITH RECURSIVE cte_name AS (
    -- Base case (anchor member)
    SELECT ... WHERE ...

    UNION ALL

    -- Recursive case (recursive member)
    SELECT ... FROM ... JOIN cte_name ON ...
)
SELECT * FROM cte_name;
```

2. **Complete Exercise 5.3: Recursive CTE** (90 min):

**First, add hierarchical support to topics** (if not exists):
```sql
-- Add parent_topic_id for topic hierarchy
ALTER TABLE topics ADD COLUMN parent_topic_id INTEGER REFERENCES topics(topic_id);

-- Create some hierarchical topics
UPDATE topics SET parent_topic_id = NULL WHERE topic_name = 'Normalization';
INSERT INTO topics (course_id, topic_name, order_index, parent_topic_id)
VALUES
    (1, '1NF', 10, (SELECT topic_id FROM topics WHERE topic_name = 'Normalization')),
    (1, '2NF', 11, (SELECT topic_id FROM topics WHERE topic_name = 'Normalization')),
    (1, '3NF', 12, (SELECT topic_id FROM topics WHERE topic_name = 'Normalization'));
```

**Recursive query**:
```sql
WITH RECURSIVE topic_hierarchy AS (
    -- Base case: root topics (no parent)
    SELECT
        topic_id,
        topic_name,
        parent_topic_id,
        course_id,
        1 as level,
        topic_name::TEXT as path,
        ARRAY[topic_id] as id_path
    FROM topics
    WHERE parent_topic_id IS NULL AND course_id = 1

    UNION ALL

    -- Recursive case: child topics
    SELECT
        t.topic_id,
        t.topic_name,
        t.parent_topic_id,
        t.course_id,
        th.level + 1,
        th.path || ' → ' || t.topic_name,
        th.id_path || t.topic_id
    FROM topics t
    JOIN topic_hierarchy th ON t.parent_topic_id = th.topic_id
)
SELECT
    REPEAT('  ', level - 1) || topic_name as indented_topic,
    level,
    path
FROM topic_hierarchy
ORDER BY path;
```

3. **Create number sequence with recursive CTE** (30 min):
```sql
-- Generate sequence of years
WITH RECURSIVE year_sequence AS (
    SELECT 2020 as year
    UNION ALL
    SELECT year + 1
    FROM year_sequence
    WHERE year < 2024
)
SELECT
    ys.year,
    COUNT(q.question_id) as question_count
FROM year_sequence ys
LEFT JOIN questions q ON q.year = ys.year
GROUP BY ys.year
ORDER BY ys.year;
```

**Day 5 Deliverable**:
- [ ] 5+ analytical queries using CTEs
- [ ] 2+ recursive CTE examples
- [ ] Saved in `advanced_queries.sql` file
- [ ] Performance comparison: CTE vs subquery

---

## Day 6: Window Functions (Saturday)

### Morning: Ranking Functions (2-3 hours)

**Learning Objectives**:
- Understand window function syntax
- Use ROW_NUMBER, RANK, DENSE_RANK
- Apply PARTITION BY
- Order results properly

**Tasks**:

1. **Read README.md Section 7: Window Functions** (30 min)

2. **Complete Exercise 6.1: ROW_NUMBER()** (60 min):
```sql
-- Rank questions by marks within each course
SELECT
    c.course_code,
    q.question_id,
    q.question_text,
    q.marks,
    q.difficulty,
    ROW_NUMBER() OVER (
        PARTITION BY c.course_id
        ORDER BY q.marks DESC
    ) as rank_in_course,
    ROW_NUMBER() OVER (
        PARTITION BY c.course_id, q.difficulty
        ORDER BY q.marks DESC
    ) as rank_in_difficulty
FROM questions q
JOIN courses c ON q.course_id = c.course_id
ORDER BY c.course_code, rank_in_course;

-- Get top 3 questions per course
WITH ranked_questions AS (
    SELECT
        course_id,
        question_text,
        marks,
        ROW_NUMBER() OVER (PARTITION BY course_id ORDER BY marks DESC) as rn
    FROM questions
)
SELECT *
FROM ranked_questions
WHERE rn <= 3;
```

3. **Complete Exercise 6.2: RANK() and DENSE_RANK()** (60 min):
```sql
-- Compare RANK vs DENSE_RANK
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
    PERCENT_RANK() OVER (ORDER BY question_count DESC) as percent_rank,
    NTILE(4) OVER (ORDER BY question_count DESC) as quartile
FROM course_stats
ORDER BY question_count DESC;
```

**Checkpoint**: Understand difference between ROW_NUMBER, RANK, DENSE_RANK? ✅

### Afternoon: LAG/LEAD and Aggregations (2-3 hours)

**Tasks**:

1. **Complete Exercise 6.3: LAG() and LEAD()** (90 min):
```sql
-- Year-over-year question comparison
WITH yearly_counts AS (
    SELECT
        year,
        COUNT(*) as question_count,
        AVG(marks) as avg_marks
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
    question_count - LAG(question_count) OVER (ORDER BY year) as yoy_change,
    ROUND(
        (question_count::NUMERIC - LAG(question_count) OVER (ORDER BY year)) /
        NULLIF(LAG(question_count) OVER (ORDER BY year), 0) * 100,
        2
    ) as yoy_percent_change,
    avg_marks,
    LAG(avg_marks) OVER (ORDER BY year) as prev_year_avg_marks
FROM yearly_counts;

-- Compare adjacent questions by marks
SELECT
    question_id,
    course_id,
    marks,
    difficulty,
    LAG(marks) OVER (PARTITION BY course_id ORDER BY marks) as prev_marks,
    LEAD(marks) OVER (PARTITION BY course_id ORDER BY marks) as next_marks,
    marks - LAG(marks) OVER (PARTITION BY course_id ORDER BY marks) as marks_diff
FROM questions
ORDER BY course_id, marks;
```

2. **Complete Exercise 6.4: Running Totals and Moving Averages** (90 min):
```sql
-- Running totals and cumulative averages
SELECT
    course_id,
    question_id,
    marks,
    difficulty,
    -- Running total
    SUM(marks) OVER (
        PARTITION BY course_id
        ORDER BY question_id
    ) as running_total,
    -- Running average
    ROUND(AVG(marks) OVER (
        PARTITION BY course_id
        ORDER BY question_id
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ), 2) as running_avg,
    -- Moving average (last 3 questions)
    ROUND(AVG(marks) OVER (
        PARTITION BY course_id
        ORDER BY question_id
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ), 2) as moving_avg_3,
    -- Count of questions so far
    COUNT(*) OVER (
        PARTITION BY course_id
        ORDER BY question_id
    ) as question_count
FROM questions
ORDER BY course_id, question_id;

-- Difficulty distribution with percentages
SELECT
    course_id,
    difficulty,
    COUNT(*) as count,
    ROUND(
        COUNT(*)::NUMERIC * 100 /
        SUM(COUNT(*)) OVER (PARTITION BY course_id),
        2
    ) as percentage,
    ROUND(AVG(marks), 2) as avg_marks
FROM questions
GROUP BY course_id, difficulty
ORDER BY course_id, difficulty;
```

**Day 6 Deliverable**:
- [ ] 10+ window function queries
- [ ] Understanding of PARTITION BY and ORDER BY
- [ ] Saved in `window_functions.sql`
- [ ] Can explain ranking vs aggregation window functions

---

## Day 7: Integration and Practice (Sunday)

### Morning: Combine All Features (2-3 hours)

**Learning Objectives**:
- Build complex analytics using all features
- Combine views, CTEs, window functions
- Optimize query performance
- Document your work

**Tasks**:

1. **Create comprehensive dashboard view** (90 min):
```sql
-- Master analytics view combining everything
CREATE VIEW course_master_dashboard AS
WITH question_stats AS (
    SELECT
        course_id,
        COUNT(*) as total_questions,
        COUNT(CASE WHEN difficulty = 'easy' THEN 1 END) as easy_count,
        COUNT(CASE WHEN difficulty = 'medium' THEN 1 END) as medium_count,
        COUNT(CASE WHEN difficulty = 'hard' THEN 1 END) as hard_count,
        ROUND(AVG(marks), 2) as avg_marks,
        MIN(year) as earliest_year,
        MAX(year) as latest_year
    FROM questions
    GROUP BY course_id
),
topic_stats AS (
    SELECT
        course_id,
        COUNT(*) as total_topics,
        COUNT(CASE WHEN parent_topic_id IS NULL THEN 1 END) as root_topics
    FROM topics
    GROUP BY course_id
),
ranked_courses AS (
    SELECT
        c.course_id,
        c.course_code,
        c.title,
        c.credits,
        COALESCE(qs.total_questions, 0) as total_questions,
        COALESCE(qs.easy_count, 0) as easy_questions,
        COALESCE(qs.medium_count, 0) as medium_questions,
        COALESCE(qs.hard_count, 0) as hard_questions,
        qs.avg_marks,
        qs.earliest_year,
        qs.latest_year,
        COALESCE(ts.total_topics, 0) as total_topics,
        DENSE_RANK() OVER (ORDER BY COALESCE(qs.total_questions, 0) DESC) as question_rank
    FROM courses c
    LEFT JOIN question_stats qs ON c.course_id = qs.course_id
    LEFT JOIN topic_stats ts ON c.course_id = ts.course_id
)
SELECT * FROM ranked_courses;

-- Query the dashboard
SELECT * FROM course_master_dashboard ORDER BY question_rank;
```

2. **Create comprehensive report queries** (90 min):
```sql
-- Complete course report with all metrics
WITH RECURSIVE topic_hierarchy AS (
    -- (recursive CTE for topics)
    SELECT
        topic_id,
        topic_name,
        parent_topic_id,
        course_id,
        1 as level,
        topic_name::TEXT as path
    FROM topics
    WHERE parent_topic_id IS NULL AND course_id = 1
    UNION ALL
    SELECT
        t.topic_id,
        t.topic_name,
        t.parent_topic_id,
        t.course_id,
        th.level + 1,
        th.path || ' → ' || t.topic_name
    FROM topics t
    JOIN topic_hierarchy th ON t.parent_topic_id = th.topic_id
),
question_analytics AS (
    SELECT
        th.topic_id,
        th.topic_name,
        th.level,
        th.path,
        COUNT(q.question_id) as question_count,
        ROUND(AVG(q.marks), 2) as avg_marks,
        STRING_AGG(DISTINCT q.difficulty, ', ') as difficulties,
        MIN(q.year) as earliest_year,
        MAX(q.year) as latest_year
    FROM topic_hierarchy th
    LEFT JOIN questions q ON th.topic_id = q.topic_id
    GROUP BY th.topic_id, th.topic_name, th.level, th.path
)
SELECT
    REPEAT('  ', level - 1) || topic_name as indented_topic,
    question_count,
    avg_marks,
    difficulties,
    earliest_year,
    latest_year,
    RANK() OVER (ORDER BY question_count DESC) as popularity_rank
FROM question_analytics
ORDER BY path;
```

**Checkpoint**: Can you build end-to-end analytics queries? ✅

### Afternoon: Challenge Problems and Documentation (2-3 hours)

**Tasks**:

1. **Complete Challenge Problem 1: Complete Analytics System** (90 min):
- Course performance dashboard view
- Question difficulty analysis
- Topic coverage report
- Historical trends with window functions
- Save all queries in `analytics_system.sql`

2. **Complete Challenge Problem 2: Implement Complete Audit System** (Optional, 90 min):
- Generic audit trigger function for any table
- Apply to all tables
- Query interface to view changes
- Rollback procedure (if time permits)

3. **Documentation and cleanup** (60 min):
```sql
-- Create index on frequently queried columns
CREATE INDEX idx_questions_course_difficulty ON questions(course_id, difficulty);
CREATE INDEX idx_questions_year ON questions(year) WHERE year IS NOT NULL;
CREATE INDEX idx_audit_log_timestamp ON audit_log(changed_at);

-- Document all database objects
SELECT
    'VIEW' as object_type,
    table_name as object_name,
    NULL as returns
FROM information_schema.views
WHERE table_schema = 'public'
UNION ALL
SELECT
    'FUNCTION' as object_type,
    routine_name,
    data_type
FROM information_schema.routines
WHERE routine_schema = 'public' AND routine_type = 'FUNCTION'
UNION ALL
SELECT
    'TRIGGER' as object_type,
    trigger_name,
    NULL
FROM information_schema.triggers
WHERE trigger_schema = 'public'
ORDER BY object_type, object_name;
```

4. **Create summary document** (30 min):
- List all views created
- List all triggers created
- List all functions/procedures created
- List all constraints added
- Document purpose of each

**Day 7 Deliverable**:
- [ ] Complete analytics system working
- [ ] All challenge problems attempted
- [ ] Full documentation of database objects
- [ ] Clean, organized SQL files
- [ ] Week 6 complete! 🎉

---

## Week 6 Final Deliverables Checklist

### Database Objects Created:
- [ ] **5+ Views** (including 1+ materialized view)
- [ ] **3+ Triggers** (audit, validation, timestamp)
- [ ] **10+ Constraints** (CHECK, UNIQUE, custom domains)
- [ ] **5+ Functions/Procedures** (analytics, business logic)
- [ ] **10+ Advanced Queries** (CTEs, window functions)

### Documentation:
- [ ] `views.sql` - All view definitions
- [ ] `triggers.sql` - All trigger definitions
- [ ] `constraints.sql` - All constraint definitions
- [ ] `functions.sql` - All function/procedure definitions
- [ ] `advanced_queries.sql` - CTE and window function examples
- [ ] `analytics_system.sql` - Complete analytics queries
- [ ] `database_objects.md` - Summary documentation

### Testing:
- [ ] All views queryable
- [ ] All triggers firing correctly
- [ ] All constraints preventing invalid data
- [ ] All functions returning correct results
- [ ] All queries optimized and documented

### Reflection:
- [ ] Completed reflection prompts in `reflection.md`
- [ ] Self-assessment quiz completed
- [ ] Mistakes documented in learning log

---

## Time Tracking Template

| Day | Planned Hours | Actual Hours | Completed? | Notes |
|-----|---------------|--------------|------------|-------|
| 1   | 4-6           |              | [ ]        |       |
| 2   | 4-6           |              | [ ]        |       |
| 3   | 4-6           |              | [ ]        |       |
| 4   | 4-6           |              | [ ]        |       |
| 5   | 4-6           |              | [ ]        |       |
| 6   | 4-6           |              | [ ]        |       |
| 7   | 4-6           |              | [ ]        |       |

---

## Tips for Success

1. **Start with simple examples** before complex ones
2. **Test incrementally** - don't write everything at once
3. **Use psql or pgAdmin** for interactive testing
4. **Read error messages carefully** - PostgreSQL errors are descriptive
5. **Check trigger execution** with SELECT statements
6. **Document as you go** - don't wait until the end
7. **Compare with production code** to validate your approach
8. **Ask for help** when stuck for >30 minutes

---

## Resources

- PostgreSQL Documentation: https://www.postgresql.org/docs/current/
- PL/pgSQL Guide: https://www.postgresql.org/docs/current/plpgsql.html
- Window Functions: https://www.postgresql.org/docs/current/tutorial-window.html
- CTEs: https://www.postgresql.org/docs/current/queries-with.html

---

**Ready to start?** Begin with Day 1 and work through systematically!

**Questions?** Review README.md and mistakes_to_expect.md first!

**Good luck! 🚀**

<!-- Auto-extracted from weeks/**/*.sql by a maintainer script. Regenerate when
     adding new query files. The 'purpose' notes come from the comments in the
     SQL files; expand them in your own words where useful. -->

# SQL Query Catalog

A catalog of the SQL written across the weekly exercises. Each entry shows the
leading comment (purpose) and the statement.

## `weeks/week_02_sql_basics/queries_week2.sql`

**Purpose:** Query 1: List all courses / Learning: Basic SELECT

```sql
SELECT * FROM courses;
```

**Purpose:** Query 2: Find all questions from year 2023 / Learning: WHERE clause with equality

```sql
SELECT question_id, question_text, year, difficulty
FROM questions
WHERE year = 2023;
```

**Purpose:** Query 3: Find all "hard" difficulty questions / Learning: WHERE with string comparison

```sql
SELECT question_id, question_text, difficulty, marks
FROM questions
WHERE difficulty = 'hard';
```

**Purpose:** Query 4: Find all questions worth more than 5 marks / Learning: WHERE with numeric comparison

```sql
SELECT question_id, question_text, marks, year
FROM questions
WHERE marks > 5;
```

**Purpose:** Query 5: Find all midterm exams from 2022 or 2023 / Learning: WHERE with OR and IN

```sql
SELECT question_text, year, exam_type
FROM questions
WHERE exam_type = 'midterm' AND year IN (2022, 2023);
```

**Purpose:** Query 6: List all questions ordered by year (newest first) / Learning: ORDER BY DESC

```sql
SELECT question_id, question_text, year, difficulty
FROM questions
ORDER BY year DESC;
```

**Purpose:** Query 7: Find questions about "normalization" (case-insensitive) / Learning: LIKE pattern matching with ILIKE (PostgreSQL)

```sql
SELECT question_text, topic_name, year
FROM questions
WHERE question_text ILIKE '%normalization%';
```

**Purpose:** Query 8: List all topics, sorted alphabetically / Learning: ORDER BY with text

```sql
SELECT topic_name, description, week_number
FROM topics
ORDER BY topic_name ASC;
```

**Purpose:** Query 9: Find all questions containing "SQL" or "query" / Learning: OR with LIKE

```sql
SELECT question_text, year, difficulty
FROM questions
WHERE question_text ILIKE '%SQL%' OR question_text ILIKE '%query%';
```

**Purpose:** Query 10: Find the 5 most valuable questions (highest marks) / Learning: ORDER BY with LIMIT

```sql
SELECT question_text, marks, difficulty
FROM questions
ORDER BY marks DESC
LIMIT 5;
```

**Purpose:** Query 11: Count total number of questions / Learning: COUNT(*)

```sql
SELECT COUNT(*) AS total_questions FROM questions;
```

**Purpose:** Query 12: Find average marks of all questions / Learning: AVG()

```sql
SELECT AVG(marks) AS average_marks FROM questions;
```

**Purpose:** Query 13: Find maximum and minimum marks / Learning: MAX() and MIN()

```sql
SELECT
    MAX(marks) AS highest_marks,
    MIN(marks) AS lowest_marks,
    MAX(marks) - MIN(marks) AS marks_range
FROM questions;
```

**Purpose:** Query 14: Count questions by difficulty / Learning: COUNT() with GROUP BY

```sql
SELECT difficulty, COUNT(*) AS question_count
FROM questions
GROUP BY difficulty
ORDER BY question_count DESC;
```

**Purpose:** Query 15: Calculate total marks available per year / Learning: SUM() with GROUP BY

```sql
SELECT year, SUM(marks) AS total_marks
FROM questions
GROUP BY year
ORDER BY year DESC;
```

**Purpose:** Query 16: Find topics with more than 3 questions / Learning: GROUP BY with HAVING

```sql
SELECT topic_name, COUNT(*) AS question_count
FROM questions
GROUP BY topic_name
HAVING COUNT(*) > 3
ORDER BY question_count DESC;
```

**Purpose:** Query 17: Find years with average marks > 6 / Learning: HAVING with aggregate condition

```sql
SELECT year, AVG(marks) AS avg_marks, COUNT(*) AS question_count
FROM questions
GROUP BY year
HAVING AVG(marks) > 6
ORDER BY avg_marks DESC;
```

**Purpose:** Query 18: Count questions by exam type and difficulty / Learning: GROUP BY with multiple columns

```sql
SELECT exam_type, difficulty, COUNT(*) AS count
FROM questions
GROUP BY exam_type, difficulty
ORDER BY exam_type, difficulty;
```

**Purpose:** Query 19: Find topics with total marks > 30 / Learning: HAVING with SUM()

```sql
SELECT topic_name, SUM(marks) AS total_marks, COUNT(*) AS question_count
FROM questions
GROUP BY topic_name
HAVING SUM(marks) > 30
ORDER BY total_marks DESC;
```

**Purpose:** Query 20: Find exam types where the average difficulty is "medium" or harder / Learning: Complex GROUP BY with conditional logic

```sql
SELECT
    exam_type,
    COUNT(*) AS total_questions,
    SUM(CASE WHEN difficulty = 'easy' THEN 1 ELSE 0 END) AS easy_count,
    SUM(CASE WHEN difficulty = 'medium' THEN 1 ELSE 0 END) AS medium_count,
    SUM(CASE WHEN difficulty = 'hard' THEN 1 ELSE 0 END) AS hard_count
FROM questions
GROUP BY exam_type
ORDER BY exam_type;
```


## `weeks/week_02_sql_basics/schema_week2.sql`

**Purpose:** Drop tables if they exist (for re-running)

```sql
DROP TABLE IF EXISTS questions CASCADE;
```

**Purpose:** (no description)

```sql
DROP TABLE IF EXISTS topics CASCADE;
```

**Purpose:** (no description)

```sql
DROP TABLE IF EXISTS courses CASCADE;
```

**Purpose:** Table 1: Courses

```sql
CREATE TABLE courses (
    course_id SERIAL PRIMARY KEY,
    course_code VARCHAR(20) UNIQUE NOT NULL,
    course_title VARCHAR(200) NOT NULL,
    semester VARCHAR(20),
    credit INTEGER CHECK (credit > 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Purpose:** Table 2: Topics (intentionally simple for Week 2)

```sql
CREATE TABLE topics (
    topic_id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES courses(course_id) ON DELETE CASCADE,
    topic_name VARCHAR(100) NOT NULL,
    description TEXT,
    week_number INTEGER CHECK (week_number > 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Purpose:** Table 3: Questions (with intentional redundancy for Week 4 lesson) / Intentional redundancy: storing course_code and topic_name again / (will be normalized in Week 4) / Answer (optional)

```sql
CREATE TABLE questions (
    question_id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES courses(course_id) ON DELETE CASCADE,
    topic_id INTEGER REFERENCES topics(topic_id) ON DELETE SET NULL,
    question_text TEXT NOT NULL,

    course_code VARCHAR(20),  -- REDUNDANT!
    topic_name VARCHAR(100),  -- REDUNDANT!

    year INTEGER CHECK (year >= 2010 AND year <= 2030),
    exam_type VARCHAR(50) CHECK (exam_type IN ('midterm', 'final', 'quiz', 'assignment')),
    difficulty VARCHAR(20) CHECK (difficulty IN ('easy', 'medium', 'hard')),
    marks INTEGER CHECK (marks > 0),

    answer_text TEXT,
    answer_reference VARCHAR(200),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Purpose:** Indexes for common queries (Week 7 will cover indexing in detail)

```sql
CREATE INDEX idx_questions_year ON questions(year);
```

**Purpose:** (no description)

```sql
CREATE INDEX idx_questions_difficulty ON questions(difficulty);
```

**Purpose:** (no description)

```sql
CREATE INDEX idx_questions_topic_id ON questions(topic_id);
```

**Purpose:** Comments for learning

```sql
COMMENT ON TABLE courses IS 'Stores academic course information';
```

**Purpose:** (no description)

```sql
COMMENT ON TABLE topics IS 'Stores course topics/chapters';
```

**Purpose:** (no description)

```sql
COMMENT ON TABLE questions IS 'Stores previous-year exam questions (intentionally denormalized for Week 2-3)';
```

**Purpose:** (no description)

```sql
COMMENT ON COLUMN questions.course_code IS 'REDUNDANT - violates 3NF (will fix in Week 4)';
```

**Purpose:** (no description)

```sql
COMMENT ON COLUMN questions.topic_name IS 'REDUNDANT - violates 3NF (will fix in Week 4)';
```


## `weeks/week_02_sql_basics/seed_week2.sql`

**Purpose:** Insert Courses

```sql
INSERT INTO courses (course_code, course_title, semester, credit) VALUES
('CS201', 'Database Management Systems', 'Fall 2024', 4),
('CS202', 'DBMS Lab', 'Fall 2024', 2),
('CS301', 'Advanced Databases', 'Spring 2025', 3);
```

**Purpose:** Insert Topics / CS201 topics / CS301 topics

```sql
INSERT INTO topics (course_id, topic_name, description, week_number) VALUES
(1, 'DBMS Fundamentals', 'Introduction to databases, data models, DBMS architecture', 1),
(1, 'SQL Basics', 'DDL, DML, SELECT queries, filtering, sorting', 2),
(1, 'ER Modeling', 'Entity-Relationship diagrams, cardinality, weak entities', 3),
(1, 'Normalization', 'Functional dependencies, 1NF, 2NF, 3NF, BCNF', 4),
(1, 'Indexing', 'B+ trees, hash indexing, query optimization', 7),
(1, 'Transactions', 'ACID properties, concurrency control, deadlock', 9),

(3, 'Query Optimization', 'Query plans, cost estimation, optimizer', 8),
(3, 'NoSQL Databases', 'Document stores, key-value stores, CAP theorem', 11),
(3, 'Vector Databases', 'Embeddings, similarity search, pgvector', 10);
```

**Purpose:** DBMS Fundamentals Questions / SQL Basics Questions / ER Modeling Questions / Normalization Questions / Indexing Questions / Transactions Questions / Query Optimization Questions / Vector Databases Questions / NoSQL Questions / Additional Mixed Difficulty Questions

```sql
INSERT INTO questions (course_id, topic_id, question_text, course_code, topic_name, year, exam_type, difficulty, marks) VALUES
(1, 1, 'What is a Database Management System (DBMS)? List its advantages over file-based systems.', 'CS201', 'DBMS Fundamentals', 2023, 'midterm', 'easy', 5),
(1, 1, 'Explain the three-level architecture (physical, logical, view) of a DBMS with a diagram.', 'CS201', 'DBMS Fundamentals', 2023, 'final', 'medium', 8),
(1, 1, 'Differentiate between schema and instance with examples.', 'CS201', 'DBMS Fundamentals', 2022, 'midterm', 'easy', 4),
(1, 1, 'What is data independence? Explain physical and logical data independence.', 'CS201', 'DBMS Fundamentals', 2022, 'final', 'medium', 6),

(1, 2, 'Write a SQL query to create a table "students" with columns: student_id (PK), name, age, major.', 'CS201', 'SQL Basics', 2023, 'midterm', 'easy', 3),
(1, 2, 'Write a query to find all students whose age is between 18 and 25.', 'CS201', 'SQL Basics', 2023, 'quiz', 'easy', 2),
(1, 2, 'What is the difference between WHERE and HAVING clauses in SQL? Provide examples.', 'CS201', 'SQL Basics', 2023, 'final', 'medium', 5),
(1, 2, 'Write a query to count the number of students in each major, showing only majors with more than 10 students.', 'CS201', 'SQL Basics', 2022, 'midterm', 'medium', 4),
(1, 2, 'Explain the difference between INNER JOIN, LEFT JOIN, and RIGHT JOIN with examples.', 'CS201', 'SQL Basics', 2022, 'final', 'medium', 6),
(1, 2, 'Write a query to find the second highest salary from an employees table.', 'CS201', 'SQL Basics', 2021, 'final', 'hard', 8),

(1, 3, 'Draw an ER diagram for a university database with entities: Student, Course, Professor, Department.', 'CS201', 'ER Modeling', 2023, 'midterm', 'medium', 10),
(1, 3, 'What is a weak entity? Provide an example with an ER diagram.', 'CS201', 'ER Modeling', 2023, 'final', 'medium', 6),
(1, 3, 'Explain cardinality ratios (1:1, 1:N, M:N) with real-world examples.', 'CS201', 'ER Modeling', 2022, 'midterm', 'easy', 5),
(1, 3, 'Convert the following ER diagram into relational schema: [Student --enrolls-in--> Course] where Student(1) to Course(N).', 'CS201', 'ER Modeling', 2022, 'final', 'medium', 8),
(1, 3, 'What are participation constraints (total vs partial)? Show in an ER diagram.', 'CS201', 'ER Modeling', 2021, 'final', 'medium', 6),

(1, 4, 'Define functional dependency. What is Armstrong''s Axioms?', 'CS201', 'Normalization', 2023, 'midterm', 'medium', 6),
(1, 4, 'Given a relation R(A,B,C,D) with FDs: A→B, B→C, C→D. Find all candidate keys.', 'CS201', 'Normalization', 2023, 'final', 'hard', 10),
(1, 4, 'Explain 1NF, 2NF, 3NF with examples. Show how to convert a table from 1NF to 3NF.', 'CS201', 'Normalization', 2022, 'midterm', 'medium', 8),
(1, 4, 'What is BCNF (Boyce-Codd Normal Form)? How is it different from 3NF?', 'CS201', 'Normalization', 2022, 'final', 'medium', 6),
(1, 4, 'Given a denormalized table with update/deletion/insertion anomalies, normalize it to 3NF.', 'CS201', 'Normalization', 2021, 'final', 'hard', 12),
(1, 4, 'What are multi-valued dependencies? Explain 4NF with an example.', 'CS201', 'Normalization', 2020, 'final', 'hard', 8),

(1, 5, 'What is indexing? Why do we need indexes in databases?', 'CS201', 'Indexing', 2023, 'midterm', 'easy', 4),
(1, 5, 'Explain the structure of a B+ tree. Why is it preferred for database indexing?', 'CS201', 'Indexing', 2023, 'final', 'medium', 8),
(1, 5, 'Compare B+ tree and hash indexing. When would you use each?', 'CS201', 'Indexing', 2022, 'midterm', 'medium', 6),
(1, 5, 'What is the order of a B+ tree? If order is 5, what is the maximum and minimum number of keys in a node?', 'CS201', 'Indexing', 2022, 'final', 'medium', 5),
(1, 5, 'Draw a B+ tree of order 3 and insert the following keys in sequence: 5, 15, 25, 10, 20, 30.', 'CS201', 'Indexing', 2021, 'final', 'hard', 10),
(1, 5, 'What is a clustered index? How is it different from a non-clustered index?', 'CS201', 'Indexing', 2020, 'midterm', 'medium', 6),

(1, 6, 'What are ACID properties? Explain each with examples.', 'CS201', 'Transactions', 2023, 'midterm', 'medium', 8),
(1, 6, 'Define serializability. What is conflict serializability?', 'CS201', 'Transactions', 2023, 'final', 'hard', 10),
(1, 6, 'What is a deadlock? Explain deadlock prevention and detection techniques.', 'CS201', 'Transactions', 2022, 'midterm', 'medium', 8),
(1, 6, 'Explain two-phase locking (2PL) protocol. What is strict 2PL?', 'CS201', 'Transactions', 2022, 'final', 'hard', 10),
(1, 6, 'What is a transaction log? How is it used for recovery?', 'CS201', 'Transactions', 2021, 'midterm', 'medium', 6),
(1, 6, 'Explain lost update, dirty read, and unrepeatable read problems with examples.', 'CS201', 'Transactions', 2021, 'final', 'medium', 8),

(3, 7, 'What is query optimization? Explain the role of a query optimizer.', 'CS301', 'Query Optimization', 2023, 'midterm', 'medium', 6),
(3, 7, 'Explain EXPLAIN ANALYZE in PostgreSQL. How do you read a query plan?', 'CS301', 'Query Optimization', 2023, 'final', 'hard', 10),
(3, 7, 'What is cost-based optimization? How does the optimizer estimate query cost?', 'CS301', 'Query Optimization', 2022, 'final', 'hard', 8),

(3, 9, 'What are text embeddings? How are they used for semantic search?', 'CS301', 'Vector Databases', 2024, 'midterm', 'medium', 6),
(3, 9, 'Explain cosine similarity. Why is it used for comparing embeddings?', 'CS301', 'Vector Databases', 2024, 'final', 'medium', 6),
(3, 9, 'What is pgvector? How does it enable vector similarity search in PostgreSQL?', 'CS301', 'Vector Databases', 2024, 'quiz', 'easy', 4),

(3, 8, 'What is the CAP theorem? Explain with examples of databases.', 'CS301', 'NoSQL Databases', 2023, 'midterm', 'medium', 7),
(3, 8, 'Compare SQL databases and NoSQL databases. When would you use each?', 'CS301', 'NoSQL Databases', 2023, 'final', 'medium', 8),

(1, 2, 'Write a query to find duplicate records in a table based on email.', 'CS201', 'SQL Basics', 2020, 'quiz', 'medium', 4),
(1, 2, 'Explain the difference between DELETE, TRUNCATE, and DROP commands.', 'CS201', 'SQL Basics', 2020, 'midterm', 'easy', 3),
(1, 4, 'What is lossless join decomposition? Prove that a decomposition is lossless.', 'CS201', 'Normalization', 2019, 'final', 'hard', 12),
(1, 5, 'What is bitmap indexing? When is it useful?', 'CS201', 'Indexing', 2019, 'midterm', 'hard', 6),
(1, 6, 'Explain timestamp-based concurrency control protocol.', 'CS201', 'Transactions', 2019, 'final', 'hard', 10),
(1, 1, 'What is data redundancy? Why is it problematic?', 'CS201', 'DBMS Fundamentals', 2021, 'quiz', 'easy', 2),
(1, 3, 'What is an aggregation relationship in ER modeling?', 'CS201', 'ER Modeling', 2020, 'midterm', 'medium', 5);
```


_Total catalogued statements: 37._

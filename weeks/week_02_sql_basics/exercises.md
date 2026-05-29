# Week 2: SQL Exercises (Filled Answer Key)

## 🧭 Navigation

**[← Back to Week 2 Overview](README.md)** | **[Theory Notes](theory_notes.md)** | **[Blank Practice Variant](exercises_blank.md)** | **[Next: Week 3 →](../week_03_er_modeling/README.md)**

---

> **This is the filled answer key.** To practice from scratch first, use the
> learner-blank variant in **[exercises_blank.md](exercises_blank.md)** (same
> prompts, empty answer spaces), then return here to self-check.

## 🎯 Exercise Goals

These exercises build on the Week 2 schema
([schema_week2.sql](schema_week2.sql)) and seed data
([seed_week2.sql](seed_week2.sql)). You will practice:

- Creating tables with the right data types and constraints
- Inserting data while respecting foreign keys
- Filtering with `WHERE`, `LIKE`, `IN`, `BETWEEN`
- Combining tables with `INNER`/`LEFT JOIN`
- Aggregating with `COUNT`/`SUM`/`AVG` + `GROUP BY` + `HAVING`

**Schema recap** (see [schema_week2.sql](schema_week2.sql)):
`courses(course_id, course_code, course_title, semester, credit, ...)`,
`topics(topic_id, course_id, topic_name, description, week_number, ...)`,
`questions(question_id, course_id, topic_id, question_text, course_code,
topic_name, year, exam_type, difficulty, marks, answer_text, ...)`.

> **How to use:** attempt each exercise yourself first, then expand **Solution**
> to self-check. Run them against your local database after `\i schema_week2.sql`
> and `\i seed_week2.sql`.

---

## Exercise Set 1: CREATE TABLE Fundamentals

### Exercise 1.1: Basic Table Creation
Create a simple `students` table with the following attributes:
- student_id (integer, primary key, auto-increment)
- name (text, not null)
- email (text, unique, not null)
- major (text)
- gpa (decimal with 2 places)

**Solution**:
```sql
CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    major TEXT,
    gpa DECIMAL(3,2)
);
```
**Verify**: `\d students` in psql to see structure.

---

### Exercise 1.2: Table with Foreign Key
Create an `enrollments` table that links students to courses. It should have its
own surrogate key, a `student_id` referencing `students`, a `course_id`
referencing `courses`, an `enrolled_on` date defaulting to today, and a `grade`
that may only be one of `'A','B','C','D','F'`. The same student must not be
enrolled in the same course twice.

**Solution**:
```sql
CREATE TABLE enrollments (
    enrollment_id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL REFERENCES students(student_id) ON DELETE CASCADE,
    course_id  INTEGER NOT NULL REFERENCES courses(course_id)  ON DELETE CASCADE,
    enrolled_on DATE DEFAULT CURRENT_DATE,
    grade CHAR(1) CHECK (grade IN ('A','B','C','D','F')),
    UNIQUE (student_id, course_id)   -- no duplicate enrollment
);
```
**Why:** `REFERENCES` enforces referential integrity; `ON DELETE CASCADE`
removes enrollments when a student/course is deleted; the composite `UNIQUE`
constraint prevents double-enrollment; `CHECK` restricts grade values.

---

## Exercise Set 2: INSERT Operations

### Exercise 2.1: Insert a parent row
Insert a course: code `CS201`, title `Database Systems`, semester `Fall 2024`,
4 credits.

**Solution**:
```sql
INSERT INTO courses (course_code, course_title, semester, credit)
VALUES ('CS201', 'Database Systems', 'Fall 2024', 4);
```
**Note:** `course_id` and `created_at` are omitted — `SERIAL` and the `DEFAULT`
fill them automatically.

---

### Exercise 2.2: Insert a child row using the parent key
Add a topic `Normalization` for `CS201`, week 4, with a short description.

**Solution**:
```sql
INSERT INTO topics (course_id, topic_name, description, week_number)
VALUES (
    (SELECT course_id FROM courses WHERE course_code = 'CS201'),
    'Normalization',
    'Decomposing tables to remove anomalies (1NF–BCNF)',
    4
);
```
**Why:** a subquery looks up the parent `course_id` so you don't hard-code it.
Inserting a `course_id` that doesn't exist would fail the foreign key.

---

### Exercise 2.3: Multi-row insert with a constraint violation
Insert two questions for `CS201` in one statement, then explain why the
following row is rejected:
`year = 2050, exam_type = 'popquiz'`.

**Solution**:
```sql
INSERT INTO questions (course_id, topic_id, question_text, year, exam_type, difficulty, marks)
VALUES
  (1, 1, 'Define BCNF and give an example.', 2023, 'final',  'medium', 8),
  (1, 1, 'What is a functional dependency?',  2022, 'midterm','easy',   5);
```
**Why the bad row fails:** `year = 2050` violates `CHECK (year BETWEEN 2010 AND
2030)` and `exam_type = 'popquiz'` violates `CHECK (exam_type IN ('midterm',
'final','quiz','assignment'))`. PostgreSQL rejects the whole statement —
constraints protect data integrity at insert time.

---

## Exercise Set 3: SELECT and WHERE

Write queries to find:

### Exercise 3.1: All questions with difficulty 'medium'
```sql
SELECT question_id, question_text
FROM questions
WHERE difficulty = 'medium';
```

### Exercise 3.2: Questions with marks >= 8
```sql
SELECT question_id, question_text, marks
FROM questions
WHERE marks >= 8;
```

### Exercise 3.3: Questions from 2023
```sql
SELECT question_id, question_text, year
FROM questions
WHERE year = 2023;
```

### Exercise 3.4: Questions containing 'SQL' in the text
```sql
SELECT question_id, question_text
FROM questions
WHERE question_text ILIKE '%SQL%';   -- ILIKE = case-insensitive LIKE
```

### Exercise 3.5: Combine conditions
Find hard questions worth more than 5 marks from 2022 or 2023.
```sql
SELECT question_id, question_text, year, marks
FROM questions
WHERE difficulty = 'hard'
  AND marks > 5
  AND year IN (2022, 2023);
```
**Why:** `ILIKE`/`LIKE` use `%` as a wildcard; `IN (...)` is shorthand for
multiple `OR` equality checks; `AND` combines all predicates.

---

## Exercise Set 4: Joins

### Exercise 4.1: INNER JOIN
List each question's text together with its course title (only questions that
have a matching course).
```sql
SELECT q.question_text, c.course_title
FROM questions AS q
JOIN courses AS c ON q.course_id = c.course_id;
```

### Exercise 4.2: LEFT JOIN
List every topic and the number of questions for it — **including topics with
zero questions**.
```sql
SELECT t.topic_name, COUNT(q.question_id) AS num_questions
FROM topics AS t
LEFT JOIN questions AS q ON q.topic_id = t.topic_id
GROUP BY t.topic_name
ORDER BY num_questions DESC;
```
**Why `LEFT JOIN`:** an `INNER JOIN` would drop topics with no questions. With
`LEFT JOIN`, unmatched topics still appear and `COUNT(q.question_id)` is `0`
(because `COUNT` ignores NULLs).

### Exercise 4.3: Multi-table join
Show question text, topic name, and course code by joining all three tables.
```sql
SELECT q.question_text, t.topic_name, c.course_code
FROM questions AS q
JOIN topics  AS t ON q.topic_id  = t.topic_id
JOIN courses AS c ON q.course_id = c.course_id;
```

---

## Exercise Set 5: Aggregates

### Exercise 5.1: COUNT per difficulty
```sql
SELECT difficulty, COUNT(*) AS num_questions
FROM questions
GROUP BY difficulty
ORDER BY num_questions DESC;
```

### Exercise 5.2: AVG / MAX / MIN of marks per course
```sql
SELECT c.course_code,
       ROUND(AVG(q.marks), 2) AS avg_marks,
       MAX(q.marks) AS max_marks,
       MIN(q.marks) AS min_marks
FROM questions AS q
JOIN courses   AS c ON q.course_id = c.course_id
GROUP BY c.course_code;
```

### Exercise 5.3: HAVING to filter groups
List only the years that have **more than 3** questions.
```sql
SELECT year, COUNT(*) AS num_questions
FROM questions
GROUP BY year
HAVING COUNT(*) > 3
ORDER BY year;
```
**Why `HAVING` not `WHERE`:** `WHERE` filters individual rows *before* grouping;
`HAVING` filters *groups* after aggregation. You cannot use an aggregate like
`COUNT(*)` in a `WHERE` clause.

### Exercise 5.4: SUM with a join and grouping
Total marks available per course, highest first.
```sql
SELECT c.course_code, SUM(q.marks) AS total_marks
FROM questions AS q
JOIN courses   AS c ON q.course_id = c.course_id
GROUP BY c.course_code
ORDER BY total_marks DESC;
```

---

## 🧩 Challenge Exercises (optional)

### Challenge 1: Find duplicates caused by the denormalized schema
The Week 2 schema redundantly stores `course_code` in `questions`. Find any
question whose stored `course_code` disagrees with the course it references
(an *update anomaly* — previewing Week 4).
```sql
SELECT q.question_id, q.course_code AS stored_code, c.course_code AS real_code
FROM questions AS q
JOIN courses   AS c ON q.course_id = c.course_id
WHERE q.course_code IS DISTINCT FROM c.course_code;
```

### Challenge 2: Top topic per difficulty
For each difficulty level, show how many questions exist and the average marks.
```sql
SELECT difficulty,
       COUNT(*)              AS num_questions,
       ROUND(AVG(marks), 2)  AS avg_marks
FROM questions
GROUP BY difficulty
ORDER BY avg_marks DESC;
```

---

## Self-Assessment

Rate your confidence (1-5):
- [ ] Creating tables with constraints
- [ ] Writing WHERE clauses (`LIKE`, `IN`, `BETWEEN`)
- [ ] Using aggregate functions
- [ ] Writing INNER vs LEFT JOIN queries
- [ ] Understanding GROUP BY vs HAVING

**Ready for Week 3?** ☐ Yes ☐ Need more practice

---

## 🧭 Navigation

**[← Back to Week 2 Overview](README.md)** | **[Theory Notes](theory_notes.md)** | **[Next: Week 3 →](../week_03_er_modeling/README.md)**

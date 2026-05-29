# Week 2: SQL Exercises (Learner-Blank Variant)

## 🧭 Navigation

**[← Back to Week 2 Overview](README.md)** | **[Theory Notes](theory_notes.md)** | **[Filled Answer Key →](exercises.md)** | **[Next: Week 3 →](../week_03_er_modeling/README.md)**

---

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

> **How to use this file:** this is the *blank* practice variant. Write your own
> answer in each empty code block first, run it against your local database after
> `\i schema_week2.sql` and `\i seed_week2.sql`, then check yourself against the
> filled answer key in **[exercises.md](exercises.md)**.

---

## Exercise Set 1: CREATE TABLE Fundamentals

### Exercise 1.1: Basic Table Creation
Create a simple `students` table with the following attributes:
- student_id (integer, primary key, auto-increment)
- name (text, not null)
- email (text, unique, not null)
- major (text)
- gpa (decimal with 2 places)

Your attempt:

```sql

```
**Verify**: `\d students` in psql to see structure.

---

### Exercise 1.2: Table with Foreign Key
Create an `enrollments` table that links students to courses. It should have its
own surrogate key, a `student_id` referencing `students`, a `course_id`
referencing `courses`, an `enrolled_on` date defaulting to today, and a `grade`
that may only be one of `'A','B','C','D','F'`. The same student must not be
enrolled in the same course twice.

Your attempt:

```sql

```

---

## Exercise Set 2: INSERT Operations

### Exercise 2.1: Insert a parent row
Insert a course: code `CS201`, title `Database Systems`, semester `Fall 2024`,
4 credits.

Your attempt:

```sql

```

---

### Exercise 2.2: Insert a child row using the parent key
Add a topic `Normalization` for `CS201`, week 4, with a short description.

Your attempt:

```sql

```

---

### Exercise 2.3: Multi-row insert with a constraint violation
Insert two questions for `CS201` in one statement, then explain why the
following row is rejected:
`year = 2050, exam_type = 'popquiz'`.

Your attempt:

```sql

```

Your explanation of why the bad row fails:

```

```

---

## Exercise Set 3: SELECT and WHERE

Write queries to find:

### Exercise 3.1: All questions with difficulty 'medium'

```sql

```

### Exercise 3.2: Questions with marks >= 8

```sql

```

### Exercise 3.3: Questions from 2023

```sql

```

### Exercise 3.4: Questions containing 'SQL' in the text

```sql

```

### Exercise 3.5: Combine conditions
Find hard questions worth more than 5 marks from 2022 or 2023.

```sql

```

---

## Exercise Set 4: Joins

### Exercise 4.1: INNER JOIN
List each question's text together with its course title (only questions that
have a matching course).

```sql

```

### Exercise 4.2: LEFT JOIN
List every topic and the number of questions for it — **including topics with
zero questions**.

```sql

```

### Exercise 4.3: Multi-table join
Show question text, topic name, and course code by joining all three tables.

```sql

```

---

## Exercise Set 5: Aggregates

### Exercise 5.1: COUNT per difficulty

```sql

```

### Exercise 5.2: AVG / MAX / MIN of marks per course

```sql

```

### Exercise 5.3: HAVING to filter groups
List only the years that have **more than 3** questions.

```sql

```

### Exercise 5.4: SUM with a join and grouping
Total marks available per course, highest first.

```sql

```

---

## 🧩 Challenge Exercises (optional)

### Challenge 1: Find duplicates caused by the denormalized schema
The Week 2 schema redundantly stores `course_code` in `questions`. Find any
question whose stored `course_code` disagrees with the course it references
(an *update anomaly* — previewing Week 4).

```sql

```

### Challenge 2: Top topic per difficulty
For each difficulty level, show how many questions exist and the average marks.

```sql

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

> Finished attempting? Compare every answer with the worked solutions and *why*
> notes in **[exercises.md](exercises.md)** (the filled answer key).

---

## 🧭 Navigation

**[← Back to Week 2 Overview](README.md)** | **[Theory Notes](theory_notes.md)** | **[Filled Answer Key →](exercises.md)** | **[Next: Week 3 →](../week_03_er_modeling/README.md)**

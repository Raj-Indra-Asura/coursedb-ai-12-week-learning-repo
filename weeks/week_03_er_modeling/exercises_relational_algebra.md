<!-- DO NOT auto-fill. Questions only. Provide your own SQL translations in the
     blank code blocks. No answers are written here. -->

# Week 3 (supplement): Relational Algebra Exercises

For each problem, write the relational-algebra expression AND its SQL
translation against the CourseDB-AI schema (`app/db/models.py`). Blank space is
left for your answers.

Relations available include: `courses(course_id, course_code, course_name, ...)`,
`topics(topic_id, course_id, topic_name, ...)`,
`questions(question_id, topic_id, course_id, year, difficulty, marks, ...)`,
`resources(resource_id, topic_id, course_id, title, year_published, ...)`.

---

## Problem 1 — Selection & Projection

List the titles of all resources published after 2020.

Relational algebra:

```
-- TODO(learner):
```

SQL:

```sql
-- TODO(learner):
```

---

## Problem 2 — Join

List each question's text together with its course name.

Relational algebra:

```
-- TODO(learner):
```

SQL:

```sql
-- TODO(learner):
```

---

## Problem 3 — Aggregation / Grouping

Count the number of questions per difficulty level.

Relational algebra (extended RA with grouping):

```
-- TODO(learner):
```

SQL:

```sql
-- TODO(learner):
```

---

## Problem 4 — Set operation

Find topics that have at least one question but no resource.

Relational algebra:

```
-- TODO(learner):
```

SQL:

```sql
-- TODO(learner):
```

---

## Problem 5 — Division / "for all"

Find courses for which resources exist covering every one of their topics.

Relational algebra:

```
-- TODO(learner):
```

SQL:

```sql
-- TODO(learner):
```

# Week 3 (supplement): Relational Algebra Exercises

## 🧭 Navigation

**[← Back to Week 3 Exercises](exercises.md)** | **[Week 3 Overview](README.md)**

For each problem, write the relational-algebra expression **and** its SQL
translation against the CourseDB-AI schema (`app/db/models.py`), then check
yourself against the worked answer.

Relations available include: `courses(course_id, course_code, course_name, ...)`,
`topics(topic_id, course_id, topic_name, ...)`,
`questions(question_id, topic_id, course_id, year, difficulty, marks, ...)`,
`resources(resource_id, topic_id, course_id, title, year_published, ...)`.

### Relational-algebra operator reference

| Symbol | Name | Meaning |
|--------|------|---------|
| σ (sigma) | Selection | keep rows matching a predicate |
| π (pi) | Projection | keep listed columns (removes duplicates) |
| ⋈ | Natural / theta join | combine rows across relations on a condition |
| ∪ ∩ − | Union / Intersect / Difference | set operations (union-compatible relations) |
| ρ (rho) | Rename | rename a relation/attribute |
| 𝒢 (gamma) | Grouping/aggregation | extended RA: group + aggregate |
| ÷ | Division | "for all" — rows related to *every* value in a set |

> **How to use this file:** attempt each problem in the blank space first, then
> expand the **Answer**. The answers show the relational algebra, the SQL, and a
> short note on *why* — this is your self-correction key.

---

## Problem 1 — Selection & Projection

List the titles of all resources published after 2020.

Your attempt (relational algebra):

```
```

Your attempt (SQL):

```sql
```

<details>
<summary><strong>Answer</strong></summary>

Relational algebra:

```
π_title ( σ_year_published > 2020 (resources) )
```

SQL:

```sql
SELECT DISTINCT title
FROM resources
WHERE year_published > 2020;
```

**Why:** `σ` (selection) filters rows where `year_published > 2020`; `π`
(projection) keeps only the `title` column. Projection in pure relational
algebra removes duplicates, which is why the SQL uses `DISTINCT` to match the
algebra exactly.
</details>

---

## Problem 2 — Join

List each question's text together with its course name.

Your attempt (relational algebra):

```
```

Your attempt (SQL):

```sql
```

<details>
<summary><strong>Answer</strong></summary>

Relational algebra:

```
π_question_text, course_name ( questions ⋈_questions.course_id = courses.course_id courses )
```

(Using natural join, since both share `course_id`:
`π_question_text, course_name (questions ⋈ courses)`.)

SQL:

```sql
SELECT q.question_text, c.course_name
FROM questions AS q
JOIN courses AS c ON q.course_id = c.course_id;
```

**Why:** the join (`⋈`) matches each question to its course on the shared
`course_id` foreign key; projection keeps the two requested columns. An inner
join drops questions whose `course_id` has no matching course (there are none if
the FK constraint holds).
</details>

---

## Problem 3 — Aggregation / Grouping

Count the number of questions per difficulty level.

Your attempt (relational algebra):

```
```

Your attempt (SQL):

```sql
```

<details>
<summary><strong>Answer</strong></summary>

Relational algebra (extended RA with grouping):

```
difficulty 𝒢 COUNT(question_id) → num_questions (questions)
```

SQL:

```sql
SELECT difficulty, COUNT(question_id) AS num_questions
FROM questions
GROUP BY difficulty;
```

**Why:** the grouping operator `𝒢` partitions `questions` by `difficulty` and
applies `COUNT` within each group. The grouping attribute(s) on the left of `𝒢`
correspond exactly to SQL's `GROUP BY` columns; aggregates that aren't grouping
keys must appear inside an aggregate function.
</details>

---

## Problem 4 — Set operation

Find topics that have at least one question but no resource.

Your attempt (relational algebra):

```
```

Your attempt (SQL):

```sql
```

<details>
<summary><strong>Answer</strong></summary>

Relational algebra (difference of the topic-id sets):

```
π_topic_id (questions) − π_topic_id (resources)
```

SQL (set difference):

```sql
SELECT topic_id FROM questions
EXCEPT
SELECT topic_id FROM resources;
```

Equivalent anti-join form:

```sql
SELECT DISTINCT q.topic_id
FROM questions AS q
WHERE NOT EXISTS (
    SELECT 1 FROM resources AS r WHERE r.topic_id = q.topic_id
);
```

**Why:** project the set of `topic_id`s that appear in `questions`, then subtract
(`−` / `EXCEPT`) the set that appears in `resources`. What remains are topics with
questions but no resources. The two relations must be **union-compatible** (same
attribute, `topic_id`) for the set difference to be valid.
</details>

---

## Problem 5 — Division / "for all"

Find courses for which resources exist covering every one of their topics.

Your attempt (relational algebra):

```
```

Your attempt (SQL):

```sql
```

<details>
<summary><strong>Answer</strong></summary>

Relational algebra (division — the "for all" operator):

```
Let CourseTopics       = π_course_id, topic_id (topics)
Let CoveredCourseTopics = π_course_id, topic_id (resources)

Answer = CoveredCourseTopics ÷ π_topic_id(...)   -- conceptually, per course
```

More precisely, a course qualifies if **for every** topic of that course there
exists a resource for that (course, topic). Division expresses this directly:

```
π_course_id, topic_id (resources)  ÷  π_topic_id (topics)
```

…restricted per course. Because plain division compares against a *single*
divisor set, the per-course "for all" is most clearly written with the
double-negation pattern below.

SQL (double-negation / "no topic left uncovered"):

```sql
SELECT c.course_id, c.course_name
FROM courses AS c
WHERE NOT EXISTS (                       -- there is no topic of this course ...
    SELECT 1
    FROM topics AS t
    WHERE t.course_id = c.course_id
      AND NOT EXISTS (                   -- ... that lacks a covering resource
          SELECT 1
          FROM resources AS r
          WHERE r.course_id = c.course_id
            AND r.topic_id  = t.topic_id
      )
);
```

**Why:** relational **division** answers "for all" questions. "Resources cover
*every* topic of the course" = "there is **no** topic of the course for which a
resource does **not** exist." That double-negation (`NOT EXISTS (… NOT EXISTS …)`)
is the standard SQL idiom for division, since SQL has no direct `÷` operator.
</details>

---

## 🧭 Navigation

**[← Back to Week 3 Exercises](exercises.md)** | **[Week 3 Overview](README.md)** | **[Next: Week 4 →](../week_04_normalization/README.md)**

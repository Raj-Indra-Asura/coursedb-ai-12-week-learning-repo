<!-- Template. The view/trigger DDL may be filled in by a maintainer; the
     "why / explanation" prose is the learner's. -->

# Views and Triggers

## Views

| View name | Purpose | Base tables |
| --------- | ------- | ----------- |
|  |  |  |

### DDL

```sql
-- Example skeleton. Replace with your own view.
-- CREATE OR REPLACE VIEW v_course_question_counts AS
-- SELECT c.course_code, count(q.question_id) AS question_count
-- FROM courses c
-- LEFT JOIN questions q ON q.course_id = c.course_id
-- GROUP BY c.course_code;
```

> **TODO(learner):** Explain why this view is useful and when to prefer it over a
> raw query.

## Triggers

| Trigger name | Event | Table | Action |
| ------------ | ----- | ----- | ------ |
|  |  |  |  |

### DDL

```sql
-- Example skeleton. Replace with your own trigger + function.
-- CREATE OR REPLACE FUNCTION set_updated_at() RETURNS trigger AS $$
-- BEGIN
--   NEW.updated_at = now();
--   RETURN NEW;
-- END;
-- $$ LANGUAGE plpgsql;
```

> **TODO(learner):** Describe the invariant each trigger enforces.

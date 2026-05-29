<!-- Structured template only. Fill the analysis rows yourself. No AI-authored prose. -->

# Normalization Report

Work each base table from `app/db/models.py` up through the normal forms.

## How to use this template

For every table, fill the row for each normal form with either a check (✔) plus
a one-line justification, or the decomposition you would apply.

## Per-table analysis

### `courses`

| Normal form | Holds? | Justification / decomposition |
| ----------- | ------ | ----------------------------- |
| 1NF |  |  |
| 2NF |  |  |
| 3NF |  |  |
| BCNF |  |  |

### `topics`

| Normal form | Holds? | Justification / decomposition |
| ----------- | ------ | ----------------------------- |
| 1NF |  |  |
| 2NF |  |  |
| 3NF |  |  |
| BCNF |  |  |

### `questions`

> Note: `questions` intentionally duplicates `course_code` and `topic_name`
> (denormalization for a Week 4 lesson).

| Normal form | Holds? | Justification / decomposition |
| ----------- | ------ | ----------------------------- |
| 1NF |  |  |
| 2NF |  |  |
| 3NF |  |  |
| BCNF |  |  |

### `resources`

| Normal form | Holds? | Justification / decomposition |
| ----------- | ------ | ----------------------------- |
| 1NF |  |  |
| 2NF |  |  |
| 3NF |  |  |
| BCNF |  |  |

> **TODO(learner):** Add the remaining tables (`resource_chunks`,
> `chunk_embeddings`, `users`, `search_logs`) following the same format.

## Summary

> **TODO(learner):** State the highest normal form your schema satisfies and any
> deliberate exceptions.

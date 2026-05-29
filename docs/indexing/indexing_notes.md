<!-- Template only. Diagrams and EXPLAIN output welcome; the conceptual prose is
     the learner's. No AI-authored explanation. -->

# Indexing Notes

## Indexes in this project

| Index | Table.column(s) | Type | Why |
| ----- | --------------- | ---- | --- |
|  |  |  |  |

> Hint: extract the declared indexes from `app/db/models.py` and
> `scripts/setup_db.py`.

## When does an index help?

> **TODO(learner):** Summarize the access patterns that benefit from each index.

## Cost of indexes

> **TODO(learner):** Note the write/storage overhead trade-off.

## Self-check questions

1. What is the difference between a clustered and a non-clustered index?
2. When would a B-tree index NOT be used by the planner?
3. Why does pgvector use IVFFlat / HNSW rather than a B-tree for vectors?

> **Notes:**

<!-- Template only. Provide your own examples. -->

# Concurrency Problems

Demonstrate each classic anomaly and the isolation level that prevents it.

| Problem | Two-session scenario | Prevented at level |
| ------- | -------------------- | ------------------ |
| Dirty read |  |  |
| Non-repeatable read |  |  |
| Phantom read |  |  |
| Lost update |  |  |
| Write skew |  |  |

## Worked example: dirty read

```sql
-- Session A
-- Session B
```

> **TODO(learner):** Narrate the interleaving and the wrong result.

## Worked example: deadlock

> **TODO(learner):** Use the wait-for-graph simulator to reproduce a 2-cycle and
> explain the victim-selection.

## Self-check questions

1. Which anomalies does `READ COMMITTED` still allow?
2. How does MVCC avoid read locks?
3. What is the difference between a lost update and write skew?

> **Notes:**

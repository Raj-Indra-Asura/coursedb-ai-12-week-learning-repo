<!-- Template only. The conceptual explanation is the learner's. -->

# Transaction Notes

## ACID at a glance

| Property | One-line meaning (your words) | How PostgreSQL provides it |
| -------- | ----------------------------- | -------------------------- |
| Atomicity |  |  |
| Consistency |  |  |
| Isolation |  |  |
| Durability |  |  |

## Isolation levels

| Level | Dirty read | Non-repeatable read | Phantom |
| ----- | ---------- | ------------------- | ------- |
| Read uncommitted |  |  |  |
| Read committed |  |  |  |
| Repeatable read |  |  |  |
| Serializable |  |  |  |

> **TODO(learner):** Fill the matrix and note PostgreSQL's default level.

## Deadlock & the wait-for graph

Reference: `dbms_internals/transactions/wait_for_graph.py`.

> **TODO(learner):** Explain how a cycle in the wait-for graph indicates a
> deadlock, using the simulator output.

## Self-check questions

1. What is the difference between consistency in ACID and in CAP?
2. How does 2-phase locking guarantee serializability?
3. What does PostgreSQL do when it detects a deadlock?

> **Notes:**

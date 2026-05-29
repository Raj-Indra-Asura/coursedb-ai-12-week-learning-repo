<!-- Template only. Provide your own runnable examples. -->

# ACID Examples

For each property, give a concrete SQL session (two terminals where relevant)
that demonstrates the property holding or being violated.

## Atomicity

```sql
-- BEGIN; ... ROLLBACK; show partial work is undone
```

> **TODO(learner):** Describe the expected outcome.

## Consistency

```sql
-- Violate a CHECK / FK and show the transaction aborts
```

> **TODO(learner):**

## Isolation

```sql
-- Session A and Session B interleaving; show the chosen isolation level's effect
```

> **TODO(learner):**

## Durability

> **TODO(learner):** Describe how a committed transaction survives a crash (WAL),
> and how you would demonstrate it.

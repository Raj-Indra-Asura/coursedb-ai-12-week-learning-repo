# Further Study: Operational & Advanced DBMS Topics

> 📘 **Scope note:** The 12-week curriculum deliberately focuses on the
> fundamentals you need to *build and reason about* a real database-backed
> application (schema design, SQL, internals, transactions, semantic search).
> The topics below are standard in a full "production DBA / distributed systems"
> course but are **out of scope as graded weeks**. This appendix exists so you
> know they exist, understand roughly what they are, and have starting points
> for self-study after Week 12.
>
> Where the repo already has a (learner-fill) stub for a topic, it is linked.

---

## 1. Backup & Recovery / Point-in-Time Recovery (PITR)

**What it is:** Strategies to restore a database after failure or human error —
logical dumps (`pg_dump`), physical base backups, and continuous WAL archiving
that lets you replay to a specific moment.

- Related stub in repo: `weeks/week_09_*/theory_notes_recovery.md` (WAL notes).
- Start here: PostgreSQL docs — *Backup and Restore*, *Continuous Archiving and
  Point-in-Time Recovery (PITR)*.
- Try: take a `pg_dump`, drop a table, and restore it; then experiment with
  `pg_basebackup` + WAL replay.

## 2. Replication / High Availability / Failover

**What it is:** Keeping one or more standby copies of the database in sync with
a primary so the system survives node failure and can scale reads.

- Concepts: streaming replication, synchronous vs. asynchronous, read replicas,
  automatic failover (e.g., Patroni), logical replication for selective sync.
- Start here: PostgreSQL docs — *High Availability, Load Balancing, and
  Replication*.
- Try: set up a primary + one streaming replica with two Docker containers and
  observe replication lag.

## 3. Security in Depth

**What it is:** Beyond "have a password" — controlling exactly who can do what,
and protecting data at rest and in transit.

- Topics: role-based access control (RBAC), `GRANT`/`REVOKE`, row-level security
  (RLS), column-level privileges, `SECURITY DEFINER` functions, TLS, and
  encryption at rest.
- Related stub in repo: `weeks/week_06_*/theory_notes_access_control.md`.
- ⚠️ See also the **insecure demo** callout in
  `weeks/week_11_frontend_integration/theory_notes.md` — never ship hardcoded
  passwords.
- Start here: PostgreSQL docs — *Database Roles and Privileges*, *Row Security
  Policies*.

## 4. Partitioning & Sharding

**What it is:** Splitting large tables (partitioning, within one server) or the
whole dataset (sharding, across servers) so queries and maintenance stay fast at
scale.

- Topics: range/list/hash partitioning, partition pruning, declarative
  partitioning, and application-level vs. middleware sharding.
- Start here: PostgreSQL docs — *Table Partitioning*.
- Try: partition the `questions` table by `academic_year` and inspect how
  `EXPLAIN` prunes partitions (ties into Week 8).

## 5. Monitoring, Tuning & Operations

**What it is:** Keeping a running database healthy and fast.

- Topics: `EXPLAIN (ANALYZE, BUFFERS)`, `pg_stat_*` views, autovacuum tuning,
  connection pooling (PgBouncer), `work_mem`/`shared_buffers`, slow-query logs.
- Ties into: Week 7 (indexing) and Week 8 (query optimization).
- Start here: PostgreSQL docs — *Monitoring Database Activity*, *The Statistics
  Collector*.

## 6. Distributed / NoSQL / Object-Relational Models

**What it is:** Alternatives and extensions to the classic relational model.

- Related (learner-fill bonus) stubs in repo:
  - `weeks/week_12_*/theory_notes_distributed.md`
  - `weeks/week_12_*/theory_notes_nosql_intro.md`
  - `weeks/week_12_*/theory_notes_oo_object_relational.md`
  - `weeks/week_12_*/theory_notes_semi_structured.md`
- Topics: CAP theorem, eventual consistency, document/key-value/column/graph
  stores, JSON/JSONB in PostgreSQL, and object-relational mapping.

---

## How to use this appendix

1. Finish the 12 graded weeks first — they give you the foundation these topics
   build on.
2. Pick one area that matches your goals (e.g., backup/recovery for an
   operations role; partitioning for scale).
3. Do the small "Try" experiment for that topic against your local
   `docker-compose` PostgreSQL + pgvector instance.

> These topics are **optional further study**, not required to "complete" the
> repository.

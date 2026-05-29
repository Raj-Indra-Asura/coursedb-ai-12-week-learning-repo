# Week 12 (supplement): Distributed Databases — Theory Notes

## 🧭 Navigation

**[← Back to Week 12 Theory](theory_notes.md)** | **[Week 12 Overview](README.md)**

> One of four "breadth" supplements for Week 12 that round out your DBMS
> education beyond the single-node relational model you built CourseDB-AI on:
> **distributed databases**, [NoSQL](theory_notes_nosql_intro.md),
> [object/object-relational](theory_notes_oo_object_relational.md), and
> [semi-structured data](theory_notes_semi_structured.md).

---

## Learning objectives

- [x] Explain what a distributed database is and why it is used.
- [x] Describe sharding (horizontal partitioning) and replication.
- [x] State the CAP theorem and its trade-offs.
- [x] Explain the two-phase commit (2PC) protocol.

## Read these references

- Silberschatz, *Database System Concepts*, "Distributed Databases" chapter.
- Brewer, "CAP Twelve Years Later".
- PostgreSQL docs: partitioning and logical replication.

---

## 1. Distributed DB intro

A **distributed database** stores data across **multiple machines (nodes)** that
cooperate to look, as much as possible, like a single logical database. We
distribute for four main reasons:

- **Scalability** — one machine eventually runs out of CPU, RAM, or disk; many
  machines share the load.
- **Availability** — if one node fails, others keep serving.
- **Latency / locality** — keep data near the users who read it (e.g. EU data in
  Europe).
- **Throughput** — parallelize reads and writes across nodes.

The cost is **complexity**: nodes communicate over an unreliable network, so we
must reason about partial failure, consistency, and coordination — problems that
do not exist on a single node.

Two orthogonal techniques achieve distribution: **partitioning (sharding)** and
**replication**. Most real systems use both.

---

## 2. Sharding & partitioning

**Sharding** = **horizontal partitioning**: split a table's *rows* across nodes,
each node holding a disjoint subset (a *shard*). Each shard has the same schema
but different rows. (Contrast **vertical partitioning**, which splits *columns*.)

Common shard-key strategies:

| Strategy | How rows map to shards | Strength | Weakness |
|----------|------------------------|----------|----------|
| **Range** | by key ranges (A–M, N–Z) | efficient range scans | hot spots if keys skew |
| **Hash** | `hash(key) % N` | even distribution | range queries hit all shards |
| **Directory/lookup** | explicit map of key → shard | flexible | the map is itself a dependency |

```sql
-- PostgreSQL declarative partitioning (single-node, but same idea)
CREATE TABLE questions (
    question_id int, year int, ...
) PARTITION BY RANGE (year);

CREATE TABLE questions_2023 PARTITION OF questions
    FOR VALUES FROM (2023) TO (2024);
```

Choosing the **shard key** is the most important decision: a good key spreads
load evenly *and* keeps queries local to one shard. A bad key creates
**hot spots** (one shard overloaded) or forces **scatter-gather** queries that
touch every shard.

---

## 3. Replication

**Replication** keeps **copies** of the same data on multiple nodes for
availability and read scaling.

- **Single-leader (primary/replica):** all writes go to one leader, which
  streams its changes (WAL — see [Week 9 recovery notes](../week_09_transactions/theory_notes_recovery.md))
  to read-only replicas. Simple; the leader is a write bottleneck and a failover
  point. This is PostgreSQL's built-in streaming/logical replication.
- **Multi-leader:** multiple nodes accept writes (e.g. one per region). Better
  write availability, but **conflicts** must be resolved.
- **Leaderless (quorum):** clients write to several nodes and read from several;
  consistency is tuned with quorum sizes `W + R > N` (Dynamo, Cassandra).

Replication can be **synchronous** (a write waits for replicas to confirm —
durable but slower) or **asynchronous** (fast, but replicas lag and a leader
crash can lose the most recent writes). This is the same durability-vs-latency
trade-off as `synchronous_commit` in Week 9, now across machines.

---

## 4. CAP theorem

**CAP** (Brewer): a distributed data store can guarantee at most **two** of:

- **C — Consistency:** every read sees the most recent write (a single, linear
  view).
- **A — Availability:** every request to a non-failed node gets a (non-error)
  response.
- **P — Partition tolerance:** the system keeps working despite the network
  dropping/delaying messages between nodes.

In a real network **partitions happen**, so P is not optional. The real choice
is what to sacrifice **during a partition**:

- **CP** — refuse/block requests on the minority side to preserve consistency
  (e.g. a strongly-consistent store, HBase, ZooKeeper).
- **AP** — keep answering on both sides and reconcile later, accepting that
  reads may be **stale** (e.g. Cassandra, DynamoDB in default mode).

> CAP is about behaviour **under partition**. When the network is healthy, a
> well-built system can deliver both consistency and availability — that nuance
> is the point of Brewer's "CAP Twelve Years Later". See also **PACELC**: *if
> Partition then choose A or C, Else choose Latency or Consistency.*

---

## 5. Two-phase commit (2PC)

To make a **single transaction span multiple nodes atomically**, we need an
agreement protocol. **2PC** uses a **coordinator** and **participants**:

```
Phase 1 — PREPARE (voting):
  Coordinator -> all participants: "PREPARE"
  Each participant: do the work, write it durably to its log, reply YES or NO.
  (A YES is a binding promise it CAN commit if asked.)

Phase 2 — COMMIT / ABORT (decision):
  If ALL voted YES -> Coordinator: "COMMIT" to all.
  If ANY voted NO   -> Coordinator: "ABORT"  to all.
  Participants apply the decision and acknowledge.
```

**Why 2PC can block:** if the coordinator crashes *after* participants voted YES
but *before* sending the decision, a participant is stuck "in doubt" — it
promised to commit, cannot unilaterally decide, and must wait for the
coordinator to recover. This is the classic blocking problem.

**3PC** adds an extra "pre-commit" round so participants can reach a decision
among themselves if the coordinator dies, reducing (but not eliminating, under
arbitrary failures) blocking. In practice modern systems prefer consensus
protocols (**Paxos**, **Raft**) that tolerate failures more gracefully.

PostgreSQL exposes 2PC via `PREPARE TRANSACTION` / `COMMIT PREPARED`.

---

## How this connects to CourseDB-AI

- CourseDB-AI runs on a **single PostgreSQL node** — perfect for learning, and
  it avoids every problem above. Recognizing *when* you'd need to distribute
  (data outgrows one machine, global users, HA requirements) is the skill.
- The `synchronous_commit` durability trade-off from Week 9 reappears here as
  **synchronous vs asynchronous replication**.
- PostgreSQL **declarative partitioning** (shown in §2) lets you practice the
  sharding *concept* on one node before ever needing a cluster.

---

## Self-check questions

1. What is the difference between sharding and replication?
2. Under a network partition, what does a CP system sacrifice compared to an AP
   system?
3. Why can 2PC block, and what does 3PC attempt to fix?
4. Give one workload that suits horizontal sharding and one that does not.
5. How does CAP relate to the ACID vs BASE distinction?

### Answers

1. **Sharding** splits *different* rows across nodes (each datum lives on one
   shard) for capacity and write scaling. **Replication** keeps *copies* of the
   *same* data on several nodes for availability and read scaling. They are
   complementary and usually combined.
2. A **CP** system sacrifices **availability**: the minority side of the
   partition returns errors / blocks rather than serve possibly-stale data. An
   **AP** system sacrifices **consistency**: both sides keep answering and may
   return stale reads, reconciling once the partition heals.
3. 2PC blocks because a participant that voted YES cannot decide on its own; if
   the coordinator crashes before broadcasting the decision, the participant is
   stuck "in doubt". **3PC** inserts a pre-commit phase so surviving
   participants can agree on the outcome without the coordinator, reducing
   blocking (though not under all failure models).
4. **Suits sharding:** a large, high-volume table with an even, well-chosen key
   (e.g. events keyed by user_id) where most queries hit one shard.
   **Does not:** workloads dominated by cross-entity joins or range scans that
   would scatter-gather across all shards, or small datasets where a single node
   suffices.
5. **ACID** (traditional relational) favors strong **consistency** — the CP side
   of CAP. **BASE** (Basically Available, Soft state, Eventual consistency)
   favors **availability** — the AP side. CAP explains the trade-off that pushes
   many distributed NoSQL systems from ACID toward BASE.

---

## Notes

Use this space to sketch a shard-key choice for one CourseDB-AI table if it grew
to billions of rows, and justify why your key avoids hot spots.

---

## 🧭 Navigation

**[← Back to Week 12 Theory](theory_notes.md)** | **[Next supplement: NoSQL →](theory_notes_nosql_intro.md)**

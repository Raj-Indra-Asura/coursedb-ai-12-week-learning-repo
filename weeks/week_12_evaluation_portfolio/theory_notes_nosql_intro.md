# Week 12 (supplement): NoSQL Introduction — Theory Notes

## 🧭 Navigation

**[← Back to Week 12 Theory](theory_notes.md)** | **[Week 12 Overview](README.md)**

> One of four breadth supplements for Week 12. Read the
> [distributed databases](theory_notes_distributed.md) supplement first — NoSQL
> systems are largely a response to the scaling and CAP trade-offs described
> there.

---

## Learning objectives

- [x] Describe the four main NoSQL families.
- [x] Relate each family to CAP trade-offs.
- [x] Explain when NoSQL is preferable to a relational DB.

## Read these references

- Sadalage & Fowler, *NoSQL Distilled*.
- MongoDB / Redis / Cassandra / Neo4j documentation overviews.

---

## 0. What "NoSQL" means

"NoSQL" ("Not Only SQL") is an umbrella for databases that **drop one or more
relational assumptions** — fixed schema, normalized tables, joins, or strong
ACID consistency — usually to gain **horizontal scalability**, **flexible
schemas**, or a **data model that fits the problem better**. They typically
favor **BASE** (eventually consistent) over **ACID**, trading consistency for
availability and partition tolerance (the AP side of CAP).

There are four classic families.

---

## 1. Document stores

Store **self-contained documents** (JSON/BSON), each a nested structure of
keys/values/arrays. No fixed schema — documents in a collection can differ.

```json
// a "question" document — related data nested in one record
{
  "_id": "q123",
  "text": "What is normalization?",
  "difficulty": "medium",
  "topic": { "id": 4, "name": "Normalization" },
  "tags": ["1NF", "2NF", "BCNF"]
}
```

- **Strength:** flexible/evolving schema; one read fetches a whole aggregate (no
  joins); maps naturally to application objects.
- **Weakness:** cross-document joins are weak; duplication risks anomalies (the
  very thing normalization in [Week 4](../week_04_normalization/theory_notes.md)
  prevents).
- **Products:** MongoDB, Couchbase, Amazon DocumentDB.

---

## 2. Key-value stores

The simplest model: a giant distributed **hash map** of `key → opaque value`.
Lookups by key are O(1)-ish and extremely fast; the store doesn't interpret the
value.

```
SET  session:abc123  "{user: 42, exp: ...}"
GET  session:abc123
```

- **Strength:** lowest latency, trivially shardable by key; ideal for caches,
  sessions, feature flags, rate limiters.
- **Weakness:** can only query by key — no rich queries, no joins.
- **Products:** Redis, Amazon DynamoDB (in its KV mode), Riak.

This is the same **hashing** idea you implemented in
[Week 7's hash index](../../dbms_internals/hash_index/), scaled across a cluster.

---

## 3. Column-family (wide-column) stores

Data is grouped into **column families**; each row can have billions of sparse
columns, and columns are stored together on disk for efficient scans of a few
columns over many rows. Optimized for **massive write throughput** and
time-series / analytics workloads.

- **Strength:** linear write scaling, tunable consistency, great for huge,
  append-heavy datasets.
- **Weakness:** you must design tables around your **queries** up front (no ad-hoc
  joins); secondary indexes are limited.
- **Products:** Apache Cassandra, HBase, Google Bigtable, ScyllaDB.

---

## 4. Graph databases

Model data as **nodes** and **edges (relationships)**, both with properties.
Optimized for **traversing relationships** — exactly the queries that are
expensive multi-join recursions in SQL.

```cypher
// Neo4j Cypher: topics a prerequisite chain leads to
MATCH (t:Topic {name:'SQL'})-[:PREREQ_OF*1..3]->(next:Topic)
RETURN next.name
```

- **Strength:** fast variable-depth traversals (social graphs, recommendations,
  prerequisite chains, fraud rings).
- **Weakness:** not built for bulk aggregate scans; sharding a graph is hard.
- **Products:** Neo4j, Amazon Neptune, JanusGraph.

---

## 5. CAP examples per family

| Family | Typical product | Default CAP lean |
|--------|-----------------|------------------|
| Document | MongoDB | CP (consistent by default; tunable) |
| Key-value | DynamoDB / Redis Cluster | AP (high availability, eventual) |
| Column-family | Cassandra | AP, **tunable** per query via consistency levels |
| Graph | Neo4j | CA-ish on a single node; CP when clustered |

Cassandra is the clearest example of **tunable consistency**: each query picks a
consistency level (`ONE`, `QUORUM`, `ALL`), sliding between availability and
consistency on a per-request basis.

---

## When to choose NoSQL vs relational

**Prefer NoSQL when:**

- The data is naturally an **aggregate/document** or a **graph**, and you rarely
  join across entities.
- You need to scale **writes horizontally** beyond one machine.
- The **schema is fluid** or varies per record.
- You can tolerate **eventual consistency** for higher availability.

**Stay relational (like CourseDB-AI) when:**

- You need **ACID** transactions, multi-table **joins**, and ad-hoc queries.
- Data integrity (foreign keys, constraints, normalization) matters.
- The dataset fits comfortably on one (or a few) well-provisioned nodes.

> Modern PostgreSQL blurs the line: its **JSONB** type (see the
> [semi-structured supplement](theory_notes_semi_structured.md)) gives you
> document-style flexibility *with* ACID — often the best of both worlds, and
> the reason CourseDB-AI stays relational.

---

## Self-check questions

1. Give one real product for each NoSQL family.
2. What query pattern is a graph database optimized for?
3. How does eventual consistency differ from strong consistency?
4. Why do many NoSQL systems favor availability over consistency?
5. When would you still choose a relational database over any NoSQL option?

### Answers

1. **Document:** MongoDB. **Key-value:** Redis (or DynamoDB). **Column-family:**
   Cassandra (or HBase/Bigtable). **Graph:** Neo4j.
2. Variable-depth **relationship traversals** — following edges between nodes
   (e.g. "friends of friends", prerequisite chains) — which would be expensive
   recursive multi-joins in SQL.
3. **Strong consistency:** every read reflects the latest committed write
   immediately (single linear view). **Eventual consistency:** replicas may
   return stale data for a while but converge to the same value once updates
   propagate, given no new writes.
4. Many NoSQL systems are built for large clusters where network **partitions
   are inevitable** (CAP). Choosing availability keeps the system responding on
   all sides during a partition, which suits web-scale workloads that prefer a
   slightly stale answer over an error or downtime.
5. When you need **ACID transactions, joins, strong integrity constraints, and
   ad-hoc querying**, and the data fits on one/few nodes — e.g. CourseDB-AI,
   financial systems, anything where correctness beats raw write-scaling.

---

## Notes

Map each CourseDB-AI entity (course, topic, question, resource) to the NoSQL
family that would fit it *least* well and explain why relational wins here.

---

## 🧭 Navigation

**[← Distributed Databases](theory_notes_distributed.md)** | **[Next supplement: Object/Object-Relational →](theory_notes_oo_object_relational.md)**

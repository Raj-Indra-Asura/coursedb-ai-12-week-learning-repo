<!-- Exam-prep QUESTION BANK. Questions only — NO answers are provided here, by
     design. Use for university revision and the portfolio FAQ. -->

# CSE 2203 Exam-Prep Question Bank

For each of the 17 syllabus topics: 5 short-answer, 2 long-answer, and 1
numerical/problem question. **Answers are intentionally omitted** — write your
own.

---

## Topic 1 — Introduction to DBMS & Database Architecture

**Short answer**
1. Define a DBMS and list three advantages over file-based storage.
2. What is data independence? Distinguish logical from physical.
3. Describe the three-schema (ANSI/SPARC) architecture.
4. What is the role of the query processor vs the storage manager?
5. Differentiate between a data model and a database schema.

**Long answer**
1. Explain the three-level architecture of a DBMS and how it provides data independence, with a diagram.
2. Compare the responsibilities of the DDL, DML, and DCL components of a database language with examples.

**Numerical / problem**
1. Given a scenario description of a university system, identify the entities, the data each level (external/conceptual/internal) would expose, and justify.

---

## Topic 2 — Entity-Relationship Modeling

**Short answer**
1. Distinguish a strong entity from a weak entity.
2. What is a discriminator (partial key)?
3. Define cardinality ratio and give the four types.
4. What is total vs partial participation?
5. When do you model an attribute as a multivalued attribute?

**Long answer**
1. Design an ER diagram for the CourseDB-AI domain (courses, topics, questions, resources, users) and justify each relationship's cardinality.
2. Explain how generalization, specialization, and aggregation extend the basic ER model, with examples.

**Numerical / problem**
1. Convert a given ER diagram with one weak entity and one many-to-many relationship into relational schemas, showing all keys.

---

## Topic 3 — Relational Model & Relational Algebra

**Short answer**
1. Define relation, tuple, attribute, and domain.
2. What is the difference between a candidate key and a superkey?
3. State the purpose of the selection (σ) and projection (π) operators.
4. What does the natural join (⋈) do?
5. Why is the division (÷) operator used for "for all" queries?

**Long answer**
1. Express a set of four English queries in relational algebra over the CourseDB-AI schema and explain each step.
2. Prove that the join operator can be expressed using Cartesian product, selection, and projection.

**Numerical / problem**
1. Given two relations R(A,B) and S(B,C) with sample tuples, compute R ⋈ S and R ÷ S.

---

## Topic 4 — SQL Fundamentals (DDL/DML/DQL)

**Short answer**
1. Differentiate `DELETE`, `TRUNCATE`, and `DROP`.
2. What is the difference between `WHERE` and `HAVING`?
3. Explain the purpose of the `GROUP BY` clause.
4. What are the three-valued logic outcomes involving `NULL`?
5. What does a `CHECK` constraint enforce?

**Long answer**
1. Write the DDL for the `courses`, `topics`, and `questions` tables with all keys and constraints, and explain each clause.
2. Explain the logical order of evaluation of an SQL `SELECT` statement's clauses.

**Numerical / problem**
1. Given a `questions` table sample, write and trace the result of a query computing average marks per difficulty, excluding groups with fewer than two questions.

---

## Topic 5 — Advanced SQL (joins, subqueries, views, triggers)

**Short answer**
1. Differentiate `INNER`, `LEFT`, `RIGHT`, and `FULL OUTER` joins.
2. What is a correlated subquery?
3. What is the difference between a view and a materialized view?
4. Name two situations where a trigger is appropriate.
5. What does a window function add over `GROUP BY`?

**Long answer**
1. Explain, with examples, how subqueries can appear in the `SELECT`, `FROM`, and `WHERE` clauses, and the trade-offs versus joins.
2. Describe the lifecycle of a row-level `BEFORE UPDATE` trigger and a use case in CourseDB-AI.

**Numerical / problem**
1. Given two sample tables, predict the row count of an inner join vs a left join and justify the difference.

---

## Topic 6 — Functional Dependencies

**Short answer**
1. Define a functional dependency.
2. State Armstrong's axioms.
3. What is the closure of an attribute set?
4. What is a minimal (canonical) cover?
5. Distinguish a full from a partial functional dependency.

**Long answer**
1. Given a relation and a set of FDs, compute all candidate keys and show your reasoning.
2. Explain how to test whether a decomposition is dependency-preserving.

**Numerical / problem**
1. For R(A,B,C,D,E) with F = {A→BC, CD→E, B→D, E→A}, compute (AB)+ and identify a candidate key.

---

## Topic 7 — Normalization

**Short answer**
1. Define 1NF, 2NF, 3NF, and BCNF in one line each.
2. What anomaly does 2NF remove?
3. When is a relation in 3NF but not BCNF?
4. What is a transitive dependency?
5. What is the goal of 4NF (multivalued dependencies)?

**Long answer**
1. Walk a given un-normalized relation through 1NF → BCNF, showing the decomposition at each step.
2. Discuss the trade-off between normalization and denormalization, using the deliberate denormalization in CourseDB-AI's `questions` table.

**Numerical / problem**
1. Given R with FDs, determine the highest normal form it satisfies and decompose it into BCNF, checking for lossless join.

---

## Topic 8 — Access Control & Security

**Short answer**
1. What do `GRANT` and `REVOKE` do?
2. Distinguish a role from a user in PostgreSQL.
3. What is row-level security?
4. What is SQL injection and one way to prevent it?
5. What does `WITH GRANT OPTION` allow?

**Long answer**
1. Design a privilege scheme for CourseDB-AI with at least three roles (admin, contributor, read-only) and explain each grant.
2. Explain how parameterized queries prevent SQL injection, with a vulnerable vs safe example.

**Numerical / problem**
1. Given a sequence of `GRANT`/`REVOKE` statements, determine the final effective privileges of a user.

---

## Topic 9 — Indexing

**Short answer**
1. Distinguish a clustered from a non-clustered index.
2. Why is a B+ tree preferred over a B-tree for disk-based indexes?
3. When does a hash index outperform a B+ tree index?
4. What is a covering index?
5. What is the downside of having many indexes on a table?

**Long answer**
1. Explain B+ tree insertion with node splitting, including how the height stays balanced.
2. Compare IVFFlat and HNSW indexing for vector similarity search in pgvector.

**Numerical / problem**
1. For a B+ tree of order 4, insert the keys 1..10 in order and draw the resulting tree, stating its height.

---

## Topic 10 — Query Processing & Optimization

**Short answer**
1. List the main stages of query processing.
2. What is a query execution plan?
3. Differentiate a nested-loop join from a hash join.
4. What statistics does the optimizer rely on?
5. What does `EXPLAIN ANALYZE` report that `EXPLAIN` does not?

**Long answer**
1. Explain how a cost-based optimizer chooses a join order, with an example.
2. Describe how an index changes the plan for a selective `WHERE` clause, referencing a real CourseDB-AI query.

**Numerical / problem**
1. Given relation cardinalities and a join, estimate the result size and the cost of nested-loop vs hash join.

---

## Topic 11 — Transactions & ACID

**Short answer**
1. State the four ACID properties.
2. What is the difference between commit and rollback?
3. What is a savepoint?
4. How does the DBMS guarantee durability?
5. What is a transaction's "schedule"?

**Long answer**
1. Explain each ACID property and the DBMS mechanism that provides it.
2. Explain serializability and how conflict-serializability is tested with a precedence graph.

**Numerical / problem**
1. Given a schedule of operations from two transactions, draw the precedence graph and decide whether it is conflict-serializable.

---

## Topic 12 — Concurrency Control

**Short answer**
1. Define dirty read, non-repeatable read, and phantom read.
2. What is two-phase locking (2PL)?
3. Distinguish shared from exclusive locks.
4. What is a deadlock?
5. How does MVCC avoid read locks?

**Long answer**
1. Compare lock-based, timestamp-based, and optimistic concurrency control.
2. Explain how a wait-for graph detects deadlocks and how a victim is chosen, referencing the CourseDB-AI simulator.

**Numerical / problem**
1. Given lock requests from three transactions, build the wait-for graph and determine whether a deadlock exists.

---

## Topic 13 — Crash Recovery & Logging

**Short answer**
1. State the write-ahead logging (WAL) rule.
2. What is a checkpoint?
3. Distinguish redo from undo.
4. What is a log sequence number (LSN)?
5. What are the three phases of ARIES?

**Long answer**
1. Explain log-based recovery using deferred vs immediate database modification.
2. Describe the ARIES recovery algorithm's analysis, redo, and undo phases.

**Numerical / problem**
1. Given a log with `BEGIN`, `UPDATE`, `COMMIT`, and a crash point, list which transactions are redone and which are undone.

---

## Topic 14 — Distributed Databases

**Short answer**
1. Distinguish sharding from replication.
2. State the CAP theorem.
3. What is a coordinator in 2PC?
4. What is data fragmentation?
5. What is a distributed transaction?

**Long answer**
1. Explain the two-phase commit protocol and the scenarios in which it blocks.
2. Discuss the trade-offs of CP vs AP systems under network partitions, with examples.

**Numerical / problem**
1. Given a 2PC run where the coordinator fails after sending `prepare`, trace each participant's state and the required recovery action.

---

## Topic 15 — Semi-structured Data (XML / JSON)

**Short answer**
1. What makes data "semi-structured"?
2. Differentiate XML elements from attributes.
3. What does an XPath expression return?
4. Differentiate PostgreSQL `json` from `jsonb`.
5. What is a JSONB GIN index used for?

**Long answer**
1. Compare relational and semi-structured storage for a hierarchical dataset, with pros and cons.
2. Show how the same query is expressed in XQuery and in PostgreSQL JSONB operators.

**Numerical / problem**
1. Given an XML document, write the XPath expressions that select two specified node sets.

---

## Topic 16 — Object-Oriented & Object-Relational Databases

**Short answer**
1. What is the object-relational impedance mismatch?
2. What is a composite type in PostgreSQL?
3. What does table inheritance provide?
4. Distinguish an OODB from an ORDB.
5. What is a user-defined type (UDT)?

**Long answer**
1. Explain how object-relational features (complex types, inheritance, methods) extend the relational model.
2. Discuss when an object-relational design is preferable to a pure relational one, with a domain example.

**Numerical / problem**
1. Map a small class hierarchy (with inheritance) to relational tables using two different strategies and compare.

---

## Topic 17 — NoSQL Databases

**Short answer**
1. Name the four main NoSQL families and one product each.
2. What query pattern suits a graph database?
3. Differentiate strong from eventual consistency.
4. What is the BASE model?
5. When is a key-value store the right choice?

**Long answer**
1. Compare document, key-value, column-family, and graph databases by data model and typical use case.
2. Explain how the CAP theorem informs the design choices of two named NoSQL systems.

**Numerical / problem**
1. Given access-pattern requirements (high write throughput, eventual consistency, range scans), recommend a NoSQL family and justify against CAP.

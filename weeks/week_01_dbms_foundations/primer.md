# Week 1 Primer: DBMS Foundations (Provided Reading)

> 📘 **This file is PROVIDED reference content — not a learner-fill template.**
> Read it top to bottom *before* writing your own notes in
> [`theory_notes.md`](theory_notes.md). It gives you enough grounding that the
> fill-in prompts make sense even if this is your first exposure to databases.
> For deeper study, pair it with any standard text (e.g., Silberschatz
> *Database System Concepts*, ch. 1) or an intro video.

---

## 🧭 Navigation

**[← Back to Week 1 Overview](README.md)** | **[Next: Theory Notes →](theory_notes.md)**

---

## 1. Data vs. Information vs. Database

- **Data** are raw, unprocessed facts with no context on their own. `"John"`,
  `25`, and `"CS"` are just values.
- **Information** is data that has been processed, organized, or given context
  so it means something: *"John is a 25-year-old Computer Science student."*
- A **database** is an organized, persistent collection of interrelated data,
  managed so it can be stored, retrieved, and updated efficiently and safely.

**Mental model:** data → (organize + relate) → database → (query + interpret) →
information.

## 2. Schema vs. Instance

- A **schema** is the *structure/design* of a database: the tables, the columns,
  their types, and the relationships between them. It changes rarely.
- An **instance** is the *actual data* stored at a particular moment in time. It
  changes constantly as rows are inserted, updated, and deleted.

**Analogy:** the schema is like a class definition in programming; an instance
is like a specific object created from that class. In CourseDB-AI, the `courses`
table definition is schema; the 12 course rows currently stored are an instance.

## 3. The Three-Level Architecture (Data Abstraction)

Databases hide complexity using three levels of abstraction:

1. **Physical level** — *how* data is actually stored on disk (files, blocks,
   pages, indexes). Most users never see this.
2. **Logical level** — *what* data is stored and how it relates (tables,
   columns, keys, constraints). This is what schema designers work with.
3. **View level** — tailored, partial perspectives for specific users or apps
   (e.g., a "questions for Week 2" view that hides everything else).

**Why it matters:** *data independence.* You can change how data is stored
(physical) without breaking the logical schema, and change the logical schema
without breaking every user view.

## 4. Why Not Just Use Files?

Before databases, applications stored data in flat files. That causes:

- **Redundancy** — the same fact copied in many files.
- **Inconsistency** — copies drift out of sync.
- **Hard access** — every new question needs a new custom program.
- **Integrity problems** — no central rules to enforce valid data.
- **Atomicity problems** — a crash mid-update leaves half-written data.
- **Concurrency problems** — two users updating the same file corrupt it.
- **Security problems** — no fine-grained access control.

A DBMS exists precisely to solve all of these in one managed system.

## 5. What a DBMS Provides

A **Database Management System** is software that sits between users/apps and
the stored data and offers:

- **Data definition (DDL)** — declare structure: `CREATE TABLE`, constraints.
- **Data manipulation (DML)** — insert/update/delete and **query** data:
  `SELECT`, `INSERT`, `UPDATE`, `DELETE`.
- **Transaction management** — group operations so they are *all-or-nothing*.
- **Concurrency control** — let many users work at once without corruption.
- **Security & authorization** — control who can see/do what.
- **Recovery** — restore a consistent state after a crash.

PostgreSQL — the DBMS used throughout this course — provides all of the above.

## 6. Key Roles and Languages (quick glossary)

- **DDL** (Data Definition Language): defines schema (`CREATE`, `ALTER`, `DROP`).
- **DML** (Data Manipulation Language): reads/writes data (`SELECT`, `INSERT`…).
- **DBA** (Database Administrator): designs, secures, and tunes the database.
- **Query optimizer**: the DBMS component that decides *how* to execute a query
  efficiently (you'll meet it in Week 8).

## 7. How This Maps to CourseDB-AI

CourseDB-AI is a real data-infrastructure project, not a chatbot or a file
organizer. Over 12 weeks you will:

- design a **schema** for courses, topics, questions, and resources (Weeks 3–4),
- write **SQL** to query it (Week 2),
- expose it through a **FastAPI** backend on **PostgreSQL** (Weeks 5–6),
- look *inside* the DBMS with **B+ tree / hash / transaction** simulators
  (Weeks 7–9),
- and add **semantic search** with embeddings + pgvector (Week 10).

Everything in this primer is the vocabulary you'll use for the rest of the
course.

---

## ✅ Before you move on

You should now be able to, in your own words:

1. Define data, information, and a database, with an example of each.
2. Explain the difference between schema and instance.
3. Name the three levels of data abstraction and why data independence matters.
4. List at least four problems a DBMS solves that flat files do not.

Now open [`theory_notes.md`](theory_notes.md) and write these in your own words —
that's where the real learning happens.

---

## 🧭 Navigation

**[← Back to Week 1 Overview](README.md)** | **[Next: Theory Notes →](theory_notes.md)**

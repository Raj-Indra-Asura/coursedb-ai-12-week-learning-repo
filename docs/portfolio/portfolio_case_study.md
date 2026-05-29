# CourseDB-AI — Technical Case Study

**Week 12: Evaluation, Polish, Portfolio**

> **TODO(learner):** This is a *starter template*. Fill in each section with
> your own words, decisions, and results. The headings below mirror the
> structure recommended in `docs/portfolio/README.md`. Delete this note when
> your case study is complete.

---

## 1. Background and Motivation

> **TODO(learner):** Why did you build CourseDB-AI? What problem with studying
> for DBMS exams (or organizing course material) does it solve?

## 2. Problem Statement

> **TODO(learner):** State the concrete problem in 2–3 sentences.

## 3. Why DBMS Matters for AI

> **TODO(learner):** Explain how solid database fundamentals support modern AI
> systems (storage, retrieval, vector search, data quality).

## 4. System Design Overview

> **TODO(learner):** Describe the high-level architecture (FastAPI backend,
> PostgreSQL + pgvector, services, frontend). Include a diagram if you have one.

## 5. Database Design and Normalization

> **TODO(learner):** Summarize your schema, key entities, and the normalization
> decisions you made (reference Week 3–4).

## 6. SQL and Analytics Layer

> **TODO(learner):** Describe the queries and analytics endpoints you built
> (reference Week 2 and the Analytics API).

## 7. Indexing and Optimization

> **TODO(learner):** What indexes did you add and why? Include before/after
> `EXPLAIN` results (reference Week 7–8 and `docs/indexing/`).

## 8. Transaction Safety

> **TODO(learner):** Explain ACID guarantees and how you reasoned about
> concurrency/deadlocks (reference Week 9 and the Wait-For Graph simulator).

## 9. Semantic Search Implementation

> **TODO(learner):** Describe chunking → embeddings → pgvector similarity, and
> the hybrid SQL + vector search (reference Week 10).
>
> ⚠️ **Note on embeddings:** `scripts/generate_embeddings.py` falls back to a
> deterministic hashing encoder when `sentence-transformers` is not installed.
> Confirm you ran a real embedding model before reporting search-quality
> numbers (see `VERIFICATION_REPORT.md`).

## 10. Evaluation Results

> **TODO(learner):** Summarize results from `docs/evaluation/` (SQL correctness,
> index impact, semantic-search relevance scores).

## 11. Challenges and Lessons Learned

> **TODO(learner):** What was hard? What would you do differently?

## 12. Future Improvements

> **TODO(learner):** What would you build next (see the "Further Study" topics
> in `ROADMAP.md`: backup/recovery, replication/HA, partitioning, security
> depth)?

## 13. Connection to AI/ML Engineering

> **TODO(learner):** Tie the project back to ML/data-engineering roles.

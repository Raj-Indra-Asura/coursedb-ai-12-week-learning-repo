<!-- DO NOT auto-fill the score columns. The relevance scores are the learner's
     judgement. AI tooling may regenerate the query list and structure only. -->

# Semantic Search Relevance Rubric

Use this 1–5 rubric to score the relevance of the top result(s) returned for
each evaluation query in `data/evaluation/eval_queries.json`. Run
`python scripts/run_evaluation.py` to (re)generate the populated results table
in `docs/evaluation/semantic_search_results.md`, then fill in the scores below.

## Relevance scale

| Score | Label | Meaning |
| ----- | ----- | ------- |
| 5 | Perfect | Top result directly and fully answers the query. |
| 4 | Strong | Top result is clearly relevant, minor gaps. |
| 3 | Partial | Result is on-topic but incomplete or tangential. |
| 2 | Weak | Loosely related; wrong sub-topic. |
| 1 | Irrelevant | Result is unrelated to the query. |

## Scoring sheet

> **TODO(learner):** Fill in the `Top-1 score`, `Top-3 hit?`, and `Comments`
> columns after reviewing the generated results table.

| Query ID | Query | Expected topic | Top-1 score (1–5) | Top-3 hit? (Y/N) | Comments |
| -------- | ----- | -------------- | ----------------- | ---------------- | -------- |
| 1 | What causes a deadlock between two transactions and how is it detected? | Transactions and Concurrency Control | | | |
| 2 | How does normalization remove redundancy and update anomalies? | Functional Dependencies and Normalization | | | |
| 3 | Explain how a B+ tree index supports efficient range queries | Indexing and B+ Trees | | | |
| 4 | What are the ACID properties of a database transaction? | Transactions and Concurrency Control | | | |
| 5 | How do SQL joins combine rows from multiple tables? | SQL Querying | | | |
| 6 | What is an entity-relationship diagram and how does it map to tables? | ER Modeling and Schema Design | | | |
| 7 | How does hashing provide constant-time equality lookups in an index? | Indexing and Hashing | | | |
| 8 | What does the query optimizer do with an EXPLAIN plan? | Query Processing and Optimization | | | |
| 9 | How are vector embeddings used for semantic similarity search? | Embeddings and Semantic Search | | | |
| 10 | What is the difference between a primary key and a foreign key constraint? | Relational Model and Constraints | | | |

## Summary metrics

> **TODO(learner):** Compute these after scoring.

- Mean Top-1 relevance score: ____ / 5
- Precision@1 (scores of 4–5 counted as relevant): ____ %
- Top-3 hit rate: ____ %

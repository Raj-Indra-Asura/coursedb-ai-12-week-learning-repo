<!-- Template only. Paste real EXPLAIN ANALYZE output into the rows yourself.
     Before/after outputs are produced by scripts/run_evaluation.py --plans. -->

# Query Plan Analysis

Compare planner behaviour before and after adding indexes. Raw output is written
to `dbms_internals/query_plan/outputs/before_indexes.txt` and
`after_indexes.txt` by `scripts/run_evaluation.py --plans`.

## Per-query comparison

| # | Query (short) | Plan before | Plan after | Cost before | Cost after | Notes |
| - | ------------- | ----------- | ---------- | ----------- | ---------- | ----- |
| 1 |  | Seq Scan? |  |  |  |  |
| 2 |  |  |  |  |  |  |
| 3 |  |  |  |  |  |  |
| 4 |  |  |  |  |  |  |
| 5 |  |  |  |  |  |  |

> **TODO(learner):** Paste the relevant lines from the EXPLAIN output and explain
> each plan change.

## Observations

> **TODO(learner):** Which queries changed from Seq Scan to Index Scan? Where did
> indexing NOT help, and why?

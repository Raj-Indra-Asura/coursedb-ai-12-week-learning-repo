<!-- Template + before/after table. Measurements and analysis are the learner's. -->

# Performance Benchmarks

Record measured timings. Use `EXPLAIN ANALYZE` and/or simple timing around the
API/services.

## Query latency: before vs after indexes

| # | Query (short) | Rows | Time before (ms) | Time after (ms) | Speedup |
| - | ------------- | ---- | ---------------- | --------------- | ------- |
| 1 |  |  |  |  |  |
| 2 |  |  |  |  |  |
| 3 |  |  |  |  |  |
| 4 |  |  |  |  |  |
| 5 |  |  |  |  |  |

> Source data: `dbms_internals/query_plan/outputs/before_indexes.txt` /
> `after_indexes.txt`.

## Semantic search latency

| Setup | k | Time (ms) | Notes |
| ----- | - | --------- | ----- |
| No vector index |  |  |  |
| IVFFlat |  |  |  |

## Methodology

> **TODO(learner):** State how many runs you averaged, warm vs cold cache, and
> hardware.

## Conclusions

> **TODO(learner):** Where did indexing help most? Any surprises?

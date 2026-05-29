<!-- Template only. Result table is auto-generated separately; the analysis prose
     is the learner's. -->

# Semantic Search Report

## Pipeline summary

| Stage | Component | Notes |
| ----- | --------- | ----- |
| Chunking | `app/services/chunking_service.py` |  |
| Embedding | `app/services/embedding_service.py` |  |
| Storage | `chunk_embeddings` (pgvector) |  |
| Retrieval | `app/services/semantic_search_service.py` |  |

> **TODO(learner):** Describe each stage in your own words.

## Results

See the auto-generated `docs/evaluation/semantic_search_results.md` for the
top-1/3/5 table produced by `scripts/run_evaluation.py --semantic`.

> **TODO(learner):** Interpret the results: which queries worked, which failed,
> and why.

## Hybrid search

> **TODO(learner):** Explain how SQL filtering combines with vector similarity.

## Self-check questions

1. Why chunk documents before embedding?
2. What distance metric does the query use, and why?
3. How does IVFFlat trade recall for speed?

> **Notes:**

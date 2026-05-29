<!-- Template only. The conceptual explanation is the learner's. -->

# Embeddings Explained

## What is an embedding?

> **TODO(learner):** Define an embedding and the vector space intuition.

## Model used

| Property | Value |
| -------- | ----- |
| Model name |  |
| Dimensionality | 384 |
| Distance metric |  |

> Note: in environments without the model cached, this project falls back to a
> deterministic hashing encoder for testing. Explain why that is acceptable for
> tests but not for real retrieval.

## From text to vector

> **TODO(learner):** Walk through tokenization → model → pooled vector.

## Similarity

> **TODO(learner):** Explain cosine vs L2 vs inner product and which pgvector
> operator (`<=>`, `<->`, `<#>`) maps to each.

## Self-check questions

1. Why are similar meanings close in embedding space?
2. What does normalizing a vector change about cosine vs dot product?
3. Why is 384 dimensions a reasonable choice here?

> **Notes:**

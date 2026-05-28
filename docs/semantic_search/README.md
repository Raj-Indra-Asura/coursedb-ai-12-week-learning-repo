# Semantic Search Documentation

**Week 10: Embeddings, pgvector, Semantic Search**

This directory contains semantic search implementation and evaluation.

---

## 📁 Files to Create

### `semantic_search_report.md` (Week 10)
- Text chunking strategy
- Embedding generation process
- pgvector implementation
- Similarity search algorithm

### `embedding_model.md` (Week 10)
- Model: all-MiniLM-L6-v2
- Embedding dimension: 384
- Token limit: 256
- Performance characteristics

### `comparison_keyword_vs_semantic.md` (Week 10)
- Test queries
- Keyword search results
- Semantic search results
- Analysis and insights

---

## 🎯 Implementation Details

### Chunking
- Chunk size: 250 words
- Overlap: 50 words
- Sentence-aware splitting

### Similarity Metric
- Cosine distance: `embedding <=> query_embedding`
- Similarity = 1 - distance
- Range: 0 (different) to 1 (identical)

---

## 📊 Test Queries

1. "questions about deadlock"
2. "database design diagram questions"
3. "normalization with functional dependency"
4. "B+ tree insertion problems"
5. "transaction isolation and lost update"

---

**TODO (Week 10)**: Implement and evaluate semantic search

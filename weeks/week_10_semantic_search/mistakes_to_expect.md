# Week 10: Semantic Search & Vector Databases - Common Mistakes

## 🎯 Purpose

Avoid common pitfalls when implementing semantic search and vector databases.

---

## Mistake Category 1: Embedding Errors

### Mistake 1.1: Mixing Embedding Models

**What happens:**
```python
# Index with model A
model_a = SentenceTransformer('all-MiniLM-L6-v2')
embedding_a = model_a.encode(text)
# Store in database

# Search with model B
model_b = SentenceTransformer('all-mpnet-base-v2')
embedding_b = model_b.encode(query)
# Results are meaningless!
```

**Why it's wrong:** Different models create incompatible vector spaces.

**How to fix:**
- Track model_name in database
- Use same model for indexing and search
- Reindex if changing models

---

### Mistake 1.2: Not Normalizing Vectors

**What happens:**
```python
# Using dot product without normalization
embedding <#> query_vec
# Results favor longer vectors
```

**How to fix:**
```python
# Use cosine distance (automatically normalized)
embedding <=> query_vec

# Or normalize manually for dot product
from sklearn.preprocessing import normalize
embedding_norm = normalize([embedding])[0]
```

---

### Mistake 1.3: Embedding Entire Documents

**What happens:**
```python
# Embedding 10,000-word document
huge_text = "..." * 10000
embedding = model.encode(huge_text)
# Quality degrades, tokens truncated
```

**How to fix:**
- Chunk documents (200-500 tokens)
- Embed each chunk separately
- Search across chunks

---

## Mistake Category 2: Chunking Problems

### Mistake 2.1: No Overlap

**What happens:**
```python
chunks = chunk_text(text, chunk_size=500, overlap=0)
# Important context split across chunks
# "...database normalization. First normal form..."
# Chunk 1: "...database normalization."
# Chunk 2: "First normal form..."
# Loses connection!
```

**How to fix:**
```python
chunks = chunk_text(text, chunk_size=500, overlap=50)
# Preserves context across boundaries
```

---

### Mistake 2.2: Chunks Too Small/Large

**What happens:**
```python
# Too small (50 chars)
chunks = chunk_text(text, chunk_size=50)
# Lacks context, too many chunks

# Too large (5000 chars)
chunks = chunk_text(text, chunk_size=5000)
# Too generic, less precise matching
```

**How to fix:**
- Optimal: 200-500 tokens (800-2000 chars)
- Test with your content
- Balance specificity and context

---

## Mistake Category 3: Search Quality

### Mistake 3.1: Using Only Semantic Search

**What happens:**
```python
query = "CS201"  # Course code
results = semantic_search(query)
# Misses exact match for "CS201"
# Returns conceptually similar but wrong results
```

**How to fix:**
```python
# Use hybrid search for better coverage
results = hybrid_search(query, 
                       keyword_weight=0.5,  # High for exact terms
                       semantic_weight=0.5)
```

---

### Mistake 3.2: Wrong Similarity Threshold

**What happens:**
```python
# No threshold - returns everything
results = semantic_search(query, top_k=100)
# Includes irrelevant results with low similarity
```

**How to fix:**
```python
# Filter by similarity threshold
results = [r for r in results if r.similarity > 0.7]
# Or set reasonable top_k (5-10)
```

---

## Mistake Category 4: Performance Issues

### Mistake 4.1: No Vector Index

**What happens:**
```sql
-- No index on embedding column
SELECT * FROM embeddings
ORDER BY embedding <=> query_vec
LIMIT 10;
-- Scans 1M rows = 10 seconds
```

**How to fix:**
```sql
CREATE INDEX ON embeddings
USING hnsw (embedding vector_cosine_ops);
-- Now < 100ms
```

---

### Mistake 4.2: Wrong Index Parameters

**What happens:**
```sql
-- IVFFlat with wrong lists
CREATE INDEX ON embeddings
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 1);  -- Only 1 cluster!
-- No benefit from index
```

**How to fix:**
```sql
-- Use √(num_rows) for lists
-- For 10,000 rows: lists = 100
CREATE INDEX ON embeddings
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);
```

---

### Mistake 4.3: Batch Processing Inefficiency

**What happens:**
```python
# One at a time
for text in texts:
    embedding = model.encode(text)  # Slow!
    # Insert
```

**How to fix:**
```python
# Batch encoding
embeddings = model.encode(texts)  # Fast!
# Batch insert
```

---

## Mistake Category 5: RAG Problems

### Mistake 5.1: Too Much Context

**What happens:**
```python
# Retrieve 50 chunks
chunks = semantic_search(query, top_k=50)
context = "\n".join([c.text for c in chunks])
# 20,000 tokens exceeds LLM limit
```

**How to fix:**
```python
# Retrieve fewer, more relevant chunks
chunks = semantic_search(query, top_k=3-5)
# Or re-rank and select top 3
```

---

### Mistake 5.2: Not Filtering Low Similarity

**What happens:**
```python
chunks = semantic_search(query, top_k=5)
# Includes chunk with 0.3 similarity (barely related)
# LLM uses it anyway, generates wrong answer
```

**How to fix:**
```python
chunks = semantic_search(query, top_k=10)
chunks = [c for c in chunks if c.similarity > 0.7]
# Use only relevant chunks
```

---

## Mistake Category 6: pgvector Issues

### Mistake 6.1: Wrong Dimension

**What happens:**
```sql
CREATE TABLE embeddings (
    embedding VECTOR(768)  -- Created for 768 dims
);

-- Insert 384-dim embedding
INSERT INTO embeddings VALUES ('[0.1, 0.2, ...]');
-- ERROR: dimension mismatch
```

**How to fix:**
- Match vector dimension to model
- all-MiniLM-L6-v2 = 384 dims
- all-mpnet-base-v2 = 768 dims

---

### Mistake 6.2: Not Casting Vector

**What happens:**
```sql
SELECT * FROM embeddings
ORDER BY embedding <=> '[0.1, 0.2, ...]'
-- ERROR: cannot compare text to vector
```

**How to fix:**
```sql
SELECT * FROM embeddings
ORDER BY embedding <=> '[0.1, 0.2, ...]'::vector
-- Explicit cast
```

---

## Quick Reference: Common Errors

| Symptom | Likely Cause | Solution |
|---------|--------------|----------|
| Poor search results | Mixed embedding models | Use same model |
| Slow searches | No vector index | Create HNSW index |
| Context lost in chunks | No overlap | Add 50-100 token overlap |
| Exact matches missed | Only semantic search | Use hybrid search |
| Out of memory | Chunks too small | Increase chunk size |
| Dimension mismatch | Wrong vector size | Match model dimensions |

---

## Best Practices

1. **Use same embedding model** throughout
2. **Chunk with overlap** (50-100 tokens)
3. **Index vectors** (HNSW for large datasets)
4. **Use hybrid search** for best coverage
5. **Filter by similarity** threshold
6. **Batch embeddings** for efficiency
7. **Monitor search quality** with metrics

---

**Remember:** Semantic search is powerful but requires careful implementation. Test thoroughly, measure quality, and iterate!

**Next:** Complete checkpoints.md to track progress

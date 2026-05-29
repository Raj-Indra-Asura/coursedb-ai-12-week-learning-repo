# Week 10: Semantic Search & Vector Databases

## 🧭 Navigation

**[← Previous: Week 9](../week_09_transactions/reflection.md)** | **[View Learning Path](../../LEARNING_PATH.md)** | **[Next: Theory Notes →](theory_notes.md)**

---

## 📋 Overview

Week 10 introduces **semantic search** and **vector databases** - modern techniques for finding information by meaning rather than exact keywords. You'll learn how to use embeddings, pgvector, and build intelligent search systems.

**What you'll master:**
- Vector embeddings and how they capture meaning
- pgvector extension for PostgreSQL
- Similarity measures (cosine, euclidean, dot product)
- Chunking strategies for large documents
- Building semantic search systems
- Hybrid search (keyword + semantic)
- Retrieval-Augmented Generation (RAG)
- Vector indexing for performance

**Why this matters:**
- Traditional search misses synonyms and paraphrases
- Users want "Google-like" intelligent search
- RAG powers modern AI applications
- Vector databases are growing rapidly
- Essential skill for AI/ML applications

---

## 1. Semantic Search vs Keyword Search

### Traditional Keyword Search

```sql
-- Find questions about normalization
SELECT * FROM questions
WHERE question_text ILIKE '%normalization%';

-- Problems:
-- ❌ Misses "normalize", "normal form"
-- ❌ Misses conceptually similar "database design"
-- ❌ Returns all matches for "normalization" even if unrelated
```

### Semantic Search

```python
# Find questions by meaning
query = "database design best practices"

# Returns relevant questions even without exact words:
# ✅ "What is normalization?" (concept match)
# ✅ "How to design efficient schemas?" (meaning match)
# ✅ "ER modeling principles" (related topic)
```

**Key Difference:** Semantic search understands **meaning**, not just words.

---

## 2. Vector Embeddings

### What are Embeddings?

**Embedding**: A numerical representation of text as a vector (list of numbers).

```python
text = "What is database normalization?"
embedding = [0.234, -0.456, 0.678, 0.123, ...]  # 768 numbers
```

**Key Properties:**
- **Similar texts** → **similar vectors**
- **Fixed size** (e.g., 384, 768, 1536 dimensions)
- **Captures semantics** (meaning encoded in numbers)

### How Embeddings Work

```
Text → Embedding Model → Vector

"normalization"      → [0.23, 0.45, -0.12, ...]
"normal forms"       → [0.21, 0.43, -0.10, ...]  ← Similar!
"cats and dogs"      → [-0.67, 0.12, 0.89, ...]  ← Different!
```

### Creating Embeddings

**Using Sentence Transformers:**
```python
from sentence_transformers import SentenceTransformer

# Load model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Generate embedding
text = "What is normalization?"
embedding = model.encode(text)
print(embedding.shape)  # (384,) - 384-dimensional vector
```

**Using OpenAI:**
```python
import openai

response = openai.embeddings.create(
    model="text-embedding-3-small",
    input="What is normalization?"
)
embedding = response.data[0].embedding  # 1536 dimensions
```

### Popular Embedding Models

| Model | Dimensions | Speed | Quality | Cost |
|-------|------------|-------|---------|------|
| all-MiniLM-L6-v2 | 384 | Fast | Good | Free |
| all-mpnet-base-v2 | 768 | Medium | Better | Free |
| text-embedding-3-small | 1536 | Fast | Excellent | Paid |
| text-embedding-3-large | 3072 | Slow | Best | Paid |

**Recommendation for CourseDB-AI:** Start with `all-MiniLM-L6-v2` (free, fast, good quality).

---

## 3. Similarity Measures

### Cosine Similarity

Measures the **angle** between vectors.

**Formula:**
```
cosine_similarity(A, B) = (A · B) / (||A|| × ||B||)
```

**Range:** -1 to 1
- **1** = identical direction (very similar)
- **0** = orthogonal (unrelated)
- **-1** = opposite direction (very different)

**Example:**
```python
from sklearn.metrics.pairwise import cosine_similarity

vec1 = [[0.23, 0.45, -0.12]]  # "normalization"
vec2 = [[0.21, 0.43, -0.10]]  # "normal forms"
vec3 = [[-0.67, 0.12, 0.89]]  # "cats"

print(cosine_similarity(vec1, vec2))  # 0.998 (very similar!)
print(cosine_similarity(vec1, vec3))  # -0.15 (very different)
```

### Euclidean Distance

Measures **straight-line distance**.

**Formula:**
```
distance(A, B) = √(Σ(Ai - Bi)²)
```

**Range:** 0 to ∞
- **0** = identical
- **Larger** = more different

### Dot Product

Simple vector multiplication, used for speed.

**Formula:**
```
dot_product(A, B) = Σ(Ai × Bi)
```

**When to use each:**
- **Cosine**: Most common, normalized (length-independent)
- **Euclidean**: When magnitude matters
- **Dot product**: Fastest, used with normalized vectors

---

## 4. pgvector Extension

**pgvector** adds vector operations to PostgreSQL.

### Installation

```sql
-- Enable extension
CREATE EXTENSION vector;
```

### Vector Data Type

```sql
CREATE TABLE embeddings (
    id SERIAL PRIMARY KEY,
    text TEXT NOT NULL,
    embedding VECTOR(384) NOT NULL  -- 384-dimensional vector
);
```

### Inserting Vectors

```python
# Python: Insert embedding
embedding_list = embedding.tolist()  # Convert numpy to list

db.execute("""
    INSERT INTO embeddings (text, embedding)
    VALUES (:text, :embedding)
""", {"text": "What is normalization?", "embedding": embedding_list})
```

### Similarity Search

```sql
-- Find 5 most similar vectors
SELECT 
    text,
    embedding <=> '[0.23, 0.45, -0.12, ...]'::vector AS distance
FROM embeddings
ORDER BY distance
LIMIT 5;
```

### pgvector Operators

| Operator | Meaning | Usage |
|----------|---------|-------|
| `<->` | Euclidean distance (L2) | `embedding <-> query_vec` |
| `<#>` | Negative dot product | `embedding <#> query_vec` |
| `<=>` | Cosine distance | `embedding <=> query_vec` |

**Most common:** `<=>` (cosine distance) = 1 - cosine_similarity

---

## 5. Vector Indexing

### The Problem

Searching millions of vectors is slow (brute force = O(n)).

**Without index:**
```sql
SELECT * FROM embeddings
ORDER BY embedding <=> query_vec  -- Scans ALL rows!
LIMIT 10;
-- 1,000,000 rows = ~5 seconds
```

### Solution: Approximate Nearest Neighbor (ANN)

Trade perfect accuracy for speed.

### IVFFlat Index

Divides vectors into clusters (like k-means).

```sql
CREATE INDEX ON embeddings
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- lists = number of clusters
-- Rule of thumb: lists = √(num_rows)
```

**How it works:**
1. Vectors grouped into 100 clusters
2. Search only nearest clusters
3. Much faster, slightly less accurate

**Trade-off:**
- ✅ 10-100x faster
- ⚠️ 95-99% recall (might miss best match)

### HNSW Index

Hierarchical graph structure (more sophisticated).

```sql
CREATE INDEX ON embeddings
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- m = connections per node (higher = more accurate, slower build)
-- ef_construction = search depth during build (higher = better quality)
```

**Trade-off:**
- ✅ Faster search than IVFFlat
- ✅ Better recall (98-99%)
- ❌ More memory usage
- ❌ Slower index building

### When to Use Each

| Scenario | Index Type | Reason |
|----------|-----------|--------|
| < 100K vectors | No index | Fast enough |
| 100K - 1M vectors | IVFFlat | Good balance |
| > 1M vectors | HNSW | Best performance |
| Memory constrained | IVFFlat | Less memory |
| Accuracy critical | HNSW | Better recall |

---

## 6. Chunking Strategy

### The Problem

Documents are often too large for embedding models:
- Token limits (512-8192 tokens)
- Quality degrades with length
- Less precise matching

**Example:**
```python
long_text = """
# Database Normalization
Normalization is a process...
[5000 words about normalization, transactions, indexing, etc.]
"""

# Embedding captures too much → less precise search
```

### Solution: Chunking

Split documents into smaller, focused chunks.

### Fixed-Size Chunking

```python
def chunk_text(text, chunk_size=500, overlap=50):
    """
    Split text into fixed-size chunks with overlap.
    
    Args:
        text: Input text
        chunk_size: Characters per chunk
        overlap: Overlapping characters between chunks
        
    Returns:
        List of chunks
    """
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap  # Move forward with overlap
    
    return chunks

# Example
text = "..." * 2000  # Long text
chunks = chunk_text(text, chunk_size=500, overlap=50)
# Result: 4-5 chunks of ~500 chars each, with 50-char overlap
```

**Why overlap?**
- Preserves context across boundaries
- Prevents split sentences from losing meaning

### Sentence-Based Chunking

```python
import nltk

def chunk_by_sentences(text, sentences_per_chunk=5):
    """
    Split text into chunks of N sentences.
    """
    sentences = nltk.sent_tokenize(text)
    chunks = []
    
    for i in range(0, len(sentences), sentences_per_chunk):
        chunk = ' '.join(sentences[i:i+sentences_per_chunk])
        chunks.append(chunk)
    
    return chunks
```

**Advantages:**
- Preserves sentence boundaries
- More natural chunks
- Better for Q&A

### Semantic Chunking

Split at logical boundaries (paragraphs, sections, topics).

```python
def chunk_by_paragraphs(text):
    """
    Split text by double newlines (paragraphs).
    """
    chunks = text.split('\n\n')
    chunks = [c.strip() for c in chunks if c.strip()]
    return chunks
```

### Best Practices

1. **Chunk size**: 200-500 tokens (balance specificity and context)
2. **Overlap**: 50-100 tokens (preserve context)
3. **Store metadata**:
   ```python
   {
       'chunk_id': 1,
       'text': "...",
       'source_id': 123,
       'chunk_index': 0,
       'total_chunks': 5
   }
   ```
4. **Choose strategy based on content**:
   - Technical docs → Sentence-based
   - Long articles → Fixed-size with overlap
   - Structured content → Semantic (by section)

---

## 7. Building Semantic Search

### Step-by-Step Implementation

#### Step 1: Database Schema

```sql
-- Resource chunks
CREATE TABLE resource_chunks (
    chunk_id SERIAL PRIMARY KEY,
    resource_id INTEGER REFERENCES resources(resource_id),
    chunk_text TEXT NOT NULL,
    chunk_index INTEGER NOT NULL,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Chunk embeddings
CREATE TABLE chunk_embeddings (
    chunk_id INTEGER PRIMARY KEY REFERENCES resource_chunks(chunk_id),
    embedding VECTOR(384) NOT NULL,
    model_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Vector index
CREATE INDEX idx_chunk_embeddings_vector
ON chunk_embeddings
USING hnsw (embedding vector_cosine_ops);
```

#### Step 2: Embedding Service

```python
from sentence_transformers import SentenceTransformer

class EmbeddingService:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.model_name = model_name
    
    def embed_text(self, text: str) -> list[float]:
        """Generate embedding for text."""
        embedding = self.model.encode(text)
        return embedding.tolist()
    
    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for multiple texts."""
        embeddings = self.model.encode(texts)
        return embeddings.tolist()
```

#### Step 3: Chunking Service

```python
class ChunkingService:
    def chunk_text(self, text: str, chunk_size=500, overlap=50):
        """Split text into chunks with overlap."""
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append({
                'text': chunk,
                'start': start,
                'end': end
            })
            start += chunk_size - overlap
        
        return chunks
```

#### Step 4: Indexing Pipeline

```python
def index_resource(resource_id: int, text: str):
    """
    Chunk and embed a resource.
    """
    # 1. Chunk text
    chunks = chunking_service.chunk_text(text)
    
    # 2. Insert chunks
    for i, chunk_data in enumerate(chunks):
        chunk_id = db.execute("""
            INSERT INTO resource_chunks 
            (resource_id, chunk_text, chunk_index, metadata)
            VALUES (:resource_id, :text, :index, :metadata)
            RETURNING chunk_id
        """, {
            'resource_id': resource_id,
            'text': chunk_data['text'],
            'index': i,
            'metadata': json.dumps(chunk_data)
        }).scalar()
        
        # 3. Generate embedding
        embedding = embedding_service.embed_text(chunk_data['text'])
        
        # 4. Store embedding
        db.execute("""
            INSERT INTO chunk_embeddings (chunk_id, embedding, model_name)
            VALUES (:chunk_id, :embedding, :model_name)
        """, {
            'chunk_id': chunk_id,
            'embedding': embedding,
            'model_name': embedding_service.model_name
        })
    
    db.commit()
```

#### Step 5: Search Function

```python
def semantic_search(query: str, top_k: int = 10):
    """
    Search for similar chunks.
    """
    # 1. Embed query
    query_embedding = embedding_service.embed_text(query)
    
    # 2. Search database
    results = db.execute("""
        SELECT 
            rc.chunk_id,
            rc.chunk_text,
            rc.resource_id,
            r.title,
            1 - (ce.embedding <=> :query_vec) AS similarity
        FROM chunk_embeddings ce
        JOIN resource_chunks rc ON ce.chunk_id = rc.chunk_id
        JOIN resources r ON rc.resource_id = r.resource_id
        ORDER BY ce.embedding <=> :query_vec
        LIMIT :top_k
    """, {
        'query_vec': query_embedding,
        'top_k': top_k
    }).fetchall()
    
    return results
```

---

## 8. Hybrid Search

Combine keyword search + semantic search for best results.

### Why Hybrid?

**Keyword search strengths:**
- Exact matches (names, codes, IDs)
- Rare/specific terms
- Fast

**Semantic search strengths:**
- Conceptual matches
- Synonyms and paraphrases
- Context understanding

**Together = Best of both worlds!**

### Implementation

```python
def hybrid_search(query: str, top_k: int = 10, 
                  keyword_weight: float = 0.3, 
                  semantic_weight: float = 0.7):
    """
    Hybrid search combining keyword + semantic.
    """
    # 1. Keyword search (PostgreSQL full-text search)
    keyword_results = db.execute("""
        SELECT 
            chunk_id,
            ts_rank(to_tsvector('english', chunk_text), 
                    plainto_tsquery('english', :query)) AS score
        FROM resource_chunks
        WHERE to_tsvector('english', chunk_text) @@ 
              plainto_tsquery('english', :query)
    """, {'query': query}).fetchall()
    
    keyword_scores = {r.chunk_id: r.score for r in keyword_results}
    
    # 2. Semantic search
    query_embedding = embedding_service.embed_text(query)
    semantic_results = db.execute("""
        SELECT 
            chunk_id,
            1 - (embedding <=> :query_vec) AS score
        FROM chunk_embeddings
        ORDER BY embedding <=> :query_vec
        LIMIT :top_k * 2
    """, {'query_vec': query_embedding, 'top_k': top_k}).fetchall()
    
    semantic_scores = {r.chunk_id: r.score for r in semantic_results}
    
    # 3. Combine scores
    all_chunk_ids = set(keyword_scores.keys()) | set(semantic_scores.keys())
    
    combined_scores = []
    for chunk_id in all_chunk_ids:
        keyword_score = keyword_scores.get(chunk_id, 0)
        semantic_score = semantic_scores.get(chunk_id, 0)
        
        final_score = (keyword_score * keyword_weight + 
                      semantic_score * semantic_weight)
        
        combined_scores.append((chunk_id, final_score))
    
    # 4. Sort and return top results
    combined_scores.sort(key=lambda x: x[1], reverse=True)
    top_chunk_ids = [cid for cid, _ in combined_scores[:top_k]]
    
    # 5. Fetch full chunks
    results = db.execute("""
        SELECT rc.*, r.title
        FROM resource_chunks rc
        JOIN resources r ON rc.resource_id = r.resource_id
        WHERE rc.chunk_id = ANY(:chunk_ids)
    """, {'chunk_ids': top_chunk_ids}).fetchall()
    
    return results
```

### SQL Hybrid Search

```sql
WITH keyword_scores AS (
    SELECT 
        chunk_id,
        ts_rank(to_tsvector('english', chunk_text), 
                plainto_tsquery('english', 'normalization')) AS score
    FROM resource_chunks
    WHERE to_tsvector('english', chunk_text) @@ 
          plainto_tsquery('english', 'normalization')
),
semantic_scores AS (
    SELECT 
        chunk_id,
        1 - (embedding <=> '[0.23, 0.45, ...]'::vector) AS score
    FROM chunk_embeddings
    ORDER BY embedding <=> '[0.23, 0.45, ...]'::vector
    LIMIT 100
)
SELECT 
    rc.chunk_id,
    rc.chunk_text,
    COALESCE(k.score, 0) * 0.3 + COALESCE(s.score, 0) * 0.7 AS final_score
FROM resource_chunks rc
LEFT JOIN keyword_scores k ON rc.chunk_id = k.chunk_id
LEFT JOIN semantic_scores s ON rc.chunk_id = s.chunk_id
WHERE k.score IS NOT NULL OR s.score IS NOT NULL
ORDER BY final_score DESC
LIMIT 10;
```

---

## 9. Retrieval-Augmented Generation (RAG)

Use semantic search to enhance LLM responses with retrieved context.

### How RAG Works

```
1. User asks question
   ↓
2. Semantic search retrieves relevant chunks
   ↓
3. Combine chunks into context
   ↓
4. Send context + question to LLM
   ↓
5. LLM generates answer based on context
```

### Implementation

```python
def rag_answer(question: str, llm_client):
    """
    Answer question using RAG.
    """
    # 1. Retrieve relevant chunks
    chunks = semantic_search(question, top_k=5)
    
    # 2. Build context
    context = "\n\n".join([
        f"Source {i+1}: {chunk.chunk_text}"
        for i, chunk in enumerate(chunks)
    ])
    
    # 3. Create prompt
    prompt = f"""
    Use the following context to answer the question. 
    If the answer is not in the context, say "I don't know."
    
    Context:
    {context}
    
    Question: {question}
    
    Answer:
    """
    
    # 4. Generate answer
    response = llm_client.generate(prompt)
    
    # 5. Return answer with sources
    return {
        'answer': response,
        'sources': [
            {'text': c.chunk_text, 'resource_id': c.resource_id}
            for c in chunks
        ]
    }
```

### Benefits

- ✅ **Reduces hallucinations** (facts from retrieved data)
- ✅ **Provides sources** (traceable to original documents)
- ✅ **Works with latest data** (no retraining needed)
- ✅ **More accurate** (grounded in actual content)

---

## 10. CourseDB-AI Implementation

### Use Cases

1. **Question Discovery**
   ```python
   query = "Find questions about query optimization techniques"
   results = semantic_search(query)
   # Returns questions about EXPLAIN, indexes, JOIN algorithms
   ```

2. **Smart Recommendations**
   ```python
   similar = find_similar_questions(question_id=123)
   # Returns conceptually similar questions
   ```

3. **Topic Exploration**
   ```python
   query = "What are the main concepts in transaction management?"
   results = semantic_search(query)
   # Returns ACID, isolation levels, deadlocks, etc.
   ```

4. **RAG-powered Q&A**
   ```python
   answer = rag_answer("How do I optimize a slow query?")
   # Returns answer synthesized from course materials
   ```

### Complete Example

```python
# CourseDB-AI Semantic Search API
@app.post("/api/search/semantic")
async def search_semantic(
    query: str,
    top_k: int = 10,
    search_type: str = "hybrid"  # "semantic", "keyword", "hybrid"
):
    """
    Semantic search endpoint.
    """
    if search_type == "semantic":
        results = semantic_search(query, top_k)
    elif search_type == "keyword":
        results = keyword_search(query, top_k)
    else:  # hybrid
        results = hybrid_search(query, top_k)
    
    return {
        'query': query,
        'results': [
            {
                'chunk_id': r.chunk_id,
                'text': r.chunk_text,
                'resource_id': r.resource_id,
                'title': r.title,
                'similarity': r.similarity
            }
            for r in results
        ]
    }
```

---

## 11. Best Practices

### ✅ DO

1. **Start with good embeddings** - Use established models
2. **Chunk appropriately** - 200-500 tokens with overlap
3. **Use hybrid search** - Combine keyword + semantic
4. **Index vectors** - HNSW for large datasets
5. **Store metadata** - Track sources, chunks, models
6. **Monitor quality** - Measure recall, precision
7. **Version embeddings** - Track which model used

### ❌ DON'T

1. **Don't embed entire documents** - Chunk first
2. **Don't ignore chunk overlap** - Preserves context
3. **Don't use only semantic search** - Miss exact matches
4. **Don't forget to normalize** - Especially for dot product
5. **Don't skip evaluation** - Test with real queries
6. **Don't mix embedding models** - Keep consistent
7. **Don't neglect index tuning** - Adjust parameters

---

## 12. Summary

**Key Takeaways:**

1. **Semantic search** finds by meaning, not just keywords
2. **Embeddings** are numerical representations of text
3. **pgvector** adds vector operations to PostgreSQL
4. **Chunking** breaks documents into searchable pieces
5. **Hybrid search** combines keyword + semantic for best results
6. **RAG** enhances LLMs with retrieved context
7. **Indexing** makes vector search fast at scale

**Next Steps:**
- Complete exercises.md for hands-on practice
- Follow implementation_plan.md for 7-day learning path
- Review mistakes_to_expect.md to avoid common pitfalls
- Build semantic search for CourseDB-AI

**Week 11 Preview:** Frontend integration with Streamlit!

---

## Resources

- [pgvector Documentation](https://github.com/pgvector/pgvector)
- [Sentence Transformers](https://www.sbert.net/)
- [OpenAI Embeddings](https://platform.openai.com/docs/guides/embeddings)
- [Vector Search Best Practices](https://www.pinecone.io/learn/vector-search/)

---

## 🧭 Navigation

**[← Previous: Week 9](../week_09_transactions/reflection.md)** | **[Back to Week 10 Overview](README.md)** | **[Next: Theory Notes →](theory_notes.md)**

---

## 📋 Week 10 File Sequence

1. **[Week 10 README](README.md)** ← You are here
2. **[Theory Notes](theory_notes.md)** - Core concepts
3. **[Exercises](exercises.md)** - Practice
4. **[Implementation Plan](implementation_plan.md)** - Apply concepts
5. **[Checkpoints](checkpoints.md)** - Track progress
6. **[Mistakes to Expect](mistakes_to_expect.md)** - Common pitfalls
7. **[Reflection](reflection.md)** - Weekly reflection
8. **[→ Week 11](../week_11_frontend_integration/README.md)** - Continue journey

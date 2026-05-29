# Week 10: Semantic Search & Vector Databases - Theory Notes

## 📚 Core Concepts

### 1. What is Semantic Search?

**Semantic Search**: Searching by *meaning* rather than exact keyword matching.

**Traditional Keyword Search:**
```sql
SELECT * FROM questions
WHERE question_text ILIKE '%normalization%';
-- Only finds exact word "normalization"
```

**Semantic Search:**
```python
# Find similar questions even if they don't contain exact words
query = "database design best practices"
# Returns: questions about normalization, ER modeling, constraints
#          even if they don't mention "best practices"
```

**Why Semantic Search?**
- Understands synonyms (car = automobile)
- Handles paraphrasing ("how to normalize" = "normalization steps")
- Works across languages
- Better user experience

---

### 2. Vector Embeddings

**Embedding**: Converting text into a numerical vector (list of numbers).

**Example:**
```python
text = "What is normalization?"
embedding = [0.23, -0.45, 0.67, 0.12, ...]  # 768 dimensions
```

**Properties:**
- Similar texts → similar vectors
- Vector math captures meaning
- Fixed size (e.g., 768 dimensions)

**How Embeddings Work:**
```
Text → Embedding Model → Vector
"database normalization" → Model → [0.23, 0.45, -0.12, ...]
"normalize tables"       → Model → [0.21, 0.43, -0.10, ...]
"cats and dogs"          → Model → [-0.67, 0.12, 0.89, ...]
```

Notice: First two are similar (normalization), third is different (animals).

---

### 3. Similarity Measures

#### **Cosine Similarity**
Measures angle between vectors.

**Formula:**
```
cosine_similarity(A, B) = (A · B) / (||A|| * ||B||)
```

**Range**: -1 to 1
- 1 = identical direction
- 0 = orthogonal (unrelated)
- -1 = opposite direction

**Example:**
```python
vec1 = [1, 0, 1]  # "database design"
vec2 = [1, 0, 0]  # "database"
vec3 = [0, 1, 0]  # "cats"

cosine_sim(vec1, vec2) = 0.707  # Similar
cosine_sim(vec1, vec3) = 0.0    # Unrelated
```

#### **Euclidean Distance**
Measures straight-line distance.

**Formula:**
```
distance(A, B) = √(Σ(Ai - Bi)²)
```

**Range**: 0 to ∞
- 0 = identical
- Larger = more different

#### **Dot Product**
Simple vector multiplication.

**Used in**: Many vector databases for speed.

---

### 4. pgvector Extension

**pgvector**: PostgreSQL extension for vector operations.

**Installation:**
```sql
CREATE EXTENSION vector;
```

**Vector Data Type:**
```sql
CREATE TABLE embeddings (
    id SERIAL PRIMARY KEY,
    text TEXT,
    embedding VECTOR(768)  -- 768-dimensional vector
);
```

**Inserting Vectors:**
```sql
INSERT INTO embeddings (text, embedding)
VALUES ('What is normalization?', '[0.23, -0.45, 0.67, ...]');
```

**Similarity Search:**
```sql
-- Find top 5 most similar
SELECT text,
       embedding <=> '[0.25, -0.43, 0.65, ...]' AS distance
FROM embeddings
ORDER BY distance
LIMIT 5;
```

**Operators:**
- `<->` : Euclidean distance
- `<#>` : Negative dot product
- `<=>` : Cosine distance

---

### 5. Embedding Models

#### **Sentence Transformers**
Open-source models for generating embeddings.

**Popular Models:**
- `all-MiniLM-L6-v2` (384 dims, fast, good quality)
- `all-mpnet-base-v2` (768 dims, best quality)
- `multi-qa-mpnet-base-dot-v1` (768 dims, optimized for Q&A)

**Usage:**
```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
embedding = model.encode("What is normalization?")
# Returns: numpy array of 384 floats
```

#### **OpenAI Embeddings**
Commercial API with high-quality embeddings.

**Models:**
- `text-embedding-3-small` (1536 dims, fast)
- `text-embedding-3-large` (3072 dims, best quality)

**Usage:**
```python
import openai

response = openai.embeddings.create(
    model="text-embedding-3-small",
    input="What is normalization?"
)
embedding = response.data[0].embedding
```

---

### 6. Indexing Vectors

**Problem**: Searching millions of vectors is slow.

**Solution**: Vector indexes for approximate nearest neighbor (ANN) search.

#### **IVFFlat Index** (pgvector)
Divides vectors into clusters.

```sql
CREATE INDEX ON embeddings
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- lists = number of clusters (√n is good rule of thumb)
```

**Trade-off:**
- Fast search
- Slightly less accurate (approximate)

#### **HNSW Index** (pgvector)
Hierarchical graph structure.

```sql
CREATE INDEX ON embeddings
USING hnsw (embedding vector_cosine_ops);
```

**Trade-off:**
- Faster than IVFFlat
- More memory usage

---

### 7. Chunking Strategy

**Problem**: Documents too large for embedding models (token limits).

**Solution**: Split documents into chunks.

**Chunking Methods:**

#### **Fixed-Size Chunking**
```python
def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []
    for i in range(0, len(text), chunk_size - overlap):
        chunks.append(text[i:i+chunk_size])
    return chunks
```

#### **Sentence Chunking**
```python
import nltk

def chunk_by_sentences(text, sentences_per_chunk=3):
    sentences = nltk.sent_tokenize(text)
    chunks = []
    for i in range(0, len(sentences), sentences_per_chunk):
        chunk = ' '.join(sentences[i:i+sentences_per_chunk])
        chunks.append(chunk)
    return chunks
```

#### **Semantic Chunking**
Split at natural boundaries (paragraphs, sections).

**Best Practices:**
- Overlap chunks (50-100 tokens) to preserve context
- Keep chunks 200-500 tokens
- Store metadata (source, page, section)

---

### 8. Hybrid Search

**Hybrid Search**: Combine keyword search + semantic search.

**Why?**
- Keyword search: Good for exact terms, names, codes
- Semantic search: Good for concepts, synonyms

**Implementation:**
```python
def hybrid_search(query, keyword_weight=0.3, semantic_weight=0.7):
    # Keyword search (BM25 score)
    keyword_results = keyword_search(query)

    # Semantic search (cosine similarity)
    semantic_results = semantic_search(query)

    # Combine scores
    combined = {}
    for doc_id, score in keyword_results:
        combined[doc_id] = score * keyword_weight

    for doc_id, score in semantic_results:
        combined[doc_id] = combined.get(doc_id, 0) + score * semantic_weight

    return sorted(combined.items(), key=lambda x: x[1], reverse=True)
```

**SQL Example:**
```sql
WITH keyword_scores AS (
    SELECT chunk_id, ts_rank(text_search, query) AS score
    FROM chunks
    WHERE text_search @@ query
),
semantic_scores AS (
    SELECT chunk_id, 1 - (embedding <=> query_embedding) AS score
    FROM chunks
    ORDER BY embedding <=> query_embedding
    LIMIT 100
)
SELECT
    c.chunk_id,
    (COALESCE(k.score, 0) * 0.3 + COALESCE(s.score, 0) * 0.7) AS final_score
FROM chunks c
LEFT JOIN keyword_scores k ON c.chunk_id = k.chunk_id
LEFT JOIN semantic_scores s ON c.chunk_id = s.chunk_id
ORDER BY final_score DESC
LIMIT 10;
```

---

### 9. Retrieval-Augmented Generation (RAG)

**RAG**: Enhance LLM responses with retrieved context.

**Process:**
1. User asks question
2. **Retrieve** relevant documents (semantic search)
3. **Augment** prompt with retrieved context
4. **Generate** answer using LLM

**Example:**
```python
def rag_answer(question):
    # 1. Retrieve
    relevant_chunks = semantic_search(question, top_k=5)
    context = "\n\n".join(chunk.text for chunk in relevant_chunks)

    # 2. Augment
    prompt = f"""
    Context: {context}

    Question: {question}

    Answer the question based on the context above.
    """

    # 3. Generate
    answer = llm.generate(prompt)
    return answer, relevant_chunks
```

**Benefits:**
- Reduces hallucinations (LLM making up facts)
- Provides sources/citations
- Works with latest data (no retraining needed)

---

## 🎯 CourseDB-AI Semantic Search

### Database Schema for Vectors:

```sql
-- Resource chunks with embeddings
CREATE TABLE resource_chunks (
    chunk_id SERIAL PRIMARY KEY,
    resource_id INTEGER REFERENCES resources(resource_id),
    chunk_text TEXT NOT NULL,
    chunk_index INTEGER NOT NULL,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Chunk embeddings (separate table for performance)
CREATE TABLE chunk_embeddings (
    chunk_id INTEGER PRIMARY KEY REFERENCES resource_chunks(chunk_id),
    embedding VECTOR(768) NOT NULL,
    model_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Vector index for fast similarity search
CREATE INDEX idx_chunk_embeddings_hnsw
ON chunk_embeddings
USING hnsw (embedding vector_cosine_ops);
```

### Semantic Search Query:

```python
# CourseDB-AI semantic search implementation
def semantic_search_questions(query: str, top_k: int = 10):
    # 1. Generate query embedding
    query_embedding = embedding_model.encode(query)

    # 2. Search database
    results = db.execute("""
        SELECT
            q.question_id,
            q.question_text,
            q.year,
            c.course_title,
            t.topic_name,
            1 - (ce.embedding <=> :query_vec) AS similarity
        FROM questions q
        JOIN chunk_embeddings ce ON q.question_id = ce.chunk_id
        JOIN courses c ON q.course_id = c.course_id
        JOIN topics t ON q.topic_id = t.topic_id
        ORDER BY ce.embedding <=> :query_vec
        LIMIT :top_k
    """, {"query_vec": query_embedding.tolist(), "top_k": top_k})

    return results.fetchall()
```

### Use Cases:

1. **Question Discovery**: "Find questions about database design principles"
2. **Topic Exploration**: "What topics are related to query performance?"
3. **Smart Recommendations**: "Questions similar to this one"
4. **Cross-year Patterns**: "How has this topic evolved over years?"

---

## ✅ Self-Check Questions

1. What's the difference between keyword search and semantic search?
2. What is a vector embedding?
3. What does cosine similarity measure?
4. When would you use IVFFlat vs HNSW index?
5. Why do we chunk documents before embedding?
6. What's the benefit of hybrid search over pure semantic search?
7. What is RAG and why is it useful?
8. What's the trade-off of using vector indexes?

---

## 🔬 Hands-On Exercises

### Exercise 1: Generate Embeddings
```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

texts = [
    "What is database normalization?",
    "Explain the normalization process",
    "How to train a cat?"
]

embeddings = model.encode(texts)

# Compare similarities
from sklearn.metrics.pairwise import cosine_similarity
similarity = cosine_similarity(embeddings)
print(similarity)
# Notice: First two texts are similar (high score)
#         Third is different (low score)
```

### Exercise 2: pgvector Search
```sql
-- 1. Create table
CREATE TABLE test_embeddings (
    id SERIAL PRIMARY KEY,
    text TEXT,
    embedding VECTOR(384)
);

-- 2. Insert sample data (run from Python with actual embeddings)
-- INSERT INTO test_embeddings VALUES (...);

-- 3. Search for similar
SELECT text, embedding <=> '[your_query_vector]' AS distance
FROM test_embeddings
ORDER BY distance
LIMIT 5;
```

### Exercise 3: Chunking

> **TODO(learner):** Implement `chunk_text_with_overlap` below. This is *your*
> exercise — the body is intentionally left as `pass`. A complete reference
> implementation already exists in `app/services/chunking_service.py`; try it
> yourself first, then compare.

```python
def chunk_text_with_overlap(text, chunk_size=200, overlap=50):
    """
    Implement text chunking with overlap.

    Args:
        text: Input text to chunk
        chunk_size: Characters per chunk
        overlap: Overlapping characters between chunks

    Returns:
        List of text chunks
    """
    pass

# Test
text = "..." * 1000  # Long text
chunks = chunk_text_with_overlap(text)
print(f"Created {len(chunks)} chunks")
print(f"First chunk: {chunks[0][:100]}...")
```

---

## 🎓 CourseDB-AI Integration Checklist

- [ ] Install pgvector extension
- [ ] Create embedding service
- [ ] Implement chunking strategy
- [ ] Generate embeddings for questions
- [ ] Create vector indexes
- [ ] Build semantic search endpoint
- [ ] Add hybrid search (keyword + semantic)
- [ ] Implement RAG for question answering
- [ ] Add similarity-based recommendations
- [ ] Create analytics dashboard (topic clustering)

---

**Next Week (Week 11):** Frontend integration with Streamlit - building the user interface!

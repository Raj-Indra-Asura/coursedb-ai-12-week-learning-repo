# Week 10: Semantic Search & Vector Databases - Exercises

## 🎯 Exercise Overview

Build semantic search skills through hands-on practice:

1. **Vector Embeddings** - Generate and understand embeddings
2. **Similarity Measures** - Calculate and compare similarity
3. **pgvector Setup** - Install and use vector extension
4. **Chunking** - Split documents effectively
5. **Semantic Search** - Build search systems
6. **Hybrid Search** - Combine keyword + semantic
7. **RAG Implementation** - Build Q&A systems

**Prerequisites:**
- PostgreSQL with pgvector extension
- Python with sentence-transformers
- CourseDB-AI database

---

## Exercise Set 1: Understanding Embeddings

### Exercise 1.1: Generate Your First Embeddings

```python
from sentence_transformers import SentenceTransformer
import numpy as np

# Load model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Generate embeddings
texts = [
    "What is database normalization?",
    "Explain the normalization process",
    "How do I normalize a database?",
    "What are the benefits of cats?"
]

embeddings = model.encode(texts)

print(f"Shape: {embeddings.shape}")
print(f"First embedding (first 10 dims): {embeddings[0][:10]}")
```

**Tasks:**
1. Run the code and observe embedding dimensions
2. Add 5 more texts (3 about databases, 2 about unrelated topics)
3. Generate embeddings for all texts
4. Notice: Do database texts have similar values?

**Questions:**
- What are the dimensions of each embedding?
- Are the values normalized?
- Do similar texts have similar embeddings? (visual inspection)

---

### Exercise 1.2: Visualizing Embeddings

```python
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# Reduce to 2D for visualization
pca = PCA(n_components=2)
embeddings_2d = pca.fit_transform(embeddings)

# Plot
plt.figure(figsize=(10, 6))
plt.scatter(embeddings_2d[:, 0], embeddings_2d[:, 1])
for i, txt in enumerate(texts):
    plt.annotate(txt[:30], (embeddings_2d[i, 0], embeddings_2d[i, 1]))
plt.title('Embedding Visualization (2D PCA)')
plt.show()
```

**Tasks:**
1. Plot your embeddings
2. Observe clustering of similar texts
3. Try with 10+ texts on different topics
4. Create separate clusters for each topic

**Questions:**
- Do similar texts cluster together?
- How much variance is explained by 2 components?
- What would 3D look like?

---

## Exercise Set 2: Similarity Measures

### Exercise 2.1: Calculate Cosine Similarity

```python
from sklearn.metrics.pairwise import cosine_similarity

# Texts
text1 = "database normalization process"
text2 = "normalizing database tables"
text3 = "cute cats and dogs"

# Embeddings
emb1 = model.encode([text1])
emb2 = model.encode([text2])
emb3 = model.encode([text3])

# Similarities
sim_1_2 = cosine_similarity(emb1, emb2)[0][0]
sim_1_3 = cosine_similarity(emb1, emb3)[0][0]

print(f"Similarity (text1, text2): {sim_1_2:.4f}")
print(f"Similarity (text1, text3): {sim_1_3:.4f}")
```

**Tasks:**
1. Calculate similarities for your texts
2. Find the most similar pair
3. Find the least similar pair
4. Create a similarity matrix for all texts

**Expected Results:**
- Database texts: similarity > 0.7
- Unrelated texts: similarity < 0.3

---

### Exercise 2.2: Compare Similarity Measures

```python
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances

def compare_measures(emb1, emb2):
    # Cosine similarity
    cos_sim = cosine_similarity([emb1], [emb2])[0][0]
    
    # Euclidean distance
    euc_dist = euclidean_distances([emb1], [emb2])[0][0]
    
    # Dot product
    dot_prod = np.dot(emb1, emb2)
    
    return cos_sim, euc_dist, dot_prod

# Compare
cos, euc, dot = compare_measures(embeddings[0], embeddings[1])
print(f"Cosine: {cos:.4f}, Euclidean: {euc:.4f}, Dot: {dot:.4f}")
```

**Tasks:**
1. Compare all three measures for 5 text pairs
2. Rank pairs by each measure
3. Do rankings match?
4. Which measure works best for your use case?

---

## Exercise Set 3: pgvector Setup

### Exercise 3.1: Install and Enable pgvector

```sql
-- Check if pgvector is available
SELECT * FROM pg_available_extensions WHERE name = 'vector';

-- Enable extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Verify installation
SELECT * FROM pg_extension WHERE extname = 'vector';
```

**Tasks:**
1. Install pgvector (if not already)
2. Enable extension in your database
3. Verify it's working

---

### Exercise 3.2: Create Vector Table

```sql
-- Create table for embeddings
CREATE TABLE IF NOT EXISTS test_embeddings (
    id SERIAL PRIMARY KEY,
    text TEXT NOT NULL,
    embedding VECTOR(384) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Verify table
\d test_embeddings
```

**Tasks:**
1. Create the table
2. Verify vector column type
3. Check dimension (384)

---

### Exercise 3.3: Insert Embeddings

```python
from sqlalchemy import create_engine, text

# Database connection
engine = create_engine('postgresql://user:pass@localhost/coursedb')

# Insert embeddings
with engine.connect() as conn:
    for i, (txt, emb) in enumerate(zip(texts, embeddings)):
        conn.execute(text("""
            INSERT INTO test_embeddings (text, embedding)
            VALUES (:text, :embedding)
        """), {"text": txt, "embedding": emb.tolist()})
    conn.commit()

print(f"Inserted {len(texts)} embeddings")
```

**Tasks:**
1. Insert your generated embeddings
2. Verify with SELECT count
3. Inspect a few rows

---

### Exercise 3.4: Similarity Search

```sql
-- Generate query embedding in Python first
-- query_embedding = model.encode(["database design best practices"])

-- Search for similar
SELECT 
    id,
    text,
    embedding <=> '[0.1, 0.2, ...]'::vector AS distance
FROM test_embeddings
ORDER BY distance
LIMIT 5;
```

**Tasks:**
1. Generate query embedding for "optimization techniques"
2. Search for top 5 similar texts
3. Verify results make sense
4. Try with different queries

---

## Exercise Set 4: Chunking Strategies

### Exercise 4.1: Fixed-Size Chunking

```python
def chunk_text(text, chunk_size=200, overlap=50):
    """
    Implement fixed-size chunking with overlap.
    """
    chunks = []
    start = 0
    
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append({
            'text': text[start:end],
            'start': start,
            'end': end
        })
        start += chunk_size - overlap
    
    return chunks

# Test
long_text = """Database normalization is the process of organizing data
to reduce redundancy. First normal form requires atomic values.
Second normal form eliminates partial dependencies. Third normal
form removes transitive dependencies.""" * 10

chunks = chunk_text(long_text, chunk_size=200, overlap=50)
print(f"Created {len(chunks)} chunks")
for i, chunk in enumerate(chunks[:3]):
    print(f"\nChunk {i}: {chunk['text'][:100]}...")
```

**Tasks:**
1. Implement the chunking function
2. Test with different chunk_size values
3. Test with different overlap values
4. Find optimal parameters for your use case

**Questions:**
- How many chunks are created?
- What happens with no overlap?
- What happens with 50% overlap?

---

### Exercise 4.2: Sentence-Based Chunking

```python
import nltk
nltk.download('punkt')

def chunk_by_sentences(text, sentences_per_chunk=3):
    """
    Implement sentence-based chunking.
    """
    sentences = nltk.sent_tokenize(text)
    chunks = []
    
    for i in range(0, len(sentences), sentences_per_chunk):
        chunk_sentences = sentences[i:i+sentences_per_chunk]
        chunks.append(' '.join(chunk_sentences))
    
    return chunks

# Test
chunks = chunk_by_sentences(long_text, sentences_per_chunk=3)
print(f"Created {len(chunks)} chunks")
for i, chunk in enumerate(chunks[:3]):
    print(f"\nChunk {i}: {chunk}")
```

**Tasks:**
1. Implement sentence-based chunking
2. Compare with fixed-size chunking
3. Which preserves meaning better?
4. Test with different sentence counts

---

## Exercise Set 5: Building Semantic Search

### Exercise 5.1: Create Schema

```sql
-- Resource chunks table
CREATE TABLE IF NOT EXISTS resource_chunks (
    chunk_id SERIAL PRIMARY KEY,
    resource_id INTEGER NOT NULL,
    chunk_text TEXT NOT NULL,
    chunk_index INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Chunk embeddings table
CREATE TABLE IF NOT EXISTS chunk_embeddings (
    chunk_id INTEGER PRIMARY KEY REFERENCES resource_chunks(chunk_id),
    embedding VECTOR(384) NOT NULL,
    model_name VARCHAR(100) DEFAULT 'all-MiniLM-L6-v2',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create index
CREATE INDEX IF NOT EXISTS idx_embeddings_vector
ON chunk_embeddings
USING hnsw (embedding vector_cosine_ops);
```

**Tasks:**
1. Create both tables
2. Create the vector index
3. Verify schema with \d commands

---

### Exercise 5.2: Index Documents

```python
class SemanticIndexer:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.model_name = model_name
    
    def index_document(self, resource_id, text, db):
        """
        Chunk and index a document.
        """
        # 1. Chunk text
        chunks = chunk_text(text, chunk_size=300, overlap=50)
        
        # 2. For each chunk
        for i, chunk_data in enumerate(chunks):
            # Insert chunk
            result = db.execute(text("""
                INSERT INTO resource_chunks 
                (resource_id, chunk_text, chunk_index)
                VALUES (:resource_id, :text, :index)
                RETURNING chunk_id
            """), {
                'resource_id': resource_id,
                'text': chunk_data['text'],
                'index': i
            })
            chunk_id = result.scalar()
            
            # Generate embedding
            embedding = self.model.encode(chunk_data['text'])
            
            # Insert embedding
            db.execute(text("""
                INSERT INTO chunk_embeddings 
                (chunk_id, embedding, model_name)
                VALUES (:chunk_id, :embedding, :model_name)
            """), {
                'chunk_id': chunk_id,
                'embedding': embedding.tolist(),
                'model_name': self.model_name
            })
        
        db.commit()
        return len(chunks)

# Test
indexer = SemanticIndexer()
num_chunks = indexer.index_document(
    resource_id=1,
    text=long_text,
    db=conn
)
print(f"Indexed {num_chunks} chunks")
```

**Tasks:**
1. Implement the indexer
2. Index 3-5 documents
3. Verify chunks are created
4. Verify embeddings are stored

---

### Exercise 5.3: Implement Search

```python
class SemanticSearcher:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
    
    def search(self, query, db, top_k=5):
        """
        Search for similar chunks.
        """
        # 1. Embed query
        query_embedding = self.model.encode(query)
        
        # 2. Search database
        results = db.execute(text("""
            SELECT 
                rc.chunk_id,
                rc.chunk_text,
                rc.resource_id,
                1 - (ce.embedding <=> :query_vec) AS similarity
            FROM chunk_embeddings ce
            JOIN resource_chunks rc ON ce.chunk_id = rc.chunk_id
            ORDER BY ce.embedding <=> :query_vec
            LIMIT :top_k
        """), {
            'query_vec': query_embedding.tolist(),
            'top_k': top_k
        })
        
        return results.fetchall()

# Test
searcher = SemanticSearcher()
results = searcher.search("database optimization", conn, top_k=5)

for r in results:
    print(f"\nSimilarity: {r.similarity:.4f}")
    print(f"Text: {r.chunk_text[:100]}...")
```

**Tasks:**
1. Implement the searcher
2. Test with different queries
3. Verify results are relevant
4. Try top_k values (5, 10, 20)

---

## Exercise Set 6: Hybrid Search

### Exercise 6.1: Keyword Search

```python
def keyword_search(query, db, top_k=10):
    """
    Implement PostgreSQL full-text search.
    """
    results = db.execute(text("""
        SELECT 
            chunk_id,
            chunk_text,
            ts_rank(
                to_tsvector('english', chunk_text),
                plainto_tsquery('english', :query)
            ) AS score
        FROM resource_chunks
        WHERE to_tsvector('english', chunk_text) @@ 
              plainto_tsquery('english', :query)
        ORDER BY score DESC
        LIMIT :top_k
    """), {'query': query, 'top_k': top_k})
    
    return results.fetchall()

# Test
results = keyword_search("normalization", conn)
for r in results:
    print(f"Score: {r.score:.4f}, Text: {r.chunk_text[:100]}...")
```

**Tasks:**
1. Implement keyword search
2. Compare with semantic search
3. What are the differences?

---

### Exercise 6.2: Combine Searches

```python
def hybrid_search(query, db, top_k=10, 
                  keyword_weight=0.3, semantic_weight=0.7):
    """
    Implement hybrid search.
    """
    # Keyword search
    keyword_results = keyword_search(query, db, top_k * 2)
    keyword_scores = {r.chunk_id: r.score for r in keyword_results}
    
    # Semantic search
    semantic_results = searcher.search(query, db, top_k * 2)
    semantic_scores = {r.chunk_id: r.similarity for r in semantic_results}
    
    # Combine
    all_ids = set(keyword_scores.keys()) | set(semantic_scores.keys())
    combined = []
    
    for chunk_id in all_ids:
        k_score = keyword_scores.get(chunk_id, 0)
        s_score = semantic_scores.get(chunk_id, 0)
        final_score = k_score * keyword_weight + s_score * semantic_weight
        combined.append((chunk_id, final_score))
    
    # Sort and get top
    combined.sort(key=lambda x: x[1], reverse=True)
    top_ids = [cid for cid, _ in combined[:top_k]]
    
    # Fetch chunks
    results = db.execute(text("""
        SELECT * FROM resource_chunks
        WHERE chunk_id = ANY(:ids)
    """), {'ids': top_ids})
    
    return results.fetchall()

# Test
results = hybrid_search("query optimization", conn, top_k=5)
for r in results:
    print(f"Text: {r.chunk_text[:100]}...")
```

**Tasks:**
1. Implement hybrid search
2. Test with different weight combinations
3. Which works best?
4. Compare all three approaches

---

## Exercise Set 7: RAG Implementation

### Exercise 7.1: Basic RAG

```python
def rag_answer(question, db, llm_function):
    """
    Implement RAG for question answering.
    """
    # 1. Retrieve relevant chunks
    chunks = searcher.search(question, db, top_k=3)
    
    # 2. Build context
    context = "\n\n".join([
        f"[Source {i+1}] {chunk.chunk_text}"
        for i, chunk in enumerate(chunks)
    ])
    
    # 3. Create prompt
    prompt = f"""
    Based on the following context, answer the question.
    If the answer is not in the context, say "I don't know."
    
    Context:
    {context}
    
    Question: {question}
    
    Answer:
    """
    
    # 4. Generate answer (mock for exercise)
    # answer = llm_function(prompt)
    
    return {
        'question': question,
        'context': context,
        'sources': [c.chunk_text for c in chunks]
    }

# Test
result = rag_answer("What is normalization?", conn, None)
print(f"Question: {result['question']}")
print(f"\nContext:\n{result['context']}")
```

**Tasks:**
1. Implement RAG pipeline
2. Test with 5 questions
3. Verify context is relevant
4. Try with different top_k values

---

## Challenge Exercises

### Challenge 1: Multi-Modal Search

Extend semantic search to handle:
- Text chunks
- Image embeddings (from diagrams)
- Code snippets

### Challenge 2: Query Expansion

Implement query expansion:
1. User query: "optimize queries"
2. Expand to: ["optimize queries", "query performance", "speed up database"]
3. Search with all variations
4. Combine results

### Challenge 3: Semantic Clustering

Cluster similar chunks:
1. Generate all embeddings
2. Use K-means clustering
3. Visualize clusters
4. Label each cluster

### Challenge 4: Re-ranking

Implement two-stage search:
1. Retrieve top 100 with fast search
2. Re-rank with more expensive model
3. Return top 10

---

## Summary

After completing these exercises, you should be able to:

✅ Generate and understand vector embeddings  
✅ Calculate similarity between vectors  
✅ Use pgvector for vector storage and search  
✅ Chunk documents effectively  
✅ Build semantic search systems  
✅ Implement hybrid search  
✅ Create RAG pipelines  

**Next Steps:**
- Apply to CourseDB-AI
- Follow implementation_plan.md
- Review mistakes_to_expect.md
- Complete reflection.md

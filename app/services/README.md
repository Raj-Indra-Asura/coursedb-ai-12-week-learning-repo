# Services Layer

This directory contains business logic services for CourseDB-AI.

---

## 📋 Service Architecture

Services separate business logic from API handlers and database operations following a clean architecture pattern:

```
API Handler → Service → Database
```

**Benefits**:
- Reusable business logic
- Easier testing
- Separation of concerns
- Cleaner code organization

---

## 📦 Services

### `sql_search_service.py` (Week 6)

**Purpose**: Implement SQL-based search with filters

**Methods**:
- `search_questions()` - Search questions with filters
- `search_resources()` - Search resources with filters

**Learning Focus**: Dynamic SQL query building, filtering, pagination

---

### `analytics_service.py` (Week 6)

**Purpose**: Generate analytical insights

**Methods**:
- `get_topic_frequency()` - Question count per topic
- `get_year_wise_trends()` - Topic trends over years
- `get_difficulty_distribution()` - Difficulty breakdown
- `get_resource_summary()` - Resource statistics

**Learning Focus**: SQL aggregate functions, views, data visualization

---

### `chunking_service.py` (Week 10)

**Purpose**: Split resources into chunks for embedding

**Methods**:
- `clean_text()` - Text normalization
- `chunk_text()` - Split text into overlapping chunks
- `chunk_resource()` - Process full resource

**Learning Focus**: Text processing, chunking strategies, context preservation

**Configuration**:
- Chunk size: 250 words
- Overlap: 50 words
- Minimum chunk size: 50 words

---

### `embedding_service.py` (Week 10)

**Purpose**: Generate vector embeddings using Sentence Transformers

**Methods**:
- `generate_embedding()` - Single text embedding
- `generate_embeddings_batch()` - Batch embedding (faster)
- `encode_for_search()` - Query encoding
- `compute_similarity()` - Cosine similarity calculation

**Model**: sentence-transformers/all-MiniLM-L6-v2
- Embedding dimension: 384
- Max sequence length: 256 tokens

**Learning Focus**: Transformer models, vector representations, batch processing

---

### `semantic_search_service.py` (Week 10)

**Purpose**: Implement vector similarity search with pgvector

**Methods**:
- `search()` - Semantic search with top-k retrieval
- `compare_with_keyword_search()` - Compare semantic vs keyword
- `get_similar_chunks()` - Find similar resources

**Learning Focus**: Vector similarity, cosine distance, pgvector operators

**pgvector Operators**:
- `<=>` : Cosine distance (we use this)
- `<->` : L2 distance
- `<#>` : Negative inner product

---

## 🔄 Service Workflow Example

### Semantic Search Flow

```python
# 1. User submits query
query = "questions about deadlock"

# 2. Embedding Service generates query vector
embedding_service = EmbeddingService()
query_embedding = embedding_service.encode_for_search(query)

# 3. Semantic Search Service finds similar chunks
search_service = SemanticSearchService(db, embedding_service)
results = search_service.search(query, top_k=5)

# 4. Results returned to API handler
# [
#   {"chunk_text": "...", "similarity": 0.85, ...},
#   ...
# ]
```

---

## 🧪 Testing Services

Services should be tested independently of API handlers:

```python
# Example test
def test_chunking_service():
    service = ChunkingService(chunk_size=100, overlap=20)
    text = "Long text to be chunked..."
    chunks = service.chunk_text(text)

    assert len(chunks) > 0
    assert all(len(chunk[0].split()) <= 100 for chunk in chunks)
```

---

## 📝 Implementation Schedule

| Week | Service | Focus |
|------|---------|-------|
| **Week 6** | SQL Search, Analytics | SQL queries, views, aggregates |
| **Week 10** | Chunking, Embedding, Semantic Search | Text processing, embeddings, vector search |
| **Week 11** | Integration | Connect all services in Streamlit UI |

---

## 🎓 Learning Tips

1. **Start with SQL Search**: Build foundation before AI features
2. **Test incrementally**: Write tests as you implement
3. **Understand the flow**: Trace data from API to database
4. **Use type hints**: Makes code more maintainable
5. **Add logging**: Debug issues easily
6. **Profile performance**: Optimize slow queries

---

## 🔗 Related Documentation

- [app/api/README.md](../api/README.md) - API endpoints
- [docs/semantic_search/](../../docs/semantic_search/) - Semantic search theory
- [Week 6 README](../../weeks/week_06_sql_queries_views_triggers_constraints/README.md)
- [Week 10 README](../../weeks/week_10_embeddings_semantic_search_pgvector/README.md)

---

**Remember**: Services contain business logic, not database models or API routing. Keep them focused and testable!

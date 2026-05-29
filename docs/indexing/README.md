# Indexing Documentation

**Week 7-8: Indexing + Query Optimization**

This directory contains indexing strategy and performance analysis.

---

## 📁 Files to Create

### `indexing_notes.md` (Week 7)
- B+ tree concepts
- Hash index concepts
- When to use each type
- PostgreSQL index types

### `index_strategy.md` (Week 7)
- Which columns to index
- Index choices for CourseDB-AI
- Composite indexes

### `query_plan_analysis.md` (Week 8)
- EXPLAIN ANALYZE outputs
- Before/after index comparisons
- Performance improvements
- Query optimization insights

---

## 🎯 Indexes Created

- `idx_questions_difficulty` on questions(difficulty)
- `idx_resources_year` on resources(academic_year)
- `idx_topics_name` on topics(topic_name)
- `idx_chunk_embeddings_vector` on chunk_embeddings using ivfflat

---

**TODO (Week 7-8)**: Document indexing decisions and performance results

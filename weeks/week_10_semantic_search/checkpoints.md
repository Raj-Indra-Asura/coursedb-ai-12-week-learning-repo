# Week 10: Semantic Search & Vector Databases - Daily Checkpoints

## 🎯 Purpose

Track your progress through Week 10 with concrete checkpoints.

---

## Day 1: Embeddings & Similarity

### Knowledge Checkpoints
- [ ] Can explain what embeddings are
- [ ] Understand cosine similarity
- [ ] Know euclidean distance vs dot product
- [ ] Can generate embeddings with sentence-transformers

### Practical Checkpoints
- [ ] Exercise 1.1 completed (Generate embeddings)
- [ ] Exercise 1.2 completed (Visualize)
- [ ] Exercise 2.1 completed (Cosine similarity)
- [ ] Exercise 2.2 completed (Compare measures)

### Self-Assessment
**Can I do this without reference?**
```python
# Generate embedding for text
# Calculate similarity between two texts
# Explain why similar texts have similar vectors
```
- [ ] Yes, confidently
- [ ] Yes, with hints
- [ ] Not yet

**Confidence: ___/5**

---

## Day 2: pgvector Setup

### Knowledge Checkpoints
- [ ] Know what pgvector is
- [ ] Understand VECTOR data type
- [ ] Know pgvector operators (<->, <#>, <=>)
- [ ] Can perform similarity search in SQL

### Practical Checkpoints
- [ ] Exercise 3.1 completed (Install pgvector)
- [ ] Exercise 3.2 completed (Create table)
- [ ] Exercise 3.3 completed (Insert embeddings)
- [ ] Exercise 3.4 completed (Search)

### Can I Do This?
```sql
-- Create vector table
-- Insert embedding
-- Search for similar vectors
```
- [ ] All correct
- [ ] Need reference
- [ ] Not yet

**Confidence: ___/5**

---

## Day 3: Chunking & Indexing

### Knowledge Checkpoints
- [ ] Understand why chunking is needed
- [ ] Know different chunking strategies
- [ ] Understand IVFFlat vs HNSW indexes
- [ ] Can choose appropriate index

### Practical Checkpoints
- [ ] Exercise 4.1 completed (Fixed-size chunking)
- [ ] Exercise 4.2 completed (Sentence chunking)
- [ ] Created index for vectors
- [ ] Benchmarked search performance

### Chunking Quiz
For a 5000-word article:
- Chunk size: _____ (chars/tokens)
- Overlap: _____ (chars/tokens)
- Method: _____ (fixed/sentence/semantic)
- Why: _________________________________________________

**Confidence: ___/5**

---

## Day 4: Semantic Search System

### Knowledge Checkpoints
- [ ] Understand indexing pipeline
- [ ] Can build document indexer
- [ ] Can build search function
- [ ] Understand end-to-end workflow

### Practical Checkpoints
- [ ] Exercise 5.1 completed (Schema)
- [ ] Exercise 5.2 completed (Indexer)
- [ ] Exercise 5.3 completed (Searcher)
- [ ] Indexed 10+ documents

### Can I Build This?
```
Document → Chunk → Embed → Store → Search
```
- [ ] Yes, from scratch
- [ ] Yes, with reference
- [ ] Not yet

**Confidence: ___/5**

---

## Day 5: Hybrid Search

### Knowledge Checkpoints
- [ ] Understand hybrid search benefits
- [ ] Know when to use keyword vs semantic
- [ ] Can combine search scores
- [ ] Can tune weights

### Practical Checkpoints
- [ ] Exercise 6.1 completed (Keyword search)
- [ ] Exercise 6.2 completed (Hybrid search)
- [ ] Tested weight combinations
- [ ] Found optimal weights

### Hybrid Search Parameters
For CourseDB-AI:
- Keyword weight: _____
- Semantic weight: _____
- Why: _________________________________________________

**Confidence: ___/5**

---

## Day 6: RAG & Advanced

### Knowledge Checkpoints
- [ ] Understand RAG pipeline
- [ ] Can retrieve relevant context
- [ ] Know how to combine with LLM
- [ ] Understand limitations

### Practical Checkpoints
- [ ] Exercise 7.1 completed (RAG)
- [ ] Tested with 10+ questions
- [ ] Evaluated answer quality
- [ ] Implemented enhancements

### RAG Pipeline
```
Question → Retrieve → Context → LLM → Answer
```
- [ ] Can implement
- [ ] Understand each step
- [ ] Know how to improve

**Confidence: ___/5**

---

## Day 7: Integration & Review

### Integration Checkpoints
- [ ] Semantic search API endpoint working
- [ ] Course materials indexed
- [ ] Search returns relevant results
- [ ] Tested with real queries

### Review Checkpoints
- [ ] All exercises completed
- [ ] All concepts understood
- [ ] Applied to CourseDB-AI
- [ ] Reflection.md completed

---

## Week 10 Final Assessment

### Comprehensive Test (No Reference)

1. **What are embeddings?**
   _____________________________________________________

2. **Name three similarity measures:**
   1. _____________________________________________________
   2. _____________________________________________________
   3. _____________________________________________________

3. **Why chunk documents?**
   _____________________________________________________

4. **IVFFlat vs HNSW - when to use each?**
   _____________________________________________________

5. **Hybrid search formula:**
   _____________________________________________________

6. **RAG pipeline steps:**
   _____________________________________________________

### Practical Skills
- [ ] Can generate embeddings
- [ ] Can use pgvector
- [ ] Can chunk documents
- [ ] Can build semantic search
- [ ] Can implement hybrid search
- [ ] Can create RAG system

### Applied Knowledge
- [ ] CourseDB-AI has semantic search
- [ ] Materials are indexed
- [ ] Search quality is good
- [ ] Documented implementation

---

## Overall Week 10 Confidence

**Topics (rate 1-5):**
- Embeddings: ___/5
- pgvector: ___/5
- Chunking: ___/5
- Semantic search: ___/5
- Hybrid search: ___/5
- RAG: ___/5

**Overall: ___/5**

---

## Next Steps

**If confidence < 3:**
- Review unclear concepts
- Redo relevant exercises
- Seek additional resources

**If confidence >= 3:**
- ✅ Ready for Week 11!
- Continue to Week 11 (Frontend Integration)

---

**Congratulations on completing Week 10!** You now understand modern semantic search and vector databases - essential skills for AI-powered applications!

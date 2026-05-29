# Week 10: Semantic Search & Vector Databases - 7-Day Implementation Plan

## 📅 Overview

Master semantic search and vector databases in 7 days through structured, hands-on learning.

**Time commitment:** 4-6 hours per day  
**Prerequisites:** Week 9 (Transactions) completed  
**Tools:** PostgreSQL + pgvector, Python, sentence-transformers

---

## Day 1: Embeddings & Similarity

### Morning: Understanding Embeddings (2-3 hours)

**Reading:**
- README.md Sections 1-3
- theory_notes.md Sections 1-3

**Hands-On:**
1. Install sentence-transformers: `pip install sentence-transformers`
2. Complete Exercise 1.1 (Generate embeddings)
3. Complete Exercise 1.2 (Visualize embeddings)
4. Complete Exercise 2.1 (Cosine similarity)

**Deliverable:** Python script that generates and compares embeddings

### Afternoon: Similarity Measures (2-3 hours)

**Hands-On:**
1. Complete Exercise 2.2 (Compare measures)
2. Experiment with different texts
3. Create similarity matrix for 10 texts
4. Document findings

**Checkpoint:**
- [ ] Can generate embeddings
- [ ] Understand similarity measures
- [ ] Can compare texts numerically
- [ ] Confidence: ___/5

---

## Day 2: pgvector Setup

### Morning: Installation & Setup (2-3 hours)

**Reading:**
- README.md Section 4
- theory_notes.md Section 4

**Hands-On:**
1. Install pgvector extension
2. Complete Exercise 3.1 (Enable extension)
3. Complete Exercise 3.2 (Create vector table)
4. Complete Exercise 3.3 (Insert embeddings)

**Deliverable:** Working pgvector database with sample data

### Afternoon: Vector Search (2-3 hours)

**Hands-On:**
1. Complete Exercise 3.4 (Similarity search)
2. Test different operators (<->, <#>, <=>)
3. Compare search results
4. Measure query performance

**Checkpoint:**
- [ ] pgvector installed and working
- [ ] Can store vectors in PostgreSQL
- [ ] Can perform similarity search
- [ ] Confidence: ___/5

---

## Day 3: Chunking & Indexing

### Morning: Chunking Strategies (2-3 hours)

**Reading:**
- README.md Section 6
- theory_notes.md Section 7

**Hands-On:**
1. Complete Exercise 4.1 (Fixed-size chunking)
2. Complete Exercise 4.2 (Sentence chunking)
3. Test with CourseDB-AI content
4. Choose optimal strategy

**Deliverable:** Chunking service for CourseDB-AI

### Afternoon: Vector Indexing (2-3 hours)

**Reading:**
- README.md Section 5

**Hands-On:**
1. Create IVFFlat index
2. Create HNSW index
3. Benchmark search performance
4. Choose index for CourseDB-AI

**Checkpoint:**
- [ ] Understand chunking trade-offs
- [ ] Can chunk documents effectively
- [ ] Understand vector indexes
- [ ] Confidence: ___/5

---

## Day 4: Semantic Search System

### Morning: Build Indexer (2-3 hours)

**Reading:**
- README.md Section 7

**Hands-On:**
1. Complete Exercise 5.1 (Create schema)
2. Complete Exercise 5.2 (Index documents)
3. Index 10 CourseDB-AI resources
4. Verify embeddings stored

**Deliverable:** Working document indexer

### Afternoon: Build Searcher (2-3 hours)

**Hands-On:**
1. Complete Exercise 5.3 (Implement search)
2. Test with various queries
3. Evaluate result quality
4. Tune parameters (top_k, etc.)

**Checkpoint:**
- [ ] Can index documents
- [ ] Can search semantically
- [ ] Results are relevant
- [ ] Confidence: ___/5

---

## Day 5: Hybrid Search

### Morning: Keyword Search (2-3 hours)

**Reading:**
- README.md Section 8

**Hands-On:**
1. Complete Exercise 6.1 (Keyword search)
2. Compare with semantic search
3. Identify strengths/weaknesses
4. Test with specific queries

**Deliverable:** Keyword search implementation

### Afternoon: Hybrid Implementation (2-3 hours)

**Hands-On:**
1. Complete Exercise 6.2 (Hybrid search)
2. Test different weight combinations
3. Evaluate on 20 test queries
4. Find optimal weights

**Checkpoint:**
- [ ] Understand hybrid search benefits
- [ ] Can combine keyword + semantic
- [ ] Found optimal weights
- [ ] Confidence: ___/5

---

## Day 6: RAG & Advanced Features

### Morning: RAG Implementation (2-3 hours)

**Reading:**
- README.md Section 9
- theory_notes.md Section 9

**Hands-On:**
1. Complete Exercise 7.1 (Basic RAG)
2. Test with 10 questions
3. Evaluate answer quality
4. Refine retrieval parameters

**Deliverable:** RAG Q&A system

### Afternoon: Advanced Features (2-3 hours)

**Hands-On:**
1. Implement query expansion (Challenge 2)
2. Add re-ranking (Challenge 4)
3. Test improvements
4. Document results

**Checkpoint:**
- [ ] Understand RAG pipeline
- [ ] Can retrieve relevant context
- [ ] Implemented enhancements
- [ ] Confidence: ___/5

---

## Day 7: Integration & Review

### Morning: CourseDB-AI Integration (2-3 hours)

**Hands-On:**
1. Add semantic search API endpoint
2. Index all course materials
3. Test search functionality
4. Add to frontend (if time)

**Deliverable:** Integrated semantic search in CourseDB-AI

### Afternoon: Review & Optimization (2-3 hours)

**Tasks:**
1. Review all checkpoints
2. Optimize search performance
3. Complete reflection.md
4. Test end-to-end workflow

**Final Checkpoint:**
- [ ] Semantic search working in CourseDB-AI
- [ ] All exercises completed
- [ ] Understand all concepts
- [ ] Overall confidence: ___/5

---

## Week Completion Checklist

**Theory:**
- [ ] Understand vector embeddings
- [ ] Know similarity measures
- [ ] Understand pgvector operations
- [ ] Know chunking strategies
- [ ] Understand vector indexing
- [ ] Know hybrid search benefits
- [ ] Understand RAG pipeline

**Practical:**
- [ ] Can generate embeddings
- [ ] Can use pgvector
- [ ] Can chunk documents
- [ ] Can build semantic search
- [ ] Can implement hybrid search
- [ ] Can create RAG system

**Applied:**
- [ ] CourseDB-AI has semantic search
- [ ] Indexed course materials
- [ ] API endpoints working
- [ ] Tested with real queries

---

## Resources

- [pgvector GitHub](https://github.com/pgvector/pgvector)
- [Sentence Transformers](https://www.sbert.net/)
- [OpenAI Embeddings](https://platform.openai.com/docs/guides/embeddings)

**Next Week:** Week 11 - Frontend Integration!

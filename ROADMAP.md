# CourseDB-AI: 12-Week Learning Roadmap

This document provides a **detailed week-by-week plan** for building CourseDB-AI while learning DBMS concepts and AI infrastructure.

---

## 🧭 Quick Navigation

**[🚀 Start Your Journey](START_HERE.md)** | **[📚 Complete Learning Path](LEARNING_PATH.md)** | **[🏠 Back to README](README.md)**

**Jump to Week**: [1](#week-1-dbms-foundations--project-orientation) | [2](#week-2-sql-basics-through-academic-data) | [3](#week-3-er-modeling--schema-design) | [4](#week-4-functional-dependencies--normalization) | [5](#week-5-postgresql--fastapi-foundation) | [6](#week-6-sql-queries-views-triggers-constraints) | [7](#week-7-indexing-b-tree-hashing) | [8](#week-8-query-optimization--explain) | [9](#week-9-transactions-acid-concurrency) | [10](#week-10-embeddings-pgvector-semantic-search) | [11](#week-11-integrated-coursedb-ai-system) | [12](#week-12-evaluation-polish-portfolio)

---

## 📋 Overview

**Duration**: 12 weeks (3 months)
**Time Commitment**: 10-15 hours per week
**Learning Model**: Theory → Exercises → Implementation → Debugging → Testing → Reflection
**Outcome**: Production-ready portfolio project + deep DBMS + AI understanding

---

## 🎯 Month 1: DBMS Foundations (Weeks 1-4)

### **Week 1: DBMS Foundations + Project Orientation**

**📂 [Go to Week 1](weeks/week_01_dbms_foundations/README.md)**

**Learning Objectives:**
- Understand what a DBMS is and why it matters
- Learn data vs information vs database
- Understand schema vs instance
- Learn physical/logical/view abstraction levels
- Understand file-system limitations
- Position CourseDB-AI as data infrastructure

**Theory Topics:**
- DBMS definition and motivation
- Data vs information
- Schema vs instance
- Three-level architecture (physical, logical, view)
- Why not use plain files or dictionaries?
- How DBMS enables AI systems

**Hands-on Tasks:**
- Create a simple Python dictionary/list-based academic resource store
- Document why it becomes messy (no constraints, no querying, no consistency)
- Write the first draft of PROJECT_SPEC.md
- Create a mental model diagram of CourseDB-AI

**Deliverables:**
- `weeks/week_01_dbms_foundations/theory_notes.md`
- `weeks/week_01_dbms_foundations/mini_project/file_based_resource_store.py`
- `weeks/week_01_dbms_foundations/reflection.md`
- First draft of PROJECT_SPEC.md

**Self-Check Questions:**
- What is the difference between data and information?
- What is a schema? What is an instance?
- Why can't we just use JSON files for CourseDB-AI?
- What problems does a DBMS solve?

---

### **Week 2: SQL Basics Through Academic Data**

**📂 [Go to Week 2](weeks/week_02_sql_basics/README.md)**

**Learning Objectives:**
- Master DDL (CREATE, ALTER, DROP) and DML (INSERT, UPDATE, DELETE)
- Write SELECT queries with WHERE, ORDER BY, LIMIT
- Use aggregates (COUNT, SUM, AVG, MIN, MAX)
- Use GROUP BY and HAVING
- Use LIKE for pattern matching

**Theory Topics:**
- Relational model basics
- Tables, rows, columns, domains
- Primary keys (basic understanding)
- SQL syntax and categories (DDL, DML, DQL)
- Filtering and sorting
- Aggregation

**Hands-on Tasks:**
- Create `schema_week2.sql` with simple tables (courses, topics, questions)
- Intentionally keep schema imperfect (for Week 4 normalization lesson)
- Insert at least 15 sample DBMS questions
- Write 20 SQL exercises covering SELECT, WHERE, ORDER BY, GROUP BY, HAVING
- Run queries in PostgreSQL via psql or DBeaver

**Deliverables:**
- `weeks/week_02_sql_basics/schema_week2.sql`
- `weeks/week_02_sql_basics/seed_week2.sql`
- `weeks/week_02_sql_basics/queries_week2.sql`
- `weeks/week_02_sql_basics/exercises.md` (20 SQL practice problems)
- `weeks/week_02_sql_basics/mistakes_to_expect.md`
- `weeks/week_02_sql_basics/reflection.md`

**Self-Check Questions:**
- What is the difference between WHERE and HAVING?
- When do you use GROUP BY?
- How do you filter with LIKE?
- What aggregate functions are available in SQL?

---

### **Week 3: ER Modeling + Schema Design**

**📂 [Go to Week 3](weeks/week_03_er_modeling/README.md)**

**Learning Objectives:**
- Design ER diagrams with entities, attributes, relationships
- Understand cardinality (1:1, 1:N, M:N)
- Map ER model to relational schema
- Identify primary keys and foreign keys
- Design the conceptual model for CourseDB-AI

**Theory Topics:**
- ER model components (entities, attributes, relationships)
- Strong vs weak entities
- Cardinality and participation
- ER to relational mapping rules
- Primary keys and foreign keys

**Entities for CourseDB-AI:**
- Course, Topic, Resource, Question, Chapter, Tag, ResourceChunk, Embedding, User, SearchLog, AuditLog

**Hands-on Tasks:**
- Create ER diagram for CourseDB-AI in Mermaid or draw.io
- Document each entity: attributes, relationships, cardinality
- Explain why Question-Topic is M:N (many-to-many)
- Explain why Resource-Chunk is 1:N (one-to-many)
- Map ER diagram to relational schema

**Deliverables:**
- `docs/er_diagrams/coursedb_ai_er_design.md`
- `docs/er_diagrams/er_diagram.mmd` (Mermaid)
- `weeks/week_03_er_modeling_schema_design/draft_schema.sql`
- `weeks/week_03_er_modeling_schema_design/er_to_tables.md`
- `weeks/week_03_er_modeling_schema_design/reflection.md`

**Self-Check Questions:**
- What is the difference between an entity and an attribute?
- What is cardinality?
- How do you represent M:N relationships in a relational schema?
- Why is Question-Topic many-to-many?

---

### **Week 4: Functional Dependencies + Normalization**

**📂 [Go to Week 4](weeks/week_04_normalization/README.md)**

**Learning Objectives:**
- Understand functional dependencies (FDs)
- Identify keys using FD closure
- Recognize update/insert/delete anomalies
- Apply normalization: 1NF, 2NF, 3NF, BCNF
- Normalize the CourseDB-AI schema

**Theory Topics:**
- Functional dependencies
- Candidate keys, primary keys, super keys
- Closure of attributes
- Anomalies in bad designs
- Normal forms: 1NF, 2NF, 3NF, BCNF
- When to denormalize (tradeoffs)

**Hands-on Tasks:**
- Create `bad_schema.sql` with denormalized tables
- Document FDs for each table
- Identify anomalies in bad schema
- Create `normalized_schema.sql` in 3NF/BCNF
- Write normalization report

**Deliverables:**
- `docs/normalization/normalization_report.md`
- `docs/normalization/fd_analysis.md`
- `docs/normalization/anomaly_examples.md`
- `weeks/week_04_normalization_functional_dependencies/bad_schema.sql`
- `weeks/week_04_normalization_functional_dependencies/normalized_schema.sql`
- `weeks/week_04_normalization_functional_dependencies/reflection.md`

**Self-Check Questions:**
- What is a functional dependency?
- How do you find candidate keys?
- What anomalies exist in a denormalized table?
- What is the difference between 2NF and 3NF?

---

## 🛠️ Month 2: Backend + DBMS Internals (Weeks 5-8)

### **Week 5: PostgreSQL + FastAPI Foundation**

**📂 [Go to Week 5](weeks/week_05_postgresql_fastapi/README.md)**

**Learning Objectives:**
- Set up PostgreSQL with Docker
- Create FastAPI backend structure
- Connect Python to PostgreSQL using SQLAlchemy
- Create database models with ORM
- Implement health check endpoint

**Theory Topics:**
- PostgreSQL architecture basics
- ORM vs raw SQL
- SQLAlchemy Core vs ORM
- FastAPI routing and dependency injection
- Database connection pooling

**Hands-on Tasks:**
- Create `docker-compose.yml` for PostgreSQL + pgvector
- Create `.env.example` for configuration
- Create `requirements.txt`
- Create `app/backend/main.py` (FastAPI app)
- Create `app/db/database.py` (connection management)
- Create `app/db/models.py` (SQLAlchemy models)
- Create `app/api/health.py` (health endpoint)
- Test database connection

**Deliverables:**
- `docker-compose.yml`
- `.env.example`
- `requirements.txt`
- `app/backend/main.py`
- `app/db/database.py`
- `app/db/models.py`
- `app/api/health.py`
- `weeks/week_05_postgresql_fastapi_foundation/setup_guide.md`
- `weeks/week_05_postgresql_fastapi_foundation/reflection.md`

**Self-Check Questions:**
- What is an ORM?
- What is SQLAlchemy?
- How does FastAPI handle dependencies?
- Why use Docker for PostgreSQL?

---

### **Week 6: SQL Queries, Views, Triggers, Constraints**

**📂 [Go to Week 6](weeks/week_06_advanced_sql/README.md)**

**Learning Objectives:**
- Implement constraints (PK, FK, UNIQUE, CHECK, NOT NULL)
- Create database views for analytics
- Create triggers for audit logging
- Write complex JOIN queries
- Implement analytics endpoints

**Theory Topics:**
- Constraints and their purpose
- Views: why and when
- Triggers: syntax and use cases
- JOINs: INNER, LEFT, RIGHT, FULL
- Subqueries vs JOINs

**Hands-on Tasks:**
- Add constraints to all tables
- Create `audit_logs` table
- Create trigger for question insert/update
- Create views:
  - `topic_question_frequency`
  - `year_wise_topic_frequency`
  - `resource_summary_view`
- Implement API endpoints:
  - `GET /questions`
  - `GET /topics`
  - `GET /analytics/topic-frequency`

**Deliverables:**
- `docs/sql/constraints_report.md`
- `docs/sql/views_and_triggers.md`
- `docs/sql/sql_query_catalog.md`
- `app/api/questions.py`
- `app/api/topics.py`
- `app/api/analytics.py`
- `weeks/week_06_sql_queries_views_triggers_constraints/reflection.md`

**Self-Check Questions:**
- What is the difference between a view and a table?
- When do triggers execute?
- What is a foreign key constraint?
- How do you audit changes in a database?

---

### **Week 7: Indexing, B+ Tree, Hashing**

**📂 [Go to Week 7](weeks/week_07_indexing_bplus/README.md)**

**Learning Objectives:**
- Understand indexing fundamentals
- Learn B+ tree structure and operations
- Learn hash index structure and limitations
- Implement educational B+ tree visualizer
- Implement hash index simulator
- Add PostgreSQL indexes to CourseDB-AI

**Theory Topics:**
- Primary vs secondary indexes
- Dense vs sparse indexes
- Clustered vs non-clustered indexes
- B+ tree: structure, insertion, search
- Hash indexes: static vs dynamic
- When to use which index type

**Hands-on Tasks:**
- Build educational B+ tree insertion visualizer
- Build hash index simulator with collision handling
- Add PostgreSQL indexes:
  - `questions(difficulty)`
  - `resources(academic_year)`
  - `topics(topic_name)`
- Document index choices

**Deliverables:**
- `dbms_internals/bplus_tree/bplus_tree.py`
- `dbms_internals/bplus_tree/README.md`
- `dbms_internals/bplus_tree/tests/test_bplus_tree.py`
- `dbms_internals/hash_index/hash_index.py`
- `dbms_internals/hash_index/README.md`
- `dbms_internals/hash_index/tests/test_hash_index.py`
- `docs/indexing/indexing_notes.md`
- `docs/indexing/bplus_tree_explanation.md`
- `docs/indexing/hash_index_explanation.md`
- `weeks/week_07_indexing_bplus_tree_hashing/reflection.md`

**Self-Check Questions:**
- What is the difference between B tree and B+ tree?
- Why are B+ trees good for range queries?
- Why are hash indexes bad for range queries?
- What is a clustered index?

---

### **Week 8: Query Optimization + EXPLAIN**

**📂 [Go to Week 8](weeks/week_08_query_optimization/README.md)**

**Learning Objectives:**
- Understand query execution plans
- Use EXPLAIN and EXPLAIN ANALYZE
- Measure query performance before/after indexes
- Understand cost estimation
- Optimize slow queries

**Theory Topics:**
- Query processing pipeline
- Query optimization techniques
- Cost-based optimization
- Sequential scan vs index scan
- Join algorithms (nested loop, hash, merge)
- EXPLAIN output interpretation

**Hands-on Tasks:**
- Generate larger sample dataset (1000+ questions)
- Run EXPLAIN ANALYZE before adding indexes
- Run EXPLAIN ANALYZE after adding indexes
- Benchmark queries:
  - Filter by difficulty
  - Filter by academic_year
  - Join questions/topics
  - Aggregate topic frequency
- Document performance improvements

**Deliverables:**
- `dbms_internals/query_plan/query_plan_demo.sql`
- `dbms_internals/query_plan/README.md`
- `dbms_internals/query_plan/outputs/before_indexes.txt`
- `dbms_internals/query_plan/outputs/after_indexes.txt`
- `docs/indexing/query_plan_analysis.md`
- `weeks/week_08_query_optimization_explain/benchmark_report.md`
- `weeks/week_08_query_optimization_explain/reflection.md`

**Self-Check Questions:**
- What does EXPLAIN show?
- What is the difference between EXPLAIN and EXPLAIN ANALYZE?
- What is a sequential scan?
- How do you know if an index is being used?

---

## 🤖 Month 3: Transactions + AI Search + Portfolio (Weeks 9-12)

### **Week 9: Transactions, ACID, Concurrency**

**📂 [Go to Week 9](weeks/week_09_transactions/README.md)**

**Learning Objectives:**
- Understand transaction concepts and ACID properties
- Implement transaction rollback
- Understand concurrency issues (lost update, dirty read)
- Understand isolation levels
- Implement wait-for graph deadlock detector

**Theory Topics:**
- Transaction states
- ACID properties
- Concurrency problems
- Serializability (conflict, view)
- Lock-based protocols
- Deadlock detection

**Hands-on Tasks:**
- Create transaction demo with COMMIT/ROLLBACK
- Simulate multi-step safe update
- Create wait-for graph deadlock detector in Python
- Document PostgreSQL isolation levels
- Test transaction behavior

**Deliverables:**
- `dbms_internals/transactions/transaction_demo.sql`
- `dbms_internals/transactions/wait_for_graph.py`
- `dbms_internals/transactions/README.md`
- `dbms_internals/transactions/tests/test_transactions.py`
- `docs/transactions/transaction_notes.md`
- `docs/transactions/acid_examples.md`
- `docs/transactions/concurrency_problems.md`
- `weeks/week_09_transactions_concurrency_acid/reflection.md`

**Self-Check Questions:**
- What does ACID stand for?
- What is a dirty read?
- What is serializability?
- How do you detect deadlocks?

---

### **Week 10: Embeddings, pgvector, Semantic Search**

**📂 [Go to Week 10](weeks/week_10_semantic_search/README.md)**

**Learning Objectives:**
- Understand text embeddings
- Learn vector similarity (cosine similarity)
- Set up pgvector extension
- Implement chunking service
- Implement embedding generation
- Implement semantic search
- Compare keyword vs semantic search

**Theory Topics:**
- Text embeddings basics
- Sentence Transformers
- Vector representations
- Cosine similarity
- Top-k retrieval
- pgvector extension
- Why embeddings matter for AI systems

**Hands-on Tasks:**
- Enable pgvector in PostgreSQL
- Add `resource_chunks` and `chunk_embeddings` tables
- Create chunking service
- Create embedding service using Sentence Transformers
- Create semantic search service
- Generate embeddings for sample data
- Implement `GET /search/semantic?q=...&top_k=5`
- Compare keyword search vs semantic search

**Test Queries:**
- "transactions waiting for each other"
- "questions about database design diagrams"
- "normalization with functional dependency"
- "B+ tree insertion problems"

**Deliverables:**
- `app/db/models.py` (updated with chunks, embeddings)
- `app/services/chunking_service.py`
- `app/services/embedding_service.py`
- `app/services/semantic_search_service.py`
- `app/api/search.py`
- `scripts/generate_embeddings.py`
- `docs/semantic_search/semantic_search_report.md`
- `docs/semantic_search/embeddings_explained.md`
- `weeks/week_10_embeddings_semantic_search_pgvector/reflection.md`

**Self-Check Questions:**
- What is an embedding?
- What is cosine similarity?
- Why is semantic search better than keyword search?
- What is pgvector?

---

### **Week 11: Integrated CourseDB-AI System**

**📂 [Go to Week 11](weeks/week_11_frontend_integration/README.md)**

**Learning Objectives:**
- Integrate all modules into a cohesive system
- Build Streamlit UI
- Complete all API endpoints
- Add integration tests
- Document system architecture

**Hands-on Tasks:**
- Complete all FastAPI endpoints:
  - Courses, Topics, Resources, Questions
  - SQL search, Semantic search
  - Analytics, DBMS demos
- Build Streamlit UI with pages:
  - Dashboard
  - Resource Upload
  - SQL Search
  - Semantic Search
  - Analytics
  - DBMS Internals
- Connect Streamlit to FastAPI
- Seed comprehensive dataset
- Add integration tests
- Document system architecture

**Deliverables:**
- `app/frontend/streamlit_app.py`
- `app/api/` (all endpoints complete)
- `docs/architecture/system_architecture.md`
- `docs/architecture/api_documentation.md`
- `app/tests/test_integration.py`
- `data/seed/sample_questions.json`
- `weeks/week_11_integrated_coursedb_ai_system/reflection.md`

**Self-Check Questions:**
- How do all the components work together?
- What is the data flow from UI to database?
- How does the API handle errors?
- Where are embeddings stored?

---

### **Week 12: Evaluation, Polish, Portfolio**

**📂 [Go to Week 12](weeks/week_12_evaluation_portfolio/README.md)**

**Learning Objectives:**
- Evaluate system correctness and performance
- Evaluate semantic search quality
- Polish documentation
- Create portfolio materials
- Prepare demo script

**Evaluation Tasks:**
- SQL correctness check
- Normalization review (3NF/BCNF compliance)
- Constraints/triggers verification
- Query performance evaluation (before/after indexes)
- Transaction rollback behavior test
- Semantic search relevance evaluation

**Semantic Search Evaluation Queries:**
- "questions about deadlock"
- "how to detect transaction cycles"
- "database design diagram questions"
- "normalization with functional dependency"
- "B+ tree insertion problems"
- "SQL join and trigger questions"
- "transaction isolation and lost update"

**For Each Query Record:**
- Top 1 result
- Top 3 results
- Top 5 results
- Manual relevance score (1-5)
- Failure cases

**Portfolio Deliverables:**
- `docs/evaluation/evaluation_report.md`
- `docs/evaluation/semantic_search_evaluation.md`
- `docs/evaluation/performance_benchmarks.md`
- `docs/portfolio/portfolio_case_study.md`
- `docs/portfolio/demo_script.md`
- `docs/portfolio/final_project_summary.md`
- Polished root README.md
- `weeks/week_12_evaluation_polish_portfolio/reflection.md`

**Self-Check Questions:**
- What are the strengths of CourseDB-AI?
- What are the limitations?
- How would you improve semantic search quality?
- How would you scale this system?

---

## 📊 Weekly Rhythm

Each week follows this structure:

| Day | Activity |
|-----|----------|
| **Day 1** | Read theory notes, watch videos, take notes |
| **Day 2** | Complete exercises, answer self-check questions |
| **Day 3-4** | Implement mini-project, write code incrementally |
| **Day 5** | Debug, test, break things intentionally |
| **Day 6** | Document, write reflection, update LEARNING_LOG.md |
| **Day 7** | Review, prepare for next week |

---

## 🎯 Success Criteria

By Week 12, you should be able to:

✅ Explain CourseDB-AI architecture without reading code
✅ Design normalized schemas from scratch
✅ Write complex SQL queries confidently
✅ Explain how B+ trees and hash indexes work
✅ Analyze query plans and optimize queries
✅ Explain ACID properties with examples
✅ Generate embeddings and implement semantic search
✅ Build RESTful APIs with FastAPI
✅ Test database-backed applications
✅ Present CourseDB-AI as a portfolio project

---

## 📚 Additional Resources

- **Database Systems Concepts** by Silberschatz, Korth, Sudarshan
- **PostgreSQL Documentation**: https://www.postgresql.org/docs/
- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **Sentence Transformers Documentation**: https://www.sbert.net/
- **pgvector GitHub**: https://github.com/pgvector/pgvector

---

## 🚀 Next Steps

1. Read this roadmap completely
2. Review AI_USAGE_RULES.md
3. **[🎯 Start Your Journey: Go to START_HERE.md](START_HERE.md)**
4. Commit early and commit often
5. Update LEARNING_LOG.md weekly
6. Ask questions, break things, learn!

---

**Remember**: This is a learning journey, not a race. Prioritize understanding over speed. Document your mistakes. Celebrate small wins. Build something you're proud of.

**Good luck! 🎓🚀**

---

## 🧭 Navigation

**[🚀 Ready to Start? Go to START_HERE](START_HERE.md)** | **[📚 View Learning Path](LEARNING_PATH.md)** | **[🏠 Back to README](README.md)**

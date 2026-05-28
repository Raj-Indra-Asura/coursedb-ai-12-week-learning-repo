# CourseDB-AI: Technical Specification

**Version**: 1.0
**Last Updated**: May 2026
**Status**: In Development

---

## 📋 Executive Summary

**CourseDB-AI** is a hybrid relational database and vector search system designed for semantic retrieval of academic resources. It combines traditional DBMS concepts (normalized schemas, indexing, transactions) with modern AI techniques (embeddings, vector similarity) to enable intelligent search over course materials, previous-year questions, and textbook chapters.

**Primary Goal**: Build a learning-first portfolio project that demonstrates deep understanding of both database systems and AI infrastructure.

---

## 🎯 Problem Definition

### **The Problem**

Students and instructors face challenges when searching for academic resources:

1. **Keyword Mismatch**: Questions about "deadlock" might use terms like "circular wait" or "transaction cycles"
2. **Poor Organization**: Questions scattered across years without topic tagging
3. **Limited Discovery**: Can't find conceptually similar questions (e.g., "all questions about database design")
4. **No Analytics**: Can't identify frequently tested topics or trends over years

### **Current Solutions (Inadequate)**

- **File System**: Questions stored in PDFs/Word docs (no structured search)
- **Spreadsheets**: Manual tagging, no semantic search, no scalability
- **Basic Databases**: Keyword search only, no understanding of meaning

### **Our Solution**

CourseDB-AI provides:
- **Structured Storage**: Normalized relational schema with proper constraints
- **SQL Filtering**: Filter by year, difficulty, topic, resource type
- **Semantic Search**: Find resources by meaning using embeddings
- **Analytics**: Topic frequency, year-wise trends
- **DBMS Internals**: Educational demos of B+ trees, hashing, query plans, transactions

---

## 👥 Target Users

1. **Primary**: Me (2nd-year CS student) - for learning and portfolio
2. **Secondary**: University students studying DBMS
3. **Tertiary**: Instructors organizing academic resources
4. **Future**: AI/ML hiring managers evaluating my portfolio

---

## 📊 Data Types

### **Core Academic Data**

| Data Type | Examples | Storage |
|-----------|----------|---------|
| **Courses** | "Database Management Systems", "DBMS Lab" | Relational table |
| **Topics** | "Normalization", "B+ Trees", "Transactions" | Relational table (hierarchical) |
| **Questions** | Previous-year exam questions | Relational table |
| **Resources** | Notes, textbook chapters, assignments | Relational table |
| **Chapters** | "Chapter 6: Indexing", "Chapter 7: Query Optimization" | Relational table |
| **Tags** | "important", "frequently-asked", "difficult" | Relational table |

### **AI/ML Data**

| Data Type | Description | Storage |
|-----------|-------------|---------|
| **Resource Chunks** | 200-300 word chunks of resources | Relational table |
| **Embeddings** | 384-dimensional vectors | pgvector (vector column) |
| **Search Logs** | User queries for analysis | Relational table |

### **Metadata**

| Data Type | Description | Storage |
|-----------|-------------|---------|
| **Audit Logs** | Question insert/update tracking | Relational table (trigger-populated) |
| **Users** | Basic user info | Relational table |

---

## 🏗️ System Architecture

### **High-Level Architecture**

```
┌─────────────────────────────────────────────────────────────┐
│                       User Interface                         │
│                     (Streamlit / React)                      │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                     FastAPI Backend                          │
├─────────────────────────────────────────────────────────────┤
│  • SQL Search Service                                        │
│  • Semantic Search Service                                   │
│  • Analytics Service                                         │
│  • DBMS Demo Service                                         │
└────────────────────────┬────────────────────────────────────┘
                         │
         ┌───────────────┴───────────────┐
         ▼                               ▼
┌──────────────────────┐       ┌──────────────────────┐
│  PostgreSQL Database │       │  Sentence Transformers│
│     with pgvector    │       │   Embedding Model     │
└──────────────────────┘       └──────────────────────┘
```

### **Technology Stack**

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | Streamlit (v1.x) | Interactive UI prototype |
| **Backend** | FastAPI (v0.104+) | RESTful API |
| **ORM** | SQLAlchemy (v2.x) | Database abstraction |
| **Database** | PostgreSQL 15+ | Relational storage |
| **Vector Extension** | pgvector (v0.5+) | Vector similarity search |
| **Embeddings** | Sentence Transformers | Text to vector conversion |
| **Model** | all-MiniLM-L6-v2 | 384-dim embeddings |
| **Testing** | pytest (v7.x) | Test automation |
| **Containerization** | Docker, docker-compose | Development environment |
| **Migrations** | Alembic | Schema versioning |
| **Visualization** | matplotlib, networkx | DBMS internals visualization |

---

## 🗄️ Database Schema

### **Core Tables**

#### **courses**
```sql
CREATE TABLE courses (
    course_id SERIAL PRIMARY KEY,
    course_code VARCHAR(20) UNIQUE NOT NULL,
    course_title VARCHAR(200) NOT NULL,
    semester VARCHAR(20),
    credit INTEGER CHECK (credit > 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### **topics**
```sql
CREATE TABLE topics (
    topic_id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES courses(course_id),
    parent_topic_id INTEGER REFERENCES topics(topic_id),
    topic_name VARCHAR(200) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### **resources**
```sql
CREATE TABLE resources (
    resource_id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES courses(course_id),
    title VARCHAR(300) NOT NULL,
    resource_type VARCHAR(50) CHECK (resource_type IN ('notes', 'question_paper', 'textbook', 'assignment', 'slides')),
    source_name VARCHAR(200),
    academic_year VARCHAR(20),
    file_path VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### **questions**
```sql
CREATE TABLE questions (
    question_id SERIAL PRIMARY KEY,
    resource_id INTEGER REFERENCES resources(resource_id),
    question_text TEXT NOT NULL,
    marks INTEGER CHECK (marks > 0),
    difficulty VARCHAR(20) CHECK (difficulty IN ('easy', 'medium', 'hard')),
    question_type VARCHAR(50) CHECK (question_type IN ('mcq', 'short', 'long', 'problem')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### **question_topics** (M:N relationship)
```sql
CREATE TABLE question_topics (
    question_id INTEGER REFERENCES questions(question_id) ON DELETE CASCADE,
    topic_id INTEGER REFERENCES topics(topic_id) ON DELETE CASCADE,
    PRIMARY KEY (question_id, topic_id)
);
```

### **Metadata Tables**

#### **chapters**
```sql
CREATE TABLE chapters (
    chapter_id SERIAL PRIMARY KEY,
    book_name VARCHAR(300) NOT NULL,
    chapter_no INTEGER CHECK (chapter_no > 0),
    chapter_title VARCHAR(300) NOT NULL,
    UNIQUE (book_name, chapter_no)
);
```

#### **tags**
```sql
CREATE TABLE tags (
    tag_id SERIAL PRIMARY KEY,
    tag_name VARCHAR(100) UNIQUE NOT NULL
);
```

#### **resource_tags** (M:N relationship)
```sql
CREATE TABLE resource_tags (
    resource_id INTEGER REFERENCES resources(resource_id) ON DELETE CASCADE,
    tag_id INTEGER REFERENCES tags(tag_id) ON DELETE CASCADE,
    PRIMARY KEY (resource_id, tag_id)
);
```

### **AI/ML Tables**

#### **resource_chunks**
```sql
CREATE TABLE resource_chunks (
    chunk_id SERIAL PRIMARY KEY,
    resource_id INTEGER REFERENCES resources(resource_id) ON DELETE CASCADE,
    chunk_text TEXT NOT NULL,
    chunk_order INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### **chunk_embeddings**
```sql
CREATE TABLE chunk_embeddings (
    embedding_id SERIAL PRIMARY KEY,
    chunk_id INTEGER REFERENCES resource_chunks(chunk_id) ON DELETE CASCADE,
    embedding VECTOR(384) NOT NULL, -- pgvector extension
    model_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Vector similarity index
CREATE INDEX idx_chunk_embeddings_vector ON chunk_embeddings USING ivfflat (embedding vector_cosine_ops);
```

### **Audit & Logging Tables**

#### **users**
```sql
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    role VARCHAR(50) CHECK (role IN ('student', 'instructor', 'admin')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### **search_logs**
```sql
CREATE TABLE search_logs (
    log_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    query_text TEXT NOT NULL,
    search_type VARCHAR(50) CHECK (search_type IN ('sql', 'semantic')),
    results_count INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### **audit_logs**
```sql
CREATE TABLE audit_logs (
    audit_id SERIAL PRIMARY KEY,
    action_type VARCHAR(50) CHECK (action_type IN ('INSERT', 'UPDATE', 'DELETE')),
    table_name VARCHAR(100) NOT NULL,
    record_id INTEGER NOT NULL,
    old_data JSONB,
    new_data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### **Triggers**

#### **Audit Trigger for Questions**
```sql
CREATE OR REPLACE FUNCTION audit_question_changes()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO audit_logs (action_type, table_name, record_id, new_data)
        VALUES ('INSERT', 'questions', NEW.question_id, row_to_json(NEW));
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO audit_logs (action_type, table_name, record_id, old_data, new_data)
        VALUES ('UPDATE', 'questions', NEW.question_id, row_to_json(OLD), row_to_json(NEW));
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_audit_questions
AFTER INSERT OR UPDATE ON questions
FOR EACH ROW EXECUTE FUNCTION audit_question_changes();
```

### **Views**

#### **topic_question_frequency**
```sql
CREATE VIEW topic_question_frequency AS
SELECT
    t.topic_name,
    COUNT(qt.question_id) AS question_count
FROM topics t
LEFT JOIN question_topics qt ON t.topic_id = qt.topic_id
GROUP BY t.topic_id, t.topic_name
ORDER BY question_count DESC;
```

#### **year_wise_topic_frequency**
```sql
CREATE VIEW year_wise_topic_frequency AS
SELECT
    r.academic_year,
    t.topic_name,
    COUNT(q.question_id) AS question_count
FROM resources r
JOIN questions q ON r.resource_id = q.resource_id
JOIN question_topics qt ON q.question_id = qt.question_id
JOIN topics t ON qt.topic_id = t.topic_id
WHERE r.academic_year IS NOT NULL
GROUP BY r.academic_year, t.topic_name
ORDER BY r.academic_year DESC, question_count DESC;
```

---

## 🔍 Core Features

### **1. SQL-Based Search**

**Endpoint**: `GET /search/sql`

**Query Parameters**:
- `topic`: Filter by topic name (partial match)
- `difficulty`: Filter by difficulty (easy, medium, hard)
- `year`: Filter by academic year
- `question_type`: Filter by question type
- `marks_min`, `marks_max`: Filter by marks range

**Example**:
```
GET /search/sql?topic=normalization&difficulty=medium&year=2023
```

### **2. Semantic Search**

**Endpoint**: `GET /search/semantic`

**Query Parameters**:
- `q`: Natural language query
- `top_k`: Number of results (default: 5)

**Algorithm**:
1. Generate embedding for query using Sentence Transformers
2. Use pgvector cosine similarity to find nearest chunks
3. Return top-k results with similarity scores

**Example**:
```
GET /search/semantic?q=questions about deadlock detection&top_k=5
```

**SQL Query**:
```sql
SELECT
    c.chunk_text,
    r.title,
    1 - (e.embedding <=> $1) AS similarity
FROM chunk_embeddings e
JOIN resource_chunks c ON e.chunk_id = c.chunk_id
JOIN resources r ON c.resource_id = r.resource_id
ORDER BY e.embedding <=> $1
LIMIT $2;
```

### **3. Analytics**

**Endpoints**:
- `GET /analytics/topic-frequency`: Topic distribution
- `GET /analytics/year-wise-trends`: Year-wise topic trends
- `GET /analytics/difficulty-distribution`: Question difficulty breakdown

### **4. DBMS Internals Demos**

#### **B+ Tree Visualizer**
- Insert keys: 10, 20, 5, 6, 12, 30, 7
- Visualize node splits
- Show search path

#### **Hash Index Simulator**
- Demonstrate key % bucket_count
- Show collision handling
- Compare with B+ tree for range queries

#### **Query Plan Analyzer**
- Run EXPLAIN ANALYZE before/after indexes
- Show cost differences
- Visualize execution plans

#### **Transaction Demo**
- Demonstrate COMMIT/ROLLBACK
- Show ACID properties
- Simulate concurrent transactions

#### **Wait-for Graph**
- Detect deadlocks from transaction logs
- Visualize wait-for graph
- Identify cycles

---

## 🚫 Non-Goals (Out of Scope)

❌ Build a full DBMS engine from scratch
❌ Implement a SQL parser
❌ Implement a query compiler
❌ Implement a storage engine
❌ Implement distributed databases
❌ Production-scale deployment
❌ Full authentication system (OAuth, JWT)
❌ RAG pipeline with LLM (future work)
❌ Real-time collaboration
❌ Mobile app
❌ Multilingual support

---

## 📈 Evaluation Plan

### **SQL Correctness**
- Verify all queries return correct results
- Test constraints enforcement
- Test trigger behavior

### **Normalization Quality**
- Verify 3NF/BCNF compliance
- Check for anomalies

### **Query Performance**
- Benchmark queries before/after indexes
- Document performance improvements

### **Semantic Search Quality**
- Manual evaluation on 20+ queries
- Record top-1, top-3, top-5 results
- Calculate relevance scores (1-5 scale)

### **Comparison: Keyword vs Semantic**
- Run same queries with both methods
- Compare result quality
- Document cases where semantic search wins

---

## 🎯 Success Criteria

✅ **Database**: Normalized schema in 3NF/BCNF
✅ **Constraints**: All PK, FK, CHECK constraints working
✅ **Triggers**: Audit trigger logs all question changes
✅ **Indexes**: B+ tree indexes improve query performance
✅ **Semantic Search**: Finds relevant results for 80%+ of test queries
✅ **API**: All endpoints return correct responses
✅ **Tests**: 80%+ test coverage
✅ **Documentation**: Complete docs for all modules
✅ **Portfolio**: Professional case study and demo script

---

## 🚀 Future Improvements

### **Phase 2: Advanced Search**
- Hybrid search (SQL + semantic combined)
- Reranking with cross-encoders
- Query expansion

### **Phase 3: Topic Classification**
- Train TF-IDF + Logistic Regression classifier
- Auto-tag questions with topics

### **Phase 4: RAG Pipeline**
- Integrate LLM (GPT-4, Claude, Llama)
- Answer questions using retrieved context

### **Phase 5: Production Deployment**
- Add authentication (JWT)
- Deploy to cloud (AWS, GCP, Azure)
- Add monitoring (Prometheus, Grafana)
- Implement caching (Redis)

### **Phase 6: React Frontend**
- Build modern web UI
- Add collaborative features
- Add real-time updates

---

## 📚 References

- **Database Systems Concepts** (Silberschatz, Korth, Sudarshan)
- **PostgreSQL Documentation**: https://www.postgresql.org/docs/
- **pgvector GitHub**: https://github.com/pgvector/pgvector
- **Sentence Transformers**: https://www.sbert.net/
- **FastAPI Documentation**: https://fastapi.tiangolo.com/

---

## 📝 Change Log

| Date | Version | Changes |
|------|---------|---------|
| 2026-05-28 | 1.0 | Initial specification |

---

## 🤝 Contributing

This is a personal learning project. Not accepting external contributions, but feedback welcome!

---

**Author**: Raj Indra Asura
**Repository**: [coursedb-ai-12-week-learning-repo](https://github.com/Raj-Indra-Asura/coursedb-ai-12-week-learning-repo)

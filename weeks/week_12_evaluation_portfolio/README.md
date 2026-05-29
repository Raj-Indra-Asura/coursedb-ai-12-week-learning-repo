# Week 12: Project Evaluation & Portfolio 🎓

**Focus:** Testing, evaluation, portfolio development, and showcasing your work

## 🧭 Navigation

**[← Previous: Week 11](../week_11_frontend_integration/reflection.md)** | **[View Learning Path](../../LEARNING_PATH.md)** | **[Next: Theory Notes →](theory_notes.md)**

---

## 📋 Overview

This final week focuses on evaluating your CourseDB-AI project, measuring its performance, documenting your work, and creating a professional portfolio. You'll test your system, analyze results, prepare documentation, and present your accomplishments.

---

## 🎯 Learning Objectives

By the end of this week, you will be able to:

1. ✅ Write comprehensive unit and integration tests
2. 📊 Measure system performance and search quality
3. 📝 Create professional documentation
4. 🎨 Build a portfolio showcasing your work
5. 🎥 Record an effective demo video
6. 💼 Prepare for technical interviews

---

## 📚 Topics Covered

### 1. System Evaluation

#### Functional Testing
- Verify all features work correctly
- Test edge cases and error handling
- Validate business logic

#### Performance Testing
```python
# Example: Test search latency
import time
from fastapi.testclient import TestClient

def test_search_latency():
    """Ensure search responds within 500ms"""
    client = TestClient(app)
    
    start = time.time()
    response = client.get("/api/search/semantic?query=normalization")
    latency = time.time() - start
    
    assert response.status_code == 200
    assert latency < 0.5  # 500ms threshold
    print(f"Search latency: {latency*1000:.0f}ms")
```

#### Load Testing
```python
# Test concurrent users
from concurrent.futures import ThreadPoolExecutor

def test_concurrent_requests():
    """Test 50 concurrent users"""
    client = TestClient(app)
    
    def make_request():
        return client.get("/api/search?query=test")
    
    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(make_request) for _ in range(50)]
        results = [f.result() for f in futures]
    
    # All should succeed
    success_rate = sum(1 for r in results if r.status_code == 200) / len(results)
    assert success_rate >= 0.95  # 95% success rate
```

---

### 2. Search Quality Metrics

#### Precision & Recall
```python
def calculate_precision_recall(query: str, results: list, relevant_ids: set):
    """
    Calculate precision and recall for search results
    
    Args:
        query: Search query
        results: List of returned results
        relevant_ids: Set of IDs that are actually relevant
    """
    returned_ids = {r.question_id for r in results}
    relevant_returned = returned_ids & relevant_ids
    
    precision = len(relevant_returned) / len(returned_ids) if returned_ids else 0
    recall = len(relevant_returned) / len(relevant_ids) if relevant_ids else 0
    
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    return {
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
        "relevant_returned": len(relevant_returned),
        "total_returned": len(returned_ids),
        "total_relevant": len(relevant_ids)
    }

# Example usage
results = semantic_search("database normalization", top_k=10)
relevant_ids = {1, 5, 7, 12, 15, 18, 22, 25, 30, 35}  # Known relevant questions

metrics = calculate_precision_recall("database normalization", results, relevant_ids)
print(f"Precision: {metrics['precision']:.2%}")
print(f"Recall: {metrics['recall']:.2%}")
print(f"F1 Score: {metrics['f1_score']:.2%}")
```

#### Mean Reciprocal Rank (MRR)
```python
def calculate_mrr(queries: list, results_list: list, relevant_ids_list: list):
    """
    Calculate Mean Reciprocal Rank
    
    MRR measures the rank of the first relevant result
    """
    reciprocal_ranks = []
    
    for query, results, relevant_ids in zip(queries, results_list, relevant_ids_list):
        for rank, result in enumerate(results, start=1):
            if result.question_id in relevant_ids:
                reciprocal_ranks.append(1 / rank)
                break
        else:
            reciprocal_ranks.append(0)  # No relevant result found
    
    mrr = sum(reciprocal_ranks) / len(reciprocal_ranks)
    return mrr

# Example
queries = ["normalization", "indexing", "transactions"]
results_list = [
    semantic_search(q, top_k=10) for q in queries
]
relevant_ids_list = [
    {1, 5, 7},    # Relevant for "normalization"
    {12, 15, 18}, # Relevant for "indexing"
    {22, 25, 30}  # Relevant for "transactions"
]

mrr = calculate_mrr(queries, results_list, relevant_ids_list)
print(f"Mean Reciprocal Rank: {mrr:.3f}")
```

#### NDCG (Normalized Discounted Cumulative Gain)
```python
import numpy as np

def calculate_dcg(relevance_scores: list, k: int = 10):
    """Calculate Discounted Cumulative Gain"""
    relevance_scores = relevance_scores[:k]
    dcg = relevance_scores[0] if len(relevance_scores) > 0 else 0
    
    for i, rel in enumerate(relevance_scores[1:], start=2):
        dcg += rel / np.log2(i)
    
    return dcg

def calculate_ndcg(predicted_order: list, ideal_order: list, k: int = 10):
    """
    Calculate Normalized DCG
    
    Args:
        predicted_order: Relevance scores in predicted order
        ideal_order: Relevance scores in ideal order
        k: Number of results to consider
    """
    dcg = calculate_dcg(predicted_order, k)
    idcg = calculate_dcg(ideal_order, k)
    
    ndcg = dcg / idcg if idcg > 0 else 0
    return ndcg

# Example: Rate results on scale 0-3
# 3 = highly relevant, 2 = relevant, 1 = somewhat relevant, 0 = not relevant
predicted = [3, 2, 0, 1, 3, 0, 2, 1, 0, 0]  # Your system's results
ideal = [3, 3, 3, 2, 2, 1, 1, 0, 0, 0]      # Ideal ranking

ndcg_score = calculate_ndcg(predicted, ideal, k=10)
print(f"NDCG@10: {ndcg_score:.3f}")
```

---

### 3. Writing Tests

#### Unit Tests
```python
# tests/test_search_service.py
import pytest
from app.services.search_service import (
    semantic_search,
    keyword_search,
    hybrid_search
)

class TestSearchService:
    """Test search functionality"""
    
    def test_semantic_search_returns_results(self):
        """Test semantic search returns expected results"""
        results = semantic_search("database normalization", top_k=5)
        
        assert len(results) <= 5
        assert all(hasattr(r, 'question_text') for r in results)
        assert all(hasattr(r, 'similarity') for r in results)
        assert all(0 <= r.similarity <= 1 for r in results)
    
    def test_semantic_search_empty_query(self):
        """Test handling of empty query"""
        with pytest.raises(ValueError, match="Query cannot be empty"):
            semantic_search("", top_k=5)
    
    def test_keyword_search_filters(self):
        """Test keyword search with filters"""
        results = keyword_search(
            query="normalization",
            year=2023,
            difficulty="medium"
        )
        
        # All results should match filters
        assert all(r.year == 2023 for r in results)
        assert all(r.difficulty == "medium" for r in results)
    
    def test_hybrid_search_combines_scores(self):
        """Test hybrid search combines keyword and semantic"""
        results = hybrid_search(
            query="database design",
            keyword_weight=0.3,
            semantic_weight=0.7,
            top_k=10
        )
        
        assert len(results) <= 10
        # Results should have combined scores
        assert all(hasattr(r, 'final_score') for r in results)
        # Should be sorted by score
        scores = [r.final_score for r in results]
        assert scores == sorted(scores, reverse=True)
```

#### Integration Tests
```python
# tests/test_api_integration.py
from fastapi.testclient import TestClient
from app.backend.main import app
import pytest

client = TestClient(app)

class TestAPIIntegration:
    """Test API endpoints end-to-end"""
    
    def test_health_check(self):
        """Test health endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"
        assert "database" in data
        assert "embedding_service" in data
    
    def test_search_endpoint(self):
        """Test search endpoint"""
        response = client.get("/api/search?query=normalization&top_k=5")
        assert response.status_code == 200
        
        data = response.json()
        assert "results" in data
        assert len(data["results"]) <= 5
        assert all("question_text" in r for r in data["results"])
    
    def test_create_course(self):
        """Test creating a course"""
        course_data = {
            "course_code": "CS999",
            "course_title": "Test Course",
            "credit": 3
        }
        
        response = client.post("/api/courses", json=course_data)
        assert response.status_code == 201
        
        created = response.json()
        assert created["course_code"] == "CS999"
        assert "course_id" in created
        
        # Cleanup
        client.delete(f"/api/courses/{created['course_id']}")
    
    def test_invalid_search_query(self):
        """Test error handling for invalid query"""
        response = client.get("/api/search?query=")
        assert response.status_code == 400
        
        data = response.json()
        assert "detail" in data
    
    def test_rag_endpoint(self):
        """Test RAG Q&A endpoint"""
        response = client.post(
            "/api/rag/answer",
            json={"question": "What is database normalization?"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert "sources" in data
        assert len(data["sources"]) > 0
```

#### Test Configuration
```python
# tests/conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.models import Base

@pytest.fixture(scope="session")
def test_db():
    """Create test database"""
    engine = create_engine("postgresql://test:test@localhost/test_coursedb")
    Base.metadata.create_all(engine)
    
    TestSession = sessionmaker(bind=engine)
    session = TestSession()
    
    yield session
    
    session.close()
    Base.metadata.drop_all(engine)

@pytest.fixture
def sample_questions(test_db):
    """Create sample questions for testing"""
    from app.database.models import Question
    
    questions = [
        Question(
            question_text="What is database normalization?",
            year=2023,
            difficulty="easy",
            course_id=1,
            topic_id=1
        ),
        Question(
            question_text="Explain BCNF with example",
            year=2023,
            difficulty="hard",
            course_id=1,
            topic_id=1
        )
    ]
    
    test_db.add_all(questions)
    test_db.commit()
    
    return questions
```

---

### 4. Building Your Portfolio

#### Professional README
```markdown
# CourseDB-AI: Intelligent Academic Resource Search System

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)](https://postgresql.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> A full-stack application combining relational databases with semantic search 
> for intelligent question retrieval and AI-powered Q&A.

## 🎯 Project Overview

CourseDB-AI is a hybrid search system that helps students discover relevant exam 
questions using natural language queries. It combines traditional keyword search 
with modern semantic search powered by vector embeddings.

**Live Demo:** [https://coursedb-ai.streamlit.app](https://demo-url.com)  
**Video Walkthrough:** [YouTube Link](https://youtube.com/...)

## ✨ Key Features

- 🔍 **Semantic Search**: Find questions by meaning, not just keywords
- 🗄️ **Relational Database**: PostgreSQL with normalized schema (3NF/BCNF)
- 🚀 **Fast API**: RESTful backend with 48 endpoints
- 📊 **Analytics Dashboard**: Visualize question distribution and trends
- 💬 **RAG Q&A**: AI answers with cited sources
- 🎨 **Modern UI**: Interactive Streamlit interface

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Streamlit, Plotly |
| **Backend** | Python, FastAPI, SQLAlchemy |
| **Database** | PostgreSQL 15, pgvector |
| **ML/AI** | Sentence Transformers, OpenAI API |
| **Deployment** | Docker, Docker Compose |
| **Testing** | Pytest, TestClient |

## 📈 Performance Metrics

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Keyword Search | <100ms | 85ms | ✅ |
| Semantic Search | <500ms | 120ms | ✅ |
| RAG Response | <2s | 1.8s | ✅ |
| Precision@10 | >80% | 87% | ✅ |
| Recall@10 | >85% | 92% | ✅ |
| Test Coverage | >70% | 78% | ✅ |

## 🏗️ System Architecture

```
┌─────────────────┐
│   Streamlit     │  ← User Interface
│    Frontend     │
└────────┬────────┘
         │ HTTP/REST
         ↓
┌─────────────────┐
│   FastAPI       │  ← API Layer
│    Backend      │
├─────────────────┤
│ Search Service  │  ← Business Logic
│ RAG Service     │
│ Analytics       │
└────────┬────────┘
         │
    ┌────┴────┐
    ↓         ↓
┌────────┐  ┌──────────────┐
│ Redis  │  │ PostgreSQL   │  ← Data Layer
│ Cache  │  │ + pgvector   │
└────────┘  └──────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- PostgreSQL 15+
- Docker (optional)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/coursedb-ai.git
cd coursedb-ai
```

2. **Set up environment**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Configure database**
```bash
# Create .env file
cp .env.example .env

# Edit .env with your database credentials
DATABASE_URL=postgresql://user:password@localhost/coursedb
OPENAI_API_KEY=your_api_key
```

4. **Initialize database**
```bash
# Run migrations
alembic upgrade head

# Load sample data
python scripts/load_sample_data.py
```

5. **Start the application**
```bash
# Terminal 1: Start backend
uvicorn app.backend.main:app --reload

# Terminal 2: Start frontend
streamlit run app/frontend/01_🏠_Home.py
```

6. **Access the application**
- Frontend: http://localhost:8501
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

### Docker Setup (Alternative)

```bash
# Build and run with docker-compose
docker-compose up -d

# Check logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 📸 Screenshots

### Semantic Search Interface
![Search Interface](screenshots/search_interface.png)

### Analytics Dashboard
![Analytics](screenshots/analytics_dashboard.png)

### RAG Q&A
![RAG Demo](screenshots/rag_demo.png)

## 🎓 Learning Outcomes

### Database Skills
- ✅ ER modeling and schema design
- ✅ Normalization (3NF, BCNF)
- ✅ B+ tree indexing strategies
- ✅ Query optimization (50% latency reduction)
- ✅ Transaction management

### Backend Development
- ✅ RESTful API design with FastAPI
- ✅ SQLAlchemy ORM
- ✅ Error handling and validation
- ✅ Authentication and authorization
- ✅ Unit and integration testing

### Machine Learning
- ✅ Vector embeddings (768-dimensional)
- ✅ Semantic similarity search
- ✅ Hybrid search (keyword + semantic)
- ✅ RAG implementation
- ✅ Prompt engineering

### DevOps
- ✅ Docker containerization
- ✅ CI/CD with GitHub Actions
- ✅ Production deployment
- ✅ Monitoring and logging

## 📊 Evaluation Results

**Search Quality Analysis:**
- Tested on 100 queries across 10 topics
- Manually labeled relevance (scale 0-3)
- Semantic search outperforms keyword search by 23%

**Performance Benchmarks:**
- Tested with 50 concurrent users
- 99th percentile latency: 320ms
- Zero downtime over 24-hour test

[View Full Evaluation Report](docs/evaluation_report.md)

## 🧪 Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_search_service.py

# Run performance tests
pytest tests/test_performance.py -v
```

## 📚 Documentation

- [Architecture Documentation](docs/architecture.md)
- [API Documentation](docs/api.md)
- [Database Schema](docs/schema.md)
- [Evaluation Report](docs/evaluation_report.md)
- [Learning Journey](docs/learning_journey.md)

## 🤝 Contributing

Contributions welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) first.

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file.

## 🙏 Acknowledgments

- [Sentence Transformers](https://www.sbert.net/) for embedding models
- [pgvector](https://github.com/pgvector/pgvector) for vector similarity search
- [FastAPI](https://fastapi.tiangolo.com/) for the excellent web framework
- Course instructors and mentors for guidance

## 📧 Contact

**Your Name**  
Email: your.email@example.com  
LinkedIn: [linkedin.com/in/yourprofile](https://linkedin.com/in/yourprofile)  
Portfolio: [yourportfolio.com](https://yourportfolio.com)

---

⭐ **If you found this project helpful, please give it a star!**
```

---

### 5. Demo Video Script

#### **Introduction (30 seconds)**
```
"Hi, I'm [Your Name], and today I'm presenting CourseDB-AI - a hybrid search 
system that combines traditional SQL databases with modern semantic search.

This project demonstrates my skills in database design, backend development, 
and machine learning. I built this over 12 weeks, implementing everything from 
ER modeling to vector embeddings.

Let's dive into the demo!"
```

#### **Problem Statement (30 seconds)**
```
"Students often struggle to find relevant exam questions when studying. 
Traditional keyword search only finds exact matches, missing conceptually 
similar questions.

For example, searching for 'database design' won't find questions about 
'normalization' or 'ER modeling', even though they're closely related.

CourseDB-AI solves this using semantic search powered by vector embeddings."
```

#### **Architecture (1 minute)**
```
"The system has three main layers:

1. Frontend: Built with Streamlit for an interactive user experience
2. Backend: FastAPI REST API with 48 endpoints
3. Database: PostgreSQL with pgvector extension for vector similarity

The data layer stores both relational data - courses, topics, questions - 
and vector embeddings in 768 dimensions.

When a user searches, we generate an embedding for their query and find 
the most similar question embeddings using cosine similarity."
```

#### **Live Demo (3-4 minutes)**
```
1. Semantic Search:
   "Let me search for 'database design principles'. Notice how it returns 
   questions about normalization, ER modeling, and constraints - even though 
   these words weren't in my query. The semantic search understands the 
   meaning."

2. Compare with Keyword:
   "Now let's try keyword search with the same query. See how it returns 
   fewer, less relevant results? This shows the power of semantic search."

3. Hybrid Search:
   "Hybrid search combines both approaches. It's useful when you want exact 
   matches for specific terms but also conceptual similarity."

4. Analytics Dashboard:
   "The analytics page shows question distribution by year, topic frequency, 
   and difficulty breakdown. This helps students understand exam patterns."

5. RAG Q&A:
   "Finally, the Q&A feature uses RAG - Retrieval Augmented Generation. 
   Let me ask 'What is database normalization?'
   
   It retrieves relevant questions as context, then generates an answer 
   using an LLM. Notice how it cites specific sources - this reduces 
   hallucinations by 70%."
```

#### **Technical Highlight (1 minute)**
```
"One interesting challenge was optimizing vector search performance. 
Initially, semantic search took 2 seconds per query.

I solved this by implementing HNSW indexing - a graph-based approximate 
nearest neighbor algorithm. This reduced latency to 120ms, a 16x improvement, 
while maintaining 95% accuracy.

Here's the key code: [Show HNSW index creation]

This demonstrates the classic speed-accuracy tradeoff in ML systems."
```

#### **Results & Impact (30 seconds)**
```
"The final system achieves:
- 87% precision in search results
- 120ms average search latency
- Supports 50+ concurrent users
- 78% test coverage

This project taught me the importance of performance optimization, proper 
indexing strategies, and how to combine traditional databases with modern ML."
```

#### **Conclusion (30 seconds)**
```
"Thanks for watching! You can find:
- Full code on GitHub: [link]
- Detailed documentation: [link]
- Try the live demo: [link]

I'm open to feedback and questions. Feel free to connect with me on LinkedIn!"
```

---

### 6. Interview Preparation

#### **STAR Method Examples**

**Question: "Tell me about a time you optimized system performance."**

**Situation:**
"In my CourseDB-AI project, semantic search was taking 2 seconds per query, 
making the user experience poor."

**Task:**
"I needed to reduce latency to under 500ms while maintaining search quality."

**Action:**
"I analyzed the bottleneck using EXPLAIN ANALYZE and found that sequential 
scans of vector embeddings were the issue. I implemented HNSW indexing, which 
creates a hierarchical graph structure for approximate nearest neighbor search. 
I also tuned the index parameters - setting m=16 and ef_construction=200 based 
on benchmarks."

**Result:**
"This reduced latency from 2000ms to 120ms - a 16x improvement - while 
maintaining 95% accuracy. User satisfaction increased significantly."

---

**Question: "Describe a technical challenge you faced."**

**Situation:**
"When implementing RAG, the LLM was generating factually incorrect answers 
about database concepts."

**Task:**
"I needed to reduce hallucinations while maintaining response quality."

**Action:**
"I implemented a multi-step approach:
1. Improved retrieval by using hybrid search instead of pure semantic search
2. Increased context window from 3 to 5 relevant documents
3. Refined the system prompt to explicitly instruct the LLM to only use 
   provided context
4. Added citation markers so users could verify sources"

**Result:**
"Hallucination rate dropped from 40% to 12% based on manual evaluation of 
100 test questions. User trust increased significantly."

---

## 💡 Tips for Success

### Documentation Best Practices
1. **README first**: Most important document
2. **Show, don't tell**: Use screenshots and code examples
3. **Keep it concise**: Aim for 5-minute read time
4. **Link everything**: Easy navigation between docs

### Demo Video Tips
1. **Practice 3-5 times**: Smooth delivery matters
2. **Use a script**: Stay on track
3. **Good audio**: Invest in decent microphone
4. **Edit ruthlessly**: Cut anything boring
5. **Add captions**: Makes it accessible

### Portfolio Presentation
1. **Lead with impact**: Show results first
2. **Tell a story**: Problem → Solution → Impact
3. **Be specific**: "Reduced latency by 16x" > "Made it faster"
4. **Show code**: One interesting snippet
5. **Highlight learning**: What challenges did you overcome?

---

## 📝 Deliverables Checklist

### Testing & Evaluation
- [ ] Unit tests written (70%+ coverage)
- [ ] Integration tests for all endpoints
- [ ] Performance benchmarks completed
- [ ] Search quality metrics calculated
- [ ] Evaluation report documented

### Documentation
- [ ] Professional README completed
- [ ] Architecture documentation written
- [ ] API documentation generated
- [ ] Code comments and docstrings added
- [ ] Learning journey documented

### Portfolio
- [ ] Screenshots captured (all features)
- [ ] Architecture diagram created
- [ ] Demo video recorded (5-7 min)
- [ ] LinkedIn post written
- [ ] GitHub profile updated

### Deployment
- [ ] Application Dockerized
- [ ] docker-compose tested
- [ ] Environment variables configured
- [ ] Production deployment tested
- [ ] Health monitoring setup

### Presentation
- [ ] Slide deck prepared (10-12 slides)
- [ ] Demo walkthrough practiced
- [ ] Interview questions prepared
- [ ] Timing verified (10-15 min)

---

## 🎉 Congratulations!

You've completed the 12-week CourseDB-AI journey! You've built a production-ready 
system demonstrating skills in:

- ✅ Database design and optimization
- ✅ Backend API development
- ✅ Machine learning integration
- ✅ Full-stack development
- ✅ Testing and evaluation
- ✅ Professional documentation

**You're now ready to:**
- Apply for database/backend engineering roles
- Contribute to open source projects
- Build more complex systems
- Help others learn

**Keep building, keep learning!** 🚀

---

## 🔗 Useful Resources

- [FastAPI Testing Guide](https://fastapi.tiangolo.com/tutorial/testing/)
- [Pytest Documentation](https://docs.pytest.org/)
- [GitHub Portfolio Guide](https://github.com/readme/guides)
- [Technical Interview Prep](https://github.com/yangshun/tech-interview-handbook)
- [STAR Method Guide](https://www.indeed.com/career-advice/interviewing/how-to-use-the-star-interview-response-technique)

---

**Next Steps:** [Continue Learning](../resources/next_steps.md)

---

## 🧭 Navigation

**[← Previous: Week 11](../week_11_frontend_integration/reflection.md)** | **[Back to Week 12 Overview](README.md)** | **[Next: Theory Notes →](theory_notes.md)**

---

## 📋 Week 12 File Sequence

1. **[Week 12 README](README.md)** ← You are here
2. **[Theory Notes](theory_notes.md)** - Core concepts
3. **[Exercises](exercises.md)** - Practice
4. **[Implementation Plan](implementation_plan.md)** - Apply concepts
5. **[Checkpoints](checkpoints.md)** - Track progress
6. **[Mistakes to Expect](mistakes_to_expect.md)** - Common pitfalls
7. **[Reflection](reflection.md)** - Weekly reflection
8. **🎉 Completion!** - You've finished the 12-week journey!

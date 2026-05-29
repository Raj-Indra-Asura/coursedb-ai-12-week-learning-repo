# Week 12: Evaluation & Portfolio - Exercises 🧪

Complete these exercises to evaluate your CourseDB-AI system and build your portfolio.

---

## Exercise Set 1: Unit Testing

### Exercise 1.1: Search Service Tests
Write comprehensive unit tests for your search service.

```python
# tests/test_search_service.py
import pytest
from app.services.search_service import semantic_search, keyword_search

class TestSemanticSearch:
    """Test semantic search functionality"""
    
    def test_returns_correct_number_of_results(self):
        """Test top_k parameter works correctly"""
        # TODO: Implement test
        pass
    
    def test_similarity_scores_in_range(self):
        """Test all similarity scores are between 0 and 1"""
        # TODO: Implement test
        pass
    
    def test_empty_query_raises_error(self):
        """Test empty query raises ValueError"""
        # TODO: Implement test
        pass
    
    def test_results_sorted_by_similarity(self):
        """Test results are sorted in descending order"""
        # TODO: Implement test
        pass

class TestKeywordSearch:
    """Test keyword search functionality"""
    
    def test_filters_by_year(self):
        """Test year filter works correctly"""
        # TODO: Implement test
        pass
    
    def test_filters_by_difficulty(self):
        """Test difficulty filter works correctly"""
        # TODO: Implement test
        pass
```

**Tasks:**
1. Implement all test methods
2. Run tests and ensure they pass
3. Achieve >80% coverage for search_service.py

---

### Exercise 1.2: Database Model Tests
Test your database models and relationships.

```python
# tests/test_models.py
import pytest
from app.database.models import Course, Topic, Question

class TestCourseModel:
    """Test Course model"""
    
    def test_create_course(self, test_db):
        """Test creating a course"""
        course = Course(
            course_code="CS999",
            course_title="Test Course",
            credit=3
        )
        test_db.add(course)
        test_db.commit()
        
        assert course.course_id is not None
        assert course.course_code == "CS999"
    
    def test_course_topics_relationship(self, test_db):
        """Test course has topics relationship"""
        # TODO: Create course with topics
        # TODO: Verify relationship works
        pass

class TestQuestionModel:
    """Test Question model"""
    
    def test_question_requires_course(self, test_db):
        """Test question requires valid course_id"""
        # TODO: Try creating question without course
        # TODO: Should raise IntegrityError
        pass
```

**Tasks:**
1. Complete all test cases
2. Test cascade deletes
3. Test constraint violations

---

## Exercise Set 2: Integration Testing

### Exercise 2.1: API Endpoint Tests
Test all major API endpoints.

```python
# tests/test_api.py
from fastapi.testclient import TestClient
from app.backend.main import app

client = TestClient(app)

class TestSearchEndpoints:
    """Test search API endpoints"""
    
    def test_semantic_search_endpoint(self):
        """Test /api/search/semantic endpoint"""
        response = client.get(
            "/api/search/semantic",
            params={"query": "normalization", "top_k": 5}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # TODO: Add more assertions
        # - Check response structure
        # - Verify result count
        # - Validate similarity scores
    
    def test_search_with_filters(self):
        """Test search with year and difficulty filters"""
        # TODO: Implement test
        pass
    
    def test_invalid_query_returns_400(self):
        """Test empty query returns 400 error"""
        # TODO: Implement test
        pass

class TestCRUDEndpoints:
    """Test CRUD operations"""
    
    def test_create_course(self):
        """Test POST /api/courses"""
        # TODO: Create a course
        # TODO: Verify it was created
        # TODO: Clean up (delete)
        pass
    
    def test_update_question(self):
        """Test PUT /api/questions/{id}"""
        # TODO: Update a question
        # TODO: Verify changes
        pass
    
    def test_delete_topic(self):
        """Test DELETE /api/topics/{id}"""
        # TODO: Delete a topic
        # TODO: Verify it's gone
        pass
```

**Tasks:**
1. Implement all test methods
2. Test error cases (404, 400, 500)
3. Ensure proper cleanup after tests

---

### Exercise 2.2: RAG System Tests
Test your RAG Q&A system.

```python
# tests/test_rag.py
class TestRAGSystem:
    """Test RAG Q&A functionality"""
    
    def test_rag_returns_answer_with_sources(self):
        """Test RAG returns both answer and sources"""
        response = client.post(
            "/api/rag/answer",
            json={"question": "What is normalization?"}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "answer" in data
        assert "sources" in data
        assert len(data["sources"]) > 0
        assert len(data["answer"]) > 50  # Meaningful answer
    
    def test_rag_cites_relevant_sources(self):
        """Test that cited sources are actually relevant"""
        # TODO: Implement test
        # Verify sources contain keywords from question
        pass
    
    def test_rag_handles_unknown_topics(self):
        """Test RAG gracefully handles questions outside domain"""
        # TODO: Ask question about unrelated topic
        # Should return "I don't know" type answer
        pass
```

**Tasks:**
1. Test answer quality
2. Verify source relevance
3. Test edge cases

---

## Exercise Set 3: Performance Testing

### Exercise 3.1: Latency Testing
Measure and optimize query latency.

```python
# tests/test_performance.py
import time
import statistics

def test_search_latency():
    """Measure average search latency"""
    queries = [
        "database normalization",
        "B+ tree indexing",
        "transaction isolation",
        "query optimization",
        "semantic search"
    ]
    
    latencies = []
    
    for query in queries:
        start = time.time()
        response = client.get(f"/api/search/semantic?query={query}")
        latency = time.time() - start
        latencies.append(latency)
        
        assert response.status_code == 200
    
    avg_latency = statistics.mean(latencies)
    p95_latency = statistics.quantiles(latencies, n=20)[18]  # 95th percentile
    
    print(f"\nAverage latency: {avg_latency*1000:.0f}ms")
    print(f"95th percentile: {p95_latency*1000:.0f}ms")
    
    # TODO: Set your target thresholds
    assert avg_latency < 0.5  # 500ms
    assert p95_latency < 1.0  # 1 second
```

**Tasks:**
1. Run latency tests
2. Identify slow queries
3. Optimize (add indexes, caching)
4. Re-run to verify improvement

---

### Exercise 3.2: Load Testing
Test system under concurrent load.

```python
from concurrent.futures import ThreadPoolExecutor
import time

def test_concurrent_users():
    """Test handling 50 concurrent users"""
    
    def make_search_request():
        start = time.time()
        response = client.get("/api/search/semantic?query=test")
        latency = time.time() - start
        return response.status_code, latency
    
    # Simulate 50 concurrent users
    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(make_search_request) for _ in range(50)]
        results = [f.result() for f in futures]
    
    status_codes = [r[0] for r in results]
    latencies = [r[1] for r in results]
    
    # Calculate metrics
    success_rate = sum(1 for s in status_codes if s == 200) / len(status_codes)
    avg_latency = statistics.mean(latencies)
    max_latency = max(latencies)
    
    print(f"\nConcurrent Users Test:")
    print(f"Success rate: {success_rate:.1%}")
    print(f"Average latency: {avg_latency*1000:.0f}ms")
    print(f"Max latency: {max_latency*1000:.0f}ms")
    
    # TODO: Set your thresholds
    assert success_rate >= 0.95  # 95% success rate
    assert avg_latency < 1.0     # 1 second average
```

**Tasks:**
1. Test with 10, 25, 50, 100 concurrent users
2. Monitor system resources (CPU, memory, DB connections)
3. Identify bottlenecks
4. Implement connection pooling/caching if needed

---

## Exercise Set 4: Search Quality Evaluation

### Exercise 4.1: Calculate Precision & Recall
Create test queries and evaluate search quality.

```python
# evaluation/search_quality.py

def evaluate_search_quality():
    """Evaluate semantic search precision and recall"""
    
    # Define test queries with known relevant questions
    test_cases = [
        {
            "query": "database normalization",
            "relevant_ids": {1, 5, 7, 12, 15, 18, 22, 25}  # IDs of relevant questions
        },
        {
            "query": "B+ tree indexing",
            "relevant_ids": {3, 8, 13, 19, 24, 29}
        },
        {
            "query": "transaction isolation levels",
            "relevant_ids": {2, 9, 14, 20, 26, 30}
        },
        # TODO: Add more test cases
    ]
    
    results = []
    
    for test_case in test_cases:
        # Get search results
        response = semantic_search(test_case["query"], top_k=10)
        returned_ids = {r.question_id for r in response}
        
        # Calculate metrics
        relevant_returned = returned_ids & test_case["relevant_ids"]
        
        precision = len(relevant_returned) / len(returned_ids)
        recall = len(relevant_returned) / len(test_case["relevant_ids"])
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        results.append({
            "query": test_case["query"],
            "precision": precision,
            "recall": recall,
            "f1_score": f1
        })
    
    # Calculate averages
    avg_precision = sum(r["precision"] for r in results) / len(results)
    avg_recall = sum(r["recall"] for r in results) / len(results)
    avg_f1 = sum(r["f1_score"] for r in results) / len(results)
    
    print("\nSearch Quality Metrics:")
    print(f"Average Precision: {avg_precision:.2%}")
    print(f"Average Recall: {avg_recall:.2%}")
    print(f"Average F1 Score: {avg_f1:.2%}")
    
    return results
```

**Tasks:**
1. Create 10+ test queries with labeled relevant questions
2. Run evaluation
3. Analyze results (which queries perform poorly?)
4. Try to improve (adjust embedding model, reranking, etc.)

---

### Exercise 4.2: Calculate MRR and NDCG
Implement advanced search metrics.

```python
def calculate_mrr(test_queries):
    """Calculate Mean Reciprocal Rank"""
    # TODO: Implement MRR calculation
    # For each query, find rank of first relevant result
    # MRR = average of 1/rank
    pass

def calculate_ndcg_at_k(test_queries, k=10):
    """Calculate NDCG@K"""
    # TODO: Implement NDCG calculation
    # Rate results on scale 0-3 (0=irrelevant, 3=highly relevant)
    # Calculate DCG and IDCG
    # NDCG = DCG / IDCG
    pass
```

**Tasks:**
1. Implement both functions
2. Create test dataset with relevance ratings
3. Calculate MRR and NDCG@10
4. Compare semantic vs keyword vs hybrid search

---

## Exercise Set 5: Portfolio Building

### Exercise 5.1: Create README
Write a professional README following this structure:

1. **Title & Badges**: Project name, tech stack badges
2. **Overview**: 2-3 sentence description
3. **Features**: Bullet list of key features
4. **Tech Stack**: Table of technologies
5. **Performance Metrics**: Table of benchmarks
6. **Architecture**: Diagram and explanation
7. **Quick Start**: Installation instructions
8. **Screenshots**: 3-5 key screenshots
9. **Learning Outcomes**: What you learned
10. **Links**: Demo, video, docs

**Tasks:**
- [ ] Write all sections
- [ ] Add badges from shields.io
- [ ] Create architecture diagram (use draw.io or mermaid)
- [ ] Take screenshots
- [ ] Proofread for typos

---

### Exercise 5.2: Record Demo Video
Record a 5-7 minute demo video.

**Script Outline:**
1. Introduction (30s): Name, project, tech stack
2. Problem (30s): What problem does it solve?
3. Architecture (1m): Show diagram, explain components
4. Demo (3-4m): Live walkthrough of features
5. Technical highlight (1m): Interesting code/challenge
6. Results (30s): Metrics, what you learned
7. Conclusion (30s): Links, call to action

**Tasks:**
- [ ] Write detailed script
- [ ] Practice 3-5 times
- [ ] Record with OBS Studio or Loom
- [ ] Edit (cut mistakes, add captions)
- [ ] Upload to YouTube
- [ ] Add to README

---

### Exercise 5.3: Write Evaluation Report
Create a comprehensive evaluation document.

**Structure:**
```markdown
# CourseDB-AI Evaluation Report

## Executive Summary
[2-3 sentences: key findings, overall assessment]

## Functional Completeness
[List all implemented features with checkmarks]

## Performance Evaluation
### Query Latency
[Table: operation, target, actual, status]

### Search Quality
[Table: precision, recall, MRR, NDCG scores]

### Database Performance
[Index usage, query times, cache hit rate]

## Code Quality
[Test coverage, PEP 8 compliance, documentation completeness]

## Challenges & Solutions
[3-5 major challenges you solved]

## Lessons Learned
[Key technical and process lessons]

## Future Improvements
[What would you add/change?]

## Conclusion
[Overall assessment of project]
```

**Tasks:**
- [ ] Write all sections with data
- [ ] Include charts/graphs
- [ ] Add code snippets for key solutions
- [ ] Export as PDF

---

## Exercise Set 6: Interview Preparation

### Exercise 6.1: STAR Method Practice
For each of these questions, write a STAR response (Situation, Task, Action, Result):

1. "Tell me about a time you optimized system performance."
2. "Describe a technical challenge you faced and how you solved it."
3. "Tell me about a time you had to learn a new technology quickly."
4. "Describe a bug that was particularly difficult to fix."
5. "Tell me about how you designed your database schema."

**Example Format:**
```
Question: "Tell me about a time you optimized system performance."

Situation: "In my CourseDB-AI project, semantic search was taking 2 seconds..."

Task: "I needed to reduce latency to under 500ms while maintaining quality..."

Action: "I analyzed the bottleneck, implemented HNSW indexing, tuned parameters..."

Result: "Reduced latency from 2000ms to 120ms - a 16x improvement..."
```

---

### Exercise 6.2: Technical Deep Dive Questions
Prepare detailed answers for:

1. **"How does your semantic search work?"**
   - Explain embeddings, similarity, indexing
   - Mention specific algorithms (HNSW)
   - Discuss trade-offs (speed vs accuracy)

2. **"Walk me through your database schema."**
   - Explain entities and relationships
   - Discuss normalization decisions
   - Mention indexes and why you created them

3. **"How did you implement RAG?"**
   - Retrieval step
   - Prompt construction
   - Generation with LLM
   - Citation mechanism

4. **"What would you improve if you had more time?"**
   - Fine-tuned embedding model
   - Advanced analytics
   - User feedback loop
   - Performance optimizations

**Tasks:**
- [ ] Write detailed answer for each question
- [ ] Include specific technical details
- [ ] Practice explaining out loud
- [ ] Time yourself (aim for 2-3 min per answer)

---

## Challenge Exercises

### Challenge 1: A/B Testing Framework
Implement A/B testing to compare search algorithms.

```python
# Compare semantic vs hybrid search
def run_ab_test(test_queries, method_a, method_b):
    """Run A/B test comparing two search methods"""
    # TODO: Implement A/B test
    # - Run same queries through both methods
    # - Calculate metrics for each
    # - Statistical significance test
    # - Declare winner
    pass
```

---

### Challenge 2: User Feedback Loop
Add ability for users to rate search results.

```python
# Add rating functionality
def rate_result(user_id, query, question_id, rating):
    """Record user rating of search result"""
    # TODO: Store rating in database
    pass

def retrain_with_feedback():
    """Use feedback to improve ranking"""
    # TODO: Implement learning from feedback
    # Options: reweight features, retrain model, adjust ranking
    pass
```

---

### Challenge 3: Advanced Analytics
Create advanced analytics dashboard.

Tasks:
- [ ] Topic clustering visualization
- [ ] Question difficulty progression over years
- [ ] Concept relationship graph
- [ ] Search query trends
- [ ] User behavior analytics

---

## Submission Checklist

### Code & Tests
- [ ] All tests passing
- [ ] Test coverage >70%
- [ ] Code formatted (black, isort)
- [ ] Linting passing (flake8)
- [ ] No security vulnerabilities

### Documentation
- [ ] README complete
- [ ] API documentation generated
- [ ] Architecture docs written
- [ ] Evaluation report complete
- [ ] Code comments added

### Portfolio
- [ ] Screenshots captured
- [ ] Demo video recorded
- [ ] LinkedIn post written
- [ ] GitHub profile updated

### Deployment
- [ ] Application Dockerized
- [ ] Deployed to production
- [ ] Environment variables set
- [ ] Health checks working

---

## Evaluation Rubric

| Component | Weight | Criteria |
|-----------|--------|----------|
| **Testing** | 25% | Coverage >70%, all tests passing |
| **Performance** | 20% | Meets latency targets, handles load |
| **Documentation** | 20% | Complete, clear, professional |
| **Portfolio** | 15% | README, video, presentation quality |
| **Code Quality** | 10% | Clean, maintainable, well-structured |
| **Search Quality** | 10% | Good precision/recall scores |

**Target: >85% for excellent work**

---

**Next:** [Implementation Plan](implementation_plan.md)

# Tests

**Testing Strategy for CourseDB-AI**

Comprehensive test suite for all components.

---

## 🧪 Test Structure

```
app/tests/
├── conftest.py          # Pytest fixtures and configuration
├── test_database.py     # Database connection tests
├── api/                 # API endpoint tests
│   ├── test_health.py
│   ├── test_courses.py
│   ├── test_questions.py
│   └── test_search.py
├── services/            # Service layer tests
│   ├── test_sql_search.py
│   ├── test_analytics.py
│   ├── test_chunking.py
│   ├── test_embedding.py
│   └── test_semantic_search.py
├── db/                  # Database model tests
│   ├── test_models.py
│   └── test_constraints.py
└── integration/         # End-to-end tests
    └── test_search_workflow.py
```

---

## 🎯 Testing Philosophy

1. **Write tests before trusting code**
2. **Test happy path and edge cases**
3. **Isolate units being tested**
4. **Use fixtures for common setup**
5. **Mock external dependencies**

---

## 📋 Test Categories

### Unit Tests
- Test individual functions
- Mock dependencies
- Fast execution
- High coverage

### Integration Tests
- Test component interactions
- Use test database
- Slower but comprehensive

### API Tests
- Test HTTP endpoints
- Validate request/response
- Check error handling

---

## 🚀 Running Tests

```bash
# Run all tests
pytest app/tests/

# Run specific test file
pytest app/tests/api/test_health.py

# Run with coverage
pytest --cov=app app/tests/

# Run with verbose output
pytest -v app/tests/
```

---

## 📝 Test Implementation Schedule

| Week | Tests to Implement |
|------|-------------------|
| **Week 5** | Database connection, health endpoint |
| **Week 6** | API endpoints, constraints, triggers |
| **Week 7** | B+ tree, hash index |
| **Week 9** | Transaction behavior |
| **Week 10** | Embedding, chunking, semantic search |
| **Week 11** | Integration tests |

---

## 🔍 Example Test

```python
def test_health_check(client):
    """Test health endpoint returns 200"""
    response = client.get("/health/")
    assert response.status_code == 200
    assert "status" in response.json()
```

---

## ✅ Test Checklist

Before marking feature complete:
- [ ] Unit tests written and passing
- [ ] Edge cases tested
- [ ] Error cases tested
- [ ] Integration test (if applicable)
- [ ] Test coverage > 80%

---

**TODO (Week 5+)**: Implement tests as features are built

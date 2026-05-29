# CourseDB-AI Application

This directory contains the main application code for CourseDB-AI.

---

## 📁 Structure

```
app/
├── backend/          # FastAPI application entry point
├── api/              # API endpoint modules
├── db/               # Database models, migrations, connection
├── services/         # Business logic services
├── frontend/         # Streamlit UI
└── tests/            # Test suite
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL with pgvector running (via docker-compose)
- Environment variables configured (.env)

### Setup
```bash
# Install dependencies
pip install -r ../requirements.txt

# Run migrations
cd db
alembic upgrade head

# Start backend
cd ../backend
uvicorn main:app --reload

# Start frontend (in separate terminal)
cd ../frontend
streamlit run streamlit_app.py
```

---

## 🏗️ Architecture

### Backend (FastAPI)
- RESTful API
- Async/await patterns
- Dependency injection for database sessions
- Pydantic models for request/response validation

### Database (PostgreSQL + pgvector)
- SQLAlchemy ORM models
- Alembic migrations
- Vector similarity search with pgvector

### Services
- **sql_search_service**: Traditional SQL-based filtering
- **semantic_search_service**: Vector similarity search
- **embedding_service**: Generate embeddings using Sentence Transformers
- **chunking_service**: Split resources into chunks
- **analytics_service**: Aggregate statistics and trends

### Frontend (Streamlit)
- Interactive dashboard
- Multi-page app structure
- API client for backend communication

---

## 📝 Development Guidelines

### Adding a New API Endpoint

1. Create endpoint in `api/` directory
2. Define Pydantic request/response models
3. Implement business logic in `services/`
4. Add tests in `tests/`
5. Document in `docs/architecture/api_documentation.md`

### Adding a New Database Table

1. Define SQLAlchemy model in `db/models.py`
2. Create Alembic migration: `alembic revision --autogenerate -m "Add table_name"`
3. Apply migration: `alembic upgrade head`
4. Add tests

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_semantic_search.py
```

---

## 📚 Learn More

- **Week 5**: PostgreSQL + FastAPI Foundation
- **Week 6**: SQL Queries, Views, Triggers
- **Week 10**: Embeddings and Semantic Search
- **Week 11**: Integrated System

---

**Status**: 🔄 Under Development (Built incrementally weeks 5-11)

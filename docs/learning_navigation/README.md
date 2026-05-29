# Learning Navigation System Documentation

## Overview

The Learning Navigation System is a unified interface that enables seamless traversal across all 12 weeks of the CourseDB-AI learning curriculum. It provides progressive navigation, resource discovery, progress tracking, and a comprehensive view of the entire learning journey.

## Architecture

### Components

1. **Data Models** (`app/db/models.py`)
   - `LearningWeek`: Stores metadata about each of the 12 weeks
   - `LearningResource`: Indexes all learning materials within each week

2. **Navigation Service** (`app/services/learning_navigation_service.py`)
   - `LearningNavigationService`: Core service for week/resource discovery and management

3. **API Endpoints** (`app/api/learning.py`)
   - RESTful API for curriculum navigation and resource access

4. **Frontend** (`app/frontend/streamlit_app.py`)
   - Interactive Streamlit dashboard for learning navigation

## Features

### 1. Curriculum Overview
- View all 12 weeks at a glance
- Track completion status (not_started, in_progress, completed)
- Monitor overall progress percentage

### 2. Progressive Navigation
- Navigate between weeks using prev/next buttons
- Jump directly to any week via dropdown selector
- Context-aware navigation with current/previous/next week info

### 3. Resource Discovery
- Automatic discovery of learning materials from filesystem
- Categorized by type:
  - 📄 Documentation (README, theory notes, implementation plans)
  - ✏️ Exercises (practice problems, checkpoints)
  - ✅ Solutions (exercise solutions)
  - 📓 Notebooks (Jupyter notebooks)
  - 💻 Code (Python scripts, SQL files)
  - 🤔 Reflection (weekly reflections)

### 4. Resource Search
- Search across all learning resources
- Filter by resource type
- Full-text search in titles and file paths

### 5. Progress Tracking
- Update week status via UI or API
- Track completed/in-progress/not-started weeks
- Calculate overall curriculum progress

### 6. Statistics Dashboard
- Total weeks and resources
- Resources by type breakdown
- Weeks by status distribution

## API Reference

### Base URL
```
http://localhost:8000/learning
```

### Endpoints

#### 1. Get Curriculum Overview
```http
GET /learning/curriculum
```

**Response:**
```json
{
  "weeks": [
    {
      "week_id": 1,
      "week_number": 1,
      "title": "DBMS Foundations + Project Orientation",
      "description": "...",
      "directory_path": "weeks/week_01_dbms_foundations",
      "status": "completed",
      "resources": [...]
    }
  ],
  "total_weeks": 12,
  "completed_weeks": 10,
  "in_progress_weeks": 2,
  "not_started_weeks": 0,
  "overall_progress": 83.33
}
```

#### 2. Get Week Navigation
```http
GET /learning/weeks/{week_number}
```

**Parameters:**
- `week_number` (path): Week number 1-12

**Response:**
```json
{
  "current_week": {...},
  "previous_week": {...},
  "next_week": {...},
  "total_weeks": 12,
  "progress_percentage": 83.33
}
```

#### 3. Get Week Details
```http
GET /learning/weeks/{week_number}/details
```

**Response:**
```json
{
  "week_id": 5,
  "week_number": 5,
  "title": "PostgreSQL + FastAPI Foundation",
  "description": "...",
  "directory_path": "weeks/week_05_postgresql_fastapi",
  "status": "completed",
  "created_at": "2026-05-29T00:00:00Z",
  "updated_at": "2026-05-29T00:00:00Z",
  "resources": [...]
}
```

#### 4. Update Week Status
```http
PUT /learning/weeks/{week_number}/status
```

**Request Body:**
```json
{
  "status": "completed"
}
```

**Response:**
```json
{
  "week_id": 5,
  "week_number": 5,
  "status": "completed",
  ...
}
```

#### 5. Initialize Curriculum
```http
POST /learning/initialize
```

Scans the `weeks/` directory and discovers all weeks and resources.

**Response:**
```json
{
  "message": "Curriculum initialized successfully",
  "total_weeks": 12,
  "total_resources": 87,
  "weeks": [
    {
      "week_number": 1,
      "title": "...",
      "resources_count": 8
    }
  ]
}
```

#### 6. Search Resources
```http
GET /learning/search?query={query}&resource_type={type}
```

**Parameters:**
- `query` (query): Search query
- `resource_type` (query, optional): Filter by type

**Response:**
```json
[
  {
    "resource_id": 42,
    "week_id": 5,
    "title": "Exercises",
    "file_path": "weeks/week_05_postgresql_fastapi/exercises.md",
    "resource_type": "exercise",
    "description": null,
    "order_index": 2,
    "created_at": "2026-05-29T00:00:00Z"
  }
]
```

#### 7. Get Statistics
```http
GET /learning/stats
```

**Response:**
```json
{
  "total_weeks": 12,
  "total_resources": 87,
  "resources_by_type": {
    "documentation": 36,
    "exercise": 12,
    "solution": 0,
    "notebook": 0,
    "code": 15,
    "reflection": 12
  },
  "weeks_by_status": {
    "completed": 10,
    "in_progress": 2,
    "not_started": 0
  }
}
```

## Usage Guide

### Setup

1. **Initialize the database tables:**
   ```bash
   # Start PostgreSQL
   docker-compose up -d

   # Run migrations (if using Alembic)
   alembic upgrade head
   ```

2. **Start the FastAPI backend:**
   ```bash
   cd app/backend
   uvicorn main:app --reload
   ```

3. **Initialize the curriculum:**
   ```bash
   curl -X POST http://localhost:8000/learning/initialize
   ```

4. **Start the Streamlit frontend:**
   ```bash
   cd app/frontend
   streamlit run streamlit_app.py
   ```

### Using the Frontend

1. **Navigate to the Streamlit app:**
   Open `http://localhost:8501` in your browser

2. **Initialize curriculum:**
   Click the "🔄 Refresh Curriculum" button to scan and index all weeks

3. **Browse weeks:**
   - Use the dropdown to select a specific week
   - Click prev/next buttons to navigate sequentially
   - View all weeks in the card grid

4. **View resources:**
   - Expand resource type categories to see all materials
   - File paths show exact locations in the repository

5. **Update progress:**
   - Change week status using the dropdown
   - Click "💾 Save Status" to persist changes

6. **Search resources:**
   - Switch to "Search Resources" page
   - Enter keywords and optional type filter
   - Results show matching resources across all weeks

### Using the API Directly

```python
import requests

BASE_URL = "http://localhost:8000/learning"

# Get curriculum overview
curriculum = requests.get(f"{BASE_URL}/curriculum").json()
print(f"Total weeks: {curriculum['total_weeks']}")
print(f"Progress: {curriculum['overall_progress']}%")

# Get specific week with navigation
week_5 = requests.get(f"{BASE_URL}/weeks/5").json()
print(f"Current: Week {week_5['current_week']['week_number']}")
print(f"Previous: {week_5['previous_week']['title']}")
print(f"Next: {week_5['next_week']['title']}")

# Search for exercises
results = requests.get(
    f"{BASE_URL}/search",
    params={"query": "exercise", "resource_type": "exercise"}
).json()
print(f"Found {len(results)} exercises")

# Update week status
response = requests.put(
    f"{BASE_URL}/weeks/5/status",
    json={"status": "completed"}
).json()
print(f"Status updated to: {response['status']}")
```

## Database Schema

### learning_weeks Table
```sql
CREATE TABLE learning_weeks (
    week_id SERIAL PRIMARY KEY,
    week_number INTEGER UNIQUE NOT NULL CHECK (week_number >= 1 AND week_number <= 12),
    title VARCHAR(200) NOT NULL,
    description TEXT,
    directory_path VARCHAR(500) NOT NULL,
    status VARCHAR(20) DEFAULT 'not_started' CHECK (status IN ('not_started', 'in_progress', 'completed')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_learning_weeks_number ON learning_weeks(week_number);
```

### learning_resources Table
```sql
CREATE TABLE learning_resources (
    resource_id SERIAL PRIMARY KEY,
    week_id INTEGER NOT NULL REFERENCES learning_weeks(week_id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    resource_type VARCHAR(50) NOT NULL CHECK (resource_type IN ('documentation', 'exercise', 'solution', 'notebook', 'code', 'reflection')),
    description TEXT,
    order_index INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_learning_resource_week_order ON learning_resources(week_id, order_index);
CREATE INDEX idx_learning_resource_title ON learning_resources(title);
```

## Resource Type Mapping

The system automatically categorizes files based on name patterns:

| File Pattern | Resource Type |
|-------------|---------------|
| `README.md` | documentation |
| `theory_notes.md` | documentation |
| `implementation_plan.md` | documentation |
| `mistakes_to_expect.md` | documentation |
| `exercises.md` | exercise |
| `checkpoints.md` | exercise |
| `solutions.md` | solution |
| `reflection.md` | reflection |
| `*.ipynb` | notebook |
| `*.py` | code |
| `*.sql` | code |

## Week Metadata

The system includes predefined metadata for all 12 weeks:

1. **Week 1:** DBMS Foundations + Project Orientation
2. **Week 2:** SQL Basics Through Academic Data
3. **Week 3:** ER Modeling + Schema Design
4. **Week 4:** Functional Dependencies + Normalization
5. **Week 5:** PostgreSQL + FastAPI Foundation
6. **Week 6:** SQL Queries, Views, Triggers, Constraints
7. **Week 7:** Indexing, B+ Tree, Hashing
8. **Week 8:** Query Optimization + EXPLAIN
9. **Week 9:** Transactions, ACID, Concurrency
10. **Week 10:** Embeddings, pgvector, Semantic Search
11. **Week 11:** Integrated CourseDB-AI System
12. **Week 12:** Evaluation, Polish, Portfolio

## Integration with Existing System

The Learning Navigation System integrates seamlessly with existing CourseDB-AI features:

- **Complementary to Course/Topic models:** Learning system focuses on curriculum structure, while Course/Topic models focus on academic content
- **API consistency:** Follows the same patterns as other API endpoints
- **Database integration:** Uses the same database and ORM (SQLAlchemy)
- **Frontend integration:** Built on the same Streamlit framework

## Future Enhancements

Potential improvements for the learning navigation system:

1. **Learning Path Recommendations:** Suggest next topics based on current progress
2. **Time Tracking:** Track time spent on each week
3. **Quiz Integration:** Link to practice quizzes for each week
4. **Progress Badges:** Award badges for completing milestones
5. **Notes System:** Allow users to add personal notes to weeks/resources
6. **Collaborative Features:** Share progress with mentors or study groups
7. **Mobile App:** Native mobile interface for on-the-go learning
8. **Offline Mode:** Download resources for offline study
9. **Resource Ratings:** Allow users to rate resource quality/difficulty
10. **Learning Analytics:** Track learning patterns and optimize curriculum

## Troubleshooting

### Issue: Curriculum not found
**Solution:** Run the initialization endpoint:
```bash
curl -X POST http://localhost:8000/learning/initialize
```

### Issue: Resources not discovered
**Solution:** Check that week directories follow the naming pattern `week_##_*` and contain supported file types.

### Issue: API connection failed
**Solution:** Ensure FastAPI backend is running on port 8000:
```bash
cd app/backend
uvicorn main:app --reload
```

### Issue: Database errors
**Solution:** Check database connection and ensure tables are created:
```bash
# Check if PostgreSQL is running
docker-compose ps

# Re-run migrations if needed
alembic upgrade head
```

## Contributing

To add new features to the learning navigation system:

1. **Add new resource types:** Update `resource_type_map` in `LearningNavigationService`
2. **Extend API:** Add new endpoints to `app/api/learning.py`
3. **Enhance service:** Add methods to `LearningNavigationService`
4. **Update frontend:** Add new pages/features to `streamlit_app.py`
5. **Update docs:** Document changes in this file

## License

Part of the CourseDB-AI learning project. See main repository LICENSE.

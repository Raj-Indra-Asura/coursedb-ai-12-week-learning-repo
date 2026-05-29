# Data Directory

This directory contains all data files for CourseDB-AI.

---

## 📁 Structure

### `raw/`
Original, unprocessed data files
- Previous-year question papers (PDF → text)
- Course syllabi
- Textbook chapter extracts
- Notes from various sources

**Status**: To be populated during Weeks 2-6

---

### `processed/`
Cleaned and structured data ready for database insertion
- `courses.json`
- `topics.json`
- `questions.json`
- `resources.json`

**Status**: To be created during Weeks 5-6

---

### `seed/`
Sample data for database seeding
- Small, curated datasets for testing
- Representative examples of all entity types
- Used by `scripts/seed_data.py`

**Contents** (to be created):
- `sample_courses.json`
- `sample_topics.json`
- `sample_questions.json`
- `sample_resources.json`

**Status**: To be created in Week 5-6

---

### `evaluation/`
Evaluation results and benchmark data
- Semantic search test queries and results
- Performance benchmarks
- Comparison data (keyword vs semantic search)

**Status**: To be created in Week 12

---

## 📝 Data Guidelines

### Data Collection (Weeks 2-6)

When collecting data:
- **Cite sources**: Always note where data came from
- **Clean thoroughly**: Remove duplicates, fix typos
- **Validate**: Check for completeness
- **Document**: Explain any transformations

### Data Privacy

⚠️ **Important**:
- Do NOT commit personal data (student names, IDs)
- Use anonymized or synthetic data
- Check `.gitignore` to ensure sensitive files excluded

### Data Quality

Ensure all data:
- Is properly formatted (JSON, CSV, SQL)
- Has no missing required fields
- Uses consistent naming conventions
- Includes metadata (source, date collected)

---

## 🔄 Data Processing Pipeline

```
raw/ (original files)
    ↓
  [cleaning, extraction]
    ↓
processed/ (structured JSON/CSV)
    ↓
  [seed_data.py]
    ↓
PostgreSQL database
    ↓
  [generate_embeddings.py]
    ↓
Vector embeddings in database
```

---

## 📊 Sample Data Statistics

**Target dataset size**:
- Courses: 5-10
- Topics: 30-50
- Questions: 100-200
- Resources: 20-50
- Resource Chunks: 200-500
- Embeddings: 200-500

---

## 🧪 Testing Data

For testing, use small datasets:
- 2-3 courses
- 10-15 topics
- 20-30 questions
- 5-10 resources

---

**Note**: This directory is mostly empty initially. You'll populate it gradually during Weeks 2-11.

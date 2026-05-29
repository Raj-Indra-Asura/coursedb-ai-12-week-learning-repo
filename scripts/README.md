# Utility Scripts

This directory contains scripts for database setup, data seeding, embedding generation, and evaluation.

---

## 📜 Scripts

### `setup_db.py`

**Purpose**: Initialize PostgreSQL database with schema

**Usage**:
```bash
python scripts/setup_db.py
```

**What it does**:
1. Connects to PostgreSQL
2. Enables pgvector extension
3. Creates all tables (courses, topics, questions, resources, etc.)
4. Creates indexes
5. Creates views
6. Creates triggers

**When to run**: Once during initial setup, or after schema changes

---

### `seed_data.py`

**Purpose**: Populate database with sample data

**Usage**:
```bash
python scripts/seed_data.py
```

**What it does**:
1. Loads seed data from `data/seed/`
2. Inserts courses, topics, resources, questions
3. Creates relationships (question_topics, resource_tags, etc.)
4. Validates data integrity

**When to run**: After setup_db.py, or to reset to clean state

---

### `generate_embeddings.py`

**Purpose**: Generate and store embeddings for all resources

**Usage**:
```bash
python scripts/generate_embeddings.py
```

**What it does**:
1. Chunks all resources using chunking service
2. Generates embeddings using Sentence Transformers
3. Inserts embeddings into chunk_embeddings table
4. Creates vector similarity index

**When to run**: After seed_data.py, or when new resources added

**Options**:
```bash
# Generate for specific resource
python scripts/generate_embeddings.py --resource-id 5

# Regenerate all embeddings
python scripts/generate_embeddings.py --regenerate

# Use different model
python scripts/generate_embeddings.py --model sentence-transformers/all-mpnet-base-v2
```

---

### `run_evaluation.py`

**Purpose**: Evaluate semantic search quality

**Usage**:
```bash
python scripts/run_evaluation.py
```

**What it does**:
1. Runs predefined test queries
2. Compares keyword search vs semantic search
3. Records top-k results for manual relevance assessment
4. Generates evaluation report in `data/evaluation/`

**When to run**: Week 12 (Evaluation)

---

## 🛠️ Development Scripts

### `init_db.sql`

**Purpose**: SQL initialization script for Docker

**Usage**: Automatically run by docker-compose on first startup

**What it does**:
- Creates database if not exists
- Enables pgvector extension
- Sets up initial configuration

---

## 📝 Script Guidelines

### Before Running Scripts

- [ ] Verify PostgreSQL is running (`docker-compose up -d`)
- [ ] Verify .env file is configured
- [ ] Verify Python dependencies installed
- [ ] Backup data if needed

### Error Handling

All scripts should:
- Check database connection before proceeding
- Validate input data
- Log errors with details
- Provide helpful error messages
- Support dry-run mode (where applicable)

---

## 🧪 Testing Scripts

```bash
# Test database connection
python scripts/setup_db.py --dry-run

# Test with small dataset
python scripts/seed_data.py --sample-size 10

# Test embedding generation on one resource
python scripts/generate_embeddings.py --resource-id 1
```

---

## 📚 Learn More

- **Week 5**: Database setup and connection
- **Week 10**: Embedding generation
- **Week 11**: System integration
- **Week 12**: Evaluation

---

**Remember**: Always test scripts on sample data before running on full dataset!

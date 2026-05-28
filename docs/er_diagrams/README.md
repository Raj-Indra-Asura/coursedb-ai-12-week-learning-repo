# ER Diagrams

**Week 3: ER Modeling + Schema Design**

This directory contains Entity-Relationship diagrams for CourseDB-AI.

---

## 📁 Files to Create

### `course_db_ai_er_design.md` (Week 3)
- Conceptual ER diagram
- Entity descriptions
- Relationship descriptions
- Cardinality explanations

### `er_to_relational.md` (Week 3)
- Mapping rules from ER to tables
- Junction table explanations
- Foreign key design

---

## 🎯 Entities

- Course
- Topic
- Resource
- Question
- Chapter
- Tag
- ResourceChunk
- Embedding
- User
- SearchLog
- AuditLog

---

## 🔗 Key Relationships

- Question-Topic: Many-to-Many
- Resource-Chapter: Many-to-Many
- Resource-Chunk: One-to-Many
- Topic-Topic: Self-referencing (hierarchy)

---

**TODO (Week 3)**: Create ER diagrams using Mermaid or draw.io

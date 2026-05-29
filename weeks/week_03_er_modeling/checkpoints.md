# Week 3: ER Modeling Progress Checkpoints

## 📋 Daily Checkpoints

Use this file to track your progress throughout Week 3. Check off items as you complete them and document your learning journey.

---

## Day 1: ER Fundamentals + Tool Setup

**Date**: ___________

### Theory Understanding
- [ ] Read `theory_notes.md` completely
- [ ] Read `README.md` for Week 3 overview
- [ ] Understand entity vs attribute difference
- [ ] Understand strong vs weak entities
- [ ] Understand cardinality (1:1, 1:N, M:N)
- [ ] Understand participation constraints (total vs partial)
- [ ] Know ER diagram notation symbols

### Tool Setup
- [ ] Choose ER diagramming tool (paper/Draw.io/Lucid chart/dbdiagram.io)
- [ ] Practice drawing entities (rectangles)
- [ ] Practice drawing attributes (ovals)
- [ ] Practice drawing relationships (diamonds)
- [ ] Practice connecting shapes with lines

### Practice Exercise
- [ ] Draw simple University ER diagram (Student, Course)
- [ ] Add attributes to each entity
- [ ] Underline primary keys
- [ ] Draw enrollment relationship (M:N)
- [ ] Label cardinality

**Time spent**: _____ hours

**What I learned today**:
```
[Write 2-3 sentences about key concepts]
```

**Tool I'm using**: ___________

**Confidence level (1-5)**: _____ / 5

---

## Day 2: Identify CourseDB-AI Entities

**Date**: ___________

### Entity Identification
- [ ] Read CourseDB-AI problem statement
- [ ] List all potential entities (nouns)
- [ ] Eliminate attributes masquerading as entities
- [ ] Identify 6+ core entities:
  - [ ] Course
  - [ ] Topic
  - [ ] Question
  - [ ] Resource
  - [ ] ResourceChunk
  - [ ] User
  - [ ] (SearchLog - relationship, not entity)

### Attribute Definition
- [ ] List 4-5 attributes for Course
- [ ] List 4-5 attributes for Topic
- [ ] List 4-5 attributes for Question
- [ ] List 4-5 attributes for Resource
- [ ] List 4-5 attributes for ResourceChunk
- [ ] List 4-5 attributes for User

### Primary Key Selection
- [ ] Identify PK for each entity
- [ ] Decide: SERIAL (auto-increment) or natural key?
- [ ] Decide: Should ResourceChunk be strong or weak entity?
- [ ] Document reasoning for PK choices

**Time spent**: _____ hours

**Entities identified**: _____ total

**Hardest decision**:
```
[Which entity was hardest to identify? Why?]
```

**Entity vs Attribute confusion**:
```
[Did you struggle with any? How did you resolve it?]
```

**Primary key decisions**:
```
Course PK: _____
Topic PK: _____
Question PK: _____
Resource PK: _____
ResourceChunk PK: _____ (strong or weak entity?)
User PK: _____
```

---

## Day 3: Determine Relationships

**Date**: ___________

### Relationship Identification
- [ ] Course → Topic: cardinality determined (1:N)
- [ ] Course → Question: cardinality determined (1:N)
- [ ] Topic → Question: cardinality determined (1:N)
- [ ] Course → Resource: cardinality determined (1:N)
- [ ] Resource → ResourceChunk: cardinality determined (1:N)
- [ ] User ↔ Question (search): cardinality determined (M:N)

### Cardinality Validation
- [ ] For each relationship, asked: "Can one A have many B?"
- [ ] For each relationship, asked: "Can one B have many A?"
- [ ] Identified which relationships need junction tables
- [ ] Documented participation constraints (total vs partial)

### Junction Table Identification
- [ ] Listed all M:N relationships
- [ ] Designed junction table for User ↔ Question (SearchLog)
- [ ] Identified additional attributes for junction table (timestamp, query)
- [ ] Determined primary key for junction table

### Query Validation
- [ ] Verified: "Get all topics for a course" query possible
- [ ] Verified: "Get all questions for a topic" query possible
- [ ] Verified: "Count questions per course" query possible
- [ ] Verified: "Find most searched questions" query possible
- [ ] Verified: "Get all chunks for a resource" query possible

**Time spent**: _____ hours

**Relationships documented**: _____ total

**Cardinality decisions**:
```
Course → Topic: 1:N (because _____)
Course → Question: 1:N (because _____)
Topic → Question: 1:N (because _____)
Resource → ResourceChunk: 1:N (because _____)
User ↔ Question: M:N (because _____)
```

**Hardest cardinality decision**:
```
[Which relationship was unclear? How did you resolve it?]
```

**Junction tables needed**: _____ (list them)

---

## Day 4: Draw Complete ER Diagram

**Date**: ___________

### ER Diagram Creation
- [ ] Laid out all entities on canvas/paper
- [ ] Drew entity rectangles with attributes inside
- [ ] Underlined all primary keys
- [ ] Drew relationship diamonds
- [ ] Connected entities to relationships with lines
- [ ] Labeled cardinality (1, N, M) on all relationships
- [ ] Marked participation constraints (single/double lines)
- [ ] Identified weak entities (double rectangles) if any

### Design Validation
- [ ] All entities present (Course, Topic, Question, Resource, ResourceChunk, User)
- [ ] All relationships connected
- [ ] All cardinality labels present
- [ ] Foreign key directions make sense
- [ ] Can answer all required queries from design
- [ ] Checked for common mistakes (see mistakes_to_expect.md)

### Comparison with Production
- [ ] Read `/app/db/models.py`
- [ ] Compared my entities with SQLAlchemy models
- [ ] Compared my relationships with ORM relationships
- [ ] Identified similarities (%)
- [ ] Identified differences
- [ ] Understood why differences exist

**Time spent**: _____ hours

**ER Diagram completed**: ☐ Hand-drawn ☐ Digital

**Similarity to production schema**: _____% 

**Major differences from production**:
1. ___________
2. ___________
3. ___________

**Why production schema differs**:
```
[Explain the design decisions in production code]
```

**What I learned from comparison**:
```
[Key insights from seeing production schema]
```

---

## Day 5: Map ER to SQL Schema

**Date**: ___________

### SQL Schema Creation
- [ ] Created database `coursedb_week3`
- [ ] Started with strong entities (no foreign keys)
- [ ] Added entities with 1:N relationships (foreign keys)
- [ ] Created junction tables for M:N relationships
- [ ] Added foreign key constraints with appropriate ON DELETE
- [ ] Added NOT NULL constraints for total participation
- [ ] Added UNIQUE constraints where needed
- [ ] Considered indexes for foreign keys

### Table Creation Order
- [ ] 1. courses (no dependencies)
- [ ] 2. users (no dependencies)
- [ ] 3. topics (depends on courses)
- [ ] 4. questions (depends on courses, topics)
- [ ] 5. resources (depends on courses)
- [ ] 6. resource_chunks (depends on resources)
- [ ] 7. search_logs (depends on users, questions)

### Schema Testing
- [ ] Ran `schema_week3.sql` successfully
- [ ] No syntax errors
- [ ] All tables created
- [ ] Verified with `\dt` in psql
- [ ] Described table structures with `\d table_name`

### Sample Data Insertion
- [ ] Inserted sample course
- [ ] Inserted sample topics
- [ ] Inserted sample questions
- [ ] Inserted sample resources
- [ ] Inserted sample resource chunks
- [ ] Inserted sample users
- [ ] Inserted sample search logs

### Validation Queries
- [ ] Query 1: Get all topics for a course
- [ ] Query 2: Get all questions for a topic
- [ ] Query 3: Count questions per course
- [ ] Query 4: Get all chunks for a resource
- [ ] Query 5: Find most searched questions
- [ ] All queries return correct results

**Time spent**: _____ hours

**SQL file created**: `schema_week3.sql` (_____ lines)

**Tables created**: _____ total

**Sample data**: _____ rows inserted total

**Query results**:
```
Query 1 (Get topics for course 1): _____ rows
Query 2 (Get questions for topic 1): _____ rows
Query 3 (Count questions per course): _____ courses
Query 4 (Get chunks for resource 1): _____ rows
Query 5 (Most searched questions): _____ rows
```

**SQL errors encountered**:
```
[List any errors and how you fixed them]
```

---

## Day 6: Compare with Production Schema

**Date**: ___________

### Production Code Analysis
- [ ] Read `/app/db/models.py` completely
- [ ] Analyzed SQLAlchemy model definitions
- [ ] Understood `relationship()` and `back_populates`
- [ ] Understood `ForeignKey()` definitions
- [ ] Analyzed column types and constraints
- [ ] Reviewed naming conventions

### Comparison Table Created
- [ ] Created detailed comparison table
- [ ] Documented entity matches
- [ ] Documented relationship matches
- [ ] Documented attribute matches
- [ ] Identified design differences
- [ ] Understood rationale for each difference

### Design Document
- [ ] Wrote design comparison document
- [ ] Explained my design decisions
- [ ] Explained production design decisions
- [ ] Documented trade-offs
- [ ] Listed key learnings
- [ ] Prepared questions for further exploration

**Time spent**: _____ hours

**Production schema analysis**: Complete ☐ Yes ☐ No

**Key differences discovered**:
1. ___________
2. ___________
3. ___________

**Production patterns to adopt**:
1. ___________
2. ___________
3. ___________

**Questions remaining**:
1. ___________
2. ___________
3. ___________

---

## Day 7: Practice with Alternative Designs

**Date**: ___________

### Library System Exercise
- [ ] Read problem statement
- [ ] Identified all entities (Book, Member, Author, Category, Loan)
- [ ] Determined all relationships
- [ ] Determined cardinality for each relationship
- [ ] Drew complete ER diagram
- [ ] Mapped to SQL schema
- [ ] Created `library_schema.sql`
- [ ] Tested with sample data
- [ ] Wrote validation queries

### E-Commerce Exercise
- [ ] Read problem statement
- [ ] Identified all entities (Customer, Product, Order, OrderItem, Review)
- [ ] Determined all relationships
- [ ] Handled M:N relationships (Order ↔ Product via OrderItems)
- [ ] Drew complete ER diagram
- [ ] Mapped to SQL schema
- [ ] Created `ecommerce_schema.sql`
- [ ] Tested with sample data
- [ ] Wrote validation queries

### Reflection
- [ ] Completed all reflection prompts in `reflection.md`
- [ ] Reflected on design decisions
- [ ] Reflected on cardinality reasoning
- [ ] Reflected on junction table usage
- [ ] Reflected on comparison with production
- [ ] Reflected on real-world applications

**Time spent**: _____ hours

**Library system**:
- Entities: _____ total
- Relationships: _____ total
- Junction tables: _____ total

**E-Commerce system**:
- Entities: _____ total
- Relationships: _____ total
- Junction tables: _____ total

**Most interesting design challenge**:
```
[Which exercise was most challenging? What did you learn?]
```

**Design patterns learned**:
1. ___________
2. ___________
3. ___________

---

## 📊 Week 3 Summary

### Time Breakdown
- Day 1 (Fundamentals + Tools): _____ hours
- Day 2 (Entity Identification): _____ hours
- Day 3 (Relationships): _____ hours
- Day 4 (ER Diagram): _____ hours
- Day 5 (SQL Mapping): _____ hours
- Day 6 (Production Comparison): _____ hours
- Day 7 (Practice Exercises): _____ hours
- **Total**: _____ hours

### Deliverables Completed
- [ ] CourseDB-AI ER Diagram (hand-drawn or digital)
- [ ] SQL Schema (`schema_week3.sql`)
- [ ] Design Comparison Document
- [ ] Library System ER + SQL
- [ ] E-Commerce System ER + SQL
- [ ] All reflection prompts answered
- [ ] All exercises completed

### Skills Gained
- [ ] Can identify entities vs attributes
- [ ] Can determine cardinality (1:1, 1:N, M:N)
- [ ] Can draw ER diagrams with correct notation
- [ ] Can map ER diagrams to SQL schemas
- [ ] Can create foreign key constraints
- [ ] Can design junction tables for M:N
- [ ] Understand weak vs strong entities
- [ ] Can validate designs with queries

### Mistakes Made and Corrected
1. ___________
2. ___________
3. ___________

**What I learned from mistakes**:
```
[Reflect on your errors and growth]
```

### Key Insights
1. ___________
2. ___________
3. ___________

### Most Valuable Concept
```
[What was the single most valuable thing you learned?]
```

### Remaining Questions
1. ___________
2. ___________
3. ___________

---

## 🎯 Readiness for Week 4: Normalization

Before moving to Week 4, ensure:

### Theory Understanding
- [ ] I can explain entities, attributes, and relationships
- [ ] I understand cardinality (1:1, 1:N, M:N)
- [ ] I know when to use junction tables
- [ ] I understand foreign key constraints
- [ ] I can read and draw ER diagrams

### Practical Skills
- [ ] I can identify entities from problem statements
- [ ] I can determine cardinality for relationships
- [ ] I can draw complete ER diagrams
- [ ] I can map ER diagrams to SQL CREATE statements
- [ ] I can validate designs with queries

### CourseDB-AI Understanding
- [ ] I understand all entities in CourseDB-AI
- [ ] I understand all relationships
- [ ] I know why each design decision was made
- [ ] I can query the database for required information

### Self-Assessment
**Confidence in ER Modeling (1-5)**: _____ / 5

**Areas where I'm strong**:
1. ___________
2. ___________

**Areas needing more practice**:
1. ___________
2. ___________

**Am I ready for Week 4?** ☐ Yes ☐ Need more time

**If not ready, what should I review?**:
```
[List specific topics to revisit]
```

---

## 📈 Progress Visualization

**Week 1 → Week 2 → Week 3 Progression**:

| Aspect | Week 1 | Week 2 | Week 3 |
|--------|--------|--------|--------|
| Focus | File System | SQL Basics | ER Modeling |
| Tool | Python | PostgreSQL | ER Diagrams |
| Complexity | Low | Medium | Medium-High |
| Design Thinking | Minimal | Some | Extensive |
| Confidence | ___/5 | ___/5 | ___/5 |

**What this progression shows**:
```
Reflect on your learning journey from manual files → SQL → database design.
How has your understanding of databases evolved?
```

---

## 🔗 Links to Week 3 Materials

- [README.md](./README.md) - Week overview
- [theory_notes.md](./theory_notes.md) - ER concepts
- [exercises.md](./exercises.md) - Practice problems
- [implementation_plan.md](./implementation_plan.md) - 7-day guide
- [reflection.md](./reflection.md) - Reflection prompts
- [mistakes_to_expect.md](./mistakes_to_expect.md) - Common errors

**Production Code**:
- `/app/db/models.py` - SQLAlchemy ORM models
- `/app/db/database.py` - Database configuration

---

## 🚀 Next Steps: Week 4 Preview

**Week 4: Normalization (1NF, 2NF, 3NF, BCNF)**

In Week 4, you'll learn to:
- Identify data anomalies (insertion, update, deletion)
- Apply normalization rules (1NF, 2NF, 3NF, BCNF)
- Understand functional dependencies
- Decompose tables to eliminate redundancy
- Balance normalization vs denormalization

**Preparation**:
- Review your Week 3 ER design
- Think about potential data anomalies
- Consider what "good design" means
- Bring questions about database design trade-offs

**Connection to Week 3**:
- ER modeling helps CREATE schemas
- Normalization helps IMPROVE schemas
- Both are essential design skills

---

**Last updated**: ___________

**Overall satisfaction with Week 3**: ⭐⭐⭐⭐⭐ (rate 1-5 stars)

**What I'm most excited about for Week 4**:
```
[Write 2-3 sentences]
```

**How Week 3 changed my perspective on databases**:
```
[Final reflection on what you learned]
```

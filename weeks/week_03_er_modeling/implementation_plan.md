# Week 3: ER Modeling Implementation Plan

## 📋 7-Day Learning Path

This plan guides you through designing the complete ER diagram for CourseDB-AI and mapping it to SQL schemas.

---

## Day 1: ER Fundamentals + Tool Setup

### Morning: Theory Review (2-3 hours)

**Read and understand:**
1. `theory_notes.md` - All ER concepts
2. `README.md` - Week 3 overview

**Key concepts to master:**
- Entities vs Attributes
- Strong vs Weak entities
- Relationships and cardinality (1:1, 1:N, M:N)
- Participation constraints
- ER diagram notation

**Self-check:**
- Can you explain the difference between an entity and an attribute?
- Can you draw the symbols for entity, attribute, relationship?
- Do you understand when to use 1:N vs M:N?

### Afternoon: Tool Setup + Practice (2-3 hours)

**Choose an ER diagramming tool:**

Option 1: **Paper + Pencil** (Recommended for learning)
- Forces you to think through design carefully
- Easy to erase and iterate
- No learning curve

Option 2: **Draw.io** (Free, web-based)
1. Go to https://draw.io
2. Practice drawing: rectangles (entities), ovals (attributes), diamonds (relationships)
3. Learn to add text labels and connect shapes

Option 3: **Lucidchart** (Professional tool)
1. Sign up for free account
2. Explore ER diagram templates
3. Practice with sample diagrams

**Practice Exercise:**
Draw an ER diagram for a simple "University" system:
- Entities: Student, Course
- Relationship: Student enrolls in Course (M:N)
- Include attributes: student_id, name, email for Student; course_id, title, credits for Course

**Deliverable:**
- Tool installed/ready to use
- One practice ER diagram drawn
- Comfortable with notation

---

## Day 2: Identify CourseDB-AI Entities

### Morning: Analyze Requirements (2-3 hours)

**Step 1: Read the CourseDB-AI problem statement**

CourseDB-AI helps students prepare for exams by:
- Storing previous year questions from multiple courses
- Organizing questions by topics
- Providing notes and resources
- Using semantic search to find relevant questions
- Tracking user searches for analytics

**Step 2: Identify entities (nouns)**

Read through the problem and highlight nouns:
- Courses
- Topics
- Questions
- Resources
- Users
- Search logs
- Resource chunks (for embeddings)

**Step 3: Determine if each noun is an entity or attribute**

Ask: "Does this thing have properties (attributes) of its own?"
- **Course**: Has code, title, description → **Entity**
- **Title**: Just a property of Course → **Attribute**
- **Topic**: Has name, order → **Entity**
- **Question**: Has text, difficulty, marks → **Entity**

**Exercise:** For each entity, list 4-5 attributes

```
Course:
- course_id (PK)
- course_code
- title
- description
- credits
- semester

Topic:
- topic_id (PK)
- topic_name
- order_index
- course_id (FK - to be determined)

[Continue for all entities...]
```

### Afternoon: Define Primary Keys (1-2 hours)

**For each entity, identify the primary key:**

- **Course**: course_id (SERIAL)
- **Topic**: topic_id (SERIAL)
- **Question**: question_id (SERIAL)
- **Resource**: resource_id (SERIAL)
- **ResourceChunk**: chunk_id (SERIAL) OR (resource_id, chunk_number) if weak entity
- **User**: user_id (SERIAL)

**Questions to consider:**
- Should chunk_id be global (strong entity) or local (weak entity)?
- Are there any natural keys (e.g., course_code)?
- Should we use SERIAL (auto-increment) or UUID?

**Deliverable:**
- List of 6+ entities
- Attributes for each entity
- Primary key identified for each entity
- Notes on design decisions

---

## Day 3: Determine Relationships

### Morning: Identify Relationships (2-3 hours)

**Step 1: For each pair of entities, ask:**
- Is there a relationship?
- What is the nature of the relationship?
- What is the cardinality?

**Example: Course and Topic**

Questions to ask:
- Can a course have multiple topics? **Yes** (Database course has: SQL, Normalization, Transactions...)
- Can a topic belong to multiple courses? **No** (Each topic belongs to one course)
- Cardinality: **1:N** (one-to-many)
- Participation: Topic needs Course (total), Course can exist without Topics (partial, but ideally total)

**Step 2: Document all relationships:**

```
1. Course → Topic
   - Cardinality: 1:N
   - Participation: Course (partial), Topic (total)
   - Implementation: Foreign key topic.course_id → courses.course_id

2. Course → Question
   - Cardinality: 1:N
   - Participation: Course (partial), Question (total)
   - Implementation: Foreign key question.course_id → courses.course_id

3. Topic → Question
   - Cardinality: 1:N
   - Participation: Topic (partial), Question (total)
   - Implementation: Foreign key question.topic_id → topics.topic_id

4. Course → Resource
   - Cardinality: 1:N
   - Participation: Course (partial), Resource (total)
   - Implementation: Foreign key resource.course_id → courses.course_id

5. Resource → ResourceChunk
   - Cardinality: 1:N
   - Participation: Resource (total), Chunk (total)
   - Implementation: Foreign key chunk.resource_id → resources.resource_id

6. User ↔ Question (via SearchLog)
   - Cardinality: M:N
   - Participation: User (partial), Question (partial)
   - Implementation: Junction table search_logs(user_id, question_id, search_query, timestamp)
```

### Afternoon: Validate Relationships (1-2 hours)

**Test your design with queries:**

For each relationship, verify you can write queries:

1. **Course → Topic**: "Get all topics for a specific course"
   - SQL: `SELECT * FROM topics WHERE course_id = ?`
   - ✅ Possible with 1:N relationship

2. **Topic → Question**: "Get all questions for a specific topic"
   - SQL: `SELECT * FROM questions WHERE topic_id = ?`
   - ✅ Possible with 1:N relationship

3. **Course → Question**: "Get all questions for a course"
   - SQL: `SELECT * FROM questions WHERE course_id = ?`
   - ✅ Possible with direct 1:N relationship

4. **User searches**: "Find most searched questions"
   - SQL: `SELECT question_id, COUNT(*) FROM search_logs GROUP BY question_id ORDER BY COUNT(*) DESC`
   - ✅ Possible with M:N junction table

**Deliverable:**
- Complete list of relationships with cardinality
- Validation queries for each relationship
- Notes on participation constraints

---

## Day 4: Draw Complete ER Diagram

### Morning: Draft ER Diagram (2-3 hours)

**Step 1: Layout entities**

On paper or in your tool, place entities:
```
        [Course]
       /    |    \
      /     |     \
  [Topic] [Question] [Resource]
    |        |          |
    |        |          |
    +--------+     [ResourceChunk]
        |
    [Question]
```

**Step 2: Add attributes to each entity**

For each entity box:
- List all attributes inside the rectangle
- Underline primary keys
- Mark foreign keys (even though they're relationships)

Example:
```
+------------------+
|     Course       |
+------------------+
| course_id (PK)   | ← Underlined
| course_code      |
| title            |
| description      |
| credits          |
| semester         |
+------------------+
```

**Step 3: Draw relationships**

Connect entities with diamonds:
```
[Course] ----< has >---- [Topic]
         1              N
```

**Step 4: Label cardinality**

For each relationship, mark:
- 1, N, or M on each side
- Total participation (double line) or partial (single line)

### Afternoon: Review and Iterate (1-2 hours)

**Validation checklist:**

- [ ] All entities present (Course, Topic, Question, Resource, ResourceChunk, User, SearchLog)
- [ ] All primary keys underlined
- [ ] All relationships connected with diamonds
- [ ] Cardinality marked on all relationships (1, N, M)
- [ ] Foreign key directions clear
- [ ] Can answer all required queries from this design

**Compare with actual implementation:**

Look at `/app/db/models.py` in the repository:
- Compare your entities with SQLAlchemy models
- Check if your relationships match
- Identify differences and understand why

**Deliverable:**
- Complete ER diagram (hand-drawn or digital)
- Validation checklist completed
- Notes on differences from actual implementation

---

## Day 5: Map ER to SQL Schema

### Morning: Create SQL Schema (3-4 hours)

**Step 1: Start with strong entities (no foreign keys)**

```sql
-- Course table (no foreign keys)
CREATE TABLE courses (
    course_id SERIAL PRIMARY KEY,
    course_code VARCHAR(20) UNIQUE NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    credits INTEGER,
    semester VARCHAR(20)
);

-- User table (no foreign keys)
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    role VARCHAR(50) DEFAULT 'student',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Step 2: Add entities with 1:N relationships (single foreign key)**

```sql
-- Topic table (references courses)
CREATE TABLE topics (
    topic_id SERIAL PRIMARY KEY,
    course_id INTEGER NOT NULL,
    topic_name VARCHAR(255) NOT NULL,
    order_index INTEGER,
    FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE
);

-- Question table (references courses AND topics)
CREATE TABLE questions (
    question_id SERIAL PRIMARY KEY,
    course_id INTEGER NOT NULL,
    topic_id INTEGER NOT NULL,
    question_text TEXT NOT NULL,
    difficulty VARCHAR(20),
    marks INTEGER,
    year INTEGER,
    FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE,
    FOREIGN KEY (topic_id) REFERENCES topics(topic_id) ON DELETE CASCADE
);

-- Resource table (references courses)
CREATE TABLE resources (
    resource_id SERIAL PRIMARY KEY,
    course_id INTEGER NOT NULL,
    title VARCHAR(255) NOT NULL,
    resource_type VARCHAR(50),
    url TEXT,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE
);

-- ResourceChunk table (references resources)
CREATE TABLE resource_chunks (
    chunk_id SERIAL PRIMARY KEY,
    resource_id INTEGER NOT NULL,
    chunk_number INTEGER NOT NULL,
    chunk_text TEXT NOT NULL,
    embedding VECTOR(1536),  -- For OpenAI embeddings
    FOREIGN KEY (resource_id) REFERENCES resources(resource_id) ON DELETE CASCADE,
    UNIQUE (resource_id, chunk_number)
);
```

**Step 3: Add M:N relationship with junction table**

```sql
-- SearchLog junction table (M:N between users and questions)
CREATE TABLE search_logs (
    log_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    question_id INTEGER,
    search_query TEXT NOT NULL,
    search_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES questions(question_id) ON DELETE SET NULL
);

-- Index for analytics queries
CREATE INDEX idx_search_logs_question ON search_logs(question_id);
CREATE INDEX idx_search_logs_user ON search_logs(user_id);
CREATE INDEX idx_search_logs_timestamp ON search_logs(search_timestamp);
```

### Afternoon: Test Schema (1-2 hours)

**Step 1: Create database and run schema**

```bash
# Create database
createdb coursedb_week3

# Run schema
psql -d coursedb_week3 -f schema_week3.sql
```

**Step 2: Insert sample data**

```sql
-- Insert sample course
INSERT INTO courses (course_code, title, description, credits) 
VALUES ('CS101', 'Database Management Systems', 'Introduction to DBMS', 3);

-- Insert sample topics
INSERT INTO topics (course_id, topic_name, order_index) 
VALUES 
    (1, 'ER Modeling', 1),
    (1, 'Normalization', 2),
    (1, 'SQL Queries', 3);

-- Insert sample questions
INSERT INTO questions (course_id, topic_id, question_text, difficulty, marks, year)
VALUES
    (1, 1, 'Explain the difference between strong and weak entities.', 'medium', 5, 2023),
    (1, 2, 'What is 3NF? Provide an example.', 'hard', 10, 2023);

-- Query to verify relationships
SELECT c.title, t.topic_name, q.question_text
FROM courses c
JOIN topics t ON c.course_id = t.course_id
JOIN questions q ON t.topic_id = q.topic_id;
```

**Step 3: Run validation queries**

Test all relationship queries from Day 3:
1. Get all topics for a course
2. Get all questions for a topic
3. Get all questions for a course
4. Count questions per topic
5. Find most searched questions

**Deliverable:**
- `schema_week3.sql` with complete CREATE TABLE statements
- Sample INSERT statements
- Validation query results
- Schema successfully created in PostgreSQL

---

## Day 6: Compare with Production Schema

### Morning: Analyze Actual Implementation (2-3 hours)

**Step 1: Read `/app/db/models.py`**

Open the actual CourseDB-AI models file:

```python
class Course(Base):
    __tablename__ = "courses"
    course_id = Column(Integer, primary_key=True)
    # ... other columns
    
    # Relationships
    topics = relationship("Topic", back_populates="course")
    questions = relationship("Question", back_populates="course")
```

**Step 2: Compare your design with production**

Create a comparison table:

| Aspect | Your Design | Production Design | Difference? |
|--------|-------------|-------------------|-------------|
| Course entity | course_id, title, ... | course_id, title, ... | ✅ Same |
| Topic → Course | 1:N, FK course_id | 1:N, FK course_id | ✅ Same |
| Question → Topic | 1:N, FK topic_id | 1:N, FK topic_id | ✅ Same |
| ResourceChunk PK | chunk_id (global) | chunk_id (global) | ✅ Same |
| SearchLog table | Exists | May not exist yet | ❓ Check |

**Step 3: Understand design differences**

For each difference, ask:
- Why did production choose this design?
- What are the trade-offs?
- Is your design also valid?

**Example differences you might find:**
- Additional indexes for performance
- Additional columns (created_at, updated_at timestamps)
- Different constraint names
- Additional validation (CHECK constraints)

### Afternoon: Document Learnings (1-2 hours)

**Create a design comparison document:**

```markdown
# CourseDB-AI ER Design Analysis

## My Design Decisions

1. **ResourceChunk as strong entity**
   - Used global chunk_id as primary key
   - Rationale: Simplifies queries, enables direct chunk retrieval
   - Alternative: Weak entity with (resource_id, chunk_number) composite key

2. **SearchLog as M:N junction table**
   - Tracks user searches for analytics
   - Enables queries like "most searched questions"
   - Could be expanded with: search_type, result_count, click_through

## Production Design Insights

1. **SQLAlchemy ORM patterns**
   - Uses relationship() for easy navigation
   - back_populates for bidirectional access
   - ON DELETE CASCADE for referential integrity

2. **Performance optimizations**
   - Indexes on foreign keys automatically created
   - Additional indexes for common queries
   - VECTOR type for pgvector embeddings

## What I Learned

- ER modeling helps think through relationships before coding
- Multiple valid designs exist; choose based on query patterns
- ORMs like SQLAlchemy map cleanly to ER diagrams
- Indexes are essential but not shown in ER diagrams

## Questions for Further Exploration

1. When should ResourceChunk be weak vs strong entity?
2. How to handle many-to-many with additional attributes?
3. What's the performance impact of different foreign key placements?
```

**Deliverable:**
- Comparison table (your design vs production)
- Design comparison document
- List of key learnings

---

## Day 7: Practice with Alternative Designs

### Morning: Design Exercise - Library System (2-3 hours)

**Problem Statement:**

"Design a library management system that tracks:
- Books (ISBN, title, author, publication_year, copies_available)
- Members (member_id, name, email, join_date, membership_type)
- Loans (which member borrowed which book, due_date, return_date)
- Authors (author_id, name, bio) - Books can have multiple authors
- Categories (category_id, name) - Books can belong to multiple categories"

**Tasks:**

1. **Identify entities:**
   - List all entities
   - Determine attributes for each
   - Identify primary keys

2. **Determine relationships:**
   - Book ↔ Author: M:N (books have multiple authors, authors write multiple books)
   - Book ↔ Category: M:N (books belong to multiple categories)
   - Member → Loan: 1:N (one member has many loans)
   - Book → Loan: 1:N (one book can be loaned multiple times, but track separately)

3. **Draw ER diagram:**
   - Include all entities, attributes, relationships
   - Mark cardinality on all relationships
   - Identify junction tables needed

4. **Map to SQL:**
   - Write CREATE TABLE statements
   - Include all foreign keys
   - Create junction tables for M:N relationships

5. **Validate:**
   - Can you query "all books by an author"?
   - Can you query "all books in a category"?
   - Can you query "overdue loans"?

### Afternoon: Design Exercise - E-Commerce (2-3 hours)

**Problem Statement:**

"Design an e-commerce system that tracks:
- Customers (customer_id, name, email, address, phone)
- Products (product_id, name, price, stock_quantity, category)
- Orders (order_id, customer_id, order_date, total_amount, status)
- OrderItems (order_id, product_id, quantity, price_at_purchase)
- Reviews (review_id, customer_id, product_id, rating, comment, review_date)"

**Tasks:**

1. Draw complete ER diagram
2. Identify all relationships and cardinality:
   - Customer → Order: ?
   - Order → OrderItem: ?
   - Product → OrderItem: ?
   - Customer → Review: ?
   - Product → Review: ?
3. Map to SQL schema
4. Write 5 validation queries

**Deliverable:**
- ER diagrams for both exercises
- SQL schemas for both exercises
- Validation queries
- Notes on design decisions

---

## Week 3 Deliverables Checklist

Before moving to Week 4, ensure you have:

### **Required Deliverables:**

- [ ] **CourseDB-AI ER Diagram** (hand-drawn or digital)
  - All entities (Course, Topic, Question, Resource, ResourceChunk, User)
  - All relationships with cardinality marked
  - Primary keys underlined
  - Foreign key directions indicated

- [ ] **SQL Schema** (`schema_week3.sql`)
  - CREATE TABLE statements for all entities
  - Foreign key constraints
  - Junction table for M:N relationships
  - Sample INSERT statements

- [ ] **Design Comparison Document**
  - Your design vs production schema
  - Explanation of differences
  - Design decisions and trade-offs
  - Key learnings

- [ ] **Practice Exercises Completed**
  - Library system ER diagram + SQL
  - E-commerce system ER diagram + SQL
  - Validation queries for both

### **Knowledge Verification:**

- [ ] Can draw ER diagrams with correct notation
- [ ] Can identify entities vs attributes
- [ ] Can determine cardinality (1:1, 1:N, M:N)
- [ ] Can map ER diagrams to SQL schemas
- [ ] Understand when to use junction tables
- [ ] Can explain design decisions

### **Ready for Week 4:**

- [ ] Understand CourseDB-AI schema completely
- [ ] Can query all relationships
- [ ] Ready to learn normalization (identifying design flaws)

---

## Common Mistakes to Avoid

See `mistakes_to_expect.md` for detailed list of common errors and how to fix them.

**Top 3 mistakes:**
1. **Confusing entities with attributes** (is "phone number" an entity or attribute?)
2. **Wrong cardinality** (1:N vs M:N confusion)
3. **Missing junction tables** for M:N relationships

---

## Additional Resources

- **ER Diagram Tools**: Draw.io, Lucidchart, dbdiagram.io
- **SQL Testing**: Use PostgreSQL to validate your schemas
- **Real-world examples**: Study schemas of open-source projects
- **Practice datasets**: University, hospital, e-commerce, social media

---

**Next Week**: Week 4 - Normalization (1NF, 2NF, 3NF, BCNF) - Learn to identify and fix data anomalies!

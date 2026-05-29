# Week 3: ER Modeling + Schema Design

**Duration**: 7 days
**Status**: 🔄 Ready to Start

## 🧭 Navigation

**[← Previous: Week 2](../week_02_sql_basics/reflection.md)** | **[View Learning Path](../../LEARNING_PATH.md)** | **[Next: Theory Notes →](theory_notes.md)**

---

## 🎯 Why This Week Matters

After Week 1's painful experience with file-based storage and Week 2's introduction to SQL, you might wonder: **"How do I design a good database schema from scratch?"**

This is where **ER (Entity-Relationship) Modeling** comes in. Before writing any SQL code, professional database designers create visual diagrams to:
- Identify entities (tables) and their attributes (columns)
- Define relationships between entities (foreign keys)
- Determine cardinality (1:1, 1:N, M:N)
- Catch design flaws early before implementation

**Why ER Modeling matters for CourseDB-AI:**
- CourseDB-AI has 6+ entities: courses, topics, questions, resources, chunks, users
- These entities have complex relationships (courses have topics, topics have questions)
- Poor design = difficult queries, data anomalies, performance issues
- Good design = clean code, efficient queries, scalable system

**Real-world impact:**
- Tech companies spend weeks on ER design before coding
- Schema changes in production are expensive (migrations, downtime)
- ER diagrams facilitate team communication (devs, PMs, stakeholders)
- Visual models catch errors that SQL syntax cannot

---

## 📚 Learning Objectives

By the end of this week, you will be able to:

✅ Draw ER diagrams with correct notation (entities, attributes, relationships)
✅ Identify entities and their attributes from problem statements
✅ Determine cardinality ratios (1:1, 1:N, M:N) between entities
✅ Distinguish between strong and weak entities
✅ Map ER diagrams to SQL schemas (CREATE TABLE statements)
✅ Design a complete ER diagram for CourseDB-AI
✅ Understand participation constraints (total vs partial)
✅ Create junction tables for M:N relationships

---

## 📖 Concepts to Learn

### **1. ER Modeling Fundamentals**

**What is ER Modeling?**
A visual technique for database design using diagrams to represent:
- **Entities**: Objects/things (Student, Course, Question)
- **Attributes**: Properties (name, age, title, difficulty)
- **Relationships**: Associations (Student enrolls Course, Topic has Questions)

**Why use diagrams instead of jumping to SQL?**
- Visual representation is easier to understand and communicate
- Identifies design problems before coding
- Serves as documentation for the database
- Facilitates stakeholder discussions (non-technical people understand diagrams)

### **2. Entities**

**Entity**: A distinguishable object or thing in the real world

**Types:**
- **Strong Entity**: Exists independently (Student, Course, Professor)
- **Weak Entity**: Depends on another entity for existence (Dependent, CourseSection)

**ER Notation:**
```
[Rectangle] = Strong Entity
[[Double Rectangle]] = Weak Entity
```

**CourseDB-AI Examples:**
- Strong: `Course`, `Topic`, `Question`, `Resource`, `User`
- Weak: `ResourceChunk` (cannot exist without Resource)

### **3. Attributes**

**Types of Attributes:**
1. **Simple**: Cannot be divided (age, email, difficulty)
2. **Composite**: Can be divided (name → first_name + last_name)
3. **Derived**: Calculated from others (age from birth_date, question_count from questions)
4. **Multivalued**: Multiple values (phone_numbers, tags, skills)

**Key Attributes:**
- **Primary Key**: Uniquely identifies entity (course_id, question_id)
- **Partial Key**: Used in weak entities (chunk_number within resource)

**ER Notation:**
```
(Oval) = Attribute
(Underlined Oval) = Primary Key
(Dashed Oval) = Derived Attribute
((Double Oval)) = Multivalued Attribute
```

### **4. Relationships**

**Relationship**: Association between two or more entities

**Examples:**
- Course *has* Topics
- Topic *contains* Questions
- Student *enrolls in* Course
- Professor *teaches* Course

**Relationship Attributes**: Relationships can have their own attributes
```
Example: Enrollment(student, course, grade, semester, enrollment_date)
```

**ER Notation:**
```
<Diamond> = Relationship
<<Double Diamond>> = Identifying Relationship (for weak entities)
```

### **5. Cardinality Ratios**

Cardinality specifies **how many** instances of one entity relate to instances of another.

#### **1:1 (One-to-One)**
- One entity instance relates to exactly one instance of another
- Example: Person → Passport (each person has one passport)
- Implementation: Foreign key on either side

#### **1:N (One-to-Many)**
- One entity instance relates to many instances of another
- Example: Course → Topics (one course has many topics)
- Example: Topic → Questions (one topic has many questions)
- Implementation: Foreign key on the "many" side

#### **M:N (Many-to-Many)**
- Multiple instances relate to multiple instances
- Example: Student ↔ Course (students enroll in many courses, courses have many students)
- Implementation: **Requires junction table** (enrollments table)

**CourseDB-AI Relationships:**
```
Course (1) → (N) Topic      [1:N - one course has many topics]
Topic (1) → (N) Question    [1:N - one topic has many questions]
Course (1) → (N) Question   [1:N - one course has many questions]
Resource (1) → (N) Chunk    [1:N - one resource has many chunks]
User (M) ↔ (N) Question     [M:N - users search many questions, questions searched by many users]
```

### **6. Participation Constraints**

**Total Participation** (double line): Every entity **must** participate
- Example: Every Question *must* belong to a Topic
- SQL: `NOT NULL` on foreign key

**Partial Participation** (single line): Not all entities must participate
- Example: Not every Professor teaches a Course (sabbatical, research-only)
- SQL: `NULL` allowed on foreign key

### **7. Weak Entities**

**Weak Entity**: Cannot exist without a strong (owner) entity

**Characteristics:**
- Has partial key (not globally unique)
- Unique only within the strong entity's scope
- Connected via identifying relationship

**Example:**
```
Course (strong) → CourseSection (weak)
- Section number alone is not unique (many courses have "Section 1")
- (course_id, section_number) together form unique identifier
```

**CourseDB-AI Example:**
```
Resource (strong) → ResourceChunk (weak)
- chunk_id is globally unique (strong entity, not weak)
- Alternative design: chunk_number within resource (weak entity)
```

### **8. Mapping ER to SQL Schema**

#### **Rule 1: Strong Entity → Table**
```
ER: Course(course_id, title, description, credits)
SQL: CREATE TABLE courses (
    course_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    credits INTEGER
);
```

#### **Rule 2: 1:1 Relationship**
Add foreign key to either side (usually the entity with fewer instances)
```
ER: Person (1) ↔ (1) Passport
SQL: CREATE TABLE passports (
    passport_id SERIAL PRIMARY KEY,
    person_id INTEGER UNIQUE NOT NULL,
    issue_date DATE,
    FOREIGN KEY (person_id) REFERENCES persons(person_id)
);
```

#### **Rule 3: 1:N Relationship**
Add foreign key on the "many" side
```
ER: Course (1) → (N) Topic
SQL: CREATE TABLE topics (
    topic_id SERIAL PRIMARY KEY,
    course_id INTEGER NOT NULL,
    topic_name VARCHAR(255),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);
```

#### **Rule 4: M:N Relationship**
Create junction table with foreign keys to both entities
```
ER: Student (M) ↔ (N) Course
SQL: CREATE TABLE enrollments (
    student_id INTEGER,
    course_id INTEGER,
    grade VARCHAR(2),
    semester VARCHAR(10),
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);
```

#### **Rule 5: Weak Entity**
Include foreign key to strong entity + partial key as composite primary key
```
ER: Employee (1) → (N) Dependent (weak)
SQL: CREATE TABLE dependents (
    employee_id INTEGER,
    dependent_name VARCHAR(100),
    relationship VARCHAR(50),
    PRIMARY KEY (employee_id, dependent_name),
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id) ON DELETE CASCADE
);
```

---

## 🛠️ This Week's Exercises

### **Exercise 1: Identify Entities and Attributes**
Read the CourseDB-AI problem statement and identify:
- All entities (courses, topics, questions, resources, users...)
- Attributes for each entity
- Primary keys for each entity
- Which attributes should be NOT NULL

### **Exercise 2: Determine Relationships**
For each pair of entities, determine:
- Is there a relationship?
- What is the cardinality (1:1, 1:N, M:N)?
- What is the participation (total or partial)?
- Does the relationship have attributes?

### **Exercise 3: Draw ER Diagram**
Create a complete ER diagram for CourseDB-AI including:
- All 6+ entities
- All relationships with cardinality
- Primary keys underlined
- Foreign key placements indicated

### **Exercise 4: Map ER to SQL**
Convert your ER diagram to SQL CREATE TABLE statements:
- One table per strong entity
- Foreign keys for 1:N relationships
- Junction tables for M:N relationships
- Appropriate constraints (NOT NULL, UNIQUE, CHECK)

### **Exercise 5: Validate Design**
Test your schema design by writing queries for:
- Get all topics for a course
- Get all questions for a topic
- Get all resources related to a course
- Find the most searched questions
- Count questions per topic

---

## 📦 Deliverables

By the end of Week 3, you should have:

1. **ER Diagram for CourseDB-AI** (hand-drawn or digital tool)
   - All entities with attributes
   - All relationships with cardinality
   - Primary keys marked
   - Weak entities identified (if any)

2. **SQL Schema from ER Diagram** (`schema_week3.sql`)
   - CREATE TABLE statements for all entities
   - Foreign key constraints for all relationships
   - Junction tables for M:N relationships
   - Appropriate data types and constraints

3. **Design Comparison Document**
   - Compare your design with the actual `app/db/models.py`
   - Identify similarities and differences
   - Explain design decisions (why certain relationships exist)
   - Document what you learned

4. **ER Modeling Notes**
   - Your own summary of ER concepts
   - Common mistakes and how to avoid them
   - Tips for identifying entities vs attributes
   - When to use weak entities

---

## ✅ Self-Check Quiz

Test your understanding before moving to Week 4:

1. **What's the difference between an entity and an attribute?**
   - Entity: _______
   - Attribute: _______

2. **How do you implement a 1:N relationship in SQL?**
   - Answer: _______

3. **When do you need a junction table?**
   - Answer: _______

4. **What's the difference between total and partial participation?**
   - Total: _______
   - Partial: _______

5. **How do you identify a weak entity?**
   - Answer: _______

6. **What's the primary key of a junction table in an M:N relationship?**
   - Answer: _______

7. **Why is ER modeling important before coding?**
   - Answer: _______

8. **How do you represent a derived attribute in ER diagrams?**
   - Answer: _______

9. **What's the difference between 1:N and M:N relationships?**
   - 1:N: _______
   - M:N: _______

10. **How do you map a multivalued attribute to SQL?**
    - Answer: _______

---

## 🎓 CourseDB-AI ER Design Deep Dive

### **Entities:**

1. **Course**
   - Attributes: course_id (PK), course_code, title, description, credits, semester
   - Strong entity

2. **Topic**
   - Attributes: topic_id (PK), course_id (FK), topic_name, order_index
   - Strong entity

3. **Question**
   - Attributes: question_id (PK), course_id (FK), topic_id (FK), question_text, difficulty, marks, year
   - Strong entity

4. **Resource**
   - Attributes: resource_id (PK), course_id (FK), title, resource_type, url, upload_date
   - Strong entity

5. **ResourceChunk**
   - Attributes: chunk_id (PK), resource_id (FK), chunk_number, chunk_text, embedding
   - Strong entity (has its own global PK)
   - Could be designed as weak entity with (resource_id, chunk_number) as composite PK

6. **User**
   - Attributes: user_id (PK), username, email, role, created_at
   - Strong entity

### **Relationships:**

1. **Course → Topic** (1:N)
   - One course has many topics
   - Foreign key: `topic.course_id → course.course_id`

2. **Course → Question** (1:N)
   - One course has many questions
   - Foreign key: `question.course_id → course.course_id`

3. **Topic → Question** (1:N)
   - One topic has many questions
   - Foreign key: `question.topic_id → topic.topic_id`

4. **Course → Resource** (1:N)
   - One course has many resources
   - Foreign key: `resource.course_id → course.course_id`

5. **Resource → ResourceChunk** (1:N)
   - One resource is split into many chunks
   - Foreign key: `chunk.resource_id → resource.resource_id`

6. **User ↔ Question** (M:N via SearchLog)
   - Users search many questions, questions searched by many users
   - Junction table: `search_logs(user_id, question_id, search_query, timestamp)`

### **Design Decisions:**

- **Why Topic entity?** Organizes questions by chapter/theme, enables hierarchical structure
- **Why ResourceChunk?** Large PDFs need to be split for embedding generation and semantic search
- **Why SearchLog?** Tracks user behavior for analytics and recommendations
- **Why NOT weak entity for chunks?** Global chunk_id simplifies queries and indexing

---

## 🔗 Additional Resources

### **ER Diagram Tools:**
- [Draw.io](https://draw.io) - Free online diagramming tool
- [Lucidchart](https://lucidchart.com) - Professional diagramming (free tier)
- [dbdiagram.io](https://dbdiagram.io) - Database schema designer
- [ERDPlus](https://erdplus.com) - Academic ER diagram tool
- Paper + Pencil - Sometimes the best tool for initial brainstorming!

### **Practice Datasets:**
- University database (students, courses, professors)
- Library management system (books, authors, members, loans)
- E-commerce system (products, customers, orders, reviews)
- Hospital system (patients, doctors, appointments, prescriptions)

---

## 📝 Study Tips

1. **Draw diagrams by hand first** - Forces you to think through relationships carefully
2. **Start with entities** - Identify nouns in problem statements
3. **Then find relationships** - Identify verbs connecting entities
4. **Check cardinality both ways** - "One course has many topics" AND "One topic belongs to one course"
5. **Validate with sample queries** - Can your design answer all required questions?
6. **Compare with real systems** - Look at `app/db/models.py` to see production design
7. **Practice on multiple domains** - Don't just memorize CourseDB-AI schema

---

## 🚀 Connection to Later Weeks

**Week 4: Normalization**
- Your ER design determines normalization requirements
- Poor ER design → data anomalies → normalization challenges

**Week 5: PostgreSQL + FastAPI**
- ER diagram → SQLAlchemy models
- Relationships → ORM configuration (foreign keys, backref)

**Week 6: Advanced SQL**
- Complex queries depend on well-designed relationships
- JOINs are easier with clear foreign keys

**Week 7: Indexing**
- Primary keys and foreign keys need indexes
- Query patterns inform index strategy

**Week 10: Semantic Search**
- Resource → ResourceChunk relationship enables chunking
- Embedding storage design depends on ER model

---

## 🎯 Week 3 Success Criteria

You've successfully completed Week 3 if you can:

✅ Draw a complete ER diagram for CourseDB-AI from memory
✅ Explain each relationship and its cardinality
✅ Map the ER diagram to SQL CREATE TABLE statements
✅ Identify design flaws in a given ER diagram
✅ Distinguish between entities that should vs shouldn't be in the database
✅ Create junction tables for M:N relationships
✅ Explain design decisions for CourseDB-AI schema

**Ready to begin?** Start with Day 1 in `implementation_plan.md`!

**Questions?** Review `theory_notes.md` and `mistakes_to_expect.md`

---

## 🧭 Navigation

**[← Previous: Week 2](../week_02_sql_basics/reflection.md)** | **[Back to Week 3 Overview](README.md)** | **[Next: Theory Notes →](theory_notes.md)**

---

## 📋 Week 3 File Sequence

1. **[Week 3 README](README.md)** ← You are here
2. **[Theory Notes](theory_notes.md)** - Core concepts
3. **[Exercises](exercises.md)** - Practice
4. **[Implementation Plan](implementation_plan.md)** - Apply concepts
5. **[Checkpoints](checkpoints.md)** - Track progress
6. **[Mistakes to Expect](mistakes_to_expect.md)** - Common pitfalls
7. **[Reflection](reflection.md)** - Weekly reflection
8. **[→ Week 4](../week_04_normalization/README.md)** - Continue journey

---

**Next Week**: Week 4 - Normalization (1NF, 2NF, 3NF, BCNF) - Learn to eliminate data anomalies!

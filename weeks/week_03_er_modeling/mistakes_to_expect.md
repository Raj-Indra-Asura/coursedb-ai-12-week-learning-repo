# Week 3: Common ER Modeling Mistakes

## 🎯 Purpose

ER modeling requires careful thinking about entities, relationships, and cardinality. This guide documents common mistakes students make and how to avoid them. Learning from these mistakes will save you hours of frustration!

---

## Mistake Category 1: Entity vs Attribute Confusion

### ❌ Mistake 1.1: Making Attributes into Entities

**Wrong:**
```
Entities: Student, Email
Relationship: Student has Email (1:1)
```

**Why it's wrong:**
- Email is a property of Student, not an independent entity
- Creates unnecessary complexity
- No additional attributes for Email entity

**Correct:**
```
Entity: Student
Attributes: student_id, name, email, major
```

**Rule of thumb:**
Ask: "Does this thing have multiple properties of its own, or is it just a single value?"
- If single value → Attribute
- If multiple properties → Entity

---

### ❌ Mistake 1.2: Making Entities into Attributes

**Wrong:**
```
Entity: Course
Attributes: course_id, title, instructor_name, instructor_email, instructor_office
```

**Why it's wrong:**
- Instructor has multiple properties (name, email, office)
- Same instructor teaches multiple courses (data duplication)
- If instructor email changes, must update all courses

**Correct:**
```
Entity 1: Course (course_id, title)
Entity 2: Instructor (instructor_id, name, email, office)
Relationship: Instructor teaches Course (1:N)
```

**Rule of thumb:**
If you're adding multiple attributes with the same prefix (instructor_*, customer_*, product_*), consider making it a separate entity.

---

### ❌ Mistake 1.3: Multivalued Attributes as Simple Attributes

**Wrong:**
```
Entity: Student
Attributes: student_id, name, phone_number (VARCHAR)
```

**Why it's wrong:**
- What if student has multiple phone numbers (home, mobile, work)?
- Can't store multiple values in single column

**Correct (Option A - Separate Entity):**
```
Entity 1: Student (student_id, name)
Entity 2: PhoneNumber (phone_id, student_id FK, phone_number, phone_type)
Relationship: Student has PhoneNumber (1:N)
```

**Correct (Option B - Array in PostgreSQL):**
```sql
CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    phone_numbers TEXT[]  -- PostgreSQL array
);
```

**Rule of thumb:**
If attribute can have multiple values, either create separate entity (1:N) or use array/JSON type.

---

## Mistake Category 2: Cardinality Errors

### ❌ Mistake 2.1: Confusing 1:N with M:N

**Wrong:**
```
Student (1) → (N) Course
Implementation: course_id FK in students table
```

**Why it's wrong:**
- One student takes MANY courses (correct)
- One course has MANY students (ALSO correct!)
- This is M:N, not 1:N

**Correct:**
```
Student (M) ↔ (N) Course
Implementation: Junction table enrollments(student_id, course_id, grade, semester)
```

**How to determine:**
Ask BOTH directions:
- "Can one Student have many Courses?" → Yes
- "Can one Course have many Students?" → Yes
- If BOTH yes → M:N (needs junction table)

---

### ❌ Mistake 2.2: Using M:N When It Should Be 1:N

**Wrong:**
```
Course (M) ↔ (N) Topic
Implementation: Junction table course_topics(course_id, topic_id)
```

**Why it's wrong:**
- In CourseDB-AI, each topic belongs to ONE course only
- "Database Normalization" topic shouldn't belong to both "DBMS" and "Data Structures" courses
- Junction table adds unnecessary complexity

**Correct:**
```
Course (1) → (N) Topic
Implementation: course_id FK in topics table
```

**How to check:**
Ask: "In the real-world domain, can Topic X belong to multiple courses?"
- If no → 1:N (foreign key)
- If yes → M:N (junction table)

---

### ❌ Mistake 2.3: Wrong Foreign Key Placement in 1:N

**Wrong:**
```sql
-- Professor (1) → (N) Course
CREATE TABLE professors (
    prof_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    course_id INTEGER  -- WRONG: Professor can teach multiple courses!
);
```

**Why it's wrong:**
- Foreign key is on the "one" side instead of "many" side
- Can only store one course per professor

**Correct:**
```sql
CREATE TABLE courses (
    course_id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    prof_id INTEGER,  -- CORRECT: Foreign key on "many" side
    FOREIGN KEY (prof_id) REFERENCES professors(prof_id)
);
```

**Rule:**
In 1:N relationships, foreign key goes on the "N" (many) side.

---

## Mistake Category 3: Junction Table Errors

### ❌ Mistake 3.1: Forgetting Junction Table for M:N

**Wrong:**
```sql
-- Student (M) ↔ (N) Course
CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    course_id INTEGER  -- WRONG: Can only store ONE course!
);
```

**Correct:**
```sql
CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE courses (
    course_id SERIAL PRIMARY KEY,
    title VARCHAR(255)
);

CREATE TABLE enrollments (  -- Junction table
    student_id INTEGER,
    course_id INTEGER,
    grade VARCHAR(2),
    semester VARCHAR(10),
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);
```

---

### ❌ Mistake 3.2: Wrong Primary Key in Junction Table

**Wrong:**
```sql
CREATE TABLE enrollments (
    enrollment_id SERIAL PRIMARY KEY,  -- Allows duplicate (student, course)!
    student_id INTEGER,
    course_id INTEGER,
    grade VARCHAR(2)
);
```

**Why it's wrong:**
- Same student can enroll in same course multiple times (duplicates)
- No constraint preventing: (student=1, course=101) appearing twice

**Correct (Option A - Composite PK):**
```sql
CREATE TABLE enrollments (
    student_id INTEGER,
    course_id INTEGER,
    grade VARCHAR(2),
    PRIMARY KEY (student_id, course_id)  -- Prevents duplicates
);
```

**Correct (Option B - Surrogate PK + Unique Constraint):**
```sql
CREATE TABLE enrollments (
    enrollment_id SERIAL PRIMARY KEY,
    student_id INTEGER,
    course_id INTEGER,
    grade VARCHAR(2),
    UNIQUE (student_id, course_id)  -- Prevents duplicates
);
```

**Rule:**
Junction tables must prevent duplicate pairs, either via composite PK or UNIQUE constraint.

---

### ❌ Mistake 3.3: Junction Table with Only Foreign Keys

**Problem:**
```sql
-- User (M) ↔ (N) Question (search logs)
CREATE TABLE search_logs (
    user_id INTEGER,
    question_id INTEGER,
    PRIMARY KEY (user_id, question_id)
);
```

**What's missing:**
- When was the search performed? (timestamp)
- What was the search query? (search_query)
- How many results? (result_count)

**Better:**
```sql
CREATE TABLE search_logs (
    log_id SERIAL PRIMARY KEY,
    user_id INTEGER,
    question_id INTEGER,
    search_query TEXT NOT NULL,
    search_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (question_id) REFERENCES questions(question_id)
);
```

**Rule:**
Junction tables often store additional attributes beyond the relationship itself.

---

## Mistake Category 4: Weak Entity Confusion

### ❌ Mistake 4.1: Treating Everything as Strong Entity

**Suboptimal:**
```sql
CREATE TABLE resource_chunks (
    chunk_id SERIAL PRIMARY KEY,  -- Global ID
    resource_id INTEGER,
    chunk_number INTEGER,
    chunk_text TEXT
);
```

**Alternative (Weak Entity):**
```sql
CREATE TABLE resource_chunks (
    resource_id INTEGER,
    chunk_number INTEGER,
    chunk_text TEXT,
    PRIMARY KEY (resource_id, chunk_number),  -- Composite key
    FOREIGN KEY (resource_id) REFERENCES resources(resource_id) ON DELETE CASCADE
);
```

**Trade-offs:**
- Strong entity (global chunk_id): Easier to reference chunks directly
- Weak entity (composite key): Enforces chunks only exist with resources

**Not always a mistake - design choice!**

---

### ❌ Mistake 4.2: Using Weak Entity When Strong Entity is Better

**Wrong:**
```sql
-- Employee (1) → (N) Project
CREATE TABLE projects (
    employee_id INTEGER,
    project_name VARCHAR(100),
    budget DECIMAL,
    PRIMARY KEY (employee_id, project_name)  -- Weak entity?
);
```

**Why it's wrong:**
- Projects are independent entities that can exist without employees
- Multiple employees can work on same project (should be M:N!)
- Project should have global project_id

**Correct:**
```sql
CREATE TABLE projects (
    project_id SERIAL PRIMARY KEY,  -- Strong entity
    project_name VARCHAR(100),
    budget DECIMAL
);

CREATE TABLE project_assignments (  -- M:N junction table
    employee_id INTEGER,
    project_id INTEGER,
    role VARCHAR(50),
    PRIMARY KEY (employee_id, project_id)
);
```

**Rule:**
Only use weak entities when the entity truly cannot exist independently.

---

## Mistake Category 5: Relationship Modeling

### ❌ Mistake 5.1: Missing Relationship

**Incomplete design:**
```
Entities: Course, Question
(No relationship defined)
```

**Problem:**
- How do you know which questions belong to which course?
- Can't query "all questions for DBMS course"

**Correct:**
```
Course (1) → (N) Question
Implementation: question.course_id → course.course_id
```

**Rule:**
If entities are related in the problem domain, model the relationship!

---

### ❌ Mistake 5.2: Redundant Relationships

**Over-designed:**
```
Course (1) → (N) Topic (1) → (N) Question
Course (1) → (N) Question  -- Redundant!
```

**Why it might be wrong:**
- Question already linked to Course through Topic
- Can query course questions via Topic JOIN
- Redundant foreign key (question.course_id)

**However, in CourseDB-AI this is INTENTIONAL:**
- Performance: Direct Course → Question link avoids extra JOIN
- Flexibility: Some questions might not have topics
- Trade-off: Redundancy for query performance

**Rule:**
Redundant relationships CAN be intentional - understand the trade-offs!

---

### ❌ Mistake 5.3: Self-Referencing Relationship Errors

**Wrong:**
```sql
-- Users follow other users
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    follows_user_id INTEGER  -- WRONG: Can only follow ONE user!
);
```

**Correct:**
```sql
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE user_follows (  -- M:N self-referencing
    follower_id INTEGER,
    followee_id INTEGER,
    follow_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (follower_id, followee_id),
    FOREIGN KEY (follower_id) REFERENCES users(user_id),
    FOREIGN KEY (followee_id) REFERENCES users(user_id),
    CHECK (follower_id != followee_id)  -- Prevent self-follow
);
```

**Rule:**
Self-referencing M:N needs junction table just like regular M:N.

---

## Mistake Category 6: SQL Mapping Errors

### ❌ Mistake 6.1: Forgetting Foreign Key Constraints

**Wrong:**
```sql
CREATE TABLE topics (
    topic_id SERIAL PRIMARY KEY,
    course_id INTEGER,  -- No constraint!
    topic_name VARCHAR(255)
);
```

**Problems:**
- Can insert topic with course_id = 999 (doesn't exist)
- No referential integrity
- No cascading deletes

**Correct:**
```sql
CREATE TABLE topics (
    topic_id SERIAL PRIMARY KEY,
    course_id INTEGER NOT NULL,
    topic_name VARCHAR(255) NOT NULL,
    FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE
);
```

---

### ❌ Mistake 6.2: Wrong ON DELETE Behavior

**Dangerous:**
```sql
FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE SET NULL
```

**Problem:**
- Deleting a course sets topic.course_id to NULL
- Orphaned topics with no course (might violate business logic)

**Better options:**
```sql
-- Option 1: Prevent deletion if topics exist
ON DELETE RESTRICT

-- Option 2: Delete topics when course deleted
ON DELETE CASCADE

-- Option 3: Set to default course (e.g., "Uncategorized")
ON DELETE SET DEFAULT
```

**Rule:**
Choose ON DELETE behavior based on business logic!

---

### ❌ Mistake 6.3: Forgetting NOT NULL on Foreign Keys

**Wrong:**
```sql
CREATE TABLE questions (
    question_id SERIAL PRIMARY KEY,
    topic_id INTEGER,  -- NULL allowed!
    question_text TEXT NOT NULL
);
```

**Problem:**
- Questions can exist without topics (orphaned data)
- Violates business rule: "Every question must belong to a topic"

**Correct:**
```sql
CREATE TABLE questions (
    question_id SERIAL PRIMARY KEY,
    topic_id INTEGER NOT NULL,  -- Enforces total participation
    question_text TEXT NOT NULL,
    FOREIGN KEY (topic_id) REFERENCES topics(topic_id)
);
```

**Rule:**
Use NOT NULL for total participation (entity must participate in relationship).

---

## Mistake Category 7: Design Process Mistakes

### ❌ Mistake 7.1: Coding Before Designing

**Wrong approach:**
1. Start writing CREATE TABLE statements
2. Realize you forgot a relationship
3. Add column to existing table
4. Realize it should be M:N
5. Create junction table
6. Repeat...

**Correct approach:**
1. Draw ER diagram on paper
2. Identify all entities, attributes, relationships
3. Validate with sample queries
4. THEN write SQL
5. Fewer iterations, cleaner design

---

### ❌ Mistake 7.2: Not Validating Design with Queries

**Problem:**
Design looks good on paper, but when you try to query:
```sql
-- "Get all questions for a course"
SELECT * FROM questions WHERE course_id = ?  -- ERROR: No course_id column!
```

**Solution:**
Before finalizing ER diagram, list required queries:
1. Get all topics for a course
2. Get all questions for a topic
3. Count questions per course
4. Find most searched questions
5. ...

Then verify your ER design supports these queries!

---

### ❌ Mistake 7.3: Over-Engineering Early

**Over-designed:**
```
Entities: Course, Topic, Subtopic, SubSubtopic, Question
Relationships: Course → Topic → Subtopic → SubSubtopic → Question
```

**Problem:**
- Adds complexity for uncertain future requirements
- "What if topics have sub-topics?" - Maybe later!

**Better:**
```
Entities: Course, Topic, Question
Start simple, add hierarchy later if needed
```

**Rule:**
Design for current requirements, not hypothetical future needs.

---

## Debugging Checklist

When your ER diagram doesn't work:

### ✅ Entity-Attribute Check:
- [ ] Are all entities truly entities (not attributes)?
- [ ] Are all attributes truly attributes (not entities)?
- [ ] Are primary keys identified for all entities?

### ✅ Cardinality Check:
- [ ] Did I check cardinality in BOTH directions?
- [ ] Do M:N relationships have junction tables?
- [ ] Are foreign keys on the correct side of 1:N relationships?

### ✅ SQL Mapping Check:
- [ ] Are all foreign key constraints present?
- [ ] Are ON DELETE behaviors appropriate?
- [ ] Are NOT NULL constraints applied for total participation?

### ✅ Query Validation Check:
- [ ] Can I query all required relationships?
- [ ] Are junction tables preventing duplicates?
- [ ] Can I JOIN to get related data?

---

## Quick Reference: Decision Tree

**Is X an entity or attribute?**
```
Does X have multiple properties? 
├─ Yes → Entity
└─ No → Is X multivalued?
    ├─ Yes → Separate entity (1:N) or array
    └─ No → Attribute
```

**What's the cardinality?**
```
Can one A have many B?
├─ Yes ┐
└─ No  ├→ Can one B have many A?
       │  ├─ Yes → M:N (junction table)
       │  └─ No → 1:N (FK on B side)
       └→ 1:1 (FK on either side)
```

**Do I need a junction table?**
```
Is it M:N?
├─ Yes → Junction table required
└─ No → Foreign key sufficient
```

---

## Learning from Mistakes

**After completing Week 3:**
1. Review this guide
2. Identify which mistakes you made
3. Understand WHY each was a mistake
4. Document your learnings in reflection.md
5. Apply lessons to Week 4 (Normalization)

**Remember:** Making mistakes is part of learning! The goal is to recognize and fix them quickly.

---

**Next:** Complete `checkpoints.md` to track your progress and ensure you've avoided these common mistakes!

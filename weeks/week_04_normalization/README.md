# Week 4: Normalization + Functional Dependencies

**Duration**: 7 days
**Status**: 🔄 Ready to Start

---

## 🎯 Why This Week Matters

After Week 3's ER modeling, you can design database schemas. But **how do you know if your design is good?**

Week 4 teaches you to **evaluate and improve** database designs using normalization theory:
- Identify data anomalies (update, delete, insert problems)
- Apply normalization rules (1NF, 2NF, 3NF, BCNF)
- Understand functional dependencies
- Decompose tables to eliminate redundancy
- Balance normalization vs performance

**Why normalization matters for CourseDB-AI:**
- Poor design → duplicate data, inconsistent updates, wasted storage
- Good design → data integrity, efficient queries, maintainable code
- Production databases must handle thousands of concurrent updates without corruption

**Real-world impact:**
- Twitter's early database anomalies caused data inconsistencies
- Facebook normalizes user data to prevent profile update bugs
- Banking systems use 3NF to prevent transaction errors
- E-commerce sites normalize to avoid order/inventory mismatches

Without normalization, you might:
- Update a course title in one table but forget another (inconsistency)
- Delete a question and accidentally lose course information
- Store the same data hundreds of times (waste)

---

## 📚 Learning Objectives

By the end of this week, you will be able to:

✅ Identify data anomalies (update, delete, insert) in table designs
✅ Understand functional dependencies (X → Y)
✅ Apply 1NF (First Normal Form) - eliminate repeating groups
✅ Apply 2NF (Second Normal Form) - eliminate partial dependencies
✅ Apply 3NF (Third Normal Form) - eliminate transitive dependencies
✅ Apply BCNF (Boyce-Codd Normal Form) - handle all anomalies
✅ Decompose tables using normalization rules
✅ Understand when denormalization is appropriate
✅ Evaluate CourseDB-AI schema for normalization compliance

---

## 📖 Concepts to Learn

### **1. Data Anomalies**

**Three types of problems caused by poor database design:**

#### **Update Anomaly**
Changing one piece of data requires updating multiple rows.

**Example:**
```
questions(question_id, course_code, course_title, question_text)
1, CS201, Database Systems, "What is DBMS?"
2, CS201, Database Systems, "Explain SQL"
3, CS201, Database Systems, "What is normalization?"
```

**Problem:** If course title changes from "Database Systems" to "Database Management Systems", we must update 3 rows! If we miss one, data becomes inconsistent.

**Solution:** Separate courses into their own table.

#### **Deletion Anomaly**
Deleting one record loses other unrelated information.

**Example:**
```
questions(question_id, course_code, course_title, question_text)
100, CS301, Operating Systems, "What is a process?"
```

**Problem:** If we delete question 100 (the only question for CS301), we lose all information about the "Operating Systems" course!

**Solution:** Store courses independently of questions.

#### **Insertion Anomaly**
Cannot insert data without having other unrelated data.

**Example:**
```
questions(question_id, course_code, course_title, question_text)
```

**Problem:** Cannot add a new course "CS401: Computer Networks" unless we have at least one question for it. But we want to create the course before questions exist!

**Solution:** Separate courses from questions.

---

### **2. Functional Dependencies (FD)**

**Definition:** X → Y (read: "X determines Y")
- If you know X, you can determine Y
- Y is functionally dependent on X
- X is the determinant

**Examples:**
```
student_id → student_name, email, major
- Knowing student_id uniquely determines name, email, and major

course_code → course_title, credits
- Knowing course_code determines title and credits

(student_id, course_id) → grade
- Knowing both student_id AND course_id determines the grade
```

**Trivial vs Non-Trivial FDs:**
- **Trivial:** X → Y where Y ⊆ X
  - Example: (student_id, name) → student_id (useless!)
- **Non-Trivial:** X → Y where Y ⊄ X
  - Example: student_id → name (useful!)

**Full vs Partial Functional Dependency:**
- **Full FD:** Y depends on ALL of X
  - Example: (student_id, course_id) → grade (need both to determine grade)
- **Partial FD:** Y depends on PART of X
  - Example: (student_id, course_id) → student_name (only need student_id!)

**Transitive Dependency:**
X → Y and Y → Z, therefore X → Z (indirect dependency)
- Example: student_id → dept_id, dept_id → dept_name
- Therefore: student_id → dept_name (transitive)

---

### **3. First Normal Form (1NF)**

**Rule:** Eliminate repeating groups and multivalued attributes.

**Requirements:**
1. Each column contains atomic (indivisible) values
2. Each column contains values of the same type
3. Each column has a unique name
4. Order of rows doesn't matter

**Violation Examples:**

**Violation 1: Multivalued attribute**
```
students(student_id, name, phone_numbers)
1, Alice, "555-1234, 555-5678, 555-9012"
```

**Fix:** Separate phone numbers table
```
students(student_id, name)
1, Alice

phone_numbers(student_id, phone_number)
1, 555-1234
1, 555-5678
1, 555-9012
```

**Violation 2: Repeating groups**
```
courses(course_id, title, topic1, topic2, topic3)
1, DBMS, SQL, Normalization, Transactions
```

**Fix:** Separate topics table
```
courses(course_id, title)
1, DBMS

topics(course_id, topic_name)
1, SQL
1, Normalization
1, Transactions
```

**Violation 3: Non-atomic values**
```
students(student_id, full_name)
1, "Alice Johnson"
```

**Fix (if needed):** Split into first_name, last_name
```
students(student_id, first_name, last_name)
1, Alice, Johnson
```

---

### **4. Second Normal Form (2NF)**

**Rule:** Must be in 1NF + eliminate partial dependencies.

**Applies to:** Tables with composite primary keys

**Definition:** Every non-key attribute must depend on the ENTIRE primary key, not just part of it.

**Violation Example:**
```
enrollments(student_id, course_id, grade, student_name, course_title)
Primary Key: (student_id, course_id)
```

**Problems:**
- student_name depends only on student_id (partial dependency!)
- course_title depends only on course_id (partial dependency!)
- grade depends on BOTH (full dependency - OK)

**Functional Dependencies:**
```
(student_id, course_id) → grade         [Full FD - OK]
student_id → student_name                [Partial FD - VIOLATION]
course_id → course_title                 [Partial FD - VIOLATION]
```

**Fix (Decompose):**
```
students(student_id, student_name)
courses(course_id, course_title)
enrollments(student_id, course_id, grade)
```

**Result:** Each non-key attribute depends on the entire key!

---

### **5. Third Normal Form (3NF)**

**Rule:** Must be in 2NF + eliminate transitive dependencies.

**Definition:** No non-key attribute should depend on another non-key attribute.

**Violation Example:**
```
employees(emp_id, emp_name, dept_id, dept_name, dept_building)
Primary Key: emp_id
```

**Problems:**
```
emp_id → dept_id       [OK - depends on key]
emp_id → dept_name     [Transitive!]
emp_id → dept_building [Transitive!]

Why transitive?
emp_id → dept_id → dept_name
emp_id → dept_id → dept_building
```

**Fix (Decompose):**
```
employees(emp_id, emp_name, dept_id)
departments(dept_id, dept_name, dept_building)
```

**Result:** No transitive dependencies!

---

### **6. Boyce-Codd Normal Form (BCNF)**

**Rule:** Must be in 3NF + every determinant must be a candidate key.

**Definition:** For every non-trivial FD X → Y, X must be a superkey.

**When 3NF is not enough:**

**Example (3NF but not BCNF):**
```
course_instructors(student_id, course_id, instructor_id)
Constraints:
- Each student has one instructor per course
- Each instructor teaches only one course
- Multiple instructors can teach the same course

Primary Key: (student_id, course_id)
FDs:
(student_id, course_id) → instructor_id  [OK]
instructor_id → course_id                [VIOLATION - determinant not a key!]
```

**Problem:** instructor_id → course_id but instructor_id is not a superkey!

**Fix:**
```
enrollments(student_id, instructor_id)
instructor_courses(instructor_id, course_id)
```

**BCNF is stricter than 3NF:**
- 3NF allows non-key attributes to determine other non-key attributes (in some cases)
- BCNF requires ALL determinants to be candidate keys

---

### **7. Normalization Process**

**Step-by-step approach:**

**Step 1: Start with unnormalized table**
```
questions(q_id, q_text, course_code, course_title, credits, topics)
1, "What is SQL?", CS201, Database Systems, 3, "SQL, Queries, DDL"
```

**Step 2: Apply 1NF (eliminate repeating groups)**
```
questions(q_id, q_text, course_code, course_title, credits, topic)
1, "What is SQL?", CS201, Database Systems, 3, SQL
1, "What is SQL?", CS201, Database Systems, 3, Queries
1, "What is SQL?", CS201, Database Systems, 3, DDL
```

**Step 3: Apply 2NF (eliminate partial dependencies)**

With composite key (q_id, topic):
- course_code, course_title, credits depend only on q_id (partial!)

Decompose:
```
questions(q_id, q_text, course_code, course_title, credits)
question_topics(q_id, topic)
```

**Step 4: Apply 3NF (eliminate transitive dependencies)**

In questions table:
- q_id → course_code
- course_code → course_title, credits (transitive!)

Decompose:
```
courses(course_code, course_title, credits)
questions(q_id, q_text, course_code)
question_topics(q_id, topic)
```

**Final result:** 3NF schema with no anomalies!

---

### **8. Denormalization (Breaking the Rules)**

**Sometimes normalization goes too far!**

**When to denormalize:**
1. **Performance:** JOINs are too expensive for frequent queries
2. **Read-heavy workloads:** More reads than writes
3. **Reporting:** Aggregate data needed frequently
4. **Caching:** Computed values stored for speed

**Example: CourseDB-AI Design Decision**

**Fully Normalized (3NF):**
```
questions(question_id, topic_id, question_text)
topics(topic_id, course_id, topic_name)
courses(course_id, title)

To get question with course:
SELECT q.*, c.title
FROM questions q
JOIN topics t ON q.topic_id = t.topic_id
JOIN courses c ON t.course_id = c.course_id
```

**Denormalized (CourseDB-AI actual design):**
```
questions(question_id, topic_id, course_id, question_text)
- Redundant course_id violates 3NF!
- But avoids JOIN for common query: "questions by course"
```

**Trade-offs:**
- ✅ **Pro:** Faster queries (no JOIN needed)
- ✅ **Pro:** Simpler application code
- ❌ **Con:** Redundant data (course_id stored twice)
- ❌ **Con:** Update anomaly risk (must update both topic_id and course_id)

**When denormalization is acceptable:**
- Query performance is critical
- Data doesn't change frequently
- Application ensures consistency
- Benefits outweigh risks

---

## 🛠️ This Week's Exercises

### **Exercise 1: Identify Anomalies**
Given a table design, identify:
- Update anomalies
- Delete anomalies
- Insert anomalies
- Functional dependencies
- Violation of which normal form?

### **Exercise 2: Normalize to 1NF**
Convert tables with repeating groups to 1NF.

### **Exercise 3: Normalize to 2NF**
Identify and eliminate partial dependencies.

### **Exercise 4: Normalize to 3NF**
Identify and eliminate transitive dependencies.

### **Exercise 5: Evaluate CourseDB-AI Schema**
Analyze the production schema for normalization compliance.

---

## 📦 Deliverables

By the end of Week 4, you should have:

1. **Normalization Practice Problems** (10+ exercises solved)
   - Identify anomalies in given schemas
   - Apply 1NF, 2NF, 3NF, BCNF
   - Document functional dependencies
   - Decompose tables step-by-step

2. **CourseDB-AI Schema Analysis**
   - Evaluate each table for normal forms
   - Identify intentional denormalization
   - Understand design trade-offs
   - Document findings

3. **Normalization Reference Guide**
   - Summary of all normal forms
   - Decision flowchart for normalization
   - Common patterns and anti-patterns
   - When to denormalize

4. **Reflection on Design Trade-offs**
   - When to normalize vs denormalize
   - Performance vs integrity trade-offs
   - Real-world normalization decisions

---

## ✅ Self-Check Quiz

Test your understanding before moving to Week 5:

1. **What are the three types of data anomalies?**
   - Update: _______
   - Delete: _______
   - Insert: _______

2. **What is a functional dependency?**
   - Answer: _______

3. **What is the rule for 1NF?**
   - Answer: _______

4. **What is the rule for 2NF?**
   - Answer: _______

5. **What is the rule for 3NF?**
   - Answer: _______

6. **What is the rule for BCNF?**
   - Answer: _______

7. **What is a partial dependency? Give an example.**
   - Answer: _______

8. **What is a transitive dependency? Give an example.**
   - Answer: _______

9. **When is denormalization acceptable?**
   - Answer: _______

10. **Is CourseDB-AI fully normalized? Why or why not?**
    - Answer: _______

---

## 🎓 CourseDB-AI Normalization Analysis

### **Current Schema:**

**courses(course_id, course_code, title, description, credits)**
- Primary Key: course_id
- FDs: course_id → all attributes
- Normal Form: **3NF ✅** (no partial or transitive dependencies)

**topics(topic_id, course_id, topic_name, order_index)**
- Primary Key: topic_id
- FDs: topic_id → all attributes
- Normal Form: **3NF ✅**

**questions(question_id, course_id, topic_id, question_text, difficulty, marks, year)**
- Primary Key: question_id
- FDs: question_id → all attributes
- **Denormalization:** course_id is redundant (can derive from topic_id → course_id)
- Normal Form: **2NF** (intentional denormalization for performance)
- **Design Decision:** Faster queries at cost of redundancy

**resources(resource_id, course_id, title, resource_type, url)**
- Primary Key: resource_id
- FDs: resource_id → all attributes
- Normal Form: **3NF ✅**

**resource_chunks(chunk_id, resource_id, chunk_number, chunk_text, embedding)**
- Primary Key: chunk_id
- FDs: chunk_id → all attributes
- Normal Form: **3NF ✅**

**users(user_id, username, email, role, created_at)**
- Primary Key: user_id
- FDs: user_id → all attributes
- Normal Form: **3NF ✅**

**search_logs(log_id, user_id, question_id, search_query, timestamp)**
- Primary Key: log_id
- FDs: log_id → all attributes
- Normal Form: **3NF ✅**

### **Summary:**
- Most tables in 3NF ✅
- One intentional denormalization (questions.course_id) for performance
- No update anomalies (application enforces consistency)
- Trade-off: Query performance > Storage efficiency

---

## 🔗 Additional Resources

### **Practice Datasets:**
- University (students, courses, enrollments)
- E-commerce (products, orders, customers)
- Hospital (patients, doctors, appointments)
- Library (books, members, loans)

### **Normalization Tools:**
- Database design tools with normalization checkers
- FD analysis tools
- Schema validators

---

## 📝 Study Tips

1. **Start with anomalies** - Understand WHY normalization matters
2. **Master functional dependencies** - Foundation of all normal forms
3. **Apply rules step-by-step** - Don't skip 1NF → 2NF → 3NF
4. **Practice decomposition** - Break tables into smaller, better tables
5. **Understand trade-offs** - Normalization isn't always the answer
6. **Analyze real schemas** - Look at CourseDB-AI, open-source projects
7. **Question everything** - "Why is this table designed this way?"

---

## 🚀 Connection to Later Weeks

**Week 5: PostgreSQL + FastAPI**
- Normalized schemas → SQLAlchemy models
- Foreign key relationships → ORM configuration
- Constraints enforce normalization rules

**Week 6: Advanced SQL**
- JOINs needed for normalized data
- Aggregates across multiple tables
- Views can denormalize for reporting

**Week 7: Indexing**
- Normalized schemas → more indexes needed
- Foreign keys must be indexed
- Query patterns inform normalization decisions

**Week 8: Query Optimization**
- Too much normalization → expensive JOINs
- Denormalization for performance
- Balance normalization vs speed

---

## 🎯 Week 4 Success Criteria

You've successfully completed Week 4 if you can:

✅ Identify all three types of anomalies in a given schema
✅ Determine functional dependencies for any table
✅ Apply 1NF, 2NF, 3NF, BCNF rules correctly
✅ Decompose tables to eliminate anomalies
✅ Explain CourseDB-AI's normalization decisions
✅ Decide when denormalization is appropriate
✅ Understand the trade-offs between normalization and performance

**Ready to begin?** Start with Day 1 in `implementation_plan.md`!

**Questions?** Review `theory_notes.md` and `mistakes_to_expect.md`

---

**Next Week**: Week 5 - PostgreSQL + FastAPI Foundation - Build the backend from your normalized schemas!

# Week 4: Normalization - Theory Notes

## 📚 Core Concepts

### 1. What is Normalization?

**Normalization** is the process of organizing database tables to:
- **Reduce redundancy** (no duplicate data)
- **Eliminate anomalies** (prevent update/delete/insert problems)
- **Ensure data integrity** (maintain consistency)

**Why Normalize?**
- Save storage space
- Maintain data consistency
- Prevent anomalies
- Improve query performance (in most cases)

---

### 2. Data Anomalies (Problems of Bad Design)

#### **Update Anomaly**
Changing data in one place requires changing it in multiple places.

**Example:**
```
questions(question_id, course_code, course_title, question_text)
1, CS201, Database Management Systems, "What is DBMS?"
2, CS201, Database Management Systems, "Explain SQL"
```
If we rename the course, we must update ALL rows with CS201!

#### **Deletion Anomaly**
Deleting one piece of information loses other information.

**Example:**
If we delete the last question for CS301, we lose all information about CS301 course.

#### **Insertion Anomaly**
Cannot insert data without other unrelated data.

**Example:**
Cannot add a new course unless there's at least one question for it.

---

### 3. Functional Dependencies (FD)

**Definition**: X → Y means "X determines Y" or "Y depends on X"

**Examples:**
- student_id → name, age, major (student ID determines all student attributes)
- course_code → course_title, credits (course code determines course details)
- question_id → question_text, year, difficulty

**Types of FDs:**
1. **Full FD**: Y depends on ALL of X (not just part)
2. **Partial FD**: Y depends on PART of X
3. **Transitive FD**: X → Y and Y → Z, so X → Z

---

### 4. Keys and Functional Dependencies

**Candidate Key**: Minimal set of attributes that uniquely identifies a tuple
- Example: student_id is a candidate key for Student
- Example: (student_id, course_id) is candidate key for Enrollment

**Primary Key**: Chosen candidate key

**Non-prime Attribute**: Attribute NOT part of any candidate key

---

### 5. Normal Forms

#### **1NF (First Normal Form)**

**Rule**: Each cell contains atomic (single) values, no repeating groups

**Violation Example:**
```
students(student_id, name, courses)
1, Alice, "CS201, CS202, CS301"  ← BAD: comma-separated values
```

**Fixed (1NF):**
```
enrollments(student_id, course_id)
1, CS201
1, CS202
1, CS301
```

---

#### **2NF (Second Normal Form)**

**Rule**: Must be in 1NF AND no partial dependencies

**Applies to**: Tables with composite keys

**Violation Example:**
```
enrollments(student_id, course_id, student_name, course_title, grade)
PK: (student_id, course_id)

FDs:
- student_id → student_name  ← PARTIAL (depends on part of key)
- course_id → course_title   ← PARTIAL
```

**Fixed (2NF):**
```
students(student_id, student_name)
courses(course_id, course_title)
enrollments(student_id, course_id, grade)
```

---

#### **3NF (Third Normal Form)**

**Rule**: Must be in 2NF AND no transitive dependencies

**Violation Example:**
```
questions(question_id, course_id, course_code, course_title, question_text)

FDs:
- question_id → course_id
- course_id → course_code    ← TRANSITIVE
- course_id → course_title   ← TRANSITIVE
```

**Fixed (3NF):**
```
courses(course_id, course_code, course_title)
questions(question_id, course_id, question_text)
```

---

#### **BCNF (Boyce-Codd Normal Form)**

**Rule**: For every FD X → Y, X must be a superkey

**Stricter than 3NF**: Removes remaining anomalies

**Violation Example:**
```
course_instructors(course_id, instructor_id, instructor_office)
FDs:
- (course_id, instructor_id) → instructor_office
- instructor_id → instructor_office  ← Violates BCNF (instructor_id not a key)
```

**Fixed (BCNF):**
```
instructors(instructor_id, instructor_office)
course_instructors(course_id, instructor_id)
```

---

### 6. Normalization Process

**Step-by-Step:**
1. **Identify all FDs** in the table
2. **Find candidate keys**
3. **Check for 1NF** (atomic values)
4. **Check for 2NF** (no partial dependencies)
5. **Check for 3NF** (no transitive dependencies)
6. **Check for BCNF** (all determinants are keys)
7. **Decompose** as needed

---

### 7. Denormalization (When to Break Rules)

Sometimes we intentionally violate normal forms for:
- **Performance**: Reduce JOINs
- **Simplicity**: Easier queries
- **Read-heavy workloads**: Optimize for SELECT

**Example in CourseDB-AI:**
```sql
questions(
    question_id,
    course_id,
    course_code,  -- REDUNDANT (denormalized)
    topic_name,   -- REDUNDANT (denormalized)
    question_text
)
```

**Trade-off**: Faster queries, but update anomalies possible.

---

## 🎯 CourseDB-AI Normalization

### Before (Week 2 Schema - Denormalized):
```sql
questions(
    question_id,
    course_id,
    topic_id,
    course_code,    -- REDUNDANT
    topic_name,     -- REDUNDANT
    question_text,
    year,
    difficulty
)
```

### After (Week 4 - Normalized to 3NF):
```sql
courses(course_id, course_code, course_title)
topics(topic_id, course_id, topic_name)
questions(question_id, course_id, topic_id, question_text, year, difficulty)
```

**Benefits:**
- No update anomalies
- Single source of truth
- Data consistency guaranteed

---

## ✅ Self-Check Questions

1. What's the difference between 2NF and 3NF?
2. Can a table in 3NF violate BCNF?
3. What's a transitive dependency? Give an example.
4. When would you intentionally denormalize?
5. What's the difference between partial and full functional dependency?
6. How do you identify candidate keys?
7. What problems does normalization solve?

---

## 🔗 Armstrong's Axioms (Advanced)

**Reflexivity**: If Y ⊆ X, then X → Y
**Augmentation**: If X → Y, then XZ → YZ
**Transitivity**: If X → Y and Y → Z, then X → Z

**Derived Rules:**
- **Union**: If X → Y and X → Z, then X → YZ
- **Decomposition**: If X → YZ, then X → Y and X → Z

---

**Next Steps:**
- Analyze Week 2 schema for normalization issues
- Create normalized schema (3NF/BCNF)
- Document functional dependencies
- Complete Week 4 deliverables

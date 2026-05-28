# Week 3: ER Modeling - Theory Notes

## 📚 Core Concepts

### 1. What is ER Modeling?

**Entity-Relationship (ER) Modeling** is a visual approach to database design that uses diagrams to represent:
- **Entities**: Things or objects (Student, Course, Professor)
- **Attributes**: Properties of entities (name, age, GPA)
- **Relationships**: Connections between entities (Student *enrolls in* Course)

**Why ER Modeling?**
- Visual representation easier to understand than SQL
- Helps identify entities and relationships before coding
- Facilitates communication with stakeholders
- Prevents design mistakes early

---

### 2. Entities

**Entity**: A distinguishable object or thing in the real world

**Examples:**
- **Strong Entity**: Exists independently (Student, Course, Professor)
- **Weak Entity**: Depends on another entity (Dependent of Employee)

**ER Diagram Notation:**
- Rectangle = Entity
- Double Rectangle = Weak Entity

---

### 3. Attributes

**Types of Attributes:**

1. **Simple**: Cannot be divided (age, email)
2. **Composite**: Can be divided (name → first_name, last_name)
3. **Derived**: Calculated from other attributes (age from birth_date)
4. **Multivalued**: Multiple values (phone_numbers, skills)

**Key Attributes:**
- **Primary Key**: Uniquely identifies entity (student_id)
- **Partial Key**: Used in weak entities (dependent_name)

**ER Diagram Notation:**
- Oval = Attribute
- Underlined = Primary Key
- Dashed Oval = Derived Attribute
- Double Oval = Multivalued Attribute

---

### 4. Relationships

**Relationship**: Association between entities

**Examples:**
- Student *enrolls in* Course
- Professor *teaches* Course
- Student *takes* Exam

**Relationship Attributes**: Sometimes relationships have attributes
- Example: Enrollment(student, course, **grade**, **semester**)

**ER Diagram Notation:**
- Diamond = Relationship
- Lines connect entities to relationships

---

### 5. Cardinality Ratios

**Cardinality** specifies how many instances of one entity relate to instances of another.

#### **1:1 (One-to-One)**
- One entity instance relates to exactly one instance of another
- Example: Person → Passport (each person has one passport)

#### **1:N (One-to-Many)**
- One entity instance relates to many instances of another
- Example: Professor → Courses (one professor teaches many courses)
- Example: Course → Questions (one course has many questions)

#### **M:N (Many-to-Many)**
- Multiple instances relate to multiple instances
- Example: Student ↔ Course (students enroll in many courses, courses have many students)
- **Implementation**: Requires junction table

**ER Diagram Notation:**
- 1, N, M written on relationship lines

---

### 6. Participation Constraints

**Total Participation** (double line): Every entity must participate
- Example: Every Course *must* belong to a Department

**Partial Participation** (single line): Not all entities must participate
- Example: Not every Professor *must* teach a Course (e.g., on sabbatical)

---

### 7. Weak Entities

**Weak Entity**: Cannot exist without a strong entity

**Example:**
- Dependent (weak) depends on Employee (strong)
- Section (weak) depends on Course (strong)

**Properties:**
- Has partial key (not globally unique)
- Identifies uniquely only within the strong entity
- Represented with double rectangle

**Identifying Relationship**: Connects weak to strong entity (double diamond)

---

### 8. Mapping ER to Relational Schema

#### **Rule 1: Strong Entity → Table**
```
Entity: Student(student_id, name, age, major)
→ Table: students(student_id PK, name, age, major)
```

#### **Rule 2: 1:1 Relationship**
Add foreign key to either side
```
Person(1) ← has → (1) Passport
→ passports(passport_id PK, person_id FK, issue_date)
```

#### **Rule 3: 1:N Relationship**
Add foreign key on the "many" side
```
Course(1) ← has → (N) Question
→ questions(question_id PK, course_id FK, question_text)
```

#### **Rule 4: M:N Relationship**
Create junction table
```
Student(M) ← enrolls → (N) Course
→ enrollments(student_id FK, course_id FK, grade, semester)
   PK: (student_id, course_id)
```

#### **Rule 5: Weak Entity**
Include foreign key to strong entity + partial key
```
Employee(1) ← has → (N) Dependent
→ dependents(employee_id FK, dependent_name, relationship)
   PK: (employee_id, dependent_name)
```

---

## 🎯 CourseDB-AI ER Design

### Entities for CourseDB-AI:
1. **Course**: Stores course information
2. **Topic**: Course topics/chapters
3. **Question**: Previous year questions
4. **Resource**: Notes, textbooks, papers
5. **ResourceChunk**: Text chunks for embeddings
6. **User**: System users

### Relationships:
- Course (1) → (N) Topic
- Course (1) → (N) Question
- Topic (1) → (N) Question
- Resource (1) → (N) ResourceChunk
- User (1) → (N) SearchLog

---

## ✅ Self-Check Questions

1. What's the difference between a strong entity and a weak entity?
2. How do you represent a 1:N relationship in SQL?
3. How do you implement an M:N relationship?
4. What's the difference between total and partial participation?
5. When should you use a composite attribute vs separate attributes?
6. How do you identify weak entities in a problem statement?
7. What's a junction table and when do you need one?

---

## 🔗 Next Steps

- Create ER diagram for CourseDB-AI
- Map ER diagram to SQL tables
- Identify all relationships and cardinalities
- Complete Week 3 deliverables

**Next Week (Week 4)**: Normalization - we'll learn how to identify and fix design problems!

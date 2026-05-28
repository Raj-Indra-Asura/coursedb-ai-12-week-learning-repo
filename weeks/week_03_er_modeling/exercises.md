# Week 3: ER Modeling Exercises

## 🎯 Exercise Goals

These exercises will help you:
- Practice identifying entities and attributes
- Determine relationships and cardinality
- Draw ER diagrams with correct notation
- Map ER diagrams to SQL schemas
- Design a complete database from scratch

---

## Exercise Set 1: Entity and Attribute Identification

### Exercise 1.1: Identify Entities

**Problem Statement:**
"A university wants to track students, courses, professors, and departments. Students enroll in courses. Professors teach courses and belong to departments. Each course is offered by one department."

**Tasks:**
1. List all entities: _______
2. For each entity, list 4-5 attributes
3. Identify the primary key for each entity
4. Mark which attributes should be NOT NULL

**Expected Entities:**
- Student: _______
- Course: _______
- Professor: _______
- Department: _______

### Exercise 1.2: Strong vs Weak Entities

Identify whether each entity is strong or weak:

1. **Employee** and **Dependent** (employee's family member)
   - Employee: Strong / Weak
   - Dependent: Strong / Weak
   - Why? _______

2. **Building** and **Room**
   - Building: Strong / Weak
   - Room: Strong / Weak
   - Why? _______

3. **Course** and **CourseSection** (specific offering like "Fall 2023 Section 1")
   - Course: Strong / Weak
   - CourseSection: Strong / Weak
   - Why? _______

### Exercise 1.3: Attribute Types

Classify each attribute as Simple, Composite, Derived, or Multivalued:

1. `phone_numbers` (a person can have multiple): _______
2. `age` (calculated from birth_date): _______
3. `address` (can be split into street, city, zip): _______
4. `email`: _______
5. `full_name` (first_name + last_name): _______
6. `total_credits` (sum of course credits): _______
7. `skills` (programming languages known): _______

---

## Exercise Set 2: Relationships and Cardinality

### Exercise 2.1: Determine Cardinality

For each relationship, determine the cardinality (1:1, 1:N, or M:N):

1. **Person → Passport**
   - Cardinality: _______
   - Explanation: _______

2. **Department → Employee**
   - Cardinality: _______
   - Explanation: _______

3. **Student → Course** (enrollment)
   - Cardinality: _______
   - Explanation: _______

4. **Author → Book** (co-authorship allowed)
   - Cardinality: _______
   - Explanation: _______

5. **Country → Capital City**
   - Cardinality: _______
   - Explanation: _______

### Exercise 2.2: CourseDB-AI Relationships

For CourseDB-AI, determine the cardinality for each relationship:

1. **Course → Topic**
   - Cardinality: _______
   - Can a topic belong to multiple courses? _______

2. **Topic → Question**
   - Cardinality: _______
   - Can a question belong to multiple topics? _______

3. **Course → Question**
   - Cardinality: _______
   - Direct or indirect relationship? _______

4. **Resource → ResourceChunk**
   - Cardinality: _______
   - Can a chunk belong to multiple resources? _______

5. **User → Question** (via search logs)
   - Cardinality: _______
   - How would you implement this? _______

### Exercise 2.3: Participation Constraints

Determine if participation is Total or Partial:

1. **Course → Department**
   - Must every course belong to a department? Total / Partial
   - Must every department have courses? Total / Partial

2. **Employee → Project**
   - Must every employee work on a project? Total / Partial
   - Must every project have employees? Total / Partial

3. **Question → Topic** (in CourseDB-AI)
   - Must every question belong to a topic? Total / Partial
   - Must every topic have questions? Total / Partial

---

## Exercise Set 3: ER Diagram Drawing

### Exercise 3.1: Simple Library System

**Problem Statement:**
"A library has books and members. Members can borrow books. Each book has a title, ISBN, author, and publication year. Each member has a member_id, name, email, and join_date. Track which member borrowed which book and the due date."

**Tasks:**
1. Draw the ER diagram (on paper or digital tool)
2. Include entities with attributes (underline primary keys)
3. Show the relationship with cardinality
4. Does the relationship have attributes? If yes, what are they?

**Hints:**
- How many books can a member borrow? (Multiple)
- Can a book be borrowed by multiple members? (Yes, but not simultaneously - track with timestamp)
- Is this 1:N or M:N? (M:N - needs junction table)

### Exercise 3.2: E-Commerce System

**Problem Statement:**
"An e-commerce platform has customers, products, and orders. Customers place orders. Each order contains multiple products. Track product quantity in each order and order date."

**Tasks:**
1. Identify all entities: _______
2. Determine relationships and cardinality:
   - Customer → Order: _______
   - Order → Product: _______
3. Draw the complete ER diagram
4. What is the primary key of the junction table? _______

### Exercise 3.3: CourseDB-AI Complete ER Diagram

**Problem Statement:**
Design the complete ER diagram for CourseDB-AI with the following requirements:

**Entities:**
- Course (course_id, course_code, title, description, credits)
- Topic (topic_id, topic_name, order_index)
- Question (question_id, question_text, difficulty, marks, year)
- Resource (resource_id, title, resource_type, url)
- ResourceChunk (chunk_id, chunk_number, chunk_text, embedding)
- User (user_id, username, email, role)

**Requirements:**
- Courses have multiple topics
- Topics have multiple questions
- Questions belong to one topic and one course
- Resources belong to courses
- Resources are split into chunks
- Track which users search which questions (with timestamp and query)

**Tasks:**
1. Draw the complete ER diagram
2. Label all relationships with cardinality
3. Mark primary keys (underline)
4. Identify any weak entities
5. Show foreign key placements

**Validation Questions:**
- Can you query: "Get all questions for a course"? (Yes/No)
- Can you query: "Get all topics for a course"? (Yes/No)
- Can you query: "Find most searched questions"? (Yes/No)
- Can you query: "Get all chunks for a resource"? (Yes/No)

---

## Exercise Set 4: Mapping ER to SQL

### Exercise 4.1: 1:N Relationship

**ER Diagram:**
```
Department (1) → (N) Employee
- Department: dept_id (PK), dept_name, location
- Employee: emp_id (PK), emp_name, salary
```

**Task:** Write the CREATE TABLE statements with foreign key constraints.

```sql
CREATE TABLE departments (
    -- Your solution here
);

CREATE TABLE employees (
    -- Your solution here
    -- Include foreign key to departments
);
```

### Exercise 4.2: M:N Relationship

**ER Diagram:**
```
Student (M) ↔ (N) Course
- Student: student_id (PK), name, major
- Course: course_id (PK), title, credits
- Enrollment attributes: grade, semester, enrollment_date
```

**Task:** Write CREATE TABLE statements for all three tables (including junction table).

```sql
CREATE TABLE students (
    -- Your solution here
);

CREATE TABLE courses (
    -- Your solution here
);

CREATE TABLE enrollments (
    -- Your junction table here
    -- Composite primary key (student_id, course_id)
    -- Foreign keys to both tables
    -- Enrollment attributes
);
```

### Exercise 4.3: Weak Entity

**ER Diagram:**
```
Employee (1) → (N) Dependent (weak entity)
- Employee: emp_id (PK), name, salary
- Dependent: dependent_name (partial key), relationship, birth_date
```

**Task:** Write CREATE TABLE statements.

```sql
CREATE TABLE employees (
    -- Your solution here
);

CREATE TABLE dependents (
    -- Your solution here
    -- Composite PK: (emp_id, dependent_name)
    -- Foreign key with ON DELETE CASCADE
);
```

### Exercise 4.4: CourseDB-AI Schema

Map your CourseDB-AI ER diagram to complete SQL schema:

```sql
-- Course table
CREATE TABLE courses (
    -- Your solution here
);

-- Topic table (references courses)
CREATE TABLE topics (
    -- Your solution here
);

-- Question table (references courses and topics)
CREATE TABLE questions (
    -- Your solution here
);

-- Resource table (references courses)
CREATE TABLE resources (
    -- Your solution here
);

-- ResourceChunk table (references resources)
CREATE TABLE resource_chunks (
    -- Your solution here
);

-- User table
CREATE TABLE users (
    -- Your solution here
);

-- SearchLog junction table (M:N between users and questions)
CREATE TABLE search_logs (
    -- Your solution here
    -- Track search_query, timestamp, user_id, question_id
);
```

**Validation:** After creating tables, test with these queries:
1. Get all topics for a specific course
2. Get all questions for a specific topic
3. Count questions per course
4. Find most searched questions
5. Get all chunks for a resource

---

## Exercise Set 5: Design Challenges

### Exercise 5.1: Identify Design Flaws

**Flawed Design:**
```sql
CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    course1 VARCHAR(100),  -- BAD: Multivalued attribute
    course2 VARCHAR(100),
    course3 VARCHAR(100)
);
```

**Problems:**
1. What's wrong with this design? _______
2. What if a student takes 4 courses? _______
3. How would you fix this? _______

**Corrected Design:**
```sql
-- Your solution here (hint: M:N relationship)
```

### Exercise 5.2: Normalize Denormalized Design

**Denormalized Table:**
```sql
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_name VARCHAR(100),
    customer_email VARCHAR(100),  -- Repeated for every order
    customer_address TEXT,        -- Repeated for every order
    product_name VARCHAR(100),
    product_price DECIMAL
);
```

**Problems:**
1. What's repeated unnecessarily? _______
2. What happens when customer email changes? _______
3. How would you redesign this? _______

**Corrected Design (ER approach):**
```
Entities: Customer, Order, Product
Relationships: Customer (1) → (N) Order, Order (M) ↔ (N) Product
Draw ER diagram and map to SQL.
```

### Exercise 5.3: Alternative CourseDB-AI Designs

Consider alternative designs for CourseDB-AI:

**Design A: Questions linked to Topics only**
```
Course → Topic → Question (no direct Course → Question link)
```

**Design B: Questions linked to both Topics and Courses**
```
Course → Topic → Question
Course → Question (redundant direct link)
```

**Questions:**
1. Which design is better? Why? _______
2. What are the trade-offs? _______
3. How do you query "all questions for a course" in each design?
   - Design A: _______
   - Design B: _______
4. Which design is used in the actual CourseDB-AI? _______

---

## Exercise Set 6: Real-World Scenarios

### Exercise 6.1: Hospital Management System

**Requirements:**
- Track patients, doctors, appointments, prescriptions
- Patients schedule appointments with doctors
- Doctors write prescriptions for patients
- Prescriptions include multiple medicines
- Track appointment date, diagnosis, and notes

**Tasks:**
1. List all entities
2. Determine relationships and cardinality
3. Draw complete ER diagram
4. Map to SQL schema
5. Write 5 sample queries to validate design

### Exercise 6.2: Social Media Platform

**Requirements:**
- Users create posts
- Users can follow other users
- Users can like and comment on posts
- Posts can have multiple tags
- Comments can be replies to other comments (nested)

**Tasks:**
1. Identify all entities (including junction tables)
2. Draw ER diagram with cardinality
3. How do you implement "Users follow Users"? (hint: self-referencing M:N)
4. How do you implement nested comments? (hint: self-referencing 1:N)
5. Map to SQL schema

---

## Self-Assessment Checklist

After completing these exercises, verify you can:

- [ ] Identify entities and attributes from problem statements
- [ ] Distinguish between strong and weak entities
- [ ] Classify attributes (simple, composite, derived, multivalued)
- [ ] Determine cardinality (1:1, 1:N, M:N) for relationships
- [ ] Understand participation constraints (total vs partial)
- [ ] Draw ER diagrams with correct notation
- [ ] Map strong entities to tables
- [ ] Map 1:N relationships using foreign keys
- [ ] Map M:N relationships using junction tables
- [ ] Map weak entities with composite keys
- [ ] Write CREATE TABLE statements from ER diagrams
- [ ] Validate designs with sample queries
- [ ] Identify and fix design flaws

---

## Solutions and Hints

### Exercise 1.1 Hints:
- **Student**: student_id (PK), name, email, major, enrollment_year
- **Course**: course_id (PK), course_code, title, credits, department_id (FK)
- **Professor**: prof_id (PK), name, email, office, department_id (FK)
- **Department**: dept_id (PK), dept_name, building

### Exercise 2.1 Hints:
1. Person → Passport: **1:1** (each person has one passport)
2. Department → Employee: **1:N** (one department has many employees)
3. Student → Course: **M:N** (students take multiple courses, courses have multiple students)
4. Author → Book: **M:N** (authors write multiple books, books can have multiple authors)
5. Country → Capital City: **1:1** (each country has one capital)

### Exercise 4.2 Solution:
```sql
CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    major VARCHAR(100)
);

CREATE TABLE courses (
    course_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    credits INTEGER
);

CREATE TABLE enrollments (
    student_id INTEGER,
    course_id INTEGER,
    grade VARCHAR(2),
    semester VARCHAR(10),
    enrollment_date DATE DEFAULT CURRENT_DATE,
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE
);
```

---

## Additional Practice

For more practice, design ER diagrams for:
1. **Netflix-like streaming service** (users, movies, subscriptions, watch history)
2. **Food delivery app** (customers, restaurants, menu items, orders, delivery drivers)
3. **Online learning platform** (students, instructors, courses, lessons, quizzes)
4. **Banking system** (customers, accounts, transactions, loans, credit cards)
5. **Airline reservation system** (passengers, flights, bookings, aircraft, crew)

---

**Next Steps:** After completing exercises, move to `implementation_plan.md` for the 7-day guided implementation!

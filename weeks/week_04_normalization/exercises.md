# Week 4: Normalization Exercises

## 🎯 Exercise Goals

These exercises will help you:
- Identify data anomalies in table designs
- Understand functional dependencies
- Apply normalization rules (1NF, 2NF, 3NF, BCNF)
- Decompose tables to eliminate redundancy
- Make trade-off decisions about normalization

---

## Exercise Set 1: Identify Anomalies

### Exercise 1.1: Update Anomaly

**Given table:**
```
student_courses(student_id, student_name, course_id, course_title, instructor, grade)
101, Alice, CS201, Database Systems, Dr. Smith, A
101, Alice, CS202, Data Structures, Dr. Jones, B
102, Bob, CS201, Database Systems, Dr. Smith, A
```

**Tasks:**
1. What happens if Alice changes her name to "Alice Johnson"?
2. How many rows need to be updated?
3. What could go wrong if we miss updating one row?
4. Identify the update anomaly.

**Solution:**
```
Problem: student_name is repeated for every course Alice takes.
Update: Must change "Alice" to "Alice Johnson" in 2 rows.
Risk: If we miss one row, Alice has two different names (inconsistency).
Anomaly: Update anomaly - changing student name requires multiple updates.
```

### Exercise 1.2: Delete Anomaly

**Given table:**
```
course_instructors(course_id, course_title, credits, instructor_id, instructor_name)
CS201, Database Systems, 3, 501, Dr. Smith
CS202, Data Structures, 3, 502, Dr. Jones
```

**Tasks:**
1. What happens if Dr. Jones stops teaching CS202 and we delete that row?
2. What information is lost?
3. Identify the delete anomaly.

**Solution:**
```
Problem: If we delete the CS202 row, we lose ALL information about:
- CS202 course exists
- Dr. Jones is an instructor
Delete Anomaly: Deleting one fact loses other unrelated facts.
```

### Exercise 1.3: Insert Anomaly

**Given table:**
```
question_topics(question_id, question_text, topic_id, topic_name, course_id, course_title)
```

**Tasks:**
1. Can we add a new course "CS301: Operating Systems" without questions?
2. Can we add a new topic "Process Management" without questions?
3. Identify the insert anomaly.

**Solution:**
```
Problem: Cannot insert course or topic without at least one question.
Insert Anomaly: Cannot add data without having other unrelated data.
```

---

## Exercise Set 2: Functional Dependencies

### Exercise 2.1: Identify Functional Dependencies

**Given table:**
```
students(student_id, student_name, email, dept_id, dept_name, dept_building)
```

**Tasks:**
List all functional dependencies (X → Y):

1. student_id → ?
2. dept_id → ?
3. email → ?
4. Any transitive dependencies?

**Solution:**
```
student_id → student_name, email, dept_id, dept_name, dept_building
dept_id → dept_name, dept_building
email → student_id (assuming email is unique)

Transitive:
student_id → dept_id → dept_name
student_id → dept_id → dept_building
```

### Exercise 2.2: Partial vs Full Dependencies

**Given table:**
```
enrollments(student_id, course_id, student_name, course_title, grade, semester)
Primary Key: (student_id, course_id)
```

**Tasks:**
Classify each FD as full or partial:

1. (student_id, course_id) → grade
2. (student_id, course_id) → semester
3. student_id → student_name
4. course_id → course_title

**Solution:**
```
(student_id, course_id) → grade         [FULL - depends on both]
(student_id, course_id) → semester      [FULL - depends on both]
student_id → student_name               [PARTIAL - depends on part of key]
course_id → course_title                [PARTIAL - depends on part of key]

Partial dependencies violate 2NF!
```

### Exercise 2.3: Transitive Dependencies

**Given table:**
```
employees(emp_id, emp_name, dept_id, dept_name, manager_id, manager_name)
Primary Key: emp_id
```

**Tasks:**
1. Identify all FDs
2. Find transitive dependencies (X → Y → Z)

**Solution:**
```
Direct FDs:
emp_id → emp_name, dept_id, dept_name, manager_id, manager_name
dept_id → dept_name
manager_id → manager_name

Transitive:
emp_id → dept_id → dept_name    [Transitive - violates 3NF]
emp_id → manager_id → manager_name [Transitive - violates 3NF]
```

---

## Exercise Set 3: Normalize to 1NF

### Exercise 3.1: Multivalued Attribute

**Unnormalized:**
```
students(student_id, name, phone_numbers)
1, Alice, "555-1234, 555-5678"
2, Bob, "555-9999"
```

**Tasks:**
1. Why is this not in 1NF?
2. Convert to 1NF.

**Solution:**
```
Violation: phone_numbers contains multiple values.

1NF Solution:
students(student_id, name)
1, Alice
2, Bob

student_phones(student_id, phone_number)
1, 555-1234
1, 555-5678
2, 555-9999
```

### Exercise 3.2: Repeating Groups

**Unnormalized:**
```
courses(course_id, title, topic1, topic2, topic3, topic4)
CS201, DBMS, SQL, ER Modeling, Normalization, Transactions
CS202, Data Structures, Arrays, Lists, Trees, NULL
```

**Tasks:**
1. Why is this not in 1NF?
2. Convert to 1NF.

**Solution:**
```
Violation: Repeating groups (topic1, topic2, topic3, topic4).

1NF Solution:
courses(course_id, title)
CS201, DBMS
CS202, Data Structures

topics(course_id, topic_name, order_index)
CS201, SQL, 1
CS201, ER Modeling, 2
CS201, Normalization, 3
CS201, Transactions, 4
CS202, Arrays, 1
CS202, Lists, 2
CS202, Trees, 3
```

### Exercise 3.3: Non-Atomic Values

**Unnormalized:**
```
orders(order_id, customer_name, order_date, items)
1, Alice, 2023-01-15, "Laptop:1, Mouse:2, Keyboard:1"
```

**Tasks:**
1. Why is this not in 1NF?
2. Convert to 1NF.

**Solution:**
```
Violation: items column contains structured data (not atomic).

1NF Solution:
orders(order_id, customer_name, order_date)
1, Alice, 2023-01-15

order_items(order_id, product_name, quantity)
1, Laptop, 1
1, Mouse, 2
1, Keyboard, 1
```

---

## Exercise Set 4: Normalize to 2NF

### Exercise 4.1: Eliminate Partial Dependencies

**Table in 1NF but not 2NF:**
```
order_details(order_id, product_id, customer_name, product_name, product_price, quantity, order_date)
Primary Key: (order_id, product_id)
```

**Functional Dependencies:**
```
(order_id, product_id) → quantity
order_id → customer_name, order_date
product_id → product_name, product_price
```

**Tasks:**
1. Identify partial dependencies.
2. Decompose to 2NF.

**Solution:**
```
Partial Dependencies (violate 2NF):
order_id → customer_name, order_date [depends on part of key]
product_id → product_name, product_price [depends on part of key]

2NF Decomposition:
orders(order_id, customer_name, order_date)
products(product_id, product_name, product_price)
order_items(order_id, product_id, quantity)
```

### Exercise 4.2: Practice Problem

**Table:**
```
student_grades(student_id, course_id, student_name, student_major, course_title, credits, grade, semester)
Primary Key: (student_id, course_id, semester)
```

**Tasks:**
1. List all FDs.
2. Identify partial dependencies.
3. Decompose to 2NF.

**Solution:**
```
FDs:
(student_id, course_id, semester) → grade
student_id → student_name, student_major
course_id → course_title, credits

Partial Dependencies:
student_id → student_name, student_major
course_id → course_title, credits

2NF Decomposition:
students(student_id, student_name, student_major)
courses(course_id, course_title, credits)
enrollments(student_id, course_id, semester, grade)
```

---

## Exercise Set 5: Normalize to 3NF

### Exercise 5.1: Eliminate Transitive Dependencies

**Table in 2NF but not 3NF:**
```
employees(emp_id, emp_name, dept_id, dept_name, dept_location)
Primary Key: emp_id
```

**Functional Dependencies:**
```
emp_id → emp_name, dept_id, dept_name, dept_location
dept_id → dept_name, dept_location
```

**Tasks:**
1. Identify transitive dependencies.
2. Decompose to 3NF.

**Solution:**
```
Transitive Dependencies (violate 3NF):
emp_id → dept_id → dept_name
emp_id → dept_id → dept_location

3NF Decomposition:
employees(emp_id, emp_name, dept_id)
departments(dept_id, dept_name, dept_location)
```

### Exercise 5.2: Complex Example

**Table:**
```
books(isbn, title, author_id, author_name, author_country, publisher_id, publisher_name, publisher_city, publication_year)
Primary Key: isbn
```

**Tasks:**
1. List all FDs.
2. Identify transitive dependencies.
3. Decompose to 3NF.

**Solution:**
```
FDs:
isbn → title, author_id, author_name, author_country, publisher_id, publisher_name, publisher_city, publication_year
author_id → author_name, author_country
publisher_id → publisher_name, publisher_city

Transitive:
isbn → author_id → author_name, author_country
isbn → publisher_id → publisher_name, publisher_city

3NF Decomposition:
books(isbn, title, author_id, publisher_id, publication_year)
authors(author_id, author_name, author_country)
publishers(publisher_id, publisher_name, publisher_city)
```

---

## Exercise Set 6: BCNF

### Exercise 6.1: When 3NF is not enough

**Table (in 3NF):**
```
course_faculty(student_id, course_title, instructor_name)
Primary Key: (student_id, course_title)

Constraints:
- Each student takes one instructor per course
- Each instructor teaches only one course (unique)
- Multiple instructors can teach different sections of same course

FDs:
(student_id, course_title) → instructor_name
instructor_name → course_title [PROBLEM!]
```

**Tasks:**
1. Why does instructor_name → course_title violate BCNF?
2. Decompose to BCNF.

**Solution:**
```
Violation: instructor_name → course_title
But instructor_name is NOT a superkey (not a candidate key).

BCNF Decomposition:
student_instructor(student_id, instructor_name)
instructor_course(instructor_name, course_title)
```

---

## Exercise Set 7: CourseDB-AI Schema Analysis

### Exercise 7.1: Evaluate Normalization

**Analyze each CourseDB-AI table:**

**courses(course_id, course_code, title, description, credits)**

Tasks:
1. Primary key: _____
2. Functional dependencies: _____
3. Normal form (1NF/2NF/3NF/BCNF): _____
4. Any anomalies? _____

**Solution:**
```
PK: course_id
FDs: course_id → course_code, title, description, credits
Normal Form: 3NF / BCNF
Anomalies: None - fully normalized
```

**questions(question_id, course_id, topic_id, question_text, difficulty, marks, year)**

Tasks:
1. Primary key: _____
2. Is course_id redundant? _____
3. Functional dependencies: _____
4. Normal form: _____
5. Why is course_id included despite redundancy?

**Solution:**
```
PK: question_id
Redundancy: course_id can be derived from topic_id (topics table)
FDs: question_id → all attributes
       topic_id → course_id (from topics table)
Normal Form: 2NF (intentional denormalization)
Reason: Performance - avoid JOIN to get course_id
Trade-off: Storage redundancy for query speed
```

### Exercise 7.2: Design Alternative

**Fully Normalized Version:**
```
questions(question_id, topic_id, question_text, difficulty, marks, year)
-- Remove course_id
```

**Tasks:**
1. How to query "all questions for course CS201"?
2. Compare with denormalized version.
3. Which design is better? Why?

**Solution:**
```
Normalized Query:
SELECT q.*
FROM questions q
JOIN topics t ON q.topic_id = t.topic_id
WHERE t.course_id = 'CS201'

Denormalized Query:
SELECT *
FROM questions
WHERE course_id = 'CS201'

Comparison:
Normalized: +Saves storage, +No redundancy, -Requires JOIN
Denormalized: +Faster query, +Simpler code, -Redundant data

Decision: Denormalized is better IF:
- "Questions by course" is a frequent query
- Course changes are rare
- Application ensures consistency
```

---

## Exercise Set 8: Real-World Scenarios

### Exercise 8.1: E-Commerce Database

**Design a normalized schema for:**
- Customers place orders
- Orders contain multiple products
- Products have categories
- Track inventory for each product

**Tasks:**
1. Identify entities
2. Determine functional dependencies
3. Create 3NF schema
4. Identify potential denormalization opportunities

**Solution:**
```
3NF Schema:
customers(customer_id, name, email, address)
products(product_id, product_name, price, category_id, stock_quantity)
categories(category_id, category_name)
orders(order_id, customer_id, order_date, total_amount)
order_items(order_id, product_id, quantity, price_at_purchase)

Potential Denormalization:
- Store customer_name in orders table (avoid JOIN for order history)
- Store product_name in order_items (preserve name even if product renamed)
```

### Exercise 8.2: Social Media Platform

**Design for:**
- Users create posts
- Posts have comments
- Users can like posts and comments
- Users follow other users

**Tasks:**
1. Create 3NF schema
2. Identify M:N relationships
3. Consider denormalization for "post with like count"

**Solution:**
```
3NF Schema:
users(user_id, username, email, created_at)
posts(post_id, user_id, content, created_at)
comments(comment_id, post_id, user_id, content, created_at)
post_likes(user_id, post_id, liked_at)
comment_likes(user_id, comment_id, liked_at)
user_follows(follower_id, followee_id, followed_at)

Denormalization Option:
posts(post_id, user_id, content, created_at, like_count)
- Cache like_count in posts table
- Update on each like/unlike
- Trade-off: Faster reads, more complex writes
```

---

## Self-Assessment Checklist

After completing these exercises, verify you can:

- [ ] Identify update, delete, and insert anomalies
- [ ] Determine functional dependencies for any table
- [ ] Recognize partial dependencies (violate 2NF)
- [ ] Recognize transitive dependencies (violate 3NF)
- [ ] Apply 1NF (eliminate repeating groups)
- [ ] Apply 2NF (eliminate partial dependencies)
- [ ] Apply 3NF (eliminate transitive dependencies)
- [ ] Apply BCNF (all determinants are candidate keys)
- [ ] Decompose tables using normalization rules
- [ ] Understand when denormalization is appropriate
- [ ] Analyze production schemas for normalization

---

## Challenge Problems

### Challenge 1: Multi-Step Normalization

**Unnormalized Table:**
```
student_courses(
    student_id, student_name, student_email, student_major,
    course_id, course_title, instructor_name, instructor_office,
    grade, semester, credit_hours
)
```

**Task:** Normalize from unnormalized → 1NF → 2NF → 3NF
Document each step with FDs and decomposition rationale.

### Challenge 2: BCNF Decomposition

Find an example where a table is in 3NF but not BCNF.
Create the scenario, identify the violation, and decompose to BCNF.

### Challenge 3: Denormalization Decision

Given a fully normalized 3NF schema for a blog platform:
- Identify 3 common queries
- Propose denormalization strategies
- Analyze trade-offs for each
- Recommend which to implement

---

**Next Steps:** After completing exercises, move to `implementation_plan.md` for the 7-day guided practice!

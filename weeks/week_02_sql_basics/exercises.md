# Week 2: SQL Exercises

## Exercise Set 1: CREATE TABLE Fundamentals

### Exercise 1.1: Basic Table Creation
Create a simple `students` table with the following attributes:
- student_id (integer, primary key, auto-increment)
- name (text, not null)
- email (text, unique, not null)
- major (text)
- gpa (decimal with 2 places)

**Solution**:
```sql
CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    major TEXT,
    gpa DECIMAL(3,2)
);
```

**Verify**: `\d students` in psql to see structure

---

### Exercise 1.2: Table with Foreign Key
Create an `enrollments` table that links students to courses

**TODO**: Write your solution here

---

## Exercise Set 2: INSERT Operations

Practice inserting data with proper constraints and foreign keys.

---

## Exercise Set 3: SELECT and WHERE

Write queries to find:
1. All questions with difficulty 'medium'
2. Questions with marks >= 8
3. Questions from 2023
4. Questions containing 'SQL' in the text

---

## Exercise Set 4: Joins

Practice combining tables:
- INNER JOIN for matching rows
- LEFT JOIN for all left + matching right
- Multi-table joins

---

## Exercise Set 5: Aggregates

Calculate:
- COUNT, SUM, AVG, MAX, MIN
- GROUP BY with aggregates
- HAVING clause for filtering groups

---

## Self-Assessment

Rate your confidence (1-5):
- [ ] Creating tables with constraints
- [ ] Writing WHERE clauses
- [ ] Using aggregate functions
- [ ] Writing JOIN queries
- [ ] Understanding GROUP BY

**Ready for Week 3?** ☐ Yes ☐ Need more practice

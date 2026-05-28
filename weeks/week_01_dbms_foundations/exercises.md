# Week 1 Exercises: DBMS Foundations

**Objective**: Test understanding of DBMS concepts through hands-on problems

---

## Exercise 1: Data vs Information

Given these raw data points:
- "Alice", 22, "DBMS", 95
- "Bob", 21, "DBMS", 88
- "Carol", 23, "AI", 92

**Your Solution**:

1. What is the data?
   - [Your answer]

2. What information can you derive?
   - [Your answer]

3. What additional context is needed?
   - [Your answer]

---

## Exercise 2: Schema vs Instance

Consider a `students` table:
- Schema: students(student_id, name, age, major)
- Instance at time T1: [(1, "Alice", 22, "CS"), (2, "Bob", 21, "CS")]
- Instance at time T2: [(1, "Alice", 22, "CS"), (2, "Bob", 21, "CS"), (3, "Carol", 23, "AI")]

**Your Solution**:

1. What happens to the schema when you add a new student?
   - [Your answer]

2. What happens to the instance when you add a new student?
   - [Your answer]

3. Can two databases have the same schema but different instances?
   - [Your answer]

---

## Exercise 3: Three-Level Architecture

For CourseDB-AI:

**Your Solution**:

1. **Physical Level**: How might PostgreSQL store question data on disk?
   - [Your answer]

2. **Logical Level**: What tables will we create?
   - [Your answer]

3. **View Level**: What custom views might we create for different users?
   - [Your answer]

---

## Exercise 4: File System Limitations

**Scenario**: Design a file-based system to store:
- Courses (course_code, title, semester)
- Questions (question_text, course_code, difficulty, year)

**Your Solution**:

1. How would you organize the files?
   - [Your answer]

2. What problems arise with data redundancy?
   - [Your answer]

3. What happens when you need to update a course title?
   - [Your answer]

4. How would you efficiently find all "hard" questions from 2023?
   - [Your answer]

5. What happens if two users try to update the same file simultaneously?
   - [Your answer]

---

## Exercise 5: DBMS Benefits

**Your Solution**:

List 5 specific ways a DBMS improves upon file systems:

1. [Benefit 1]
2. [Benefit 2]
3. [Benefit 3]
4. [Benefit 4]
5. [Benefit 5]

---

## Exercise 6: CourseDB-AI Positioning

**Your Solution**:

Explain in 3-4 sentences why CourseDB-AI is "data infrastructure" and not just a "search engine":

[Your explanation]

---

## Self-Assessment

- [ ] I completed all exercises
- [ ] I answered in my own words
- [ ] I understand why each concept matters
- [ ] I can explain these concepts to someone else

---

**Completed**: [Date]

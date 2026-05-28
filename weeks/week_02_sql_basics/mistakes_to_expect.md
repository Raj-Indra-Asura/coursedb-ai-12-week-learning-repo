# Week 2: Common Mistakes to Expect

This document lists the most common SQL mistakes beginners make. Read through this **before** and **during** your Week 2 implementation to avoid frustration.

---

## 🔴 Category 1: Syntax Errors

### Mistake 1.1: Forgetting Semicolons
**What you'll do**:
```sql
SELECT * FROM questions
SELECT * FROM topics
```

**Error message**:
```
ERROR:  syntax error at or near "SELECT"
LINE 2: SELECT * FROM topics
```

**Why it happens**: SQL requires semicolons to terminate statements.

**Fix**:
```sql
SELECT * FROM questions;
SELECT * FROM topics;
```

---

### Mistake 1.2: Missing Commas in Column Lists
**What you'll do**:
```sql
SELECT question_id question_text difficulty
FROM questions;
```

**Error message**:
```
ERROR:  syntax error at or near "question_text"
```

**Fix**:
```sql
SELECT question_id, question_text, difficulty
FROM questions;
```

**Tip**: Always separate column names with commas.

---

### Mistake 1.3: Single Quotes vs Double Quotes
**What you'll do**:
```sql
SELECT * FROM questions WHERE difficulty = "hard";
```

**Error message** (PostgreSQL):
```
ERROR:  column "hard" does not exist
```

**Why it happens**: Double quotes are for identifiers (table/column names), single quotes are for string literals.

**Fix**:
```sql
SELECT * FROM questions WHERE difficulty = 'hard';
```

**Rule**:
- Single quotes `'` for strings
- Double quotes `"` for table/column names (if needed)

---

## 🟠 Category 2: JOIN Mistakes

### Mistake 2.1: Ambiguous Column Names
**What you'll do**:
```sql
SELECT question_id, topic_name
FROM questions
JOIN topics ON topic_id = topic_id;
```

**Error message**:
```
ERROR:  column reference "topic_id" is ambiguous
```

**Why it happens**: Both tables have a `topic_id` column.

**Fix**:
```sql
SELECT q.question_id, t.topic_name
FROM questions q
JOIN topics t ON q.topic_id = t.topic_id;
```

**Best practice**: Always use table aliases in JOINs.

---

### Mistake 2.2: Forgetting JOIN Condition
**What you'll do**:
```sql
SELECT question_text, topic_name
FROM questions, topics;
```

**What happens**: You get a Cartesian product (every question paired with every topic).

**If you have**:
- 50 questions
- 10 topics

**You get**: 50 × 10 = 500 rows (probably not what you want!)

**Fix**:
```sql
SELECT q.question_text, t.topic_name
FROM questions q
JOIN topics t ON q.topic_id = t.topic_id;
```

---

### Mistake 2.3: Using = Instead of IS for NULL
**What you'll do**:
```sql
SELECT * FROM topics t
LEFT JOIN questions q ON t.topic_id = q.topic_id
WHERE q.question_id = NULL;
```

**What happens**: Returns 0 rows (but you expected topics with no questions).

**Why**: NULL is not equal to anything, not even itself.

**Fix**:
```sql
SELECT * FROM topics t
LEFT JOIN questions q ON t.topic_id = q.topic_id
WHERE q.question_id IS NULL;
```

**Rule**: Always use `IS NULL` or `IS NOT NULL`, never `= NULL`.

---

## 🟡 Category 3: WHERE vs HAVING

### Mistake 3.1: Using WHERE After GROUP BY for Aggregates
**What you'll do**:
```sql
SELECT difficulty, COUNT(*) as count
FROM questions
GROUP BY difficulty
WHERE COUNT(*) > 5;
```

**Error message**:
```
ERROR:  syntax error at or near "WHERE"
```

**Why**: WHERE filters rows before grouping; HAVING filters groups after.

**Fix**:
```sql
SELECT difficulty, COUNT(*) as count
FROM questions
GROUP BY difficulty
HAVING COUNT(*) > 5;
```

**Remember**:
- `WHERE` filters individual rows (before GROUP BY)
- `HAVING` filters groups (after GROUP BY)

---

### Mistake 3.2: Using Aggregate in WHERE
**What you'll do**:
```sql
SELECT topic_id, AVG(marks) as avg_marks
FROM questions
WHERE AVG(marks) > 5
GROUP BY topic_id;
```

**Error message**:
```
ERROR:  aggregate functions are not allowed in WHERE
```

**Fix**:
```sql
SELECT topic_id, AVG(marks) as avg_marks
FROM questions
GROUP BY topic_id
HAVING AVG(marks) > 5;
```

---

## 🟢 Category 4: Data Type Mismatches

### Mistake 4.1: Comparing Different Types
**What you'll do**:
```sql
SELECT * FROM questions WHERE marks = '5';
```

**What happens**: Might work (implicit conversion) but inefficient and error-prone.

**Better**:
```sql
SELECT * FROM questions WHERE marks = 5;
```

**Tip**: Match types exactly; don't rely on implicit conversions.

---

### Mistake 4.2: String Concatenation Confusion
**What you'll do**:
```sql
SELECT 'Question ID: ' + question_id FROM questions;
```

**Error** (PostgreSQL):
```
ERROR:  operator does not exist: text + integer
```

**Fix**:
```sql
SELECT 'Question ID: ' || question_id FROM questions;
```

**Rule**: PostgreSQL uses `||` for concatenation, not `+`.

---

## 🔵 Category 5: ORDER BY and LIMIT

### Mistake 5.1: LIMIT Without ORDER BY
**What you'll do**:
```sql
SELECT * FROM questions LIMIT 10;
```

**What happens**: You get 10 random rows (order is not guaranteed).

**Better**:
```sql
SELECT * FROM questions
ORDER BY question_id
LIMIT 10;
```

**Rule**: Always use ORDER BY with LIMIT for predictable results.

---

### Mistake 5.2: Ordering by Non-Selected Columns in GROUP BY
**What you'll do**:
```sql
SELECT difficulty, COUNT(*) as count
FROM questions
GROUP BY difficulty
ORDER BY marks DESC;
```

**Error**:
```
ERROR:  column "questions.marks" must appear in the GROUP BY clause or be used in an aggregate function
```

**Why**: After GROUP BY, you can only reference grouped columns or aggregates.

**Fix**:
```sql
SELECT difficulty, COUNT(*) as count, AVG(marks) as avg_marks
FROM questions
GROUP BY difficulty
ORDER BY avg_marks DESC;
```

---

## 🟣 Category 6: INSERT and UPDATE Mistakes

### Mistake 6.1: Missing Columns in INSERT
**What you'll do**:
```sql
INSERT INTO questions (question_text, difficulty)
VALUES ('What is a primary key?', 'easy', 2023, 5);
```

**Error**:
```
ERROR:  INSERT has more expressions than target columns
```

**Fix**:
```sql
INSERT INTO questions (question_text, difficulty, year, marks)
VALUES ('What is a primary key?', 'easy', 2023, 5);
```

**Rule**: Column list must match value list exactly.

---

### Mistake 6.2: Foreign Key Violation
**What you'll do**:
```sql
INSERT INTO questions (question_text, topic_id, difficulty)
VALUES ('What is ACID?', 9999, 'hard');
```

**Error**:
```
ERROR:  insert or update on table "questions" violates foreign key constraint
DETAIL:  Key (topic_id)=(9999) is not present in table "topics".
```

**Why**: Foreign key constraint ensures topic_id exists in topics table.

**Fix**: Use a valid topic_id:
```sql
-- First, find a valid topic_id
SELECT topic_id FROM topics LIMIT 1;

-- Then insert
INSERT INTO questions (question_text, topic_id, difficulty)
VALUES ('What is ACID?', 1, 'hard');
```

---

### Mistake 6.3: UPDATE Without WHERE
**What you'll do**:
```sql
UPDATE questions SET difficulty = 'hard';
```

**What happens**: **ALL** questions are now 'hard' (probably not what you want!).

**Fix**:
```sql
UPDATE questions
SET difficulty = 'hard'
WHERE question_id = 5;
```

**Warning**: Always use WHERE with UPDATE unless you really want to update all rows.

---

### Mistake 6.4: DELETE Without WHERE
**What you'll do**:
```sql
DELETE FROM questions;
```

**What happens**: **ALL** questions are deleted!

**Fix**:
```sql
DELETE FROM questions WHERE question_id = 5;
```

**Tip**: Test with SELECT first:
```sql
-- Test what will be deleted
SELECT * FROM questions WHERE question_id = 5;

-- Then delete
DELETE FROM questions WHERE question_id = 5;
```

---

## 🟤 Category 7: COUNT Confusion

### Mistake 7.1: COUNT(*) vs COUNT(column)
**What you'll do**:
```sql
SELECT COUNT(difficulty) FROM questions;
```

**What you might expect**: Total number of questions

**What you actually get**: Number of questions with non-NULL difficulty

**Why**: COUNT(column) ignores NULL values.

**Fix**:
```sql
SELECT COUNT(*) FROM questions;  -- Counts all rows including NULLs
```

**Rule**:
- `COUNT(*)` counts all rows
- `COUNT(column)` counts non-NULL values in that column

---

## ⚫ Category 8: Case Sensitivity

### Mistake 8.1: Case-Sensitive String Comparison
**What you'll do**:
```sql
SELECT * FROM questions WHERE difficulty = 'Hard';
```

**What happens**: Returns 0 rows if data is stored as 'hard' (lowercase).

**Fix (case-insensitive)**:
```sql
SELECT * FROM questions WHERE difficulty ILIKE 'hard';
```

**Or**:
```sql
SELECT * FROM questions WHERE LOWER(difficulty) = 'hard';
```

**Rule**: Use `ILIKE` for case-insensitive LIKE, or convert to lowercase.

---

### Mistake 8.2: Quoted Identifiers
**What you'll do**:
```sql
CREATE TABLE "Questions" (id INT);
SELECT * FROM questions;  -- Won't work!
```

**Error**:
```
ERROR:  relation "questions" does not exist
```

**Why**: Double quotes make identifiers case-sensitive.

**Fix**:
```sql
SELECT * FROM "Questions";  -- Must match exact case
```

**Best practice**: Avoid quoted identifiers; use lowercase names.

---

## ⚪ Category 9: Logical Operator Mistakes

### Mistake 9.1: Incorrect AND/OR Logic
**What you want**: Easy or medium questions from 2023

**What you'll do**:
```sql
SELECT * FROM questions
WHERE difficulty = 'easy' OR difficulty = 'medium' AND year = 2023;
```

**What happens**: Gets all easy questions (any year) + medium questions from 2023

**Why**: AND has higher precedence than OR.

**Fix**:
```sql
SELECT * FROM questions
WHERE (difficulty = 'easy' OR difficulty = 'medium') AND year = 2023;
```

**Or use IN**:
```sql
SELECT * FROM questions
WHERE difficulty IN ('easy', 'medium') AND year = 2023;
```

---

### Mistake 9.2: Using OR Instead of IN
**What you'll do**:
```sql
SELECT * FROM questions
WHERE difficulty = 'easy' OR 'medium' OR 'hard';
```

**Error**:
```
ERROR:  argument of OR must be type boolean
```

**Fix**:
```sql
SELECT * FROM questions
WHERE difficulty IN ('easy', 'medium', 'hard');
```

---

## 🎯 Prevention Checklist

Before running any query, check:

- [ ] All statements end with semicolons
- [ ] String values use single quotes
- [ ] All column names in SELECT have commas
- [ ] JOINs have ON conditions
- [ ] Table aliases used for ambiguous columns
- [ ] NULL checked with IS NULL, not = NULL
- [ ] Aggregates use HAVING, not WHERE
- [ ] UPDATE and DELETE have WHERE clauses
- [ ] COUNT(*) vs COUNT(column) used correctly
- [ ] LIMIT has ORDER BY for predictable results

---

## 🔧 Debugging Strategies

### Strategy 1: Test with SELECT First
Before UPDATE or DELETE:
```sql
-- First, see what will be affected
SELECT * FROM questions WHERE question_id = 5;

-- Then execute
UPDATE questions SET difficulty = 'hard' WHERE question_id = 5;
```

---

### Strategy 2: Build Queries Incrementally
Start simple, add complexity:
```sql
-- Step 1: Basic SELECT
SELECT * FROM questions;

-- Step 2: Add WHERE
SELECT * FROM questions WHERE difficulty = 'hard';

-- Step 3: Add JOIN
SELECT q.*, t.topic_name
FROM questions q
JOIN topics t ON q.topic_id = t.topic_id
WHERE q.difficulty = 'hard';

-- Step 4: Add ORDER and LIMIT
SELECT q.*, t.topic_name
FROM questions q
JOIN topics t ON q.topic_id = t.topic_id
WHERE q.difficulty = 'hard'
ORDER BY q.marks DESC
LIMIT 10;
```

---

### Strategy 3: Use EXPLAIN for Performance Issues
```sql
EXPLAIN SELECT * FROM questions WHERE difficulty = 'hard';
```

Shows how PostgreSQL executes the query (preview of Week 8).

---

## 📚 Resources for Error Messages

When you get an error:

1. **Read the error carefully**: Line number and exact problem are usually specified.
2. **Google the error code**: PostgreSQL error codes are well-documented.
3. **Check PostgreSQL docs**: https://www.postgresql.org/docs/current/errcodes-appendix.html
4. **Ask specific questions**: Include exact error message and query.

---

## 🚀 Moving Forward

**Don't be discouraged by errors!**

Every SQL developer makes these mistakes. The key is:
- Learn from each error
- Build mental checklists
- Test queries incrementally
- Use transactions when making changes (Week 9)

**Remember**: Errors are part of the learning process. Week 2 is about building SQL muscle memory.

---

**Last updated**: Week 2 curriculum

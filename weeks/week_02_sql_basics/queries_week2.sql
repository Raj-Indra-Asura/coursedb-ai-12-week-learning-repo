-- Week 2: SQL Basics - Practice Queries
-- 20 SQL exercises to master SELECT, WHERE, ORDER BY, GROUP BY, HAVING, and aggregates

-- ===========================================
-- SECTION 1: Basic SELECT and WHERE (5 queries)
-- ===========================================

-- Query 1: List all courses
-- Learning: Basic SELECT
SELECT * FROM courses;

-- Query 2: Find all questions from year 2023
-- Learning: WHERE clause with equality
SELECT question_id, question_text, year, difficulty
FROM questions
WHERE year = 2023;

-- Query 3: Find all "hard" difficulty questions
-- Learning: WHERE with string comparison
SELECT question_id, question_text, difficulty, marks
FROM questions
WHERE difficulty = 'hard';

-- Query 4: Find all questions worth more than 5 marks
-- Learning: WHERE with numeric comparison
SELECT question_id, question_text, marks, year
FROM questions
WHERE marks > 5;

-- Query 5: Find all midterm exams from 2022 or 2023
-- Learning: WHERE with OR and IN
SELECT question_text, year, exam_type
FROM questions
WHERE exam_type = 'midterm' AND year IN (2022, 2023);


-- ===========================================
-- SECTION 2: Sorting and Pattern Matching (5 queries)
-- ===========================================

-- Query 6: List all questions ordered by year (newest first)
-- Learning: ORDER BY DESC
SELECT question_id, question_text, year, difficulty
FROM questions
ORDER BY year DESC;

-- Query 7: Find questions about "normalization" (case-insensitive)
-- Learning: LIKE pattern matching with ILIKE (PostgreSQL)
SELECT question_text, topic_name, year
FROM questions
WHERE question_text ILIKE '%normalization%';

-- Query 8: List all topics, sorted alphabetically
-- Learning: ORDER BY with text
SELECT topic_name, description, week_number
FROM topics
ORDER BY topic_name ASC;

-- Query 9: Find all questions containing "SQL" or "query"
-- Learning: OR with LIKE
SELECT question_text, year, difficulty
FROM questions
WHERE question_text ILIKE '%SQL%' OR question_text ILIKE '%query%';

-- Query 10: Find the 5 most valuable questions (highest marks)
-- Learning: ORDER BY with LIMIT
SELECT question_text, marks, difficulty
FROM questions
ORDER BY marks DESC
LIMIT 5;


-- ===========================================
-- SECTION 3: Aggregates (5 queries)
-- ===========================================

-- Query 11: Count total number of questions
-- Learning: COUNT(*)
SELECT COUNT(*) AS total_questions FROM questions;

-- Query 12: Find average marks of all questions
-- Learning: AVG()
SELECT AVG(marks) AS average_marks FROM questions;

-- Query 13: Find maximum and minimum marks
-- Learning: MAX() and MIN()
SELECT
    MAX(marks) AS highest_marks,
    MIN(marks) AS lowest_marks,
    MAX(marks) - MIN(marks) AS marks_range
FROM questions;

-- Query 14: Count questions by difficulty
-- Learning: COUNT() with GROUP BY
SELECT difficulty, COUNT(*) AS question_count
FROM questions
GROUP BY difficulty
ORDER BY question_count DESC;

-- Query 15: Calculate total marks available per year
-- Learning: SUM() with GROUP BY
SELECT year, SUM(marks) AS total_marks
FROM questions
GROUP BY year
ORDER BY year DESC;


-- ===========================================
-- SECTION 4: GROUP BY and HAVING (5 queries)
-- ===========================================

-- Query 16: Find topics with more than 3 questions
-- Learning: GROUP BY with HAVING
SELECT topic_name, COUNT(*) AS question_count
FROM questions
GROUP BY topic_name
HAVING COUNT(*) > 3
ORDER BY question_count DESC;

-- Query 17: Find years with average marks > 6
-- Learning: HAVING with aggregate condition
SELECT year, AVG(marks) AS avg_marks, COUNT(*) AS question_count
FROM questions
GROUP BY year
HAVING AVG(marks) > 6
ORDER BY avg_marks DESC;

-- Query 18: Count questions by exam type and difficulty
-- Learning: GROUP BY with multiple columns
SELECT exam_type, difficulty, COUNT(*) AS count
FROM questions
GROUP BY exam_type, difficulty
ORDER BY exam_type, difficulty;

-- Query 19: Find topics with total marks > 30
-- Learning: HAVING with SUM()
SELECT topic_name, SUM(marks) AS total_marks, COUNT(*) AS question_count
FROM questions
GROUP BY topic_name
HAVING SUM(marks) > 30
ORDER BY total_marks DESC;

-- Query 20: Find exam types where the average difficulty is "medium" or harder
-- Learning: Complex GROUP BY with conditional logic
SELECT
    exam_type,
    COUNT(*) AS total_questions,
    SUM(CASE WHEN difficulty = 'easy' THEN 1 ELSE 0 END) AS easy_count,
    SUM(CASE WHEN difficulty = 'medium' THEN 1 ELSE 0 END) AS medium_count,
    SUM(CASE WHEN difficulty = 'hard' THEN 1 ELSE 0 END) AS hard_count
FROM questions
GROUP BY exam_type
ORDER BY exam_type;


-- ===========================================
-- BONUS CHALLENGE QUERIES
-- ===========================================

-- Bonus 1: Find questions that appeared in consecutive years
-- Learning: Self-join concept (preview for Week 3)
-- Hint: Think about joining questions table with itself

-- Bonus 2: Find the most frequently asked topic per year
-- Learning: Subqueries (will learn in Week 3)
-- Hint: Use a subquery to find max count first

-- Bonus 3: List courses with no questions yet
-- Learning: LEFT JOIN (Week 3 topic)
-- Hint: Join courses and questions, filter for NULL

-- ===========================================
-- LEARNING CHECKPOINTS
-- ===========================================

-- After completing these queries, you should be able to:
-- ✅ Write SELECT statements with column selection
-- ✅ Filter data using WHERE with =, >, <, IN, LIKE/ILIKE
-- ✅ Sort results using ORDER BY ASC/DESC
-- ✅ Use LIMIT to restrict result count
-- ✅ Apply aggregate functions: COUNT, SUM, AVG, MIN, MAX
-- ✅ Group data using GROUP BY
-- ✅ Filter groups using HAVING
-- ✅ Understand the difference between WHERE and HAVING
-- ✅ Combine multiple conditions with AND/OR
-- ✅ Use pattern matching with LIKE/ILIKE and %

-- ===========================================
-- COMMON MISTAKES TO AVOID
-- ===========================================

-- Mistake 1: Using WHERE instead of HAVING for aggregates
-- WRONG: SELECT difficulty, COUNT(*) FROM questions WHERE COUNT(*) > 3 GROUP BY difficulty;
-- RIGHT: SELECT difficulty, COUNT(*) FROM questions GROUP BY difficulty HAVING COUNT(*) > 3;

-- Mistake 2: Forgetting to include non-aggregated columns in GROUP BY
-- WRONG: SELECT topic_name, year, COUNT(*) FROM questions GROUP BY topic_name;
-- RIGHT: SELECT topic_name, year, COUNT(*) FROM questions GROUP BY topic_name, year;

-- Mistake 3: Using LIKE case-sensitively when you want case-insensitive
-- WRONG: ... WHERE question_text LIKE '%SQL%'  -- won't match "sql"
-- RIGHT: ... WHERE question_text ILIKE '%SQL%'  -- matches "SQL", "sql", "Sql"

-- Mistake 4: Confusing COUNT(*) and COUNT(column)
-- COUNT(*) counts all rows (including NULLs)
-- COUNT(column) counts non-NULL values in that column

-- ===========================================
-- SELF-CHECK QUESTIONS
-- ===========================================

-- 1. What's the difference between WHERE and HAVING?
-- Answer: WHERE filters rows before grouping; HAVING filters groups after aggregation

-- 2. Can you use ORDER BY without GROUP BY?
-- Answer: Yes! ORDER BY works on any result set

-- 3. What does LIMIT do?
-- Answer: Restricts the number of rows returned

-- 4. How do you find the second-highest value?
-- Answer: ORDER BY column DESC LIMIT 1 OFFSET 1

-- 5. What's the difference between COUNT(*) and COUNT(column)?
-- Answer: COUNT(*) includes NULLs; COUNT(column) counts only non-NULL values

-- ===========================================
-- PRACTICE EXERCISES (Write your own queries!)
-- ===========================================

-- Exercise A: Find all "easy" questions from 2023 worth exactly 5 marks

-- Exercise B: Count how many questions exist per course_code

-- Exercise C: Find the average marks for each difficulty level

-- Exercise D: List all topics that have at least one "hard" question

-- Exercise E: Find years where more than 10 questions were asked

-- Write your solutions below:


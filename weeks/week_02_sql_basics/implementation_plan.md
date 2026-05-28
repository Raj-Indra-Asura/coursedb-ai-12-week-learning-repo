# Week 2: Implementation Plan

## 🎯 Goal
Build a SQL-based academic resource storage system and experience the power of declarative queries. This hands-on success will demonstrate why SQL elegantly solves the problems from Week 1.

---

## 📋 Step-by-Step Implementation

### Step 1: Set Up PostgreSQL Environment (Day 1)
**What to do:**
- Install PostgreSQL on your system
- Create a new database called `coursedb_week2`
- Verify connection with psql or GUI tool (pgAdmin, DBeaver)
- Understand basic PostgreSQL commands

**Why:**
- Experience working with a real DBMS
- Understand client-server architecture
- Learn database connection basics

**Setup commands:**
```bash
# Install PostgreSQL (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib

# Create database
sudo -u postgres createdb coursedb_week2

# Connect to database
psql -U postgres -d coursedb_week2
```

**Expected output:**
```
psql (14.x)
Type "help" for help.

coursedb_week2=#
```

**TODO for you:**
- [ ] Install PostgreSQL successfully
- [ ] Create `coursedb_week2` database
- [ ] Connect using psql
- [ ] Test basic commands: `\l`, `\dt`, `\q`
- [ ] Document connection string for future use

---

### Step 2: Create Schema and Load Sample Data (Day 2)
**What to do:**
- Run `schema_week2.sql` to create tables
- Run `seed_week2.sql` to load sample data
- Verify data was inserted correctly
- Understand table relationships

**Why:**
- Experience structured schema definition
- See primary keys and foreign keys in action
- Compare with Week 1's manual file structure

**Commands:**
```bash
# Run schema creation
psql -U postgres -d coursedb_week2 -f schema_week2.sql

# Load seed data
psql -U postgres -d coursedb_week2 -f seed_week2.sql

# Verify
psql -U postgres -d coursedb_week2 -c "SELECT COUNT(*) FROM questions;"
```

**Expected tables:**
```
courses (course_id, course_code, course_title, semester, credit)
topics (topic_id, course_id, topic_name, description)
questions (question_id, topic_id, question_text, difficulty, year, marks)
resources (resource_id, topic_id, resource_title, resource_type, url)
```

**TODO for you:**
- [ ] Run schema_week2.sql successfully
- [ ] Run seed_week2.sql successfully
- [ ] Verify all 4 tables exist: `\dt`
- [ ] Count rows in each table: `SELECT COUNT(*) FROM table_name;`
- [ ] Describe table structure: `\d questions`
- [ ] Compare complexity with Week 1's file setup

**Reflection checkpoint:**
Write 2-3 sentences comparing:
- Week 1: Manual file creation and ID management
- Week 2: Schema creation with auto-increment PKs and FK constraints

---

### Step 3: Practice SELECT Queries (Day 3)
**What to do:**
- Write SELECT queries with WHERE clauses
- Practice filtering, sorting, and limiting results
- Use comparison operators (=, <, >, <=, >=, !=)
- Use pattern matching with LIKE
- Use logical operators (AND, OR, NOT)

**Why:**
- Master fundamental query syntax
- Experience declarative data retrieval
- Compare with Week 1's imperative search loops

**Example queries to write:**
```sql
-- 1. Find all questions from 2023
SELECT * FROM questions WHERE year = 2023;

-- 2. Find hard questions
SELECT * FROM questions WHERE difficulty = 'hard';

-- 3. Find questions worth more than 5 marks
SELECT question_text, marks FROM questions WHERE marks > 5;

-- 4. Find questions containing 'transaction'
SELECT * FROM questions WHERE question_text ILIKE '%transaction%';

-- 5. Find medium or hard questions from 2023
SELECT * FROM questions
WHERE difficulty IN ('medium', 'hard')
AND year = 2023;

-- 6. Get top 10 highest-mark questions
SELECT question_text, marks
FROM questions
ORDER BY marks DESC
LIMIT 10;

-- 7. Find questions with NULL difficulty
SELECT * FROM questions WHERE difficulty IS NULL;

-- 8. Count questions per difficulty level
SELECT difficulty, COUNT(*)
FROM questions
GROUP BY difficulty;
```

**TODO for you:**
- [ ] Write and test all 8 example queries above
- [ ] Create 5 more queries of your own
- [ ] Measure query execution time: `\timing on`
- [ ] Compare with Week 1's O(n) linear search
- [ ] Document fastest vs slowest query

**Performance comparison:**
```
Week 1 file search for 1 record in 100: _____ ms
Week 2 SQL search for same record: _____ ms
Speedup: _____x faster
```

---

### Step 4: Practice JOIN Queries (Day 4)
**What to do:**
- Write INNER JOIN queries to combine tables
- Write LEFT JOIN queries to find missing data
- Understand JOIN syntax and execution
- Manually trace JOIN operations

**Why:**
- Experience the power of declarative joins
- Compare with Week 1's manual nested loops
- Understand referential integrity benefits

**Example queries:**
```sql
-- 1. Get questions with topic names (INNER JOIN)
SELECT q.question_id, q.question_text, t.topic_name
FROM questions q
INNER JOIN topics t ON q.topic_id = t.topic_id;

-- 2. Get questions with topic and course names (two JOINs)
SELECT q.question_text, t.topic_name, c.course_title
FROM questions q
INNER JOIN topics t ON q.topic_id = t.topic_id
INNER JOIN courses c ON t.course_id = c.course_id;

-- 3. Count questions per topic (JOIN + GROUP BY)
SELECT t.topic_name, COUNT(q.question_id) as question_count
FROM topics t
LEFT JOIN questions q ON t.topic_id = q.topic_id
GROUP BY t.topic_id, t.topic_name
ORDER BY question_count DESC;

-- 4. Find topics with no questions (LEFT JOIN + WHERE NULL)
SELECT t.topic_name
FROM topics t
LEFT JOIN questions q ON t.topic_id = q.topic_id
WHERE q.question_id IS NULL;

-- 5. Count questions per course
SELECT c.course_title, COUNT(q.question_id) as total_questions
FROM courses c
LEFT JOIN topics t ON c.course_id = t.course_id
LEFT JOIN questions q ON t.topic_id = q.topic_id
GROUP BY c.course_id, c.course_title;

-- 6. Find average marks per topic
SELECT t.topic_name, AVG(q.marks) as avg_marks
FROM topics t
INNER JOIN questions q ON t.topic_id = q.topic_id
GROUP BY t.topic_id, t.topic_name
HAVING AVG(q.marks) > 5;
```

**TODO for you:**
- [ ] Write and test all 6 JOIN queries above
- [ ] Draw a manual JOIN trace for query #1 (first 5 rows)
- [ ] Compare with Week 1's manual join implementation
- [ ] Measure JOIN query performance
- [ ] Create 3 more JOIN queries of your own

**Comparison task:**
Calculate lines of code:
- Week 1: Manual join with nested loops = _____ lines
- Week 2: SQL JOIN = _____ lines
- Reduction: _____% fewer lines

---

### Step 5: Practice Aggregates and GROUP BY (Day 5)
**What to do:**
- Use COUNT, SUM, AVG, MAX, MIN functions
- Group data with GROUP BY
- Filter groups with HAVING
- Understand aggregation execution order

**Why:**
- Master data summarization
- Compare with Week 1's manual counting loops
- Prepare for analytics queries in CourseDB-AI

**Example queries:**
```sql
-- 1. Total number of questions
SELECT COUNT(*) as total_questions FROM questions;

-- 2. Questions per difficulty level
SELECT difficulty, COUNT(*) as count
FROM questions
GROUP BY difficulty
ORDER BY count DESC;

-- 3. Average marks per difficulty
SELECT difficulty,
       AVG(marks) as avg_marks,
       MIN(marks) as min_marks,
       MAX(marks) as max_marks
FROM questions
GROUP BY difficulty;

-- 4. Questions per year
SELECT year, COUNT(*) as count
FROM questions
GROUP BY year
ORDER BY year DESC;

-- 5. Topics with more than 5 questions
SELECT t.topic_name, COUNT(q.question_id) as question_count
FROM topics t
INNER JOIN questions q ON t.topic_id = q.topic_id
GROUP BY t.topic_id, t.topic_name
HAVING COUNT(q.question_id) > 5;

-- 6. Distribution of marks
SELECT marks, COUNT(*) as frequency
FROM questions
GROUP BY marks
ORDER BY marks;

-- 7. Courses ordered by total marks available
SELECT c.course_title, SUM(q.marks) as total_marks
FROM courses c
LEFT JOIN topics t ON c.course_id = t.course_id
LEFT JOIN questions q ON t.topic_id = q.topic_id
GROUP BY c.course_id, c.course_title
ORDER BY total_marks DESC NULLS LAST;
```

**TODO for you:**
- [ ] Write and test all 7 aggregate queries above
- [ ] Understand the difference between WHERE and HAVING
- [ ] Test what happens with COUNT(*) vs COUNT(column)
- [ ] Test aggregates on empty sets
- [ ] Create 5 more aggregate queries for analytics
- [ ] Compare with Week 1's manual counting code

**Challenge queries:**
- Find the hardest topic (highest avg difficulty)
- Find years with most questions
- Calculate total marks available per course
- Find topics with no easy questions

---

### Step 6: Write Your Own Queries (Day 6)
**What to do:**
- Design 10 queries for CourseDB-AI use cases
- Practice combining SELECT, JOIN, WHERE, GROUP BY, HAVING
- Optimize queries for performance
- Document query purpose and expected results

**Why:**
- Apply SQL knowledge to real scenarios
- Prepare for backend API implementation (Week 5)
- Develop query design thinking

**Query scenarios to implement:**
```sql
-- Scenario 1: Student searches for "normalization" questions
-- TODO: Write query to find questions containing keyword

-- Scenario 2: Student wants hard questions from last 2 years
-- TODO: Write query with difficulty and year filters

-- Scenario 3: Admin needs topic popularity report
-- TODO: Write query showing topics by question count

-- Scenario 4: Show course completion coverage
-- TODO: Write query showing courses with topic and question counts

-- Scenario 5: Find under-resourced topics
-- TODO: Write query for topics with <3 questions

-- Scenario 6: Question difficulty distribution per course
-- TODO: Write query with GROUP BY and aggregates

-- Scenario 7: Find most asked exam years
-- TODO: Write query grouping by year

-- Scenario 8: Topic with highest average marks
-- TODO: Write query with JOIN and AVG

-- Scenario 9: List resources per topic
-- TODO: Write query joining topics and resources

-- Scenario 10: Full academic data view
-- TODO: Write comprehensive query joining all tables
```

**TODO for you:**
- [ ] Implement all 10 scenario queries
- [ ] Test each query with sample data
- [ ] Verify results are correct
- [ ] Measure query execution time
- [ ] Add EXPLAIN ANALYZE to understand query plans
- [ ] Document 3 performance observations

---

### Step 7: Create Comparison Document (Day 7)
**What to do:**
- Compare Week 1 (files) vs Week 2 (SQL) approaches
- Measure lines of code, performance, complexity
- Document specific advantages of SQL
- Reflect on learning journey

**Why:**
- Solidify understanding of DBMS benefits
- Prepare for ER modeling (Week 3)
- Connect to CourseDB-AI architecture decisions

**Comparison table to fill:**
| Feature | Week 1 (File System) | Week 2 (SQL) | Improvement |
|---------|---------------------|--------------|-------------|
| Setup complexity | Manual file creation | Schema definition | Clearer structure |
| ID management | Manual generation | SERIAL auto-increment | Automatic |
| Search speed | O(n) - _____ ms | O(log n) - _____ ms | _____x faster |
| Join complexity | _____ lines of code | _____ lines SQL | _____% reduction |
| Data integrity | Manual validation | FK constraints | Enforced |
| Concurrent access | Race conditions | ACID transactions | Safe |
| Querying | Imperative loops | Declarative SELECT | More expressive |
| Aggregation | Manual counting code | Built-in functions | Native support |
| Code maintainability | High (scattered logic) | Low (centralized) | Better |

**TODO for you:**
- [ ] Fill in all comparison measurements
- [ ] Write 3-4 paragraphs on SQL advantages
- [ ] Document 5 specific "aha moments"
- [ ] Explain how SQL enables CourseDB-AI features
- [ ] List remaining questions about databases
- [ ] Commit work: "week-02: complete SQL implementation with comparisons"

**Reflection prompts:**
1. What was the most satisfying part of using SQL?
2. How would SQL handle 10,000 questions efficiently?
3. Why is declarative querying more powerful than imperative code?
4. How does SQL's abstraction help developers?
5. What SQL features are you excited to learn next?

---

## 🎯 Connection to CourseDB-AI

This week's SQL practice directly connects to CourseDB-AI by:

1. **Database Schema Foundation**: The tables you created (courses, topics, questions) form CourseDB-AI's core schema.

2. **Query Patterns for APIs**: Every query you wrote becomes an API endpoint:
   - `GET /questions?difficulty=hard` → Week 2 Exercise 3
   - `GET /topics/:id/questions` → Week 2 Exercise 4
   - `GET /analytics/questions-per-topic` → Week 2 Exercise 5

3. **Search Functionality**: LIKE queries enable basic search; Week 10 adds semantic search.

4. **Analytics Dashboard**: GROUP BY queries power usage statistics and trends.

5. **Data Integrity**: FK constraints ensure questions always link to valid topics.

---

## ✅ Success Criteria

By the end of this week, you should have:
- [ ] PostgreSQL installed and configured
- [ ] Schema and seed data loaded successfully
- [ ] 20+ working SQL queries documented
- [ ] Comparison document showing SQL advantages
- [ ] All exercises completed
- [ ] Understanding of CourseDB-AI's SQL foundation

---

## 🚨 Common Mistakes to Avoid

1. **Forgetting semicolons**: SQL statements must end with `;`
2. **Case sensitivity**: PostgreSQL is case-sensitive for quoted identifiers
3. **Ambiguous columns**: Always prefix columns in JOINs (e.g., `t.topic_id`)
4. **WHERE vs HAVING**: Use WHERE before GROUP BY, HAVING after
5. **COUNT(*) vs COUNT(column)**: COUNT(*) includes NULLs, COUNT(column) doesn't
6. **String comparison**: Use ILIKE for case-insensitive matching
7. **JOIN without ON**: Always specify join condition
8. **Using = NULL**: Must use IS NULL or IS NOT NULL

---

## 📚 Resources

- `theory_notes.md` - SQL concepts and syntax
- `exercises.md` - Practice problems
- `schema_week2.sql` - Table definitions
- `seed_week2.sql` - Sample data
- `queries_week2.sql` - Example queries
- PostgreSQL documentation: https://www.postgresql.org/docs/

---

## 🔗 Next Week Preview

**Week 3: ER Modeling + Schema Design**
- Design entity-relationship diagrams
- Model CourseDB-AI's complete data structure
- Learn cardinality and relationship types
- Map ER diagrams to SQL tables
- Plan before implementing!

# Week 2: SQL Basics Through Academic Data

**Duration**: 7 days
**Status**: 🔄 Ready to Start

---

## 🎯 Why This Week Matters

After Week 1's frustrating experience with file-based storage, this week introduces **SQL** - a declarative language that elegantly solves most of the problems you encountered. You'll experience the power of:
- Structured data with schemas
- Declarative queries instead of imperative code
- Built-in constraints and validation
- Simple joins instead of manual lookups

This week is **foundational** for everything that follows. Without solid SQL skills, you cannot:
- Design normalized schemas (Week 4)
- Write complex analytics queries (Week 6)
- Understand query optimization (Week 8)
- Build CourseDB-AI's search and analytics features

---

## 📚 Learning Objectives

By the end of this week, you will be able to:

✅ Create tables with appropriate data types and constraints
✅ Insert, update, and delete data using SQL DML statements
✅ Write SELECT queries with filtering, sorting, and grouping
✅ Perform joins across multiple tables
✅ Use aggregate functions (COUNT, SUM, AVG, MAX, MIN)
✅ Apply WHERE, HAVING, ORDER BY, LIMIT clauses correctly
✅ Understand the difference between INNER, LEFT, RIGHT joins
✅ Write subqueries for complex data retrieval
✅ Compare SQL approach with Week 1's file-based system

---

## 📖 Concepts to Learn

### **1. Relational Model Basics**

- **Relation (Table)**: Collection of related data
- **Tuple (Row)**: Single record in a table
- **Attribute (Column)**: Property of an entity
- **Domain**: Set of allowed values for an attribute
- **Schema**: Structure of the table (column names and types)

### **2. SQL Categories**

- **DDL (Data Definition Language)**: CREATE, ALTER, DROP
- **DML (Data Manipulation Language)**: INSERT, UPDATE, DELETE
- **DQL (Data Query Language)**: SELECT
- **DCL (Data Control Language)**: GRANT, REVOKE

### **3. SELECT Query Structure**

```sql
SELECT column1, column2
FROM table_name
WHERE condition
GROUP BY column1
HAVING group_condition
ORDER BY column1 DESC
LIMIT 10;
```

Execution order: FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT

### **4. Join Types**

- **INNER JOIN**: Returns matching rows from both tables
- **LEFT JOIN**: All rows from left table + matching from right
- **RIGHT JOIN**: All rows from right table + matching from left
- **FULL OUTER JOIN**: All rows from both tables

### **5. Aggregate Functions**

- COUNT(*): Count all rows
- COUNT(column): Count non-null values
- SUM(column): Sum of values
- AVG(column): Average value
- MAX(column), MIN(column): Maximum and minimum

### **6. SQL vs File System**

| Operation | File System (Week 1) | SQL (Week 2) |
|-----------|---------------------|--------------|
| Find by ID | O(n) linear scan | O(log n) with index |
| Filter data | Write loop + conditions | `WHERE` clause |
| Join data | Manual nested loops | `JOIN` keyword |
| Aggregate | Write counting code | `COUNT`, `SUM`, etc. |
| Sort | Implement sorting algorithm | `ORDER BY` clause |
| Unique IDs | Manual generation | `SERIAL` auto-increment |

---

## 🧠 Mental Model

```
Week 1 File System → Week 2 SQL Tables → Week 3 ER Design → Week 4 Normalization
     (Pain)              (Relief!)         (Planning)         (Perfection)
```

**The SQL Mindset Shift**:
- Week 1: "How do I implement this?" (Imperative)
- Week 2: "What do I want?" (Declarative)

---

## 🛠️ Hands-On Exercises

### **Exercise 1: CREATE TABLE Practice**

Create tables for CourseDB-AI's academic data:
```sql
-- TODO: Create courses table
-- columns: course_id (PK), course_code, course_title, semester, credit

-- TODO: Create topics table
-- columns: topic_id (PK), course_id (FK), topic_name, description

-- TODO: Create questions table
-- columns: question_id (PK), topic_id (FK), question_text, difficulty, year, marks
```

**Self-check**:
1. Did you specify primary keys?
2. Did you use appropriate data types?
3. Did you add foreign key constraints?

### **Exercise 2: INSERT and UPDATE**

Insert sample data and practice updates:
```sql
-- TODO: Insert 3 courses
-- TODO: Insert 5 topics
-- TODO: Insert 10 questions

-- TODO: Update a question's difficulty
-- TODO: Update multiple questions at once
```

### **Exercise 3: SELECT with WHERE**

Practice filtering queries:
```sql
-- Find all questions with difficulty 'hard'
-- Find questions from year 2023
-- Find questions with marks > 5
-- Find questions containing 'SQL' in text (use LIKE)
-- Find questions NOT from 2023
```

### **Exercise 4: Joins**

Practice combining tables:
```sql
-- Get all questions with their topic names
-- Get all topics with their course names
-- Get count of questions per topic
-- Get count of topics per course
-- Find topics with no questions (LEFT JOIN + WHERE NULL)
```

### **Exercise 5: Aggregates and GROUP BY**

Practice summarization:
```sql
-- Count total questions
-- Count questions per difficulty level
-- Average marks per difficulty
-- Find topic with most questions
-- Count questions per year
```

---

## 💻 Mini Implementation

### **Task**: Build SQL Schema for CourseDB-AI

**Requirements**:
1. Create schema in `schema_week2.sql`
2. Create seed data in `seed_week2.sql` with:
   - 3 courses (CS201 DBMS, CS301 AI, CS202 Web Dev)
   - 10+ topics across courses
   - 20+ previous-year DBMS questions
3. Create 20 practice queries in `queries_week2.sql`

**Already provided** in the repository:
- ✅ `schema_week2.sql` - Database schema
- ✅ `seed_week2.sql` - 50+ sample questions
- ✅ `queries_week2.sql` - 20 practice queries

**Your tasks**:
- [ ] Read and understand the provided schema
- [ ] Run the schema to create tables
- [ ] Load the seed data
- [ ] Execute all 20 practice queries
- [ ] Modify queries to answer new questions
- [ ] Compare with Week 1's file-based approach

---

## 🐛 Debugging Exercise

### **Common SQL Errors**

1. **Syntax Error**: Missing semicolon
2. **Ambiguous Column**: Column name exists in multiple tables
3. **Foreign Key Violation**: Trying to insert invalid FK
4. **Type Mismatch**: Inserting string into integer column
5. **Division by Zero**: AVG() or SUM() on empty set

**Practice**:
- [ ] Intentionally cause each error
- [ ] Read and understand the error message
- [ ] Fix the error
- [ ] Document what you learned

---

## 📝 Documentation Task

### **Compare SQL vs File System**

Create a document comparing your Week 1 and Week 2 implementations:

| Feature | Week 1 (Files) | Week 2 (SQL) | Winner |
|---------|---------------|--------------|--------|
| Lines of code | _____ | _____ | SQL |
| Search speed | _____ ms | _____ ms | SQL |
| Join complexity | High (manual loops) | Low (JOIN keyword) | SQL |
| Data integrity | Manual | Automatic (FK) | SQL |
| Concurrent access | Race conditions | Transaction safe | SQL |

**Write 3-4 paragraphs** on:
1. What was easier in SQL?
2. What surprised you about SQL?
3. What's still confusing?
4. How does this apply to CourseDB-AI?

---

## 🤔 Reflection Questions

1. **Compare Approaches**: How many lines of code did you write in Week 1 vs Week 2 for the same functionality?

2. **Declarative vs Imperative**: What does it mean that SQL is "declarative"? Why is this powerful?

3. **CourseDB-AI Connection**: How will SQL help with CourseDB-AI's search and analytics features?

4. **Abstraction**: SQL hides implementation details. Is this good or bad? Why?

5. **Next Steps**: What SQL features are you curious about? (Views? Triggers? Stored procedures?)

---

## 📦 Deliverables

By the end of Week 2, you should have:

- [ ] Completed schema with 3+ tables
- [ ] Seed data with 20+ questions
- [ ] 20 working SQL queries
- [ ] Comparison document (SQL vs files)
- [ ] All exercises completed
- [ ] Reflection questions answered
- [ ] Self-check quiz passed (below)
- [ ] Ready to design ER model in Week 3

---

## ✅ Self-Check Quiz

Test your understanding before moving to Week 3:

1. **What is the difference between DDL and DML?**
   - [ ] I can explain with examples

2. **What is a primary key? Why is it needed?**
   - [ ] I can explain and identify PKs

3. **What is a foreign key? How does it enforce integrity?**
   - [ ] I can explain FK constraints

4. **What is the difference between WHERE and HAVING?**
   - [ ] I understand when to use each

5. **What is the execution order of a SELECT query?**
   - [ ] I can write the correct order

6. **What does INNER JOIN return?**
   - [ ] I can explain with examples

7. **What does LEFT JOIN return?**
   - [ ] I can explain with examples

8. **When do you use GROUP BY?**
   - [ ] I can write aggregate queries

9. **What does COUNT(*) vs COUNT(column) do?**
   - [ ] I understand NULL handling

10. **How is SQL better than file-based storage?**
    - [ ] I can list 5+ advantages

**Score**: ___ / 10

**Am I ready for Week 3?** ☐ Yes ☐ Need review

---

## 🔗 How This Connects to CourseDB-AI

### **Direct Applications**:

1. **Course Management**: SQL tables for courses, topics, resources
2. **Question Storage**: Structured storage with metadata (year, difficulty, marks)
3. **Search Queries**: Find questions by topic, difficulty, year
4. **Analytics**: Count questions per topic, trend analysis
5. **Relationships**: Link questions to topics to courses

### **Week 2 → Final Project**:
- Tables created this week become CourseDB-AI's foundation
- Queries practiced become API endpoint logic
- Joins learned enable resource relationship queries
- Aggregates enable analytics dashboard

### **Skills for AI/ML**:
- **Data retrieval**: Essential for training data collection
- **Data cleaning**: SQL for preprocessing and validation
- **Feature engineering**: Aggregates and joins for features
- **Monitoring**: SQL queries for model performance metrics

---

## 📚 Resources

- **PostgreSQL Documentation**: https://www.postgresql.org/docs/
- **SQL Tutorial**: https://www.sqltutorial.org/
- **SQL Practice**: https://sqlzoo.net/
- **Week 2 Files**:
  - `theory_notes.md` - SQL concepts and syntax
  - `schema_week2.sql` - Table definitions
  - `seed_week2.sql` - Sample data
  - `queries_week2.sql` - Practice queries

---

## 🔜 Next Week Preview

**Week 3: ER Modeling + Schema Design**
- Design entity-relationship diagrams
- Model CourseDB-AI's complete data structure
- Learn cardinality and relationship types
- Map ER diagrams to SQL tables
- Plan before implementing!

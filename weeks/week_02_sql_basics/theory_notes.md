# Week 2: SQL Basics - Theory Notes

## 🧭 Navigation

**[← Back to Week 2 Overview](README.md)** | **[Next: Exercises →](exercises.md)**

---

## 📚 Core Concepts

###1. Relational Model Basics

**What is the Relational Model?**
- Data organized in **tables (relations)**
- Each table has **rows (tuples)** and **columns (attributes)**
- Tables are related through **keys**

**Terminology:**
- **Relation** = Table
- **Tuple** = Row/Record
- **Attribute** = Column/Field
- **Domain** = Set of allowed values for an attribute
- **Schema** = Structure of the table (column names and types)
- **Instance** = Actual data at a point in time

### 2. SQL Categories

SQL is divided into several categories:

#### **DDL (Data Definition Language)**
Defines database structure: CREATE TABLE, ALTER TABLE, DROP TABLE, TRUNCATE TABLE

#### **DML (Data Manipulation Language)**
Modifies data: INSERT, UPDATE, DELETE

#### **DQL (Data Query Language)**
Retrieves data: SELECT

### 3. SELECT Queries

**Basic Syntax:**
```sql
SELECT column1, column2 FROM table_name
WHERE condition
ORDER BY column
LIMIT n;
```

### 4. WHERE Clause (Filtering)

**Comparison Operators:** =, !=, >, <, >=, <=

**Logical Operators:** AND, OR, NOT

**Special Operators:** IN, BETWEEN, LIKE, IS NULL

### 5. ORDER BY (Sorting)

Sort results in ASC (ascending) or DESC (descending) order.

### 6. Aggregate Functions

COUNT(*), COUNT(column), SUM(column), AVG(column), MIN(column), MAX(column)

### 7. GROUP BY

Group rows that have the same values in specified columns.

**Key Rule:** Every column in SELECT (except aggregates) must be in GROUP BY

### 8. HAVING Clause

Filter groups after aggregation.

**Key Difference:**
- `WHERE` filters **rows** before grouping
- `HAVING` filters **groups** after aggregation

---

## 🎯 CourseDB-AI Connection

| SQL Concept | CourseDB-AI Use Case |
|-------------|---------------------|
| **SELECT** | Retrieve questions for display in UI |
| **WHERE** | Filter questions by year, difficulty, topic |
| **ORDER BY** | Sort questions by relevance, year, marks |
| **LIMIT** | Pagination in web interface |
| **COUNT** | Dashboard statistics (total questions per topic) |
| **GROUP BY** | Analytics: questions per year, per difficulty |
| **HAVING** | Find frequently-tested topics (count > threshold) |

---

## ❌ Common Mistakes

### 1. WHERE vs HAVING Confusion
```sql
-- ❌ WRONG: Can't use aggregate in WHERE
SELECT difficulty, COUNT(*) FROM questions
WHERE COUNT(*) > 5 GROUP BY difficulty;

-- ✅ RIGHT: Use HAVING for aggregates
SELECT difficulty, COUNT(*) FROM questions
GROUP BY difficulty HAVING COUNT(*) > 5;
```

### 2. Forgetting GROUP BY
```sql
-- ❌ WRONG: difficulty not in GROUP BY
SELECT year, difficulty, COUNT(*) FROM questions GROUP BY year;

-- ✅ RIGHT: Include all non-aggregate columns
SELECT year, difficulty, COUNT(*) FROM questions GROUP BY year, difficulty;
```

---

## ✅ Self-Check Questions

1. What's the difference between `WHERE` and `HAVING`?
2. Can you use `ORDER BY` without `GROUP BY`?
3. What does `COUNT(*)` count that `COUNT(column)` doesn't?
4. How do you find the 3rd highest value in a column?
5. What's the execution order of SQL clauses?

---

**Next Steps:** Complete the 20 queries in `queries_week2.sql` and exercises!

---

## 🧭 Navigation

**[← Back to Week 2 Overview](README.md)** | **[Next: Exercises →](exercises.md)**


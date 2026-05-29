# Week 2: Progress Checkpoints

## 📋 Daily Checkpoints

Use this file to track your progress throughout Week 2. Check off items as you complete them.

---

## Day 1: PostgreSQL Setup & Environment

**Date**: ___________

### Installation
- [ ] Install PostgreSQL successfully
- [ ] Verify installation: `psql --version`
- [ ] Start PostgreSQL service
- [ ] Create `coursedb_week2` database
- [ ] Connect to database using psql or GUI tool

### Basic Commands
- [ ] Learn `\l` (list databases)
- [ ] Learn `\dt` (list tables)
- [ ] Learn `\d table_name` (describe table)
- [ ] Learn `\q` (quit psql)
- [ ] Learn `\?` (help)

### Theory
- [ ] Read `theory_notes.md` - Relational model basics
- [ ] Read `README.md` - Week 2 overview
- [ ] Understand DDL vs DML vs DQL
- [ ] Understand primary keys and foreign keys
- [ ] Review Week 1 comparison table

### Reflection
- [ ] Write initial thoughts comparing file system vs SQL
- [ ] List 3 expectations for SQL learning

**Time spent**: _____ hours

**What I learned today**:
```
[Write 2-3 sentences]
```

**Setup issues encountered**:
```
[Document any installation or connection problems]
```

---

## Day 2: Schema Creation & Data Loading

**Date**: ___________

### Schema Implementation
- [ ] Read and understand `schema_week2.sql`
- [ ] Run schema creation: `psql -U postgres -d coursedb_week2 -f schema_week2.sql`
- [ ] Verify tables created: `\dt`
- [ ] Describe each table structure: `\d courses`, `\d topics`, `\d questions`
- [ ] Understand foreign key relationships

### Seed Data
- [ ] Read and understand `seed_week2.sql`
- [ ] Load seed data: `psql -U postgres -d coursedb_week2 -f seed_week2.sql`
- [ ] Count rows in each table:
  - Courses: _____ rows
  - Topics: _____ rows
  - Questions: _____ rows
  - Resources: _____ rows

### Verification
- [ ] Run sample query: `SELECT * FROM courses;`
- [ ] Test foreign key constraint with invalid insert
- [ ] Understand auto-increment with SERIAL
- [ ] Compare with Week 1's manual ID generation

**Time spent**: _____ hours

**Schema observations**:
```
Compare Week 1 (manual files) vs Week 2 (schema creation):
- Which was easier?
- Which is more maintainable?
- What surprised you about constraints?
```

---

## Day 3: SELECT Queries & WHERE Clauses

**Date**: ___________

### Basic SELECT
- [ ] Practice: `SELECT * FROM questions;`
- [ ] Practice: `SELECT question_id, question_text FROM questions;`
- [ ] Practice: `SELECT COUNT(*) FROM questions;`
- [ ] Practice: `SELECT DISTINCT difficulty FROM questions;`

### WHERE Clauses
- [ ] Find questions with difficulty = 'hard'
- [ ] Find questions from year 2023
- [ ] Find questions with marks > 5
- [ ] Find questions with marks BETWEEN 5 AND 10
- [ ] Find questions with difficulty IN ('easy', 'medium')
- [ ] Find questions containing 'SQL' using LIKE

### Sorting & Limiting
- [ ] ORDER BY marks DESC
- [ ] ORDER BY difficulty, marks DESC
- [ ] LIMIT 10 results
- [ ] Get top 5 highest-mark questions

### Performance Testing
- [ ] Enable timing: `\timing on`
- [ ] Measure search for specific question_id: _____ ms
- [ ] Compare with Week 1 file search: _____ ms
- [ ] Calculate speedup: _____x faster

**Time spent**: _____ hours

**Queries written**: _____

**Performance comparison**:
```
Week 1 search time: _____ ms
Week 2 search time: _____ ms
Why is SQL faster?
```

**Aha moments**:
```
What surprised you about declarative queries?
```

---

## Day 4: JOIN Operations

**Date**: ___________

### INNER JOIN Practice
- [ ] Join questions with topics (get topic_name)
- [ ] Join questions with topics and courses (3-table join)
- [ ] Use table aliases (q, t, c)
- [ ] Test ambiguous column error (intentionally)
- [ ] Fix with proper table prefixes

### LEFT JOIN Practice
- [ ] Find topics with no questions (LEFT JOIN + WHERE NULL)
- [ ] Count questions per topic (including topics with 0)
- [ ] Get all courses with question counts
- [ ] Understand LEFT JOIN vs INNER JOIN difference

### Complex Joins
- [ ] Get all questions with course title and topic name
- [ ] Filter joined results with WHERE
- [ ] Sort joined results
- [ ] Limit joined results to top 10

### Manual JOIN Trace
- [ ] Pick a simple join query
- [ ] Manually trace how JOIN combines rows
- [ ] Draw table showing intermediate results
- [ ] Compare with Week 1's nested loop implementation

**Time spent**: _____ hours

**JOIN queries written**: _____

**Code comparison**:
```
Week 1 manual join: _____ lines of Python code
Week 2 SQL JOIN: _____ lines of SQL
Reduction: _____% fewer lines
```

**Understanding check**:
```
Explain in your own words:
- What does INNER JOIN return?
- What does LEFT JOIN return?
- When would you use each?
```

---

## Day 5: Aggregates & GROUP BY

**Date**: ___________

### Aggregate Functions
- [ ] COUNT(*) - Total questions
- [ ] COUNT(difficulty) - Non-NULL difficulties
- [ ] AVG(marks) - Average marks
- [ ] SUM(marks) - Total marks
- [ ] MAX(marks), MIN(marks) - Range

### GROUP BY Practice
- [ ] Count questions per difficulty level
- [ ] Count questions per year
- [ ] Average marks per difficulty
- [ ] Count topics per course
- [ ] Count questions per topic

### HAVING Clause
- [ ] Find topics with more than 5 questions
- [ ] Find difficulty levels with avg marks > 5
- [ ] Understand WHERE vs HAVING difference
- [ ] Test using aggregate in WHERE (should error)

### Complex Aggregates
- [ ] Multi-level grouping
- [ ] Aggregates with JOINs
- [ ] Nested aggregates (if needed)
- [ ] ORDER BY aggregate results

**Time spent**: _____ hours

**Aggregate queries written**: _____

**WHERE vs HAVING understanding**:
```
Explain when to use each:
- WHERE: _____
- HAVING: _____
Give an example of each.
```

**Comparison with Week 1**:
```
Week 1 manual counting: _____ lines
Week 2 SQL aggregates: _____ lines
Which is more readable?
```

---

## Day 6: Query Design & Optimization

**Date**: ___________

### CourseDB-AI Query Scenarios
- [ ] Implement all 10 scenario queries from implementation_plan.md
- [ ] Test each query with sample data
- [ ] Verify results are correct
- [ ] Measure execution time for each
- [ ] Document slowest query

### Query Experimentation
- [ ] Create 5 additional queries of your own
- [ ] Try complex nested queries
- [ ] Experiment with subqueries
- [ ] Test query with EXPLAIN (preview of Week 8)

### Error Practice
- [ ] Intentionally trigger 5 common errors from mistakes_to_expect.md
- [ ] Read error messages carefully
- [ ] Fix each error
- [ ] Document what you learned

### Code Organization
- [ ] Save all queries in `my_queries_week2.sql`
- [ ] Add comments explaining each query
- [ ] Group queries by category
- [ ] Prepare queries for Week 3 use

**Time spent**: _____ hours

**Total queries created**: _____

**Most interesting query**:
```sql
-- Paste your most interesting or complex query here
-- Explain what it does and why it's interesting
```

**Error lessons learned**:
```
List 3 errors you made and how you fixed them:
1.
2.
3.
```

---

## Day 7: Comparison & Reflection

**Date**: ___________

### Final Comparison Document
- [ ] Complete comparison table (implementation_plan.md)
- [ ] Measure all performance metrics
- [ ] Calculate lines of code reduction
- [ ] Document specific SQL advantages
- [ ] List 5 "aha moments"

### Deliverables Check
- [ ] All 20+ practice queries working
- [ ] `my_queries_week2.sql` created and documented
- [ ] Comparison document completed
- [ ] All exercises in exercises.md completed
- [ ] Reflection.md filled out completely

### Self-Assessment
- [ ] Complete self-check quiz in README.md
- [ ] Review all theory_notes.md concepts
- [ ] Test SQL knowledge with random queries
- [ ] Identify weak areas for review

### Documentation
- [ ] Add comprehensive comments to all queries
- [ ] Create summary of Week 2 learnings
- [ ] Document remaining questions
- [ ] Prepare questions for Week 3

### Git Commit
- [ ] Stage all files: `git add .`
- [ ] Commit: `git commit -m "week-02: complete SQL implementation with comparisons"`
- [ ] Review what you accomplished

**Time spent**: _____ hours

**Week 2 total time**: _____ hours

**Completion status**: _____%

**Self-check quiz score**: _____ / 10

---

## 📊 Week 2 Summary

### Time Breakdown
- Day 1 (Setup): _____ hours
- Day 2 (Schema): _____ hours
- Day 3 (SELECT): _____ hours
- Day 4 (JOIN): _____ hours
- Day 5 (Aggregates): _____ hours
- Day 6 (Query Design): _____ hours
- Day 7 (Comparison): _____ hours
- **Total**: _____ hours

### Completed Deliverables
- [ ] PostgreSQL installed and configured
- [ ] Schema and seed data loaded
- [ ] 20+ SQL queries documented
- [ ] Comparison document (Week 1 vs Week 2)
- [ ] All exercises completed
- [ ] Reflection questions answered
- [ ] Self-check quiz passed
- [ ] `my_queries_week2.sql` with 20+ queries

### Key Metrics
- Total queries written: _____
- Performance improvement over Week 1: _____x faster
- Code reduction: _____% fewer lines
- Confidence level: _____ / 5

### Key Takeaways
1. ___________
2. ___________
3. ___________

### Challenges Overcome
1. ___________
2. ___________
3. ___________

### Questions for Week 3
1. ___________
2. ___________
3. ___________

---

## 🎯 Readiness for Week 3

Before moving to Week 3 (ER Modeling), ensure:

**Theory Understanding**:
- [ ] I understand the relational model (tables, rows, columns)
- [ ] I can explain primary keys and foreign keys
- [ ] I understand DDL vs DML vs DQL
- [ ] I can explain JOIN types (INNER, LEFT)
- [ ] I understand WHERE vs HAVING
- [ ] I understand aggregate functions

**Practical Skills**:
- [ ] I can create tables with constraints
- [ ] I can write SELECT queries with WHERE
- [ ] I can write JOIN queries (2+ tables)
- [ ] I can use aggregate functions with GROUP BY
- [ ] I can read and understand error messages
- [ ] I can debug common SQL mistakes

**CourseDB-AI Connection**:
- [ ] I understand how SQL enables CourseDB-AI features
- [ ] I can map SQL queries to API endpoints
- [ ] I see how SQL improves over file system
- [ ] I understand data integrity importance

**Am I ready for Week 3?** ☐ Yes ☐ Need more time

**If not ready, what do I need to review?**:
```
[List specific topics to revisit]
```

---

## 📈 Progress Visualization

**Week 1 vs Week 2 Comparison**:

| Metric | Week 1 | Week 2 | Improvement |
|--------|--------|--------|-------------|
| Lines of code | _____ | _____ | _____% less |
| Search time | _____ ms | _____ ms | _____x faster |
| Time to implement | _____ hrs | _____ hrs | _____% less |
| Bugs encountered | _____ | _____ | _____% less |
| Confidence level | _____ / 5 | _____ / 5 | _____ gain |

**What this shows**:
```
Reflect on the quantitative improvements from Week 1 to Week 2.
Why is SQL objectively better for database operations?
```

---

## 🔗 Links to Week 2 Materials

- [README.md](./README.md) - Week overview
- [theory_notes.md](./theory_notes.md) - SQL concepts
- [exercises.md](./exercises.md) - Practice problems
- [implementation_plan.md](./implementation_plan.md) - Step-by-step guide
- [reflection.md](./reflection.md) - Reflection prompts
- [mistakes_to_expect.md](./mistakes_to_expect.md) - Common errors
- [schema_week2.sql](./schema_week2.sql) - Table definitions
- [seed_week2.sql](./seed_week2.sql) - Sample data
- [queries_week2.sql](./queries_week2.sql) - Example queries

---

## 🚀 Next Steps

**Week 3 Preview: ER Modeling + Schema Design**

In Week 3, you'll learn to:
- Design entity-relationship diagrams
- Model CourseDB-AI's complete data structure
- Understand cardinality (1:1, 1:N, M:N)
- Map ER diagrams to SQL schemas
- Plan database structure before coding

**Preparation**:
- Review your Week 2 schema
- Think about CourseDB-AI's complete requirements
- Consider what entities and relationships exist
- Bring questions about database design

---

**Last updated**: ___________

**Overall satisfaction with Week 2**: ⭐⭐⭐⭐⭐ (rate 1-5 stars)

**What I'm most excited about for Week 3**:
```
[Write 2-3 sentences]
```

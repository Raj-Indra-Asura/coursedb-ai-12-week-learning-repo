# Week 6: Advanced SQL - Daily Checkpoints

## 🎯 Purpose

Track your daily progress through Week 6 with concrete, measurable checkpoints. Each day has specific deliverables you can verify.

**How to use this document:**
- [ ] Check off items as you complete them
- [ ] Verify each checkpoint before moving to next day
- [ ] Don't skip checkpoints—they build on each other
- [ ] If stuck on a checkpoint for >1 hour, review mistakes_to_expect.md

---

## Day 1: Database Views ✅

### Morning Checkpoint (Simple Views)

**Time estimate:** 2-3 hours

**Deliverables:**

- [ ] **PostgreSQL connection verified**
  ```bash
  psql -U coursedb_user -d coursedb_dev -c "SELECT current_database();"
  ```

- [ ] **First simple view created and tested**
  ```sql
  -- Verify view exists
  \dv active_courses
  
  -- Query the view
  SELECT * FROM active_courses LIMIT 5;
  ```

- [ ] **Exercise 1.1 completed**: `active_courses_with_questions` view
  - [ ] View created without errors
  - [ ] Query returns results
  - [ ] Question count shows correct numbers

- [ ] **Exercise 1.2 completed**: `course_analytics` view
  - [ ] Multiple aggregations working
  - [ ] Difficulty counts showing correctly
  - [ ] Average marks calculated

**Self-check questions:**
1. Can you query your view like a table? (Yes/No)
2. What happens if you try to UPDATE the course_analytics view? (Should fail)
3. How many rows does active_courses_with_questions return? _____

### Afternoon Checkpoint (Materialized Views)

**Time estimate:** 2-3 hours

**Deliverables:**

- [ ] **Complex view with multiple JOINs created**
  ```sql
  SELECT * FROM comprehensive_course_stats LIMIT 3;
  ```

- [ ] **Exercise 1.3 completed**: Materialized view
  - [ ] Materialized view created
  - [ ] Unique index created for concurrent refresh
  - [ ] REFRESH command executed successfully
  - [ ] Can query after refresh

- [ ] **Understand materialized view refresh**
  ```sql
  -- Insert new data
  INSERT INTO questions (course_id, topic_id, question_text, difficulty, marks)
  VALUES (1, 1, 'Test materialization', 'easy', 5);
  
  -- View still shows old count (verify)
  SELECT * FROM course_performance_stats WHERE course_code = 'CS201';
  
  -- Refresh and verify count updated
  REFRESH MATERIALIZED VIEW course_performance_stats;
  SELECT * FROM course_performance_stats WHERE course_code = 'CS201';
  ```

- [ ] **Views documentation created**
  - [ ] List all views in a text file
  - [ ] Document purpose of each view
  - [ ] Note which views are materialized

**Self-check questions:**
1. What's the difference between regular view and materialized view? _____
2. When should you use materialized view? _____
3. How often should you refresh materialized views? _____

**Day 1 Complete:** You can create and use views! ✅

---

## Day 2: Database Triggers ✅

### Morning Checkpoint (Audit Triggers)

**Time estimate:** 2-3 hours

**Deliverables:**

- [ ] **Audit log table created**
  ```sql
  \d audit_log
  -- Should show: audit_id, table_name, record_id, operation, old_data, new_data, changed_at
  ```

- [ ] **Exercise 2.1 completed**: Question audit trigger
  - [ ] Trigger function created
  - [ ] Trigger attached to questions table
  - [ ] Trigger fires on INSERT
  - [ ] Trigger fires on UPDATE
  - [ ] Trigger fires on DELETE

- [ ] **Audit trigger tested**
  ```sql
  -- Test INSERT
  INSERT INTO questions (course_id, topic_id, question_text, difficulty, marks)
  VALUES (1, 1, 'Test audit', 'easy', 10);
  
  -- Verify audit log
  SELECT operation, new_data->>'question_text', changed_at
  FROM audit_log
  WHERE table_name = 'questions'
  ORDER BY changed_at DESC
  LIMIT 1;
  -- Should show INSERT operation
  
  -- Test UPDATE
  UPDATE questions SET difficulty = 'hard' WHERE question_id = 1;
  
  -- Verify shows old and new values
  SELECT
      operation,
      old_data->>'difficulty' as old_difficulty,
      new_data->>'difficulty' as new_difficulty
  FROM audit_log
  WHERE table_name = 'questions' AND operation = 'UPDATE'
  ORDER BY changed_at DESC LIMIT 1;
  ```

- [ ] **Audit extended to other tables**
  - [ ] Course audit trigger created
  - [ ] Topic audit trigger created
  - [ ] All triggers tested

**Self-check questions:**
1. What is TG_OP used for? _____
2. What's the difference between OLD and NEW? _____
3. When would you use BEFORE vs AFTER trigger? _____

### Afternoon Checkpoint (Validation Triggers)

**Time estimate:** 2-3 hours

**Deliverables:**

- [ ] **Exercise 2.2 completed**: Validation trigger
  - [ ] Validation function created
  - [ ] Trigger attached as BEFORE INSERT OR UPDATE
  - [ ] Marks validation working (1-100)
  - [ ] Difficulty validation working (easy/medium/hard)
  - [ ] Year validation working

- [ ] **Validation trigger tested**
  ```sql
  -- This should fail with descriptive error
  INSERT INTO questions (course_id, topic_id, question_text, difficulty, marks)
  VALUES (1, 1, 'Test', 'invalid_difficulty', 150);
  -- ERROR: Invalid difficulty: invalid_difficulty
  
  -- This should succeed
  INSERT INTO questions (course_id, topic_id, question_text, difficulty, marks)
  VALUES (1, 1, 'What is normalization?', 'medium', 15);
  -- Success
  ```

- [ ] **Exercise 2.3 completed**: Automatic timestamp
  - [ ] `updated_at` column added to courses
  - [ ] Timestamp trigger function created
  - [ ] Trigger attached to courses
  - [ ] UPDATE automatically updates timestamp

- [ ] **Timestamp trigger tested**
  ```sql
  -- Check current timestamp
  SELECT course_id, title, updated_at FROM courses WHERE course_id = 1;
  
  -- Wait 2 seconds, then update
  SELECT pg_sleep(2);
  UPDATE courses SET title = 'Updated Title' WHERE course_id = 1;
  
  -- Verify timestamp changed
  SELECT course_id, title, updated_at FROM courses WHERE course_id = 1;
  ```

**Self-check questions:**
1. Can triggers prevent invalid data from being inserted? (Yes/No)
2. What happens if trigger function raises an exception? _____
3. Should you use BEFORE or AFTER for validation? _____

**Day 2 Complete:** You can create audit and validation triggers! ✅

---

## Day 3: Constraints ✅

### Morning Checkpoint (CHECK and UNIQUE)

**Time estimate:** 2-3 hours

**Deliverables:**

- [ ] **Exercise 3.1 completed**: CHECK constraints
  - [ ] `valid_difficulty` constraint added
  - [ ] `valid_marks` constraint added
  - [ ] `valid_year` constraint added
  - [ ] `valid_credits` constraint added to courses

- [ ] **CHECK constraints tested**
  ```sql
  -- These should fail
  INSERT INTO questions (course_id, topic_id, question_text, difficulty, marks)
  VALUES (1, 1, 'Test', 'super_hard', 5);
  -- ERROR: new row violates check constraint "valid_difficulty"
  
  INSERT INTO questions (course_id, topic_id, question_text, difficulty, marks)
  VALUES (1, 1, 'Test', 'easy', 150);
  -- ERROR: new row violates check constraint "valid_marks"
  
  -- This should succeed
  INSERT INTO questions (course_id, topic_id, question_text, difficulty, marks, year)
  VALUES (1, 1, 'What is ACID?', 'medium', 15, 2024);
  -- Success
  ```

- [ ] **Exercise 3.2 completed**: UNIQUE constraints
  - [ ] `unique_course_code` constraint added
  - [ ] `unique_topic_per_course` constraint added

- [ ] **UNIQUE constraints tested**
  ```sql
  -- This should fail (duplicate course code)
  INSERT INTO courses (course_code, title, credits)
  VALUES ('CS201', 'Duplicate', 4);
  -- ERROR: duplicate key value violates unique constraint
  
  -- This should fail (duplicate topic name for same course)
  INSERT INTO topics (course_id, topic_name, order_index)
  VALUES (1, 'Normalization', 99);
  -- ERROR: duplicate key value violates unique constraint
  ```

- [ ] **View all constraints**
  ```sql
  SELECT constraint_name, constraint_type
  FROM information_schema.table_constraints
  WHERE table_name = 'questions' AND table_schema = 'public';
  ```

**Self-check questions:**
1. What happens when CHECK constraint is violated? _____
2. Can you have multiple CHECK constraints on same column? (Yes/No)
3. What's the difference between UNIQUE constraint and unique index? _____

### Afternoon Checkpoint (Custom Domains)

**Time estimate:** 2-3 hours

**Deliverables:**

- [ ] **Exercise 3.3 completed**: Custom domains
  - [ ] `difficulty_level` domain created
  - [ ] `question_marks` domain created
  - [ ] `academic_year` domain created (optional)

- [ ] **Custom domains tested**
  ```sql
  -- Create test table using domains
  CREATE TABLE test_questions (
      id SERIAL PRIMARY KEY,
      difficulty difficulty_level,
      marks question_marks
  );
  
  -- This should work
  INSERT INTO test_questions (difficulty, marks) VALUES ('easy', 10);
  
  -- This should fail
  INSERT INTO test_questions (difficulty, marks) VALUES ('invalid', 150);
  
  -- Cleanup
  DROP TABLE test_questions;
  ```

- [ ] **Constraints documented**
  - [ ] List all CHECK constraints and their rules
  - [ ] List all UNIQUE constraints
  - [ ] List all custom domains
  - [ ] Save in `constraints.sql` file

**Self-check questions:**
1. What's the advantage of custom domains over CHECK constraints? _____
2. Can you modify a domain after creation? _____
3. Where would you use custom domains in CourseDB-AI? _____

**Day 3 Complete:** Your database enforces data integrity! ✅

---

## Day 4: Stored Procedures and Functions ✅

### Morning Checkpoint (Functions)

**Time estimate:** 2-3 hours

**Deliverables:**

- [ ] **Exercise 4.1 completed**: Function returning single value
  - [ ] `get_course_question_count()` function created
  - [ ] Function tested with multiple courses
  - [ ] Function returns correct counts

- [ ] **Function tested in queries**
  ```sql
  SELECT
      course_id,
      course_code,
      get_course_question_count(course_id) as question_count
  FROM courses
  LIMIT 5;
  ```

- [ ] **Additional utility functions created**
  - [ ] `get_course_avg_marks()` function
  - [ ] At least one more analytics function
  - [ ] All functions tested

- [ ] **Functions handle NULL correctly**
  ```sql
  -- Test with course that has no questions
  SELECT get_course_question_count(999);
  -- Should return 0, not NULL
  ```

**Self-check questions:**
1. How do you call a function in a SELECT query? _____
2. What does RETURNS INTEGER mean? _____
3. Why use COALESCE in functions? _____

### Afternoon Checkpoint (Functions Returning Tables & Procedures)

**Time estimate:** 2-3 hours

**Deliverables:**

- [ ] **Exercise 4.2 completed**: Function returning table
  - [ ] `get_course_topics_with_stats()` function created
  - [ ] Function returns multiple columns
  - [ ] Can query like a table

- [ ] **Table-returning function tested**
  ```sql
  SELECT * FROM get_course_topics_with_stats(1);
  -- Should return: topic_id, topic_name, question_count, avg_marks
  
  -- Use in JOIN
  SELECT c.course_code, t.topic_name, t.question_count
  FROM courses c
  CROSS JOIN LATERAL get_course_topics_with_stats(c.course_id) t
  WHERE c.course_id = 1;
  ```

- [ ] **Exercise 4.3 completed**: Archive procedure
  - [ ] `archived_questions` table created
  - [ ] `archive_old_questions()` procedure created
  - [ ] Procedure tested (with small year threshold first!)

- [ ] **Procedure tested safely**
  ```sql
  -- Start transaction for testing
  BEGIN;
      -- Archive questions older than 2010
      CALL archive_old_questions(2010);
      
      -- Verify archived
      SELECT COUNT(*) FROM archived_questions;
      
      -- Verify deleted from main table
      SELECT COUNT(*) FROM questions WHERE year < 2010;
      -- Should be 0
  ROLLBACK;  -- Undo for safety
  ```

- [ ] **Functions and procedures documented**
  - [ ] List all functions with signatures
  - [ ] Document what each returns
  - [ ] Save in `functions.sql` file

**Self-check questions:**
1. What's the difference between FUNCTION and PROCEDURE? _____
2. How do you call a procedure? _____
3. Can procedures return values? _____

**Day 4 Complete:** You can encapsulate logic in the database! ✅

---

## Day 5: Common Table Expressions ✅

### Morning Checkpoint (Basic CTEs)

**Time estimate:** 2-3 hours

**Deliverables:**

- [ ] **Exercise 5.1 completed**: Basic CTE
  - [ ] Difficulty distribution CTE working
  - [ ] Results showing easy/medium/hard counts
  - [ ] Query returns correct data

- [ ] **Basic CTE tested**
  ```sql
  -- Copy your CTE query and run it
  -- Verify output makes sense
  ```

- [ ] **Exercise 5.2 completed**: Multiple CTEs
  - [ ] 4 CTEs chained together
  - [ ] Final SELECT joins all CTEs
  - [ ] Results showing comprehensive stats

- [ ] **Multiple CTEs tested**
  ```sql
  -- Run your multi-CTE query
  -- Verify each stat is correct by comparing with individual queries
  
  -- For example, verify question count
  SELECT course_id, COUNT(*) FROM questions GROUP BY course_id;
  -- Should match total_questions in your CTE result
  ```

**Self-check questions:**
1. What's the syntax structure of a CTE? _____
2. Can you reference one CTE from another? (Yes/No)
3. When are CTEs better than subqueries? _____

### Afternoon Checkpoint (Recursive CTEs)

**Time estimate:** 2-3 hours

**Deliverables:**

- [ ] **Hierarchical data prepared**
  - [ ] `parent_topic_id` column added to topics (if needed)
  - [ ] Some hierarchical topics created
  - [ ] Parent-child relationships verified

- [ ] **Exercise 5.3 completed**: Recursive CTE
  - [ ] Recursive CTE created
  - [ ] Base case (anchor) working
  - [ ] Recursive case working
  - [ ] Termination condition present

- [ ] **Recursive CTE tested**
  ```sql
  -- Run your recursive topic hierarchy query
  -- Verify hierarchy displays correctly
  -- Check indentation shows levels
  ```

- [ ] **Number sequence CTE created**
  ```sql
  WITH RECURSIVE years AS (
      SELECT 2020 as year
      UNION ALL
      SELECT year + 1 FROM years WHERE year < 2024
  )
  SELECT * FROM years;
  -- Should return: 2020, 2021, 2022, 2023, 2024
  ```

- [ ] **Advanced queries saved**
  - [ ] All CTE queries saved to `advanced_queries.sql`
  - [ ] Comments explaining each query
  - [ ] Queries formatted and readable

**Self-check questions:**
1. What are the two parts of a recursive CTE? _____
2. Why is a termination condition critical? _____
3. What happens without WHERE clause in recursive part? _____

**Day 5 Complete:** You can write complex analytical queries! ✅

---

## Day 6: Window Functions ✅

### Morning Checkpoint (Ranking Functions)

**Time estimate:** 2-3 hours

**Deliverables:**

- [ ] **Exercise 6.1 completed**: ROW_NUMBER()
  - [ ] Questions ranked within each course
  - [ ] PARTITION BY working correctly
  - [ ] Top 3 questions per course query working

- [ ] **ROW_NUMBER tested**
  ```sql
  -- Run your ranking query
  -- Verify rank resets for each course
  -- Verify ties get different row numbers
  ```

- [ ] **Exercise 6.2 completed**: RANK() and DENSE_RANK()
  - [ ] Courses ranked by question count
  - [ ] Understand difference between RANK and DENSE_RANK
  - [ ] PERCENT_RANK working

- [ ] **Ranking functions compared**
  ```sql
  -- Compare ROW_NUMBER vs RANK vs DENSE_RANK on same data
  WITH test_data AS (
      SELECT course_code, COUNT(*) as q_count FROM courses c
      LEFT JOIN questions q ON c.course_id = q.course_id
      GROUP BY course_code
  )
  SELECT
      course_code,
      q_count,
      ROW_NUMBER() OVER (ORDER BY q_count DESC) as row_num,
      RANK() OVER (ORDER BY q_count DESC) as rank,
      DENSE_RANK() OVER (ORDER BY q_count DESC) as dense_rank
  FROM test_data;
  -- Observe differences with ties
  ```

**Self-check questions:**
1. What does PARTITION BY do? _____
2. What's the difference between RANK() and DENSE_RANK()? _____
3. How do you get top N per group? _____

### Afternoon Checkpoint (LAG/LEAD and Aggregations)

**Time estimate:** 2-3 hours

**Deliverables:**

- [ ] **Exercise 6.3 completed**: LAG() and LEAD()
  - [ ] Year-over-year comparison working
  - [ ] LAG returning previous row values
  - [ ] LEAD returning next row values
  - [ ] YoY change calculated correctly

- [ ] **LAG/LEAD tested**
  ```sql
  -- Run your year-over-year query
  -- Verify:
  -- - First row has NULL for prev_year_count
  -- - Last row has NULL for next_year_count
  -- - YoY change calculations are correct
  ```

- [ ] **Exercise 6.4 completed**: Running totals
  - [ ] Running total calculated correctly
  - [ ] Running average working
  - [ ] Moving average (last 3) working

- [ ] **Aggregation window functions tested**
  ```sql
  -- Verify running total increases monotonically
  -- Verify running average makes sense
  -- Verify moving average changes correctly
  ```

- [ ] **Window functions saved**
  - [ ] All queries saved to `window_functions.sql`
  - [ ] Each query commented with purpose
  - [ ] Complex queries have examples

**Self-check questions:**
1. What does ROWS BETWEEN do? _____
2. What's the difference between window aggregate and GROUP BY? _____
3. When would you use LAG/LEAD? _____

**Day 6 Complete:** You can perform advanced analytics! ✅

---

## Day 7: Integration and Practice ✅

### Morning Checkpoint (Comprehensive Analytics)

**Time estimate:** 2-3 hours

**Deliverables:**

- [ ] **Master dashboard view created**
  - [ ] Combines CTEs, window functions, aggregations
  - [ ] Shows comprehensive course statistics
  - [ ] Queryable like a regular view

- [ ] **Dashboard tested**
  ```sql
  SELECT * FROM course_master_dashboard ORDER BY question_rank LIMIT 5;
  -- Should show top 5 courses with all metrics
  ```

- [ ] **Comprehensive report query created**
  - [ ] Uses recursive CTE for hierarchy
  - [ ] Includes question analytics per topic
  - [ ] Ranks topics by popularity

**Self-check questions:**
1. How many advanced SQL features does your dashboard use? _____
2. Can you explain the query to someone else? (Yes/No)
3. What would you improve about the dashboard? _____

### Afternoon Checkpoint (Final Integration)

**Time estimate:** 2-3 hours

**Deliverables:**

- [ ] **Challenge 1 attempted**: Complete analytics system
  - [ ] Course performance metrics
  - [ ] Question difficulty analysis
  - [ ] Topic coverage report
  - [ ] Historical trends
  - [ ] All saved in `analytics_system.sql`

- [ ] **Challenge 2 attempted** (optional): Audit system
  - [ ] Generic audit trigger function
  - [ ] Applied to multiple tables
  - [ ] Query interface for viewing changes

- [ ] **Indexes created for performance**
  ```sql
  CREATE INDEX idx_questions_course_difficulty 
  ON questions(course_id, difficulty);
  
  CREATE INDEX idx_questions_year 
  ON questions(year) WHERE year IS NOT NULL;
  
  CREATE INDEX idx_audit_log_timestamp 
  ON audit_log(changed_at);
  
  -- Verify indexes exist
  \di+ idx_questions_*
  ```

- [ ] **Database objects documented**
  ```sql
  -- Run this query and save output
  SELECT
      'VIEW' as type, table_name as name
  FROM information_schema.views
  WHERE table_schema = 'public'
  UNION ALL
  SELECT
      'FUNCTION', routine_name
  FROM information_schema.routines
  WHERE routine_schema = 'public' AND routine_type = 'FUNCTION'
  UNION ALL
  SELECT
      'TRIGGER', trigger_name
  FROM information_schema.triggers
  WHERE trigger_schema = 'public'
  ORDER BY type, name;
  ```

- [ ] **All SQL files organized**
  - [ ] `views.sql` - All view definitions
  - [ ] `triggers.sql` - All trigger definitions
  - [ ] `constraints.sql` - All constraints
  - [ ] `functions.sql` - All functions/procedures
  - [ ] `advanced_queries.sql` - CTE examples
  - [ ] `window_functions.sql` - Window function examples
  - [ ] `analytics_system.sql` - Complete analytics

**Day 7 Complete:** Week 6 is done! 🎉

---

## Week 6 Final Self-Assessment

### Features Implemented

**Views:**
- [ ] At least 3 regular views created
- [ ] At least 1 materialized view created
- [ ] All views tested and documented

**Triggers:**
- [ ] Audit triggers on major tables
- [ ] Validation triggers working
- [ ] Timestamp triggers implemented
- [ ] All triggers tested

**Constraints:**
- [ ] CHECK constraints on appropriate columns
- [ ] UNIQUE constraints for business keys
- [ ] Custom domains created (optional)
- [ ] All constraints tested

**Stored Procedures/Functions:**
- [ ] At least 3 functions returning values
- [ ] At least 1 function returning table
- [ ] At least 1 procedure created
- [ ] All tested and documented

**CTEs:**
- [ ] At least 3 queries using basic CTEs
- [ ] At least 1 recursive CTE
- [ ] All saved and documented

**Window Functions:**
- [ ] ROW_NUMBER() examples working
- [ ] RANK/DENSE_RANK examples working
- [ ] LAG/LEAD examples working
- [ ] Running totals working
- [ ] At least 10 window function queries total

### Knowledge Check

**Confidence Rating (1-5):**
- [ ] Views: _____ / 5
- [ ] Materialized Views: _____ / 5
- [ ] Triggers: _____ / 5
- [ ] Constraints: _____ / 5
- [ ] Functions: _____ / 5
- [ ] Procedures: _____ / 5
- [ ] CTEs: _____ / 5
- [ ] Recursive CTEs: _____ / 5
- [ ] Window Functions: _____ / 5

**Can you explain these concepts?**
- [ ] When to use materialized vs regular view
- [ ] BEFORE vs AFTER triggers
- [ ] Database validation vs application validation
- [ ] Function vs procedure
- [ ] CTE vs subquery
- [ ] Window function vs GROUP BY
- [ ] ROW_NUMBER vs RANK vs DENSE_RANK
- [ ] When to use recursive CTE

**Can you debug these issues?**
- [ ] View not updatable
- [ ] Trigger causing infinite loop
- [ ] Constraint violation on existing data
- [ ] Function returning NULL unexpectedly
- [ ] Recursive CTE not terminating
- [ ] Window function in WHERE clause error

### Deliverables Checklist

**SQL Files:**
- [ ] `views.sql` (all view definitions)
- [ ] `triggers.sql` (all trigger definitions)
- [ ] `constraints.sql` (all constraints)
- [ ] `functions.sql` (all functions/procedures)
- [ ] `advanced_queries.sql` (CTE examples)
- [ ] `window_functions.sql` (window function examples)
- [ ] `analytics_system.sql` (complete analytics)

**Documentation:**
- [ ] Database objects summary document
- [ ] Purpose of each view documented
- [ ] Trigger behavior explained
- [ ] Function signatures documented
- [ ] Complex queries have comments

**Testing:**
- [ ] All views queryable
- [ ] All triggers fire correctly
- [ ] All constraints prevent invalid data
- [ ] All functions return correct results
- [ ] All queries optimized

### Reflection

**Completed reflection.md prompts:**
- [ ] At least 5 reflection prompts completed
- [ ] Identified most useful features
- [ ] Identified areas needing more practice
- [ ] Created action items for next steps

**Time Tracking:**

| Day | Planned Hours | Actual Hours | Completed? |
|-----|---------------|--------------|------------|
| 1   | 4-6           | _____        | [ ]        |
| 2   | 4-6           | _____        | [ ]        |
| 3   | 4-6           | _____        | [ ]        |
| 4   | 4-6           | _____        | [ ]        |
| 5   | 4-6           | _____        | [ ]        |
| 6   | 4-6           | _____        | [ ]        |
| 7   | 4-6           | _____        | [ ]        |

**Total time spent:** _____ hours

---

## Ready for Week 7?

**Prerequisites for Week 7 (Indexing):**
- [ ] All Week 6 checkpoints completed
- [ ] Advanced SQL features working in CourseDB-AI
- [ ] Understanding of query performance concepts
- [ ] Confidence rating >= 3/5 for all major features

**If not ready:**
- Review incomplete checkpoints
- Re-read relevant sections in README.md
- Check mistakes_to_expect.md for troubleshooting
- Practice with exercises.md

**If ready:**
- Commit all Week 6 code
- Document your progress
- Take a break! 🎉
- Start Week 7: Indexing (B+ Tree, Hash Index)

---

## Quick Troubleshooting

**If stuck on a checkpoint:**
1. Re-read the relevant exercise in exercises.md
2. Check mistakes_to_expect.md for your specific error
3. Review README.md concepts section
4. Test in small increments (don't write everything at once)
5. Use RAISE NOTICE for debugging
6. Ask for help after 1 hour stuck

**Common issues:**
- "View not updatable" → Review Mistake 1.1
- "Infinite loop" → Review Mistake 2.1
- "Constraint violation" → Review Mistake 3.1
- "Function error" → Review Mistake 4.2
- "Recursive CTE forever" → Review Mistake 5.1
- "Window function in WHERE" → Review Mistake 6.3

---

**Great job completing Week 6! You've mastered advanced SQL features that most developers never learn. These skills will set you apart in the job market! 🚀**

# Week 7: Indexing & B+ Trees - 7-Day Implementation Plan

**Goal**: Master database indexing through hands-on practice, transforming slow queries into fast ones.

**Prerequisites**:
- Week 6 completed (Advanced SQL features working)
- CourseDB-AI database with data
- PostgreSQL access
- Understanding of SELECT queries

---

## Day 1: Index Fundamentals (Monday)

### Morning: Your First Index (2-3 hours)

**Learning Objectives**:
- Understand what indexes are
- Create your first index
- Measure performance improvement
- Use EXPLAIN ANALYZE

**Tasks**:

1. **Read README.md Sections 1-2** (30 min)
   - What is an index?
   - Types of indexes

2. **Complete Exercise 1.1** (30 min):
   ```sql
   -- Measure query without index
   EXPLAIN ANALYZE SELECT * FROM questions WHERE year = 2023;
   
   -- Create index
   CREATE INDEX idx_questions_year ON questions(year);
   
   -- Measure again
   EXPLAIN ANALYZE SELECT * FROM questions WHERE year = 2023;
   
   -- Calculate speedup
   ```

3. **Understand EXPLAIN output** (45 min):
   ```sql
   -- Practice reading EXPLAIN ANALYZE
   -- Identify: Seq Scan vs Index Scan
   -- Understand: cost, rows, time metrics
   ```

4. **Complete Exercise 1.2** (20 min):
   - Measure index storage size
   - Understand space/performance trade-off

**Checkpoint**: Can you create an index and measure its impact? ✅

### Afternoon: B+ Tree Structure (2-3 hours)

**Tasks**:

1. **Read README.md Section 3** (45 min):
   - B+ tree structure
   - Why B+ trees for databases
   - Operations: search, insert, delete

2. **Draw a B+ tree** (45 min):
   ```
   Manual exercise: Draw B+ tree for values [5, 10, 15, 20, 25, 30]
   Order = 3 (max 2 keys per node)
   
   Practice:
   - Insert 35
   - Search for 20
   - Delete 10
   ```

3. **Visualize queries on B+ tree** (30 min):
   ```sql
   -- Single value search
   SELECT * FROM questions WHERE year = 2023;
   -- Trace path through tree
   
   -- Range query
   SELECT * FROM questions WHERE year BETWEEN 2020 AND 2023;
   -- How does B+ tree handle this efficiently?
   ```

4. **Complete Exercise 1.3** (30 min):
   - Compare different scan types
   - Understand when each is used

**Day 1 Deliverable**:
- [ ] First index created and tested
- [ ] Understand EXPLAIN ANALYZE output
- [ ] Can explain B+ tree structure
- [ ] Document speedup achieved: _____x

**Evening Reflection** (30 min):
- What surprised you about indexes?
- How much speedup did you achieve?
- Draw a B+ tree from memory

---

## Day 2: Composite Indexes (Tuesday)

### Morning: Leftmost Prefix Rule (2-3 hours)

**Learning Objectives**:
- Master composite indexes
- Understand leftmost prefix rule
- Choose correct column order

**Tasks**:

1. **Read README.md Section 4** (20 min):
   - Composite indexes
   - Leftmost prefix rule

2. **Complete Exercise 2.1** (45 min):
   ```sql
   CREATE INDEX idx_year_diff_marks 
   ON questions(year, difficulty, marks);
   
   -- Test which queries use the index:
   WHERE year = 2023                          -- ✅
   WHERE year = 2023 AND difficulty = 'hard'  -- ✅
   WHERE difficulty = 'hard'                  -- ❌
   WHERE year = 2023 AND marks = 10           -- ✅ (partial)
   ```

3. **Experiment with column order** (60 min):
   ```sql
   -- Create idx(year, difficulty)
   -- vs idx(difficulty, year)
   
   -- Test both with your query patterns
   -- Measure which performs better
   ```

4. **Complete Exercise 2.2** (30 min):
   - Choose index column order for real queries
   - Document decision rationale

**Checkpoint**: Can you predict which queries use composite index? ✅

### Afternoon: Multiple Indexes vs Composite (2-3 hours)

**Tasks**:

1. **Complete Exercise 2.3** (45 min):
   ```sql
   -- Option A: Two indexes
   CREATE INDEX idx_year ON questions(year);
   CREATE INDEX idx_difficulty ON questions(difficulty);
   
   -- Option B: One composite
   CREATE INDEX idx_year_difficulty ON questions(year, difficulty);
   
   -- Compare for query: WHERE year = 2023 AND difficulty = 'hard'
   ```

2. **Analyze your query patterns** (60 min):
   ```sql
   -- List all queries in your app
   -- Identify common WHERE conditions
   -- Design index strategy
   
   -- Example query log:
   -- 60% - WHERE year = X
   -- 30% - WHERE year = X AND difficulty = Y
   -- 10% - WHERE difficulty = Y
   
   -- Best index? _____
   ```

3. **Create indexes for CourseDB-AI** (45 min):
   ```sql
   -- Based on your analysis, create indexes for:
   -- - questions table
   -- - courses table
   -- - topics table
   ```

**Day 2 Deliverable**:
- [ ] Understand leftmost prefix rule
- [ ] Can choose composite column order
- [ ] Created 3+ indexes for CourseDB-AI
- [ ] Documented index strategy

**Evening Task**: Review mistakes_to_expect.md sections on composite indexes

---

## Day 3: Covering Indexes (Wednesday)

### Morning: Index-Only Scans (2-3 hours)

**Learning Objectives**:
- Achieve Index Only Scan
- Create covering indexes
- Maximize query performance

**Tasks**:

1. **Read README.md Section 5** (20 min):
   - Covering indexes
   - Index Only Scan

2. **Complete Exercise 3.1** (60 min):
   ```sql
   -- Goal: Analytics query with Index Only Scan
   
   -- Query:
   SELECT year, difficulty, COUNT(*), AVG(marks)
   FROM questions
   GROUP BY year, difficulty;
   
   -- Create covering index
   CREATE INDEX idx_questions_analytics
   ON questions(year, difficulty, marks);
   
   -- Verify: EXPLAIN should show Index Only Scan
   -- Heap Fetches: 0
   ```

3. **Find opportunities for covering indexes** (60 min):
   ```sql
   -- Review your app's queries
   -- Identify queries accessing few columns
   
   -- Example:
   SELECT course_code, title FROM courses WHERE status = 'active';
   
   -- Covering index:
   CREATE INDEX idx_courses_active
   ON courses(status, course_code, title);
   ```

4. **Measure improvements** (30 min):
   ```sql
   -- Before: Regular index
   -- After: Covering index
   -- Calculate speedup
   ```

**Checkpoint**: Can you achieve Index Only Scan? ✅

### Afternoon: INCLUDE Columns (2-3 hours)

**Tasks**:

1. **Complete Exercise 3.2** (45 min):
   ```sql
   -- Use INCLUDE for non-key columns
   CREATE INDEX idx_year_include_marks
   ON questions(year) INCLUDE (marks);
   
   -- Benefits:
   -- - marks not part of key (smaller internal nodes)
   -- - Still enables Index Only Scan
   ```

2. **Create covering indexes for common queries** (90 min):
   ```sql
   -- Query 1: Course search
   SELECT course_code, title, credits
   FROM courses
   WHERE status = 'active';
   
   -- Covering index:
   CREATE INDEX idx_courses_active_cover
   ON courses(status) INCLUDE (course_code, title, credits);
   
   -- Query 2: Question search
   SELECT question_id, question_text, marks
   FROM questions
   WHERE year = 2023 AND difficulty = 'hard';
   
   -- Covering index:
   CREATE INDEX idx_questions_search_cover
   ON questions(year, difficulty) INCLUDE (question_text, marks);
   ```

3. **Benchmark improvements** (30 min):
   - Measure all queries before/after covering indexes
   - Document speedups

**Day 3 Deliverable**:
- [ ] 3+ covering indexes created
- [ ] Achieved Index Only Scan for key queries
- [ ] Measured speedups: _____x average
- [ ] Documented covering index strategy

---

## Day 4: Partial Indexes (Thursday)

### Morning: Filtered Indexes (2-3 hours)

**Learning Objectives**:
- Create partial indexes
- Reduce index size
- Optimize for specific queries

**Tasks**:

1. **Read README.md Section 4 (Partial Indexes)** (20 min)

2. **Complete Exercise 4.1** (60 min):
   ```sql
   -- Scenario: 90% of queries search recent data
   
   -- Full index (large)
   CREATE INDEX idx_year_full ON questions(year);
   
   -- Partial index (smaller, faster)
   CREATE INDEX idx_year_recent ON questions(year)
   WHERE year >= 2020;
   
   -- Compare sizes:
   SELECT pg_size_pretty(pg_relation_size('idx_year_full'));
   SELECT pg_size_pretty(pg_relation_size('idx_year_recent'));
   ```

3. **Complete Exercise 4.2** (60 min):
   ```sql
   -- Common filter: hard questions
   CREATE INDEX idx_hard_questions
   ON questions(question_id)
   WHERE difficulty = 'hard';
   
   -- Benefits:
   -- - 3x smaller than full index
   -- - Faster for hard question queries
   ```

4. **Identify partial index opportunities** (30 min):
   ```sql
   -- Look for:
   -- - Status filters (WHERE status = 'active')
   -- - Date ranges (WHERE created_at > '2023-01-01')
   -- - Boolean flags (WHERE is_published = true)
   
   -- Create partial indexes for these
   ```

**Checkpoint**: Can you create and use partial indexes? ✅

### Afternoon: Index Strategy Refinement (2-3 hours)

**Tasks**:

1. **Audit current indexes** (60 min):
   ```sql
   -- List all indexes
   SELECT tablename, indexname, pg_size_pretty(pg_relation_size(indexrelid))
   FROM pg_stat_user_indexes
   WHERE schemaname = 'public';
   
   -- Check which are used
   SELECT indexname, idx_scan
   FROM pg_stat_user_indexes
   WHERE schemaname = 'public'
   ORDER BY idx_scan ASC;
   ```

2. **Find unused indexes** (45 min):
   ```sql
   -- Unused indexes (idx_scan = 0)
   SELECT indexname, pg_size_pretty(pg_relation_size(indexrelid))
   FROM pg_stat_user_indexes
   WHERE schemaname = 'public'
     AND idx_scan = 0
     AND indexrelid NOT IN (
         SELECT conindid FROM pg_constraint WHERE contype IN ('p', 'u')
     );
   
   -- DROP unused indexes
   ```

3. **Optimize index strategy** (45 min):
   ```sql
   -- Replace full indexes with partial where appropriate
   -- Combine multiple indexes into composite
   -- Add covering indexes for hot queries
   ```

**Day 4 Deliverable**:
- [ ] 2+ partial indexes created
- [ ] Unused indexes identified and dropped
- [ ] Index strategy documented
- [ ] Total index size reduced by _____% 

---

## Day 5: Query Optimization (Friday)

### Morning: EXPLAIN ANALYZE Mastery (2-3 hours)

**Learning Objectives**:
- Master EXPLAIN ANALYZE
- Identify query bottlenecks
- Optimize slow queries

**Tasks**:

1. **Read EXPLAIN documentation** (30 min):
   - Scan types: Seq Scan, Index Scan, Index Only Scan
   - Cost estimation
   - Actual time metrics

2. **Practice reading EXPLAIN** (60 min):
   ```sql
   -- For each query type, run EXPLAIN ANALYZE:
   
   -- Simple filter
   EXPLAIN ANALYZE
   SELECT * FROM questions WHERE year = 2023;
   
   -- Join
   EXPLAIN ANALYZE
   SELECT c.course_code, COUNT(q.question_id)
   FROM courses c
   LEFT JOIN questions q ON c.course_id = q.course_id
   GROUP BY c.course_code;
   
   -- Complex analytics
   EXPLAIN ANALYZE
   SELECT year, difficulty, AVG(marks)
   FROM questions
   WHERE year BETWEEN 2020 AND 2023
   GROUP BY year, difficulty
   ORDER BY year DESC, difficulty;
   
   -- Identify bottlenecks in each
   ```

3. **Complete Exercise 5.1** (60 min):
   ```sql
   -- Optimize slow analytics query
   -- See exercises.md for full query
   
   -- Steps:
   -- 1. Measure baseline
   -- 2. Identify bottlenecks with EXPLAIN
   -- 3. Create indexes
   -- 4. Remeasure
   -- 5. Document improvement
   ```

**Checkpoint**: Can you identify and fix slow queries? ✅

### Afternoon: Real-World Optimization (2-3 hours)

**Tasks**:

1. **Find slowest queries in your app** (45 min):
   ```sql
   -- Enable query logging (if not already)
   -- Review application logs
   -- Identify top 5 slowest queries
   ```

2. **Optimize each query** (90 min):
   ```sql
   -- For each slow query:
   -- 1. Run EXPLAIN ANALYZE (baseline)
   -- 2. Identify bottleneck
   -- 3. Create appropriate index
   -- 4. Verify improvement
   -- 5. Document results
   
   -- Example:
   -- Query: Dashboard analytics
   -- Before: 2500ms (Seq Scan)
   -- Index: idx_questions_year_course
   -- After: 25ms (Index Scan)
   -- Speedup: 100x
   ```

3. **Document optimization results** (30 min):
   ```
   # Query Optimization Report
   
   ## Query 1: [Name]
   - Original time: ___ ms
   - Bottleneck: ___
   - Index created: ___
   - New time: ___ ms
   - Speedup: ___x
   
   ## Query 2: [Name]
   ...
   ```

**Day 5 Deliverable**:
- [ ] Top 5 slow queries identified
- [ ] All queries optimized
- [ ] Average speedup: _____x
- [ ] Optimization report created

---

## Day 6: Advanced Indexing (Saturday)

### Morning: Hash Indexes and Special Types (2-3 hours)

**Tasks**:

1. **Complete Exercise 6.1** (45 min):
   ```sql
   -- Compare B+ tree vs hash index
   
   -- B+ tree (default)
   CREATE INDEX idx_code_btree ON courses(course_code);
   EXPLAIN ANALYZE
   SELECT * FROM courses WHERE course_code = 'CS201';
   
   -- Hash index
   CREATE INDEX idx_code_hash ON courses USING HASH (course_code);
   EXPLAIN ANALYZE
   SELECT * FROM courses WHERE course_code = 'CS201';
   
   -- Compare performance
   ```

2. **Experiment with GIN indexes** (60 min):
   ```sql
   -- If you have JSONB columns or arrays
   
   -- Add JSONB column to questions
   ALTER TABLE questions ADD COLUMN metadata JSONB;
   
   -- Update with sample data
   UPDATE questions SET metadata = '{"tags": ["sql", "database"], "reviewed": true}';
   
   -- Create GIN index
   CREATE INDEX idx_metadata_gin ON questions USING GIN (metadata);
   
   -- Query JSONB
   EXPLAIN ANALYZE
   SELECT * FROM questions WHERE metadata @> '{"reviewed": true}';
   ```

3. **Learn about expression indexes** (45 min):
   ```sql
   -- Index on expression
   CREATE INDEX idx_lower_difficulty
   ON questions(LOWER(difficulty));
   
   -- Now this query uses index:
   SELECT * FROM questions WHERE LOWER(difficulty) = 'hard';
   ```

**Checkpoint**: Can you use different index types? ✅

### Afternoon: Complete Challenge Exercises (2-3 hours)

**Tasks**:

1. **Challenge 1: Full indexing strategy** (90 min):
   - Design complete index strategy for CourseDB-AI
   - Create all necessary indexes
   - Document rationale for each
   - Test with real queries

2. **Challenge 2: Query optimization competition** (60 min):
   - Optimize the complex query from exercises.md
   - Get execution time as low as possible
   - Document your approach

**Day 6 Deliverable**:
- [ ] Hash index tested and compared
- [ ] GIN index created (if applicable)
- [ ] Expression index tested
- [ ] Both challenges completed
- [ ] indexing_strategy.sql created

---

## Day 7: Integration and Review (Sunday)

### Morning: Production-Ready Indexing (2-3 hours)

**Tasks**:

1. **Final index audit** (60 min):
   ```sql
   -- Review all indexes
   SELECT
       tablename,
       indexname,
       pg_size_pretty(pg_relation_size(indexrelid)) as size,
       idx_scan as scans
   FROM pg_stat_user_indexes
   WHERE schemaname = 'public'
   ORDER BY tablename, idx_scan DESC;
   
   -- Check for:
   -- - Unused indexes (drop them)
   -- - Duplicate indexes (keep best one)
   -- - Missing indexes (add them)
   ```

2. **Benchmark entire application** (60 min):
   ```sql
   -- Run all API endpoints
   -- Measure response times
   -- Verify indexes are being used
   
   -- Example metrics:
   -- GET /courses: 15ms → 5ms (3x faster)
   -- GET /questions?year=2023: 250ms → 10ms (25x faster)
   -- GET /analytics: 5000ms → 100ms (50x faster)
   ```

3. **Document final index strategy** (30 min):
   ```sql
   -- Create comprehensive documentation
   -- Include:
   -- - All indexes and their purpose
   -- - Expected query patterns
   -- - Maintenance recommendations
   -- - Performance benchmarks
   ```

**Checkpoint**: Is your indexing strategy production-ready? ✅

### Afternoon: Learning Review and Documentation (2-3 hours)

**Tasks**:

1. **Complete reflection.md** (60 min):
   - Answer all reflection prompts
   - Document key learnings
   - Identify areas for more practice

2. **Create index maintenance plan** (45 min):
   ```sql
   -- Document how to:
   -- - Monitor index usage
   -- - Rebuild indexes periodically
   -- - Add new indexes as queries evolve
   -- - Remove unused indexes
   
   -- Example schedule:
   -- Weekly: Check slow queries
   -- Monthly: Review index usage statistics
   -- Quarterly: Rebuild indexes (REINDEX)
   ```

3. **Final testing** (45 min):
   ```sql
   -- Run comprehensive test suite
   -- Verify all queries work correctly
   -- Confirm performance targets met
   -- Test with large data volumes
   ```

**Day 7 Deliverable**:
- [ ] All indexes documented
- [ ] Performance benchmarks recorded
- [ ] Index maintenance plan created
- [ ] Reflection completed
- [ ] Week 7 complete! 🎉

---

## Week 7 Final Deliverables Checklist

### Indexes Created:
- [ ] **questions table**: 3+ indexes
- [ ] **courses table**: 2+ indexes  
- [ ] **topics table**: 1+ index
- [ ] **At least 1 covering index**
- [ ] **At least 1 partial index**
- [ ] **All indexes tested and working**

### Performance Improvements:
- [ ] Key queries identified and optimized
- [ ] Average speedup: _____x
- [ ] Before/after metrics documented
- [ ] No unused indexes remaining

### Documentation:
- [ ] `indexing_strategy.sql` - All index definitions
- [ ] `optimization_report.md` - Performance results
- [ ] `maintenance_plan.md` - Ongoing maintenance
- [ ] Reflection completed

### Knowledge Mastery:
- [ ] Can create any type of index
- [ ] Can read EXPLAIN ANALYZE output
- [ ] Can identify when indexes are used
- [ ] Can optimize slow queries
- [ ] Understand index trade-offs
- [ ] Can design indexing strategy

---

## Time Tracking Template

| Day | Planned Hours | Actual Hours | Completed? | Notes |
|-----|---------------|--------------|------------|-------|
| 1   | 4-6           |              | [ ]        |       |
| 2   | 4-6           |              | [ ]        |       |
| 3   | 4-6           |              | [ ]        |       |
| 4   | 4-6           |              | [ ]        |       |
| 5   | 4-6           |              | [ ]        |       |
| 6   | 4-6           |              | [ ]        |       |
| 7   | 4-6           |              | [ ]        |       |

**Total time**: _____ hours

---

## Tips for Success

1. **Measure everything**: Always use EXPLAIN ANALYZE before and after
2. **Start simple**: Single-column indexes before composite
3. **Be patient**: Query planning takes time, results are cached
4. **Clear cache when testing**: 
   ```sql
   DISCARD ALL;  -- Clear PostgreSQL cache
   ```
5. **Test with real data**: Small datasets may not show index benefits
6. **Document as you go**: Record all speedups and decisions
7. **Don't over-index**: More indexes ≠ better performance

---

## Resources

- PostgreSQL EXPLAIN: https://www.postgresql.org/docs/current/using-explain.html
- Index Types: https://www.postgresql.org/docs/current/indexes-types.html
- Index Usage: https://www.postgresql.org/docs/current/indexes-usage.html
- Performance Tips: https://wiki.postgresql.org/wiki/Performance_Optimization

---

**Ready to transform your database performance? Let's build lightning-fast queries! ⚡**

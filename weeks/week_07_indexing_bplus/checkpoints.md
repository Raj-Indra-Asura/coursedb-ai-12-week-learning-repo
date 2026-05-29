# Week 7: Indexing & B+ Trees - Daily Checkpoints

## 🎯 Purpose

Track your daily progress through Week 7 with concrete, measurable checkpoints. Each day has specific deliverables you can verify.

**How to use this document:**
- [ ] Check off items as you complete them
- [ ] Verify each checkpoint before moving to next day
- [ ] Don't skip checkpoints—they build on each other
- [ ] Record your speedups and learnings

---

## Day 1: Index Fundamentals ✅

### Morning Checkpoint (Your First Index)

**Time estimate:** 2-3 hours

**Deliverables:**

- [ ] **PostgreSQL connection verified**
  ```bash
  psql -U coursedb_user -d coursedb_dev -c "SELECT count(*) FROM questions;"
  ```

- [ ] **Exercise 1.1 completed**: First index created
  - [ ] Measured query without index
  - [ ] Created index on year column
  - [ ] Measured query with index
  - [ ] Calculated speedup

- [ ] **Performance measurements recorded:**
  ```
  Query: SELECT * FROM questions WHERE year = 2023;
  
  Without index:
  - Scan type: Seq Scan
  - Execution time: _____ ms
  
  With index:
  - Scan type: Index Scan
  - Execution time: _____ ms
  
  Speedup: _____x
  ```

- [ ] **Can read EXPLAIN ANALYZE output:**
  - [ ] Identify scan type (Seq Scan vs Index Scan)
  - [ ] Understand cost values
  - [ ] Read actual time metrics

**Self-check questions:**
1. What does "Seq Scan" mean? _____
2. What scan type indicates index is used? _____
3. What was your speedup? _____x

### Afternoon Checkpoint (B+ Tree Structure)

**Time estimate:** 2-3 hours

**Deliverables:**

- [ ] **B+ tree drawing completed:**
  - [ ] Drew B+ tree for values [5, 10, 15, 20, 25, 30]
  - [ ] Labeled internal nodes and leaf nodes
  - [ ] Showed linked leaves
  - [ ] Traced search operation

- [ ] **Exercise 1.3 completed**: Different scan types
  - [ ] Observed Seq Scan
  - [ ] Observed Index Scan
  - [ ] Observed Index Only Scan (if possible)
  - [ ] Understood when each is used

- [ ] **B+ tree concepts understood:**
  - [ ] Why high fanout matters
  - [ ] Why data is only in leaves
  - [ ] How linked leaves enable range queries
  - [ ] Why B+ trees are perfect for databases

**Self-check questions:**
1. What's the benefit of high fanout? _____
2. Why are leaves linked? _____
3. How does B+ tree find a range? _____

**Day 1 Complete:** You understand indexes and can measure their impact! ✅

---

## Day 2: Composite Indexes ✅

### Morning Checkpoint (Leftmost Prefix Rule)

**Time estimate:** 2-3 hours

**Deliverables:**

- [ ] **Exercise 2.1 completed**: Leftmost prefix testing
  - [ ] Created composite index `idx(year, difficulty, marks)`
  - [ ] Tested `WHERE year = X` → uses index ✅
  - [ ] Tested `WHERE year = X AND difficulty = Y` → uses index ✅
  - [ ] Tested `WHERE difficulty = Y` → does NOT use index ✅
  - [ ] Tested `WHERE year = X AND marks = Z` → partially uses index ✅

- [ ] **Leftmost prefix rule mastered:**
  ```
  Given index idx(A, B, C):
  
  Uses index:
  - WHERE A = 1  ✅
  - WHERE A = 1 AND B = 2  ✅
  - WHERE A = 1 AND B = 2 AND C = 3  ✅
  - WHERE A = 1 AND C = 3  ✅ (A only)
  
  Cannot use index:
  - WHERE B = 2  ❌
  - WHERE C = 3  ❌
  - WHERE B = 2 AND C = 3  ❌
  ```

- [ ] **EXPLAIN verified for each query:**
  - [ ] Recorded which queries use index
  - [ ] Understood why some queries can't use index

**Self-check questions:**
1. Can query use index if it skips the first column? (Yes/No)
2. Does WHERE column order matter? (Yes/No - No!)
3. Can you predict which queries use composite index? (Yes/No)

### Afternoon Checkpoint (Index Strategy)

**Time estimate:** 2-3 hours

**Deliverables:**

- [ ] **Exercise 2.2 completed**: Column order decision
  - [ ] Analyzed query patterns for CourseDB-AI
  - [ ] Chose appropriate column order
  - [ ] Documented rationale

- [ ] **Exercise 2.3 completed**: Multiple vs composite
  - [ ] Tested two separate indexes
  - [ ] Tested one composite index
  - [ ] Compared performance for combined query
  - [ ] Made informed decision

- [ ] **CourseDB-AI indexes created:**
  - [ ] At least 1 index on questions table
  - [ ] At least 1 index on courses table
  - [ ] At least 1 composite index
  - [ ] All indexes tested with EXPLAIN

**Query patterns documented:**
```
Common queries:
1. WHERE year = X  (frequency: ____%)
2. WHERE year = X AND difficulty = Y  (frequency: ____%)
3. WHERE difficulty = Y  (frequency: ____%)

Index strategy chosen:
Index: _____
Rationale: _____
```

**Day 2 Complete:** You can design effective composite indexes! ✅

---

## Day 3: Covering Indexes ✅

### Morning Checkpoint (Index-Only Scans)

**Time estimate:** 2-3 hours

**Deliverables:**

- [ ] **Exercise 3.1 completed**: First covering index
  - [ ] Identified query for optimization
  - [ ] Created covering index with all needed columns
  - [ ] Achieved Index Only Scan
  - [ ] Verified Heap Fetches = 0

- [ ] **Index Only Scan achieved:**
  ```sql
  Query: _____
  
  Index created:
  CREATE INDEX _____ ON questions(_____);
  
  EXPLAIN shows:
  - Scan type: Index Only Scan ✅
  - Heap Fetches: 0 ✅
  - Execution time: _____ ms
  
  Speedup vs regular index: _____x
  ```

- [ ] **Covering index opportunities identified:**
  - [ ] Found 3+ queries that access few columns
  - [ ] Listed columns each query needs
  - [ ] Designed covering indexes for each

**Self-check questions:**
1. What is "Heap Fetches"? _____
2. When is Heap Fetches = 0? _____
3. What columns must covering index include? _____

### Afternoon Checkpoint (INCLUDE Columns)

**Time estimate:** 2-3 hours

**Deliverables:**

- [ ] **Exercise 3.2 completed**: INCLUDE syntax
  - [ ] Created index with INCLUDE clause
  - [ ] Understood benefit of INCLUDE
  - [ ] Compared size with regular composite

- [ ] **Covering indexes created:**
  - [ ] At least 3 covering indexes
  - [ ] Each index tested with EXPLAIN
  - [ ] Index Only Scan verified for each
  - [ ] Performance improvements measured

- [ ] **Performance benchmarks recorded:**
  
  | Query | Before (ms) | After (Index Only) | Speedup |
  |-------|-------------|-------------------|---------|
  | Query 1 | _____ | _____ | _____x |
  | Query 2 | _____ | _____ | _____x |
  | Query 3 | _____ | _____ | _____x |
  
  Average speedup: _____x

**Day 3 Complete:** You can achieve Index Only Scans! ✅

---

## Day 4: Partial Indexes ✅

### Morning Checkpoint (Filtered Indexes)

**Time estimate:** 2-3 hours

**Deliverables:**

- [ ] **Exercise 4.1 completed**: First partial index
  - [ ] Created full index, measured size
  - [ ] Created partial index, measured size
  - [ ] Compared sizes
  - [ ] Verified partial index is used

- [ ] **Partial index measurements:**
  ```sql
  Full index size: _____ kB
  Partial index size: _____ kB
  Size reduction: _____x smaller
  
  Partial index:
  CREATE INDEX idx_year_recent ON questions(year)
  WHERE year >= 2020;
  
  Query that uses it:
  SELECT * FROM questions WHERE year = 2023;
  
  EXPLAIN shows: Index Scan using idx_year_recent ✅
  ```

- [ ] **Exercise 4.2 completed**: Common filter index
  - [ ] Created partial index for specific condition
  - [ ] Verified size savings
  - [ ] Tested query performance

**Self-check questions:**
1. When should you use partial index? _____
2. What's the trade-off of partial indexes? _____
3. Name 3 good use cases for partial indexes: _____, _____, _____

### Afternoon Checkpoint (Index Optimization)

**Time estimate:** 2-3 hours

**Deliverables:**

- [ ] **Index usage audited:**
  ```sql
  -- Ran this query:
  SELECT indexname, idx_scan, pg_size_pretty(pg_relation_size(indexrelid))
  FROM pg_stat_user_indexes
  WHERE tablename = 'questions';
  
  -- Results recorded
  ```

- [ ] **Unused indexes identified:**
  - [ ] Found indexes with idx_scan = 0
  - [ ] Determined which are truly unused
  - [ ] Dropped unnecessary indexes

- [ ] **Index strategy optimized:**
  - [ ] Replaced full indexes with partial where appropriate
  - [ ] Combined separate indexes into composite
  - [ ] Removed duplicate/redundant indexes
  - [ ] Documented final index strategy

**Optimization results:**
```
Before optimization:
- Total indexes: _____
- Total size: _____ kB
- Unused indexes: _____

After optimization:
- Total indexes: _____
- Total size: _____ kB
- Space saved: _____ kB (_____%)
```

**Day 4 Complete:** Your indexes are lean and efficient! ✅

---

## Day 5: Query Optimization ✅

### Morning Checkpoint (EXPLAIN Mastery)

**Time estimate:** 2-3 hours

**Deliverables:**

- [ ] **EXPLAIN practice completed:**
  - [ ] Ran EXPLAIN ANALYZE on 10+ different queries
  - [ ] Identified scan types for each
  - [ ] Understood cost estimates
  - [ ] Compared estimated vs actual rows

- [ ] **Exercise 5.1 completed**: Slow query optimization
  - [ ] Measured baseline performance
  - [ ] Identified bottleneck with EXPLAIN
  - [ ] Created appropriate indexes
  - [ ] Remeasured and calculated improvement

- [ ] **Slow query optimization documented:**
  ```
  Query: [Course analytics query]
  
  Before:
  - Scan type: Seq Scan
  - Execution time: _____ ms
  - Bottleneck: No index on year column
  
  Index created: _____
  
  After:
  - Scan type: Index Scan
  - Execution time: _____ ms
  - Speedup: _____x
  ```

**Self-check questions:**
1. What does high "cost" indicate? _____
2. Why compare estimated vs actual rows? _____
3. How do you know if index is being used? _____

### Afternoon Checkpoint (Real-World Optimization)

**Time estimate:** 2-3 hours

**Deliverables:**

- [ ] **Top 5 slow queries identified:**
  1. Query: _____ (time: _____ ms)
  2. Query: _____ (time: _____ ms)
  3. Query: _____ (time: _____ ms)
  4. Query: _____ (time: _____ ms)
  5. Query: _____ (time: _____ ms)

- [ ] **Each query optimized:**
  - [ ] Query 1: Index created, speedup: _____x
  - [ ] Query 2: Index created, speedup: _____x
  - [ ] Query 3: Index created, speedup: _____x
  - [ ] Query 4: Index created, speedup: _____x
  - [ ] Query 5: Index created, speedup: _____x

- [ ] **Optimization report created:**
  - [ ] Documented all optimizations
  - [ ] Recorded before/after metrics
  - [ ] Explained index choices
  - [ ] Calculated overall improvement

**Overall results:**
```
Average query time before: _____ ms
Average query time after: _____ ms
Average speedup: _____x
Total time saved per 1000 requests: _____ seconds
```

**Day 5 Complete:** You can optimize any slow query! ✅

---

## Day 6: Advanced Indexing ✅

### Morning Checkpoint (Hash and Special Indexes)

**Time estimate:** 2-3 hours

**Deliverables:**

- [ ] **Exercise 6.1 completed**: Hash vs B+ tree
  - [ ] Created B+ tree index, tested performance
  - [ ] Created hash index, tested performance
  - [ ] Compared for equality queries
  - [ ] Tested range queries (hash fails)
  - [ ] Made decision: when to use each

- [ ] **Hash index comparison:**
  ```
  Equality query: WHERE course_code = 'CS201'
  - B+ tree time: _____ ms
  - Hash time: _____ ms
  - Winner: _____
  
  Range query: WHERE course_code > 'CS200'
  - B+ tree: Works ✅
  - Hash: Does not work ❌
  
  Conclusion: Use _____ for this use case
  ```

- [ ] **Expression index tested** (if applicable):
  ```sql
  CREATE INDEX idx_lower_difficulty
  ON questions(LOWER(difficulty));
  
  SELECT * FROM questions WHERE LOWER(difficulty) = 'hard';
  -- Uses expression index ✅
  ```

**Self-check questions:**
1. When is hash index faster than B+ tree? _____
2. What can't hash index do? _____
3. When would you use expression index? _____

### Afternoon Checkpoint (Challenge Exercises)

**Time estimate:** 2-3 hours

**Deliverables:**

- [ ] **Challenge 1 completed**: Full indexing strategy
  - [ ] Analyzed all CourseDB-AI queries
  - [ ] Designed comprehensive index strategy
  - [ ] Created all necessary indexes
  - [ ] Tested with real queries
  - [ ] Documented rationale

- [ ] **indexing_strategy.sql created:**
  ```sql
  -- Contains:
  -- - All index definitions
  -- - Comments explaining each index
  -- - Query patterns each index supports
  -- - Performance benchmarks
  ```

- [ ] **Challenge 2 attempted**: Query optimization competition
  - [ ] Optimized complex query
  - [ ] Achieved significant speedup
  - [ ] Documented approach

**Final index strategy:**
```
questions table:
- Index 1: _____ (rationale: _____)
- Index 2: _____ (rationale: _____)
- Index 3: _____ (rationale: _____)

courses table:
- Index 1: _____ (rationale: _____)
- Index 2: _____ (rationale: _____)

topics table:
- Index 1: _____ (rationale: _____)

Total indexes: _____
Total size: _____ kB
All queries optimized: Yes / No
```

**Day 6 Complete:** You have advanced indexing skills! ✅

---

## Day 7: Integration and Review ✅

### Morning Checkpoint (Production-Ready)

**Time estimate:** 2-3 hours

**Deliverables:**

- [ ] **Final index audit completed:**
  ```sql
  SELECT tablename, indexname, pg_size_pretty(pg_relation_size(indexrelid)),
         idx_scan
  FROM pg_stat_user_indexes
  WHERE schemaname = 'public'
  ORDER BY tablename, idx_scan DESC;
  
  -- Verified all indexes are used
  -- Removed any unused indexes
  ```

- [ ] **Application benchmarked:**
  - [ ] All API endpoints tested
  - [ ] Response times measured
  - [ ] Performance improvements documented

- [ ] **Application performance metrics:**
  
  | Endpoint | Before (ms) | After (ms) | Speedup |
  |----------|-------------|-----------|---------|
  | GET /courses | _____ | _____ | _____x |
  | GET /questions?year=X | _____ | _____ | _____x |
  | GET /analytics | _____ | _____ | _____x |
  | POST /questions | _____ | _____ | (_____x slower acceptable) |
  
  Overall speedup: _____x

- [ ] **Index documentation completed:**
  - [ ] All indexes listed with purpose
  - [ ] Query patterns documented
  - [ ] Maintenance plan created
  - [ ] Performance benchmarks recorded

**Self-check questions:**
1. Are there any unused indexes? _____
2. Are write operations acceptably fast? _____
3. Is every index justified and documented? _____

### Afternoon Checkpoint (Review and Mastery)

**Time estimate:** 2-3 hours

**Deliverables:**

- [ ] **Reflection completed:**
  - [ ] Answered 5+ reflection prompts
  - [ ] Documented key learnings
  - [ ] Identified areas needing practice
  - [ ] Created action items

- [ ] **Index maintenance plan created:**
  ```
  Weekly:
  - Check slow query log
  - Review new queries needing indexes
  
  Monthly:
  - Check index usage statistics
  - Drop unused indexes
  
  Quarterly:
  - Rebuild indexes (REINDEX)
  - Audit index strategy
  
  After bulk operations:
  - Run ANALYZE
  - Check statistics accuracy
  ```

- [ ] **Final testing completed:**
  - [ ] All queries work correctly
  - [ ] Performance targets met
  - [ ] No regressions introduced
  - [ ] Tested with realistic data volumes

**Day 7 Complete:** Week 7 is done! 🎉

---

## Week 7 Final Self-Assessment

### Knowledge Check

**Concepts mastered:**
- [ ] What indexes are and why they matter
- [ ] B+ tree structure and operations
- [ ] How to create different types of indexes
- [ ] Leftmost prefix rule for composite indexes
- [ ] How to achieve Index Only Scan
- [ ] When and how to use partial indexes
- [ ] How to read EXPLAIN ANALYZE output
- [ ] How to identify and fix slow queries
- [ ] Index maintenance and monitoring

**Skills acquired:**
- [ ] Can create any type of index
- [ ] Can read and interpret EXPLAIN output
- [ ] Can optimize slow queries systematically
- [ ] Can design comprehensive indexing strategy
- [ ] Can balance read vs write performance
- [ ] Can identify and remove unused indexes
- [ ] Can measure performance improvements

**Confidence rating (1-5):**
- [ ] Creating indexes: _____ / 5
- [ ] Reading EXPLAIN: _____ / 5
- [ ] Composite indexes: _____ / 5
- [ ] Covering indexes: _____ / 5
- [ ] Query optimization: _____ / 5
- [ ] Index strategy: _____ / 5

### Deliverables Checklist

**Indexes created:**
- [ ] questions table: _____+ indexes
- [ ] courses table: _____+ indexes
- [ ] topics table: _____+ index
- [ ] At least 1 composite index
- [ ] At least 1 covering index
- [ ] At least 1 partial index

**Performance improvements:**
- [ ] Average query speedup: _____x
- [ ] Slowest query improvement: _____x
- [ ] All key queries under 100ms
- [ ] Write performance impact documented

**Documentation:**
- [ ] indexing_strategy.sql created
- [ ] optimization_report.md created
- [ ] maintenance_plan.md created
- [ ] All indexes commented and explained

**Testing:**
- [ ] All queries tested with EXPLAIN
- [ ] Performance benchmarks recorded
- [ ] No unused indexes remaining
- [ ] Application works correctly

### Time Tracking

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

## Ready for Week 8?

**Prerequisites for Week 8 (Query Optimization):**
- [ ] All Week 7 checkpoints completed
- [ ] Can read EXPLAIN ANALYZE fluently
- [ ] Understand index types and when to use each
- [ ] Have optimized real queries
- [ ] Confidence rating >= 3/5 for all major topics

**If not ready:**
- Review incomplete checkpoints
- Re-read relevant README.md sections
- Practice more with exercises.md
- Check mistakes_to_expect.md for troubleshooting

**If ready:**
- Commit all Week 7 work
- Document your progress
- Celebrate your achievements! 🎉
- Start Week 8: Query Optimization & Performance Tuning

---

## Quick Troubleshooting

**If stuck on a checkpoint:**
1. Re-read the relevant README.md section
2. Check exercises.md for detailed examples
3. Review mistakes_to_expect.md for your specific issue
4. Use EXPLAIN ANALYZE to investigate
5. Check pg_stat_user_indexes for index usage
6. Ask for help after 1 hour stuck

**Common issues:**
- "Index not used" → Review Mistake 1.1-1.4
- "Can't achieve Index Only Scan" → Review Mistake 5.1
- "Leftmost prefix confusion" → Review Mistake 2.1, 2.3
- "EXPLAIN interpretation" → Review Mistake 3.1-3.3
- "Too many indexes" → Review Mistake 4.1-4.2

---

**Congratulations on completing Week 7! You now have the skills to make any database blazingly fast. These indexing skills will serve you throughout your entire career! 🚀⚡**

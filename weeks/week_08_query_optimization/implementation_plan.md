# Week 8: Query Optimization & Performance Tuning - 7-Day Implementation Plan

**Goal**: Master systematic query optimization through hands-on practice

**Prerequisites**:
- Week 7 completed (Indexing fundamentals)
- Can read EXPLAIN output
- CourseDB-AI database with data
- Understanding of indexes

---

## Day 1: EXPLAIN Mastery (Monday)

### Morning: Understanding EXPLAIN (2-3 hours)

**Learning Objectives**:
- Read EXPLAIN output fluently
- Understand cost estimation
- Identify scan types
- Interpret actual vs estimated metrics

**Tasks**:

1. **Read README.md Sections 1-2** (30 min)
   - Query optimization overview
   - EXPLAIN and EXPLAIN ANALYZE

2. **Complete Exercise 1.1** (45 min):
   ```sql
   -- Practice reading EXPLAIN
   EXPLAIN SELECT * FROM questions WHERE year = 2023;
   EXPLAIN ANALYZE SELECT * FROM questions WHERE year = 2023;
   
   -- Compare estimated vs actual
   ```

3. **Complete Exercise 1.2** (45 min):
   - Test all scan types (Seq, Index, Index Only, Bitmap)
   - Record execution times
   - Understand when each is used

4. **Practice with your own queries** (30 min):
   ```sql
   -- Run EXPLAIN on CourseDB-AI queries
   EXPLAIN ANALYZE [your query];
   
   -- Identify: scan type, cost, rows, time
   ```

**Checkpoint**: Can you read EXPLAIN output and identify bottlenecks? ✅

### Afternoon: Cost Estimation (2-3 hours)

**Tasks**:

1. **Complete Exercise 1.3** (30 min):
   - Compare costs when forcing different plans
   - Understand optimizer decisions

2. **Explore EXPLAIN options** (60 min):
   ```sql
   -- Basic
   EXPLAIN SELECT ...;
   
   -- With execution
   EXPLAIN ANALYZE SELECT ...;
   
   -- With buffers (I/O)
   EXPLAIN (ANALYZE, BUFFERS) SELECT ...;
   
   -- Verbose
   EXPLAIN (ANALYZE, VERBOSE) SELECT ...;
   ```

3. **Document findings** (45 min):
   - Create cheat sheet for EXPLAIN output
   - List common scan types and when used
   - Note cost patterns

**Day 1 Deliverable**:
- [ ] Can read any EXPLAIN output
- [ ] Understand scan types
- [ ] Created EXPLAIN cheat sheet
- [ ] Confidence rating: _____ / 5

**Evening Reflection** (30 min):
- What surprised you about query plans?
- Which scan type is most common?
- Document your EXPLAIN cheat sheet

---

## Day 2: Join Optimization (Tuesday)

### Morning: Join Algorithms (2-3 hours)

**Learning Objectives**:
- Understand Nested Loop, Hash, and Merge joins
- Identify which algorithm is used
- Know when each is optimal

**Tasks**:

1. **Read README.md Section 4** (20 min):
   - Join algorithms

2. **Complete Exercise 2.1** (60 min):
   ```sql
   -- Test Nested Loop Join (small tables)
   -- Test Hash Join (large tables)
   -- Test Merge Join (sorted tables)
   
   -- Record which algorithm is chosen and why
   ```

3. **Analyze CourseDB-AI joins** (60 min):
   ```sql
   -- Find all JOIN queries in your app
   SELECT c.*, COUNT(q.*)
   FROM courses c
   JOIN questions q ON c.course_id = q.course_id
   GROUP BY c.course_id;
   
   -- Run EXPLAIN ANALYZE
   -- Identify join algorithm
   -- Determine if optimal
   ```

4. **Create join optimization guide** (30 min):
   - When to use each algorithm
   - How to optimize each type

**Checkpoint**: Can you identify and optimize join queries? ✅

### Afternoon: Join Order and Indexes (2-3 hours)

**Tasks**:

1. **Complete Exercise 2.2** (45 min):
   - Test join order impact
   - Filter early for better performance

2. **Complete Exercise 2.3** (30 min):
   - Verify indexes on foreign keys
   - Measure join performance with/without indexes

3. **Optimize all CourseDB-AI joins** (90 min):
   ```sql
   -- Audit all joins
   -- Ensure foreign keys are indexed
   -- Verify optimal join order
   
   -- Create missing indexes:
   CREATE INDEX idx_questions_course ON questions(course_id);
   CREATE INDEX idx_questions_topic ON questions(topic_id);
   CREATE INDEX idx_topics_course ON topics(course_id);
   ```

**Day 2 Deliverable**:
- [ ] Understand all join algorithms
- [ ] All foreign keys indexed
- [ ] Join queries optimized
- [ ] Average join speedup: _____x

---

## Day 3: Query Rewriting (Wednesday)

### Morning: Avoiding Anti-Patterns (2-3 hours)

**Learning Objectives**:
- Avoid SELECT *
- Write SARGABLE queries
- Use appropriate operators

**Tasks**:

1. **Read README.md Section 5** (30 min):
   - Query optimization techniques

2. **Complete Exercise 3.1** (20 min):
   ```sql
   -- Compare SELECT * vs specific columns
   -- Measure data reduction
   ```

3. **Complete Exercise 3.2** (30 min):
   ```sql
   -- Avoid functions on indexed columns
   
   -- Bad:
   WHERE YEAR(created_at) = 2023
   
   -- Good:
   WHERE created_at >= '2023-01-01'
     AND created_at < '2024-01-01'
   ```

4. **Audit CourseDB-AI queries** (90 min):
   - Find all SELECT * queries → rewrite
   - Find function calls on indexed columns → fix
   - Document rewrites

**Checkpoint**: Have you eliminated anti-patterns? ✅

### Afternoon: Subquery Optimization (2-3 hours)

**Tasks**:

1. **Complete Exercise 3.3** (45 min):
   ```sql
   -- Compare IN vs EXISTS vs JOIN
   -- Measure performance differences
   ```

2. **Complete Exercise 3.4** (20 min):
   - Add LIMIT for pagination
   - Create indexes for ORDER BY

3. **Optimize subqueries in app** (90 min):
   ```sql
   -- Find all IN subqueries
   -- Convert to EXISTS where beneficial
   -- Add LIMIT to paginated queries
   ```

**Day 3 Deliverable**:
- [ ] No more SELECT *
- [ ] All queries are SARGABLE
- [ ] Subqueries optimized
- [ ] LIMIT added to pagination

---

## Day 4: Real-World Optimization (Thursday)

### Morning: Dashboard Query Optimization (2-3 hours)

**Learning Objectives**:
- Apply systematic optimization process
- Measure before/after improvements
- Document optimizations

**Tasks**:

1. **Read README.md Section 8** (20 min):
   - Practical optimization workflow

2. **Complete Exercise 4.1** (90 min):
   ```sql
   -- Optimize analytics dashboard query
   -- Follow 6-step process:
   -- 1. Identify slow query
   -- 2. Analyze with EXPLAIN ANALYZE
   -- 3. Identify root cause
   -- 4. Apply fix
   -- 5. Verify improvement
   -- 6. Document
   ```

3. **Create optimization template** (30 min):
   ```
   ## Query: [Name]
   
   ### Before:
   - Execution time: _____ ms
   - EXPLAIN output: _____
   - Bottlenecks: _____
   
   ### Optimization:
   - Indexes created: _____
   - Query rewrite: _____
   
   ### After:
   - Execution time: _____ ms
   - Speedup: _____x
   ```

**Checkpoint**: Can you optimize complex queries systematically? ✅

### Afternoon: Search Query Optimization (2-3 hours)

**Tasks**:

1. **Complete Exercise 4.2** (60 min):
   ```sql
   -- Optimize question search with multiple filters
   -- Create composite indexes
   -- Verify optimal index usage
   ```

2. **Optimize all search endpoints** (90 min):
   ```sql
   -- Question search
   -- Course search
   -- Topic search
   
   -- For each:
   -- 1. Profile with EXPLAIN
   -- 2. Create appropriate indexes
   -- 3. Measure improvement
   ```

**Day 4 Deliverable**:
- [ ] Dashboard query optimized (speedup: _____x)
- [ ] Search queries optimized (speedup: _____x)
- [ ] Optimization documentation created
- [ ] All changes tested

---

## Day 5: N+1 Queries and Application-Level Optimization (Friday)

### Morning: Fixing N+1 Queries (2-3 hours)

**Learning Objectives**:
- Identify N+1 query patterns
- Use eager loading (joinedload, selectinload)
- Measure query reduction

**Tasks**:

1. **Read README.md Section 5 (Technique 5)** (15 min):
   - N+1 query problem

2. **Complete Exercise 4.3** (45 min):
   ```python
   # Find N+1 patterns in FastAPI code
   
   # Bad:
   courses = db.query(Course).all()
   for course in courses:
       topics = db.query(Topic).filter(
           Topic.course_id == course.id
       ).all()
   
   # Good:
   courses = db.query(Course).options(
       joinedload(Course.topics)
   ).all()
   ```

3. **Enable SQL logging** (30 min):
   ```python
   # See all queries
   engine = create_engine(DATABASE_URL, echo=True)
   
   # Run endpoints, count queries
   ```

4. **Fix all N+1 patterns** (90 min):
   - Search codebase for loops with queries
   - Convert to eager loading
   - Verify query reduction

**Checkpoint**: Have you eliminated N+1 queries? ✅

### Afternoon: Batch Operations and Caching (2-3 hours)

**Tasks**:

1. **Optimize bulk operations** (60 min):
   ```python
   # Bad: Row-by-row insert
   for question in questions:
       db.add(Question(**question))
       db.commit()  # N commits!
   
   # Good: Batch insert
   db.bulk_insert_mappings(Question, questions)
   db.commit()  # 1 commit
   ```

2. **Consider query caching** (45 min):
   ```python
   # For frequently accessed, rarely changing data
   from functools import lru_cache
   
   @lru_cache(maxsize=100)
   def get_course_list():
       return db.query(Course).all()
   ```

3. **Profile entire application** (45 min):
   - Use SQL logging or profiler
   - Identify remaining bottlenecks
   - Document findings

**Day 5 Deliverable**:
- [ ] No N+1 queries remaining
- [ ] Bulk operations optimized
- [ ] Caching strategy considered
- [ ] Application profile documented

---

## Day 6: Statistics and Maintenance (Saturday)

### Morning: Database Statistics (2-3 hours)

**Learning Objectives**:
- Understand statistics impact
- Use ANALYZE effectively
- Monitor statistics freshness

**Tasks**:

1. **Read README.md Section 6** (20 min):
   - Statistics and VACUUM

2. **Complete Exercise 5.1** (30 min):
   ```sql
   -- Test with outdated statistics
   -- Update with ANALYZE
   -- Compare query plans
   ```

3. **Create maintenance schedule** (60 min):
   ```sql
   -- Check statistics age
   SELECT schemaname, tablename, last_analyze, last_autoanalyze
   FROM pg_stat_user_tables;
   
   -- Update all statistics
   ANALYZE;
   
   -- Schedule:
   -- Daily: Auto-vacuum handles it
   -- After bulk changes: Manual ANALYZE
   ```

4. **Complete Exercise 5.2** (30 min):
   - Check dead tuples
   - Run VACUUM
   - Understand cleanup

**Checkpoint**: Do you maintain database statistics? ✅

### Afternoon: Monitoring and Alerts (2-3 hours)

**Tasks**:

1. **Set up pg_stat_statements** (60 min):
   ```sql
   CREATE EXTENSION pg_stat_statements;
   
   -- Find slow queries
   SELECT calls, mean_exec_time, query
   FROM pg_stat_statements
   ORDER BY mean_exec_time DESC
   LIMIT 10;
   ```

2. **Create monitoring queries** (60 min):
   ```sql
   -- Unused indexes
   SELECT * FROM pg_stat_user_indexes
   WHERE idx_scan = 0;
   
   -- Large tables
   SELECT tablename, pg_size_pretty(pg_total_relation_size(tablename::regclass))
   FROM pg_tables
   WHERE schemaname = 'public'
   ORDER BY pg_total_relation_size(tablename::regclass) DESC;
   
   -- Slow queries (from logs)
   -- Dead tuples (need VACUUM)
   ```

3. **Document monitoring strategy** (30 min):
   - What to monitor
   - Alert thresholds
   - Response procedures

**Day 6 Deliverable**:
- [ ] Statistics up-to-date
- [ ] VACUUM schedule created
- [ ] Monitoring queries documented
- [ ] pg_stat_statements enabled

---

## Day 7: Final Optimization and Review (Sunday)

### Morning: Complete Optimization (2-3 hours)

**Tasks**:

1. **Challenge 1: Complete CourseDB-AI Optimization** (120 min):
   - Profile all endpoints
   - Optimize remaining slow queries
   - Document all optimizations
   - Create optimization_report.md

**Optimization report template:**
```markdown
# CourseDB-AI Query Optimization Report

## Summary
- Total queries optimized: _____
- Average speedup: _____x
- Total indexes created: _____

## Optimized Queries

### Query 1: Analytics Dashboard
- Before: _____ ms
- After: _____ ms
- Speedup: _____x
- Changes: _____

### Query 2: Question Search
...

## Indexes Created
1. CREATE INDEX _____ ON _____(_____);
   - Purpose: _____
   - Impact: _____

## N+1 Queries Fixed
1. Endpoint: _____
   - Before: _____ queries
   - After: _____ queries

## Recommendations
- _____
```

**Checkpoint**: Is entire application optimized? ✅

### Afternoon: Learning Review (2-3 hours)

**Tasks**:

1. **Complete reflection.md** (60 min):
   - Answer reflection prompts
   - Document key learnings
   - Identify areas for more practice

2. **Create optimization playbook** (45 min):
   ```markdown
   # Query Optimization Playbook
   
   ## Step 1: Identify
   - Use pg_stat_statements
   - Check application logs
   - User complaints
   
   ## Step 2: Analyze
   - Run EXPLAIN ANALYZE
   - Identify scan types
   - Check for missing indexes
   
   ## Step 3: Optimize
   - Create indexes
   - Rewrite query
   - Fix N+1 patterns
   
   ## Step 4: Verify
   - Measure improvement
   - Check for regressions
   - Document changes
   ```

3. **Final testing** (45 min):
   - Run full test suite
   - Benchmark all endpoints
   - Verify no regressions
   - Celebrate improvements! 🎉

**Day 7 Deliverable**:
- [ ] optimization_report.md created
- [ ] Optimization playbook documented
- [ ] Reflection completed
- [ ] Week 8 complete! 🎉

---

## Week 8 Final Deliverables Checklist

### Query Optimizations:
- [ ] **All slow queries identified and optimized**
- [ ] **Average speedup: _____x**
- [ ] **Before/after metrics documented**

### Indexes:
- [ ] **All appropriate indexes created**
- [ ] **Foreign keys indexed**
- [ ] **Covering indexes for hot queries**
- [ ] **No unused indexes**

### Code Quality:
- [ ] **No N+1 queries**
- [ ] **No SELECT ***
- [ ] **All queries SARGABLE**
- [ ] **LIMIT added to pagination**

### Maintenance:
- [ ] **ANALYZE run on all tables**
- [ ] **VACUUM schedule created**
- [ ] **pg_stat_statements enabled**
- [ ] **Monitoring queries documented**

### Documentation:
- [ ] **optimization_report.md**
- [ ] **Optimization playbook**
- [ ] **EXPLAIN cheat sheet**
- [ ] **Monitoring strategy**

### Knowledge Mastery:
- [ ] Can read EXPLAIN output fluently
- [ ] Can identify all join algorithms
- [ ] Can optimize any slow query
- [ ] Can prevent N+1 queries
- [ ] Can maintain database statistics

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

1. **Always measure before optimizing** - No guessing!
2. **Use EXPLAIN ANALYZE religiously** - It's your best tool
3. **Document everything** - Future you will thank you
4. **Test after each change** - Verify no regressions
5. **Start with biggest wins** - 80/20 rule applies
6. **Keep queries readable** - Sometimes slower is clearer
7. **Monitor in production** - Optimization is ongoing

---

## Resources

- PostgreSQL EXPLAIN: https://www.postgresql.org/docs/current/using-explain.html
- Query Performance Tips: https://wiki.postgresql.org/wiki/Performance_Optimization
- pg_stat_statements: https://www.postgresql.org/docs/current/pgstatstatements.html
- SQLAlchemy eager loading: https://docs.sqlalchemy.org/en/14/orm/loading_relationships.html

---

**Ready to make every query blazingly fast? Let's optimize! ⚡🚀**

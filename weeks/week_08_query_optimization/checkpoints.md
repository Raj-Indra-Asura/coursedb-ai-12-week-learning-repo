# Week 8: Query Optimization & Performance Tuning - Daily Checkpoints

## 🎯 Purpose

Track your daily progress through Week 8 with concrete, measurable checkpoints. Each day has specific deliverables you can verify.

**How to use this document:**
- [ ] Check off items as you complete them
- [ ] Verify each checkpoint before moving to next day
- [ ] Record your measurements and speedups
- [ ] Don't skip checkpoints—they build systematically

---

## Day 1: EXPLAIN Mastery ✅

### Morning Checkpoint (Understanding EXPLAIN)

**Time estimate:** 2-3 hours

**Deliverables:**

- [ ] **PostgreSQL connection verified**
  ```bash
  psql -U coursedb_user -d coursedb_dev -c "SELECT version();"
  ```

- [ ] **Exercise 1.1 completed**: EXPLAIN vs EXPLAIN ANALYZE
  - [ ] Ran EXPLAIN (without execution)
  - [ ] Ran EXPLAIN ANALYZE (with execution)
  - [ ] Compared estimated vs actual metrics

- [ ] **Metrics recorded:**
  ```
  Query: SELECT * FROM questions WHERE year = 2023;
  
  EXPLAIN (estimated):
  - Scan type: _____
  - Cost: _____
  - Estimated rows: _____
  
  EXPLAIN ANALYZE (actual):
  - Scan type: _____
  - Actual rows: _____
  - Execution time: _____ ms
  ```

- [ ] **Exercise 1.2 completed**: Scan type recognition
  - [ ] Observed Seq Scan
  - [ ] Observed Index Scan
  - [ ] Observed Index Only Scan
  - [ ] Observed Bitmap Scan

**Self-check questions:**
1. What's the difference between "cost" and "execution time"? _____
2. Why might estimated rows differ from actual rows? _____
3. Which scan type is fastest? _____

### Afternoon Checkpoint (EXPLAIN Options)

**Time estimate:** 2-3 hours

**Deliverables:**

- [ ] **Exercise 1.3 completed**: Cost estimation
  - [ ] Tested with enable_seqscan OFF
  - [ ] Compared optimizer choices
  - [ ] Understood when Seq Scan is optimal

- [ ] **EXPLAIN options tested:**
  ```sql
  -- Tested these variations:
  EXPLAIN SELECT ...;
  EXPLAIN ANALYZE SELECT ...;
  EXPLAIN (ANALYZE, BUFFERS) SELECT ...;
  EXPLAIN (ANALYZE, VERBOSE) SELECT ...;
  ```

- [ ] **Created EXPLAIN cheat sheet:**
  | Metric | Meaning |
  |--------|---------|
  | cost | _____ |
  | rows | _____ |
  | width | _____ |
  | actual time | _____ |
  | loops | _____ |
  | Execution Time | _____ |

**Day 1 Complete:** You can read and interpret EXPLAIN output! ✅

---

## Day 2: Join Optimization ✅

### Morning Checkpoint (Join Algorithms)

**Time estimate:** 2-3 hours

**Deliverables:**

- [ ] **Exercise 2.1 completed**: Join algorithm comparison
  - [ ] Created test tables (small, medium, large)
  - [ ] Observed Nested Loop Join
  - [ ] Observed Hash Join
  - [ ] Observed Merge Join

- [ ] **Join algorithm summary:**
  | Algorithm | When Used | Example Time |
  |-----------|-----------|--------------|
  | Nested Loop | _____ | _____ ms |
  | Hash Join | _____ | _____ ms |
  | Merge Join | _____ | _____ ms |

- [ ] **Analyzed CourseDB-AI joins:**
  ```sql
  -- Identified join queries in app:
  1. Query: _____
     Join algorithm: _____
     Optimal: Yes / No
  
  2. Query: _____
     Join algorithm: _____
     Optimal: Yes / No
  ```

**Self-check questions:**
1. Which join is best for small × large with index? _____
2. Which join requires equality condition? _____
3. When would optimizer choose Merge Join? _____

### Afternoon Checkpoint (Join Optimization)

**Time estimate:** 2-3 hours

**Deliverables:**

- [ ] **Exercise 2.2 completed**: Join order
  - [ ] Tested join with late filtering
  - [ ] Tested join with early filtering
  - [ ] Measured speedup: _____x

- [ ] **Exercise 2.3 completed**: Foreign key indexes
  - [ ] Measured join WITHOUT index
  - [ ] Created index on foreign key
  - [ ] Measured join WITH index
  - [ ] Speedup: _____x

- [ ] **All foreign keys indexed:**
  ```sql
  CREATE INDEX idx_questions_course ON questions(course_id);
  CREATE INDEX idx_questions_topic ON questions(topic_id);
  CREATE INDEX idx_topics_course ON topics(course_id);
  
  -- Verified with:
  \d questions
  \d topics
  ```

**Day 2 Complete:** All joins are optimized! ✅

---

## Day 3: Query Rewriting ✅

### Morning Checkpoint (Avoiding Anti-Patterns)

**Time estimate:** 2-3 hours

**Deliverables:**

- [ ] **Exercise 3.1 completed**: SELECT * vs specific columns
  - [ ] Measured SELECT * data transfer: _____ bytes
  - [ ] Measured specific columns: _____ bytes
  - [ ] Data reduction: _____x

- [ ] **Exercise 3.2 completed**: SARGABLE queries
  - [ ] Tested function on indexed column (bad)
  - [ ] Rewrote to be SARGABLE (good)
  - [ ] Speedup: _____x

- [ ] **Audited CourseDB-AI queries:**
  - [ ] Found _____ queries with SELECT *
  - [ ] Rewrote to specific columns
  - [ ] Found _____ queries with functions on indexes
  - [ ] Rewrote to be SARGABLE

**Self-check questions:**
1. Why is SELECT * bad? _____
2. What does SARGABLE mean? _____
3. Give example of non-SARGABLE query: _____

### Afternoon Checkpoint (Subquery Optimization)

**Time estimate:** 2-3 hours

**Deliverables:**

- [ ] **Exercise 3.3 completed**: IN vs EXISTS vs JOIN
  - [ ] Tested IN with subquery: _____ ms
  - [ ] Tested EXISTS: _____ ms
  - [ ] Tested JOIN: _____ ms
  - [ ] Fastest method: _____

- [ ] **Exercise 3.4 completed**: LIMIT for pagination
  - [ ] Query without LIMIT: _____ ms
  - [ ] Query with LIMIT: _____ ms
  - [ ] Speedup: _____x

- [ ] **Optimized subqueries in app:**
  - [ ] Converted _____ IN to EXISTS
  - [ ] Added LIMIT to _____ pagination queries
  - [ ] Created indexes for ORDER BY

**Day 3 Complete:** Queries follow best practices! ✅

---

## Day 4: Real-World Optimization ✅

### Morning Checkpoint (Dashboard Optimization)

**Time estimate:** 2-3 hours

**Deliverables:**

- [ ] **Exercise 4.1 completed**: Analytics query
  ```
  Query: Dashboard analytics
  
  Before:
  - Execution time: _____ ms
  - Bottlenecks: _____
  
  Optimizations applied:
  - Index 1: _____
  - Index 2: _____
  - Query rewrite: _____
  
  After:
  - Execution time: _____ ms
  - Speedup: _____x
  ```

- [ ] **Created optimization template:**
  - [ ] Documented before/after metrics
  - [ ] Listed indexes created
  - [ ] Explained rationale
  - [ ] Verified improvement

**Self-check questions:**
1. What was the main bottleneck? _____
2. Which optimization had biggest impact? _____
3. How did you verify correctness? _____

### Afternoon Checkpoint (Search Optimization)

**Time estimate:** 2-3 hours

**Deliverables:**

- [ ] **Exercise 4.2 completed**: Question search
  ```
  Before: _____ ms
  Indexes created: _____
  After: _____ ms
  Speedup: _____x
  ```

- [ ] **Optimized all search endpoints:**
  | Endpoint | Before | After | Speedup |
  |----------|--------|-------|---------|
  | GET /questions | _____ ms | _____ ms | _____x |
  | GET /courses | _____ ms | _____ ms | _____x |
  | GET /topics | _____ ms | _____ ms | _____x |

**Day 4 Complete:** Key queries are fast! ✅

---

## Day 5: N+1 Queries and Application-Level Optimization ✅

### Morning Checkpoint (Fixing N+1)

**Time estimate:** 2-3 hours

**Deliverables:**

- [ ] **Exercise 4.3 completed**: N+1 elimination
  ```python
  # Before:
  # Queries: 1 + N
  # Time: _____ ms
  
  # After (with eager loading):
  # Queries: 1
  # Time: _____ ms
  # Speedup: _____x
  ```

- [ ] **SQL logging enabled:**
  ```python
  engine = create_engine(DATABASE_URL, echo=True)
  # Ran endpoints and counted queries
  ```

- [ ] **All N+1 patterns fixed:**
  - [ ] Endpoint 1: _____ queries → 1 query
  - [ ] Endpoint 2: _____ queries → 1 query
  - [ ] Endpoint 3: _____ queries → 1 query

**Self-check questions:**
1. How many N+1 patterns did you find? _____
2. What eager loading strategy did you use? _____
3. What's the difference between joinedload and selectinload? _____

### Afternoon Checkpoint (Batch Operations)

**Time estimate:** 2-3 hours

**Deliverables:**

- [ ] **Optimized bulk operations:**
  ```python
  # Before (row-by-row):
  # Time: _____ ms for 1000 inserts
  
  # After (batch):
  # Time: _____ ms for 1000 inserts
  # Speedup: _____x
  ```

- [ ] **Profiled entire application:**
  - [ ] Identified top 10 slowest queries
  - [ ] Optimized top 5
  - [ ] Average speedup: _____x

**Day 5 Complete:** Application code is optimized! ✅

---

## Day 6: Statistics and Maintenance ✅

### Morning Checkpoint (Database Statistics)

**Time estimate:** 2-3 hours

**Deliverables:**

- [ ] **Exercise 5.1 completed**: Statistics impact
  ```sql
  -- Before ANALYZE:
  Estimated rows: _____
  Actual rows: _____
  Accuracy: _____x off
  
  -- After ANALYZE:
  Estimated rows: _____
  Actual rows: _____
  Accuracy: Accurate ✅
  ```

- [ ] **Exercise 5.2 completed**: VACUUM
  ```sql
  -- Dead tuples before: _____
  -- Dead tuples after: _____
  -- Space reclaimed: _____ KB
  ```

- [ ] **Created maintenance schedule:**
  ```
  Daily: Check autovacuum status
  Weekly: Review slow queries
  Monthly: Manual ANALYZE
  Quarterly: VACUUM FULL (during maintenance window)
  ```

**Self-check questions:**
1. When should you run ANALYZE? _____
2. What's the difference between VACUUM and VACUUM FULL? _____
3. How do you check if statistics are stale? _____

### Afternoon Checkpoint (Monitoring Setup)

**Time estimate:** 2-3 hours

**Deliverables:**

- [ ] **pg_stat_statements enabled:**
  ```sql
  CREATE EXTENSION pg_stat_statements;
  
  -- Verified with:
  SELECT * FROM pg_stat_statements LIMIT 1;
  ```

- [ ] **Monitoring queries documented:**
  ```sql
  -- Slow queries
  SELECT calls, mean_exec_time, query
  FROM pg_stat_statements
  WHERE mean_exec_time > 100
  ORDER BY mean_exec_time DESC;
  
  -- Unused indexes
  SELECT indexname, idx_scan
  FROM pg_stat_user_indexes
  WHERE idx_scan = 0;
  
  -- Dead tuples
  SELECT tablename, n_dead_tup, n_live_tup
  FROM pg_stat_user_tables;
  ```

- [ ] **Alert thresholds defined:**
  - [ ] Query > 1000ms: Alert
  - [ ] Dead tuples > 10%: Review
  - [ ] Unused index: Consider dropping

**Day 6 Complete:** Monitoring is in place! ✅

---

## Day 7: Final Optimization and Review ✅

### Morning Checkpoint (Complete Optimization)

**Time estimate:** 2-3 hours

**Deliverables:**

- [ ] **Challenge 1 completed**: Full optimization
  ```markdown
  # Optimization Report
  
  ## Summary
  - Total queries optimized: _____
  - Average speedup: _____x
  - Total indexes created: _____
  - N+1 queries eliminated: _____
  
  ## Top 5 Optimizations
  1. Query: _____
     Speedup: _____x
  
  2. Query: _____
     Speedup: _____x
  
  ... (full report)
  ```

- [ ] **All endpoints benchmarked:**
  | Endpoint | Before | After | Speedup |
  |----------|--------|-------|---------|
  | Dashboard | _____ | _____ | _____x |
  | Search | _____ | _____ | _____x |
  | Analytics | _____ | _____ | _____x |
  
  **Overall improvement**: _____x

**Self-check questions:**
1. What was your biggest win? _____
2. Are there any queries still > 100ms? _____
3. Have you documented all changes? _____

### Afternoon Checkpoint (Review and Documentation)

**Time estimate:** 2-3 hours

**Deliverables:**

- [ ] **Reflection completed:**
  - [ ] Answered 5+ reflection prompts
  - [ ] Documented key learnings
  - [ ] Created action items

- [ ] **Optimization playbook created:**
  ```markdown
  # Query Optimization Playbook
  
  ## When to Optimize
  - Query > _____ms
  - Called > _____ times/sec
  - User-facing: Yes
  
  ## How to Optimize
  1. Measure with EXPLAIN ANALYZE
  2. Identify bottleneck
  3. Apply appropriate fix
  4. Verify improvement
  5. Monitor in production
  
  ## Common Fixes
  - Missing index → CREATE INDEX
  - N+1 queries → Eager loading
  - SELECT * → Specific columns
  - Stale stats → ANALYZE
  ```

- [ ] **Final testing completed:**
  - [ ] All queries work correctly
  - [ ] No regressions introduced
  - [ ] Performance targets met
  - [ ] Documentation complete

**Day 7 Complete:** Week 8 is done! 🎉

---

## Week 8 Final Self-Assessment

### Knowledge Check

**Concepts mastered:**
- [ ] Can read EXPLAIN output fluently
- [ ] Understand all join algorithms
- [ ] Know when each scan type is used
- [ ] Can identify N+1 query patterns
- [ ] Understand statistics and their impact
- [ ] Can optimize queries systematically
- [ ] Know when to optimize and when not to

**Skills acquired:**
- [ ] Can profile any slow query
- [ ] Can create appropriate indexes
- [ ] Can rewrite queries for performance
- [ ] Can eliminate N+1 queries
- [ ] Can maintain database statistics
- [ ] Can monitor query performance
- [ ] Can document optimizations

**Confidence rating (1-5):**
- [ ] Reading EXPLAIN: _____ / 5
- [ ] Join optimization: _____ / 5
- [ ] Query rewriting: _____ / 5
- [ ] N+1 prevention: _____ / 5
- [ ] Statistics maintenance: _____ / 5
- [ ] Overall optimization: _____ / 5

### Deliverables Checklist

**Optimizations:**
- [ ] _____ queries optimized
- [ ] Average speedup: _____x
- [ ] _____ indexes created
- [ ] _____ N+1 queries fixed
- [ ] All changes documented

**Maintenance:**
- [ ] Statistics up-to-date (ANALYZE run)
- [ ] VACUUM schedule created
- [ ] pg_stat_statements enabled
- [ ] Monitoring queries documented

**Documentation:**
- [ ] optimization_report.md created
- [ ] Optimization playbook created
- [ ] EXPLAIN cheat sheet created
- [ ] Monitoring strategy documented

**Code Quality:**
- [ ] No SELECT *
- [ ] No N+1 queries
- [ ] All queries SARGABLE
- [ ] Foreign keys indexed
- [ ] Pagination uses LIMIT

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

## Ready for Week 9?

**Prerequisites for Week 9 (Transactions & ACID):**
- [ ] All Week 8 checkpoints completed
- [ ] Can read EXPLAIN fluently
- [ ] Have optimized real queries
- [ ] Understand join algorithms
- [ ] Confidence rating >= 3/5 for all topics

**If not ready:**
- Review incomplete checkpoints
- Re-read relevant README.md sections
- Practice more with exercises.md
- Check mistakes_to_expect.md

**If ready:**
- Commit all Week 8 work
- Document your achievements
- Celebrate your optimization wins! 🎉
- Start Week 9: Transactions, ACID, Concurrency

---

## Quick Troubleshooting

**If stuck on a checkpoint:**
1. Re-read relevant README.md section
2. Check exercises.md for examples
3. Review mistakes_to_expect.md
4. Use EXPLAIN ANALYZE to investigate
5. Check pg_stat_user_indexes for index usage
6. Ask for help after 1 hour stuck

**Common issues:**
- "Query still slow after index" → Check EXPLAIN, verify index is used
- "Estimates way off" → Run ANALYZE
- "N+1 not fixed" → Enable SQL logging, verify eager loading
- "Can't read EXPLAIN" → Review Day 1 materials

---

**Congratulations on completing Week 8! You now have professional-level query optimization skills. You can make any database application blazingly fast! ⚡🚀**

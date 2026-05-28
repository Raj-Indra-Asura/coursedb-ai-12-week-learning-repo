# Query Plan Analysis

**Week 8: Query Optimization + EXPLAIN**

Learn to read and optimize PostgreSQL query plans.

---

## 🎯 Learning Objectives

- Read EXPLAIN ANALYZE output
- Understand Sequential Scan vs Index Scan
- Measure query performance
- Optimize slow queries

---

## 📊 EXPLAIN Output

```
Seq Scan on questions  (cost=0.00..18.50 rows=5 width=100) (actual time=0.015..0.234 rows=342 loops=1)
  Filter: (difficulty = 'medium'::text)
  Rows Removed by Filter: 658
Planning Time: 0.089 ms
Execution Time: 0.267 ms
```

### Key Metrics:
- **cost**: Estimated cost (0.00 startup, 18.50 total)
- **rows**: Estimated rows returned
- **width**: Average row size in bytes
- **actual time**: Real time (ms)
- **loops**: Times node was executed

---

## 🔄 Sequential Scan vs Index Scan

| Scan Type | When Used | Performance |
|-----------|-----------|-------------|
| **Sequential Scan** | Read all rows | O(n) |
| **Index Scan** | Use index to find rows | O(log n) |

---

## 🧪 Running Analysis

```bash
# Connect to PostgreSQL
psql -U postgres -d coursedb

# Run demo queries
\i dbms_internals/query_plan/query_plan_demo.sql

# Save output
\o outputs/analysis.txt
```

---

## 📝 Exercise

1. Run Query 1 before index. Record execution time.
2. Create index on `difficulty`.
3. Run Query 1 again. Compare.
4. Calculate performance improvement.

**Document findings in Week 8 reflection.md**

---

## 🔍 Self-Check

1. What does EXPLAIN ANALYZE show?
2. When does PostgreSQL use indexes?
3. Why might an index NOT be used?
4. What is the cost estimate?

---

**Next**: Apply to CourseDB-AI semantic search queries!

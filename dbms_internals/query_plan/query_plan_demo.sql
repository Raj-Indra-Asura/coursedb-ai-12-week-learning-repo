-- Query Plan Demo SQL
-- Week 8: Query Optimization + EXPLAIN

-- This file contains queries to analyze with EXPLAIN ANALYZE
-- Run these queries before and after creating indexes to see the difference

-- TODO (Week 8): Connect to PostgreSQL and run these queries

-- ============================================================================
-- SETUP: Create sample data
-- ============================================================================

-- Create larger dataset for meaningful query plans
INSERT INTO questions (resource_id, question_text, marks, difficulty, question_type)
SELECT
    (random() * 10)::int + 1,
    'Sample question ' || generate_series,
    (random() * 20)::int + 1,
    CASE (random() * 3)::int
        WHEN 0 THEN 'easy'
        WHEN 1 THEN 'medium'
        ELSE 'hard'
    END,
    CASE (random() * 4)::int
        WHEN 0 THEN 'mcq'
        WHEN 1 THEN 'short'
        WHEN 2 THEN 'long'
        ELSE 'problem'
    END
FROM generate_series(1, 1000);

-- ============================================================================
-- QUERY 1: Filter by difficulty (before index)
-- ============================================================================

-- Expected: Sequential Scan
EXPLAIN ANALYZE
SELECT * FROM questions
WHERE difficulty = 'medium';

-- ============================================================================
-- QUERY 2: Filter by academic year (before index)
-- ============================================================================

-- Expected: Sequential Scan
EXPLAIN ANALYZE
SELECT r.* FROM resources r
WHERE r.academic_year = '2023';

-- ============================================================================
-- QUERY 3: Join with topic filter (before index)
-- ============================================================================

-- Expected: Sequential Scan + Hash Join
EXPLAIN ANALYZE
SELECT q.question_text, t.topic_name
FROM questions q
JOIN question_topics qt ON q.question_id = qt.question_id
JOIN topics t ON qt.topic_id = t.topic_id
WHERE t.topic_name ILIKE '%normalization%';

-- ============================================================================
-- QUERY 4: Aggregate by difficulty
-- ============================================================================

-- Expected: Sequential Scan + HashAggregate
EXPLAIN ANALYZE
SELECT difficulty, COUNT(*) as count
FROM questions
GROUP BY difficulty;

-- ============================================================================
-- CREATE INDEXES
-- ============================================================================

-- TODO (Week 8): After running queries above, create indexes

CREATE INDEX idx_questions_difficulty ON questions(difficulty);
CREATE INDEX idx_resources_year ON resources(academic_year);
CREATE INDEX idx_topics_name ON topics(topic_name);

-- ============================================================================
-- RE-RUN QUERIES (after indexes)
-- ============================================================================

-- TODO (Week 8): Run queries again and compare plans

-- Query 1 again (should use Index Scan)
EXPLAIN ANALYZE
SELECT * FROM questions
WHERE difficulty = 'medium';

-- Query 2 again (should use Index Scan)
EXPLAIN ANALYZE
SELECT r.* FROM resources r
WHERE r.academic_year = '2023';

-- Query 3 again (should use Index Scan on topics)
EXPLAIN ANALYZE
SELECT q.question_text, t.topic_name
FROM questions q
JOIN question_topics qt ON q.question_id = qt.question_id
JOIN topics t ON qt.topic_id = t.topic_id
WHERE t.topic_name ILIKE '%normalization%';

-- ============================================================================
-- ANALYSIS CHECKLIST
-- ============================================================================

-- For each query, document:
-- [ ] Execution time before index
-- [ ] Execution time after index
-- [ ] Scan type (Sequential Scan vs Index Scan)
-- [ ] Cost estimate
-- [ ] Actual rows returned
-- [ ] Performance improvement percentage

-- Save output to: dbms_internals/query_plan/outputs/analysis.txt

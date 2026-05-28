-- Transaction Demo SQL
-- Week 9: Transactions, ACID, Concurrency

-- This file demonstrates transaction behavior in PostgreSQL

-- ============================================================================
-- DEMO 1: COMMIT - Successful Transaction
-- ============================================================================

-- TODO (Week 9): Run in psql

BEGIN;

-- Insert a new question
INSERT INTO questions (resource_id, question_text, marks, difficulty, question_type)
VALUES (1, 'What is ACID?', 5, 'easy', 'short');

-- Update difficulty
UPDATE questions
SET difficulty = 'medium'
WHERE question_text = 'What is ACID?';

-- Check audit log (should show both INSERT and UPDATE)
SELECT * FROM audit_logs ORDER BY created_at DESC LIMIT 5;

COMMIT;

-- Verify changes persisted
SELECT * FROM questions WHERE question_text = 'What is ACID?';

-- ============================================================================
-- DEMO 2: ROLLBACK - Failed Transaction
-- ============================================================================

BEGIN;

-- Delete a question
DELETE FROM questions WHERE question_id = 1;

-- Oops, made a mistake!
ROLLBACK;

-- Verify question still exists
SELECT * FROM questions WHERE question_id = 1;

-- ============================================================================
-- DEMO 3: Multi-step Safe Update with Savepoint
-- ============================================================================

BEGIN;

-- Create savepoint before risky operation
SAVEPOINT before_update;

UPDATE questions
SET marks = marks * 2
WHERE difficulty = 'hard';

-- Check if update looks correct
SELECT difficulty, AVG(marks) FROM questions GROUP BY difficulty;

-- If something wrong, rollback to savepoint
-- ROLLBACK TO SAVEPOINT before_update;

-- If correct, commit
COMMIT;

-- ============================================================================
-- DEMO 4: Concurrent Updates (Run in TWO sessions)
-- ============================================================================

-- Session 1:
BEGIN;
UPDATE questions SET marks = 10 WHERE question_id = 1;
-- Don't commit yet...

-- Session 2 (in another terminal):
BEGIN;
UPDATE questions SET marks = 15 WHERE question_id = 1;
-- This will WAIT for Session 1 to complete

-- Back to Session 1:
COMMIT;
-- Now Session 2 proceeds

-- ============================================================================
-- DEMO 5: Deadlock Simulation
-- ============================================================================

-- Session 1:
BEGIN;
UPDATE questions SET marks = 10 WHERE question_id = 1;
-- Now update question_id = 2
UPDATE questions SET marks = 20 WHERE question_id = 2;

-- Session 2 (simultaneously):
BEGIN;
UPDATE questions SET marks = 15 WHERE question_id = 2;
-- Now try to update question_id = 1
UPDATE questions SET marks = 25 WHERE question_id = 1;
-- DEADLOCK! PostgreSQL will detect and abort one transaction

-- ============================================================================
-- ANALYSIS TASKS (Week 9)
-- ============================================================================

-- TODO: Document in weeks/week_09.../reflection.md
-- 1. How long did concurrent update wait?
-- 2. Which transaction was aborted in deadlock?
-- 3. What isolation level is being used?
-- 4. How does audit trigger behave with ROLLBACK?

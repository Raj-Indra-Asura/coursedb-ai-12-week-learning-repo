-- Week 2: SQL Basics - Schema Definition
-- This is an INTENTIONALLY IMPERFECT schema for learning purposes
-- Issues: redundancy, update anomalies (to be fixed in Week 4: Normalization)

-- Drop tables if they exist (for re-running)
DROP TABLE IF EXISTS questions CASCADE;
DROP TABLE IF EXISTS topics CASCADE;
DROP TABLE IF EXISTS courses CASCADE;

-- Table 1: Courses
CREATE TABLE courses (
    course_id SERIAL PRIMARY KEY,
    course_code VARCHAR(20) UNIQUE NOT NULL,
    course_title VARCHAR(200) NOT NULL,
    semester VARCHAR(20),
    credit INTEGER CHECK (credit > 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table 2: Topics (intentionally simple for Week 2)
CREATE TABLE topics (
    topic_id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES courses(course_id) ON DELETE CASCADE,
    topic_name VARCHAR(100) NOT NULL,
    description TEXT,
    week_number INTEGER CHECK (week_number > 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table 3: Questions (with intentional redundancy for Week 4 lesson)
CREATE TABLE questions (
    question_id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES courses(course_id) ON DELETE CASCADE,
    topic_id INTEGER REFERENCES topics(topic_id) ON DELETE SET NULL,
    question_text TEXT NOT NULL,

    -- Intentional redundancy: storing course_code and topic_name again
    -- (will be normalized in Week 4)
    course_code VARCHAR(20),  -- REDUNDANT!
    topic_name VARCHAR(100),  -- REDUNDANT!

    year INTEGER CHECK (year >= 2010 AND year <= 2030),
    exam_type VARCHAR(50) CHECK (exam_type IN ('midterm', 'final', 'quiz', 'assignment')),
    difficulty VARCHAR(20) CHECK (difficulty IN ('easy', 'medium', 'hard')),
    marks INTEGER CHECK (marks > 0),

    -- Answer (optional)
    answer_text TEXT,
    answer_reference VARCHAR(200),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for common queries (Week 7 will cover indexing in detail)
CREATE INDEX idx_questions_year ON questions(year);
CREATE INDEX idx_questions_difficulty ON questions(difficulty);
CREATE INDEX idx_questions_topic_id ON questions(topic_id);

-- Comments for learning
COMMENT ON TABLE courses IS 'Stores academic course information';
COMMENT ON TABLE topics IS 'Stores course topics/chapters';
COMMENT ON TABLE questions IS 'Stores previous-year exam questions (intentionally denormalized for Week 2-3)';
COMMENT ON COLUMN questions.course_code IS 'REDUNDANT - violates 3NF (will fix in Week 4)';
COMMENT ON COLUMN questions.topic_name IS 'REDUNDANT - violates 3NF (will fix in Week 4)';

-- Week 2 Learning Note:
-- This schema works but has issues:
-- 1. course_code and topic_name are stored redundantly in questions table
-- 2. Update anomalies: if course_code changes, must update questions table too
-- 3. Deletion anomalies: if last question for a topic is deleted, topic info is lost
-- We'll fix these in Week 4 with normalization!

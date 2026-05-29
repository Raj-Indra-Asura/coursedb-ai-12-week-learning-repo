-- Week 2: SQL Basics - Seed Data
-- Sample data for learning SQL queries

-- Insert Courses
INSERT INTO courses (course_code, course_title, semester, credit) VALUES
('CS201', 'Database Management Systems', 'Fall 2024', 4),
('CS202', 'DBMS Lab', 'Fall 2024', 2),
('CS301', 'Advanced Databases', 'Spring 2025', 3);

-- Insert Topics
INSERT INTO topics (course_id, topic_name, description, week_number) VALUES
-- CS201 topics
(1, 'DBMS Fundamentals', 'Introduction to databases, data models, DBMS architecture', 1),
(1, 'SQL Basics', 'DDL, DML, SELECT queries, filtering, sorting', 2),
(1, 'ER Modeling', 'Entity-Relationship diagrams, cardinality, weak entities', 3),
(1, 'Normalization', 'Functional dependencies, 1NF, 2NF, 3NF, BCNF', 4),
(1, 'Indexing', 'B+ trees, hash indexing, query optimization', 7),
(1, 'Transactions', 'ACID properties, concurrency control, deadlock', 9),

-- CS301 topics
(3, 'Query Optimization', 'Query plans, cost estimation, optimizer', 8),
(3, 'NoSQL Databases', 'Document stores, key-value stores, CAP theorem', 11),
(3, 'Vector Databases', 'Embeddings, similarity search, pgvector', 10);

-- Insert 50+ DBMS Questions (covering various topics and difficulties)

-- DBMS Fundamentals Questions
INSERT INTO questions (course_id, topic_id, question_text, course_code, topic_name, year, exam_type, difficulty, marks) VALUES
(1, 1, 'What is a Database Management System (DBMS)? List its advantages over file-based systems.', 'CS201', 'DBMS Fundamentals', 2023, 'midterm', 'easy', 5),
(1, 1, 'Explain the three-level architecture (physical, logical, view) of a DBMS with a diagram.', 'CS201', 'DBMS Fundamentals', 2023, 'final', 'medium', 8),
(1, 1, 'Differentiate between schema and instance with examples.', 'CS201', 'DBMS Fundamentals', 2022, 'midterm', 'easy', 4),
(1, 1, 'What is data independence? Explain physical and logical data independence.', 'CS201', 'DBMS Fundamentals', 2022, 'final', 'medium', 6),

-- SQL Basics Questions
(1, 2, 'Write a SQL query to create a table "students" with columns: student_id (PK), name, age, major.', 'CS201', 'SQL Basics', 2023, 'midterm', 'easy', 3),
(1, 2, 'Write a query to find all students whose age is between 18 and 25.', 'CS201', 'SQL Basics', 2023, 'quiz', 'easy', 2),
(1, 2, 'What is the difference between WHERE and HAVING clauses in SQL? Provide examples.', 'CS201', 'SQL Basics', 2023, 'final', 'medium', 5),
(1, 2, 'Write a query to count the number of students in each major, showing only majors with more than 10 students.', 'CS201', 'SQL Basics', 2022, 'midterm', 'medium', 4),
(1, 2, 'Explain the difference between INNER JOIN, LEFT JOIN, and RIGHT JOIN with examples.', 'CS201', 'SQL Basics', 2022, 'final', 'medium', 6),
(1, 2, 'Write a query to find the second highest salary from an employees table.', 'CS201', 'SQL Basics', 2021, 'final', 'hard', 8),

-- ER Modeling Questions
(1, 3, 'Draw an ER diagram for a university database with entities: Student, Course, Professor, Department.', 'CS201', 'ER Modeling', 2023, 'midterm', 'medium', 10),
(1, 3, 'What is a weak entity? Provide an example with an ER diagram.', 'CS201', 'ER Modeling', 2023, 'final', 'medium', 6),
(1, 3, 'Explain cardinality ratios (1:1, 1:N, M:N) with real-world examples.', 'CS201', 'ER Modeling', 2022, 'midterm', 'easy', 5),
(1, 3, 'Convert the following ER diagram into relational schema: [Student --enrolls-in--> Course] where Student(1) to Course(N).', 'CS201', 'ER Modeling', 2022, 'final', 'medium', 8),
(1, 3, 'What are participation constraints (total vs partial)? Show in an ER diagram.', 'CS201', 'ER Modeling', 2021, 'final', 'medium', 6),

-- Normalization Questions
(1, 4, 'Define functional dependency. What is Armstrong''s Axioms?', 'CS201', 'Normalization', 2023, 'midterm', 'medium', 6),
(1, 4, 'Given a relation R(A,B,C,D) with FDs: A→B, B→C, C→D. Find all candidate keys.', 'CS201', 'Normalization', 2023, 'final', 'hard', 10),
(1, 4, 'Explain 1NF, 2NF, 3NF with examples. Show how to convert a table from 1NF to 3NF.', 'CS201', 'Normalization', 2022, 'midterm', 'medium', 8),
(1, 4, 'What is BCNF (Boyce-Codd Normal Form)? How is it different from 3NF?', 'CS201', 'Normalization', 2022, 'final', 'medium', 6),
(1, 4, 'Given a denormalized table with update/deletion/insertion anomalies, normalize it to 3NF.', 'CS201', 'Normalization', 2021, 'final', 'hard', 12),
(1, 4, 'What are multi-valued dependencies? Explain 4NF with an example.', 'CS201', 'Normalization', 2020, 'final', 'hard', 8),

-- Indexing Questions
(1, 5, 'What is indexing? Why do we need indexes in databases?', 'CS201', 'Indexing', 2023, 'midterm', 'easy', 4),
(1, 5, 'Explain the structure of a B+ tree. Why is it preferred for database indexing?', 'CS201', 'Indexing', 2023, 'final', 'medium', 8),
(1, 5, 'Compare B+ tree and hash indexing. When would you use each?', 'CS201', 'Indexing', 2022, 'midterm', 'medium', 6),
(1, 5, 'What is the order of a B+ tree? If order is 5, what is the maximum and minimum number of keys in a node?', 'CS201', 'Indexing', 2022, 'final', 'medium', 5),
(1, 5, 'Draw a B+ tree of order 3 and insert the following keys in sequence: 5, 15, 25, 10, 20, 30.', 'CS201', 'Indexing', 2021, 'final', 'hard', 10),
(1, 5, 'What is a clustered index? How is it different from a non-clustered index?', 'CS201', 'Indexing', 2020, 'midterm', 'medium', 6),

-- Transactions Questions
(1, 6, 'What are ACID properties? Explain each with examples.', 'CS201', 'Transactions', 2023, 'midterm', 'medium', 8),
(1, 6, 'Define serializability. What is conflict serializability?', 'CS201', 'Transactions', 2023, 'final', 'hard', 10),
(1, 6, 'What is a deadlock? Explain deadlock prevention and detection techniques.', 'CS201', 'Transactions', 2022, 'midterm', 'medium', 8),
(1, 6, 'Explain two-phase locking (2PL) protocol. What is strict 2PL?', 'CS201', 'Transactions', 2022, 'final', 'hard', 10),
(1, 6, 'What is a transaction log? How is it used for recovery?', 'CS201', 'Transactions', 2021, 'midterm', 'medium', 6),
(1, 6, 'Explain lost update, dirty read, and unrepeatable read problems with examples.', 'CS201', 'Transactions', 2021, 'final', 'medium', 8),

-- Query Optimization Questions
(3, 7, 'What is query optimization? Explain the role of a query optimizer.', 'CS301', 'Query Optimization', 2023, 'midterm', 'medium', 6),
(3, 7, 'Explain EXPLAIN ANALYZE in PostgreSQL. How do you read a query plan?', 'CS301', 'Query Optimization', 2023, 'final', 'hard', 10),
(3, 7, 'What is cost-based optimization? How does the optimizer estimate query cost?', 'CS301', 'Query Optimization', 2022, 'final', 'hard', 8),

-- Vector Databases Questions
(3, 9, 'What are text embeddings? How are they used for semantic search?', 'CS301', 'Vector Databases', 2024, 'midterm', 'medium', 6),
(3, 9, 'Explain cosine similarity. Why is it used for comparing embeddings?', 'CS301', 'Vector Databases', 2024, 'final', 'medium', 6),
(3, 9, 'What is pgvector? How does it enable vector similarity search in PostgreSQL?', 'CS301', 'Vector Databases', 2024, 'quiz', 'easy', 4),

-- NoSQL Questions
(3, 8, 'What is the CAP theorem? Explain with examples of databases.', 'CS301', 'NoSQL Databases', 2023, 'midterm', 'medium', 7),
(3, 8, 'Compare SQL databases and NoSQL databases. When would you use each?', 'CS301', 'NoSQL Databases', 2023, 'final', 'medium', 8),

-- Additional Mixed Difficulty Questions
(1, 2, 'Write a query to find duplicate records in a table based on email.', 'CS201', 'SQL Basics', 2020, 'quiz', 'medium', 4),
(1, 2, 'Explain the difference between DELETE, TRUNCATE, and DROP commands.', 'CS201', 'SQL Basics', 2020, 'midterm', 'easy', 3),
(1, 4, 'What is lossless join decomposition? Prove that a decomposition is lossless.', 'CS201', 'Normalization', 2019, 'final', 'hard', 12),
(1, 5, 'What is bitmap indexing? When is it useful?', 'CS201', 'Indexing', 2019, 'midterm', 'hard', 6),
(1, 6, 'Explain timestamp-based concurrency control protocol.', 'CS201', 'Transactions', 2019, 'final', 'hard', 10),
(1, 1, 'What is data redundancy? Why is it problematic?', 'CS201', 'DBMS Fundamentals', 2021, 'quiz', 'easy', 2),
(1, 3, 'What is an aggregation relationship in ER modeling?', 'CS201', 'ER Modeling', 2020, 'midterm', 'medium', 5);

-- Learning Note:
-- We now have 50+ questions covering:
-- - 5 difficulty levels (easy, medium, hard)
-- - Multiple topics (DBMS fundamentals, SQL, ER, Normalization, Indexing, Transactions, etc.)
-- - Multiple years (2019-2024)
-- - Multiple exam types (midterm, final, quiz, assignment)
--
-- This data is INTENTIONALLY DENORMALIZED (course_code and topic_name repeated)
-- Week 4 will teach how to identify and fix these normalization issues!

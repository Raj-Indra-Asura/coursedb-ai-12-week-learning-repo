<!-- Auto-generated from the FastAPI OpenAPI schema by a maintainer script.
     Regenerate after changing routes. Conceptual explanations are the learner's. -->

# API Documentation

CourseDB-AI exposes a FastAPI application. Interactive docs are available at
`/docs` (Swagger UI) and `/redoc` when the server is running. The tables below
are generated from the live route table.

## Health & Diagnostics

| Method | Path | Summary |
| ------ | ---- | ------- |
| `GET` | `/health/` | Basic health check endpoint |
| `GET` | `/health/db` | Check database connection health |
| `GET` | `/health/db/counts` | Get row counts for all main tables |
| `GET` | `/health/db/tables` | Check if database tables exist |

## Core REST API

| Method | Path | Summary |
| ------ | ---- | ------- |
| `GET` | `/api/analytics/course-statistics` | Get detailed statistics for each course. |
| `GET` | `/api/analytics/difficulty-distribution` | Get distribution of questions by difficulty level. |
| `GET` | `/api/analytics/exam-type-distribution` | Get distribution of questions by exam type. |
| `GET` | `/api/analytics/marks-distribution` | Get distribution of marks across questions. |
| `GET` | `/api/analytics/overview` | Get overall system statistics. |
| `GET` | `/api/analytics/resource-summary` | Get summary statistics for resources. |
| `GET` | `/api/analytics/topic-coverage` | Get topic coverage analysis showing which topics have questions/resources. |
| `GET` | `/api/analytics/topic-frequency` | Get question count per topic, ordered by frequency. |
| `GET` | `/api/analytics/year-wise-trends` | Get topic distribution trends by academic year. |
| `GET` | `/api/courses/` | List all courses with pagination |
| `POST` | `/api/courses/` | Create a new course |
| `DELETE` | `/api/courses/{course_id}` | Delete a course |
| `GET` | `/api/courses/{course_id}` | Get a specific course by ID |
| `PUT` | `/api/courses/{course_id}` | Update an existing course |
| `GET` | `/api/courses/{course_id}/topics` | Get all topics for a specific course |
| `GET` | `/api/questions/` | List all questions with extensive filtering options. |
| `POST` | `/api/questions/` | Create a new question. |
| `GET` | `/api/questions/search/by-topic/{topic_name}` | Search questions by topic name (case-insensitive partial match). |
| `GET` | `/api/questions/stats/by-difficulty` | Get question count grouped by difficulty. |
| `GET` | `/api/questions/stats/by-year` | Get question count grouped by year. |
| `DELETE` | `/api/questions/{question_id}` | Delete a question. |
| `GET` | `/api/questions/{question_id}` | Get a specific question by ID. |
| `PUT` | `/api/questions/{question_id}` | Update an existing question (partial update supported). |
| `GET` | `/api/resources/` | List all resources with extensive filtering options. |
| `POST` | `/api/resources/` | Create a new resource. |
| `GET` | `/api/resources/stats/by-type` | Get resource count grouped by type. |
| `GET` | `/api/resources/stats/by-year` | Get resource count grouped by academic year. |
| `DELETE` | `/api/resources/{resource_id}` | Delete a resource. |
| `GET` | `/api/resources/{resource_id}` | Get a specific resource by ID. |
| `PUT` | `/api/resources/{resource_id}` | Update an existing resource (partial update supported). |
| `GET` | `/api/resources/{resource_id}/chunks` | Get all chunks for a specific resource. |
| `GET` | `/api/search/compare` | Compare semantic search vs keyword search |
| `GET` | `/api/search/health` | Check search service health |
| `GET` | `/api/search/hybrid` | Hybrid search combining semantic + keyword search |
| `GET` | `/api/search/semantic` | Search using semantic vector similarity |
| `GET` | `/api/search/semantic/similar-chunks/{chunk_id}` | Find chunks similar to a given chunk |
| `GET` | `/api/search/sql` | SQL-based search with metadata filters |
| `GET` | `/api/topics/` | List all topics with optional filtering. |
| `POST` | `/api/topics/` | Create a new topic. |
| `DELETE` | `/api/topics/{topic_id}` | Delete a topic. |
| `GET` | `/api/topics/{topic_id}` | Get a specific topic by ID. |
| `PUT` | `/api/topics/{topic_id}` | Update an existing topic (partial update supported). |
| `GET` | `/api/topics/{topic_id}/questions` | Get all questions for a specific topic. |

## DBMS Internals Demo

| Method | Path | Summary |
| ------ | ---- | ------- |
| `POST` | `/dbms-demo/bplus-tree/insert` | Demonstrate B+ tree insertion. |
| `POST` | `/dbms-demo/deadlock/detect` | Detect deadlocks from a set of transaction resource dependencies. |
| `POST` | `/dbms-demo/hash-index/lookup` | Demonstrate hash-index placement and lookup. |
| `GET` | `/dbms-demo/query-plan` | Run ``EXPLAIN`` on a representative query and return the plan. |
| `POST` | `/dbms-demo/transaction/demo` | Walk through a transaction scenario. |

## Learning Navigation

| Method | Path | Summary |
| ------ | ---- | ------- |
| `GET` | `/learning/curriculum` | Get complete overview of the 12-week learning curriculum |
| `POST` | `/learning/initialize` | Initialize or refresh the learning curriculum from filesystem |
| `GET` | `/learning/search` | Search for learning resources across all weeks |
| `GET` | `/learning/stats` | Get statistics about the learning curriculum |
| `GET` | `/learning/weeks/{week_number}` | Get navigation context for a specific week |
| `GET` | `/learning/weeks/{week_number}/details` | Get detailed information about a specific week |
| `PUT` | `/learning/weeks/{week_number}/status` | Update the status of a learning week |

## Root

| Method | Path | Summary |
| ------ | ---- | ------- |
| `GET` | `/` | Root endpoint - API information |

_Total documented endpoints: 60._

> **TODO(learner):** Add request/response examples and usage notes for the
> endpoints you implemented as part of your portfolio write-up.

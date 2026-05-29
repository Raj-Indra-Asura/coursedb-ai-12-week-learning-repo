<!-- Auto-extracted from app/db/models.py by a maintainer script. Regenerate after
     model changes. Explanations / rationale columns are for the learner. -->

# Constraints Report

Generated from the SQLAlchemy models in `app/db/models.py`. It lists primary
keys, foreign keys, unique, check, and not-null constraints per table.

## `courses`

- **Primary key:** course_id
- **Foreign keys:** (none)
- **Unique columns:** course_code
- **NOT NULL columns:** course_id, course_code, course_title
- **Check constraints:** (none)
- **Indexes:** ix_courses_course_code

## `learning_weeks`

- **Primary key:** week_id
- **Foreign keys:** (none)
- **Unique columns:** week_number
- **NOT NULL columns:** week_id, week_number, title, directory_path
- **Check constraints:** (none)
- **Indexes:** ix_learning_weeks_week_number

## `users`

- **Primary key:** user_id
- **Foreign keys:** (none)
- **Unique columns:** username, email
- **NOT NULL columns:** user_id, username, email
- **Check constraints:** (none)
- **Indexes:** ix_users_username

## `learning_resources`

- **Primary key:** resource_id
- **Foreign keys:** `week_id` -> `learning_weeks.week_id` (on_delete=CASCADE)
- **Unique columns:** (none)
- **NOT NULL columns:** resource_id, week_id, title, file_path, resource_type
- **Check constraints:** (none)
- **Indexes:** idx_learning_resource_week_order, ix_learning_resources_title

## `search_logs`

- **Primary key:** log_id
- **Foreign keys:** `user_id` -> `users.user_id` (on_delete=SET NULL)
- **Unique columns:** (none)
- **NOT NULL columns:** log_id, query_text
- **Check constraints:** (none)
- **Indexes:** idx_search_logs_user_date, ix_search_logs_created_at

## `topics`

- **Primary key:** topic_id
- **Foreign keys:** `course_id` -> `courses.course_id` (on_delete=CASCADE)
- **Unique columns:** (none)
- **NOT NULL columns:** topic_id, course_id, topic_name
- **Check constraints:** (none)
- **Indexes:** ix_topics_topic_name

## `questions`

- **Primary key:** question_id
- **Foreign keys:** `course_id` -> `courses.course_id` (on_delete=CASCADE); `topic_id` -> `topics.topic_id` (on_delete=SET NULL)
- **Unique columns:** (none)
- **NOT NULL columns:** question_id, course_id, question_text
- **Check constraints:** (none)
- **Indexes:** idx_questions_course_topic, idx_questions_year_difficulty, ix_questions_difficulty, ix_questions_year

## `resources`

- **Primary key:** resource_id
- **Foreign keys:** `course_id` -> `courses.course_id` (on_delete=CASCADE); `topic_id` -> `topics.topic_id` (on_delete=SET NULL)
- **Unique columns:** (none)
- **NOT NULL columns:** resource_id, course_id, title
- **Check constraints:** (none)
- **Indexes:** ix_resources_title

## `resource_chunks`

- **Primary key:** chunk_id
- **Foreign keys:** `resource_id` -> `resources.resource_id` (on_delete=CASCADE)
- **Unique columns:** (none)
- **NOT NULL columns:** chunk_id, resource_id, chunk_index, chunk_text
- **Check constraints:** (none)
- **Indexes:** idx_chunk_resource_index

## `chunk_embeddings`

- **Primary key:** embedding_id
- **Foreign keys:** `chunk_id` -> `resource_chunks.chunk_id` (on_delete=CASCADE)
- **Unique columns:** chunk_id
- **NOT NULL columns:** embedding_id, chunk_id
- **Check constraints:** (none)
- **Indexes:** (none)

> **TODO(learner):** For each constraint, note *why* it exists (which business
> rule or integrity requirement it enforces).

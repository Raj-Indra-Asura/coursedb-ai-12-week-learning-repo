<!-- ER skeleton auto-generated from app/db/models.py. The diagram is provided;
     the prose explanation of design choices is the learner's to write. -->

# CourseDB-AI ER Design

Entity-relationship diagram derived from the SQLAlchemy models. Relationship
lines follow the foreign keys defined in `app/db/models.py`.

```mermaid
erDiagram
    learning_weeks ||--o{ learning_resources : "week_id"
    users ||--o{ search_logs : "user_id"
    courses ||--o{ topics : "course_id"
    courses ||--o{ questions : "course_id"
    topics ||--o{ questions : "topic_id"
    courses ||--o{ resources : "course_id"
    topics ||--o{ resources : "topic_id"
    resources ||--o{ resource_chunks : "resource_id"
    resource_chunks ||--o{ chunk_embeddings : "chunk_id"

    courses {
        INTEGER course_id PK
        VARCHAR course_code
        VARCHAR course_title
        VARCHAR semester
        INTEGER credit
        DATETIME created_at
    }
    learning_weeks {
        INTEGER week_id PK
        INTEGER week_number
        VARCHAR title
        TEXT description
        VARCHAR directory_path
        VARCHAR status
        DATETIME created_at
        DATETIME updated_at
    }
    users {
        INTEGER user_id PK
        VARCHAR username
        VARCHAR email
        VARCHAR full_name
        DATETIME created_at
    }
    learning_resources {
        INTEGER resource_id PK
        INTEGER week_id FK
        VARCHAR title
        VARCHAR file_path
        VARCHAR resource_type
        TEXT description
        INTEGER order_index
        DATETIME created_at
    }
    search_logs {
        INTEGER log_id PK
        INTEGER user_id FK
        TEXT query_text
        VARCHAR search_type
        INTEGER results_count
        FLOAT execution_time_ms
        DATETIME created_at
    }
    topics {
        INTEGER topic_id PK
        INTEGER course_id FK
        VARCHAR topic_name
        TEXT description
        INTEGER week_number
        DATETIME created_at
    }
    questions {
        INTEGER question_id PK
        INTEGER course_id FK
        INTEGER topic_id FK
        TEXT question_text
        VARCHAR course_code
        VARCHAR topic_name
        INTEGER year
        VARCHAR exam_type
        VARCHAR difficulty
        INTEGER marks
        TEXT answer_text
        VARCHAR answer_reference
        DATETIME created_at
        DATETIME updated_at
    }
    resources {
        INTEGER resource_id PK
        INTEGER course_id FK
        INTEGER topic_id FK
        VARCHAR title
        VARCHAR resource_type
        VARCHAR file_path
        VARCHAR url
        TEXT description
        VARCHAR author
        INTEGER year_published
        DATETIME created_at
    }
    resource_chunks {
        INTEGER chunk_id PK
        INTEGER resource_id FK
        INTEGER chunk_index
        TEXT chunk_text
        INTEGER word_count
        DATETIME created_at
    }
    chunk_embeddings {
        INTEGER embedding_id PK
        INTEGER chunk_id FK
        VECTOR embedding
        VARCHAR model_name
        DATETIME created_at
    }
```

> **TODO(learner):** Explain the design: entity choices, cardinalities,
> intentional denormalization (e.g. `questions.course_code`), and trade-offs.

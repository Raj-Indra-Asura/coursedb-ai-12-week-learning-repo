"""
SQLAlchemy ORM Models

Implemented for CourseDB-AI Learning Project
Weeks 5-11: Progressive implementation

Models:
- Course (Week 5)
- Topic (Week 5)
- Resource (Week 5)
- Question (Week 5)
- ResourceChunk (Week 10)
- ChunkEmbedding (Week 10)
- User (Week 11)
- SearchLog (Week 11)
- LearningWeek (Learning Navigation)
- LearningResource (Learning Navigation)
"""

from pgvector.sqlalchemy import Vector
from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

Base = declarative_base()


# ==========================================
# Week 5: Core Models
# ==========================================


class Course(Base):
    """
    Stores academic course information

    Learning Objectives (Week 5):
    - Understand ORM mapping (table <-> class)
    - Learn relationship definitions
    - Understand constraints (UNIQUE, NOT NULL, CHECK)
    """

    __tablename__ = "courses"

    course_id = Column(Integer, primary_key=True, autoincrement=True)
    course_code = Column(String(20), unique=True, nullable=False, index=True)
    course_title = Column(String(200), nullable=False)
    semester = Column(String(20))
    credit = Column(Integer, CheckConstraint("credit > 0"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    topics = relationship("Topic", back_populates="course", cascade="all, delete-orphan")
    questions = relationship("Question", back_populates="course")
    resources = relationship("Resource", back_populates="course", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Course(course_code='{self.course_code}', title='{self.course_title}')>"


class Topic(Base):
    """
    Stores course topics/chapters

    Learning Objectives (Week 5):
    - Understand foreign keys
    - Learn cascade operations
    - Understand back_populates for bidirectional relationships
    """

    __tablename__ = "topics"

    topic_id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey("courses.course_id", ondelete="CASCADE"), nullable=False)
    topic_name = Column(String(100), nullable=False, index=True)
    description = Column(Text)
    week_number = Column(Integer, CheckConstraint("week_number > 0"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    course = relationship("Course", back_populates="topics")
    questions = relationship("Question", back_populates="topic")
    resources = relationship("Resource", back_populates="topic")

    def __repr__(self):
        return f"<Topic(topic_name='{self.topic_name}', course_id={self.course_id})>"


class Question(Base):
    """
    Stores previous-year exam questions

    Learning Objectives (Week 5-6):
    - Multiple foreign keys
    - CHECK constraints for enums
    - Indexing strategy (year, difficulty, topic_id)
    - Intentional denormalization (course_code, topic_name) for Week 4 lesson
    """

    __tablename__ = "questions"

    question_id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey("courses.course_id", ondelete="CASCADE"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.topic_id", ondelete="SET NULL"), nullable=True)
    question_text = Column(Text, nullable=False)

    # Intentional redundancy for normalization lesson (Week 4)
    course_code = Column(String(20))  # REDUNDANT - should be fetched via FK
    topic_name = Column(String(100))  # REDUNDANT - should be fetched via FK

    year = Column(Integer, CheckConstraint("year >= 2010 AND year <= 2030"), index=True)
    exam_type = Column(
        String(50), CheckConstraint("exam_type IN ('midterm', 'final', 'quiz', 'assignment')")
    )
    difficulty = Column(
        String(20), CheckConstraint("difficulty IN ('easy', 'medium', 'hard')"), index=True
    )
    marks = Column(Integer, CheckConstraint("marks > 0"))

    # Answer (optional)
    answer_text = Column(Text, nullable=True)
    answer_reference = Column(String(200), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    course = relationship("Course", back_populates="questions")
    topic = relationship("Topic", back_populates="questions")

    # Composite indexes for common queries
    __table_args__ = (
        Index("idx_questions_year_difficulty", "year", "difficulty"),
        Index("idx_questions_course_topic", "course_id", "topic_id"),
    )

    def __repr__(self):
        return (
            f"<Question(id={self.question_id}, year={self.year}, difficulty='{self.difficulty}')>"
        )


class Resource(Base):
    """
    Stores academic resources (notes, textbooks, papers)

    Learning Objectives (Week 5-6):
    - Understand file path storage
    - Learn resource type enumeration
    - Understand text chunking for AI (Week 10)
    """

    __tablename__ = "resources"

    resource_id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey("courses.course_id", ondelete="CASCADE"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.topic_id", ondelete="SET NULL"), nullable=True)
    title = Column(String(200), nullable=False, index=True)
    resource_type = Column(
        String(50),
        CheckConstraint("resource_type IN ('note', 'textbook', 'paper', 'video', 'slide')"),
    )
    file_path = Column(String(500), nullable=True)
    url = Column(String(500), nullable=True)
    description = Column(Text)
    author = Column(String(200))
    year_published = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    chunks = relationship("ResourceChunk", back_populates="resource", cascade="all, delete-orphan")
    course = relationship("Course", back_populates="resources")
    topic = relationship("Topic", back_populates="resources")

    def __repr__(self):
        return f"<Resource(title='{self.title}', type='{self.resource_type}')>"


# ==========================================
# Week 10: Semantic Search Models
# ==========================================


class ResourceChunk(Base):
    """
    Stores 200-300 word chunks of resources for semantic search

    Learning Objectives (Week 10):
    - Understand text chunking strategy
    - Learn chunk_index for ordering
    - Connection to embeddings (1:1 relationship)

    Why chunking?
    - Large documents exceed model context windows
    - Improves embedding quality (focused semantic meaning)
    - Enables precise retrieval (return relevant paragraph, not whole doc)
    """

    __tablename__ = "resource_chunks"

    chunk_id = Column(Integer, primary_key=True, autoincrement=True)
    resource_id = Column(
        Integer, ForeignKey("resources.resource_id", ondelete="CASCADE"), nullable=False
    )
    chunk_index = Column(Integer, nullable=False)  # Order within document
    chunk_text = Column(Text, nullable=False)
    word_count = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    resource = relationship("Resource", back_populates="chunks")
    embedding = relationship(
        "ChunkEmbedding", back_populates="chunk", uselist=False, cascade="all, delete-orphan"
    )

    __table_args__ = (Index("idx_chunk_resource_index", "resource_id", "chunk_index"),)

    def __repr__(self):
        return f"<ResourceChunk(chunk_id={self.chunk_id}, resource_id={self.resource_id}, index={self.chunk_index})>"


class ChunkEmbedding(Base):
    """
    Stores 384-dimensional vector embeddings for semantic search

    Learning Objectives (Week 10):
    - Understand vector embeddings
    - Learn pgvector extension usage
    - Understand cosine similarity search

    Model: all-MiniLM-L6-v2 (384 dimensions)
    - Fast inference
    - Good semantic quality
    - Suitable for academic text

    pgvector operators:
    - <-> : L2 distance (Euclidean)
    - <#> : Inner product
    - <=> : Cosine distance (1 - cosine similarity)
    """

    __tablename__ = "chunk_embeddings"

    embedding_id = Column(Integer, primary_key=True, autoincrement=True)
    chunk_id = Column(
        Integer,
        ForeignKey("resource_chunks.chunk_id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    embedding = Column(Vector(384))  # pgvector type for 384-dim vectors
    model_name = Column(String(100), default="all-MiniLM-L6-v2")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    chunk = relationship("ResourceChunk", back_populates="embedding")

    def __repr__(self):
        return f"<ChunkEmbedding(chunk_id={self.chunk_id}, model='{self.model_name}')>"


# ==========================================
# Week 11: User & Analytics Models
# ==========================================


class User(Base):
    """
    Basic user information for authentication/tracking

    Learning Objectives (Week 11):
    - User management basics
    - Password hashing (not implemented here - see FastAPI security)
    - Audit trail connection
    """

    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False)
    full_name = Column(String(200))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    search_logs = relationship("SearchLog", back_populates="user")

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"


class SearchLog(Base):
    """
    Logs user search queries for analytics

    Learning Objectives (Week 11):
    - Analytics data collection
    - Search result evaluation
    - User behavior tracking

    Use cases:
    - Find popular search terms
    - Evaluate search quality (results_count)
    - A/B testing different search algorithms
    """

    __tablename__ = "search_logs"

    log_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="SET NULL"), nullable=True)
    query_text = Column(Text, nullable=False)
    search_type = Column(
        String(20), CheckConstraint("search_type IN ('sql', 'semantic', 'hybrid')")
    )
    results_count = Column(Integer)
    execution_time_ms = Column(Float)  # Query performance tracking
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    # Relationships
    user = relationship("User", back_populates="search_logs")

    __table_args__ = (Index("idx_search_logs_user_date", "user_id", "created_at"),)

    def __repr__(self):
        return f"<SearchLog(query='{self.query_text[:30]}...', type='{self.search_type}')>"


# ==========================================
# Learning Navigation Models
# ==========================================


class LearningWeek(Base):
    """
    Stores metadata about each week of the 12-week learning curriculum

    Learning Objectives:
    - Track learning progression across 12 weeks
    - Enable unified navigation across curriculum
    - Link week metadata to directory structure

    Use cases:
    - Progressive navigation (prev/next week)
    - Learning path visualization
    - Curriculum overview
    - Progress tracking
    """

    __tablename__ = "learning_weeks"

    week_id = Column(Integer, primary_key=True, autoincrement=True)
    week_number = Column(
        Integer,
        CheckConstraint("week_number >= 1 AND week_number <= 12"),
        unique=True,
        nullable=False,
        index=True,
    )
    title = Column(String(200), nullable=False)
    description = Column(Text)
    directory_path = Column(String(500), nullable=False)
    status = Column(
        String(20),
        CheckConstraint("status IN ('not_started', 'in_progress', 'completed')"),
        default="not_started",
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    resources = relationship(
        "LearningResource", back_populates="week", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<LearningWeek(week={self.week_number}, title='{self.title}')>"


class LearningResource(Base):
    """
    Stores individual learning resources within each week

    Learning Objectives:
    - Index all learning materials (docs, exercises, notebooks, solutions)
    - Enable unified search across curriculum
    - Track resource types and purposes

    Resource Types:
    - documentation: README, theory notes, implementation plans
    - exercise: Practice problems, checkpoints
    - solution: Solutions to exercises
    - notebook: Jupyter notebooks for interactive learning
    - code: Example code, mini projects
    - reflection: Weekly reflections and learnings
    """

    __tablename__ = "learning_resources"

    resource_id = Column(Integer, primary_key=True, autoincrement=True)
    week_id = Column(
        Integer, ForeignKey("learning_weeks.week_id", ondelete="CASCADE"), nullable=False
    )
    title = Column(String(200), nullable=False, index=True)
    file_path = Column(String(500), nullable=False)
    resource_type = Column(
        String(50),
        CheckConstraint(
            "resource_type IN ('documentation', 'exercise', 'solution', 'notebook', 'code', 'reflection')"
        ),
        nullable=False,
    )
    description = Column(Text)
    order_index = Column(Integer, default=0)  # Order within week
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    week = relationship("LearningWeek", back_populates="resources")

    __table_args__ = (Index("idx_learning_resource_week_order", "week_id", "order_index"),)

    def __repr__(self):
        return f"<LearningResource(title='{self.title}', type='{self.resource_type}')>"


# ==========================================
# Learning Notes
# ==========================================

"""
Key SQLAlchemy Concepts Demonstrated:

1. **Declarative Base**: Base class for all models
2. **Columns**: Define table structure with types and constraints
3. **Primary Keys**: Unique identifiers (auto-incrementing INTEGERs)
4. **Foreign Keys**: Relationships between tables (course_id, topic_id)
5. **Constraints**:
   - UNIQUE: course_code, username, email
   - NOT NULL: Required fields
   - CHECK: Validate values (difficulty IN (...), marks > 0)
6. **Indexes**: Speed up queries (year, difficulty, topic_id)
7. **Relationships**:
   - One-to-Many: Course -> Topics, Course -> Questions
   - Many-to-One: Questions -> Course
   - One-to-One: ResourceChunk -> ChunkEmbedding
8. **Cascades**: Delete behavior (CASCADE, SET NULL)
9. **Timestamps**: created_at, updated_at with server_default
10. **pgvector**: Vector column type for embeddings

Week-by-Week Implementation:
- Week 5: Course, Topic, Question, Resource (core CRUD)
- Week 6: Add constraints, indexes, relationships
- Week 10: ResourceChunk, ChunkEmbedding (semantic search)
- Week 11: User, SearchLog (analytics)

Next Steps:
- Create database migration with Alembic
- Implement CRUD operations in services
- Connect models to FastAPI endpoints
"""

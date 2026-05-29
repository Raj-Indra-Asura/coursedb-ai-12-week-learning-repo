"""
Database Setup Script

Week 5-10: PostgreSQL + FastAPI Foundation

This script initializes the PostgreSQL database with:
- pgvector extension for vector similarity search
- All tables (courses, topics, questions, resources, chunks, embeddings, users, logs)
- Indexes for query optimization
- Views for analytics
- Constraints for data integrity

Usage:
    python scripts/setup_db.py [--drop-all] [--skip-pgvector]

Options:
    --drop-all: Drop all existing tables and recreate (WARNING: destroys data)
    --skip-pgvector: Skip pgvector extension installation (if already installed)

Learning Objectives:
- Understand database initialization process
- Learn pgvector extension setup
- Practice idempotent schema creation
- Understand index creation strategy
"""

import sys
import os
import argparse
from typing import Optional

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import create_engine, text, inspect
from sqlalchemy.exc import ProgrammingError, OperationalError
from sqlalchemy.orm import Session

from app.db.database import DATABASE_URL, engine, SessionLocal, get_db_info
from app.db.models import Base, Course, Topic, Question, Resource, ResourceChunk, ChunkEmbedding, User, SearchLog


def check_database_connection(db_engine) -> bool:
    """
    Verify database connection is working

    Args:
        db_engine: SQLAlchemy engine

    Returns:
        True if connection successful, False otherwise
    """
    try:
        with db_engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False


def enable_pgvector_extension(db_engine) -> bool:
    """
    Enable pgvector extension in PostgreSQL

    Learning Objectives (Week 10):
    - Understand PostgreSQL extensions
    - Learn CREATE EXTENSION IF NOT EXISTS (idempotent)
    - Practice error handling for database operations

    Args:
        db_engine: SQLAlchemy engine

    Returns:
        True if successful, False otherwise
    """
    print("\n🔧 Installing pgvector extension...")

    try:
        with db_engine.connect() as conn:
            # Check if extension already exists
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT 1 FROM pg_extension WHERE extname = 'vector'
                )
            """))
            exists = result.scalar()

            if exists:
                print("  ℹ️  pgvector extension already installed")
            else:
                # Install extension
                conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
                conn.commit()
                print("  ✅ pgvector extension installed successfully")

            # Verify installation
            result = conn.execute(text("SELECT extversion FROM pg_extension WHERE extname = 'vector'"))
            version = result.scalar()

            if version:
                print(f"  📦 pgvector version: {version}")
                return True
            else:
                print("  ⚠️  pgvector extension not found after installation")
                return False

    except ProgrammingError as e:
        if "permission denied" in str(e).lower():
            print(f"  ❌ Permission denied: Need superuser access to install extensions")
            print(f"  💡 Run: psql -U postgres -d {get_db_info()['database']} -c 'CREATE EXTENSION vector;'")
        else:
            print(f"  ❌ Error installing pgvector: {e}")
        return False
    except Exception as e:
        print(f"  ❌ Unexpected error: {e}")
        return False


def drop_all_tables(db_engine):
    """
    Drop all tables (WARNING: destroys all data)

    Learning Objectives (Week 5):
    - Understand metadata.drop_all()
    - Learn cascade deletion
    - Practice safe destructive operations

    Args:
        db_engine: SQLAlchemy engine
    """
    print("\n⚠️  Dropping all existing tables...")

    try:
        Base.metadata.drop_all(bind=db_engine)
        print("  ✅ All tables dropped successfully")
    except Exception as e:
        print(f"  ❌ Error dropping tables: {e}")
        raise


def create_all_tables(db_engine):
    """
    Create all tables defined in SQLAlchemy models

    Learning Objectives (Week 5-10):
    - Understand metadata.create_all() (idempotent)
    - Learn table creation order (handles foreign keys)
    - Practice schema deployment

    Args:
        db_engine: SQLAlchemy engine
    """
    print("\n📊 Creating database tables...")

    try:
        Base.metadata.create_all(bind=db_engine)
        print("  ✅ All tables created successfully")

        # Verify tables were created
        inspector = inspect(db_engine)
        tables = inspector.get_table_names()

        print(f"\n📋 Created {len(tables)} tables:")
        for table in sorted(tables):
            print(f"   • {table}")

    except Exception as e:
        print(f"  ❌ Error creating tables: {e}")
        raise


def create_additional_indexes(db_engine):
    """
    Create additional indexes for query optimization

    Learning Objectives (Week 7):
    - Understand index strategy
    - Learn IVFFLAT index for pgvector (approximate nearest neighbor)
    - Balance between query speed and insert speed

    Args:
        db_engine: SQLAlchemy engine
    """
    print("\n🔍 Creating additional indexes...")

    indexes = [
        # pgvector IVFFLAT index for fast similarity search
        # Learning Note: IVFFLAT divides vectors into clusters for faster search
        # lists=100: Number of clusters (good for ~10K-100K vectors)
        # opclass: vector_cosine_ops for cosine distance
        """
        CREATE INDEX IF NOT EXISTS idx_chunk_embeddings_vector
        ON chunk_embeddings
        USING ivfflat (embedding vector_cosine_ops)
        WITH (lists = 100)
        """,

        # Additional text search indexes
        """
        CREATE INDEX IF NOT EXISTS idx_questions_text_search
        ON questions
        USING gin(to_tsvector('english', question_text))
        """,

        """
        CREATE INDEX IF NOT EXISTS idx_resources_title_search
        ON resources
        USING gin(to_tsvector('english', title))
        """,
    ]

    try:
        with db_engine.connect() as conn:
            for idx_sql in indexes:
                try:
                    conn.execute(text(idx_sql))
                    conn.commit()
                    # Extract index name from SQL
                    idx_name = idx_sql.split("IF NOT EXISTS")[1].split()[0].strip()
                    print(f"  ✅ Created index: {idx_name}")
                except Exception as e:
                    # Skip if index already exists or if there's an issue
                    if "already exists" not in str(e).lower():
                        print(f"  ⚠️  Index creation warning: {e}")

        print("  ✅ Additional indexes created successfully")

    except Exception as e:
        print(f"  ❌ Error creating indexes: {e}")
        # Don't raise - indexes are optional optimization


def create_views(db_engine):
    """
    Create database views for analytics

    Learning Objectives (Week 6):
    - Understand views (virtual tables)
    - Learn aggregation patterns
    - Practice materialized vs regular views

    Args:
        db_engine: SQLAlchemy engine
    """
    print("\n👁️  Creating database views...")

    views = [
        # Course summary view
        """
        CREATE OR REPLACE VIEW course_summary AS
        SELECT
            c.course_id,
            c.course_code,
            c.course_title,
            c.semester,
            COUNT(DISTINCT t.topic_id) as topic_count,
            COUNT(DISTINCT q.question_id) as question_count,
            COUNT(DISTINCT r.resource_id) as resource_count
        FROM courses c
        LEFT JOIN topics t ON c.course_id = t.course_id
        LEFT JOIN questions q ON c.course_id = q.course_id
        LEFT JOIN resources r ON c.course_id = r.course_id
        GROUP BY c.course_id, c.course_code, c.course_title, c.semester
        """,

        # Search analytics view
        """
        CREATE OR REPLACE VIEW search_analytics AS
        SELECT
            search_type,
            DATE(created_at) as search_date,
            COUNT(*) as search_count,
            AVG(results_count) as avg_results,
            AVG(execution_time_ms) as avg_execution_time_ms
        FROM search_logs
        GROUP BY search_type, DATE(created_at)
        """,

        # Question difficulty distribution
        """
        CREATE OR REPLACE VIEW question_difficulty_stats AS
        SELECT
            c.course_code,
            c.course_title,
            q.difficulty,
            q.exam_type,
            COUNT(*) as question_count
        FROM questions q
        JOIN courses c ON q.course_id = c.course_id
        GROUP BY c.course_code, c.course_title, q.difficulty, q.exam_type
        """,
    ]

    try:
        with db_engine.connect() as conn:
            for view_sql in views:
                try:
                    conn.execute(text(view_sql))
                    conn.commit()
                    # Extract view name
                    view_name = view_sql.split("VIEW")[1].split("AS")[0].strip()
                    print(f"  ✅ Created view: {view_name}")
                except Exception as e:
                    print(f"  ⚠️  View creation warning: {e}")

        print("  ✅ Database views created successfully")

    except Exception as e:
        print(f"  ❌ Error creating views: {e}")
        # Don't raise - views are optional


def verify_setup(db_engine):
    """
    Verify database setup is correct

    Args:
        db_engine: SQLAlchemy engine

    Returns:
        True if verification passed, False otherwise
    """
    print("\n✅ Verifying database setup...")

    try:
        inspector = inspect(db_engine)

        # Check tables
        tables = inspector.get_table_names()
        expected_tables = ['courses', 'topics', 'questions', 'resources',
                          'resource_chunks', 'chunk_embeddings', 'users', 'search_logs']

        missing_tables = set(expected_tables) - set(tables)
        if missing_tables:
            print(f"  ❌ Missing tables: {missing_tables}")
            return False

        print(f"  ✅ All {len(expected_tables)} core tables exist")

        # Check pgvector extension
        with db_engine.connect() as conn:
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT 1 FROM pg_extension WHERE extname = 'vector'
                )
            """))
            pgvector_exists = result.scalar()

            if pgvector_exists:
                print("  ✅ pgvector extension is installed")
            else:
                print("  ⚠️  pgvector extension not found")
                return False

        # Check chunk_embeddings table has vector column
        columns = [col['name'] for col in inspector.get_columns('chunk_embeddings')]
        if 'embedding' in columns:
            print("  ✅ Vector embedding column exists")
        else:
            print("  ❌ Vector embedding column not found")
            return False

        print("\n🎉 Database verification passed!")
        return True

    except Exception as e:
        print(f"  ❌ Verification error: {e}")
        return False


def print_database_info():
    """Print database connection information"""
    print("\n" + "=" * 60)
    print("CourseDB-AI Database Setup")
    print("=" * 60)

    db_info = get_db_info()
    print("\n📊 Database Information:")
    print(f"   Driver:   {db_info['driver']}")
    print(f"   Host:     {db_info['host']}")
    print(f"   Port:     {db_info['port']}")
    print(f"   Database: {db_info['database']}")
    print(f"   Username: {db_info['username']}")
    print()


def main():
    """Main setup function"""
    parser = argparse.ArgumentParser(
        description="Initialize CourseDB-AI database"
    )
    parser.add_argument(
        "--drop-all",
        action="store_true",
        help="Drop all existing tables and recreate (WARNING: destroys data)"
    )
    parser.add_argument(
        "--skip-pgvector",
        action="store_true",
        help="Skip pgvector extension installation"
    )

    args = parser.parse_args()

    # Print database info
    print_database_info()

    # Check database connection
    print("🔌 Checking database connection...")
    if not check_database_connection(engine):
        print("\n❌ Cannot connect to database. Please check:")
        print("   1. PostgreSQL is running")
        print("   2. Database exists")
        print("   3. Credentials are correct (DATABASE_URL environment variable)")
        print(f"\n   Current DATABASE_URL: {DATABASE_URL.split('@')[0]}@...")
        sys.exit(1)

    print("  ✅ Database connection successful")

    try:
        # Install pgvector extension
        if not args.skip_pgvector:
            if not enable_pgvector_extension(engine):
                print("\n⚠️  Warning: pgvector installation failed")
                print("Continuing with setup, but semantic search will not work")
                print()
        else:
            print("\n⏭️  Skipping pgvector installation (--skip-pgvector)")

        # Drop tables if requested
        if args.drop_all:
            confirm = input("\n⚠️  Are you sure you want to drop all tables? Type 'yes' to confirm: ")
            if confirm.lower() == 'yes':
                drop_all_tables(engine)
            else:
                print("  ℹ️  Drop operation cancelled")

        # Create tables
        create_all_tables(engine)

        # Create additional indexes
        create_additional_indexes(engine)

        # Create views
        create_views(engine)

        # Verify setup
        if verify_setup(engine):
            print("\n" + "=" * 60)
            print("✅ Database Setup Complete!")
            print("=" * 60)
            print("\n📝 Next Steps:")
            print("   1. Run: python scripts/seed_data.py")
            print("   2. Run: python scripts/generate_embeddings.py")
            print("   3. Start API: uvicorn app.backend.main:app --reload")
            print()
        else:
            print("\n⚠️  Setup completed with warnings")
            sys.exit(1)

    except Exception as e:
        print(f"\n❌ Fatal error during setup: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

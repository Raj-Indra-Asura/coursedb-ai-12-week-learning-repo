-- ============================================================================
-- CourseDB-AI: Database bootstrap script
-- ----------------------------------------------------------------------------
-- This file is mounted into the Postgres container at
-- /docker-entrypoint-initdb.d/init_db.sql and is executed automatically the
-- FIRST time the data volume is initialised.
--
-- Responsibilities:
--   1. Enable the PostgreSQL extensions the project depends on.
--      - vector  : pgvector, provides the `vector` column type + ANN search.
--      - pg_trgm : trigram matching for fuzzy / `ILIKE` text search.
--   2. (Optional) Create a least-privilege application role.
--
-- The schema itself is created by Alembic migrations (`alembic upgrade head`)
-- or `scripts/setup_db.py`, NOT here. Keep this file limited to cluster-level
-- bootstrap so it stays idempotent and migration-driven.
-- ============================================================================

-- Required extensions ---------------------------------------------------------
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Optional least-privilege application role -----------------------------------
-- The superuser defined by POSTGRES_USER owns the database. For defense in
-- depth you may run the application as a non-superuser role with only the
-- privileges it needs. This is created idempotently.
DO
$$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'coursedb_app') THEN
        CREATE ROLE coursedb_app LOGIN PASSWORD 'coursedb_app_password';
    END IF;
END
$$;

-- Allow the application role to use the public schema and operate on objects
-- created later by migrations.
GRANT USAGE ON SCHEMA public TO coursedb_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO coursedb_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
    GRANT USAGE, SELECT ON SEQUENCES TO coursedb_app;

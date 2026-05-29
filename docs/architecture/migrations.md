# Database Migrations (Alembic)

CourseDB-AI uses [Alembic](https://alembic.sqlalchemy.org/) to manage the
PostgreSQL schema. The SQLAlchemy models in `app/db/models.py` are the single
source of truth; Alembic turns changes to those models into versioned, ordered
migration scripts under `alembic/versions/`.

## Layout

```
alembic.ini                     # Alembic configuration (logging, script location)
alembic/
├── env.py                      # Wires Alembic to app.db.models.Base + DATABASE_URL
├── script.py.mako              # Template used when generating a new revision
└── versions/
    └── f0f92986b448_initial_schema.py   # Initial schema (8 core + 2 learning tables)
```

## Configuration notes

- `alembic/env.py` imports `Base` from `app.db.models` so `target_metadata`
  reflects every model.
- The database URL is read from the `DATABASE_URL` environment variable when
  set; otherwise it falls back to the placeholder in `alembic.ini`. Always set
  `DATABASE_URL` (the `.env` file and `docker-compose.yml` already do this).
- The initial migration creates the `vector` and `pg_trgm` extensions on
  PostgreSQL before creating the `chunk_embeddings` table (which uses a
  `vector(384)` column). On SQLite these statements are skipped.

## Common commands

All commands assume your virtual environment is active and `DATABASE_URL`
points at the target database.

| Action | Command |
| --- | --- |
| Apply all migrations | `alembic upgrade head` |
| Roll back one migration | `alembic downgrade -1` |
| Roll back everything | `alembic downgrade base` |
| Show current revision | `alembic current` |
| Show history | `alembic history --verbose` |

There are also `make migrate` and related shortcuts in the `Makefile`.

## Adding a new migration

1. Edit the models in `app/db/models.py` (add/alter a column, table, index,
   constraint, etc.).
2. Generate a revision by autogeneration:

   ```bash
   alembic revision --autogenerate -m "short description of the change"
   ```

3. **Review the generated file** in `alembic/versions/`. Autogenerate is a
   starting point, not a guarantee. In particular check:
   - `server_default` values render the way you expect on PostgreSQL.
   - `CheckConstraint` and named constraints are present.
   - pgvector columns import `pgvector.sqlalchemy` and use the right `dim`.
   - Any data migration / backfill you need is added by hand.
4. Apply it locally against a disposable database:

   ```bash
   alembic upgrade head
   ```

5. Verify the downgrade path works too:

   ```bash
   alembic downgrade -1 && alembic upgrade head
   ```

6. Commit the new file in `alembic/versions/` together with the model change in
   the same commit.

## Continuous integration

The CI workflow (`.github/workflows/ci.yml`) runs `alembic upgrade head`
against a PostgreSQL service container that uses the `pgvector/pgvector:pg16`
image, so a broken or missing migration fails the build.

## Troubleshooting

- **`Can't locate revision identified by ...`** — your local DB is ahead of the
  scripts in `versions/`. Run `alembic downgrade base` on a disposable DB, or
  re-create the database.
- **`type "vector" does not exist`** — the pgvector extension is not installed.
  Use the `pgvector/pgvector:pg16` image or run `CREATE EXTENSION vector;` as a
  superuser (see `scripts/init_db.sql`).
- **Autogenerate produces an empty migration** — the models already match the
  database; there is nothing to migrate.

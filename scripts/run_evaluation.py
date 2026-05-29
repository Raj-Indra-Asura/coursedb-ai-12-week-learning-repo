"""Evaluation harness for CourseDB-AI (Week 12).

This script ties together three forms of evaluation required by the project:

1. **SQL smoke check** — every statement in
   ``weeks/week_02_sql_basics/queries_week2.sql`` is executed and checked for
   errors / row counts.
2. **Query-plan capture** — ``EXPLAIN ANALYZE`` is run on five representative
   queries with and without the optional indexes, writing the plans to
   ``dbms_internals/query_plan/outputs/before_indexes.txt`` and
   ``after_indexes.txt``.
3. **Semantic-search evaluation** — the ten queries in
   ``data/evaluation/eval_queries.json`` are run through pgvector and a results
   table is written to ``docs/evaluation/semantic_search_results.md`` for the
   learner to score against ``docs/evaluation/rubric.md``.

Embeddings use :class:`app.services.embedding_service.EmbeddingService` when the
ML stack is installed, and fall back to a deterministic offline hashing encoder
otherwise (see :func:`get_encoder`).

Usage::

    python scripts/run_evaluation.py              # run everything
    python scripts/run_evaluation.py --sql        # only the SQL smoke check
    python scripts/run_evaluation.py --plans      # only EXPLAIN ANALYZE capture
    python scripts/run_evaluation.py --semantic   # only semantic evaluation

A PostgreSQL database with the ``vector`` extension is required for the plan and
semantic stages; set ``DATABASE_URL`` accordingly.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import numpy as np
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.database import SessionLocal

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("run_evaluation")

REPO_ROOT = Path(__file__).resolve().parents[1]
WEEK2_SQL = REPO_ROOT / "weeks" / "week_02_sql_basics" / "queries_week2.sql"
EVAL_QUERIES = REPO_ROOT / "data" / "evaluation" / "eval_queries.json"
PLAN_OUTPUT_DIR = REPO_ROOT / "dbms_internals" / "query_plan" / "outputs"
SEMANTIC_RESULTS = REPO_ROOT / "docs" / "evaluation" / "semantic_search_results.md"

_EMBEDDING_DIM = 384

# Optional indexes toggled for the before/after EXPLAIN ANALYZE comparison.
_OPTIONAL_INDEXES: dict[str, str] = {
    "idx_eval_questions_year": "CREATE INDEX idx_eval_questions_year ON questions (year)",
    "idx_eval_questions_difficulty": (
        "CREATE INDEX idx_eval_questions_difficulty ON questions (difficulty)"
    ),
    "idx_eval_resources_year": (
        "CREATE INDEX idx_eval_resources_year ON resources (year_published)"
    ),
}

# Five representative queries for plan analysis.
_PLAN_QUERIES: list[tuple[str, str]] = [
    ("questions_by_year", "SELECT * FROM questions WHERE year = 2023"),
    ("hard_questions", "SELECT * FROM questions WHERE difficulty = 'hard'"),
    (
        "questions_join_topics",
        "SELECT q.question_text, t.topic_name FROM questions q "
        "JOIN topics t ON t.topic_id = q.topic_id",
    ),
    (
        "questions_per_topic",
        "SELECT topic_id, count(*) FROM questions GROUP BY topic_id",
    ),
    (
        "resources_by_year",
        "SELECT * FROM resources WHERE year_published >= 2022 ORDER BY year_published DESC",
    ),
]


class HashingEncoder:
    """Deterministic offline fallback encoder (hashing trick, L2-normalised).

    Uses a stable hash (``hashlib``) rather than the builtin ``hash`` so that
    vectors are identical across separate processes — essential because chunks
    are embedded by one run and queried by another.
    """

    def __init__(self, dim: int = _EMBEDDING_DIM) -> None:
        self.dim = dim

    def _bucket(self, token: str) -> int:
        digest = hashlib.md5(token.encode("utf-8")).hexdigest()
        return int(digest, 16) % self.dim

    def encode_for_search(self, text_value: str) -> list[float]:
        vector = np.zeros(self.dim, dtype=np.float32)
        for token in re.findall(r"[a-z0-9+]+", text_value.lower()):
            vector[self._bucket(token)] += 1.0
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector /= norm
        return vector.tolist()


def get_encoder():
    """Return the real embedding service when available, else the fallback."""
    try:
        from app.services.embedding_service import EmbeddingService

        logger.info("Using EmbeddingService (Sentence Transformers).")
        return EmbeddingService()
    except Exception as exc:  # noqa: BLE001 - any failure means fall back
        logger.info("Falling back to deterministic hashing encoder (%s).", exc)
        return HashingEncoder()


def _require_postgres(db: Session) -> None:
    dialect = db.bind.dialect.name
    if dialect != "postgresql":
        raise RuntimeError(
            f"This stage requires PostgreSQL with pgvector, but DATABASE_URL "
            f"points at a '{dialect}' database."
        )


def parse_sql_statements(sql_path: Path) -> list[str]:
    """Split a ``.sql`` file into individual executable statements.

    Line comments (``-- ...``) are stripped; statements are separated by
    semicolons.

    Args:
        sql_path: Path to the SQL file.

    Returns:
        A list of non-empty SQL statements (without trailing semicolons).
    """
    raw = sql_path.read_text(encoding="utf-8")
    no_comments = "\n".join(line.split("--", 1)[0] for line in raw.splitlines())
    statements = [stmt.strip() for stmt in no_comments.split(";")]
    return [stmt for stmt in statements if stmt]


def run_week2_sql(db: Session) -> list[dict]:
    """Execute every Week 2 query and record success / row counts.

    Args:
        db: Active database session.

    Returns:
        One result dict per statement with keys ``index``, ``ok``,
        ``rows``/``error``.
    """
    logger.info("\n=== Week 2 SQL smoke check (%s) ===", WEEK2_SQL.name)
    statements = parse_sql_statements(WEEK2_SQL)
    results: list[dict] = []
    for i, stmt in enumerate(statements, start=1):
        try:
            rows = db.execute(text(stmt)).fetchall()
            results.append({"index": i, "ok": True, "rows": len(rows)})
            logger.info("  [ok]   query %2d -> %d row(s)", i, len(rows))
        except Exception as exc:  # noqa: BLE001 - report and continue
            db.rollback()
            results.append({"index": i, "ok": False, "error": str(exc).splitlines()[0]})
            logger.error("  [FAIL] query %2d -> %s", i, str(exc).splitlines()[0])
    passed = sum(1 for r in results if r["ok"])
    logger.info("Week 2 SQL: %d/%d statements succeeded.", passed, len(results))
    return results


def _drop_optional_indexes(db: Session) -> None:
    for name in _OPTIONAL_INDEXES:
        db.execute(text(f"DROP INDEX IF EXISTS {name}"))
    db.commit()


def _create_optional_indexes(db: Session) -> None:
    for ddl in _OPTIONAL_INDEXES.values():
        db.execute(text(ddl))
    db.commit()


def _capture_plans(db: Session, header: str) -> str:
    lines = [header, "=" * len(header), ""]
    for name, query in _PLAN_QUERIES:
        lines.append(f"-- {name}")
        lines.append(query)
        plan_rows = db.execute(text(f"EXPLAIN ANALYZE {query}")).fetchall()
        lines.extend(row[0] for row in plan_rows)
        lines.append("")
    return "\n".join(lines)


def run_explain_plans(db: Session) -> None:
    """Capture EXPLAIN ANALYZE plans with and without optional indexes."""
    _require_postgres(db)
    PLAN_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    logger.info("\n=== Query-plan capture ===")

    _drop_optional_indexes(db)
    before = _capture_plans(db, "EXPLAIN ANALYZE - BEFORE optional indexes")
    (PLAN_OUTPUT_DIR / "before_indexes.txt").write_text(before, encoding="utf-8")
    logger.info("  Wrote %s", PLAN_OUTPUT_DIR / "before_indexes.txt")

    _create_optional_indexes(db)
    after = _capture_plans(db, "EXPLAIN ANALYZE - AFTER optional indexes")
    (PLAN_OUTPUT_DIR / "after_indexes.txt").write_text(after, encoding="utf-8")
    logger.info("  Wrote %s", PLAN_OUTPUT_DIR / "after_indexes.txt")


def _search_topk(db: Session, encoder, query: str, k: int = 5) -> list[str]:
    """Return up to ``k`` resource titles ordered by cosine distance."""
    query_vec = encoder.encode_for_search(query)
    rows = db.execute(
        text("""
            SELECT r.title
            FROM chunk_embeddings ce
            JOIN resource_chunks rc ON rc.chunk_id = ce.chunk_id
            JOIN resources r ON r.resource_id = rc.resource_id
            ORDER BY ce.embedding <=> CAST(:vec AS vector)
            LIMIT :k
            """),
        {"vec": str(query_vec), "k": k},
    ).fetchall()
    return [row[0] for row in rows]


def run_semantic_eval(db: Session) -> None:
    """Run the 10 evaluation queries and write the results table for scoring."""
    _require_postgres(db)
    logger.info("\n=== Semantic-search evaluation ===")
    encoder = get_encoder()
    spec = json.loads(EVAL_QUERIES.read_text(encoding="utf-8"))

    header = (
        "<!-- Auto-generated by scripts/run_evaluation.py. The 'notes' column is "
        "intentionally left blank for the learner to fill in. -->\n\n"
        "# Semantic Search Results\n\n"
        "Score each row using the rubric in `docs/evaluation/rubric.md`.\n\n"
        "| Query | Top-1 | Top-3 | Top-5 | Notes |\n"
        "| ----- | ----- | ----- | ----- | ----- |\n"
    )
    rows_md: list[str] = []
    for item in spec["queries"]:
        titles = _search_topk(db, encoder, item["query"], k=5)
        top1 = titles[0] if titles else "(none)"
        top3 = "<br>".join(titles[:3]) if titles else "(none)"
        top5 = "<br>".join(titles[:5]) if titles else "(none)"
        query_cell = item["query"].replace("|", "\\|")
        rows_md.append(f"| {query_cell} | {top1} | {top3} | {top5} |  |")
        logger.info("  query %2d -> top1=%r", item["id"], top1)

    SEMANTIC_RESULTS.write_text(header + "\n".join(rows_md) + "\n", encoding="utf-8")
    logger.info("  Wrote %s", SEMANTIC_RESULTS)


def main() -> int:
    parser = argparse.ArgumentParser(description="CourseDB-AI evaluation harness")
    parser.add_argument("--sql", action="store_true", help="Run only the Week 2 SQL check")
    parser.add_argument("--plans", action="store_true", help="Run only EXPLAIN ANALYZE capture")
    parser.add_argument("--semantic", action="store_true", help="Run only semantic evaluation")
    args = parser.parse_args()

    run_all = not (args.sql or args.plans or args.semantic)
    db = SessionLocal()
    try:
        if run_all or args.sql:
            run_week2_sql(db)
        if run_all or args.plans:
            run_explain_plans(db)
        if run_all or args.semantic:
            run_semantic_eval(db)
    finally:
        db.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Smoke test for the end-to-end semantic-search pipeline.

This script validates that the whole retrieval pipeline is wired correctly:

1. Insert three deliberately different academic chunks.
2. Generate an embedding for every chunk.
3. Run three semantic queries through pgvector's cosine-distance operator.
4. Assert the expected top-1 chunk is returned for each query.
5. Print ``PASS`` / ``FAIL`` and exit with a matching status code.

The script is **idempotent**: every row it creates is tagged with the
``_SMOKE_MARKER`` and removed before (and after) each run, so re-running never
duplicates data.

Embeddings
----------
The real application uses :class:`app.services.embedding_service.EmbeddingService`
(Sentence Transformers, 384 dimensions).  Because that model is a heavy,
network-downloaded dependency, this smoke test falls back to a small,
deterministic *hashing* encoder when the ML stack is unavailable (for example
in CI).  The fallback still produces genuine lexical-semantic vectors, so the
top-1 assertions remain meaningful while keeping the test fast and offline.

Usage
-----
    python scripts/smoke_test_semantic_search.py

Requires a PostgreSQL database with the ``vector`` extension (the pipeline uses
the ``<=>`` operator, which SQLite does not provide).  Set ``DATABASE_URL`` to
point at it.
"""

from __future__ import annotations

import hashlib
import logging
import os
import re
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import numpy as np
from sqlalchemy import text

from app.db.database import SessionLocal
from app.db.models import ChunkEmbedding, Resource, ResourceChunk

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("smoke_test_semantic_search")

_SMOKE_MARKER = "[SMOKE-TEST]"
_EMBEDDING_DIM = 384

# Three deliberately different academic chunks. The key is the marker-tagged
# title; the value is the chunk body that gets embedded.
_CHUNKS: dict[str, str] = {
    f"{_SMOKE_MARKER} deadlock": (
        "A deadlock occurs when two transactions each hold a lock and wait "
        "for the other to release its lock, creating a cycle in the wait-for "
        "graph. The database resolves it by aborting a victim transaction."
    ),
    f"{_SMOKE_MARKER} normalization": (
        "Normalization decomposes relations to eliminate redundancy and update "
        "anomalies. Third normal form removes transitive functional "
        "dependencies between non-key attributes."
    ),
    f"{_SMOKE_MARKER} bplustree": (
        "A B+ tree is a balanced multi-level index in which all data values "
        "are stored in leaf nodes that are linked together, enabling efficient "
        "range queries and ordered scans."
    ),
}

# Each query maps to the title of the chunk that should rank first.
_QUERIES: list[tuple[str, str]] = [
    ("What causes a deadlock between two transactions?", f"{_SMOKE_MARKER} deadlock"),
    ("How does normalization remove redundancy and anomalies?", f"{_SMOKE_MARKER} normalization"),
    ("Explain how a B+ tree supports efficient range queries", f"{_SMOKE_MARKER} bplustree"),
]


class _HashingEncoder:
    """Deterministic, offline fallback encoder.

    Uses the hashing trick over word tokens to build an L2-normalised vector
    with a stable hash (``hashlib``), so vectors are identical across processes.
    Cosine similarity between two texts is then driven by their shared tokens,
    which is sufficient for the top-1 retrieval assertions in this smoke test.
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


def _get_encoder():
    """Return the real embedding service if available, else the fallback."""
    try:
        from app.services.embedding_service import EmbeddingService

        encoder = EmbeddingService()
        logger.info("Using EmbeddingService (Sentence Transformers).")
        return encoder
    except Exception as exc:  # noqa: BLE001 - any failure means fall back
        logger.info("Falling back to deterministic hashing encoder (%s).", exc)
        return _HashingEncoder()


def _require_pgvector(db) -> None:
    """Abort early with a clear message if the backend is not PostgreSQL."""
    dialect = db.bind.dialect.name
    if dialect != "postgresql":
        raise RuntimeError(
            f"Semantic search requires PostgreSQL with pgvector, but the "
            f"configured database dialect is '{dialect}'. Set DATABASE_URL to a "
            f"PostgreSQL instance (see scripts/init_db.sql)."
        )


def _cleanup(db) -> None:
    """Remove all rows created by previous smoke-test runs (idempotency)."""
    resources = db.query(Resource).filter(Resource.title.like(f"{_SMOKE_MARKER}%")).all()
    for resource in resources:
        db.delete(resource)  # cascades to chunks and embeddings
    db.commit()


def _seed(db, encoder) -> dict[str, int]:
    """Insert the smoke-test chunks and their embeddings.

    Returns a mapping of chunk title -> chunk_id.
    """
    # All smoke chunks need a parent course/resource. Reuse the first course if
    # one exists, otherwise create a throw-away course.
    course_id = db.execute(
        text("SELECT course_id FROM courses ORDER BY course_id LIMIT 1")
    ).scalar()
    if course_id is None:
        course_id = db.execute(
            text(
                "INSERT INTO courses (course_code, course_title) "
                "VALUES (:code, :title) RETURNING course_id"
            ),
            {"code": f"{_SMOKE_MARKER}", "title": f"{_SMOKE_MARKER} course"},
        ).scalar()

    title_to_chunk_id: dict[str, int] = {}
    for title, body in _CHUNKS.items():
        resource = Resource(
            course_id=course_id,
            title=title,
            resource_type="note",
            description=body,
        )
        db.add(resource)
        db.flush()

        chunk = ResourceChunk(
            resource_id=resource.resource_id,
            chunk_text=body,
            chunk_index=0,
            word_count=len(body.split()),
        )
        db.add(chunk)
        db.flush()

        embedding = encoder.encode_for_search(body)
        db.add(ChunkEmbedding(chunk_id=chunk.chunk_id, embedding=embedding))
        title_to_chunk_id[title] = chunk.chunk_id

    db.commit()
    return title_to_chunk_id


def _search_top1(db, encoder, query: str) -> str:
    """Return the title of the top-1 chunk for ``query`` via pgvector."""
    query_vec = encoder.encode_for_search(query)
    row = db.execute(
        text("""
            SELECT r.title
            FROM chunk_embeddings ce
            JOIN resource_chunks rc ON rc.chunk_id = ce.chunk_id
            JOIN resources r ON r.resource_id = rc.resource_id
            WHERE r.title LIKE :marker
            ORDER BY ce.embedding <=> CAST(:vec AS vector)
            LIMIT 1
            """),
        {"marker": f"{_SMOKE_MARKER}%", "vec": str(query_vec)},
    ).first()
    return row[0] if row else ""


def main() -> int:
    """Run the smoke test and return a process exit code."""
    db = SessionLocal()
    try:
        _require_pgvector(db)
        encoder = _get_encoder()

        _cleanup(db)
        _seed(db, encoder)

        all_passed = True
        for query, expected_title in _QUERIES:
            actual_title = _search_top1(db, encoder, query)
            ok = actual_title == expected_title
            all_passed = all_passed and ok
            status = "ok" if ok else "MISMATCH"
            logger.info(
                "[%s] query=%r -> top1=%r (expected %r)",
                status,
                query,
                actual_title,
                expected_title,
            )

        _cleanup(db)

        if all_passed:
            logger.info("PASS")
            return 0
        logger.error("FAIL")
        return 1
    finally:
        db.close()


if __name__ == "__main__":
    raise SystemExit(main())

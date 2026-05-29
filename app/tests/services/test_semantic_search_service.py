"""Tests for the semantic search service.

The live pgvector query path requires PostgreSQL, so these tests use a mocked
database session and embedding service to verify the query wiring and result
formatting deterministically.
"""

from types import SimpleNamespace
from unittest.mock import MagicMock

from app.services.semantic_search_service import SemanticSearchService


class _FakeEmbedding:
    def __init__(self) -> None:
        self.calls: list[str] = []

    def encode_for_search(self, query: str) -> list[float]:
        self.calls.append(query)
        return [0.1] * 384


def _row(**kwargs):
    defaults = dict(
        chunk_id=1,
        chunk_text="text",
        resource_id=2,
        resource_title="Title",
        resource_type="note",
        url=None,
        similarity=0.9,
    )
    defaults.update(kwargs)
    return SimpleNamespace(**defaults)


def test_init_stores_dependencies() -> None:
    db = MagicMock()
    emb = _FakeEmbedding()
    service = SemanticSearchService(db, emb)
    assert service.db is db
    assert service.embedding_service is emb


def test_search_encodes_query() -> None:
    db = MagicMock()
    db.execute.return_value.fetchall.return_value = []
    emb = _FakeEmbedding()
    SemanticSearchService(db, emb).search("deadlock")
    assert emb.calls == ["deadlock"]


def test_search_formats_rows() -> None:
    db = MagicMock()
    db.execute.return_value.fetchall.return_value = [_row(chunk_id=7, similarity=0.8)]
    results = SemanticSearchService(db, _FakeEmbedding()).search("q")
    assert results[0]["chunk_id"] == 7
    assert results[0]["similarity"] == 0.8


def test_search_passes_top_k_and_threshold() -> None:
    db = MagicMock()
    db.execute.return_value.fetchall.return_value = []
    SemanticSearchService(db, _FakeEmbedding()).search("q", top_k=3, similarity_threshold=0.7)
    params = db.execute.call_args.args[1]
    assert params["limit"] == 3
    assert params["threshold"] == 0.7


def test_search_empty_returns_empty_list() -> None:
    db = MagicMock()
    db.execute.return_value.fetchall.return_value = []
    assert SemanticSearchService(db, _FakeEmbedding()).search("q") == []

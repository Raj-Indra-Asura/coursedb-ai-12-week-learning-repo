"""Tests for the semantic search service.

The live pgvector query path requires PostgreSQL, so these tests use a mocked
database session and embedding service to verify the query wiring and result
formatting deterministically.
"""

from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

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


# ---------------------------------------------------------------------------
# search_by_course
# ---------------------------------------------------------------------------


def test_search_by_course_encodes_and_passes_filters() -> None:
    db = MagicMock()
    db.execute.return_value.fetchall.return_value = []
    emb = _FakeEmbedding()
    SemanticSearchService(db, emb).search_by_course(
        "deadlock", course_id=5, top_k=4, similarity_threshold=0.6
    )
    assert emb.calls == ["deadlock"]
    params = db.execute.call_args.args[1]
    assert params["course_id"] == 5
    assert params["limit"] == 4
    assert params["threshold"] == 0.6


def test_search_by_course_formats_rows() -> None:
    db = MagicMock()
    db.execute.return_value.fetchall.return_value = [_row(chunk_id=9, course_id=5, similarity=0.7)]
    results = SemanticSearchService(db, _FakeEmbedding()).search_by_course("q", course_id=5)
    assert results[0]["chunk_id"] == 9
    assert results[0]["course_id"] == 5
    assert results[0]["similarity"] == 0.7


# ---------------------------------------------------------------------------
# compare_with_keyword_search
# ---------------------------------------------------------------------------


def test_compare_with_keyword_search_computes_overlap() -> None:
    db = MagicMock()
    # First execute() = semantic search rows, second = keyword search rows.
    semantic_rows = [_row(chunk_id=1, similarity=0.8), _row(chunk_id=2, similarity=0.6)]
    keyword_rows = [_row(chunk_id=2), _row(chunk_id=3)]
    db.execute.side_effect = [
        MagicMock(fetchall=MagicMock(return_value=semantic_rows)),
        MagicMock(fetchall=MagicMock(return_value=keyword_rows)),
    ]

    result = SemanticSearchService(db, _FakeEmbedding()).compare_with_keyword_search("q", top_k=5)

    assert result["query"] == "q"
    assert len(result["semantic_results"]) == 2
    assert len(result["keyword_results"]) == 2
    comparison = result["comparison"]
    assert comparison["semantic_count"] == 2
    assert comparison["keyword_count"] == 2
    assert comparison["overlap_count"] == 1  # chunk_id 2 appears in both
    assert comparison["unique_to_semantic"] == 1  # chunk_id 1
    assert comparison["unique_to_keyword"] == 1  # chunk_id 3
    assert comparison["semantic_avg_score"] == round((0.8 + 0.6) / 2, 3)


def test_compare_with_keyword_search_handles_empty_semantic() -> None:
    db = MagicMock()
    db.execute.side_effect = [
        MagicMock(fetchall=MagicMock(return_value=[])),
        MagicMock(fetchall=MagicMock(return_value=[])),
    ]
    result = SemanticSearchService(db, _FakeEmbedding()).compare_with_keyword_search("q")
    assert result["comparison"]["semantic_avg_score"] == 0
    assert result["comparison"]["overlap_count"] == 0


# ---------------------------------------------------------------------------
# get_similar_chunks
# ---------------------------------------------------------------------------


def test_get_similar_chunks_passes_chunk_id_and_formats() -> None:
    db = MagicMock()
    db.execute.return_value.fetchall.return_value = [_row(chunk_id=42, similarity=0.95)]
    results = SemanticSearchService(db, _FakeEmbedding()).get_similar_chunks(7, top_k=3)
    params = db.execute.call_args.args[1]
    assert params["chunk_id"] == 7
    assert params["limit"] == 3
    assert results[0]["chunk_id"] == 42
    assert results[0]["similarity"] == 0.95


# ---------------------------------------------------------------------------
# hybrid_search
# ---------------------------------------------------------------------------


def _keyword_row(**kwargs):
    defaults = dict(
        chunk_id=1,
        chunk_text="text",
        resource_id=2,
        resource_title="Title",
        resource_type="note",
        url=None,
        keyword_score=2.0,
    )
    defaults.update(kwargs)
    return SimpleNamespace(**defaults)


def test_hybrid_search_merges_and_ranks() -> None:
    db = MagicMock()
    # search() runs first (semantic), then the keyword query.
    semantic_rows = [_row(chunk_id=1, similarity=0.9)]
    keyword_rows = [
        _keyword_row(chunk_id=1, keyword_score=4.0),
        _keyword_row(chunk_id=2, keyword_score=2.0),
    ]
    db.execute.side_effect = [
        MagicMock(fetchall=MagicMock(return_value=semantic_rows)),
        MagicMock(fetchall=MagicMock(return_value=keyword_rows)),
    ]

    results = SemanticSearchService(db, _FakeEmbedding()).hybrid_search(
        "q", top_k=5, semantic_weight=0.7
    )

    by_id = {r["chunk_id"]: r for r in results}
    # chunk 1 present in both: semantic_score kept, keyword_score normalized to 1.0 (max).
    assert by_id[1]["semantic_score"] == 0.9
    assert by_id[1]["keyword_score"] == 1.0
    assert by_id[1]["hybrid_score"] == pytest.approx(0.7 * 0.9 + 0.3 * 1.0)
    # chunk 2 only from keyword: keyword_score normalized to 2.0/4.0 = 0.5.
    assert by_id[2]["semantic_score"] == 0.0
    assert by_id[2]["keyword_score"] == 0.5
    # Results sorted by hybrid_score descending.
    scores = [r["hybrid_score"] for r in results]
    assert scores == sorted(scores, reverse=True)


def test_hybrid_search_handles_no_keyword_matches() -> None:
    db = MagicMock()
    semantic_rows = [_row(chunk_id=1, similarity=0.5)]
    db.execute.side_effect = [
        MagicMock(fetchall=MagicMock(return_value=semantic_rows)),
        MagicMock(fetchall=MagicMock(return_value=[])),
    ]
    results = SemanticSearchService(db, _FakeEmbedding()).hybrid_search("q", top_k=5)
    assert len(results) == 1
    assert results[0]["keyword_score"] == 0.0
    assert results[0]["hybrid_score"] == pytest.approx(0.7 * 0.5)


def test_hybrid_search_respects_top_k() -> None:
    db = MagicMock()
    semantic_rows = [_row(chunk_id=i, similarity=0.5) for i in range(1, 6)]
    db.execute.side_effect = [
        MagicMock(fetchall=MagicMock(return_value=semantic_rows)),
        MagicMock(fetchall=MagicMock(return_value=[])),
    ]
    results = SemanticSearchService(db, _FakeEmbedding()).hybrid_search("q", top_k=2)
    assert len(results) == 2

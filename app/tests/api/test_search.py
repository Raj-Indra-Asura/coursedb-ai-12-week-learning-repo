"""Tests for the search API.

SQL search runs against the real (SQLite) test database. Semantic search is
exercised with a mocked embedding service and a mocked vector-search backend so
the tests stay deterministic and require neither the ML stack nor pgvector.
"""

import pytest
from fastapi.testclient import TestClient

import app.api.search as search_module
from app.db.models import Question
from app.services.semantic_search_service import SemanticSearchService


def test_sql_search_returns_all(client: TestClient, sample_questions: list[Question]) -> None:
    data = client.get("/api/search/sql").json()
    assert data["search_type"] == "sql"
    assert data["count"] == 3


def test_sql_search_filter_by_difficulty(
    client: TestClient, sample_questions: list[Question]
) -> None:
    data = client.get("/api/search/sql", params={"difficulty": "hard"}).json()
    assert data["count"] == 1


def test_sql_search_filter_by_year(client: TestClient, sample_questions: list[Question]) -> None:
    data = client.get("/api/search/sql", params={"year": 2023}).json()
    assert data["count"] == 2


def test_sql_search_no_match(client: TestClient, sample_questions: list[Question]) -> None:
    data = client.get("/api/search/sql", params={"year": 2010}).json()
    assert data["count"] == 0


def test_search_health_reports_status(client: TestClient) -> None:
    # Embedding model is not installed in CI, so health should still respond
    # with a structured payload (healthy or unhealthy).
    data = client.get("/api/search/health").json()
    assert "status" in data


def test_semantic_search_with_mocked_services(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    class FakeEmbeddingService:
        model_name = "fake-model"

        def encode_for_search(self, query: str) -> list[float]:
            return [0.0] * 384

    canned = [{"chunk_id": 1, "similarity": 0.9, "chunk_text": "deadlock prevention"}]

    monkeypatch.setattr(search_module, "get_embedding_service", lambda: FakeEmbeddingService())
    monkeypatch.setattr(SemanticSearchService, "search", lambda self, **kwargs: canned)

    response = client.get("/api/search/semantic", params={"q": "deadlock", "top_k": 5})
    assert response.status_code == 200
    body = response.json()
    assert body["search_type"] == "semantic"
    assert body["count"] == 1
    assert body["results"] == canned


def test_semantic_search_requires_query(client: TestClient) -> None:
    assert client.get("/api/search/semantic").status_code == 422

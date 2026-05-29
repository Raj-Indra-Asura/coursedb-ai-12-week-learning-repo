"""Tests for the embedding service.

Pure numeric helpers (``compute_similarity``) are tested without loading the
model. Tests that need the actual model are skipped when
``sentence-transformers`` is not installed.
"""

import numpy as np
import pytest

from app.services.embedding_service import EmbeddingService


def _service_without_model() -> EmbeddingService:
    """Build an instance without running the model-loading ``__init__``."""
    return EmbeddingService.__new__(EmbeddingService)


def test_compute_similarity_identical_vectors() -> None:
    service = _service_without_model()
    vec = np.array([1.0, 0.0, 0.0])
    assert service.compute_similarity(vec, vec) == pytest.approx(1.0)


def test_compute_similarity_orthogonal_vectors() -> None:
    service = _service_without_model()
    a = np.array([1.0, 0.0])
    b = np.array([0.0, 1.0])
    assert service.compute_similarity(a, b) == pytest.approx(0.0)


def test_compute_similarity_opposite_vectors() -> None:
    service = _service_without_model()
    a = np.array([1.0, 0.0])
    b = np.array([-1.0, 0.0])
    assert service.compute_similarity(a, b) == pytest.approx(-1.0)


def test_compute_similarity_zero_vector_returns_zero() -> None:
    service = _service_without_model()
    assert service.compute_similarity(np.zeros(3), np.array([1.0, 2.0, 3.0])) == 0.0


def test_compute_similarity_accepts_lists() -> None:
    service = _service_without_model()
    assert service.compute_similarity([1.0, 0.0], [1.0, 0.0]) == pytest.approx(1.0)


@pytest.mark.requires_model
def test_generate_embedding_dimension() -> None:
    pytest.importorskip("sentence_transformers")
    service = EmbeddingService()
    embedding = service.generate_embedding("What is normalization?")
    assert embedding.shape == (384,)

"""Tests for the evaluation-harness inputs and the offline embedding fallback.

These cover the B7 deliverables that do not need a live database:

* ``data/evaluation/eval_queries.json`` is well-formed and matches the schema
  consumed by ``scripts/run_evaluation.py`` (a ``queries`` list of objects with
  ``id``, ``query`` and ``expected_topic``).
* The deterministic ``_HashingEncoder`` fallback in
  ``scripts/generate_embeddings.py`` produces stable, correctly shaped,
  L2-normalised vectors so the embedding pipeline runs without the ML stack.
"""

import json
from pathlib import Path

import numpy as np

from scripts.generate_embeddings import _EMBEDDING_DIM, _HashingEncoder

_REPO_ROOT = Path(__file__).resolve().parents[3]
_EVAL_QUERIES = _REPO_ROOT / "data" / "evaluation" / "eval_queries.json"


def test_eval_queries_file_exists() -> None:
    assert _EVAL_QUERIES.is_file()


def test_eval_queries_has_ten_well_formed_queries() -> None:
    spec = json.loads(_EVAL_QUERIES.read_text(encoding="utf-8"))
    queries = spec["queries"]

    assert len(queries) == 10
    for item in queries:
        assert isinstance(item["id"], int)
        assert item["query"].strip()
        assert item["expected_topic"].strip()


def test_eval_query_ids_are_unique() -> None:
    spec = json.loads(_EVAL_QUERIES.read_text(encoding="utf-8"))
    ids = [item["id"] for item in spec["queries"]]

    assert len(ids) == len(set(ids))


def test_hashing_encoder_batch_shape() -> None:
    encoder = _HashingEncoder()

    vectors = encoder.generate_embeddings_batch(["deadlock detection", "b+ tree range scan"])

    assert vectors.shape == (2, _EMBEDDING_DIM)


def test_hashing_encoder_is_deterministic() -> None:
    encoder = _HashingEncoder()

    first = encoder.generate_embeddings_batch(["normalization removes anomalies"])
    second = encoder.generate_embeddings_batch(["normalization removes anomalies"])

    assert np.array_equal(first, second)


def test_hashing_encoder_vectors_are_unit_norm() -> None:
    encoder = _HashingEncoder()

    vector = encoder.generate_embeddings_batch(["write ahead logging recovery"])[0]

    assert np.isclose(np.linalg.norm(vector), 1.0)

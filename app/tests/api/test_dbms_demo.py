"""Tests for the DBMS internals demonstration API."""

from fastapi.testclient import TestClient


def test_bplus_tree_insert(client: TestClient) -> None:
    response = client.post(
        "/dbms-demo/bplus-tree/insert", json={"keys": [10, 20, 5, 30, 15], "order": 3}
    )
    assert response.status_code == 200
    body = response.json()
    assert body["inserted_keys"] == [10, 20, 5, 30, 15]
    assert body["height"] >= 1
    assert "root" in body


def test_bplus_tree_requires_keys(client: TestClient) -> None:
    assert client.post("/dbms-demo/bplus-tree/insert", json={"keys": []}).status_code == 422


def test_hash_index_lookup(client: TestClient) -> None:
    data = client.post(
        "/dbms-demo/hash-index/lookup", params={"key": 42, "bucket_count": 10}
    ).json()
    assert data["bucket_index"] == 42 % 10
    assert data["found"] is True
    assert 42 in data["bucket_keys"]


def test_query_plan_unknown_type(client: TestClient) -> None:
    assert client.get("/dbms-demo/query-plan", params={"query_type": "nope"}).status_code == 400


def test_query_plan_known_type(client: TestClient) -> None:
    response = client.get("/dbms-demo/query-plan", params={"query_type": "questions_by_year"})
    assert response.status_code == 200
    assert response.json()["query_type"] == "questions_by_year"


def test_transaction_demo_commit(client: TestClient) -> None:
    data = client.post("/dbms-demo/transaction/demo", params={"scenario": "commit"}).json()
    assert data["scenario"] == "commit"
    assert any("COMMIT" in step for step in data["steps"])


def test_transaction_demo_unknown(client: TestClient) -> None:
    assert client.post("/dbms-demo/transaction/demo", params={"scenario": "x"}).status_code == 400


def test_deadlock_detection_positive(client: TestClient) -> None:
    payload = {
        "transactions": [
            {"tx_id": "T1", "holds": ["X"], "waits_for": ["Y"]},
            {"tx_id": "T2", "holds": ["Y"], "waits_for": ["X"]},
        ]
    }
    data = client.post("/dbms-demo/deadlock/detect", json=payload).json()
    assert data["deadlock_detected"] is True
    assert data["cycle"] is not None


def test_deadlock_detection_negative(client: TestClient) -> None:
    payload = {
        "transactions": [
            {"tx_id": "T1", "holds": ["X"], "waits_for": []},
            {"tx_id": "T2", "holds": ["Y"], "waits_for": ["X"]},
        ]
    }
    data = client.post("/dbms-demo/deadlock/detect", json=payload).json()
    assert data["deadlock_detected"] is False
    assert data["cycle"] is None

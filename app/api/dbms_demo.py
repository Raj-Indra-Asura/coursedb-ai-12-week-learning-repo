"""DBMS internals demonstration API.

Weeks 7-9: interactive demonstrations of database internals.

These endpoints wrap the educational simulators in ``dbms_internals/`` so the
frontend can visualise the algorithms:

    1. B+ tree insertion (Week 7).
    2. Hash index lookup (Week 7).
    3. Query-plan analysis via ``EXPLAIN`` (Week 8).
    4. Transaction behaviour walkthrough (Week 9).
    5. Deadlock detection with a wait-for graph (Week 9).
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.database import get_db
from dbms_internals.bplus_tree.bplus_tree import BPlusTree, BPlusTreeNode
from dbms_internals.hash_index.hash_index import HashIndex
from dbms_internals.transactions.wait_for_graph import WaitForGraph

router = APIRouter(prefix="/dbms-demo", tags=["dbms-demos"])


# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------
class BPlusTreeInsertRequest(BaseModel):
    """Request body for the B+ tree insertion demo."""

    keys: list[int] = Field(..., min_length=1, description="Keys to insert in order")
    order: int = Field(3, ge=3, le=10, description="Maximum children per node")


class BPlusTreeNodeView(BaseModel):
    """Serialised view of a single B+ tree node."""

    is_leaf: bool
    keys: list[int]
    children: list[BPlusTreeNodeView] = []


class BPlusTreeInsertResponse(BaseModel):
    """Final tree structure and summary statistics after insertion."""

    order: int
    inserted_keys: list[int]
    height: int
    root: BPlusTreeNodeView


class HashIndexLookupResponse(BaseModel):
    """Result of a hash-index lookup demonstration."""

    key: int
    bucket_count: int
    bucket_index: int
    found: bool
    bucket_keys: list[int]


class QueryPlanResponse(BaseModel):
    """Output of an ``EXPLAIN`` run."""

    query_type: str
    use_index: bool
    dialect: str
    sql: str
    plan: list[str]


class TransactionDemoResponse(BaseModel):
    """Scripted walkthrough of a transaction scenario."""

    scenario: str
    isolation_level: str | None
    steps: list[str]
    outcome: str


class TransactionInput(BaseModel):
    """A single transaction's resource holdings for deadlock detection."""

    tx_id: str
    holds: list[str] = []
    waits_for: list[str] = []


class DeadlockDetectRequest(BaseModel):
    """Request body for deadlock detection."""

    transactions: list[TransactionInput] = Field(..., min_length=1)


class DeadlockDetectResponse(BaseModel):
    """Result of wait-for-graph deadlock detection."""

    deadlock_detected: bool
    cycle: list[str] | None


BPlusTreeNodeView.model_rebuild()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _serialize_bplus_node(node: BPlusTreeNode) -> BPlusTreeNodeView:
    """Recursively convert a B+ tree node into a serialisable view."""
    children: list[BPlusTreeNodeView] = []
    if not node.is_leaf:
        children = [_serialize_bplus_node(child) for child in node.children]
    return BPlusTreeNodeView(is_leaf=node.is_leaf, keys=list(node.keys), children=children)


def _tree_height(node: BPlusTreeNode) -> int:
    """Return the height (number of levels) of the tree rooted at ``node``."""
    if node.is_leaf:
        return 1
    return 1 + max(_tree_height(child) for child in node.children)


# Whitelisted, parameter-free queries for the EXPLAIN demo. Using a fixed
# mapping avoids any user-supplied SQL (no injection surface).
_QUERY_PLAN_TEMPLATES: dict[str, str] = {
    "questions_by_year": "SELECT * FROM questions WHERE year = 2023",
    "questions_by_difficulty": "SELECT * FROM questions WHERE difficulty = 'hard'",
    "topics_by_course": "SELECT * FROM topics WHERE course_id = 1",
}


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@router.post("/bplus-tree/insert", response_model=BPlusTreeInsertResponse)
async def bplus_tree_insert(payload: BPlusTreeInsertRequest) -> BPlusTreeInsertResponse:
    """Demonstrate B+ tree insertion.

    Builds a B+ tree of the requested order, inserts the supplied keys in
    order and returns the resulting tree structure plus its height.

    Args:
        payload: Keys to insert and the tree order.

    Returns:
        The final tree structure and summary statistics.
    """
    tree = BPlusTree(order=payload.order)
    for key in payload.keys:
        tree.insert(key)
    return BPlusTreeInsertResponse(
        order=payload.order,
        inserted_keys=payload.keys,
        height=_tree_height(tree.root),
        root=_serialize_bplus_node(tree.root),
    )


@router.post("/hash-index/lookup", response_model=HashIndexLookupResponse)
async def hash_index_lookup(
    key: int = Query(..., description="Key to insert and look up"),
    bucket_count: int = Query(10, ge=1, le=1000, description="Number of hash buckets"),
) -> HashIndexLookupResponse:
    """Demonstrate hash-index placement and lookup.

    Inserts ``key`` into a fresh hash index and reports which bucket it maps
    to along with the bucket's current contents.

    Args:
        key: The key to insert and look up.
        bucket_count: Number of buckets in the index.

    Returns:
        The bucket placement and lookup result.
    """
    index = HashIndex(bucket_count=bucket_count)
    index.insert(key, value=key)
    bucket_index = index._hash(key)
    bucket_keys = [k for k, _ in index.buckets[bucket_index].key_value_pairs]
    found = key in bucket_keys
    return HashIndexLookupResponse(
        key=key,
        bucket_count=bucket_count,
        bucket_index=bucket_index,
        found=found,
        bucket_keys=bucket_keys,
    )


@router.get("/query-plan", response_model=QueryPlanResponse)
async def query_plan_demo(
    query_type: str = Query(..., description=f"One of: {', '.join(_QUERY_PLAN_TEMPLATES)}"),
    use_index: bool = True,
    db: Session = Depends(get_db),
) -> QueryPlanResponse:
    """Run ``EXPLAIN`` on a representative query and return the plan.

    Only a fixed whitelist of queries can be analysed, so there is no SQL
    injection surface. The ``EXPLAIN`` syntax is chosen based on the active
    database dialect (PostgreSQL vs SQLite).

    Args:
        query_type: Which whitelisted query to analyse.
        use_index: Whether to hint that indexes should be considered (advisory;
            recorded in the response for the learner to correlate with plans).
        db: Database session.

    Raises:
        HTTPException: If ``query_type`` is unknown.

    Returns:
        The query, dialect and the textual ``EXPLAIN`` output.
    """
    if query_type not in _QUERY_PLAN_TEMPLATES:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown query_type. Choose one of: {sorted(_QUERY_PLAN_TEMPLATES)}",
        )

    sql = _QUERY_PLAN_TEMPLATES[query_type]
    dialect = db.bind.dialect.name if db.bind is not None else "unknown"
    if dialect == "postgresql":
        explain_sql = f"EXPLAIN {sql}"
    elif dialect == "sqlite":
        explain_sql = f"EXPLAIN QUERY PLAN {sql}"
    else:
        explain_sql = f"EXPLAIN {sql}"

    try:
        result = db.execute(text(explain_sql))
        plan = [" | ".join(str(col) for col in row) for row in result.fetchall()]
    except Exception as exc:  # noqa: BLE001 - surfaced to the client as 500
        raise HTTPException(status_code=500, detail=f"EXPLAIN failed: {exc}") from exc

    return QueryPlanResponse(
        query_type=query_type,
        use_index=use_index,
        dialect=dialect,
        sql=sql,
        plan=plan,
    )


@router.post("/transaction/demo", response_model=TransactionDemoResponse)
async def transaction_demo(
    scenario: str = Query(..., description="commit, rollback, or concurrent"),
    db: Session = Depends(get_db),
) -> TransactionDemoResponse:
    """Walk through a transaction scenario.

    Returns a scripted, read-only explanation of the SQL steps involved in a
    ``commit``, ``rollback`` or ``concurrent`` scenario, together with the
    current transaction isolation level. The demo does not mutate data.

    Args:
        scenario: ``"commit"``, ``"rollback"`` or ``"concurrent"``.
        db: Database session.

    Raises:
        HTTPException: If ``scenario`` is unknown.

    Returns:
        The scripted steps and outcome.
    """
    scenarios: dict[str, dict[str, Any]] = {
        "commit": {
            "steps": [
                "BEGIN;",
                "INSERT INTO questions (...) VALUES (...);",
                "UPDATE questions SET marks = marks + 1 WHERE ...;",
                "COMMIT;",
            ],
            "outcome": "All changes are made durable and visible to other transactions.",
        },
        "rollback": {
            "steps": [
                "BEGIN;",
                "INSERT INTO questions (...) VALUES (...);",
                "-- error / explicit abort",
                "ROLLBACK;",
            ],
            "outcome": "All changes are discarded; the database is unchanged (Atomicity).",
        },
        "concurrent": {
            "steps": [
                "T1: BEGIN; UPDATE topics SET ... WHERE topic_id = 1;",
                "T2: BEGIN; UPDATE topics SET ... WHERE topic_id = 1;  -- blocks",
                "T1: COMMIT;",
                "T2: (unblocks) COMMIT;",
            ],
            "outcome": "Row-level locks serialise the conflicting updates (Isolation).",
        },
    }
    if scenario not in scenarios:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown scenario. Choose one of: {sorted(scenarios)}",
        )

    isolation_level: str | None
    try:
        connection = db.connection()
        isolation_level = connection.get_isolation_level()
    except Exception:  # noqa: BLE001 - isolation level is best-effort metadata
        isolation_level = None

    return TransactionDemoResponse(
        scenario=scenario,
        isolation_level=isolation_level,
        steps=scenarios[scenario]["steps"],
        outcome=scenarios[scenario]["outcome"],
    )


@router.post("/deadlock/detect", response_model=DeadlockDetectResponse)
async def deadlock_detection(payload: DeadlockDetectRequest) -> DeadlockDetectResponse:
    """Detect deadlocks from a set of transaction resource dependencies.

    Builds a wait-for graph from the supplied transactions and runs cycle
    detection. A cycle indicates a deadlock.

    Args:
        payload: The transactions with their held and awaited resources.

    Returns:
        Whether a deadlock exists and, if so, the cycle of transaction ids.
    """
    graph = WaitForGraph()
    for tx in payload.transactions:
        graph.add_transaction(tx.tx_id, holds=tx.holds, waits_for=tx.waits_for)

    detected = graph.detect_deadlock()
    cycle = graph.get_deadlock_cycle() if detected else None
    return DeadlockDetectResponse(deadlock_detected=detected, cycle=cycle)

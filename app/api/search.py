"""
Search API Endpoints

Week 10-11: Semantic Search + Integration

Provides both SQL-based and semantic vector search.

Search Modes:
1. SQL Search: Filter by metadata (difficulty, year, topic, type)
2. Semantic Search: Find similar resources using embeddings
3. Hybrid Search: Combine SQL + semantic for best results

Learning Objectives:
- Compare keyword vs semantic search
- Understand vector similarity (cosine distance)
- Use pgvector for efficient nearest neighbor search
- Implement hybrid search strategies
"""

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.embedding_service import EmbeddingService
from app.services.semantic_search_service import SemanticSearchService
from app.services.sql_search_service import SQLSearchService

router = APIRouter(prefix="/api/search", tags=["search"])

# Global embedding service (loaded once at startup)
_embedding_service: EmbeddingService | None = None


def get_embedding_service() -> EmbeddingService:
    """Get or create embedding service singleton"""
    global _embedding_service
    if _embedding_service is None:
        _embedding_service = EmbeddingService()
    return _embedding_service


# ==========================================
# Semantic Search Endpoints
# ==========================================


@router.get("/semantic")
async def semantic_search(
    q: str = Query(..., description="Search query", min_length=1),
    top_k: int = Query(5, ge=1, le=50, description="Number of results"),
    similarity_threshold: float = Query(
        0.5, ge=0.0, le=1.0, description="Minimum similarity score"
    ),
    course_id: int | None = Query(None, description="Filter by course ID"),
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    """
    Search using semantic vector similarity

    **How it works:**
    1. Generates embedding for query using Sentence Transformers
    2. Uses pgvector cosine similarity to find nearest chunks
    3. Returns top_k results with similarity scores

    **Example:**
    ```
    GET /api/search/semantic?q=deadlock prevention&top_k=5
    ```

    Learning Note:
    - Semantic search understands meaning, not just keywords
    - "deadlock prevention" matches "avoiding lock contention"
    - Better than keyword search for conceptual queries
    """
    try:
        embedding_service = get_embedding_service()
        search_service = SemanticSearchService(db, embedding_service)

        if course_id:
            results = search_service.search_by_course(
                query=q, course_id=course_id, top_k=top_k, similarity_threshold=similarity_threshold
            )
        else:
            results = search_service.search(
                query=q, top_k=top_k, similarity_threshold=similarity_threshold
            )

        return {"query": q, "search_type": "semantic", "count": len(results), "results": results}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@router.get("/semantic/similar-chunks/{chunk_id}")
async def get_similar_chunks(
    chunk_id: int, top_k: int = Query(5, ge=1, le=20), db: Session = Depends(get_db)
) -> dict[str, Any]:
    """
    Find chunks similar to a given chunk

    Useful for:
    - "Related resources" feature
    - "Similar questions" recommendations
    - Content exploration

    Learning Note:
    - Uses existing chunk embedding (no re-encoding)
    - Excludes the original chunk from results
    """
    try:
        embedding_service = get_embedding_service()
        search_service = SemanticSearchService(db, embedding_service)

        results = search_service.get_similar_chunks(chunk_id, top_k=top_k)

        return {"chunk_id": chunk_id, "count": len(results), "results": results}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Similar chunks search failed: {str(e)}")


# ==========================================
# Hybrid Search Endpoint
# ==========================================


@router.get("/hybrid")
async def hybrid_search(
    q: str = Query(..., description="Search query", min_length=1),
    top_k: int = Query(10, ge=1, le=50),
    semantic_weight: float = Query(
        0.7, ge=0.0, le=1.0, description="Weight for semantic score (0-1)"
    ),
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    """
    Hybrid search combining semantic + keyword search

    **Algorithm:**
    1. Run semantic search (get 2 * top_k results)
    2. Run keyword search (get 2 * top_k results)
    3. Normalize scores to 0-1 range
    4. Combine scores with weights
    5. Return top_k results

    **Parameters:**
    - semantic_weight: Weight for semantic score (keyword weight = 1 - semantic_weight)
    - Default 0.7 means 70% semantic, 30% keyword

    Learning Note:
    - Hybrid search gets best of both worlds
    - Semantic finds conceptually similar content
    - Keyword ensures exact matches aren't missed
    - Weight tuning depends on use case
    """
    try:
        embedding_service = get_embedding_service()
        search_service = SemanticSearchService(db, embedding_service)

        results = search_service.hybrid_search(
            query=q, top_k=top_k, semantic_weight=semantic_weight
        )

        return {
            "query": q,
            "search_type": "hybrid",
            "semantic_weight": semantic_weight,
            "keyword_weight": 1 - semantic_weight,
            "count": len(results),
            "results": results,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Hybrid search failed: {str(e)}")


# ==========================================
# Search Comparison Endpoint
# ==========================================


@router.get("/compare")
async def compare_search(
    q: str = Query(..., description="Search query", min_length=1),
    top_k: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    """
    Compare semantic search vs keyword search

    **Returns:**
    - Semantic search results with similarity scores
    - Keyword search results
    - Comparison metrics (overlap, unique results)

    **Example:**
    ```
    GET /api/search/compare?q=database normalization&top_k=5
    ```

    Learning Note:
    - Demonstrates difference between semantic and keyword search
    - Useful for understanding when each method works better
    - Shows how hybrid search combines both approaches
    """
    try:
        embedding_service = get_embedding_service()
        search_service = SemanticSearchService(db, embedding_service)

        comparison = search_service.compare_with_keyword_search(query=q, top_k=top_k)

        return comparison

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Comparison failed: {str(e)}")


# ==========================================
# SQL Search Endpoint
# ==========================================


@router.get("/sql")
async def sql_search(
    topic_name: str | None = Query(None, description="Filter by topic name"),
    difficulty: str | None = Query(None, description="Filter by difficulty"),
    year: int | None = Query(None, ge=2010, le=2030, description="Filter by year"),
    exam_type: str | None = Query(None, description="Filter by exam type"),
    course_id: int | None = Query(None, description="Filter by course ID"),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    """
    SQL-based search with metadata filters

    **How it works:**
    - Filters questions by metadata (topic, difficulty, year, etc.)
    - Uses database indexes for fast filtering
    - Returns exact matches only

    **Example:**
    ```
    GET /api/search/sql?topic_name=Normalization&difficulty=Medium&year=2023
    ```

    Learning Note:
    - SQL search is fast for structured queries
    - Best for filtering by known metadata
    - Limited to exact matches (no semantic understanding)
    - Complement with semantic search for better results
    """
    try:
        sql_service = SQLSearchService(db)

        results = sql_service.search_questions(
            topic_name=topic_name,
            difficulty=difficulty,
            year=year,
            exam_type=exam_type,
            course_id=course_id,
            limit=limit,
        )

        return {
            "search_type": "sql",
            "filters": {
                "topic_name": topic_name,
                "difficulty": difficulty,
                "year": year,
                "exam_type": exam_type,
                "course_id": course_id,
            },
            "count": len(results),
            "results": results,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"SQL search failed: {str(e)}")


# ==========================================
# Health Check
# ==========================================


@router.get("/health")
async def search_health() -> dict[str, Any]:
    """
    Check search service health

    Returns:
    - Embedding service status
    - Model information
    """
    try:
        embedding_service = get_embedding_service()

        return {
            "status": "healthy",
            "embedding_model": embedding_service.model_name,
            "embedding_dimension": embedding_service.get_embedding_dimension(),
            "services": {"embedding": "ready", "semantic_search": "ready", "sql_search": "ready"},
        }

    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

"""
Search API Endpoints

Week 10-11: Semantic Search + Integration

Provides both SQL-based and semantic vector search.

Search Modes:
1. SQL Search: Filter by metadata (difficulty, year, topic, type)
2. Semantic Search: Find similar resources using embeddings

Learning Objectives:
- Compare keyword vs semantic search
- Understand vector similarity (cosine distance)
- Use pgvector for efficient nearest neighbor search
- Implement hybrid search strategies

TODO (Week 10):
1. Implement SQL search with filters
2. Implement semantic search with pgvector
3. Add comparison endpoint
4. Log search queries for analysis

TODO (Week 11):
5. Optimize search performance
6. Add result ranking
7. Implement hybrid search (SQL + semantic)
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

router = APIRouter(prefix="/search", tags=["search"])


# TODO (Week 10): Implement search endpoints

# SQL Search
# @router.get("/sql")
# async def sql_search(
#     topic: Optional[str] = None,
#     difficulty: Optional[str] = None,
#     year: Optional[str] = None,
#     question_type: Optional[str] = None,
#     db: Session = Depends(get_db)
# ):
#     """Search using SQL filters"""
#     pass


# Semantic Search
# @router.get("/semantic")
# async def semantic_search(
#     q: str = Query(..., description="Search query"),
#     top_k: int = Query(5, ge=1, le=20),
#     db: Session = Depends(get_db)
# ):
#     """
#     Search using semantic vector similarity
#
#     Steps:
#     1. Generate embedding for query using Sentence Transformers
#     2. Use pgvector cosine similarity to find nearest chunks
#     3. Return top_k results with similarity scores
#     """
#     pass


# Compare Search Methods
# @router.get("/compare")
# async def compare_search(
#     q: str,
#     db: Session = Depends(get_db)
# ):
#     """Compare SQL keyword search vs semantic search"""
#     pass

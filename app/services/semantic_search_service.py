"""
Semantic Search Service

Week 10: Embeddings, pgvector, Semantic Search

Implements vector similarity search using pgvector.

Learning Objectives:
- Use pgvector for similarity search
- Understand cosine distance vs cosine similarity
- Implement top-k retrieval
- Compare with keyword search

How It Works:
1. User submits query: "questions about deadlock"
2. Generate query embedding using Sentence Transformers
3. Use pgvector to find nearest neighbor chunks
4. Return top-k results with similarity scores

pgvector Operators:
- <-> : L2 distance (Euclidean)
- <#> : Negative inner product
- <=> : Cosine distance (1 - cosine similarity)

We use <=> (cosine distance) because:
- Best for normalized embeddings
- Range: 0 (identical) to 2 (opposite)
- Similarity = 1 - distance

TODO (Week 10):
1. Implement query embedding
2. Write pgvector similarity query
3. Format results with metadata
4. Add similarity score threshold
5. Implement result reranking (optional)
"""

from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Dict
import numpy as np


class SemanticSearchService:
    """Service for semantic vector search"""

    def __init__(self, db: Session, embedding_service):
        self.db = db
        self.embedding_service = embedding_service

    # TODO (Week 10): Implement semantic search methods

    def search(
        self,
        query: str,
        top_k: int = 5,
        similarity_threshold: float = 0.5
    ) -> List[Dict]:
        """
        Semantic search using vector similarity

        Args:
            query: Natural language search query
            top_k: Number of results to return
            similarity_threshold: Minimum similarity score (0-1)

        Returns:
        [
            {
                "chunk_text": "...",
                "resource_title": "...",
                "similarity": 0.85,
                "resource_id": 1,
                "chunk_id": 10
            },
            ...
        ]

        SQL Query (approximate):
        SELECT
            c.chunk_text,
            r.title as resource_title,
            1 - (e.embedding <=> $1) as similarity,
            c.resource_id,
            c.chunk_id
        FROM chunk_embeddings e
        JOIN resource_chunks c ON e.chunk_id = c.chunk_id
        JOIN resources r ON c.resource_id = r.resource_id
        WHERE 1 - (e.embedding <=> $1) > $2
        ORDER BY e.embedding <=> $1
        LIMIT $3;
        """
        # TODO (Week 10): Implement semantic search
        # 1. Generate query embedding
        # 2. Execute pgvector similarity query
        # 3. Format and return results
        pass

    def compare_with_keyword_search(
        self,
        query: str,
        top_k: int = 5
    ) -> Dict:
        """
        Compare semantic search vs keyword search

        Returns:
        {
            "query": "questions about deadlock",
            "semantic_results": [...],
            "keyword_results": [...],
            "analysis": {
                "semantic_score": 0.85,
                "keyword_score": 0.60,
                "winner": "semantic"
            }
        }
        """
        # TODO (Week 10): Implement comparison
        # 1. Run semantic search
        # 2. Run keyword search (ILIKE)
        # 3. Compare results
        # 4. Analyze which performed better
        pass

    def get_similar_chunks(
        self,
        chunk_id: int,
        top_k: int = 5
    ) -> List[Dict]:
        """
        Find similar chunks to a given chunk

        Useful for:
        - "Related resources"
        - "Similar questions"
        - Exploration
        """
        # TODO (Week 10): Implement similar chunks search
        pass

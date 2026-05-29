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
"""

from sqlalchemy import text
from sqlalchemy.orm import Session


class SemanticSearchService:
    """Service for semantic vector search"""

    def __init__(self, db: Session, embedding_service):
        """
        Initialize semantic search service

        Args:
            db: Database session
            embedding_service: EmbeddingService instance for query encoding

        Learning Note:
        - Reuses embedding_service to avoid loading model multiple times
        - Database session provided per request via dependency injection
        """
        self.db = db
        self.embedding_service = embedding_service

    def search(self, query: str, top_k: int = 5, similarity_threshold: float = 0.5) -> list[dict]:
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

        Learning Note:
        - pgvector <=> operator returns cosine distance (0-2)
        - Similarity = 1 - (distance / 2) for normalized vectors
        - Results ordered by distance (closest first)
        """
        # 1. Generate query embedding
        query_embedding = self.embedding_service.encode_for_search(query)

        # 2. Execute pgvector similarity query
        # Convert list to string format for pgvector
        embedding_str = str(query_embedding)

        sql_query = text("""
            SELECT
                rc.chunk_id,
                rc.chunk_text,
                rc.resource_id,
                r.title as resource_title,
                r.resource_type,
                r.url,
                1 - (ce.embedding <=> :query_embedding::vector) as similarity
            FROM chunk_embeddings ce
            JOIN resource_chunks rc ON ce.chunk_id = rc.chunk_id
            JOIN resources r ON rc.resource_id = r.resource_id
            WHERE 1 - (ce.embedding <=> :query_embedding::vector) >= :threshold
            ORDER BY ce.embedding <=> :query_embedding::vector
            LIMIT :limit
        """)

        results = self.db.execute(
            sql_query,
            {"query_embedding": embedding_str, "threshold": similarity_threshold, "limit": top_k},
        ).fetchall()

        # 3. Format and return results
        return [
            {
                "chunk_id": row.chunk_id,
                "chunk_text": row.chunk_text,
                "resource_id": row.resource_id,
                "resource_title": row.resource_title,
                "resource_type": row.resource_type,
                "url": row.url,
                "similarity": float(row.similarity),
            }
            for row in results
        ]

    def search_by_course(
        self, query: str, course_id: int, top_k: int = 5, similarity_threshold: float = 0.5
    ) -> list[dict]:
        """
        Semantic search filtered by course

        Same as search() but only returns results from specified course

        Learning Note:
        - Filtering after vector search is more efficient than filtering before
        - pgvector index scan + filter vs full table scan
        """
        query_embedding = self.embedding_service.encode_for_search(query)
        embedding_str = str(query_embedding)

        sql_query = text("""
            SELECT
                rc.chunk_id,
                rc.chunk_text,
                rc.resource_id,
                r.title as resource_title,
                r.resource_type,
                r.url,
                r.course_id,
                1 - (ce.embedding <=> :query_embedding::vector) as similarity
            FROM chunk_embeddings ce
            JOIN resource_chunks rc ON ce.chunk_id = rc.chunk_id
            JOIN resources r ON rc.resource_id = r.resource_id
            WHERE r.course_id = :course_id
                AND 1 - (ce.embedding <=> :query_embedding::vector) >= :threshold
            ORDER BY ce.embedding <=> :query_embedding::vector
            LIMIT :limit
        """)

        results = self.db.execute(
            sql_query,
            {
                "query_embedding": embedding_str,
                "course_id": course_id,
                "threshold": similarity_threshold,
                "limit": top_k,
            },
        ).fetchall()

        return [
            {
                "chunk_id": row.chunk_id,
                "chunk_text": row.chunk_text,
                "resource_id": row.resource_id,
                "resource_title": row.resource_title,
                "resource_type": row.resource_type,
                "url": row.url,
                "course_id": row.course_id,
                "similarity": float(row.similarity),
            }
            for row in results
        ]

    def compare_with_keyword_search(self, query: str, top_k: int = 5) -> dict:
        """
        Compare semantic search vs keyword search

        Returns:
        {
            "query": "questions about deadlock",
            "semantic_results": [...],
            "keyword_results": [...],
            "comparison": {
                "semantic_avg_score": 0.85,
                "keyword_matches": 3,
                "overlap_count": 2
            }
        }

        Learning Note:
        - Semantic search understands meaning (deadlock = lock contention)
        - Keyword search is literal (exact word match only)
        - Hybrid search combines both for best results
        """
        # 1. Run semantic search
        semantic_results = self.search(query, top_k=top_k, similarity_threshold=0.3)

        # 2. Run keyword search (ILIKE for case-insensitive)
        keyword_query = text("""
            SELECT
                rc.chunk_id,
                rc.chunk_text,
                rc.resource_id,
                r.title as resource_title,
                r.resource_type,
                r.url
            FROM resource_chunks rc
            JOIN resources r ON rc.resource_id = r.resource_id
            WHERE rc.chunk_text ILIKE :pattern
                OR r.title ILIKE :pattern
            LIMIT :limit
        """)

        keyword_results_raw = self.db.execute(
            keyword_query, {"pattern": f"%{query}%", "limit": top_k}
        ).fetchall()

        keyword_results = [
            {
                "chunk_id": row.chunk_id,
                "chunk_text": row.chunk_text,
                "resource_id": row.resource_id,
                "resource_title": row.resource_title,
                "resource_type": row.resource_type,
                "url": row.url,
                "match_type": "keyword",
            }
            for row in keyword_results_raw
        ]

        # 3. Analyze results
        semantic_chunk_ids = {r["chunk_id"] for r in semantic_results}
        keyword_chunk_ids = {r["chunk_id"] for r in keyword_results}
        overlap = semantic_chunk_ids & keyword_chunk_ids

        semantic_avg = (
            sum(r["similarity"] for r in semantic_results) / len(semantic_results)
            if semantic_results
            else 0
        )

        return {
            "query": query,
            "semantic_results": semantic_results,
            "keyword_results": keyword_results,
            "comparison": {
                "semantic_count": len(semantic_results),
                "semantic_avg_score": round(semantic_avg, 3),
                "keyword_count": len(keyword_results),
                "overlap_count": len(overlap),
                "unique_to_semantic": len(semantic_chunk_ids - keyword_chunk_ids),
                "unique_to_keyword": len(keyword_chunk_ids - semantic_chunk_ids),
            },
        }

    def get_similar_chunks(self, chunk_id: int, top_k: int = 5) -> list[dict]:
        """
        Find similar chunks to a given chunk

        Useful for:
        - "Related resources"
        - "Similar questions"
        - Content exploration

        Learning Note:
        - Uses chunk's existing embedding (no re-encoding needed)
        - Excludes the original chunk from results
        - Finds semantically related content
        """
        sql_query = text("""
            SELECT
                rc2.chunk_id,
                rc2.chunk_text,
                rc2.resource_id,
                r.title as resource_title,
                r.resource_type,
                1 - (ce2.embedding <=> ce1.embedding) as similarity
            FROM chunk_embeddings ce1
            JOIN chunk_embeddings ce2 ON ce2.chunk_id != ce1.chunk_id
            JOIN resource_chunks rc2 ON ce2.chunk_id = rc2.chunk_id
            JOIN resources r ON rc2.resource_id = r.resource_id
            WHERE ce1.chunk_id = :chunk_id
            ORDER BY ce2.embedding <=> ce1.embedding
            LIMIT :limit
        """)

        results = self.db.execute(sql_query, {"chunk_id": chunk_id, "limit": top_k}).fetchall()

        return [
            {
                "chunk_id": row.chunk_id,
                "chunk_text": row.chunk_text,
                "resource_id": row.resource_id,
                "resource_title": row.resource_title,
                "resource_type": row.resource_type,
                "similarity": float(row.similarity),
            }
            for row in results
        ]

    def hybrid_search(
        self, query: str, top_k: int = 10, semantic_weight: float = 0.7
    ) -> list[dict]:
        """
        Hybrid search combining semantic + keyword search

        Args:
            query: Search query
            top_k: Total results to return
            semantic_weight: Weight for semantic (0-1), keyword gets (1 - weight)

        Returns:
            Ranked results combining both search methods

        Algorithm:
        1. Run semantic search (get 2 * top_k results)
        2. Run keyword search (get 2 * top_k results)
        3. Normalize scores to 0-1 range
        4. Combine scores with weights
        5. Return top_k results

        Learning Note:
        - Hybrid search gets best of both worlds
        - Semantic finds conceptually similar content
        - Keyword ensures exact matches aren't missed
        - Weight tuning depends on use case
        """
        # Get extra results for better merging
        fetch_count = top_k * 2

        # 1. Semantic search
        semantic_results = self.search(query, top_k=fetch_count, similarity_threshold=0.3)

        # 2. Keyword search with scoring
        keyword_query = text("""
            SELECT
                rc.chunk_id,
                rc.chunk_text,
                rc.resource_id,
                r.title as resource_title,
                r.resource_type,
                r.url,
                (LENGTH(rc.chunk_text) - LENGTH(REPLACE(LOWER(rc.chunk_text), LOWER(:query), ''))) / LENGTH(:query) as keyword_score
            FROM resource_chunks rc
            JOIN resources r ON rc.resource_id = r.resource_id
            WHERE rc.chunk_text ILIKE :pattern
                OR r.title ILIKE :pattern
            ORDER BY keyword_score DESC
            LIMIT :limit
        """)

        keyword_results_raw = self.db.execute(
            keyword_query, {"query": query, "pattern": f"%{query}%", "limit": fetch_count}
        ).fetchall()

        # Build combined results
        combined = {}

        # Add semantic results
        for result in semantic_results:
            chunk_id = result["chunk_id"]
            combined[chunk_id] = {
                **result,
                "semantic_score": result["similarity"],
                "keyword_score": 0.0,
            }

        # Add/merge keyword results
        for row in keyword_results_raw:
            chunk_id = row.chunk_id
            keyword_score = float(row.keyword_score) if row.keyword_score else 0.0

            if chunk_id in combined:
                combined[chunk_id]["keyword_score"] = keyword_score
            else:
                combined[chunk_id] = {
                    "chunk_id": chunk_id,
                    "chunk_text": row.chunk_text,
                    "resource_id": row.resource_id,
                    "resource_title": row.resource_title,
                    "resource_type": row.resource_type,
                    "url": row.url,
                    "semantic_score": 0.0,
                    "keyword_score": keyword_score,
                }

        # Normalize keyword scores to 0-1 range
        if combined:
            max_keyword = max(r["keyword_score"] for r in combined.values())
            if max_keyword > 0:
                for result in combined.values():
                    result["keyword_score"] = result["keyword_score"] / max_keyword

        # Compute hybrid score
        for result in combined.values():
            result["hybrid_score"] = (
                semantic_weight * result["semantic_score"]
                + (1 - semantic_weight) * result["keyword_score"]
            )

        # Sort by hybrid score and return top_k
        ranked_results = sorted(combined.values(), key=lambda x: x["hybrid_score"], reverse=True)[
            :top_k
        ]

        return ranked_results

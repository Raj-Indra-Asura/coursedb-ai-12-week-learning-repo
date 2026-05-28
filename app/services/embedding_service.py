"""
Embedding Service

Week 10: Embeddings, pgvector, Semantic Search

Generates vector embeddings for text using Sentence Transformers.

Learning Objectives:
- Use pre-trained embedding models
- Understand vector representations
- Handle batch processing
- Optimize embedding generation

Model: sentence-transformers/all-MiniLM-L6-v2
- Embedding dimension: 384
- Max sequence length: 256 tokens (512 with truncation)
- Fast and efficient for semantic search

Why This Model?
- Lightweight and fast
- Good performance for semantic search
- Lower compute requirements than larger models

TODO (Week 10):
1. Load Sentence Transformers model
2. Implement text embedding generation
3. Handle batch processing
4. Add error handling for long texts
5. Cache model in memory
"""

from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Union


class EmbeddingService:
    """Service for generating text embeddings"""

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model_name = model_name
        # TODO (Week 10): Load model
        # self.model = SentenceTransformer(model_name)

    # TODO (Week 10): Implement embedding methods

    def generate_embedding(self, text: str) -> np.ndarray:
        """
        Generate embedding for a single text

        Args:
            text: Input text (will be truncated if too long)

        Returns:
            numpy array of shape (384,)

        Example:
        >>> service = EmbeddingService()
        >>> embedding = service.generate_embedding("What is normalization?")
        >>> embedding.shape
        (384,)
        """
        # TODO (Week 10): Generate embedding using model.encode()
        pass

    def generate_embeddings_batch(self, texts: List[str]) -> np.ndarray:
        """
        Generate embeddings for multiple texts (faster than one-by-one)

        Args:
            texts: List of input texts

        Returns:
            numpy array of shape (n_texts, 384)

        Performance:
        - Batch processing is ~10x faster than individual encoding
        - Use for bulk embedding generation
        """
        # TODO (Week 10): Generate batch embeddings
        pass

    def encode_for_search(self, query: str) -> List[float]:
        """
        Encode query for semantic search

        Returns:
            List of floats for pgvector compatibility

        Note: pgvector expects List[float] not np.ndarray
        """
        # TODO (Week 10): Generate embedding and convert to list
        pass

    def compute_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """
        Compute cosine similarity between two embeddings

        Formula: cos(θ) = (A · B) / (||A|| * ||B||)

        Returns:
            Similarity score between -1 and 1 (higher = more similar)
        """
        # TODO (Week 10): Implement cosine similarity
        pass

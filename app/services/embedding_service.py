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

from typing import List
import logging

import numpy as np

logger = logging.getLogger(__name__)


class EmbeddingService:
    """Service for generating text embeddings"""

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initialize embedding service with pre-trained model

        Args:
            model_name: HuggingFace model identifier

        Learning Note:
        - Model is loaded once and cached in memory
        - Singleton pattern recommended for production use
        - First load downloads model (~80MB)
        - ``sentence_transformers`` is imported lazily so that the rest of
          the application (and the test-suite) can import this module without
          requiring the heavy ML stack to be installed.
        """
        self.model_name = model_name
        logger.info("Loading embedding model: %s ...", model_name)
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as exc:  # pragma: no cover - depends on optional dep
            raise ImportError(
                "sentence-transformers is required to use EmbeddingService. "
                "Install it with `pip install sentence-transformers`."
            ) from exc
        self.model = SentenceTransformer(model_name)
        self.model.max_seq_length = 512  # Allow longer sequences
        logger.info("Model loaded. Embedding dimension: %d", self.get_embedding_dimension())

    def get_embedding_dimension(self) -> int:
        """Get the dimension of embeddings produced by this model"""
        return self.model.get_sentence_embedding_dimension()

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

        Learning Note:
        - Sentence Transformers automatically:
          1. Tokenizes text
          2. Truncates to max_seq_length
          3. Passes through BERT-like model
          4. Mean pools token embeddings
          5. Normalizes to unit vector
        """
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")

        # encode() returns normalized embeddings by default
        embedding = self.model.encode(
            text,
            convert_to_numpy=True,
            show_progress_bar=False
        )

        return embedding

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

        Learning Note:
        - Batch processing leverages GPU/CPU parallelization
        - Model processes multiple texts simultaneously
        - Much more efficient than loop with generate_embedding()
        """
        if not texts or len(texts) == 0:
            raise ValueError("Text list cannot be empty")

        # Filter out empty texts
        valid_texts = [t for t in texts if t and t.strip()]
        if not valid_texts:
            raise ValueError("All texts are empty")

        embeddings = self.model.encode(
            valid_texts,
            convert_to_numpy=True,
            show_progress_bar=len(valid_texts) > 100,  # Show progress for large batches
            batch_size=32  # Process 32 texts at a time
        )

        return embeddings

    def encode_for_search(self, query: str) -> List[float]:
        """
        Encode query for semantic search

        Returns:
            List of floats for pgvector compatibility

        Note: pgvector expects List[float] not np.ndarray

        Learning Note:
        - pgvector SQL syntax: embedding <=> '[0.1, 0.2, ...]'::vector
        - Python list converts to proper format
        - Cosine distance operator <=> works on normalized vectors
        """
        embedding = self.generate_embedding(query)
        # Convert numpy array to Python list for pgvector
        return embedding.tolist()

    def compute_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """
        Compute cosine similarity between two embeddings

        Formula: cos(θ) = (A · B) / (||A|| * ||B||)

        Returns:
            Similarity score between -1 and 1 (higher = more similar)

        Learning Note:
        - Cosine similarity measures angle between vectors
        - 1.0 = identical direction (very similar)
        - 0.0 = perpendicular (unrelated)
        - -1.0 = opposite direction (very dissimilar)

        For normalized vectors (like sentence-transformers output):
        - cosine_similarity = dot_product (since ||A|| = ||B|| = 1)
        - cosine_distance = 1 - cosine_similarity
        """
        # Ensure inputs are numpy arrays
        if not isinstance(embedding1, np.ndarray):
            embedding1 = np.array(embedding1)
        if not isinstance(embedding2, np.ndarray):
            embedding2 = np.array(embedding2)

        # Compute cosine similarity
        dot_product = np.dot(embedding1, embedding2)
        norm1 = np.linalg.norm(embedding1)
        norm2 = np.linalg.norm(embedding2)

        # Avoid division by zero
        if norm1 == 0 or norm2 == 0:
            return 0.0

        similarity = dot_product / (norm1 * norm2)

        # Clamp to [-1, 1] due to floating point errors
        return float(np.clip(similarity, -1.0, 1.0))

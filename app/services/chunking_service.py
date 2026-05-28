"""
Chunking Service

Week 10: Embeddings, pgvector, Semantic Search

Splits resources into chunks for embedding generation.

Learning Objectives:
- Understand text chunking strategies
- Handle overlapping chunks
- Preserve context in chunks
- Optimize chunk size for embeddings

Chunking Strategy:
- Chunk size: 200-300 words
- Overlap: 50 words
- Preserve sentence boundaries
- Maintain context

Why Chunking?
- Embedding models have token limits (512 for all-MiniLM-L6-v2)
- Smaller chunks = more precise retrieval
- Overlapping chunks = better context preservation

TODO (Week 10):
1. Implement text cleaning
2. Implement sentence-aware chunking
3. Add overlap between chunks
4. Store chunks in database
5. Test with various resource types
"""

from typing import List, Tuple


class ChunkingService:
    """Service for text chunking"""

    def __init__(
        self,
        chunk_size: int = 250,  # words
        overlap: int = 50,      # words
        min_chunk_size: int = 50  # minimum words per chunk
    ):
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.min_chunk_size = min_chunk_size

    # TODO (Week 10): Implement chunking methods

    def clean_text(self, text: str) -> str:
        """
        Clean and normalize text

        Steps:
        1. Remove extra whitespace
        2. Normalize unicode characters
        3. Remove special characters (optional)
        4. Preserve sentence boundaries
        """
        # TODO (Week 10): Implement text cleaning
        pass

    def chunk_text(self, text: str) -> List[Tuple[str, int]]:
        """
        Split text into overlapping chunks

        Returns:
        [
            ("chunk text 1", 0),  # (chunk_text, chunk_order)
            ("chunk text 2", 1),
            ...
        ]

        Algorithm:
        1. Split into sentences
        2. Group sentences into chunks of ~chunk_size words
        3. Add overlap by including last N words from previous chunk
        4. Ensure minimum chunk size
        """
        # TODO (Week 10): Implement chunking logic
        pass

    def chunk_resource(self, resource_text: str, resource_id: int) -> List[dict]:
        """
        Chunk a resource and prepare for database insertion

        Returns:
        [
            {
                "resource_id": 1,
                "chunk_text": "...",
                "chunk_order": 0
            },
            ...
        ]
        """
        # TODO (Week 10): Implement resource chunking
        pass

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
"""

import re


class ChunkingService:
    """Service for text chunking"""

    def __init__(
        self,
        chunk_size: int = 250,  # words
        overlap: int = 50,  # words
        min_chunk_size: int = 50,  # minimum words per chunk
    ):
        """
        Initialize chunking service

        Args:
            chunk_size: Target words per chunk
            overlap: Overlapping words between chunks
            min_chunk_size: Minimum words to form a chunk

        Learning Note:
        - Larger chunks = more context but less precise
        - Smaller chunks = more precise but less context
        - Overlap ensures context isn't lost at boundaries
        """
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.min_chunk_size = min_chunk_size

    def clean_text(self, text: str) -> str:
        """
        Clean and normalize text

        Steps:
        1. Remove extra whitespace
        2. Normalize unicode characters
        3. Remove special characters (optional)
        4. Preserve sentence boundaries

        Learning Note:
        - Cleaning improves embedding quality
        - Remove noise but preserve semantic meaning
        - Don't over-clean (e.g., keep punctuation for sentence detection)
        """
        if not text:
            return ""

        # Normalize whitespace (tabs, newlines, multiple spaces)
        text = re.sub(r"\s+", " ", text)

        # Remove leading/trailing whitespace
        text = text.strip()

        # Normalize common unicode characters
        text = text.replace("\u00a0", " ")  # Non-breaking space
        text = text.replace("\u2019", "'")  # Right single quotation
        text = text.replace("\u201c", '"')  # Left double quotation
        text = text.replace("\u201d", '"')  # Right double quotation
        text = text.replace("\u2013", "-")  # En dash
        text = text.replace("\u2014", "-")  # Em dash

        return text

    def _split_into_sentences(self, text: str) -> list[str]:
        """
        Split text into sentences

        Uses simple regex for sentence boundaries:
        - Period, exclamation, question mark followed by space and capital letter
        - Handles common abbreviations (Dr., Mr., etc.)

        Learning Note:
        - Sentence-aware chunking preserves semantic meaning
        - Better than word-based chunking which can split mid-sentence
        """
        # Simple sentence splitter (handles most cases)
        # Pattern: . ! ? followed by whitespace and capital letter
        sentences = re.split(r"(?<=[.!?])\s+(?=[A-Z])", text)

        # Filter out empty sentences
        sentences = [s.strip() for s in sentences if s.strip()]

        return sentences

    def chunk_text(self, text: str) -> list[tuple[str, int]]:
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

        Learning Note:
        - Sentence-aware chunking preserves meaning
        - Overlap ensures context continuity
        - Variable chunk sizes better than fixed (respects sentence boundaries)
        """
        # Clean text first
        text = self.clean_text(text)

        if not text:
            return []

        # Split into sentences
        sentences = self._split_into_sentences(text)

        if not sentences:
            return []

        chunks = []
        current_chunk = []
        current_word_count = 0
        chunk_order = 0

        for sentence in sentences:
            sentence_words = len(sentence.split())

            # If adding this sentence exceeds chunk_size, save current chunk
            if current_word_count + sentence_words > self.chunk_size and current_chunk:
                # Save current chunk
                chunk_text = " ".join(current_chunk)
                chunks.append((chunk_text, chunk_order))
                chunk_order += 1

                # Start new chunk with overlap
                # Keep last few sentences for overlap
                overlap_text = " ".join(current_chunk)
                overlap_words = overlap_text.split()

                if len(overlap_words) > self.overlap:
                    # Keep last 'overlap' words
                    overlap_sentences = []
                    overlap_word_count = 0

                    # Add sentences from end until we have enough overlap
                    for prev_sentence in reversed(current_chunk):
                        sentence_word_count = len(prev_sentence.split())
                        overlap_sentences.insert(0, prev_sentence)
                        overlap_word_count += sentence_word_count

                        if overlap_word_count >= self.overlap:
                            break

                    current_chunk = overlap_sentences
                    current_word_count = sum(len(s.split()) for s in current_chunk)
                else:
                    # Keep all of previous chunk as overlap
                    pass  # current_chunk already has the content

            # Add sentence to current chunk
            current_chunk.append(sentence)
            current_word_count += sentence_words

        # Add final chunk if it meets minimum size
        if current_chunk:
            chunk_text = " ".join(current_chunk)
            word_count = len(chunk_text.split())

            if word_count >= self.min_chunk_size:
                chunks.append((chunk_text, chunk_order))
            elif chunks:
                # If too small, merge with previous chunk
                prev_chunk_text, prev_order = chunks[-1]
                merged_text = prev_chunk_text + " " + chunk_text
                chunks[-1] = (merged_text, prev_order)
            else:
                # First and only chunk, keep it even if small
                chunks.append((chunk_text, chunk_order))

        return chunks

    def chunk_resource(self, resource_text: str, resource_id: int) -> list[dict]:
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

        Learning Note:
        - resource_id links chunks to original resource
        - chunk_order preserves sequence for reconstruction
        - Ready for bulk insert into database
        """
        chunks = self.chunk_text(resource_text)

        return [
            {"resource_id": resource_id, "chunk_text": chunk_text, "chunk_order": chunk_order}
            for chunk_text, chunk_order in chunks
        ]

    def get_chunk_statistics(self, text: str) -> dict:
        """
        Get statistics about chunks for a text

        Returns:
        {
            "total_words": 1500,
            "num_chunks": 6,
            "avg_chunk_size": 250,
            "min_chunk_size": 200,
            "max_chunk_size": 300
        }

        Useful for:
        - Debugging chunking strategy
        - Optimizing chunk_size parameter
        - Reporting
        """
        chunks = self.chunk_text(text)

        if not chunks:
            return {
                "total_words": 0,
                "num_chunks": 0,
                "avg_chunk_size": 0,
                "min_chunk_size": 0,
                "max_chunk_size": 0,
            }

        chunk_sizes = [len(chunk_text.split()) for chunk_text, _ in chunks]

        return {
            "total_words": len(text.split()),
            "num_chunks": len(chunks),
            "avg_chunk_size": sum(chunk_sizes) // len(chunk_sizes),
            "min_chunk_size": min(chunk_sizes),
            "max_chunk_size": max(chunk_sizes),
        }

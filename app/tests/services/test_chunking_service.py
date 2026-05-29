"""Tests for the text chunking service."""

from app.services.chunking_service import ChunkingService


def _long_text(num_sentences: int = 60) -> str:
    return " ".join(f"Sentence number {i} about databases." for i in range(num_sentences))


def test_clean_text_normalizes_whitespace() -> None:
    service = ChunkingService()
    assert service.clean_text("a\n\t  b   c") == "a b c"


def test_clean_text_empty_returns_empty() -> None:
    assert ChunkingService().clean_text("") == ""


def test_chunk_text_returns_indexed_chunks() -> None:
    service = ChunkingService(chunk_size=20, overlap=5, min_chunk_size=5)
    chunks = service.chunk_text(_long_text())
    assert len(chunks) >= 2
    assert [order for _, order in chunks] == list(range(len(chunks)))


def test_chunk_text_short_input_single_chunk() -> None:
    service = ChunkingService(chunk_size=250, overlap=50, min_chunk_size=1)
    chunks = service.chunk_text("Short text about indexing.")
    assert len(chunks) == 1


def test_chunk_resource_attaches_resource_id() -> None:
    service = ChunkingService(chunk_size=20, overlap=5, min_chunk_size=5)
    result = service.chunk_resource(_long_text(), resource_id=42)
    assert all(item["resource_id"] == 42 for item in result)
    assert "chunk_text" in result[0]


def test_get_chunk_statistics_nonempty() -> None:
    service = ChunkingService(chunk_size=20, overlap=5, min_chunk_size=5)
    stats = service.get_chunk_statistics(_long_text())
    assert stats["num_chunks"] >= 1
    assert stats["total_words"] > 0
    assert stats["max_chunk_size"] >= stats["min_chunk_size"]


def test_get_chunk_statistics_empty() -> None:
    stats = ChunkingService().get_chunk_statistics("")
    assert stats["num_chunks"] == 0

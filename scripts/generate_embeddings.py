"""
Embedding Generation Script

Week 10: Embeddings, pgvector, Semantic Search

Generates embeddings for all resource chunks using Sentence Transformers.

This script:
1. Reads all resources from the database
2. Chunks each resource's content
3. Generates embeddings for each chunk
4. Stores embeddings in the chunk_embeddings table

Usage:
    python scripts/generate_embeddings.py [--batch-size 32] [--force]

Options:
    --batch-size: Number of chunks to process at once (default: 32)
    --force: Regenerate embeddings even if they already exist
    --resource-id: Process only a specific resource (optional)

Learning Objectives:
- Understand bulk embedding generation
- Learn batch processing for efficiency
- Practice database transactions for large operations
"""

import argparse
import os
import sys

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy.orm import Session
from tqdm import tqdm

from app.db.database import SessionLocal
from app.db.models import ChunkEmbedding, Resource, ResourceChunk
from app.services.chunking_service import ChunkingService
from app.services.embedding_service import EmbeddingService


def get_resources_to_process(db: Session, resource_id: int = None) -> list[Resource]:
    """
    Get resources that need embedding generation

    Args:
        db: Database session
        resource_id: Optional specific resource ID to process

    Returns:
        List of Resource objects
    """
    query = db.query(Resource)

    if resource_id:
        query = query.filter(Resource.resource_id == resource_id)

    resources = query.all()

    print(f"Found {len(resources)} resources to process")

    return resources


def chunk_resource(
    resource: Resource, chunking_service: ChunkingService, db: Session
) -> list[ResourceChunk]:
    """
    Chunk a resource and store chunks in database

    Args:
        resource: Resource to chunk
        chunking_service: ChunkingService instance
        db: Database session

    Returns:
        List of created ResourceChunk objects
    """
    # Check if resource has description/content to chunk
    if not resource.description or not resource.description.strip():
        print(f"  ⚠️  Resource {resource.resource_id} has no description, skipping")
        return []

    # Check if chunks already exist
    existing_chunks = (
        db.query(ResourceChunk).filter(ResourceChunk.resource_id == resource.resource_id).count()
    )

    if existing_chunks > 0:
        print(
            f"  ℹ️  Resource {resource.resource_id} already has {existing_chunks} chunks, skipping chunking"
        )
        chunks = (
            db.query(ResourceChunk).filter(ResourceChunk.resource_id == resource.resource_id).all()
        )
        return chunks

    # Chunk the resource
    chunk_data = chunking_service.chunk_resource(resource.description, resource.resource_id)

    if not chunk_data:
        print(f"  ⚠️  No chunks generated for resource {resource.resource_id}")
        return []

    # Create ResourceChunk objects
    chunks = []
    for chunk_dict in chunk_data:
        chunk_text = chunk_dict["chunk_text"]
        chunk = ResourceChunk(
            resource_id=chunk_dict["resource_id"],
            chunk_text=chunk_text,
            chunk_index=chunk_dict["chunk_order"],
            word_count=len(chunk_text.split()),
        )
        db.add(chunk)
        chunks.append(chunk)

    db.flush()  # Get chunk IDs without committing

    print(f"  ✅ Created {len(chunks)} chunks for resource {resource.resource_id}")

    return chunks


def generate_embeddings_for_chunks(
    chunks: list[ResourceChunk],
    embedding_service: EmbeddingService,
    db: Session,
    force: bool = False,
) -> int:
    """
    Generate embeddings for chunks

    Args:
        chunks: List of ResourceChunk objects
        embedding_service: EmbeddingService instance
        db: Database session
        force: If True, regenerate even if embeddings exist

    Returns:
        Number of embeddings generated
    """
    if not chunks:
        return 0

    # Filter chunks that need embeddings
    chunks_to_process = []

    for chunk in chunks:
        # Check if embedding already exists
        existing = (
            db.query(ChunkEmbedding).filter(ChunkEmbedding.chunk_id == chunk.chunk_id).first()
        )

        if existing and not force:
            continue

        chunks_to_process.append(chunk)

    if not chunks_to_process:
        return 0

    # Extract texts
    texts = [chunk.chunk_text for chunk in chunks_to_process]

    # Generate embeddings (batch processing)
    print(f"  🔄 Generating embeddings for {len(texts)} chunks...")
    embeddings = embedding_service.generate_embeddings_batch(texts)

    # Store embeddings
    count = 0
    for chunk, embedding in zip(chunks_to_process, embeddings, strict=False):
        # Check if embedding already exists (in case of force regeneration)
        existing = (
            db.query(ChunkEmbedding).filter(ChunkEmbedding.chunk_id == chunk.chunk_id).first()
        )

        if existing:
            # Update existing
            existing.embedding = embedding.tolist()
        else:
            # Create new
            chunk_embedding = ChunkEmbedding(chunk_id=chunk.chunk_id, embedding=embedding.tolist())
            db.add(chunk_embedding)

        count += 1

    db.flush()

    print(f"  ✅ Generated {count} embeddings")

    return count


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Generate embeddings for resource chunks")
    parser.add_argument(
        "--batch-size",
        type=int,
        default=32,
        help="Number of resources to process in one transaction (default: 32)",
    )
    parser.add_argument(
        "--force", action="store_true", help="Regenerate embeddings even if they already exist"
    )
    parser.add_argument("--resource-id", type=int, help="Process only a specific resource ID")

    args = parser.parse_args()

    print("=" * 60)
    print("CourseDB-AI Embedding Generation")
    print("=" * 60)
    print()

    # Initialize services
    print("🔧 Initializing services...")
    embedding_service = EmbeddingService()
    chunking_service = ChunkingService()

    # Create database session
    db = SessionLocal()

    try:
        # Get resources to process
        resources = get_resources_to_process(db, args.resource_id)

        if not resources:
            print("❌ No resources found to process")
            return

        print(f"\n📊 Processing {len(resources)} resources")
        print(f"⚙️  Batch size: {args.batch_size}")
        print(f"⚙️  Force regeneration: {args.force}")
        print()

        # Statistics
        total_chunks = 0
        total_embeddings = 0

        # Process resources in batches
        for i in range(0, len(resources), args.batch_size):
            batch = resources[i : i + args.batch_size]

            print(
                f"\n📦 Processing batch {i // args.batch_size + 1}/{(len(resources) + args.batch_size - 1) // args.batch_size}"
            )

            for resource in tqdm(batch, desc="Resources"):
                try:
                    # Chunk the resource
                    chunks = chunk_resource(resource, chunking_service, db)
                    total_chunks += len(chunks)

                    # Generate embeddings
                    embeddings_generated = generate_embeddings_for_chunks(
                        chunks, embedding_service, db, force=args.force
                    )
                    total_embeddings += embeddings_generated

                except Exception as e:
                    print(f"\n❌ Error processing resource {resource.resource_id}: {e}")
                    db.rollback()
                    continue

            # Commit batch
            db.commit()
            print("✅ Batch committed")

        print()
        print("=" * 60)
        print("✅ Embedding Generation Complete!")
        print("=" * 60)
        print(f"📊 Total chunks created/found: {total_chunks}")
        print(f"🎯 Total embeddings generated: {total_embeddings}")
        print()

        # Verify with database query
        total_chunks_db = db.query(ResourceChunk).count()
        total_embeddings_db = db.query(ChunkEmbedding).count()

        print("📈 Database Statistics:")
        print(f"   Total chunks in DB: {total_chunks_db}")
        print(f"   Total embeddings in DB: {total_embeddings_db}")
        print(
            f"   Coverage: {(total_embeddings_db / total_chunks_db * 100) if total_chunks_db > 0 else 0:.1f}%"
        )
        print()

    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        db.rollback()
        raise

    finally:
        db.close()
        print("✅ Database connection closed")


if __name__ == "__main__":
    main()

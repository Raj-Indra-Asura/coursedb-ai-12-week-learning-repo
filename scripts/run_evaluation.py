"""
Evaluation Script

Week 12: Evaluation, Polish, Portfolio

Evaluates CourseDB-AI system performance:
- Semantic search quality (precision, recall, relevance)
- Search comparison (semantic vs keyword vs hybrid)
- Query performance metrics (latency, throughput)
- System behavior under load
- Embedding quality assessment

Usage:
    python scripts/run_evaluation.py [--full] [--output report.json]

Options:
    --full: Run comprehensive evaluation (takes longer)
    --output: Save evaluation report to file (JSON format)
    --skip-performance: Skip performance benchmarks
    --skip-quality: Skip quality evaluation

Learning Objectives:
- Understand information retrieval metrics
- Learn A/B testing methodology
- Practice performance benchmarking
- Evaluate embedding quality
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from typing import Any

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.db.models import ChunkEmbedding, Question, Resource, ResourceChunk
from app.services.semantic_search_service import SemanticSearchService

# ==========================================
# Evaluation Test Queries
# ==========================================

# Test queries with expected relevant results
EVALUATION_QUERIES = [
    {
        "query": "SQL joins and query optimization",
        "expected_topics": ["SQL Basics", "Query Processing"],
        "expected_keywords": ["join", "query", "optimization"],
    },
    {
        "query": "database transactions and ACID properties",
        "expected_topics": ["Transactions"],
        "expected_keywords": ["transaction", "acid", "atomicity", "consistency"],
    },
    {
        "query": "B-tree indexing structures",
        "expected_topics": ["Indexing"],
        "expected_keywords": ["b-tree", "b+tree", "index"],
    },
    {
        "query": "machine learning classification algorithms",
        "expected_topics": ["Machine Learning Basics"],
        "expected_keywords": ["machine learning", "classification", "supervised"],
    },
    {
        "query": "neural networks backpropagation",
        "expected_topics": ["Neural Networks"],
        "expected_keywords": ["neural", "network", "backpropagation"],
    },
    {
        "query": "web authentication JWT tokens",
        "expected_topics": ["Authentication"],
        "expected_keywords": ["jwt", "token", "authentication"],
    },
    {
        "query": "normalization and functional dependencies",
        "expected_topics": ["Normalization"],
        "expected_keywords": ["normalization", "functional", "dependency", "3nf"],
    },
    {
        "query": "search algorithms BFS DFS",
        "expected_topics": ["Search Algorithms"],
        "expected_keywords": ["search", "bfs", "dfs", "algorithm"],
    },
]

PERFORMANCE_QUERIES = [
    "What is normalization?",
    "Explain ACID properties",
    "How do indexes work?",
    "What are neural networks?",
    "Describe transactions",
    "SQL join types",
    "Machine learning basics",
    "Web development authentication",
]


# ==========================================
# Evaluation Functions
# ==========================================


def calculate_precision_recall(
    results: list[dict], expected_topics: list[str], expected_keywords: list[str]
) -> dict[str, float]:
    """
    Calculate precision and recall for search results

    Learning Objectives (Week 12):
    - Understand information retrieval metrics
    - Learn precision = relevant_retrieved / total_retrieved
    - Learn recall = relevant_retrieved / total_relevant

    Args:
        results: Search results
        expected_topics: Expected relevant topics
        expected_keywords: Expected relevant keywords

    Returns:
        Dictionary with precision, recall, f1_score
    """
    if not results:
        return {"precision": 0.0, "recall": 0.0, "f1_score": 0.0}

    # Check relevance based on topics and keywords
    relevant_count = 0

    for result in results:
        # Check if result matches expected topics or keywords
        result_text = (
            result.get("chunk_text", "")
            + " "
            + result.get("resource_title", "")
            + " "
            + str(result.get("metadata", {}))
        ).lower()

        # Check if any expected topic or keyword is present
        is_relevant = False

        for topic in expected_topics:
            if topic.lower() in result_text:
                is_relevant = True
                break

        if not is_relevant:
            for keyword in expected_keywords:
                if keyword.lower() in result_text:
                    is_relevant = True
                    break

        if is_relevant:
            relevant_count += 1

    # Calculate metrics
    total_retrieved = len(results)
    total_relevant = len(expected_topics) + len(expected_keywords)

    precision = relevant_count / total_retrieved if total_retrieved > 0 else 0.0
    recall = relevant_count / total_relevant if total_relevant > 0 else 0.0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

    return {
        "precision": round(precision, 3),
        "recall": round(recall, 3),
        "f1_score": round(f1_score, 3),
        "relevant_count": relevant_count,
        "total_retrieved": total_retrieved,
    }


def evaluate_search_quality(db: Session) -> dict[str, Any]:
    """
    Evaluate semantic search quality

    Learning Objectives (Week 12):
    - Compare different search methods
    - Measure relevance and accuracy
    - Analyze result quality

    Args:
        db: Database session

    Returns:
        Dictionary with quality metrics
    """
    print("\n🔍 Evaluating Search Quality...")

    semantic_service = SemanticSearchService(db)

    results = {"semantic_search": [], "hybrid_search": [], "average_metrics": {}}

    for query_data in EVALUATION_QUERIES:
        query = query_data["query"]
        expected_topics = query_data["expected_topics"]
        expected_keywords = query_data["expected_keywords"]

        print(f"\n  Testing query: '{query}'")

        try:
            # Test semantic search
            semantic_results = semantic_service.search(query, top_k=5, similarity_threshold=0.3)
            semantic_metrics = calculate_precision_recall(
                semantic_results, expected_topics, expected_keywords
            )

            # Test hybrid search
            hybrid_results = semantic_service.hybrid_search(query, top_k=5, semantic_weight=0.7)
            hybrid_metrics = calculate_precision_recall(
                hybrid_results, expected_topics, expected_keywords
            )

            results["semantic_search"].append(
                {
                    "query": query,
                    "results_count": len(semantic_results),
                    "metrics": semantic_metrics,
                }
            )

            results["hybrid_search"].append(
                {"query": query, "results_count": len(hybrid_results), "metrics": hybrid_metrics}
            )

            print(
                f"    Semantic - Precision: {semantic_metrics['precision']:.3f}, Recall: {semantic_metrics['recall']:.3f}"
            )
            print(
                f"    Hybrid   - Precision: {hybrid_metrics['precision']:.3f}, Recall: {hybrid_metrics['recall']:.3f}"
            )

        except Exception as e:
            print(f"    ❌ Error: {e}")

    # Calculate average metrics
    if results["semantic_search"]:
        semantic_avg_precision = sum(
            r["metrics"]["precision"] for r in results["semantic_search"]
        ) / len(results["semantic_search"])
        semantic_avg_recall = sum(r["metrics"]["recall"] for r in results["semantic_search"]) / len(
            results["semantic_search"]
        )
        semantic_avg_f1 = sum(r["metrics"]["f1_score"] for r in results["semantic_search"]) / len(
            results["semantic_search"]
        )

        hybrid_avg_precision = sum(
            r["metrics"]["precision"] for r in results["hybrid_search"]
        ) / len(results["hybrid_search"])
        hybrid_avg_recall = sum(r["metrics"]["recall"] for r in results["hybrid_search"]) / len(
            results["hybrid_search"]
        )
        hybrid_avg_f1 = sum(r["metrics"]["f1_score"] for r in results["hybrid_search"]) / len(
            results["hybrid_search"]
        )

        results["average_metrics"] = {
            "semantic": {
                "precision": round(semantic_avg_precision, 3),
                "recall": round(semantic_avg_recall, 3),
                "f1_score": round(semantic_avg_f1, 3),
            },
            "hybrid": {
                "precision": round(hybrid_avg_precision, 3),
                "recall": round(hybrid_avg_recall, 3),
                "f1_score": round(hybrid_avg_f1, 3),
            },
        }

    print("\n  ✅ Search quality evaluation complete")

    return results


def evaluate_performance(db: Session) -> dict[str, Any]:
    """
    Evaluate search performance (latency, throughput)

    Learning Objectives (Week 12):
    - Measure query latency
    - Calculate throughput (queries per second)
    - Compare performance across methods

    Args:
        db: Database session

    Returns:
        Dictionary with performance metrics
    """
    print("\n⚡ Evaluating Search Performance...")

    semantic_service = SemanticSearchService(db)

    results = {
        "semantic_search": {
            "latencies": [],
            "avg_latency_ms": 0,
            "min_latency_ms": 0,
            "max_latency_ms": 0,
            "throughput_qps": 0,
        },
        "hybrid_search": {
            "latencies": [],
            "avg_latency_ms": 0,
            "min_latency_ms": 0,
            "max_latency_ms": 0,
            "throughput_qps": 0,
        },
    }

    # Test semantic search performance
    print("\n  Testing semantic search performance...")
    for query in PERFORMANCE_QUERIES:
        start_time = time.time()
        try:
            semantic_service.search(query, top_k=5)
        except Exception:
            pass
        latency_ms = (time.time() - start_time) * 1000
        results["semantic_search"]["latencies"].append(latency_ms)

    # Calculate semantic search metrics
    latencies = results["semantic_search"]["latencies"]
    if latencies:
        results["semantic_search"]["avg_latency_ms"] = round(sum(latencies) / len(latencies), 2)
        results["semantic_search"]["min_latency_ms"] = round(min(latencies), 2)
        results["semantic_search"]["max_latency_ms"] = round(max(latencies), 2)
        results["semantic_search"]["throughput_qps"] = round(
            len(latencies) / (sum(latencies) / 1000), 2
        )

    print(f"    Average latency: {results['semantic_search']['avg_latency_ms']} ms")
    print(f"    Throughput: {results['semantic_search']['throughput_qps']} queries/sec")

    # Test hybrid search performance
    print("\n  Testing hybrid search performance...")
    for query in PERFORMANCE_QUERIES:
        start_time = time.time()
        try:
            semantic_service.hybrid_search(query, top_k=5)
        except Exception:
            pass
        latency_ms = (time.time() - start_time) * 1000
        results["hybrid_search"]["latencies"].append(latency_ms)

    # Calculate hybrid search metrics
    latencies = results["hybrid_search"]["latencies"]
    if latencies:
        results["hybrid_search"]["avg_latency_ms"] = round(sum(latencies) / len(latencies), 2)
        results["hybrid_search"]["min_latency_ms"] = round(min(latencies), 2)
        results["hybrid_search"]["max_latency_ms"] = round(max(latencies), 2)
        results["hybrid_search"]["throughput_qps"] = round(
            len(latencies) / (sum(latencies) / 1000), 2
        )

    print(f"    Average latency: {results['hybrid_search']['avg_latency_ms']} ms")
    print(f"    Throughput: {results['hybrid_search']['throughput_qps']} queries/sec")

    print("\n  ✅ Performance evaluation complete")

    return results


def evaluate_embeddings(db: Session) -> dict[str, Any]:
    """
    Evaluate embedding quality

    Learning Objectives (Week 12):
    - Assess embedding coverage
    - Check vector dimensions
    - Verify embedding consistency

    Args:
        db: Database session

    Returns:
        Dictionary with embedding metrics
    """
    print("\n🎯 Evaluating Embeddings...")

    # Count resources, chunks, and embeddings
    resource_count = db.query(Resource).count()
    chunk_count = db.query(ResourceChunk).count()
    embedding_count = db.query(ChunkEmbedding).count()

    # Calculate coverage
    coverage = (embedding_count / chunk_count * 100) if chunk_count > 0 else 0

    # Check embedding dimensions
    sample_embedding = db.query(ChunkEmbedding).first()
    embedding_dim = (
        len(sample_embedding.embedding) if sample_embedding and sample_embedding.embedding else 0
    )

    results = {
        "resource_count": resource_count,
        "chunk_count": chunk_count,
        "embedding_count": embedding_count,
        "coverage_percent": round(coverage, 2),
        "embedding_dimension": embedding_dim,
        "model_name": sample_embedding.model_name if sample_embedding else "unknown",
    }

    print(f"    Resources: {resource_count}")
    print(f"    Chunks: {chunk_count}")
    print(f"    Embeddings: {embedding_count}")
    print(f"    Coverage: {coverage:.1f}%")
    print(f"    Dimension: {embedding_dim}")

    print("\n  ✅ Embedding evaluation complete")

    return results


def evaluate_database_health(db: Session) -> dict[str, Any]:
    """
    Evaluate database health and statistics

    Learning Objectives (Week 12):
    - Check data integrity
    - Verify relationships
    - Assess database size

    Args:
        db: Database session

    Returns:
        Dictionary with database health metrics
    """
    print("\n🏥 Evaluating Database Health...")

    from app.db.models import Course, Topic

    course_count = db.query(Course).count()
    topic_count = db.query(Topic).count()
    question_count = db.query(Question).count()
    resource_count = db.query(Resource).count()

    # Check for orphaned records
    orphaned_topics = (
        db.query(Topic).filter(~Topic.course_id.in_(db.query(Course.course_id))).count()
    )

    orphaned_questions = (
        db.query(Question).filter(~Question.course_id.in_(db.query(Course.course_id))).count()
    )

    results = {
        "tables": {
            "courses": course_count,
            "topics": topic_count,
            "questions": question_count,
            "resources": resource_count,
        },
        "data_integrity": {
            "orphaned_topics": orphaned_topics,
            "orphaned_questions": orphaned_questions,
            "healthy": orphaned_topics == 0 and orphaned_questions == 0,
        },
    }

    print(f"    Courses: {course_count}")
    print(f"    Topics: {topic_count}")
    print(f"    Questions: {question_count}")
    print(f"    Resources: {resource_count}")
    print(f"    Orphaned records: {orphaned_topics + orphaned_questions}")

    if results["data_integrity"]["healthy"]:
        print("    ✅ Database is healthy")
    else:
        print("    ⚠️  Database has integrity issues")

    print("\n  ✅ Database health evaluation complete")

    return results


def generate_report(evaluation_results: dict[str, Any], output_file: str = None):
    """
    Generate evaluation report

    Args:
        evaluation_results: Dictionary with all evaluation results
        output_file: Optional file path to save JSON report
    """
    print("\n" + "=" * 60)
    print("📊 Evaluation Report")
    print("=" * 60)

    # Print summary
    print("\n🎯 Quality Metrics:")
    if "quality" in evaluation_results:
        avg_metrics = evaluation_results["quality"].get("average_metrics", {})
        if "semantic" in avg_metrics:
            print("  Semantic Search:")
            print(f"    Precision: {avg_metrics['semantic']['precision']:.3f}")
            print(f"    Recall:    {avg_metrics['semantic']['recall']:.3f}")
            print(f"    F1 Score:  {avg_metrics['semantic']['f1_score']:.3f}")

        if "hybrid" in avg_metrics:
            print("\n  Hybrid Search:")
            print(f"    Precision: {avg_metrics['hybrid']['precision']:.3f}")
            print(f"    Recall:    {avg_metrics['hybrid']['recall']:.3f}")
            print(f"    F1 Score:  {avg_metrics['hybrid']['f1_score']:.3f}")

    print("\n⚡ Performance Metrics:")
    if "performance" in evaluation_results:
        perf = evaluation_results["performance"]
        if "semantic_search" in perf:
            print("  Semantic Search:")
            print(f"    Avg Latency: {perf['semantic_search']['avg_latency_ms']} ms")
            print(f"    Throughput:  {perf['semantic_search']['throughput_qps']} queries/sec")

        if "hybrid_search" in perf:
            print("\n  Hybrid Search:")
            print(f"    Avg Latency: {perf['hybrid_search']['avg_latency_ms']} ms")
            print(f"    Throughput:  {perf['hybrid_search']['throughput_qps']} queries/sec")

    print("\n🎯 Embedding Coverage:")
    if "embeddings" in evaluation_results:
        emb = evaluation_results["embeddings"]
        print(f"  Coverage: {emb['coverage_percent']}%")
        print(f"  Total Embeddings: {emb['embedding_count']}")
        print(f"  Dimension: {emb['embedding_dimension']}")

    print("\n🏥 Database Health:")
    if "database" in evaluation_results:
        db_health = evaluation_results["database"]
        print(f"  Total Records: {sum(db_health['tables'].values())}")
        print(
            f"  Integrity: {'✅ Healthy' if db_health['data_integrity']['healthy'] else '⚠️ Issues detected'}"
        )

    # Save to file if requested
    if output_file:
        evaluation_results["timestamp"] = datetime.now().isoformat()
        with open(output_file, "w") as f:
            json.dump(evaluation_results, f, indent=2)
        print(f"\n📄 Report saved to: {output_file}")

    print("\n" + "=" * 60)


def main():
    """Main evaluation function"""
    parser = argparse.ArgumentParser(description="Evaluate CourseDB-AI system")
    parser.add_argument(
        "--full", action="store_true", help="Run comprehensive evaluation (takes longer)"
    )
    parser.add_argument("--output", type=str, help="Save evaluation report to file (JSON format)")
    parser.add_argument(
        "--skip-performance", action="store_true", help="Skip performance benchmarks"
    )
    parser.add_argument("--skip-quality", action="store_true", help="Skip quality evaluation")

    args = parser.parse_args()

    print("=" * 60)
    print("CourseDB-AI Evaluation")
    print("=" * 60)
    print()

    # Create database session
    db = SessionLocal()

    evaluation_results = {}

    try:
        # Database health check (always run)
        evaluation_results["database"] = evaluate_database_health(db)

        # Embedding evaluation (always run)
        evaluation_results["embeddings"] = evaluate_embeddings(db)

        # Quality evaluation
        if not args.skip_quality:
            evaluation_results["quality"] = evaluate_search_quality(db)
        else:
            print("\n⏭️  Skipping quality evaluation")

        # Performance evaluation
        if not args.skip_performance:
            evaluation_results["performance"] = evaluate_performance(db)
        else:
            print("\n⏭️  Skipping performance evaluation")

        # Generate report
        generate_report(evaluation_results, args.output)

        print("\n✅ Evaluation completed successfully!")
        print()

    except Exception as e:
        print(f"\n❌ Fatal error during evaluation: {e}")
        import traceback

        traceback.print_exc()
        raise

    finally:
        db.close()
        print("✅ Database connection closed")


if __name__ == "__main__":
    main()

"""
Data Seeding Script

Week 5-6: PostgreSQL + FastAPI Foundation

Seeds the database with sample academic data:
- Courses (Database systems, AI, Web development)
- Topics (organized by week)
- Resources (notes, textbooks, papers)
- Questions (previous year exams with answers)
- Users (for testing)

Usage:
    python scripts/seed_data.py [--clear] [--minimal]

Options:
    --clear: Clear existing data before seeding
    --minimal: Load only minimal dataset (faster for testing)

Learning Objectives:
- Understand data relationships and foreign keys
- Practice batch insertions for performance
- Learn transaction management
- Understand data validation and integrity
"""

import argparse
import os
import sys
from typing import Any

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.db.models import Course, Question, Resource, Topic, User

# ==========================================
# Sample Data Definitions
# ==========================================

COURSES_DATA = [
    {
        "course_code": "CS201",
        "course_title": "Database Systems",
        "semester": "Spring 2024",
        "credit": 3,
    },
    {
        "course_code": "CS301",
        "course_title": "Artificial Intelligence",
        "semester": "Spring 2024",
        "credit": 3,
    },
    {
        "course_code": "CS202",
        "course_title": "Web Development",
        "semester": "Fall 2023",
        "credit": 3,
    },
]

TOPICS_DATA = {
    "CS201": [
        {
            "topic_name": "Database Introduction",
            "description": "Introduction to databases, DBMS concepts, and data models",
            "week_number": 1,
        },
        {
            "topic_name": "Relational Model",
            "description": "Relations, attributes, tuples, keys, integrity constraints",
            "week_number": 2,
        },
        {
            "topic_name": "SQL Basics",
            "description": "SELECT, WHERE, JOIN operations, basic queries",
            "week_number": 3,
        },
        {
            "topic_name": "Normalization",
            "description": "Functional dependencies, normal forms (1NF, 2NF, 3NF, BCNF)",
            "week_number": 4,
        },
        {
            "topic_name": "Indexing",
            "description": "B+ trees, hash indexes, query optimization",
            "week_number": 5,
        },
        {
            "topic_name": "Transactions",
            "description": "ACID properties, concurrency control, isolation levels",
            "week_number": 6,
        },
        {
            "topic_name": "Query Processing",
            "description": "Query optimization, execution plans, cost estimation",
            "week_number": 7,
        },
        {
            "topic_name": "NoSQL Databases",
            "description": "Document stores, key-value stores, CAP theorem",
            "week_number": 8,
        },
    ],
    "CS301": [
        {
            "topic_name": "AI Introduction",
            "description": "History of AI, intelligent agents, problem-solving",
            "week_number": 1,
        },
        {
            "topic_name": "Search Algorithms",
            "description": "BFS, DFS, A*, heuristic search",
            "week_number": 2,
        },
        {
            "topic_name": "Knowledge Representation",
            "description": "Logic, ontologies, semantic networks",
            "week_number": 3,
        },
        {
            "topic_name": "Machine Learning Basics",
            "description": "Supervised vs unsupervised learning, regression, classification",
            "week_number": 4,
        },
        {
            "topic_name": "Neural Networks",
            "description": "Perceptrons, backpropagation, deep learning",
            "week_number": 5,
        },
        {
            "topic_name": "Natural Language Processing",
            "description": "Text processing, embeddings, transformers",
            "week_number": 6,
        },
    ],
    "CS202": [
        {
            "topic_name": "HTML & CSS",
            "description": "Web page structure, styling, responsive design",
            "week_number": 1,
        },
        {
            "topic_name": "JavaScript Fundamentals",
            "description": "Variables, functions, DOM manipulation, events",
            "week_number": 2,
        },
        {
            "topic_name": "Backend Development",
            "description": "Node.js, Express, REST APIs",
            "week_number": 3,
        },
        {
            "topic_name": "Databases for Web",
            "description": "SQL vs NoSQL, ORM, database integration",
            "week_number": 4,
        },
        {
            "topic_name": "Authentication",
            "description": "Sessions, JWT, OAuth, password hashing",
            "week_number": 5,
        },
    ],
}

QUESTIONS_DATA = [
    # CS201 - Database Systems Questions
    {
        "course_code": "CS201",
        "topic_name": "SQL Basics",
        "question_text": "Write an SQL query to retrieve all students who have scored more than 80 marks in any subject.",
        "year": 2023,
        "exam_type": "midterm",
        "difficulty": "easy",
        "marks": 5,
        "answer_text": "SELECT DISTINCT s.student_id, s.student_name FROM students s JOIN enrollments e ON s.student_id = e.student_id WHERE e.marks > 80;",
        "answer_reference": "Lecture 3, SQL SELECT & JOIN",
    },
    {
        "course_code": "CS201",
        "topic_name": "Normalization",
        "question_text": "Explain the concept of functional dependency with an example. Define 3NF and check if the given relation R(A, B, C, D) with FDs {A→B, B→C, C→D} is in 3NF.",
        "year": 2023,
        "exam_type": "midterm",
        "difficulty": "medium",
        "marks": 10,
        "answer_text": "A functional dependency X→Y means X uniquely determines Y. 3NF requires no transitive dependencies. The given relation is NOT in 3NF because there's a transitive dependency A→D through B and C.",
        "answer_reference": "Lecture 4, Normalization Theory",
    },
    {
        "course_code": "CS201",
        "topic_name": "Indexing",
        "question_text": "Compare B-tree and hash index structures. When would you use each? Explain with examples.",
        "year": 2023,
        "exam_type": "final",
        "difficulty": "medium",
        "marks": 8,
        "answer_text": "B-tree supports range queries and maintains sorted order, ideal for range scans. Hash index provides O(1) lookup for equality searches but doesn't support range queries. Use B-tree for ordered data access, hash for exact-match lookups.",
        "answer_reference": "Lecture 5, Index Structures",
    },
    {
        "course_code": "CS201",
        "topic_name": "Transactions",
        "question_text": "What are the ACID properties? Explain each with a real-world banking transaction example.",
        "year": 2022,
        "exam_type": "final",
        "difficulty": "easy",
        "marks": 8,
        "answer_text": "ACID: Atomicity (all or nothing - money transfer completes fully or not at all), Consistency (account balances remain valid), Isolation (concurrent transfers don't interfere), Durability (committed transfers persist even after system crash).",
        "answer_reference": "Lecture 6, Transaction Management",
    },
    {
        "course_code": "CS201",
        "topic_name": "Transactions",
        "question_text": "Explain the difference between deadlock and starvation. How does a DBMS detect deadlocks?",
        "year": 2023,
        "exam_type": "final",
        "difficulty": "hard",
        "marks": 10,
        "answer_text": "Deadlock: circular wait where transactions block each other. Starvation: transaction repeatedly postponed. DBMS detects deadlocks using wait-for graphs - cycle detection indicates deadlock. One transaction is then rolled back.",
        "answer_reference": "Lecture 6, Concurrency Control",
    },
    # CS301 - AI Questions
    {
        "course_code": "CS301",
        "topic_name": "Search Algorithms",
        "question_text": "Compare BFS and DFS search algorithms. When would you prefer one over the other?",
        "year": 2023,
        "exam_type": "midterm",
        "difficulty": "easy",
        "marks": 6,
        "answer_text": "BFS explores level by level (queue), guarantees shortest path, higher memory. DFS explores depth-first (stack), lower memory, may not find shortest path. Use BFS for shortest path, DFS for memory-constrained search.",
        "answer_reference": "Lecture 2, Search Algorithms",
    },
    {
        "course_code": "CS301",
        "topic_name": "Machine Learning Basics",
        "question_text": "Explain the difference between supervised and unsupervised learning with examples.",
        "year": 2023,
        "exam_type": "midterm",
        "difficulty": "easy",
        "marks": 5,
        "answer_text": "Supervised learning uses labeled data (input-output pairs) for training, e.g., spam classification. Unsupervised learning finds patterns in unlabeled data, e.g., customer segmentation using clustering.",
        "answer_reference": "Lecture 4, ML Fundamentals",
    },
    {
        "course_code": "CS301",
        "topic_name": "Neural Networks",
        "question_text": "Describe the backpropagation algorithm. Why is it important for training neural networks?",
        "year": 2023,
        "exam_type": "final",
        "difficulty": "hard",
        "marks": 12,
        "answer_text": "Backpropagation computes gradients of loss function w.r.t. network weights by propagating errors backward through layers using chain rule. Essential for updating weights via gradient descent to minimize loss.",
        "answer_reference": "Lecture 5, Neural Network Training",
    },
    # CS202 - Web Development Questions
    {
        "course_code": "CS202",
        "topic_name": "JavaScript Fundamentals",
        "question_text": "What is event bubbling in JavaScript? Explain with an example.",
        "year": 2023,
        "exam_type": "midterm",
        "difficulty": "medium",
        "marks": 6,
        "answer_text": "Event bubbling is when an event triggered on a child element propagates up to parent elements. Example: clicking a button inside a div triggers both button and div click handlers. Can be stopped with stopPropagation().",
        "answer_reference": "Lecture 2, DOM Events",
    },
    {
        "course_code": "CS202",
        "topic_name": "Authentication",
        "question_text": "Compare session-based and token-based (JWT) authentication. What are the pros and cons of each?",
        "year": 2023,
        "exam_type": "final",
        "difficulty": "hard",
        "marks": 10,
        "answer_text": "Session-based: server stores state, easier to revoke, requires session storage. JWT: stateless, scalable, harder to revoke, contains claims. Use sessions for traditional apps, JWT for stateless APIs and microservices.",
        "answer_reference": "Lecture 5, Authentication Methods",
    },
]

RESOURCES_DATA = [
    # CS201 Resources
    {
        "course_code": "CS201",
        "topic_name": "Database Introduction",
        "title": "Introduction to Database Systems",
        "resource_type": "note",
        "url": "https://example.com/db-intro.pdf",
        "description": "Comprehensive introduction to database management systems. Covers data models, database architecture, and the role of DBMS in modern applications. Includes examples of hierarchical, network, and relational models.",
        "author": "Prof. John Smith",
        "year_published": 2023,
    },
    {
        "course_code": "CS201",
        "topic_name": "SQL Basics",
        "title": "SQL Tutorial for Beginners",
        "resource_type": "note",
        "url": "https://example.com/sql-basics.pdf",
        "description": "Step-by-step tutorial covering SQL fundamentals including SELECT, INSERT, UPDATE, DELETE operations. Explains JOINs with visual diagrams, aggregate functions, and subqueries with practical examples.",
        "author": "Prof. John Smith",
        "year_published": 2023,
    },
    {
        "course_code": "CS201",
        "topic_name": "Indexing",
        "title": "Database Indexing Techniques",
        "resource_type": "paper",
        "url": "https://example.com/indexing-paper.pdf",
        "description": "Research paper analyzing various indexing structures including B+ trees, hash indexes, and bitmap indexes. Compares performance characteristics for different query patterns and discusses index selection strategies.",
        "author": "Dr. Alice Johnson",
        "year_published": 2022,
    },
    {
        "course_code": "CS201",
        "topic_name": "Transactions",
        "title": "Transaction Processing Concepts",
        "resource_type": "textbook",
        "url": "https://example.com/transactions-textbook.pdf",
        "description": "Detailed coverage of transaction management including ACID properties, concurrency control mechanisms (2PL, timestamp ordering), deadlock detection and prevention, and recovery techniques.",
        "author": "Dr. Michael Brown",
        "year_published": 2021,
    },
    # CS301 Resources
    {
        "course_code": "CS301",
        "topic_name": "Machine Learning Basics",
        "title": "Introduction to Machine Learning",
        "resource_type": "note",
        "url": "https://example.com/ml-intro.pdf",
        "description": "Foundation concepts in machine learning covering supervised, unsupervised, and reinforcement learning. Explains regression, classification, clustering with mathematical foundations and Python examples.",
        "author": "Prof. Sarah Lee",
        "year_published": 2023,
    },
    {
        "course_code": "CS301",
        "topic_name": "Neural Networks",
        "title": "Deep Learning Fundamentals",
        "resource_type": "textbook",
        "url": "https://example.com/deep-learning.pdf",
        "description": "Comprehensive guide to neural networks and deep learning. Covers perceptrons, multi-layer networks, backpropagation algorithm, convolutional networks, and recurrent networks with implementation details.",
        "author": "Prof. David Chen",
        "year_published": 2022,
    },
    # CS202 Resources
    {
        "course_code": "CS202",
        "topic_name": "Backend Development",
        "title": "Node.js and Express Guide",
        "resource_type": "note",
        "url": "https://example.com/nodejs-guide.pdf",
        "description": "Practical guide to building web applications with Node.js and Express framework. Covers routing, middleware, error handling, and RESTful API design patterns with code examples.",
        "author": "Prof. Emily Davis",
        "year_published": 2023,
    },
]

USERS_DATA = [
    {"username": "student1", "email": "student1@example.com", "full_name": "Alice Johnson"},
    {"username": "student2", "email": "student2@example.com", "full_name": "Bob Smith"},
    {"username": "student3", "email": "student3@example.com", "full_name": "Charlie Brown"},
    {"username": "professor", "email": "prof@example.com", "full_name": "Dr. Jane Wilson"},
]


# ==========================================
# Seeding Functions
# ==========================================


def clear_all_data(db: Session):
    """
    Clear all existing data from database

    Learning Objectives:
    - Understand cascade deletion through relationships
    - Learn transaction management
    - Practice error handling

    Args:
        db: Database session
    """
    print("\n🗑️  Clearing existing data...")

    try:
        # Delete in reverse dependency order
        db.query(Question).delete()
        db.query(Resource).delete()
        db.query(Topic).delete()
        db.query(Course).delete()
        db.query(User).delete()

        db.commit()
        print("  ✅ All existing data cleared")

    except Exception as e:
        print(f"  ❌ Error clearing data: {e}")
        db.rollback()
        raise


def seed_courses(db: Session, course_data: list[dict[str, Any]]) -> dict[str, Course]:
    """
    Seed courses into database

    Args:
        db: Database session
        course_data: List of course dictionaries

    Returns:
        Dictionary mapping course_code to Course objects
    """
    print("\n📚 Seeding courses...")

    courses = {}

    for data in course_data:
        # Check if course already exists
        existing = db.query(Course).filter_by(course_code=data["course_code"]).first()

        if existing:
            print(f"  ℹ️  Course {data['course_code']} already exists, skipping")
            courses[data["course_code"]] = existing
            continue

        course = Course(**data)
        db.add(course)
        courses[data["course_code"]] = course

        print(f"  ✅ Added course: {data['course_code']} - {data['course_title']}")

    db.flush()  # Get IDs without committing

    return courses


def seed_topics(
    db: Session, topics_data: dict[str, list[dict]], courses: dict[str, Course]
) -> dict[str, list[Topic]]:
    """
    Seed topics into database

    Args:
        db: Database session
        topics_data: Dictionary mapping course_code to list of topic dictionaries
        courses: Dictionary of course objects

    Returns:
        Dictionary mapping course_code to list of Topic objects
    """
    print("\n📖 Seeding topics...")

    all_topics = {}

    for course_code, topic_list in topics_data.items():
        if course_code not in courses:
            print(f"  ⚠️  Course {course_code} not found, skipping topics")
            continue

        course = courses[course_code]
        topics = []

        for data in topic_list:
            topic = Topic(course_id=course.course_id, **data)
            db.add(topic)
            topics.append(topic)

            print(f"  ✅ Added topic: {course_code} - {data['topic_name']}")

        all_topics[course_code] = topics

    db.flush()

    return all_topics


def seed_questions(
    db: Session,
    questions_data: list[dict],
    courses: dict[str, Course],
    topics_by_course: dict[str, list[Topic]],
):
    """
    Seed questions into database

    Args:
        db: Database session
        questions_data: List of question dictionaries
        courses: Dictionary of course objects
        topics_by_course: Dictionary mapping course_code to topics
    """
    print("\n❓ Seeding questions...")

    for data in questions_data:
        course_code = data.pop("course_code")
        topic_name = data.pop("topic_name")

        if course_code not in courses:
            print(f"  ⚠️  Course {course_code} not found, skipping question")
            continue

        course = courses[course_code]

        # Find topic by name
        topic = None
        if course_code in topics_by_course:
            for t in topics_by_course[course_code]:
                if t.topic_name == topic_name:
                    topic = t
                    break

        question = Question(
            course_id=course.course_id,
            topic_id=topic.topic_id if topic else None,
            course_code=course_code,  # Intentional denormalization for Week 4 lesson
            topic_name=topic_name,  # Intentional denormalization for Week 4 lesson
            **data,
        )
        db.add(question)

        print(f"  ✅ Added question: {course_code} - {data['question_text'][:50]}...")

    db.flush()


def seed_resources(
    db: Session,
    resources_data: list[dict],
    courses: dict[str, Course],
    topics_by_course: dict[str, list[Topic]],
):
    """
    Seed resources into database

    Args:
        db: Database session
        resources_data: List of resource dictionaries
        courses: Dictionary of course objects
        topics_by_course: Dictionary mapping course_code to topics
    """
    print("\n📄 Seeding resources...")

    for data in resources_data:
        course_code = data.pop("course_code")
        topic_name = data.pop("topic_name")

        if course_code not in courses:
            print(f"  ⚠️  Course {course_code} not found, skipping resource")
            continue

        course = courses[course_code]

        # Find topic by name
        topic = None
        if course_code in topics_by_course:
            for t in topics_by_course[course_code]:
                if t.topic_name == topic_name:
                    topic = t
                    break

        resource = Resource(
            course_id=course.course_id, topic_id=topic.topic_id if topic else None, **data
        )
        db.add(resource)

        print(f"  ✅ Added resource: {data['title']}")

    db.flush()


def seed_users(db: Session, users_data: list[dict]):
    """
    Seed users into database

    Args:
        db: Database session
        users_data: List of user dictionaries
    """
    print("\n👤 Seeding users...")

    for data in users_data:
        # Check if user already exists
        existing = db.query(User).filter_by(username=data["username"]).first()

        if existing:
            print(f"  ℹ️  User {data['username']} already exists, skipping")
            continue

        user = User(**data)
        db.add(user)

        print(f"  ✅ Added user: {data['username']} - {data['full_name']}")

    db.flush()


def print_statistics(db: Session):
    """
    Print database statistics after seeding

    Args:
        db: Database session
    """
    print("\n" + "=" * 60)
    print("📊 Database Statistics")
    print("=" * 60)

    course_count = db.query(Course).count()
    topic_count = db.query(Topic).count()
    question_count = db.query(Question).count()
    resource_count = db.query(Resource).count()
    user_count = db.query(User).count()

    print(f"  Courses:   {course_count}")
    print(f"  Topics:    {topic_count}")
    print(f"  Questions: {question_count}")
    print(f"  Resources: {resource_count}")
    print(f"  Users:     {user_count}")
    print()


def main():
    """Main seeding function"""
    parser = argparse.ArgumentParser(description="Seed CourseDB-AI database with sample data")
    parser.add_argument("--clear", action="store_true", help="Clear existing data before seeding")
    parser.add_argument(
        "--minimal", action="store_true", help="Load only minimal dataset (faster for testing)"
    )

    args = parser.parse_args()

    print("=" * 60)
    print("CourseDB-AI Data Seeding")
    print("=" * 60)
    print()

    # Create database session
    db = SessionLocal()

    try:
        # Clear existing data if requested
        if args.clear:
            clear_all_data(db)

        # Prepare data (minimal or full)
        courses_data = COURSES_DATA[:1] if args.minimal else COURSES_DATA

        # Seed data
        print("🌱 Starting data seeding...")

        courses = seed_courses(db, courses_data)
        topics = seed_topics(db, TOPICS_DATA, courses)
        seed_questions(db, QUESTIONS_DATA, courses, topics)
        seed_resources(db, RESOURCES_DATA, courses, topics)
        seed_users(db, USERS_DATA)

        # Commit all changes
        db.commit()

        print("\n✅ Data seeding completed successfully!")

        # Print statistics
        print_statistics(db)

        print("📝 Next Steps:")
        print("   1. Run: python scripts/generate_embeddings.py")
        print("   2. Start API: uvicorn app.backend.main:app --reload")
        print("   3. Test semantic search: http://localhost:8000/search/semantic?q=SQL")
        print()

    except Exception as e:
        print(f"\n❌ Fatal error during seeding: {e}")
        db.rollback()
        import traceback

        traceback.print_exc()
        raise

    finally:
        db.close()
        print("✅ Database connection closed")


if __name__ == "__main__":
    main()

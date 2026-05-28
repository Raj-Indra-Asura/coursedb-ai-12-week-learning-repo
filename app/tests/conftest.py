"""
Pytest Configuration and Fixtures

Week 5: PostgreSQL + FastAPI Foundation

This file contains shared pytest fixtures and configuration.

Learning Objectives:
- Understand pytest fixtures
- Set up test database
- Create test client
- Manage test data lifecycle
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# TODO (Week 5): Import app and database dependencies
# from app.backend.main import app
# from app.db.database import Base, get_db
# from app.db.models import *


# TODO (Week 5): Create test database fixture
# @pytest.fixture(scope="function")
# def test_db():
#     """
#     Create a fresh test database for each test
#
#     Uses in-memory SQLite for fast tests
#     Alternative: Use PostgreSQL test database
#     """
#     # Create in-memory database
#     engine = create_engine(
#         "sqlite:///:memory:",
#         connect_args={"check_same_thread": False},
#         poolclass=StaticPool,
#     )
#
#     # Create tables
#     Base.metadata.create_all(bind=engine)
#
#     # Create session
#     TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#     db = TestingSessionLocal()
#
#     try:
#         yield db
#     finally:
#         db.close()
#         Base.metadata.drop_all(bind=engine)


# TODO (Week 5): Create test client fixture
# @pytest.fixture(scope="function")
# def client(test_db):
#     """
#     Create FastAPI test client
#
#     Overrides get_db dependency to use test database
#     """
#     def override_get_db():
#         try:
#             yield test_db
#         finally:
#             test_db.close()
#
#     app.dependency_overrides[get_db] = override_get_db
#
#     with TestClient(app) as test_client:
#         yield test_client
#
#     app.dependency_overrides.clear()


# TODO (Week 6): Add sample data fixtures
# @pytest.fixture
# def sample_course(test_db):
#     """Create a sample course for testing"""
#     pass
#
# @pytest.fixture
# def sample_questions(test_db):
#     """Create sample questions for testing"""
#     pass

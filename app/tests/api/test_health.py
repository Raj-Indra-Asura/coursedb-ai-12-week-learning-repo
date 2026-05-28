"""
Health Endpoint Tests

Week 5: PostgreSQL + FastAPI Foundation

Test the health check endpoint.
"""

import pytest

# TODO (Week 5): Implement health tests

# def test_health_check_returns_200(client):
#     """Test health endpoint returns 200 OK"""
#     response = client.get("/health/")
#     assert response.status_code == 200


# def test_health_check_returns_json(client):
#     """Test health endpoint returns JSON"""
#     response = client.get("/health/")
#     assert response.headers["content-type"] == "application/json"
#     data = response.json()
#     assert "status" in data


# def test_database_health_check(client):
#     """Test database health endpoint"""
#     response = client.get("/health/db")
#     assert response.status_code == 200
#     data = response.json()
#     assert data["database"] == "connected"

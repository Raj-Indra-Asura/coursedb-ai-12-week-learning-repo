"""Tests for the resources CRUD API."""

from fastapi.testclient import TestClient


def _make_course(client: TestClient) -> int:
    return client.post(
        "/api/courses/",
        json={"course_code": "CSE2203", "course_title": "DBMS", "credit": 3},
    ).json()["course_id"]


def _resource_payload(course_id: int, **overrides) -> dict:
    payload = {
        "course_id": course_id,
        "title": "DBMS Lecture Notes",
        "resource_type": "note",
        "description": "Week 1 notes",
    }
    payload.update(overrides)
    return payload


def test_create_resource(client: TestClient) -> None:
    course_id = _make_course(client)
    response = client.post("/api/resources/", json=_resource_payload(course_id))
    assert response.status_code == 201
    assert response.json()["title"] == "DBMS Lecture Notes"


def test_list_resources(client: TestClient) -> None:
    course_id = _make_course(client)
    client.post("/api/resources/", json=_resource_payload(course_id))
    response = client.get("/api/resources/")
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_get_resource_by_id(client: TestClient) -> None:
    course_id = _make_course(client)
    created = client.post("/api/resources/", json=_resource_payload(course_id)).json()
    response = client.get(f"/api/resources/{created['resource_id']}")
    assert response.status_code == 200


def test_get_missing_resource_returns_404(client: TestClient) -> None:
    assert client.get("/api/resources/99999").status_code == 404


def test_invalid_resource_type_rejected(client: TestClient) -> None:
    course_id = _make_course(client)
    response = client.post(
        "/api/resources/", json=_resource_payload(course_id, resource_type="bogus")
    )
    assert response.status_code == 422


def test_delete_resource(client: TestClient) -> None:
    course_id = _make_course(client)
    created = client.post("/api/resources/", json=_resource_payload(course_id)).json()
    assert client.delete(f"/api/resources/{created['resource_id']}").status_code == 204
    assert client.get(f"/api/resources/{created['resource_id']}").status_code == 404


def test_resource_chunks_endpoint(client: TestClient) -> None:
    course_id = _make_course(client)
    created = client.post("/api/resources/", json=_resource_payload(course_id)).json()
    response = client.get(f"/api/resources/{created['resource_id']}/chunks")
    assert response.status_code == 200


def test_list_resources_filters(client: TestClient) -> None:
    course_id = _make_course(client)
    client.post(
        "/api/resources/",
        json=_resource_payload(
            course_id,
            title="Final Paper 2023",
            resource_type="paper",
            year_published=2023,
            author="Dr. Smith",
        ),
    )
    client.post(
        "/api/resources/",
        json=_resource_payload(
            course_id,
            title="Lecture Slides",
            resource_type="slide",
            year_published=2022,
        ),
    )

    assert len(client.get(f"/api/resources/?course_id={course_id}").json()) == 2
    assert len(client.get("/api/resources/?resource_type=paper").json()) == 1
    assert len(client.get("/api/resources/?academic_year=2023").json()) == 1
    assert len(client.get("/api/resources/?search=Final").json()) == 1
    # search also matches the author field (regression test for source_name bug)
    assert len(client.get("/api/resources/?search=Smith").json()) == 1


def test_create_resource_invalid_course_returns_400(client: TestClient) -> None:
    response = client.post("/api/resources/", json=_resource_payload(99999))
    assert response.status_code == 400


def test_update_resource_success(client: TestClient) -> None:
    course_id = _make_course(client)
    created = client.post("/api/resources/", json=_resource_payload(course_id)).json()
    response = client.put(
        f"/api/resources/{created['resource_id']}",
        json={"title": "Updated Notes", "year_published": 2024},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "Updated Notes"
    assert body["year_published"] == 2024


def test_update_missing_resource_returns_404(client: TestClient) -> None:
    assert client.put("/api/resources/99999", json={"title": "x"}).status_code == 404


def test_delete_missing_resource_returns_404(client: TestClient) -> None:
    assert client.delete("/api/resources/99999").status_code == 404


def test_resource_chunks_missing_resource_returns_404(client: TestClient) -> None:
    assert client.get("/api/resources/99999/chunks").status_code == 404


def test_resources_stats_by_type(client: TestClient) -> None:
    course_id = _make_course(client)
    client.post("/api/resources/", json=_resource_payload(course_id, resource_type="paper"))
    client.post("/api/resources/", json=_resource_payload(course_id, resource_type="note"))
    stats = client.get("/api/resources/stats/by-type").json()
    by_type = {row["resource_type"]: row["count"] for row in stats}
    assert by_type["paper"] == 1
    assert by_type["note"] == 1


def test_resources_stats_by_year(client: TestClient) -> None:
    course_id = _make_course(client)
    client.post("/api/resources/", json=_resource_payload(course_id, year_published=2023))
    client.post("/api/resources/", json=_resource_payload(course_id, year_published=2023))
    client.post("/api/resources/", json=_resource_payload(course_id, year_published=2022))
    stats = client.get("/api/resources/stats/by-year").json()
    by_year = {row["academic_year"]: row["count"] for row in stats}
    assert by_year[2023] == 2
    assert by_year[2022] == 1

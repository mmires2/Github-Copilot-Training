import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_root_redirect():
    """Test that root endpoint redirects to static/index.html"""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities():
    """Test that all activities are returned"""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0
    assert "Chess Club" in data


def test_signup_for_activity_success():
    """Test successful signup for an activity"""
    response = client.post(
        "/activities/Tennis%20Club/signup?email=newstudent@mergington.edu"
    )
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]


def test_signup_duplicate_fails():
    """Test that duplicate signup is rejected"""
    email = "michael@mergington.edu"
    response = client.post(
        f"/activities/Chess%20Club/signup?email={email}"
    )
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_nonexistent_activity():
    """Test signup fails for non-existent activity"""
    response = client.post(
        "/activities/Nonexistent%20Club/signup?email=test@mergington.edu"
    )
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_delete_participant_success():
    """Test successful removal of a participant"""
    email = "test-delete@mergington.edu"
    # First, add a participant
    client.post(f"/activities/Art%20Club/signup?email={email}")
    # Then delete them
    response = client.delete(f"/activities/Art%20Club/participants/{email}")
    assert response.status_code == 200
    assert "Unregistered" in response.json()["message"]


def test_delete_nonexistent_participant():
    """Test deletion fails for non-existent participant"""
    response = client.delete(
        "/activities/Science%20Club/participants/nonexistent@mergington.edu"
    )
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]

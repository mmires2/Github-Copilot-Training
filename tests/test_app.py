import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


class TestRootEndpoint:
    """Tests for the root endpoint"""

    def test_root_redirect(self):
        """Test that root endpoint redirects to static/index.html"""
        # Arrange
        expected_status = 307
        expected_location = "/static/index.html"

        # Act
        response = client.get("/", follow_redirects=False)

        # Assert
        assert response.status_code == expected_status
        assert response.headers["location"] == expected_location


class TestActivitiesEndpoint:
    """Tests for the activities endpoint"""

    def test_get_activities_returns_all_activities(self):
        """Test that all activities are returned"""
        # Arrange
        expected_activity = "Chess Club"

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        assert response.status_code == 200
        assert isinstance(data, dict)
        assert len(data) > 0
        assert expected_activity in data


class TestSignupEndpoint:
    """Tests for the signup endpoint"""

    def test_signup_for_activity_success(self):
        """Test successful signup for an activity"""
        # Arrange
        activity_name = "Tennis%20Club"
        email = "newstudent@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )

        # Assert
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]

    def test_signup_duplicate_fails(self):
        """Test that duplicate signup is rejected"""
        # Arrange
        activity_name = "Chess%20Club"
        email = "michael@mergington.edu"
        expected_status = 400
        expected_detail = "already signed up"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )

        # Assert
        assert response.status_code == expected_status
        assert expected_detail in response.json()["detail"]

    def test_signup_nonexistent_activity(self):
        """Test signup fails for non-existent activity"""
        # Arrange
        activity_name = "Nonexistent%20Club"
        email = "test@mergington.edu"
        expected_status = 404
        expected_detail = "Activity not found"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )

        # Assert
        assert response.status_code == expected_status
        assert expected_detail in response.json()["detail"]


class TestDeleteParticipantEndpoint:
    """Tests for the delete participant endpoint"""

    def test_delete_participant_success(self):
        """Test successful removal of a participant"""
        # Arrange
        activity_name = "Art%20Club"
        email = "test-delete@mergington.edu"

        # First, sign up the participant
        client.post(f"/activities/{activity_name}/signup?email={email}")

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )

        # Assert
        assert response.status_code == 200
        assert "Unregistered" in response.json()["message"]

    def test_delete_nonexistent_participant(self):
        """Test deletion fails for non-existent participant"""
        # Arrange
        activity_name = "Science%20Club"
        email = "nonexistent@mergington.edu"
        expected_status = 404
        expected_detail = "Participant not found"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )

        # Assert
        assert response.status_code == expected_status
        assert expected_detail in response.json()["detail"]

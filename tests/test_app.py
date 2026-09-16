from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_delete_participant_unregisters_student():
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    response = client.delete(f"/activities/{activity_name}/participants?email={email}")

    assert response.status_code == 200
    payload = response.json()
    assert payload["message"] == f"Removed {email} from {activity_name}"

    activities = client.get("/activities").json()
    assert email not in activities[activity_name]["participants"]


def test_delete_participant_returns_error_for_missing_student():
    response = client.delete("/activities/Chess Club/participants?email=missing@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"

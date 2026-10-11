import pytest
from fastapi.testclient import TestClient
from src.api import webhooks
from src.api.main import app

client = TestClient(app)


def test_health_check():
    """Verify the API is breathing before demoing."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "operational", "system": "OrionSync"}


def test_twilio_webhook_ingestion(monkeypatch: pytest.MonkeyPatch):
    """Verify that Twilio webhooks are accepted instantly with correct XML."""
    # Stub the background workflow so CI never calls the real Twilio API
    monkeypatch.setattr(webhooks, "orchestrate_workflow", lambda **kwargs: None)

    payload = {
        "From": "whatsapp:+1234567890",
        "Body": "Send a heavy duty tow to the A104",
        "NumMedia": "0",
    }

    # Twilio sends data as form-urlencoded, not JSON
    response = client.post(
        "/api/v1/webhooks/twilio",
        data=payload,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 202
    assert response.headers["content-type"] == "application/xml"
    assert "<Response></Response>" in response.text


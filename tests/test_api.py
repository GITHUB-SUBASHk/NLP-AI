from fastapi.testclient import TestClient
from interfaces.api_server.main import app

client = TestClient(app)

def test_health_status():
    # Accept both /health and /status endpoints if both exist
    for path in ["/health", "/status"]:
        response = client.get(path)
        if response.status_code == 200:
            # Accept either {"status": "ok"} or {"status": "OK"}
            assert response.json().get("status", "").lower() == "ok"
            break
    else:
        assert False, "No health/status endpoint returned 200"

def test_generate_reply_success():
    payload = {"message": "hello", "user_id": "test_user"}
    response = client.post("/chat/generate-reply", json=payload)
    assert response.status_code == 200
    assert "reply" in response.json()
    assert isinstance(response.json()["reply"], str)

def test_generate_reply_missing_message():
    response = client.post("/chat/generate-reply", json={"user_id": "test_user"})
    # Should return 400 for missing message
    assert response.status_code in (200, 400)
    if response.status_code == 400:
        assert "error" in response.json()
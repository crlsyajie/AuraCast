import json
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_weather():
    response = client.get("/v1/weather")
    assert response.status_code == 200
    data = response.json()
    assert "current" in data
    assert "forecast" in data
    assert "list" in data["forecast"]
    assert len(data["forecast"]["list"]) == 8  # Enforce 24 hour window constraint test on mock fallback

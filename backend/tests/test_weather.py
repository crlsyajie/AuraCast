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
    assert "derived" in data

    # Asserting derived contains required fields for action plan
    derived = data["derived"]
    assert "temp" in derived
    assert "pop" in derived
    assert "wind" in derived
    assert "uvi" in derived
    assert "humidity" in derived

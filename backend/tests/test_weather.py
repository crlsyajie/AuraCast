import json
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_weather():
    response = client.get("/v1/weather?lat=13.7565&lon=121.0583")
    assert response.status_code == 200
    data = response.json()
    assert "current" in data
    assert "forecast" in data
    assert "derived" in data
    assert data["current"]["coord"]["lat"] == 13.7565
    assert data["current"]["coord"]["lon"] == 121.0583
    assert data["current"]["name"] == "Batangas"

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_sunny_high_uv_scenario():
    response = client.post(
        "/v1/analyze",
        json={"temp": 30.0, "pop": 10.0, "uvi": 9.0, "wind": 5.0, "humidity": 60.0, "forecast": [{"pop": 0.6, "main": {"temp": 31.0}}]}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["scenario"] == "Sunny/High UV"
    assert "High UV" in data["recommendation"]

def test_rain_windy_scenario():
    response = client.post(
        "/v1/analyze",
        json={"temp": 20.0, "pop": 60.0, "uvi": 2.0, "wind": 25.0, "humidity": 90.0, "forecast": [{"pop": 0.8, "main": {"temp": 19.0}}]}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["scenario"] == "Rain/Windy"
    assert "Heavy rain" in data["recommendation"]

def test_cold_scenario():
    response = client.post(
        "/v1/analyze",
        json={"temp": 5.0, "pop": 0.0, "uvi": 1.0, "wind": 5.0, "humidity": 50.0, "forecast": [{"pop": 0.0, "main": {"temp": 6.0}}]}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["scenario"] == "Cold"
    assert "Cold temperatures" in data["recommendation"]

def test_moderate_scenario():
    response = client.post(
        "/v1/analyze",
        json={"temp": 25.0, "pop": 0.0, "uvi": 5.0, "wind": 5.0, "humidity": 40.0, "forecast": [{"pop": 0.0, "main": {"temp": 26.0}}]}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["scenario"] == "Moderate"
    assert "moderate" in data["recommendation"]

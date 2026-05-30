from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_sunny_high_uv_scenario():
    response = client.post(
        "/v1/analyze",
        json={"temp": 30.0, "pop": 10.0, "uvi": 9.0, "wind": 5.0, "humidity": 60.0}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["smart_recommendation"] == "Sunny/High UV"
    assert "High UV" in data["daily_action_plan"]

def test_rain_windy_scenario():
    response = client.post(
        "/v1/analyze",
        json={"temp": 20.0, "pop": 60.0, "uvi": 2.0, "wind": 25.0, "humidity": 90.0}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["smart_recommendation"] == "Rain/Windy"
    assert "Heavy rain" in data["daily_action_plan"]

def test_cold_scenario():
    response = client.post(
        "/v1/analyze",
        json={"temp": 5.0, "pop": 0.0, "uvi": 1.0, "wind": 5.0, "humidity": 50.0}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["smart_recommendation"] == "Cold"
    assert "Cold temperatures" in data["daily_action_plan"]

def test_moderate_scenario():
    response = client.post(
        "/v1/analyze",
        json={"temp": 25.0, "pop": 0.0, "uvi": 5.0, "wind": 5.0, "humidity": 40.0}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["smart_recommendation"] == "Moderate"
    assert "moderate" in data["daily_action_plan"]

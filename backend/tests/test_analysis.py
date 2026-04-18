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
    assert data["scenario"] == "Sunny/High UV"
    assert "sunscreen" in data["recommendation"].lower()
    assert "schedule" in data["action_plan"].lower()

def test_rain_windy_scenario():
    response = client.post(
        "/v1/analyze",
        json={"temp": 20.0, "pop": 60.0, "uvi": 2.0, "wind": 25.0, "humidity": 90.0}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["scenario"] == "Rain/Windy"
    assert "umbrella" in data["recommendation"].lower()
    assert "reschedule" in data["action_plan"].lower()

def test_cold_scenario():
    response = client.post(
        "/v1/analyze",
        json={"temp": 5.0, "pop": 0.0, "uvi": 1.0, "wind": 5.0, "humidity": 50.0}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["scenario"] == "Cold"
    assert "coat" in data["recommendation"].lower()
    assert "keep moving" in data["action_plan"].lower()

def test_moderate_scenario():
    response = client.post(
        "/v1/analyze",
        json={"temp": 20.0, "pop": 0.0, "uvi": 5.0, "wind": 5.0, "humidity": 40.0}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["scenario"] == "Moderate"
    assert "comfortable walking shoes" in data["recommendation"].lower()
    assert "ideal conditions" in data["action_plan"].lower()

def test_warm_humid_scenario():
    response = client.post(
        "/v1/analyze",
        json={"temp": 26.0, "pop": 0.0, "uvi": 5.0, "wind": 5.0, "humidity": 75.0}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["scenario"] == "Warm/Humid"
    assert "cooling towel" in data["recommendation"].lower()
    assert "pace yourself" in data["action_plan"].lower()

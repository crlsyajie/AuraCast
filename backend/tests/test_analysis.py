from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_sunny_high_uv_scenario():
    response = client.post(
        "/v1/analyze",
        json={"temp": 30.0, "pop": 10.0, "uvi": 9.0, "wind": 5.0, "humidity": 60.0, "forecast_24h": [{"temp": 32.0, "pop": 10.0, "wind": 5.0, "humidity": 50.0}]}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["scenario"] == "Sunny/High UV"
    assert "High UV" in data["action_plan"]
    assert "Bring sunglasses" in data["smart_recommendations"]

def test_rain_windy_scenario():
    response = client.post(
        "/v1/analyze",
        json={"temp": 20.0, "pop": 60.0, "uvi": 2.0, "wind": 25.0, "humidity": 90.0, "forecast_24h": [{"temp": 20.0, "pop": 60.0, "wind": 25.0, "humidity": 90.0}]}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["scenario"] == "Rain/Windy"
    assert "Heavy rain" in data["action_plan"]
    assert "Bring an umbrella" in data["smart_recommendations"]
    assert "Wear a windbreaker" in data["smart_recommendations"]

def test_cold_scenario():
    response = client.post(
        "/v1/analyze",
        json={"temp": 5.0, "pop": 0.0, "uvi": 1.0, "wind": 5.0, "humidity": 50.0, "forecast_24h": [{"temp": 5.0, "pop": 0.0, "wind": 5.0, "humidity": 50.0}]}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["scenario"] == "Cold"
    assert "Cold temperatures" in data["action_plan"]
    assert "Bring a jacket" in data["smart_recommendations"]

def test_moderate_scenario():
    response = client.post(
        "/v1/analyze",
        json={"temp": 25.0, "pop": 0.0, "uvi": 5.0, "wind": 5.0, "humidity": 40.0}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["scenario"] == "Moderate"
    assert "moderate" in data["action_plan"]
    assert "Enjoy your day out!" in data["smart_recommendations"]

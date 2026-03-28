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
    assert "High UV detected. Wear sunscreen, sunglasses, and a hat" in data["recommendation"]

def test_rain_windy_scenario():
    response = client.post(
        "/v1/analyze",
        json={"temp": 20.0, "pop": 60.0, "uvi": 2.0, "wind": 25.0, "humidity": 90.0}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["scenario"] == "Rain/Windy"
    assert "Heavy rain and strong winds expected. Bring an umbrella, wear a raincoat" in data["recommendation"]

def test_hot_scenario():
    response = client.post(
        "/v1/analyze",
        json={"temp": 35.0, "pop": 10.0, "uvi": 5.0, "wind": 5.0, "humidity": 60.0}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["scenario"] == "Hot"
    assert "Hot weather. Wear light clothing, stay hydrated, and bring a water bottle." in data["recommendation"]

def test_rain_possible_scenario():
    response = client.post(
        "/v1/analyze",
        json={"temp": 25.0, "pop": 40.0, "uvi": 3.0, "wind": 5.0, "humidity": 80.0}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["scenario"] == "Rain Possible"
    assert "Rain is possible. Bring an umbrella or raincoat just in case." in data["recommendation"]

def test_cold_scenario():
    response = client.post(
        "/v1/analyze",
        json={"temp": 5.0, "pop": 0.0, "uvi": 1.0, "wind": 5.0, "humidity": 50.0}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["scenario"] == "Cold"
    assert "Cold temperatures. Dress warmly in layers, bring a jacket and gloves." in data["recommendation"]

def test_moderate_scenario():
    response = client.post(
        "/v1/analyze",
        json={"temp": 25.0, "pop": 0.0, "uvi": 5.0, "wind": 5.0, "humidity": 40.0}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["scenario"] == "Moderate"
    assert "Weather is moderate. Wear comfortable clothes. Have a great day!" in data["recommendation"]

from fastapi.testclient import TestClient
from main import app
from database import get_db, engine, Base
from sqlalchemy.orm import sessionmaker
import pytest

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_analyze_weather_moderate():
    response = client.post(
        "/v1/analyze",
        json={"temp": 25.0, "pop": 10.0, "uvi": 4.0, "wind": 10.0, "humidity": 50.0}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["scenario"] == "Moderate"
    assert "Weather is moderate" in data["recommendation"]
    assert "smart_recommendations" in data
    assert "Wear light clothing" in data["smart_recommendations"]

def test_analyze_weather_sunny_high_uv():
    response = client.post(
        "/v1/analyze",
        json={"temp": 30.0, "pop": 0.0, "uvi": 9.0, "wind": 5.0, "humidity": 40.0}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["scenario"] == "Sunny/High UV"
    assert "High UV detected" in data["recommendation"]
    assert "smart_recommendations" in data
    assert "Wear sunscreen" in data["smart_recommendations"]

def test_analyze_weather_rain_windy():
    response = client.post(
        "/v1/analyze",
        json={"temp": 20.0, "pop": 80.0, "uvi": 2.0, "wind": 25.0, "humidity": 90.0}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["scenario"] == "Rain/Windy"
    assert "Heavy rain" in data["recommendation"]
    assert "smart_recommendations" in data
    assert "Bring an umbrella" in data["smart_recommendations"]

def test_analyze_weather_cold():
    response = client.post(
        "/v1/analyze",
        json={"temp": 5.0, "pop": 10.0, "uvi": 1.0, "wind": 15.0, "humidity": 60.0}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["scenario"] == "Cold"
    assert "Cold temperatures" in data["recommendation"]
    assert "smart_recommendations" in data
    assert "Wear a heavy coat" in data["smart_recommendations"]

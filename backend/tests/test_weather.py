import json
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_weather():
    response = client.get("/v1/weather")
    print(response.json())

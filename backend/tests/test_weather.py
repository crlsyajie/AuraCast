import json
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

from unittest.mock import patch
import httpx
import os

def test_weather():
    response = client.get("/v1/weather")
    print(response.json())

def test_weather_live_api():
    with patch.dict(os.environ, {"OPENWEATHER_API_KEY": "dummy_key"}):
        with patch("httpx.AsyncClient.get") as mock_get:
            # We need to mock the response twice: once for current_url, once for forecast_url
            mock_response_current = httpx.Response(200, json={"main": {"temp": 28, "humidity": 70}, "wind": {"speed": 4}, "weather": [{"main": "Clouds"}]})
            mock_response_forecast = httpx.Response(200, json={"list": [{"pop": 0.1}]})
            mock_get.side_effect = [mock_response_current, mock_response_forecast]

            response = client.get("/v1/weather?lat=13.7565&lon=121.0583")

            assert response.status_code == 200

            # Check the forecast_url call
            calls = mock_get.call_args_list
            assert len(calls) == 2
            forecast_call_url = calls[1][0][0]
            assert "cnt=8" in forecast_call_url

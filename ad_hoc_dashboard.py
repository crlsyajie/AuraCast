import os
import sys
import json
import httpx
import asyncio

async def run_dashboard():
    lat = 13.7565
    lon = 121.0583
    api_key = os.getenv("OPENWEATHER_API_KEY")

    # Ensure backend directory is in path for imports
    sys.path.insert(0, os.path.abspath("backend"))

    if not api_key:
        mock_file_path = os.path.join("backend", "mock_weather.json")
        with open(mock_file_path, "r") as f:
            mock_data = json.load(f)
            current = mock_data["current"]
            forecast = mock_data["forecast"]
            forecast["list"] = forecast["list"][:8] # cnt=8 limit
    else:
        current_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={api_key}"
        forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units=metric&appid={api_key}&cnt=8"

        async with httpx.AsyncClient() as client:
            current_res = await client.get(current_url)
            forecast_res = await client.get(forecast_url)
            current = current_res.json()
            forecast = forecast_res.json()

    # Calculate derived metrics
    pop = forecast["list"][0].get("pop", 0) * 100
    derived = {
        "temp": current["main"]["temp"],
        "pop": pop,
        "wind": current["wind"]["speed"] * 3.6,
        "uvi": 4.0,
        "humidity": current["main"]["humidity"]
    }

    # Initialize DB (using sqlite by default for ad-hoc if no DATABASE_URL)
    if "DATABASE_URL" not in os.environ:
        os.environ["DATABASE_URL"] = "sqlite:///./weather.db"

    from fastapi.testclient import TestClient
    from main import app
    from database import engine, Base

    # Make sure tables are created
    Base.metadata.create_all(bind=engine)

    with TestClient(app) as test_client:
        response = test_client.post("/v1/analyze", json=derived)
        if response.status_code != 200:
            print(f"Error calling /v1/analyze: {response.text}")
            return
        analysis = response.json()

    # Display in Dashboard Format
    print("=====================================================")
    print("                 AURACAST DASHBOARD")
    print("=====================================================")
    print(f" Location:   Batangas City, Calabarzon, Philippines")
    print(f" Condition:  {current['weather'][0]['description'].capitalize()}")
    print(f" Temp:       {derived['temp']} °C")
    print(f" Humidity:   {derived['humidity']} %")
    print(f" Wind:       {derived['wind']:.2f} km/h")
    print(f" PoP:        {derived['pop']} %")
    print("-----------------------------------------------------")
    print("                24-HOUR FORECAST")
    print("-----------------------------------------------------")
    for item in forecast["list"]:
        dt_txt = item.get("dt_txt", "")
        f_temp = item["main"]["temp"]
        f_desc = item["weather"][0]["description"]
        print(f" {dt_txt} | {f_temp}°C | {f_desc.capitalize()}")
    print("=====================================================")
    print("                DAILY ACTION PLAN")
    print("=====================================================")
    print(f" Scenario:             {analysis['scenario']}")
    print(f" Smart Recommendation: {analysis['recommendation']}")
    print("=====================================================")

if __name__ == "__main__":
    asyncio.run(run_dashboard())

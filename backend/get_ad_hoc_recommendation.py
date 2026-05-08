import asyncio
from fastapi.testclient import TestClient
from main import app, get_db
from database import engine, Base
import os

# Ensure DB is created
Base.metadata.create_all(bind=engine)

client = TestClient(app)

def main():
    # 1. Get weather data
    print("Fetching weather data...")
    response = client.get("/v1/weather?lat=13.7565&lon=121.0583")
    if response.status_code != 200:
        print(f"Failed to get weather data: {response.text}")
        return

    weather_data = response.json()
    derived = weather_data["derived"]

    # 2. Pass to analyze endpoint
    analyze_payload = {
        "temp": derived["temp"],
        "pop": derived["pop"],
        "uvi": derived["uvi"],
        "wind": derived["wind"],
        "humidity": derived["humidity"]
    }

    print("Analyzing weather data...")
    analyze_response = client.post("/v1/analyze", json=analyze_payload)
    if analyze_response.status_code != 200:
        print(f"Failed to analyze data: {analyze_response.text}")
        return

    action_plan = analyze_response.json()

    # 3. Display in AuraCast dashboard format
    print("\n" + "="*50)
    print("                 AURACAST DASHBOARD")
    print("="*50)
    print(" 📍 Location: Batangas City, Calabarzon, Philippines")
    print(f" 🌡️ Current Temp: {derived['temp']}°C")
    print(f" 💧 Humidity:     {derived['humidity']}%")
    print(f" 💨 Wind Speed:   {derived['wind']:.2f} km/h")
    print(f" 🌧️ Chance of Rain: {derived['pop']}%")
    print(f" ☀️ UV Index:     {derived['uvi']}")
    print("-" * 50)
    print(" 💡 Daily Smart Recommendations")
    print("-" * 50)
    print(f" 🏷️  Scenario: {action_plan['scenario']}")
    print(f" 📋 Daily Action Plan:")
    print(f"    > {action_plan['recommendation']}")
    print("=" * 50 + "\n")

if __name__ == "__main__":
    main()

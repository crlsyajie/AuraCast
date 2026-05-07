import os
import httpx
import asyncio
import json

async def run_dashboard():
    lat, lon = 13.7565, 121.0583
    api_key = os.getenv("OPENWEATHER_API_KEY")

    if api_key:
        current_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={api_key}"
        forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units=metric&cnt=8&appid={api_key}"
        async with httpx.AsyncClient() as client:
            current_res = await client.get(current_url)
            forecast_res = await client.get(forecast_url)
            current = current_res.json()
            forecast = forecast_res.json()
    else:
        # Use mock
        with open("backend/mock_weather.json", "r") as f:
            mock_data = json.load(f)
            current = mock_data["current"]
            # To simulate cnt=8, grab first 8
            forecast = mock_data["forecast"]
            forecast["list"] = forecast["list"][:8]

    pop = forecast["list"][0].get("pop", 0) * 100
    temp = current["main"]["temp"]
    wind = current["wind"]["speed"] * 3.6
    uvi = 4.0
    humidity = current["main"]["humidity"]

    payload = {
        "temp": temp,
        "pop": pop,
        "uvi": uvi,
        "wind": wind,
        "humidity": humidity
    }

    # Pass to AuraCast backend /v1/analyze
    async with httpx.AsyncClient() as client:
        analyze_res = await client.post("http://localhost:8000/v1/analyze", json=payload)

    if analyze_res.status_code == 200:
        action_plan = analyze_res.json()
    else:
        print("Failed to get analysis from backend")
        return

    # Display in AuraCast dashboard format
    print("=" * 50)
    print(" 🌤️  AURACAST DASHBOARD ".center(50))
    print("=" * 50)
    print(f"📍 Location: {current['name']}, {current['sys']['country']}")
    print(f"🌡️  Temperature: {temp}°C")
    print(f"💧 Humidity: {humidity}%")
    print(f"💨 Wind Speed: {wind:.2f} km/h")
    print(f"☔ Probability of Precipitation: {pop}%")
    print("-" * 50)
    print("📋 DAILY SMART RECOMMENDATIONS".center(50))
    print(f"Scenario: {action_plan['scenario']}")
    print(f"Action Plan: {action_plan['recommendation']}")
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(run_dashboard())

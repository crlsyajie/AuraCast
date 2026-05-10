import os
import json
import httpx
import asyncio

async def fetch_weather_and_analyze():
    lat = 13.7565
    lon = 121.0583
    api_key = os.getenv("OPENWEATHER_API_KEY")

    if not api_key:
        print("Using local mock data...")
        with open("backend/mock_weather.json", "r") as f:
            mock_data = json.load(f)
            current = mock_data["current"]
            forecast = mock_data["forecast"]
    else:
        print("Using OpenWeather API...")
        current_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={api_key}"
        forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units=metric&cnt=8&appid={api_key}"

        async with httpx.AsyncClient() as client:
            current_res = await client.get(current_url)
            forecast_res = await client.get(forecast_url)

            if current_res.status_code != 200 or forecast_res.status_code != 200:
                print("Error fetching from OpenWeather API.")
                return

            current = current_res.json()
            forecast = forecast_res.json()

    # Extract required data
    temp = current["main"]["temp"]
    pop = forecast["list"][0].get("pop", 0) * 100
    wind = current["wind"]["speed"] * 3.6 # m/s to km/h
    humidity = current["main"]["humidity"]
    uvi = 4.0 # default fallback for current API

    # POST to analyze endpoint
    analyze_url = "http://127.0.0.1:8000/v1/analyze"
    payload = {
        "temp": temp,
        "pop": pop,
        "uvi": uvi,
        "wind": wind,
        "humidity": humidity
    }

    async with httpx.AsyncClient() as client:
        res = await client.post(analyze_url, json=payload)

        if res.status_code != 200:
            print(f"Error from analyze endpoint: {res.status_code} - {res.text}")
            return

        action_plan = res.json()

    print("\n" + "="*50)
    print("🌤️  AuraCast Dashboard - Batangas City, PH")
    print("="*50 + "\n")

    # 1. Location / Primary Forecast
    desc = current["weather"][0]["description"].title()
    feels_like = current["main"]["feels_like"]
    temp_max = current["main"]["temp_max"]
    print(f"📍 Location: Batangas, PH")
    print(f"🌡️  Current Temp: {temp}°C (Feels like {feels_like}°C)")
    print(f"📈 Max Temp: {temp_max}°C")
    print(f"☁️  Condition: {desc}\n")

    # 2. Today's Highlights
    print("--- Today's Highlights ---")
    print(f"💨 Wind: {wind:.2f} km/h")
    print(f"💧 Humidity: {humidity}%")
    print(f"☀️  UV Index: {uvi}")
    print(f"🌧️  Rain Probability: {pop}%\n")

    # 3. Daily Smart Recommendations
    print("--- 💡 Daily Smart Recommendations ---")
    print(f"Scenario: {action_plan['scenario']}")
    print(f"Action Plan: {action_plan['recommendation']}\n")

    # 4. 24-Hour Forecast
    print("--- 🕒 24-Hour Forecast ---")
    # Using the first 8 items (8 * 3 hours = 24 hours)
    for item in forecast["list"][:8]:
        time = item["dt_txt"]
        f_temp = item["main"]["temp"]
        f_desc = item["weather"][0]["description"].title()
        print(f"- {time}: {f_temp}°C, {f_desc}")
    print("\n" + "="*50)

if __name__ == "__main__":
    asyncio.run(fetch_weather_and_analyze())

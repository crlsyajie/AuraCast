import os
import json
import asyncio
import httpx

async def fetch_weather_and_analyze():
    lat = 13.7565
    lon = 121.0583
    api_key = os.getenv("OPENWEATHER_API_KEY")

    if not api_key:
        print("OPENWEATHER_API_KEY not set. Using mock data.")
        mock_file_path = os.path.join(os.path.dirname(__file__), "mock_weather.json")
        try:
            with open(mock_file_path, "r") as f:
                mock_data = json.load(f)
                current = mock_data["current"]
                forecast = mock_data["forecast"]
        except FileNotFoundError:
            print("Mock weather data file not found")
            return
    else:
        print("Fetching from OpenWeather API...")
        current_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={api_key}"
        forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&cnt=8&units=metric&appid={api_key}"

        async with httpx.AsyncClient() as client:
            current_res = await client.get(current_url)
            forecast_res = await client.get(forecast_url)
            if current_res.status_code != 200 or forecast_res.status_code != 200:
                print("Failed to fetch weather data from OpenWeather API.")
                return
            current = current_res.json()
            forecast = forecast_res.json()

    # Derived data matching backend logic
    pop = forecast["list"][0].get("pop", 0) * 100
    derived = {
        "temp": current["main"]["temp"],
        "pop": pop,
        "wind": current["wind"]["speed"] * 3.6, # Convert m/s to km/h
        "uvi": 4.0, # Fallback default
        "humidity": current["main"]["humidity"]
    }

    print("Passing data to AuraCast backend /v1/analyze endpoint...")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post("http://localhost:8000/v1/analyze", json=derived)
            if response.status_code == 200:
                plan = response.json()

                print("\n" + "="*60)
                print(" " * 15 + "AURACAST DASHBOARD")
                print("="*60)
                print(f"Location:        Batangas City, Calabarzon, Philippines")
                print(f"Coordinates:     {lat}, {lon}")
                print("-" * 60)
                print("TODAY'S HIGHLIGHTS:")
                print(f"  Temperature:   {derived['temp']} °C")
                print(f"  Precipitation: {derived['pop']}%")
                print(f"  Wind Speed:    {derived['wind']:.2f} km/h")
                print(f"  Humidity:      {derived['humidity']}%")
                print(f"  UV Index:      {derived['uvi']}")
                print("-" * 60)
                print("DAILY SMART RECOMMENDATIONS:")
                print(f"  Scenario:      {plan['scenario']}")
                print(f"  Action Plan:   {plan['recommendation']}")
                print("="*60 + "\n")
            else:
                print("Failed to get analysis from backend:", response.text)
        except Exception as e:
            print("Could not connect to backend server. Make sure it is running on port 8000.")
            print(e)

if __name__ == "__main__":
    asyncio.run(fetch_weather_and_analyze())

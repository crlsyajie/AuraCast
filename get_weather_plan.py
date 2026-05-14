import requests
from datetime import datetime

BACKEND_URL = "http://localhost:8000"

def get_weather(lat, lon):
    res = requests.get(f"{BACKEND_URL}/v1/weather?lat={lat}&lon={lon}")
    res.raise_for_status()
    return res.json()

def analyze_weather(derived_data):
    res = requests.post(f"{BACKEND_URL}/v1/analyze", json=derived_data)
    res.raise_for_status()
    return res.json()

def main():
    print("Fetching weather data for Batangas City...")
    lat, lon = 13.7565, 121.0583

    weather_data = get_weather(lat, lon)
    derived = weather_data["derived"]
    current = weather_data["current"]

    analysis = analyze_weather(derived)

    # Format Output
    print("\n" + "="*50)
    print("                AURACAST DASHBOARD")
    print("="*50)

    # Location section
    day_name = datetime.fromtimestamp(current["dt"]).strftime('%A')
    date_str = datetime.fromtimestamp(current["dt"]).strftime('%d %b %Y')
    print(f"\n[Location]")
    print(f"{current['name']}, {current['sys']['country']}")
    print(f"{day_name}, {date_str}")
    print(f"{round(current['main']['temp'])}°C / {round(current['main']['temp_max'])}°C")
    print(f"{current['weather'][0]['main']} (Feels like {round(current['main']['feels_like'])}°C)")

    # Highlights
    print("\n[Today's Highlights]")
    print(f"- Wind Status: {round(current['wind']['speed'] * 3.6, 2)} km/h")
    print(f"- Humidity: {current['main']['humidity']}%")
    print(f"- UV Index: {derived['uvi']} uv")
    print(f"- Visibility: {round(current['visibility'] / 1000, 1)} km")

    # Daily Action Plan
    print("\n[Daily Smart Recommendations]")
    print(f"Scenario: {analysis['scenario']}")
    print(f"Action Plan: {analysis['recommendation']}")

    # 24-Hour Forecast
    print("\n[24-Hour Forecast]")
    forecasts = weather_data["forecast"]["list"][:8]
    for i, f in enumerate(forecasts):
        time_str = "Now" if i == 0 else datetime.fromtimestamp(f["dt"]).strftime('%I:%M %p')
        temp = round(f["main"]["temp"])
        desc = f["weather"][0]["main"]
        print(f"  {time_str:<10} | {temp}°C | {desc}")

    print("="*50)

if __name__ == "__main__":
    main()

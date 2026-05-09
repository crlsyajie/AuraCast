import httpx
import sys

def main():
    base_url = "http://localhost:8000"
    try:
        weather_res = httpx.get(f"{base_url}/v1/weather?lat=13.7565&lon=121.0583")
        weather_res.raise_for_status()
        weather_data = weather_res.json()
    except Exception as e:
        print(f"Error fetching weather: {e}")
        sys.exit(1)

    derived = weather_data['derived']

    try:
        analyze_res = httpx.post(f"{base_url}/v1/analyze", json={
            "temp": derived['temp'],
            "pop": derived['pop'],
            "uvi": derived['uvi'],
            "wind": derived['wind'],
            "humidity": derived['humidity']
        })
        analyze_res.raise_for_status()
        action_plan = analyze_res.json()
    except Exception as e:
        print(f"Error analyzing weather: {e}")
        sys.exit(1)

    # AuraCast Dashboard Format
    print("==================================================")
    print("         AuraCast Dashboard - Batangas City       ")
    print("==================================================")
    print(" 🌍 Location: Batangas City, Calabarzon, PH")
    print(f" 🌡️  Temperature : {derived['temp']}°C")
    print(f" 💧 Humidity    : {derived['humidity']}%")
    print(f" 💨 Wind Speed  : {derived['wind']:.2f} km/h")
    print(f" ☀️  UV Index    : {derived['uvi']}")
    print(f" 🌧️  Chance of Rain: {derived['pop']}%")
    print("--------------------------------------------------")
    print(" 💡 DAILY SMART RECOMMENDATIONS")
    print(f"    Scenario : {action_plan['scenario']}")
    print(f"    Daily Action Plan : {action_plan['recommendation']}")
    print("==================================================")

if __name__ == "__main__":
    main()

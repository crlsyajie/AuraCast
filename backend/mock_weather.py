import time
from datetime import datetime, timedelta, timezone

def get_mock_weather(lat: float, lon: float):
    now = int(time.time())

    current = {
        "coord": {"lon": lon, "lat": lat},
        "weather": [{"id": 500, "main": "Rain", "description": "light rain", "icon": "10d"}],
        "base": "stations",
        "main": {
            "temp": 28.5,
            "feels_like": 32.2,
            "temp_min": 28.0,
            "temp_max": 29.0,
            "pressure": 1012,
            "humidity": 78,
            "sea_level": 1012,
            "grnd_level": 1010
        },
        "visibility": 10000,
        "wind": {"speed": 4.5, "deg": 180, "gust": 6.2},
        "clouds": {"all": 100},
        "dt": now,
        "sys": {"country": "PH", "sunrise": now - 20000, "sunset": now + 20000},
        "timezone": 28800,
        "id": 1726449,
        "name": "Batangas City",
        "cod": 200
    }

    forecast_list = []
    base_time = datetime.now(timezone.utc)

    # We must ensure we have entries containing "12:00:00" for 5 days so the UI shows it.
    for i in range(6):
        day_12 = (base_time + timedelta(days=i)).replace(hour=12, minute=0, second=0)
        forecast_list.append({
            "dt": int(day_12.timestamp()),
            "main": {"temp": 29.0, "temp_min": 27.0, "temp_max": 32.0, "humidity": 75},
            "weather": [{"id": 800, "main": "Clear", "description": "clear sky", "icon": "01d"}],
            "wind": {"speed": 3.0},
            "pop": 0.1,
            "dt_txt": day_12.strftime("%Y-%m-%d %H:%M:%S")
        })

    # Add a current forecast entry to grab POP
    forecast_list.insert(0, {
        "dt": now,
        "main": {"temp": 28.5, "temp_min": 28.0, "temp_max": 29.0, "humidity": 78},
        "weather": [{"id": 500, "main": "Rain", "description": "light rain", "icon": "10d"}],
        "wind": {"speed": 4.5},
        "pop": 0.8,
        "dt_txt": base_time.strftime("%Y-%m-%d %H:%M:%S")
    })

    forecast = {
        "cod": "200",
        "message": 0,
        "cnt": len(forecast_list),
        "list": forecast_list,
        "city": {
            "id": 1726449,
            "name": "Batangas City",
            "coord": {"lat": lat, "lon": lon},
            "country": "PH",
            "timezone": 28800
        }
    }

    return current, forecast

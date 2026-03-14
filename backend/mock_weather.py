import json

mock_current = {
    "coord": {"lon": 121.0597, "lat": 13.7559},
    "weather": [{"id": 801, "main": "Clouds", "description": "few clouds", "icon": "02d"}],
    "base": "stations",
    "main": {
        "temp": 32.5,
        "feels_like": 36.0,
        "temp_min": 32.0,
        "temp_max": 33.0,
        "pressure": 1010,
        "humidity": 65,
        "sea_level": 1010,
        "grnd_level": 1005
    },
    "visibility": 10000,
    "wind": {"speed": 4.5, "deg": 90, "gust": 6.2},
    "clouds": {"all": 20},
    "dt": 1710486000,
    "sys": {
        "type": 1,
        "id": 8160,
        "country": "PH",
        "sunrise": 1710453600,
        "sunset": 1710497100
    },
    "timezone": 28800,
    "id": 1726449,
    "name": "Batangas City",
    "cod": 200
}

mock_forecast = {
    "cod": "200",
    "message": 0,
    "cnt": 8,
    "list": [
        {
            "dt": 1710493200,
            "main": {"temp": 31.0, "feels_like": 35.0, "temp_min": 31.0, "temp_max": 31.0, "pressure": 1010, "humidity": 70},
            "weather": [{"id": 802, "main": "Clouds", "description": "scattered clouds", "icon": "03n"}],
            "clouds": {"all": 40},
            "wind": {"speed": 4.0, "deg": 100},
            "visibility": 10000,
            "pop": 0.1,
            "dt_txt": "2024-03-15 09:00:00"
        },
        {
            "dt": 1710504000,
            "main": {"temp": 29.5, "feels_like": 33.0, "temp_min": 29.5, "temp_max": 29.5, "pressure": 1011, "humidity": 75},
            "weather": [{"id": 803, "main": "Clouds", "description": "broken clouds", "icon": "04n"}],
            "clouds": {"all": 60},
            "wind": {"speed": 3.5, "deg": 110},
            "visibility": 10000,
            "pop": 0.2,
            "dt_txt": "2024-03-15 12:00:00"
        },
        {
            "dt": 1710514800,
            "main": {"temp": 28.0, "feels_like": 31.0, "temp_min": 28.0, "temp_max": 28.0, "pressure": 1012, "humidity": 80},
            "weather": [{"id": 500, "main": "Rain", "description": "light rain", "icon": "10n"}],
            "clouds": {"all": 80},
            "wind": {"speed": 3.0, "deg": 120},
            "visibility": 8000,
            "pop": 0.5,
            "rain": {"3h": 1.2},
            "dt_txt": "2024-03-15 15:00:00"
        },
        {
            "dt": 1710525600,
            "main": {"temp": 27.5, "feels_like": 30.5, "temp_min": 27.5, "temp_max": 27.5, "pressure": 1012, "humidity": 82},
            "weather": [{"id": 500, "main": "Rain", "description": "light rain", "icon": "10n"}],
            "clouds": {"all": 90},
            "wind": {"speed": 2.5, "deg": 130},
            "visibility": 7000,
            "pop": 0.6,
            "rain": {"3h": 2.5},
            "dt_txt": "2024-03-15 18:00:00"
        },
        {
            "dt": 1710536400,
            "main": {"temp": 27.0, "feels_like": 30.0, "temp_min": 27.0, "temp_max": 27.0, "pressure": 1013, "humidity": 85},
            "weather": [{"id": 804, "main": "Clouds", "description": "overcast clouds", "icon": "04d"}],
            "clouds": {"all": 95},
            "wind": {"speed": 2.0, "deg": 140},
            "visibility": 9000,
            "pop": 0.3,
            "dt_txt": "2024-03-15 21:00:00"
        },
        {
            "dt": 1710547200,
            "main": {"temp": 28.5, "feels_like": 32.0, "temp_min": 28.5, "temp_max": 28.5, "pressure": 1014, "humidity": 80},
            "weather": [{"id": 802, "main": "Clouds", "description": "scattered clouds", "icon": "03d"}],
            "clouds": {"all": 40},
            "wind": {"speed": 3.0, "deg": 150},
            "visibility": 10000,
            "pop": 0.1,
            "dt_txt": "2024-03-16 00:00:00"
        },
        {
            "dt": 1710558000,
            "main": {"temp": 31.0, "feels_like": 35.5, "temp_min": 31.0, "temp_max": 31.0, "pressure": 1013, "humidity": 70},
            "weather": [{"id": 801, "main": "Clouds", "description": "few clouds", "icon": "02d"}],
            "clouds": {"all": 20},
            "wind": {"speed": 4.0, "deg": 160},
            "visibility": 10000,
            "pop": 0.0,
            "dt_txt": "2024-03-16 03:00:00"
        },
        {
            "dt": 1710568800,
            "main": {"temp": 33.5, "feels_like": 38.0, "temp_min": 33.5, "temp_max": 33.5, "pressure": 1011, "humidity": 60},
            "weather": [{"id": 800, "main": "Clear", "description": "clear sky", "icon": "01d"}],
            "clouds": {"all": 0},
            "wind": {"speed": 5.0, "deg": 170},
            "visibility": 10000,
            "pop": 0.0,
            "dt_txt": "2024-03-16 06:00:00"
        }
    ],
    "city": {
        "id": 1726449,
        "name": "Batangas City",
        "coord": {"lat": 13.7559, "lon": 121.0597},
        "country": "PH",
        "population": 237370,
        "timezone": 28800,
        "sunrise": 1710453600,
        "sunset": 1710497100
    }
}

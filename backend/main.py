from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
import os
import httpx
from dotenv import load_dotenv
from database import get_db
import models
import json

load_dotenv()

app = FastAPI(title="AuraCast Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class WeatherData(BaseModel):
    temp: float
    pop: float
    uvi: float
    wind: float
    humidity: float
    forecast_pop_24h: float
    forecast_temp_min_24h: float
    forecast_temp_max_24h: float

class ActionPlan(BaseModel):
    recommendation: str
    scenario: str

@app.post("/v1/analyze", response_model=ActionPlan)
def analyze_weather(data: WeatherData, db: Session = Depends(get_db)):
    # Save weather log
    weather_log = models.WeatherLog(
        temperature=data.temp,
        humidity=data.humidity,
        uv_data=data.uvi
    )
    db.add(weather_log)
    db.commit()
    db.refresh(weather_log)

    action_plan = None
    if data.forecast_pop_24h >= 50 or data.pop >= 50:
        if data.wind >= 20:
            action_plan = ActionPlan(
                recommendation="Heavy rain and strong winds expected. Stay indoors if possible and secure loose items.",
                scenario="Rain/Windy"
            )
        else:
            action_plan = ActionPlan(
                recommendation="High chance of rain in the next 24 hours. Don't forget to bring an umbrella and a raincoat.",
                scenario="Rain"
            )
    elif data.forecast_temp_max_24h >= 32 or data.uvi >= 8:
        action_plan = ActionPlan(
            recommendation="High temperatures or UV detected. Wear sunscreen, bring sunglasses, and stay hydrated.",
            scenario="Sunny/High UV"
        )
    elif data.forecast_temp_min_24h < 15 or data.temp < 15:
        action_plan = ActionPlan(
            recommendation="Cold temperatures expected. Dress warmly in layers and bring a jacket.",
            scenario="Cold"
        )
    else:
        action_plan = ActionPlan(
            recommendation="Weather is moderate over the next 24 hours. Perfect day for outdoor activities. Bring light clothes and a water bottle.",
            scenario="Moderate"
        )

    # Save recommendation log
    rec_log = models.RecommendationLog(
        weather_log_id=weather_log.id,
        recommendation=action_plan.recommendation,
        scenario=action_plan.scenario,
        is_followed=False
    )
    db.add(rec_log)
    db.commit()

    return action_plan

@app.get("/v1/history")
def get_history(db: Session = Depends(get_db)):
    logs = db.query(models.RecommendationLog).order_by(models.RecommendationLog.timestamp.desc()).limit(5).all()
    history = []
    for log in logs:
        weather = log.weather_log
        history.append({
            "id": log.id,
            "recommendation": log.recommendation,
            "scenario": log.scenario,
            "is_followed": log.is_followed,
            "timestamp": log.timestamp,
            "weather": {
                "temperature": weather.temperature,
                "humidity": weather.humidity,
                "uv_data": weather.uv_data
            } if weather else None
        })
    return history

@app.get("/v1/weather")
async def get_weather(lat: float = 13.75, lon: float = 121.05):
    api_key = os.getenv("OPENWEATHER_API_KEY")

    if not api_key:
        # Fall back to mock response if API key is not configured
        mock_file_path = os.path.join(os.path.dirname(__file__), "mock_weather.json")
        try:
            with open(mock_file_path, "r") as f:
                mock_data = json.load(f)
                current = mock_data["current"]
                forecast = mock_data["forecast"]
        except FileNotFoundError:
            raise HTTPException(status_code=500, detail="Mock weather data file not found")
    else:
        # Use Current Weather data endpoint
        current_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={api_key}"
        forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units=metric&appid={api_key}"

        async with httpx.AsyncClient() as client:
            current_res = await client.get(current_url)
            forecast_res = await client.get(forecast_url)

            if current_res.status_code != 200:
                raise HTTPException(status_code=current_res.status_code, detail="Failed to fetch current weather")
            if forecast_res.status_code != 200:
                raise HTTPException(status_code=forecast_res.status_code, detail="Failed to fetch forecast")

            current = current_res.json()
            forecast = forecast_res.json()

    # Pop is not directly available in current, grab it from forecast for today
    pop = forecast["list"][0].get("pop", 0) * 100

    # Calculate 24-hour forecast derived fields (next 8 3-hour chunks)
    forecast_24h = forecast["list"][:8]
    forecast_pop_24h = max([item.get("pop", 0) for item in forecast_24h]) * 100
    forecast_temp_min_24h = min([item["main"]["temp_min"] for item in forecast_24h])
    forecast_temp_max_24h = max([item["main"]["temp_max"] for item in forecast_24h])

    # Note: OpenWeather current API does not provide UVI. We will mock UVI or set to a default for analysis
    # as the free tier does not include UVI easily in the current weather endpoint

    return {
        "current": current,
        "forecast": forecast,
        "derived": {
            "temp": current["main"]["temp"],
            "pop": pop,
            "wind": current["wind"]["speed"] * 3.6, # Convert m/s to km/h
            "uvi": 4.0, # Fallback default
            "humidity": current["main"]["humidity"],
            "forecast_pop_24h": forecast_pop_24h,
            "forecast_temp_min_24h": forecast_temp_min_24h,
            "forecast_temp_max_24h": forecast_temp_max_24h
        }
    }

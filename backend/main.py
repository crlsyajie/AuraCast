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

from typing import List, Optional

class HourlyForecast(BaseModel):
    temp: float
    pop: float
    wind: float
    humidity: float

class WeatherData(BaseModel):
    temp: float
    pop: float
    uvi: float
    wind: float
    humidity: float
    forecast_24h: Optional[List[HourlyForecast]] = None

class ActionPlan(BaseModel):
    action_plan: str
    smart_recommendations: List[str]
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

    action_plan_text = ""
    scenario = ""
    smart_recommendations = []

    if data.uvi >= 8 and data.pop < 20:
        action_plan_text = "High UV detected. Wear sunscreen and limit outdoor exposure."
        scenario = "Sunny/High UV"
    elif data.pop >= 50 and data.wind >= 20:
        action_plan_text = "Heavy rain and strong winds expected. Stay indoors if possible."
        scenario = "Rain/Windy"
    elif data.temp < 10:
        action_plan_text = "Cold temperatures. Dress warmly in layers."
        scenario = "Cold"
    else:
        action_plan_text = "Weather is moderate. Have a great day!"
        scenario = "Moderate"

    if data.forecast_24h:
        will_rain = any(f.pop >= 50 for f in data.forecast_24h)
        high_wind = any(f.wind >= 20 for f in data.forecast_24h)
        cold = any(f.temp < 20 for f in data.forecast_24h)
        hot = any(f.temp > 30 for f in data.forecast_24h)

        if will_rain:
            smart_recommendations.append("Bring an umbrella")
        if high_wind:
            smart_recommendations.append("Wear a windbreaker")
        if cold:
            smart_recommendations.append("Bring a jacket")
        if hot and data.uvi >= 6:
            smart_recommendations.append("Bring sunglasses")

    # Default fallback if empty
    if not smart_recommendations:
        smart_recommendations.append("Enjoy your day out!")

    action_plan = ActionPlan(
        action_plan=action_plan_text,
        smart_recommendations=smart_recommendations,
        scenario=scenario
    )

    # Save recommendation log
    rec_log = models.RecommendationLog(
        weather_log_id=weather_log.id,
        action_plan=action_plan.action_plan,
        smart_recommendations=json.dumps(action_plan.smart_recommendations),
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
        smart_recs = []
        if log.smart_recommendations:
            try:
                smart_recs = json.loads(log.smart_recommendations)
            except json.JSONDecodeError:
                pass

        history.append({
            "id": log.id,
            "action_plan": log.action_plan,
            "smart_recommendations": smart_recs,
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
async def get_weather(lat: float = 13.7565, lon: float = 121.0583):
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
            "humidity": current["main"]["humidity"]
        }
    }

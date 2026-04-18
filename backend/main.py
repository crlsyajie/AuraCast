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

class ActionPlan(BaseModel):
    action_plan: str
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
    if data.uvi >= 8 and data.pop < 20:
        action_plan = ActionPlan(
            action_plan="Schedule outdoor activities before 10 AM or after 4 PM to avoid peak UV radiation.",
            recommendation="Bring broad-spectrum sunscreen (SPF 30+), UV-blocking sunglasses, and a wide-brimmed hat.",
            scenario="Sunny/High UV"
        )
    elif data.pop >= 50 and data.wind >= 20:
        action_plan = ActionPlan(
            action_plan="Reschedule outdoor events and plan indoor activities. Allow extra time for commuting.",
            recommendation="Bring a sturdy windproof umbrella, a waterproof jacket, and rain boots.",
            scenario="Rain/Windy"
        )
    elif data.temp < 10:
        action_plan = ActionPlan(
            action_plan="Keep outdoor time brief and keep moving to stay warm. Ensure your heating system is functioning.",
            recommendation="Bring a heavy winter coat, thermal layers, gloves, and a warm beanie.",
            scenario="Cold"
        )
    elif data.temp >= 25 and data.humidity >= 70:
        action_plan = ActionPlan(
            action_plan="Pace yourself if exercising outdoors due to high humidity. Plan for air-conditioned breaks.",
            recommendation="Bring a large water bottle, light breathable clothing, and a cooling towel.",
            scenario="Warm/Humid"
        )
    else:
        action_plan = ActionPlan(
            action_plan="Ideal conditions for a mix of indoor and outdoor activities. Enjoy a walk or outdoor dining.",
            recommendation="Bring a light jacket for the evening, a water bottle to stay hydrated, and comfortable walking shoes.",
            scenario="Moderate"
        )

    # Save recommendation log
    rec_log = models.RecommendationLog(
        weather_log_id=weather_log.id,
        action_plan=action_plan.action_plan,
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

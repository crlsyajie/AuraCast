from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
import os
import httpx
from dotenv import load_dotenv
from database import get_db
import models

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
            recommendation="High UV detected. Wear sunscreen and limit outdoor exposure.",
            scenario="Sunny/High UV"
        )
    elif data.pop >= 50 and data.wind >= 20:
        action_plan = ActionPlan(
            recommendation="Heavy rain and strong winds expected. Stay indoors if possible.",
            scenario="Rain/Windy"
        )
    elif data.temp < 10:
        action_plan = ActionPlan(
            recommendation="Cold temperatures. Dress warmly in layers.",
            scenario="Cold"
        )
    else:
        action_plan = ActionPlan(
            recommendation="Weather is moderate. Have a great day!",
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
async def get_weather(lat: float = 13.7559, lon: float = 121.0597):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        try:
            from mock_weather import mock_current, mock_forecast
            current = mock_current
            forecast = mock_forecast
            # Filter to 24-hour forecast (8 items of 3-hour intervals)
            forecast["list"] = forecast["list"][:8]

            pop = forecast["list"][0].get("pop", 0) * 100

            return {
                "current": current,
                "forecast": forecast,
                "derived": {
                    "temp": current["main"]["temp"],
                    "pop": pop,
                    "wind": current["wind"]["speed"] * 3.6,
                    "uvi": 8.0, # Mock a high UV scenario for interesting action plan
                    "humidity": current["main"]["humidity"]
                }
            }
        except ImportError:
            raise HTTPException(status_code=500, detail="API key not configured and mock data missing")

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

        # Filter to 24-hour forecast (8 items of 3-hour intervals)
        forecast["list"] = forecast["list"][:8]

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

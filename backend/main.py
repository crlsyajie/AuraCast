from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import httpx
from dotenv import load_dotenv

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

class ActionPlan(BaseModel):
    recommendation: str
    scenario: str

@app.post("/v1/analyze", response_model=ActionPlan)
def analyze_weather(data: WeatherData):
    if data.uvi >= 8 and data.pop < 20:
        return ActionPlan(
            recommendation="High UV detected. Wear sunscreen and limit outdoor exposure.",
            scenario="Sunny/High UV"
        )
    elif data.pop >= 50 and data.wind >= 20:
        return ActionPlan(
            recommendation="Heavy rain and strong winds expected. Stay indoors if possible.",
            scenario="Rain/Windy"
        )
    elif data.temp < 10:
        return ActionPlan(
            recommendation="Cold temperatures. Dress warmly in layers.",
            scenario="Cold"
        )
    else:
        return ActionPlan(
            recommendation="Weather is moderate. Have a great day!",
            scenario="Moderate"
        )

@app.get("/v1/weather")
async def get_weather(lat: float = 23.8103, lon: float = 90.4125):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="API key not configured")

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
                "uvi": 4.0 # Fallback default
            }
        }

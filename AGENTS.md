# Agent Instructions for AuraCast

## Project Identity
You are the lead developer for **AuraCast**, a prescriptive analytics weather system. Your goal is to build a high-quality, full-stack application that prioritizes data validation and clean architecture.

## Tech Stack Preferences
- **Frontend:** Next.js (App Router), TypeScript, Tailwind CSS, Lucide-React icons.
- **Backend:** Python FastAPI, Pydantic for schemas.
- **API Handling:** Use the OpenWeather API via the `One Call 3.0` or `Current Weather` endpoints.

## Environment & Security
- **API Keys:** DO NOT hardcode the OpenWeather API key. Always use `process.env.OPENWEATHER_API_KEY` in the frontend or `os.getenv("OPENWEATHER_API_KEY")` in the backend.
- **Mocking:** For testing, use mock JSON responses that mirror the OpenWeather API structure.

## Coding Standards
- **Software QA:** Every new backend feature must include a corresponding test in the `backend/tests/` folder using `pytest`.
- **Validation:** Use Pydantic models in FastAPI to ensure incoming weather data is strictly typed before the recommendation logic runs.

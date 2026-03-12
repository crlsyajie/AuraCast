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
- 
## Visual Design Reference (CRUCIAL)
- **UI Blueprint:** Use the attached image `image_0.png` as the *absolute blueprint* for the dashboard's layout, color palette (Dark Mode with 2D icons), and information hierarchy.
- **Layout Hierarchy:**
  1. Top Left: Location/Primary Forecast (e.g., Dhaka, 28°C).
  2. Bottom Left: "Others Countries" list.
  3. Top Right: "Today’s Highlight" (Wind, Humidity, UV, Sunrise/Sunset).
  4. Bottom Right: "10-Day Forecast" grid.
- **New Section (REQUIRED):** You must replace the "Others Countries" section with a *matching, card-based section* titled **"Daily Smart Recommendations"**.
## Database & Persistence
- **Choice:** PostgreSQL (using SQLAlchemy or Tortoise ORM in FastAPI).
- **Architecture:** Use a `models/` folder in the backend. 
- **Tracking:** We need to store:
  1. `WeatherSnapshots`: Raw data from OpenWeather.
  2. `UserActions`: Which recommendations the user "accepted" or "ignored" (crucial for future ML training).
- **Migrations:** Use `Alembic` for database migrations.

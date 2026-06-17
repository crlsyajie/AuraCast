from sqlalchemy import Column, Integer, Float, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import datetime
from database import Base

class WeatherLog(Base):
    __tablename__ = "weather_logs"

    id = Column(Integer, primary_key=True, index=True)
    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    uv_data = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))

    recommendations = relationship("RecommendationLog", back_populates="weather_log")


class RecommendationLog(Base):
    __tablename__ = "recommendation_logs"

    id = Column(Integer, primary_key=True, index=True)
    weather_log_id = Column(Integer, ForeignKey("weather_logs.id"))
    recommendation = Column(String, nullable=False)
    smart_recommendations = Column(String, nullable=True) # Stored as JSON string
    scenario = Column(String, nullable=False)
    is_followed = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))

    weather_log = relationship("WeatherLog", back_populates="recommendations")

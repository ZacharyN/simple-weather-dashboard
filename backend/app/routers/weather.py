from fastapi import APIRouter, HTTPException, Query

from app.services.openweather import OpenWeatherService
from app.models.weather import WeatherResponse, ForecastResponse, AlertsResponse, HistoryResponse

router = APIRouter()
weather_service = OpenWeatherService()


@router.get("/current", response_model=WeatherResponse)
async def get_current_weather(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude")
):
    """Get current weather conditions."""
    try:
        return await weather_service.get_current_weather(lat, lon)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/forecast", response_model=ForecastResponse)
async def get_forecast(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude")
):
    """Get hourly and daily forecast."""
    try:
        return await weather_service.get_forecast(lat, lon)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/alerts", response_model=AlertsResponse)
async def get_alerts(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude")
):
    """Get weather alerts for location."""
    try:
        return await weather_service.get_alerts(lat, lon)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history", response_model=HistoryResponse)
async def get_history(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
    hours: int = Query(24, description="Hours of history", ge=1, le=48)
):
    """Get precipitation history for past hours."""
    try:
        return await weather_service.get_history(lat, lon, hours)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

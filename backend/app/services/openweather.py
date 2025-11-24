import httpx
from datetime import datetime, timedelta
from typing import Any

from app.config import get_settings
from app.models.weather import (
    WeatherResponse,
    ForecastResponse,
    AlertsResponse,
    HistoryResponse,
    HistoryEntry,
)


class OpenWeatherService:
    BASE_URL = "https://api.openweathermap.org/data/3.0/onecall"

    def __init__(self):
        settings = get_settings()
        self.api_key = settings.openweather_api_key

    async def _make_request(self, endpoint: str, params: dict) -> dict[str, Any]:
        """Make async request to OpenWeather API."""
        params["appid"] = self.api_key
        params["units"] = "imperial"  # Use imperial units (Fahrenheit)

        async with httpx.AsyncClient() as client:
            url = f"{self.BASE_URL}{endpoint}" if endpoint else self.BASE_URL
            response = await client.get(url, params=params, timeout=30.0)
            response.raise_for_status()
            return response.json()

    async def get_current_weather(self, lat: float, lon: float) -> WeatherResponse:
        """Get current weather conditions."""
        data = await self._make_request("", {
            "lat": lat,
            "lon": lon,
            "exclude": "minutely,hourly,daily,alerts"
        })

        return WeatherResponse(
            lat=data["lat"],
            lon=data["lon"],
            timezone=data["timezone"],
            timezone_offset=data["timezone_offset"],
            current=data["current"]
        )

    async def get_forecast(self, lat: float, lon: float) -> ForecastResponse:
        """Get hourly and daily forecast."""
        data = await self._make_request("", {
            "lat": lat,
            "lon": lon,
            "exclude": "minutely,current,alerts"
        })

        return ForecastResponse(
            lat=data["lat"],
            lon=data["lon"],
            timezone=data["timezone"],
            timezone_offset=data["timezone_offset"],
            hourly=data.get("hourly", []),
            daily=data.get("daily", [])
        )

    async def get_alerts(self, lat: float, lon: float) -> AlertsResponse:
        """Get weather alerts for location."""
        data = await self._make_request("", {
            "lat": lat,
            "lon": lon,
            "exclude": "minutely,hourly,daily,current"
        })

        return AlertsResponse(
            lat=data["lat"],
            lon=data["lon"],
            timezone=data["timezone"],
            alerts=data.get("alerts", [])
        )

    async def get_history(self, lat: float, lon: float, hours: int = 24) -> HistoryResponse:
        """Get precipitation history using timemachine endpoint."""
        history_entries: list[HistoryEntry] = []

        # Get historical data for each hour
        now = datetime.utcnow()

        async with httpx.AsyncClient() as client:
            for i in range(hours):
                timestamp = int((now - timedelta(hours=i+1)).timestamp())

                params = {
                    "lat": lat,
                    "lon": lon,
                    "dt": timestamp,
                    "appid": self.api_key,
                    "units": "imperial"
                }

                try:
                    response = await client.get(
                        f"{self.BASE_URL}/timemachine",
                        params=params,
                        timeout=30.0
                    )
                    response.raise_for_status()
                    data = response.json()

                    # Extract relevant data from timemachine response
                    if "data" in data and len(data["data"]) > 0:
                        hour_data = data["data"][0]

                        # Calculate precipitation (rain + snow)
                        precipitation = 0.0
                        if "rain" in hour_data:
                            precipitation += hour_data["rain"].get("1h", 0)
                        if "snow" in hour_data:
                            precipitation += hour_data["snow"].get("1h", 0)

                        history_entries.append(HistoryEntry(
                            dt=hour_data["dt"],
                            temp=hour_data.get("temp", 0),
                            humidity=hour_data.get("humidity", 0),
                            precipitation=precipitation,
                            weather=hour_data.get("weather", [])
                        ))
                except Exception:
                    # Skip failed requests for individual hours
                    continue

        # Sort by timestamp (oldest first)
        history_entries.sort(key=lambda x: x.dt)

        return HistoryResponse(
            lat=lat,
            lon=lon,
            timezone="UTC",
            history=history_entries
        )

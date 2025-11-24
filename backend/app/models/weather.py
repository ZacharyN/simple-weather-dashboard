from pydantic import BaseModel
from typing import Optional


class WeatherCondition(BaseModel):
    id: int
    main: str
    description: str
    icon: str


class CurrentWeather(BaseModel):
    dt: int
    sunrise: int
    sunset: int
    temp: float
    feels_like: float
    humidity: int
    pressure: int
    uvi: float
    clouds: int
    visibility: int
    wind_speed: float
    wind_deg: int
    wind_gust: Optional[float] = None
    weather: list[WeatherCondition]
    rain: Optional[dict] = None
    snow: Optional[dict] = None


class HourlyForecast(BaseModel):
    dt: int
    temp: float
    feels_like: float
    humidity: int
    pressure: int
    uvi: float
    clouds: int
    visibility: int
    wind_speed: float
    wind_deg: int
    wind_gust: Optional[float] = None
    weather: list[WeatherCondition]
    pop: float  # Probability of precipitation
    rain: Optional[dict] = None
    snow: Optional[dict] = None


class DailyTemp(BaseModel):
    day: float
    min: float
    max: float
    night: float
    eve: float
    morn: float


class DailyFeelsLike(BaseModel):
    day: float
    night: float
    eve: float
    morn: float


class DailyForecast(BaseModel):
    dt: int
    sunrise: int
    sunset: int
    moonrise: int
    moonset: int
    moon_phase: float
    summary: Optional[str] = None
    temp: DailyTemp
    feels_like: DailyFeelsLike
    humidity: int
    pressure: int
    wind_speed: float
    wind_deg: int
    wind_gust: Optional[float] = None
    weather: list[WeatherCondition]
    clouds: int
    pop: float
    uvi: float
    rain: Optional[float] = None
    snow: Optional[float] = None


class WeatherAlert(BaseModel):
    sender_name: str
    event: str
    start: int
    end: int
    description: str
    tags: list[str]


class WeatherResponse(BaseModel):
    lat: float
    lon: float
    timezone: str
    timezone_offset: int
    current: CurrentWeather


class ForecastResponse(BaseModel):
    lat: float
    lon: float
    timezone: str
    timezone_offset: int
    hourly: list[HourlyForecast]
    daily: list[DailyForecast]


class AlertsResponse(BaseModel):
    lat: float
    lon: float
    timezone: str
    alerts: list[WeatherAlert]


class HistoryEntry(BaseModel):
    dt: int
    temp: float
    humidity: int
    precipitation: float
    weather: list[WeatherCondition]


class HistoryResponse(BaseModel):
    lat: float
    lon: float
    timezone: str
    history: list[HistoryEntry]

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    openweather_api_key: str
    default_lat: float = 40.7128  # New York City
    default_lon: float = -74.0060
    cors_origins: list[str] = ["http://localhost:3000", "http://frontend:3000"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()

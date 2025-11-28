from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    openweather_api_key: str
    default_lat: float = 41.267652  # Omaha, NE
    default_lon: float = -96.1420957
    # Allow all origins for local development/production
    # This enables access via localhost, IP address, or any hostname
    cors_origins: list[str] = ["*"]
    # Backend server port (change if 8000 is already in use)
    backend_port: int = 8000

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()

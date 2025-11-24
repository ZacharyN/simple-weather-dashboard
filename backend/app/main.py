from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routers import weather

settings = get_settings()

app = FastAPI(
    title="Weather Dashboard API",
    description="API proxy for OpenWeather One Call 3.0",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(weather.router, prefix="/weather", tags=["weather"])


@app.get("/health")
async def health_check():
    return {"status": "healthy"}

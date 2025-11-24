# ZNME Weather Dashboard

A clean, modern weather dashboard built with FastAPI and Nuxt 4.

## Features

- Current weather conditions
- 48-hour hourly forecast
- 8-day daily forecast
- Government weather alerts
- 24-hour precipitation history

## Tech Stack

- **Backend**: FastAPI, Python 3.11
- **Frontend**: Nuxt 4, Nuxt UI, Nuxt Icon
- **API**: OpenWeather One Call API 3.0
- **Deployment**: Docker Compose

## Prerequisites

- Docker & Docker Compose
- OpenWeather API key ([Get one here](https://openweathermap.org/api/one-call-3))

## Quick Start

1. **Clone and configure**
   ```bash
   cd weatherDashboard
   cp .env.example .env
   ```

2. **Add your API key**
   Edit `.env` and add your OpenWeather API key:
   ```
   OPENWEATHER_API_KEY=your_api_key_here
   ```

3. **Run with Docker**
   ```bash
   # Production
   docker-compose up -d

   # Development (with hot reload)
   docker-compose -f docker-compose.dev.yml up
   ```

4. **Access the dashboard**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## Development

### Backend (FastAPI)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend (Nuxt 4)

```bash
cd frontend
npm install
npm run dev
```

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /weather/current?lat=&lon=` | Current conditions |
| `GET /weather/forecast?lat=&lon=` | Hourly & daily forecast |
| `GET /weather/alerts?lat=&lon=` | Weather alerts |
| `GET /weather/history?lat=&lon=&hours=24` | Precipitation history |
| `GET /health` | Health check |

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENWEATHER_API_KEY` | Your OpenWeather API key | Required |
| `DEFAULT_LAT` | Default latitude | 40.7128 |
| `DEFAULT_LON` | Default longitude | -74.0060 |
| `NUXT_PUBLIC_API_BASE` | Backend API URL | http://localhost:8000 |

## License

MIT

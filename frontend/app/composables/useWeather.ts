interface WeatherCondition {
  id: number
  main: string
  description: string
  icon: string
}

interface CurrentWeather {
  dt: number
  sunrise: number
  sunset: number
  temp: number
  feels_like: number
  humidity: number
  pressure: number
  uvi: number
  clouds: number
  visibility: number
  wind_speed: number
  wind_deg: number
  wind_gust?: number
  weather: WeatherCondition[]
  rain?: Record<string, number>
  snow?: Record<string, number>
}

interface HourlyForecast {
  dt: number
  temp: number
  feels_like: number
  humidity: number
  pop: number
  weather: WeatherCondition[]
}

interface DailyForecast {
  dt: number
  sunrise: number
  sunset: number
  moonrise: number
  moonset: number
  moon_phase: number
  summary?: string
  temp: {
    day: number
    min: number
    max: number
    night: number
    eve: number
    morn: number
  }
  feels_like: {
    day: number
    night: number
    eve: number
    morn: number
  }
  humidity: number
  pressure: number
  wind_speed: number
  wind_deg: number
  wind_gust?: number
  clouds: number
  weather: WeatherCondition[]
  pop: number
  uvi: number
  rain?: number
  snow?: number
}

interface WeatherAlert {
  sender_name: string
  event: string
  start: number
  end: number
  description: string
  tags: string[]
}

interface HistoryEntry {
  dt: number
  temp: number
  humidity: number
  precipitation: number
  weather: WeatherCondition[]
}

export interface WeatherData {
  current: CurrentWeather | null
  hourly: HourlyForecast[]
  daily: DailyForecast[]
  alerts: WeatherAlert[]
  history: HistoryEntry[]
  timezone: string
}

export function useWeather() {
  // API requests go through Nuxt's proxy at /api
  // The proxy forwards to the backend internally, avoiding mixed content issues
  const apiBase = '/api'

  // Use useState for shared state across components
  const weatherData = useState<WeatherData>('weatherData', () => ({
    current: null,
    hourly: [],
    daily: [],
    alerts: [],
    history: [],
    timezone: ''
  }))

  const loading = useState<boolean>('weatherLoading', () => false)
  const error = useState<string | null>('weatherError', () => null)

  const fetchCurrentWeather = async (lat: number, lon: number) => {
    const response = await $fetch<any>(`${apiBase}/weather/current`, {
      params: { lat, lon }
    })
    weatherData.value.current = response.current
    weatherData.value.timezone = response.timezone
  }

  const fetchForecast = async (lat: number, lon: number) => {
    const response = await $fetch<any>(`${apiBase}/weather/forecast`, {
      params: { lat, lon }
    })
    weatherData.value.hourly = response.hourly
    weatherData.value.daily = response.daily
  }

  const fetchAlerts = async (lat: number, lon: number) => {
    const response = await $fetch<any>(`${apiBase}/weather/alerts`, {
      params: { lat, lon }
    })
    weatherData.value.alerts = response.alerts || []
  }

  const fetchHistory = async (lat: number, lon: number, hours: number = 24) => {
    const response = await $fetch<any>(`${apiBase}/weather/history`, {
      params: { lat, lon, hours }
    })
    weatherData.value.history = response.history || []
  }

  const fetchAllWeatherData = async (lat: number, lon: number) => {
    loading.value = true
    error.value = null

    try {
      await Promise.all([
        fetchCurrentWeather(lat, lon),
        fetchForecast(lat, lon),
        fetchAlerts(lat, lon),
        fetchHistory(lat, lon)
      ])
    } catch (e: any) {
      error.value = e.message || 'Failed to fetch weather data'
      console.error('Weather fetch error:', e)
    } finally {
      loading.value = false
    }
  }

  const getWeatherIconUrl = (icon: string) => {
    return `https://openweathermap.org/img/wn/${icon}@2x.png`
  }

  const formatTemp = (temp: number) => {
    return `${Math.round(temp)}°F`
  }

  const formatTime = (timestamp: number, timezone: string = 'UTC') => {
    return new Date(timestamp * 1000).toLocaleTimeString('en-US', {
      hour: 'numeric',
      minute: '2-digit',
      timeZone: timezone
    })
  }

  const formatDate = (timestamp: number, timezone: string = 'UTC') => {
    return new Date(timestamp * 1000).toLocaleDateString('en-US', {
      weekday: 'short',
      month: 'short',
      day: 'numeric',
      timeZone: timezone
    })
  }

  const formatDay = (timestamp: number, timezone: string = 'UTC') => {
    return new Date(timestamp * 1000).toLocaleDateString('en-US', {
      weekday: 'short',
      timeZone: timezone
    })
  }

  const getWindDirection = (deg: number) => {
    const directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    const index = Math.round(deg / 45) % 8
    return directions[index]
  }

  return {
    weatherData,
    loading,
    error,
    fetchAllWeatherData,
    getWeatherIconUrl,
    formatTemp,
    formatTime,
    formatDate,
    formatDay,
    getWindDirection
  }
}

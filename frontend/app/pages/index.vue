<script setup lang="ts">
const { weatherData, loading, error, fetchAllWeatherData } = useWeather()
const config = useRuntimeConfig()

// Default coordinates from environment variables
const lat = ref(parseFloat(config.public.defaultLat))
const lon = ref(parseFloat(config.public.defaultLon))
const locationName = ref('Default Location')

// Fetch weather data on mount
onMounted(async () => {
  // Try to get user's location
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      async (position) => {
        lat.value = position.coords.latitude
        lon.value = position.coords.longitude
        locationName.value = 'Current Location'
        await fetchAllWeatherData(lat.value, lon.value)
      },
      async () => {
        // Fallback to default location
        await fetchAllWeatherData(lat.value, lon.value)
      }
    )
  } else {
    await fetchAllWeatherData(lat.value, lon.value)
  }
})

const refreshWeather = async () => {
  await fetchAllWeatherData(lat.value, lon.value)
}

const lastUpdated = computed(() => {
  if (weatherData.value.current) {
    return new Date().toLocaleTimeString()
  }
  return ''
})
</script>

<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <UContainer class="py-8">
      <!-- Header -->
      <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between mb-8 gap-4">
        <div>
          <h1 class="text-3xl font-bold text-gray-900 dark:text-white">
            Weather Dashboard
          </h1>
          <p class="text-gray-500 dark:text-gray-400 mt-1">
            {{ locationName }}
            <span v-if="lastUpdated" class="text-sm">
              · Updated {{ lastUpdated }}
            </span>
          </p>
        </div>
        <UButton
          @click="refreshWeather"
          :loading="loading"
          icon="i-heroicons-arrow-path"
          color="primary"
          variant="soft"
        >
          Refresh
        </UButton>
      </div>

      <!-- Loading State -->
      <div v-if="loading && !weatherData.current" class="flex items-center justify-center py-20">
        <UIcon name="i-heroicons-arrow-path" class="w-8 h-8 animate-spin text-primary-500" />
      </div>

      <!-- Error State -->
      <UAlert
        v-else-if="error"
        color="error"
        icon="i-heroicons-exclamation-circle"
        title="Error loading weather data"
        :description="error"
        class="mb-6"
      />

      <!-- Weather Content -->
      <div v-else class="space-y-6">
        <!-- Weather Alerts -->
        <WeatherAlerts />

        <!-- Current Conditions -->
        <CurrentConditions />

        <!-- Hourly Forecast -->
        <HourlyForecast />

        <!-- Two Column Layout for Daily and Precipitation -->
        <div class="grid md:grid-cols-2 gap-6">
          <DailyForecast />
          <PrecipitationHistory />
        </div>
      </div>
    </UContainer>
  </div>
</template>

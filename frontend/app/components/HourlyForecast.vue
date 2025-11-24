<script setup lang="ts">
const { weatherData, getWeatherIconUrl, formatTemp, formatTime } = useWeather()

const hourlyData = computed(() => {
  // Show next 24 hours
  const hours = weatherData.value.hourly.slice(0, 24)
  const current = weatherData.value.current

  if (!current) return hours

  // Get sunrise and sunset times
  const sunrise = current.sunrise
  const sunset = current.sunset

  // Combine hourly data with sunrise/sunset markers
  const combined = [...hours]

  // Insert sunrise marker if it falls within the 24-hour window
  if (sunrise && sunrise >= hours[0].dt && sunrise <= hours[hours.length - 1].dt) {
    const sunriseMarker = { dt: sunrise, type: 'sunrise' }
    const insertIndex = combined.findIndex(h => h.dt > sunrise)
    if (insertIndex !== -1) {
      combined.splice(insertIndex, 0, sunriseMarker)
    } else {
      combined.push(sunriseMarker)
    }
  }

  // Insert sunset marker if it falls within the 24-hour window
  if (sunset && sunset >= hours[0].dt && sunset <= hours[hours.length - 1].dt) {
    const sunsetMarker = { dt: sunset, type: 'sunset' }
    const insertIndex = combined.findIndex(h => h.dt > sunset)
    if (insertIndex !== -1) {
      combined.splice(insertIndex, 0, sunsetMarker)
    } else {
      combined.push(sunsetMarker)
    }
  }

  return combined
})
</script>

<template>
  <UCard v-if="hourlyData.length">
    <template #header>
      <h2 class="text-xl font-semibold">Hourly Forecast</h2>
    </template>

    <div class="overflow-x-auto">
      <div class="flex gap-4 pb-2" style="min-width: max-content;">
        <template v-for="item in hourlyData" :key="item.dt">
          <!-- Sunrise marker -->
          <div
            v-if="item.type === 'sunrise'"
            class="flex flex-col items-center justify-center p-3 rounded-lg bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800/30 min-w-[80px]"
          >
            <div class="text-xs text-amber-700 dark:text-amber-400 mb-1">Sunrise</div>
            <UIcon name="i-wi-sunrise" class="w-12 h-12 text-amber-500" />
            <div class="text-sm font-medium text-amber-700 dark:text-amber-400 mt-1">
              {{ formatTime(item.dt, weatherData.timezone) }}
            </div>
          </div>

          <!-- Sunset marker -->
          <div
            v-else-if="item.type === 'sunset'"
            class="flex flex-col items-center justify-center p-3 rounded-lg bg-orange-50 dark:bg-orange-900/20 border border-orange-200 dark:border-orange-800/30 min-w-[80px]"
          >
            <div class="text-xs text-orange-700 dark:text-orange-400 mb-1">Sunset</div>
            <UIcon name="i-wi-sunset" class="w-12 h-12 text-orange-500" />
            <div class="text-sm font-medium text-orange-700 dark:text-orange-400 mt-1">
              {{ formatTime(item.dt, weatherData.timezone) }}
            </div>
          </div>

          <!-- Regular hourly forecast -->
          <div
            v-else
            class="flex flex-col items-center p-3 rounded-lg bg-gray-50 dark:bg-gray-800 min-w-[80px]"
          >
            <div class="text-sm text-gray-500 dark:text-gray-400">
              {{ formatTime(item.dt, weatherData.timezone) }}
            </div>
            <img
              v-if="item.weather && item.weather[0]"
              :src="getWeatherIconUrl(item.weather[0].icon)"
              :alt="item.weather[0].description"
              class="w-12 h-12"
            />
            <div class="font-medium">{{ formatTemp(item.temp) }}</div>
            <div class="text-xs text-blue-500" v-if="item.pop > 0">
              {{ Math.round(item.pop * 100) }}%
            </div>
          </div>
        </template>
      </div>
    </div>
  </UCard>
</template>

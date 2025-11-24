<script setup lang="ts">
const { weatherData, getWeatherIconUrl, formatTemp, getWindDirection } = useWeather()

const current = computed(() => weatherData.value.current)
</script>

<template>
  <UCard v-if="current">
    <template #header>
      <div class="flex items-center justify-between">
        <h2 class="text-xl font-semibold">Current Conditions</h2>
        <span class="text-sm text-gray-500 dark:text-gray-400">
          {{ new Date(current.dt * 1000).toLocaleTimeString() }}
        </span>
      </div>
    </template>

    <div class="flex flex-col md:flex-row items-center gap-6">
      <!-- Main temp and condition -->
      <div class="flex flex-col items-center md:w-1/3">
        <img
          v-if="current.weather[0]"
          :src="getWeatherIconUrl(current.weather[0].icon)"
          :alt="current.weather[0].description"
          class="w-24 h-24"
        />
        <div class="text-lg text-gray-600 dark:text-gray-300 capitalize -mt-1 mb-3">
          {{ current.weather[0]?.description }}
        </div>
        <div class="text-5xl font-bold">{{ formatTemp(current.temp) }}</div>
        <div class="text-sm text-gray-500 dark:text-gray-400 mt-1">
          Feels like {{ formatTemp(current.feels_like) }}
        </div>
      </div>

      <!-- Weather details grid -->
      <div class="grid grid-cols-2 md:grid-cols-3 gap-3 md:w-2/3">
        <!-- Humidity -->
        <div class="flex flex-col items-center justify-center p-4 rounded-lg bg-gray-50 dark:bg-gray-900/20 border border-gray-100 dark:border-gray-800/30">
          <UIcon name="i-wi-humidity" class="w-8 h-8 text-gray-500 mb-2" />
          <div class="text-xs text-gray-600 dark:text-gray-400 mb-1">Humidity</div>
          <div class="text-lg font-semibold text-gray-900 dark:text-white">{{ current.humidity }}%</div>
        </div>

        <!-- Wind -->
        <div class="flex flex-col items-center justify-center p-4 rounded-lg bg-gray-50 dark:bg-gray-900/20 border border-gray-100 dark:border-gray-800/30">
          <UIcon name="i-wi-strong-wind" class="w-8 h-8 text-gray-500 mb-2" />
          <div class="text-xs text-gray-600 dark:text-gray-400 mb-1">Wind</div>
          <div class="text-lg font-semibold text-gray-900 dark:text-white">
            {{ Math.round(current.wind_speed) }} mph {{ getWindDirection(current.wind_deg) }}
          </div>
        </div>

        <!-- UV Index -->
        <div class="flex flex-col items-center justify-center p-4 rounded-lg bg-gray-50 dark:bg-gray-900/20 border border-gray-100 dark:border-gray-800/30">
          <UIcon name="i-wi-day-sunny" class="w-8 h-8 text-gray-500 mb-2" />
          <div class="text-xs text-gray-600 dark:text-gray-400 mb-1">UV Index</div>
          <div class="text-lg font-semibold text-gray-900 dark:text-white">{{ Math.round(current.uvi) }}</div>
        </div>

        <!-- Visibility -->
        <div class="flex flex-col items-center justify-center p-4 rounded-lg bg-gray-50 dark:bg-gray-900/20 border border-gray-100 dark:border-gray-800/30">
          <UIcon name="i-wi-fog" class="w-8 h-8 text-gray-500 mb-2" />
          <div class="text-xs text-gray-600 dark:text-gray-400 mb-1">Visibility</div>
          <div class="text-lg font-semibold text-gray-900 dark:text-white">{{ Math.round(current.visibility / 1609) }} mi</div>
        </div>

        <!-- Pressure -->
        <div class="flex flex-col items-center justify-center p-4 rounded-lg bg-gray-50 dark:bg-gray-900/20 border border-gray-100 dark:border-gray-800/30">
          <UIcon name="i-wi-barometer" class="w-8 h-8 text-gray-500 mb-2" />
          <div class="text-xs text-gray-600 dark:text-gray-400 mb-1">Pressure</div>
          <div class="text-lg font-semibold text-gray-900 dark:text-white">{{ current.pressure }} hPa</div>
        </div>

        <!-- Clouds -->
        <div class="flex flex-col items-center justify-center p-4 rounded-lg bg-gray-50 dark:bg-gray-900/20 border border-gray-100 dark:border-gray-800/30">
          <UIcon name="i-wi-cloudy" class="w-8 h-8 text-gray-500 mb-2" />
          <div class="text-xs text-gray-600 dark:text-gray-400 mb-1">Clouds</div>
          <div class="text-lg font-semibold text-gray-900 dark:text-white">{{ current.clouds }}%</div>
        </div>
      </div>
    </div>
  </UCard>
</template>

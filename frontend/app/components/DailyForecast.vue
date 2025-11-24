<script setup lang="ts">
const { weatherData, getWeatherIconUrl, formatTemp, formatDay, formatTime, getWindDirection } = useWeather()

const dailyData = computed(() => weatherData.value.daily)
const selectedDay = ref<any>(null)
const isModalOpen = ref(false)

const openDayDetails = (day: any) => {
  selectedDay.value = day
  isModalOpen.value = true
}

const getMoonPhase = (phase: number) => {
  if (phase === 0 || phase === 1) return 'New Moon'
  if (phase < 0.25) return 'Waxing Crescent'
  if (phase === 0.25) return 'First Quarter'
  if (phase < 0.5) return 'Waxing Gibbous'
  if (phase === 0.5) return 'Full Moon'
  if (phase < 0.75) return 'Waning Gibbous'
  if (phase === 0.75) return 'Last Quarter'
  return 'Waning Crescent'
}
</script>

<template>
  <UCard v-if="dailyData.length">
    <template #header>
      <h2 class="text-xl font-semibold">8-Day Forecast</h2>
    </template>

    <div class="space-y-3">
      <div
        v-for="day in dailyData"
        :key="day.dt"
        @click="openDayDetails(day)"
        class="flex items-center justify-between p-3 rounded-lg bg-gray-50 dark:bg-gray-800 hover:bg-gray-100 dark:hover:bg-gray-700 cursor-pointer transition-colors"
      >
        <div class="w-20 font-medium">
          {{ formatDay(day.dt, weatherData.timezone) }}
        </div>

        <div class="flex items-center gap-2">
          <img
            v-if="day.weather[0]"
            :src="getWeatherIconUrl(day.weather[0].icon)"
            :alt="day.weather[0].description"
            class="w-10 h-10"
          />
          <span class="text-sm text-gray-500 dark:text-gray-400 capitalize hidden sm:inline">
            {{ day.weather[0]?.description }}
          </span>
        </div>

        <div class="flex items-center gap-3">
          <span v-if="day.pop > 0" class="text-sm text-blue-500">
            {{ Math.round(day.pop * 100) }}%
          </span>
          <div class="text-right">
            <span class="font-medium">{{ formatTemp(day.temp.max) }}</span>
            <span class="text-gray-400 mx-1">/</span>
            <span class="text-gray-500">{{ formatTemp(day.temp.min) }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal for day details -->
    <UModal v-model:open="isModalOpen">
      <template #content>
        <UCard v-if="selectedDay">
          <template #header>
            <div class="flex flex-col items-center text-center">
              <img
                v-if="selectedDay.weather[0]"
                :src="getWeatherIconUrl(selectedDay.weather[0].icon)"
                :alt="selectedDay.weather[0].description"
                class="w-20 h-20"
              />
              <div class="text-lg text-gray-600 dark:text-gray-300 capitalize -mt-1 mb-2">
                {{ selectedDay.weather[0]?.description }}
              </div>
              <div class="font-semibold text-2xl mb-1">
                {{ new Date(selectedDay.dt * 1000).toLocaleDateString('en-US', { weekday: 'long', month: 'short', day: 'numeric' }) }}
              </div>
              <div class="text-3xl font-bold mb-2">
                {{ formatTemp(selectedDay.temp.max) }} / {{ formatTemp(selectedDay.temp.min) }}
              </div>
            </div>
          </template>

          <!-- Summary if available -->
          <p v-if="selectedDay.summary" class="text-sm text-gray-600 dark:text-gray-300 mb-4 text-center">
            {{ selectedDay.summary }}
          </p>

          <!-- Temperature Throughout Day -->
          <div class="mb-4 grid grid-cols-4 gap-2">
            <div class="flex flex-col items-center p-3 rounded-lg bg-gray-50 dark:bg-gray-900/20 border border-gray-100 dark:border-gray-800/30">
              <div class="text-xs text-gray-600 dark:text-gray-400 mb-1">Morning</div>
              <div class="text-sm font-semibold text-gray-900 dark:text-white">{{ formatTemp(selectedDay.temp.morn) }}</div>
            </div>
            <div class="flex flex-col items-center p-3 rounded-lg bg-gray-50 dark:bg-gray-900/20 border border-gray-100 dark:border-gray-800/30">
              <div class="text-xs text-gray-600 dark:text-gray-400 mb-1">Day</div>
              <div class="text-sm font-semibold text-gray-900 dark:text-white">{{ formatTemp(selectedDay.temp.day) }}</div>
            </div>
            <div class="flex flex-col items-center p-3 rounded-lg bg-gray-50 dark:bg-gray-900/20 border border-gray-100 dark:border-gray-800/30">
              <div class="text-xs text-gray-600 dark:text-gray-400 mb-1">Evening</div>
              <div class="text-sm font-semibold text-gray-900 dark:text-white">{{ formatTemp(selectedDay.temp.eve) }}</div>
            </div>
            <div class="flex flex-col items-center p-3 rounded-lg bg-gray-50 dark:bg-gray-900/20 border border-gray-100 dark:border-gray-800/30">
              <div class="text-xs text-gray-600 dark:text-gray-400 mb-1">Night</div>
              <div class="text-sm font-semibold text-gray-900 dark:text-white">{{ formatTemp(selectedDay.temp.night) }}</div>
            </div>
          </div>

          <!-- Weather Details -->
          <div class="grid grid-cols-2 md:grid-cols-3 gap-3">
            <!-- Humidity -->
            <div class="flex flex-col items-center justify-center p-4 rounded-lg bg-gray-50 dark:bg-gray-900/20 border border-gray-100 dark:border-gray-800/30">
              <UIcon name="i-wi-humidity" class="w-8 h-8 text-gray-500 mb-2" />
              <div class="text-xs text-gray-600 dark:text-gray-400 mb-1">Humidity</div>
              <div class="text-lg font-semibold text-gray-900 dark:text-white">{{ selectedDay.humidity }}%</div>
            </div>

            <!-- Wind -->
            <div class="flex flex-col items-center justify-center p-4 rounded-lg bg-gray-50 dark:bg-gray-900/20 border border-gray-100 dark:border-gray-800/30">
              <UIcon name="i-wi-strong-wind" class="w-8 h-8 text-gray-500 mb-2" />
              <div class="text-xs text-gray-600 dark:text-gray-400 mb-1">Wind</div>
              <div class="text-lg font-semibold text-gray-900 dark:text-white">
                {{ Math.round(selectedDay.wind_speed) }} mph {{ getWindDirection(selectedDay.wind_deg) }}
              </div>
            </div>

            <!-- UV Index -->
            <div class="flex flex-col items-center justify-center p-4 rounded-lg bg-gray-50 dark:bg-gray-900/20 border border-gray-100 dark:border-gray-800/30">
              <UIcon name="i-wi-day-sunny" class="w-8 h-8 text-gray-500 mb-2" />
              <div class="text-xs text-gray-600 dark:text-gray-400 mb-1">UV Index</div>
              <div class="text-lg font-semibold text-gray-900 dark:text-white">{{ Math.round(selectedDay.uvi) }}</div>
            </div>

            <!-- Pressure -->
            <div class="flex flex-col items-center justify-center p-4 rounded-lg bg-gray-50 dark:bg-gray-900/20 border border-gray-100 dark:border-gray-800/30">
              <UIcon name="i-wi-barometer" class="w-8 h-8 text-gray-500 mb-2" />
              <div class="text-xs text-gray-600 dark:text-gray-400 mb-1">Pressure</div>
              <div class="text-lg font-semibold text-gray-900 dark:text-white">{{ selectedDay.pressure }} hPa</div>
            </div>

            <!-- Clouds -->
            <div class="flex flex-col items-center justify-center p-4 rounded-lg bg-gray-50 dark:bg-gray-900/20 border border-gray-100 dark:border-gray-800/30">
              <UIcon name="i-wi-cloudy" class="w-8 h-8 text-gray-500 mb-2" />
              <div class="text-xs text-gray-600 dark:text-gray-400 mb-1">Clouds</div>
              <div class="text-lg font-semibold text-gray-900 dark:text-white">{{ selectedDay.clouds }}%</div>
            </div>

            <!-- Precipitation Chance -->
            <div v-if="selectedDay.pop > 0" class="flex flex-col items-center justify-center p-4 rounded-lg bg-gray-50 dark:bg-gray-900/20 border border-gray-100 dark:border-gray-800/30">
              <UIcon name="i-wi-raindrops" class="w-8 h-8 text-gray-500 mb-2" />
              <div class="text-xs text-gray-600 dark:text-gray-400 mb-1">Precip Chance</div>
              <div class="text-lg font-semibold text-gray-900 dark:text-white">{{ Math.round(selectedDay.pop * 100) }}%</div>
            </div>
          </div>

          <!-- Sun & Moon -->
          <div class="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
            <div class="grid grid-cols-2 gap-3">
              <div class="flex flex-col items-center p-3 rounded-lg bg-gray-50 dark:bg-gray-900/20">
                <div class="text-xs text-gray-600 dark:text-gray-400 mb-2">Sunrise / Sunset</div>
                <div class="flex items-center gap-2 mb-1">
                  <UIcon name="i-wi-sunrise" class="w-5 h-5 text-amber-500" />
                  <span class="text-sm font-medium">{{ formatTime(selectedDay.sunrise, weatherData.timezone) }}</span>
                </div>
                <div class="flex items-center gap-2">
                  <UIcon name="i-wi-sunset" class="w-5 h-5 text-orange-500" />
                  <span class="text-sm font-medium">{{ formatTime(selectedDay.sunset, weatherData.timezone) }}</span>
                </div>
              </div>
              <div class="flex flex-col items-center justify-center p-3 rounded-lg bg-gray-50 dark:bg-gray-900/20">
                <UIcon name="i-wi-moon-alt-waxing-crescent-3" class="w-8 h-8 text-gray-500 mb-2" />
                <div class="text-xs text-gray-600 dark:text-gray-400 mb-1">Moon Phase</div>
                <div class="text-sm font-medium">{{ getMoonPhase(selectedDay.moon_phase) }}</div>
              </div>
            </div>
          </div>
        </UCard>
      </template>
    </UModal>
  </UCard>
</template>

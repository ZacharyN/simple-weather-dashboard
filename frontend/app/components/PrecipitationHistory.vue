<script setup lang="ts">
const { weatherData, formatTime } = useWeather()

const historyData = computed(() => weatherData.value.history)

const maxPrecipitation = computed(() => {
  const values = historyData.value.map(h => h.precipitation)
  return Math.max(...values, 0.1) // Min 0.1 to avoid division by zero
})

const totalPrecipitation = computed(() => {
  return historyData.value.reduce((sum, h) => sum + h.precipitation, 0)
})
</script>

<template>
  <UCard v-if="historyData.length">
    <template #header>
      <div class="flex items-center justify-between">
        <h2 class="text-xl font-semibold">Precipitation History</h2>
        <span class="text-sm text-gray-500 dark:text-gray-400">
          Past 24 hours: {{ totalPrecipitation.toFixed(2) }}" total
        </span>
      </div>
    </template>

    <div v-if="totalPrecipitation === 0" class="text-center py-8 text-gray-500 dark:text-gray-400">
      <UIcon name="i-heroicons-sun" class="w-12 h-12 mx-auto mb-2" />
      <p>No precipitation in the past 24 hours</p>
    </div>

    <div v-else class="space-y-2">
      <div
        v-for="entry in historyData.filter(h => h.precipitation > 0)"
        :key="entry.dt"
        class="flex items-center gap-3"
      >
        <div class="w-20 text-sm text-gray-500 dark:text-gray-400">
          {{ formatTime(entry.dt, weatherData.timezone) }}
        </div>
        <div class="flex-1 h-4 bg-gray-100 dark:bg-gray-800 rounded-full overflow-hidden">
          <div
            class="h-full bg-blue-500 rounded-full"
            :style="{ width: `${(entry.precipitation / maxPrecipitation) * 100}%` }"
          />
        </div>
        <div class="w-16 text-sm text-right">
          {{ entry.precipitation.toFixed(2) }}"
        </div>
      </div>
    </div>
  </UCard>
</template>

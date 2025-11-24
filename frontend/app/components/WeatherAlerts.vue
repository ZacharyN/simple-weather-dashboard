<script setup lang="ts">
const { weatherData } = useWeather()

const alerts = computed(() => weatherData.value.alerts)

const getAlertColor = (event: string) => {
  const eventLower = event.toLowerCase()
  if (eventLower.includes('warning') || eventLower.includes('severe')) {
    return 'error'
  }
  if (eventLower.includes('watch') || eventLower.includes('advisory')) {
    return 'warning'
  }
  return 'info'
}

const formatAlertTime = (timestamp: number) => {
  return new Date(timestamp * 1000).toLocaleString('en-US', {
    weekday: 'short',
    month: 'short',
    day: 'numeric',
    hour: 'numeric',
    minute: '2-digit'
  })
}
</script>

<template>
  <div v-if="alerts.length" class="space-y-3">
    <UAlert
      v-for="(alert, index) in alerts"
      :key="index"
      :color="getAlertColor(alert.event)"
      icon="i-heroicons-exclamation-triangle"
      :title="alert.event"
    >
      <template #description>
        <div class="space-y-2">
          <p class="text-sm">{{ alert.description.slice(0, 300) }}{{ alert.description.length > 300 ? '...' : '' }}</p>
          <div class="text-xs text-gray-500 dark:text-gray-400">
            <span>{{ formatAlertTime(alert.start) }}</span>
            <span class="mx-2">to</span>
            <span>{{ formatAlertTime(alert.end) }}</span>
          </div>
          <div class="text-xs text-gray-500 dark:text-gray-400">
            Source: {{ alert.sender_name }}
          </div>
        </div>
      </template>
    </UAlert>
  </div>
</template>

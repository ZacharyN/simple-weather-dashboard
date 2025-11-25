export default defineNuxtConfig({
  modules: [
    '@nuxt/ui',
    '@nuxt/icon'
  ],

  css: ['~/assets/css/main.css'],

  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:8000',
      defaultLat: process.env.NUXT_PUBLIC_DEFAULT_LAT || '41.267652',
      defaultLon: process.env.NUXT_PUBLIC_DEFAULT_LON || '-96.1420957'
    }
  },

  devtools: { enabled: true },

  compatibilityDate: '2024-11-01'
})

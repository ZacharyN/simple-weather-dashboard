export default defineNuxtConfig({
  modules: [
    '@nuxt/ui',
    '@nuxt/icon'
  ],

  css: ['~/assets/css/main.css'],

  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:8000'
    }
  },

  devtools: { enabled: true },

  compatibilityDate: '2024-11-01'
})

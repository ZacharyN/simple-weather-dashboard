export default defineNuxtConfig({
  modules: [
    '@nuxt/ui',
    '@nuxt/icon'
  ],

  css: ['~/assets/css/main.css'],

  // Bundle icons at build time to avoid /api/_nuxt_icon conflicts with backend proxy
  icon: {
    clientBundle: {
      scan: true,
      sizeLimitKb: 512
    }
  },

  runtimeConfig: {
    // Private config (server-side only) - used for proxying
    backendUrl: process.env.BACKEND_URL || 'http://localhost:8000',
    public: {
      defaultLat: process.env.NUXT_PUBLIC_DEFAULT_LAT || '41.267652',
      defaultLon: process.env.NUXT_PUBLIC_DEFAULT_LON || '-96.1420957'
    }
  },

  // Proxy API requests to backend - enables single-proxy homelab deployment
  nitro: {
    routeRules: {
      '/api/**': {
        proxy: `${process.env.BACKEND_URL || 'http://localhost:8000'}/**`
      }
    }
  },

  devtools: { enabled: true },

  compatibilityDate: '2024-11-01'
})

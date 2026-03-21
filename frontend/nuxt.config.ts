// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: {
    enabled: true,

    timeline: {
      enabled: true,
    },
  },
    runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE
    }
  },
  routeRules: {
    '/api/**': {
      proxy: 'http://backend:8000/api/**'
    }
  },
  // css: ['~/assets/css/main.css'],
  modules: ['@nuxtjs/tailwindcss', '@nuxt/eslint', '@nuxtjs/color-mode', 'nuxt-bootstrap-icons'],
  colorMode: {
    classSuffix: '' // Isto faz com que ele use a classe 'dark' em vez de 'dark-mode'
  },
    tailwindcss: {
    cssPath: '~/assets/css/tailwind.css',
    configPath: 'tailwind.config',
    exposeConfig: false,
    viewer: true,
  }
})
<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 md:py-12">
    
    <div v-if="userPending" class="animate-pulse space-y-8">
      <div class="space-y-3">
        <div class="h-8 bg-slate-200 dark:bg-slate-700 rounded-lg w-1/4"></div>
        <div class="h-4 bg-slate-200 dark:bg-slate-700 rounded-lg w-2/4"></div>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div v-for="i in 3" :key="i" class="h-32 bg-slate-200 dark:bg-slate-700 rounded-xl"></div>
      </div>
    </div>
    
    <div v-else-if="userData" class="space-y-8">
      
      <header class="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-200 dark:border-slate-800 pb-6">
        <div>
          <h1 class="text-2xl md:text-3xl font-bold text-slate-900 dark:text-white flex items-center gap-2">
            Olá, {{ userData.first_name }}
          </h1>
          <p class="text-sm md:text-base text-slate-500 dark:text-slate-400 mt-1">
            Bem-vindo ao seu portal do residente. Resumo das suas actividades.
          </p>
        </div>
        
        <div class="flex items-center gap-3">
          <div class="text-right hidden md:block">
            <p class="text-sm font-medium text-slate-900 dark:text-white">{{ userData.first_name }} {{ userData.last_name }}</p>
            <NuxtLink to="/dashboard/student/me/security" class="text-xs text-blue-600 dark:text-blue-400 hover:underline">
              Gerir Segurança
            </NuxtLink>
          </div>
          <div class="h-12 w-12 rounded-full bg-blue-100 dark:bg-blue-900/50 text-blue-700 dark:text-blue-300 flex items-center justify-center text-lg font-bold border border-blue-200 dark:border-blue-800">
            {{ getIniciais(userData.first_name, userData.last_name) }}
          </div>
        </div>
      </header>

      <section class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-1 gap-6">
        
        <NuxtLink to="/dashboard/student/me" class="group bg-white dark:bg-slate-900 rounded-xl p-6 border border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-md hover:border-blue-300 dark:hover:border-blue-700 transition-all duration-200 flex flex-col h-full">
          <div class="h-10 w-10 rounded-lg bg-slate-100 dark:bg-slate-800 flex items-center justify-center text-slate-600 dark:text-slate-300 mb-4 group-hover:bg-blue-50 group-hover:text-blue-600 dark:group-hover:bg-blue-900/30 transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg>
          </div>
          <h2 class="text-lg font-semibold text-slate-900 dark:text-white mb-2">Dossiê Pessoal</h2>
          <p class="text-sm text-slate-500 dark:text-slate-400 flex-grow">Consulte os seus dados pessoais, informações do encarregado e registo de presenças.</p>
          <div class="mt-4 text-sm font-medium text-blue-600 dark:text-blue-400 flex items-center gap-1 group-hover:translate-x-1 transition-transform">
            Aceder Perfil <span aria-hidden="true">&rarr;</span>
          </div>
        </NuxtLink>

      </section>

    </div>
  </div>
</template>

<script setup lang="ts">
import { inject, type Ref } from 'vue'

interface UserData {
  id: number
  email: string
  first_name: string
  last_name: string
}

// Assumindo que estes dados vêm do layout pai (Dashboard Layout)
const userData = inject<Ref<UserData | null>>('userData')
const userPending = inject<Ref<boolean>>('pendingData')

const getIniciais = (first: string, last: string) => {
  return (first?.[0] || '') + (last?.[0] || '').toUpperCase()
}
</script>
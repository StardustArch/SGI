<template>
  <div class="max-w-7xl mx-auto p-4 md:p-8 min-h-[80vh] flex flex-col justify-center">
    
    <div v-if="userPending" class="space-y-8 animate-pulse">
      <div class="h-12 bg-gray-200 dark:bg-gray-700 rounded-2xl w-1/3"></div>
      <div class="h-6 bg-gray-200 dark:bg-gray-700 rounded-xl w-2/3"></div>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div v-for="n in 4" :key="n" class="h-48 bg-gray-200 dark:bg-gray-700 rounded-[2rem]"></div>
      </div>
    </div>
    
    <div v-else-if="userData" class="space-y-10">
      
      <div class="relative">
        <h1 class="text-4xl md:text-5xl font-extrabold tracking-tight text-gray-900 dark:text-white mb-4">
          Olá, <span class="text-transparent bg-clip-text bg-gradient-to-r from-rose-500 to-orange-500">{{ userData.first_name }}!</span> 👋
        </h1>
        <p class="text-xl text-stone-500 dark:text-gray-400 max-w-2xl leading-relaxed">
          Bem-vindo ao seu portal do estudante. O que deseja tratar hoje?
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 xl:grid-cols-4 gap-6">
        
        <NuxtLink to="/dashboard/student/finance" class="group nav-card">
          <div class="card-icon-bg bg-emerald-50 text-emerald-600 dark:bg-emerald-900/20 dark:text-emerald-400">
            <BootstrapIcon name="wallet2" class="w-8 h-8" />
          </div>
          <div>
            <h3 class="card-title group-hover:text-emerald-600 transition-colors">Financeiro</h3>
            <p class="card-desc">Mensalidades e pagamentos.</p>
          </div>
          <div class="absolute top-6 right-6 opacity-0 group-hover:opacity-100 transition-all transform group-hover:translate-x-1 text-emerald-500">
            <BootstrapIcon name="arrow-right" class="w-6 h-6" />
          </div>
        </NuxtLink>

        <NuxtLink to="/dashboard/student/exits" class="group nav-card">
          <div class="card-icon-bg bg-rose-50 text-rose-600 dark:bg-rose-900/20 dark:text-rose-400">
            <BootstrapIcon name="door-open" class="w-8 h-8" />
          </div>
          <div>
            <h3 class="card-title group-hover:text-rose-600 transition-colors">Pedidos de Saída</h3>
            <p class="card-desc">Solicitar e consultar autorizações.</p>
          </div>
          <div class="absolute top-6 right-6 opacity-0 group-hover:opacity-100 transition-all transform group-hover:translate-x-1 text-rose-500">
            <BootstrapIcon name="arrow-right" class="w-6 h-6" />
          </div>
        </NuxtLink>

        <NuxtLink to="/dashboard/student/attendance" class="group nav-card">
          <div class="card-icon-bg bg-violet-50 text-violet-600 dark:bg-violet-900/20 dark:text-violet-400">
            <BootstrapIcon name="calendar-check" class="w-8 h-8" />
          </div>
          <div>
            <h3 class="card-title group-hover:text-violet-600 transition-colors">Presenças</h3>
            <p class="card-desc">Histórico de assiduidade.</p>
          </div>
          <div class="absolute top-6 right-6 opacity-0 group-hover:opacity-100 transition-all transform group-hover:translate-x-1 text-violet-500">
            <BootstrapIcon name="arrow-right" class="w-6 h-6" />
          </div>
        </NuxtLink>

        <NuxtLink to="/dashboard/student/discipline" class="group nav-card">
          <div class="card-icon-bg bg-amber-50 text-amber-600 dark:bg-amber-900/20 dark:text-amber-400">
            <BootstrapIcon name="shield-exclamation" class="w-8 h-8" />
          </div>
          <div>
            <h3 class="card-title group-hover:text-amber-600 transition-colors">Disciplina</h3>
            <p class="card-desc">Ocorrências e comportamento.</p>
          </div>
          <div class="absolute top-6 right-6 opacity-0 group-hover:opacity-100 transition-all transform group-hover:translate-x-1 text-amber-500">
            <BootstrapIcon name="arrow-right" class="w-6 h-6" />
          </div>
        </NuxtLink>

      </div>
      
      <div class="pt-8 border-t border-stone-100 dark:border-gray-700">
         <NuxtLink to="/dashboard/student/me" class="inline-flex items-center gap-2 text-sm font-bold text-stone-400 hover:text-rose-500 transition-colors">
            <BootstrapIcon name="person-circle" />
            Gerir o meu perfil e senha
         </NuxtLink>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import { inject, type Ref } from 'vue'

interface UserData {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  perfil: number;
}

const userData = inject<Ref<UserData | null>>('userData')
const userPending = inject<Ref<boolean>>('pendingData')
</script>

<style scoped>
/* Estilos Base dos Cartões */
.nav-card {
  @apply relative bg-white dark:bg-gray-800 rounded-[2rem] p-8 
         border border-stone-100 dark:border-gray-700 shadow-sm 
         hover:shadow-xl hover:-translate-y-2 transition-all duration-300 ease-out
         flex flex-col gap-6 cursor-pointer overflow-hidden;
}

/* Ícone com Fundo Colorido */
.card-icon-bg {
  @apply w-16 h-16 rounded-2xl flex items-center justify-center mb-2 transition-transform duration-300 group-hover:scale-110;
}

/* Tipografia */
.card-title {
  @apply text-xl font-bold text-gray-800 dark:text-white mb-2;
}

.card-desc {
  @apply text-sm text-stone-500 dark:text-gray-400 font-medium leading-relaxed;
}
</style>
<template>
  <div>
    <div v-if="userPending" class="dark:text-gray-300">
      A carregar dados...
    </div>
    
    <div v-else-if="userData" class="space-y-6">
      <h1 class="text-3xl font-bold dark:text-white">
        Olá, {{ userData.first_name }}!
      </h1>
      <p class="text-lg text-gray-600 dark:text-gray-400">
        Bem-vindo ao seu portal de Encarregado de Educação. Selecione uma ação abaixo.
      </p>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        
        <NuxtLink to="/dashboard/foreman/students" class="action-card">
          <BootstrapIcon name="people-fill" class="w-8 h-8 mb-2 text-blue-500" />
          <span class="font-semibold dark:text-white">Meus Educandos</span>
          <span class="text-sm text-gray-500 dark:text-gray-400">Ver a lista dos seus educandos.</span>
        </NuxtLink>

        <NuxtLink to="/dashboard/foreman/financas" class="action-card">
          <BootstrapIcon name="cash-coin" class="w-8 h-8 mb-2 text-blue-500" />
          <span class="font-semibold dark:text-white">Hist. Financeiro</span>
          <span class="text-sm text-gray-500 dark:text-gray-400">Ver pagamentos dos seus educandos.</span>
        </NuxtLink>
        
        <NuxtLink to="/dashboard/foreman/pedidos" class="action-card">
          <BootstrapIcon name="arrow-up-circle-fill" class="w-8 h-8 mb-2 text-blue-500" />
          <span class="font-semibold dark:text-white">Pedidos de Saída</span>
          <span class="text-sm text-gray-500 dark:text-gray-400">Ver os pedidos de saída.</span>
        </NuxtLink>

        <NuxtLink to="/dashboard/foreman/presencas" class="action-card">
          <BootstrapIcon name="calendar-check-fill" class="w-8 h-8 mb-2 text-blue-500" />
          <span class="font-semibold dark:text-white">Hist. Presenças</span>
          <span class="text-sm text-gray-500 dark:text-gray-400">Ver assiduidade nos estudos.</span>
        </NuxtLink>

      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { inject, type Ref } from 'vue'

// Definir os tipos para o Typescript
interface UserData {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  perfil: number;
}

// "Injecta" os dados fornecidos pelo "Pai" (dashboard.vue)
const userData = inject<Ref<UserData | null>>('userData')
const userPending = inject<Ref<boolean>>('pendingData') // O 'pai' fornece 'pendingData'
</script>

<style scoped>
/* Estilo para os cartões de ação rápida */
.action-card {
  @apply flex flex-col items-center justify-center p-6 bg-white dark:bg-gray-800 rounded-lg shadow-md transition-transform transform hover:-translate-y-1 hover:shadow-lg;
}
</style>
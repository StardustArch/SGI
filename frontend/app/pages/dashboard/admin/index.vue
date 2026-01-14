<template>
  <div>
    <div v-if="userPending" class="dark:text-gray-300">
      A carregar dados...
    </div>
    
    <div v-else-if="userData?.perfil === 1" class="space-y-6">
      <h1 class="text-3xl font-bold dark:text-white">
        Olá, {{ userData.first_name }}!
      </h1>
      <p class="text-lg text-gray-600 dark:text-gray-400">
        Bem-vindo ao Painel de Administrador. Selecione uma ação rápida abaixo ou use o menu lateral.
      </p>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        
        <NuxtLink to="/dashboard/admin/reports" class="action-card">
          <BootstrapIcon name="bar-chart-line-fill" class="w-8 h-8 mb-2 text-blue-500" />
          <span class="font-semibold dark:text-white">Ver Relatórios</span>
          <span class="text-sm text-gray-500 dark:text-gray-400">Sumário financeiro e disciplinar.</span>
        </NuxtLink>
        
        <NuxtLink to="/dashboard/admin/estudantes" class="action-card">
          <BootstrapIcon name="people-fill" class="w-8 h-8 mb-2 text-blue-500" />
          <span class="font-semibold dark:text-white">Gerir Estudantes</span>
          <span class="text-sm text-gray-500 dark:text-gray-400">Registar ou editar perfis.</span>
        </NuxtLink>

        </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { inject, type Ref, watchEffect, ref } from 'vue' // Adicionámos 'watchEffect' e 'ref'
import { useRouter } from 'vue-router' // Adicionámos 'useRouter'

// Definir os tipos para o Typescript
interface UserData {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  perfil: number; // 1: Admin, 2: Estudante, 3: Encarregado
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
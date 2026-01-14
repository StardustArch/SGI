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
        Bem-vindo ao seu portal de estudante. Use os links laterais para ver o seu histórico ou submeter pedidos.
      </p>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        
          <NuxtLink to="/dashboard/student/financas" class="action-card">
            <BootstrapIcon name="cash-coin" class="w-8 h-8 mb-2 text-blue-500" />
            <span class="font-semibold dark:text-white">Hist. Financeiro</span>
            <span class="text-sm text-gray-500 dark:text-gray-400">Ver as suas mensalidades.</span>
          </NuxtLink>
          <NuxtLink to="/dashboard/student/disciplina" class="action-card">
            <BootstrapIcon name="info-circle-fill" class="w-8 h-8 mb-2 text-blue-500" />
            <span class="font-semibold dark:text-white">Hist. Disciplinar</span>
            <span class="text-sm text-gray-500 dark:text-gray-400">Ver as suas sanções.</span>
          </NuxtLink>

                    <NuxtLink to="/dashboard/student/presencas" class="action-card">
            <BootstrapIcon name="calendar-check-fill" class="w-8 h-8 mb-2 text-blue-500" />

            <span class="font-semibold dark:text-white">Hist. Presenças</span>
            <span class="text-sm text-gray-500 dark:text-gray-400">Ver as suas presenças.</span>
          </NuxtLink>
        <NuxtLink to="/dashboard/student/pedidos" class="action-card">
          <BootstrapIcon name="arrow-up-circle-fill" class="w-8 h-8 mb-2 text-blue-500" />
          <span class="font-semibold dark:text-white">Pedidos de Saída</span>
          <span class="text-sm text-gray-500 dark:text-gray-400">Submeter ou ver os seus pedidos.</span>
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
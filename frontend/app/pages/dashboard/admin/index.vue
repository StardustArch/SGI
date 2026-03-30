<template>
  <div class="space-y-8 dark:text-white max-w-8xl mx-auto p-4 md:p-8">
    
    <header class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
      <div>
        <h1 class="text-4xl font-black text-gray-900 dark:text-white tracking-tighter">
          Dashboard <span class="text-rose-500">{{ user?.perfil_nome }}</span>
        </h1>
        <p class="text-stone-500 dark:text-gray-400 font-medium">
          {{ pending ? 'A sincronizar dados...' : 'Visão geral do ecossistema do internato.' }}
        </p>
      </div>
      
      <button 
        @click="refresh()" 
        :disabled="pending"
        class="flex items-center gap-2 px-5 py-2.5 bg-white dark:bg-gray-800 border border-stone-200 dark:border-gray-700 rounded-2xl shadow-sm hover:bg-stone-50 transition-all active:scale-95 disabled:opacity-50"
      >
        <BootstrapIcon name="arrow-clockwise" :class="{ 'animate-spin': pending }" class="w-5 h-5" />
        <span class="text-sm font-bold">Actualizar</span>
      </button>
    </header>

    <div v-if="error" class="p-6 bg-rose-50 border border-rose-100 rounded-[2rem] flex flex-col items-center text-center space-y-3">
      <BootstrapIcon name="exclamation-triangle-fill" class="text-rose-500 w-12 h-12" />
      <h3 class="font-bold text-rose-800">Falha na ligação com o servidor</h3>
      <p class="text-rose-600 text-sm">Não conseguimos recuperar os indicadores de gestão neste momento.</p>
    </div>

    <div v-if="pending" class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div v-for="i in 3" :key="i" class="h-32 bg-stone-100 dark:bg-gray-800 animate-pulse rounded-[2rem]"></div>
      <div class="md:col-span-3 h-64 bg-stone-50 dark:bg-gray-800/50 animate-pulse rounded-[2rem]"></div>
    </div>

    <div v-else-if="dashboard" class="space-y-10 animate-in fade-in slide-in-from-bottom-4 duration-700">
      
      <!-- Dados Administrativos (Gestor/Suporte) -->
      <section v-if="dashboard.administrative" class="space-y-4">
        <h2 class="text-sm font-black uppercase tracking-widest text-stone-400 flex items-center gap-2">
          <BootstrapIcon name="buildings" /> Gestão de Capacidade
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <!-- Card Alunos Activos -->
          <div class="bg-white dark:bg-gray-800 p-6 rounded-[2rem] border border-stone-100 dark:border-gray-700 shadow-sm">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-stone-500 text-xs font-bold uppercase">Alunos Activos</p>
                <h3 class="text-3xl font-black">{{ dashboard.administrative.total_estudantes_ativos || 0 }}</h3>
              </div>
              <BootstrapIcon name="people-fill" class="text-blue-500 text-3xl" />
            </div>
          </div>

          <!-- Card Ocupação (calculada) -->
          <div class="bg-white dark:bg-gray-800 p-6 rounded-[2rem] border border-stone-100 dark:border-gray-700 shadow-sm">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-stone-500 text-xs font-bold uppercase">Ocupação</p>
                <h3 class="text-3xl font-black">
                  {{ ocupacaoPercent }}%
                </h3>
                <p class="text-xs text-stone-400">{{ dashboard.administrative.total_ocupadas }}/{{ dashboard.administrative.total_vagas }} camas</p>
              </div>
              <BootstrapIcon name="door-closed-fill" :class="ocupacaoPercent > 90 ? 'text-rose-500' : 'text-emerald-500'" class="text-3xl" />
            </div>
          </div>

          <!-- Card Pedidos Pendentes -->
          <div class="bg-white dark:bg-gray-800 p-6 rounded-[2rem] border border-stone-100 dark:border-gray-700 shadow-sm">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-stone-500 text-xs font-bold uppercase">Pedidos Pendentes</p>
                <h3 class="text-3xl font-black">{{ dashboard.administrative.pedidos_saida_pendentes || 0 }}</h3>
              </div>
              <BootstrapIcon name="clock-history" class="text-orange-500 text-3xl" />
            </div>
            <NuxtLink to="/dashboard/admin/exits" class="text-xs text-rose-500 hover:underline mt-2 block">Ver todos</NuxtLink>
          </div>
        </div>
      </section>

      <!-- Dados Financeiros (Financeiro/Suporte) -->
      <section v-if="dashboard.finance" class="space-y-4">
        <h2 class="text-sm font-black uppercase tracking-widest text-stone-400 flex items-center gap-2">
          <BootstrapIcon name="cash-stack" /> Saúde Financeira (Mês Actual)
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div class="bg-white dark:bg-gray-800 p-6 rounded-[2rem] border border-stone-100 dark:border-gray-700 shadow-sm">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-stone-500 text-xs font-bold uppercase">Arrecadado</p>
                <h3 class="text-3xl font-black text-emerald-600">{{ formatMoeda(dashboard.finance.total_arrecadado_mes || 0) }}</h3>
              </div>
              <BootstrapIcon name="cash-coin" class="text-emerald-500 text-3xl" />
            </div>
          </div>
          <div class="bg-white dark:bg-gray-800 p-6 rounded-[2rem] border border-stone-100 dark:border-gray-700 shadow-sm">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-stone-500 text-xs font-bold uppercase">Pendentes</p>
                <h3 class="text-3xl font-black">{{ dashboard.finance.total_estudantes_pendentes || 0 }}</h3>
              </div>
              <BootstrapIcon name="hourglass-split" class="text-amber-500 text-3xl" />
            </div>
          </div>
          <div class="bg-white dark:bg-gray-800 p-6 rounded-[2rem] border border-stone-100 dark:border-gray-700 shadow-sm">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-stone-500 text-xs font-bold uppercase">Em Atraso</p>
                <h3 class="text-3xl font-black text-rose-500">{{ dashboard.finance.total_estudantes_atraso || 0 }}</h3>
              </div>
              <BootstrapIcon name="exclamation-triangle" class="text-rose-500 text-3xl" />
            </div>
          </div>
        </div>
      </section>

      <!-- Dados Disciplinares (Disciplinar/Suporte) -->
      <section v-if="dashboard.discipline" class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div class="bg-white dark:bg-gray-800 p-8 rounded-[2.5rem] border border-stone-100 dark:border-gray-700 shadow-sm">
          <div class="flex justify-between items-center mb-6">
            <h3 class="font-bold text-xl flex items-center gap-2">
              <BootstrapIcon name="shield-exclamation" class="text-rose-500" /> Top Infratores
            </h3>
            <span class="text-xs font-bold text-stone-400">Últimos 30 dias</span>
          </div>
          <div v-if="dashboard.discipline.top_infratores?.length" class="space-y-4">
            <div v-for="inf in dashboard.discipline.top_infratores" :key="inf.estudante_id" class="flex justify-between items-center p-4 bg-stone-50 dark:bg-gray-700/50 rounded-2xl">
              <span class="font-medium">{{ inf.estudante__nome_completo }}</span>
              <span class="px-3 py-1 bg-rose-100 text-rose-600 rounded-lg text-xs font-black">{{ inf.total }} Sanções</span>
            </div>
          </div>
          <p v-else class="text-stone-400 text-sm">Nenhuma infração registada.</p>
        </div>

        <div class="bg-white dark:bg-gray-800 p-8 rounded-[2.5rem] border border-stone-100 dark:border-gray-700 shadow-sm">
          <div class="flex justify-between items-center mb-6">
            <h3 class="font-bold text-xl flex items-center gap-2">
              <BootstrapIcon name="calendar-x" class="text-orange-500" /> Maiores Ausências (Estudo)
            </h3>
          </div>
          <div v-if="dashboard.discipline.top_ausentes?.length" class="space-y-4">
            <div v-for="aus in dashboard.discipline.top_ausentes" :key="aus.estudante_id" class="flex justify-between items-center p-4 bg-stone-50 dark:bg-gray-700/50 rounded-2xl">
              <span class="font-medium">{{ aus.estudante__nome_completo }}</span>
              <span class="px-3 py-1 bg-orange-100 text-orange-600 rounded-lg text-xs font-black">{{ aus.total }} Faltas</span>
            </div>
          </div>
          <p v-else class="text-stone-400 text-sm">Presença total garantida.</p>
        </div>
      </section>

    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useApi } from '~/composables/useApi'
import { useAuth } from '~/composables/useAuth'

const { api } = useApi()
const { user, fetchUser, accessToken } = useAuth()

// Garantir que o user esteja carregado antes do dashboard
onMounted(async () => {
  if (!user.value && accessToken.value) {
    await fetchUser()
  }
})

// Buscar dados do dashboard
const { data: dashboard, pending, error, refresh } = await useAsyncData(
  'admin-dashboard-data',
  async () => {
    if (!accessToken.value) return null
    return await api<any>('/admin/dashboard/')
  },
  { 
    watch: [user],
    server: false
  }
)

// Calcular percentagem de ocupação (se existirem dados)
const ocupacaoPercent = computed(() => {
  if (!dashboard.value?.administrative) return 0
  const totalVagas = dashboard.value.administrative.total_vagas || 0
  const totalOcupadas = dashboard.value.administrative.total_ocupadas || 0
  if (totalVagas === 0) return 0
  return Math.round((totalOcupadas / totalVagas) * 100)
})

const formatMoeda = (valor: number) => {
  return new Intl.NumberFormat('pt-MZ', { style: 'currency', currency: 'MZN' }).format(valor)
}
</script>

<style scoped>
.animate-in {
  animation: fadeIn 0.5s ease-out;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
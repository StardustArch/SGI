<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 md:py-8">
    
    <!-- Cabeçalho -->
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6 md:mb-8">
      <div>
        <h1 class="text-2xl md:text-3xl font-bold text-slate-900 dark:text-white">
          Dashboard <span class="text-blue-600 dark:text-blue-400">{{ user?.perfil_nome }}</span>
        </h1>
        <p class="text-sm md:text-base text-slate-500 dark:text-slate-400 mt-1">
          {{ pending ? 'A sincronizar dados...' : 'Visão geral do ecossistema do internato.' }}
        </p>
      </div>
      
      <button 
        @click="refresh()" 
        :disabled="pending"
        class="flex items-center gap-2 px-4 py-2.5 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-lg shadow-sm hover:bg-slate-50 dark:hover:bg-slate-800 transition-all disabled:opacity-50 min-h-[44px]"
      >
        <BootstrapIcon name="arrow-clockwise" :class="{ 'animate-spin': pending }" class="w-5 h-5 text-slate-600 dark:text-slate-400" />
        <span class="text-sm font-medium text-slate-700 dark:text-slate-300">Actualizar</span>
      </button>
    </div>

    <!-- Erro -->
    <div v-if="error" class="p-6 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800/30 rounded-xl flex flex-col items-center text-center space-y-3">
      <BootstrapIcon name="exclamation-triangle-fill" class="text-red-500 dark:text-red-400 w-10 h-10" />
      <h3 class="font-semibold text-red-800 dark:text-red-300">Falha na ligação com o servidor</h3>
      <p class="text-red-600 dark:text-red-400 text-sm">Não conseguimos recuperar os indicadores de gestão neste momento.</p>
    </div>

    <!-- Loading -->
    <div v-if="pending" class="space-y-5 md:space-y-6">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 md:gap-5">
        <div v-for="i in 3" :key="i" class="h-28 bg-slate-100 dark:bg-slate-800 animate-pulse rounded-xl"></div>
      </div>
      <div class="h-64 bg-slate-50 dark:bg-slate-800/50 animate-pulse rounded-xl"></div>
    </div>

    <!-- Conteúdo -->
    <div v-else-if="dashboard" class="space-y-8">
      
      <!-- Dados Administrativos (Gestor/Suporte) -->
      <section v-if="dashboard.administrative" class="space-y-4">
        <h2 class="text-sm font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider flex items-center gap-2">
          <BootstrapIcon name="buildings" class="w-4 h-4" />
          Gestão de Capacidade
        </h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-5">
          <!-- Card Alunos Activos -->
          <div class="bg-white dark:bg-slate-900 p-5 md:p-6 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-xs font-medium text-slate-500 dark:text-slate-400 uppercase mb-1">Alunos Activos</p>
                <h3 class="text-2xl md:text-3xl font-bold text-slate-900 dark:text-white">{{ dashboard.administrative.total_estudantes_ativos || 0 }}</h3>
              </div>
              <div class="h-12 w-12 rounded-lg bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 flex items-center justify-center">
                <BootstrapIcon name="people-fill" class="w-6 h-6" />
              </div>
            </div>
          </div>

          <!-- Card Ocupação -->
          <div class="bg-white dark:bg-slate-900 p-5 md:p-6 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-xs font-medium text-slate-500 dark:text-slate-400 uppercase mb-1">Ocupação</p>
                <h3 class="text-2xl md:text-3xl font-bold text-slate-900 dark:text-white">
                  {{ ocupacaoPercent }}%
                </h3>
                <p class="text-xs text-slate-400 dark:text-slate-500 mt-0.5">
                  {{ dashboard.administrative.total_ocupadas }}/{{ dashboard.administrative.total_vagas }} camas
                </p>
              </div>
              <div :class="[
                'h-12 w-12 rounded-lg flex items-center justify-center',
                ocupacaoPercent > 90 
                  ? 'bg-rose-50 dark:bg-rose-900/30 text-rose-600 dark:text-rose-400' 
                  : 'bg-emerald-50 dark:bg-emerald-900/30 text-emerald-600 dark:text-emerald-400'
              ]">
                <BootstrapIcon name="door-closed-fill" class="w-6 h-6" />
              </div>
            </div>
          </div>

          <!-- Card Pedidos Pendentes -->
          <div class="bg-white dark:bg-slate-900 p-5 md:p-6 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-xs font-medium text-slate-500 dark:text-slate-400 uppercase mb-1">Pedidos Pendentes</p>
                <h3 class="text-2xl md:text-3xl font-bold text-slate-900 dark:text-white">{{ dashboard.administrative.pedidos_saida_pendentes || 0 }}</h3>
              </div>
              <div class="h-12 w-12 rounded-lg bg-amber-50 dark:bg-amber-900/30 text-amber-600 dark:text-amber-400 flex items-center justify-center">
                <BootstrapIcon name="clock-history" class="w-6 h-6" />
              </div>
            </div>
            <NuxtLink to="/dashboard/admin/exits" class="text-xs font-medium text-blue-600 dark:text-blue-400 hover:underline mt-3 inline-block">
              Ver todos →
            </NuxtLink>
          </div>
        </div>
      </section>

      <!-- Dados Financeiros (Financeiro/Suporte) -->
      <section v-if="dashboard.finance" class="space-y-4">
        <h2 class="text-sm font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wider flex items-center gap-2">
          <BootstrapIcon name="cash-stack" class="w-4 h-4" />
          Saúde Financeira (Mês Actual)
        </h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-5">
          <!-- Arrecadado -->
          <div class="bg-white dark:bg-slate-900 p-5 md:p-6 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-xs font-medium text-slate-500 dark:text-slate-400 uppercase mb-1">Arrecadado</p>
                <h3 class="text-xl md:text-2xl font-bold text-emerald-600 dark:text-emerald-400">{{ formatMoeda(dashboard.finance.total_arrecadado_mes || 0) }}</h3>
              </div>
              <div class="h-12 w-12 rounded-lg bg-emerald-50 dark:bg-emerald-900/30 text-emerald-600 dark:text-emerald-400 flex items-center justify-center">
                <BootstrapIcon name="cash-coin" class="w-6 h-6" />
              </div>
            </div>
          </div>
          <!-- Pendentes -->
          <div class="bg-white dark:bg-slate-900 p-5 md:p-6 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-xs font-medium text-slate-500 dark:text-slate-400 uppercase mb-1">Pendentes</p>
                <h3 class="text-2xl md:text-3xl font-bold text-slate-900 dark:text-white">{{ dashboard.finance.total_estudantes_pendentes || 0 }}</h3>
              </div>
              <div class="h-12 w-12 rounded-lg bg-amber-50 dark:bg-amber-900/30 text-amber-600 dark:text-amber-400 flex items-center justify-center">
                <BootstrapIcon name="hourglass-split" class="w-6 h-6" />
              </div>
            </div>
          </div>
          <!-- Em Atraso -->
          <div class="bg-white dark:bg-slate-900 p-5 md:p-6 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-xs font-medium text-slate-500 dark:text-slate-400 uppercase mb-1">Em Atraso</p>
                <h3 class="text-2xl md:text-3xl font-bold text-rose-600 dark:text-rose-400">{{ dashboard.finance.total_estudantes_atraso || 0 }}</h3>
              </div>
              <div class="h-12 w-12 rounded-lg bg-rose-50 dark:bg-rose-900/30 text-rose-600 dark:text-rose-400 flex items-center justify-center">
                <BootstrapIcon name="exclamation-triangle" class="w-6 h-6" />
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Dados Disciplinares (Disciplinar/Suporte) -->
      <section v-if="dashboard.discipline" class="grid grid-cols-1 lg:grid-cols-2 gap-5 md:gap-6">
        <!-- Top Infratores -->
        <div class="bg-white dark:bg-slate-900 p-5 md:p-6 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm">
          <div class="flex flex-wrap justify-between items-center gap-2 mb-5 border-b border-slate-100 dark:border-slate-800 pb-3">
            <h3 class="text-base font-semibold text-slate-900 dark:text-white flex items-center gap-2">
              <BootstrapIcon name="shield-exclamation" class="w-5 h-5 text-rose-500" />
              Top Infratores
            </h3>
            <span class="text-xs font-medium text-slate-400 dark:text-slate-500">Últimos 30 dias</span>
          </div>
          <div v-if="dashboard.discipline.top_infratores?.length" class="space-y-3">
            <div v-for="inf in dashboard.discipline.top_infratores" :key="inf.estudante_id" class="flex flex-wrap justify-between items-center gap-2 p-3 bg-slate-50 dark:bg-slate-800/50 rounded-lg">
              <span class="font-medium text-slate-700 dark:text-slate-300 text-sm">{{ inf.estudante__nome_completo }}</span>
              <span class="px-2.5 py-0.5 bg-rose-50 dark:bg-rose-900/30 text-rose-700 dark:text-rose-300 rounded-md text-xs font-medium border border-rose-200 dark:border-rose-800/30">
                {{ inf.total }} Sanções
              </span>
            </div>
          </div>
          <p v-else class="text-slate-400 dark:text-slate-500 text-sm text-center py-6">Nenhuma infração registada.</p>
        </div>

        <!-- Maiores Ausências -->
        <div class="bg-white dark:bg-slate-900 p-5 md:p-6 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm">
          <div class="flex flex-wrap justify-between items-center gap-2 mb-5 border-b border-slate-100 dark:border-slate-800 pb-3">
            <h3 class="text-base font-semibold text-slate-900 dark:text-white flex items-center gap-2">
              <BootstrapIcon name="calendar-x" class="w-5 h-5 text-amber-500" />
              Maiores Ausências (Estudo)
            </h3>
          </div>
          <div v-if="dashboard.discipline.top_ausentes?.length" class="space-y-3">
            <div v-for="aus in dashboard.discipline.top_ausentes" :key="aus.estudante_id" class="flex flex-wrap justify-between items-center gap-2 p-3 bg-slate-50 dark:bg-slate-800/50 rounded-lg">
              <span class="font-medium text-slate-700 dark:text-slate-300 text-sm">{{ aus.estudante__nome_completo }}</span>
              <span class="px-2.5 py-0.5 bg-amber-50 dark:bg-amber-900/30 text-amber-700 dark:text-amber-300 rounded-md text-xs font-medium border border-amber-200 dark:border-amber-800/30">
                {{ aus.total }} Faltas
              </span>
            </div>
          </div>
          <p v-else class="text-slate-400 dark:text-slate-500 text-sm text-center py-6">Presença total garantida.</p>
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

onMounted(async () => {
  if (!user.value && accessToken.value) {
    await fetchUser()
  }
})

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
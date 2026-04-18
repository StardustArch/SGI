<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 md:py-8">
    
    <!-- Cabeçalho -->
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6">
      <div>
        <h1 class="text-2xl md:text-3xl font-bold text-slate-900 dark:text-white">Relatórios & Insights</h1>
        <p class="text-sm md:text-base text-slate-500 dark:text-slate-400 mt-1">
          {{ descricaoPerfil }}
        </p>
      </div>
      <div v-if="showExport" class="flex gap-3">
        <button @click="exportar('xlsx')" class="px-4 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white text-sm font-medium transition-colors flex items-center gap-2 min-h-[44px]">
          <BootstrapIcon name="file-excel" class="w-4 h-4" />
          Excel
        </button>
        <button @click="exportar('pdf')" class="px-4 py-2 rounded-lg bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium transition-colors flex items-center gap-2 min-h-[44px]">
          <BootstrapIcon name="file-pdf" class="w-4 h-4" />
          PDF
        </button>
      </div>
    </div>

    <!-- Cards de sumário financeiro -->
    <div v-if="showFinanceiro" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-5 mb-6">
      <div class="bg-white dark:bg-slate-900 rounded-xl p-5 border border-slate-200 dark:border-slate-800 shadow-sm">
        <p class="text-xs font-medium text-slate-500 dark:text-slate-400 uppercase mb-1">Receita Arrecadada (Mês)</p>
        <h3 class="text-xl md:text-2xl font-bold text-slate-900 dark:text-white">{{ formatMoeda(dashboardData?.finance?.total_arrecadado_mes || 0) }}</h3>
      </div>
      <div class="bg-white dark:bg-slate-900 rounded-xl p-5 border border-slate-200 dark:border-slate-800 shadow-sm">
        <p class="text-xs font-medium text-slate-500 dark:text-slate-400 uppercase mb-1">Estudantes Pendentes</p>
        <h3 class="text-xl md:text-2xl font-bold text-slate-900 dark:text-white">{{ dashboardData?.finance?.total_estudantes_pendentes || 0 }}</h3>
      </div>
      <div class="bg-white dark:bg-slate-900 rounded-xl p-5 border border-slate-200 dark:border-slate-800 shadow-sm">
        <p class="text-xs font-medium text-slate-500 dark:text-slate-400 uppercase mb-1">Em Atraso</p>
        <h3 class="text-xl md:text-2xl font-bold text-rose-600 dark:text-rose-400">{{ dashboardData?.finance?.total_estudantes_atraso || 0 }}</h3>
      </div>
    </div>

    <!-- Gráficos disciplinares -->
    <div v-if="showDisciplinar" class="grid grid-cols-1 lg:grid-cols-2 gap-5 md:gap-6 mb-6">
      <!-- Top Infratores -->
      <div class="bg-white dark:bg-slate-900 rounded-xl p-5 md:p-6 border border-slate-200 dark:border-slate-800 shadow-sm">
        <h3 class="text-base font-semibold text-slate-900 dark:text-white flex items-center gap-2 mb-5 border-b border-slate-100 dark:border-slate-800 pb-3">
          <BootstrapIcon name="shield-exclamation" class="w-5 h-5 text-rose-500" />
          Top 10 Infratores (Mês)
        </h3>
        <div v-if="dashboardData?.discipline?.top_infratores?.length" class="space-y-3">
          <div v-for="(item, idx) in dashboardData.discipline.top_infratores.slice(0,5)" :key="idx" class="flex items-center gap-3">
            <span class="text-sm font-medium text-slate-400 dark:text-slate-500 w-6">#{{ idx+1 }}</span>
            <div class="flex-1">
              <div class="flex justify-between mb-1">
                <span class="text-sm font-medium text-slate-700 dark:text-slate-300 truncate">{{ item.estudante__nome_completo }}</span>
                <span class="text-xs font-medium text-rose-600 dark:text-rose-400">{{ item.total }} sanções</span>
              </div>
              <div class="w-full bg-slate-100 dark:bg-slate-800 h-1.5 rounded-full overflow-hidden">
                <div class="bg-rose-500 h-full rounded-full" :style="{ width: Math.min(item.total * 8, 100) + '%' }"></div>
              </div>
            </div>
          </div>
        </div>
        <p v-else class="text-slate-500 dark:text-slate-400 text-sm text-center py-6">Nenhuma sanção registada este mês.</p>
      </div>

      <!-- Top Ausências -->
      <div class="bg-white dark:bg-slate-900 rounded-xl p-5 md:p-6 border border-slate-200 dark:border-slate-800 shadow-sm">
        <h3 class="text-base font-semibold text-slate-900 dark:text-white flex items-center gap-2 mb-5 border-b border-slate-100 dark:border-slate-800 pb-3">
          <BootstrapIcon name="calendar-x" class="w-5 h-5 text-amber-500" />
          Top 10 Ausências (Estudo)
        </h3>
        <div v-if="dashboardData?.discipline?.top_ausentes?.length" class="space-y-3">
          <div v-for="(item, idx) in dashboardData.discipline.top_ausentes.slice(0,5)" :key="idx" class="flex items-center gap-3">
            <span class="text-sm font-medium text-slate-400 dark:text-slate-500 w-6">#{{ idx+1 }}</span>
            <div class="flex-1">
              <div class="flex justify-between mb-1">
                <span class="text-sm font-medium text-slate-700 dark:text-slate-300 truncate">{{ item.estudante__nome_completo }}</span>
                <span class="text-xs font-medium text-amber-600 dark:text-amber-400">{{ item.total }} faltas</span>
              </div>
              <div class="w-full bg-slate-100 dark:bg-slate-800 h-1.5 rounded-full overflow-hidden">
                <div class="bg-amber-500 h-full rounded-full" :style="{ width: Math.min(item.total * 5, 100) + '%' }"></div>
              </div>
            </div>
          </div>
        </div>
        <p v-else class="text-slate-500 dark:text-slate-400 text-sm text-center py-6">Nenhuma ausência registada este mês.</p>
      </div>
    </div>

    <!-- Resumo de pedidos de saída -->
    <div v-if="showPedidos" class="bg-white dark:bg-slate-900 rounded-xl p-5 md:p-6 border border-slate-200 dark:border-slate-800 shadow-sm mb-6">
      <h3 class="text-base font-semibold text-slate-900 dark:text-white flex items-center gap-2 mb-5 border-b border-slate-100 dark:border-slate-800 pb-3">
        <BootstrapIcon name="door-open" class="w-5 h-5 text-blue-500" />
        Pedidos de Saída (Mês)
      </h3>
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 text-center">
        <div class="p-4 bg-slate-50 dark:bg-slate-800/50 rounded-lg">
          <p class="text-amber-600 dark:text-amber-400 text-sm font-medium mb-1">Pendentes</p>
          <p class="text-2xl font-bold text-slate-900 dark:text-white">{{ dashboardData?.discipline?.sumario_pedidos?.total_pendentes || 0 }}</p>
        </div>
        <div class="p-4 bg-slate-50 dark:bg-slate-800/50 rounded-lg">
          <p class="text-emerald-600 dark:text-emerald-400 text-sm font-medium mb-1">Aprovados</p>
          <p class="text-2xl font-bold text-slate-900 dark:text-white">{{ dashboardData?.discipline?.sumario_pedidos?.total_autorizados || 0 }}</p>
        </div>
        <div class="p-4 bg-slate-50 dark:bg-slate-800/50 rounded-lg">
          <p class="text-rose-600 dark:text-rose-400 text-sm font-medium mb-1">Rejeitados</p>
          <p class="text-2xl font-bold text-slate-900 dark:text-white">{{ dashboardData?.discipline?.sumario_pedidos?.total_rejeitados || 0 }}</p>
        </div>
      </div>
    </div>

    <!-- Sanções por tipo -->
    <div v-if="showDisciplinar && dashboardData?.discipline?.sancao_por_tipo?.length" class="bg-white dark:bg-slate-900 rounded-xl p-5 md:p-6 border border-slate-200 dark:border-slate-800 shadow-sm">
      <h3 class="text-base font-semibold text-slate-900 dark:text-white mb-5 border-b border-slate-100 dark:border-slate-800 pb-3">Sanções por Tipo (Mês)</h3>
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
        <div v-for="tipo in dashboardData.discipline.sancao_por_tipo" :key="tipo.tipo_sancao" class="bg-slate-50 dark:bg-slate-800/50 p-4 rounded-lg text-center border border-slate-200 dark:border-slate-700">
          <p class="font-bold text-xl text-rose-600 dark:text-rose-400">{{ tipo.total }}</p>
          <p class="text-xs text-slate-500 dark:text-slate-400">{{ tipo.tipo_sancao }}</p>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted, inject } from 'vue'
import { useApi } from '~/composables/useApi'

const { api } = useApi()
const userData = inject<any>('userData')
const perfilNome = computed(() => userData?.value?.perfil_nome)

// Determina quais blocos mostrar baseado no perfil
const showFinanceiro = computed(() => {
  const p = perfilNome.value
  return p === 'Financeiro' || p === 'Suporte'
})

const showDisciplinar = computed(() => {
  const p = perfilNome.value
  return p === 'Disciplinar' || p === 'Suporte'
})

const showPedidos = computed(() => {
  const p = perfilNome.value
  return p === 'Gestor' || p === 'Suporte'
})

const descricaoPerfil = computed(() => {
  if (showFinanceiro.value && showDisciplinar.value && showPedidos.value) return 'Visão completa do internato'
  if (showFinanceiro.value) return 'Análise financeira do internato'
  if (showDisciplinar.value) return 'Acompanhamento disciplinar do internato'
  return 'Dados disponíveis do internato'
})

// Dados do dashboard unificado
const dashboardData = ref<any>(null)
const loading = ref(true)

async function carregarDashboard() {
  loading.value = true
  try {
    const data = await api<any>('/admin/dashboard/')
    dashboardData.value = data
  } catch (error) {
    console.error('Erro ao carregar dashboard:', error)
  } finally {
    loading.value = false
  }
}

// Determinar tipo de relatório para exportação
const tipoRelatorio = computed(() => {
  if (showFinanceiro.value && !showDisciplinar.value && !showPedidos.value) return 'financeiro'
  if (showDisciplinar.value && !showFinanceiro.value && !showPedidos.value) return 'disciplinar'
  if (showPedidos.value && !showFinanceiro.value && !showDisciplinar.value) return 'pedidos'
  if (showFinanceiro.value && showDisciplinar.value && showPedidos.value) return 'completo'
  return null
})

const showExport = computed(() => !!tipoRelatorio.value)

async function exportar(formato: string) {
  if (!tipoRelatorio.value) return
  try {
    const params = new URLSearchParams()
    params.append('tipo', tipoRelatorio.value)
    params.append('formato', formato)

    const blob = await api<Blob>(`/admin/relatorios/exportar/?${params.toString()}`, {
      method: 'GET',
      responseType: 'blob'
    })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `relatorio_${tipoRelatorio.value}_${new Date().toISOString().slice(0,10)}.${formato}`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    window.URL.revokeObjectURL(url)
  } catch (err) {
    console.error('Erro ao exportar:', err)
    alert('Erro ao gerar relatório.')
  }
}

const formatMoeda = (v: any) => new Intl.NumberFormat('pt-MZ', { style: 'currency', currency: 'MZN' }).format(Number(v))

onMounted(() => {
  carregarDashboard()
})
</script>
<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 md:py-8">
    
    <!-- Cabeçalho -->
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6">
      <div>
        <h1 class="text-2xl md:text-3xl font-bold text-slate-900 dark:text-white">Gestão Financeira</h1>
        <p class="text-sm md:text-base text-slate-500 dark:text-slate-400 mt-1">Controlo de mensalidades e fluxos de caixa.</p>
      </div>

      <NuxtLink 
        to="/dashboard/admin/finance/generate" 
        class="px-5 py-2.5 rounded-lg bg-blue-600 hover:bg-blue-700 text-white font-medium text-sm transition-colors flex items-center gap-2 min-h-[44px]"
      >
        <BootstrapIcon name="plus-circle" class="w-4 h-4" />
        Gerar Lote
      </NuxtLink>
    </div>

    <!-- Cards de Estatísticas -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-5 mb-6">
      <!-- Arrecadado -->
      <div class="bg-white dark:bg-slate-900 rounded-xl p-5 border border-slate-200 dark:border-slate-800 shadow-sm">
        <div class="flex items-center gap-4">
          <div class="h-12 w-12 rounded-lg bg-emerald-50 dark:bg-emerald-900/30 text-emerald-600 dark:text-emerald-400 flex items-center justify-center">
            <BootstrapIcon name="cash-coin" class="w-6 h-6" />
          </div>
          <div>
            <p class="text-xs font-medium text-slate-500 dark:text-slate-400 uppercase mb-1">Arrecadado (Mês)</p>
            <h3 class="text-xl md:text-2xl font-bold text-slate-900 dark:text-white">{{ formatMoeda(stats?.total_arrecadado_mes || 0) }}</h3>
          </div>
        </div>
      </div>

      <!-- Pendentes -->
      <div class="bg-white dark:bg-slate-900 rounded-xl p-5 border border-slate-200 dark:border-slate-800 shadow-sm">
        <div class="flex items-center gap-4">
          <div class="h-12 w-12 rounded-lg bg-amber-50 dark:bg-amber-900/30 text-amber-600 dark:text-amber-400 flex items-center justify-center">
            <BootstrapIcon name="hourglass-split" class="w-6 h-6" />
          </div>
          <div>
            <p class="text-xs font-medium text-slate-500 dark:text-slate-400 uppercase mb-1">Pendentes</p>
            <h3 class="text-xl md:text-2xl font-bold text-slate-900 dark:text-white">
              {{ stats?.total_estudantes_pendentes || 0 }} <span class="text-sm font-normal text-slate-400">Alunos</span>
            </h3>
          </div>
        </div>
      </div>

      <!-- Em Atraso -->
      <div class="bg-white dark:bg-slate-900 rounded-xl p-5 border border-slate-200 dark:border-slate-800 shadow-sm">
        <div class="flex items-center gap-4">
          <div class="h-12 w-12 rounded-lg bg-rose-50 dark:bg-rose-900/30 text-rose-600 dark:text-rose-400 flex items-center justify-center">
            <BootstrapIcon name="exclamation-circle" class="w-6 h-6" />
          </div>
          <div>
            <p class="text-xs font-medium text-slate-500 dark:text-slate-400 uppercase mb-1">Em Atraso</p>
            <h3 class="text-xl md:text-2xl font-bold text-rose-600 dark:text-rose-400">{{ stats?.total_estudantes_atraso || 0 }}</h3>
          </div>
        </div>
      </div>
    </div>

    <!-- Filtros -->
    <div class="bg-white dark:bg-slate-900 rounded-xl p-4 border border-slate-200 dark:border-slate-800 shadow-sm mb-6">
      <div class="flex flex-col md:flex-row gap-3">
        <div class="flex-1 relative">
          <BootstrapIcon name="search" class="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 w-4 h-4" />
          <input 
            v-model="pesquisa" 
            type="text" 
            placeholder="Pesquisar por aluno ou número..." 
            class="w-full pl-10 pr-4 py-2.5 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg text-sm text-slate-900 dark:text-white placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
          />
        </div>
        <select 
          v-model="filtroEstado" 
          class="px-4 py-2.5 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg text-sm text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 cursor-pointer md:w-48"
        >
          <option :value="null">Todos os Estados</option>
          <option value="Pendente">Pendentes</option>
          <option value="Pago">Pagos</option>
          <option value="Atraso">Em Atraso</option>
        </select>
      </div>
    </div>

    <!-- Lista de Mensalidades em Grid de Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div 
        v-for="item in (mensalidades?.results || mensalidades || [])" 
        :key="item.id" 
        class="bg-white dark:bg-slate-900 rounded-xl p-5 border border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-md transition-shadow flex flex-col"
      >
        <div class="flex items-start justify-between mb-3">
          <div>
            <h3 class="font-semibold text-slate-900 dark:text-white">{{ item.nome_estudante }}</h3>
            <p class="text-xs text-slate-500 dark:text-slate-400 mt-0.5">{{ formatMes(item.mes_referencia) }}</p>
          </div>
          <span :class="[
            'px-2.5 py-0.5 rounded-md text-xs font-medium border',
            getStatusBadge(item.estado)
          ]">
            {{ item.estado }}
          </span>
        </div>

        <div class="flex-1">
          <p class="text-sm text-slate-600 dark:text-slate-300 mb-1">{{ item.tipo || 'Mensalidade' }}</p>
          <p class="text-lg font-bold text-slate-900 dark:text-white">{{ formatMoeda(item.valor_pago || 25000) }}</p>
        </div>

        <div class="mt-4 pt-3 border-t border-slate-100 dark:border-slate-800">
          <NuxtLink 
            :to="`/dashboard/admin/finance/confirm/${item.id}`"
            class="inline-flex items-center gap-1 text-sm font-medium text-blue-600 dark:text-blue-400 hover:underline"
          >
            Detalhes / Confirmar
            <BootstrapIcon name="arrow-right" class="w-4 h-4" />
          </NuxtLink>
        </div>
      </div>
    </div>

    <!-- Mensagem quando não há resultados -->
    <div v-if="(mensalidades?.results || mensalidades || []).length === 0" class="p-16 text-center bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 mt-6">
      <BootstrapIcon name="cash-stack" class="w-12 h-12 text-slate-300 dark:text-slate-600 mx-auto mb-3" />
      <p class="text-slate-500 dark:text-slate-400 font-medium">Nenhuma mensalidade encontrada com estes filtros.</p>
    </div>

  </div>
</template>

<script setup lang="ts">
const { api } = useApi()

const pesquisa = ref('')
const filtroEstado = ref<string | null>(null)

// 1. Buscar dashboard para stats financeiros
const { data: dashboard } = await useAsyncData('admin-dashboard', () => api<any>('/admin/dashboard/'))
const stats = computed(() => dashboard.value?.finance)

// 2. Buscar mensalidades (listagem)
const { data: mensalidades } = await useAsyncData(
  'admin-fin-list',
  () => {
    const params: any = {}
    if (filtroEstado.value) params.estado = filtroEstado.value
    if (pesquisa.value) params.search = pesquisa.value
    return api<any>('/admin/financeiro/mensalidades/', { params })
  },
  { watch: [pesquisa, filtroEstado] }
)

// Helpers
const getStatusBadge = (estado: string) => {
  if (estado === 'Pago') return 'bg-emerald-50 text-emerald-700 border-emerald-200 dark:bg-emerald-900/20 dark:text-emerald-400 dark:border-emerald-800/30'
  if (estado === 'Atraso') return 'bg-rose-50 text-rose-700 border-rose-200 dark:bg-rose-900/20 dark:text-rose-400 dark:border-rose-800/30'
  return 'bg-amber-50 text-amber-700 border-amber-200 dark:bg-amber-900/20 dark:text-amber-400 dark:border-amber-800/30'
}

const formatMoeda = (valor: any) => new Intl.NumberFormat('pt-MZ', { style: 'currency', currency: 'MZN' }).format(Number(valor))
const formatMes = (data: string) => new Date(data).toLocaleDateString('pt-PT', { month: 'long', year: 'numeric' })
</script>
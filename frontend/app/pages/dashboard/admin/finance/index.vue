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

    <!-- Filtros + Toggle de visualização -->
    <div class="bg-white dark:bg-slate-900 rounded-xl p-4 border border-slate-200 dark:border-slate-800 shadow-sm mb-6">
      <div class="flex flex-col md:flex-row gap-3">
        <div class="flex-1 relative">
          <BootstrapIcon name="search" class="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 w-4 h-4" />
          <input 
            v-model="pesquisa" 
            type="text" 
            placeholder="Pesquisar por aluno..." 
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
        <!-- Toggle de visualização -->
        <div class="flex items-center gap-2 ml-auto">
          <button 
            @click="modoVisualizacao = 'cards'" 
            class="p-2 rounded-lg transition-colors"
            :class="modoVisualizacao === 'cards' ? 'bg-blue-100 text-blue-600 dark:bg-blue-900/30 dark:text-blue-400' : 'text-slate-400 hover:text-slate-600 dark:hover:text-slate-300'"
            title="Visualização em cards"
          >
            <BootstrapIcon name="grid-3x3-gap-fill" class="w-5 h-5" />
          </button>
          <button 
            @click="modoVisualizacao = 'tabela'" 
            class="p-2 rounded-lg transition-colors"
            :class="modoVisualizacao === 'tabela' ? 'bg-blue-100 text-blue-600 dark:bg-blue-900/30 dark:text-blue-400' : 'text-slate-400 hover:text-slate-600 dark:hover:text-slate-300'"
            title="Visualização em tabela"
          >
            <BootstrapIcon name="table" class="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>

<!-- Cards agrupados por estudante -->
<div v-if="modoVisualizacao === 'cards'" class="space-y-3">
  <div
    v-for="grupo in estudantesAgrupados"
    :key="grupo.id"
    class="bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm overflow-hidden"
  >
    <button
      @click="toggleExpandir(grupo.id)"
      class="w-full flex items-center justify-between gap-4 p-4 hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors text-left"
    >
      <div class="flex items-center gap-3">
        <div class="h-10 w-10 rounded-full bg-slate-100 dark:bg-slate-800 flex items-center justify-center text-slate-500 dark:text-slate-300 font-semibold text-sm">
          {{ grupo.nome.charAt(0).toUpperCase() }}
        </div>
        <div>
          <h3 class="font-semibold text-slate-900 dark:text-white">{{ grupo.nome }}</h3>
          <p class="text-xs text-slate-500 dark:text-slate-400">{{ grupo.mensalidades.length }} mensalidade(s)</p>
        </div>
      </div>

      <div class="flex items-center gap-2">
        <span v-if="grupo.totalAtraso" class="px-2.5 py-0.5 rounded-md text-xs font-medium border bg-rose-50 text-rose-700 border-rose-200 dark:bg-rose-900/20 dark:text-rose-400 dark:border-rose-800/30">
          {{ grupo.totalAtraso }} em atraso
        </span>
        <span v-if="grupo.totalPendente" class="px-2.5 py-0.5 rounded-md text-xs font-medium border bg-amber-50 text-amber-700 border-amber-200 dark:bg-amber-900/20 dark:text-amber-400 dark:border-amber-800/30">
          {{ grupo.totalPendente }} pendente(s)
        </span>
        <span v-if="grupo.totalPago" class="px-2.5 py-0.5 rounded-md text-xs font-medium border bg-emerald-50 text-emerald-700 border-emerald-200 dark:bg-emerald-900/20 dark:text-emerald-400 dark:border-emerald-800/30">
          {{ grupo.totalPago }} pago(s)
        </span>
        <BootstrapIcon :name="expandido[grupo.id] ? 'chevron-up' : 'chevron-down'" class="w-4 h-4 text-slate-400" />
      </div>
    </button>

    <div v-if="expandido[grupo.id]" class="border-t border-slate-100 dark:border-slate-800 divide-y divide-slate-100 dark:divide-slate-800">
      <div v-for="item in grupo.mensalidades" :key="item.id" class="flex items-center justify-between gap-4 px-4 py-3">
        <div>
          <p class="text-sm font-medium text-slate-900 dark:text-white capitalize">{{ formatMes(item.mes_referencia) }}</p>
          <p class="text-xs text-slate-500 dark:text-slate-400">{{ item.tipo || 'Mensalidade' }}</p>
        </div>
        <div class="flex items-center gap-3">
          <span class="text-sm font-medium text-slate-700 dark:text-slate-300">{{ formatMoeda(item.valor_pago || 2500) }}</span>
          <span :class="['px-2.5 py-0.5 rounded-md text-xs font-medium border', getStatusBadge(item.estado)]">
            {{ item.estado }}
          </span>
          <NuxtLink :to="`/dashboard/admin/finance/confirm/${item.id}`" class="text-sm font-medium text-blue-600 dark:text-blue-400 hover:underline">
            Confirmar
          </NuxtLink>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- Tabela agrupada por estudante -->
<div v-else class="overflow-x-auto rounded-xl border border-slate-200 dark:border-slate-800">
  <table class="min-w-full divide-y divide-slate-200 dark:divide-slate-800 text-sm">
    <thead class="bg-slate-50 dark:bg-slate-800/50">
      <tr>
        <th class="px-4 py-3 text-left font-semibold text-slate-600 dark:text-slate-300">Mês</th>
        <th class="px-4 py-3 text-left font-semibold text-slate-600 dark:text-slate-300">Valor</th>
        <th class="px-4 py-3 text-left font-semibold text-slate-600 dark:text-slate-300">Estado</th>
        <th class="px-4 py-3 text-left font-semibold text-slate-600 dark:text-slate-300">Tipo</th>
        <th class="px-4 py-3 text-right font-semibold text-slate-600 dark:text-slate-300">Ações</th>
      </tr>
    </thead>
    <tbody class="divide-y divide-slate-200 dark:divide-slate-800 bg-white dark:bg-slate-900">
      <template v-for="grupo in estudantesAgrupados" :key="grupo.id">
        <tr class="bg-slate-50 dark:bg-slate-800/40">
          <td colspan="5" class="px-4 py-2 font-semibold text-slate-700 dark:text-slate-200 text-xs uppercase tracking-wide">
            {{ grupo.nome }} <span class="text-slate-400 font-normal">({{ grupo.mensalidades.length }})</span>
          </td>
        </tr>
        <tr v-for="item in grupo.mensalidades" :key="item.id" class="hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors">
          <td class="px-4 py-3 pl-8 text-slate-700 dark:text-slate-300 capitalize">{{ formatMes(item.mes_referencia) }}</td>
          <td class="px-4 py-3 text-slate-700 dark:text-slate-300 font-medium">{{ formatMoeda(item.valor_pago || 2500) }}</td>
          <td class="px-4 py-3">
            <span :class="['px-2.5 py-0.5 rounded-md text-xs font-medium border', getStatusBadge(item.estado)]">
              {{ item.estado }}
            </span>
          </td>
          <td class="px-4 py-3 text-slate-700 dark:text-slate-300">{{ item.tipo || 'Mensalidade' }}</td>
          <td class="px-4 py-3 text-right">
            <NuxtLink :to="`/dashboard/admin/finance/confirm/${item.id}`" class="inline-flex items-center gap-1 text-sm font-medium text-blue-600 dark:text-blue-400 hover:underline">
              Confirmar
              <BootstrapIcon name="arrow-right" class="w-4 h-4" />
            </NuxtLink>
          </td>
        </tr>
      </template>
    </tbody>
  </table>
</div>

<div v-if="estudantesAgrupados.length === 0" class="p-16 text-center bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 mt-6">
  <BootstrapIcon name="cash-stack" class="w-12 h-12 text-slate-300 dark:text-slate-600 mx-auto mb-3" />
  <p class="text-slate-500 dark:text-slate-400 font-medium">Nenhuma mensalidade encontrada com estes filtros.</p>
</div>

    <!-- Mensagem quando não há resultados -->
    <div v-if="listaFiltrada.length === 0" class="p-16 text-center bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 mt-6">
      <BootstrapIcon name="cash-stack" class="w-12 h-12 text-slate-300 dark:text-slate-600 mx-auto mb-3" />
      <p class="text-slate-500 dark:text-slate-400 font-medium">Nenhuma mensalidade encontrada com estes filtros.</p>
    </div>

  </div>
</template>

<script setup lang="ts">
import { computed, ref, reactive } from 'vue'

const { api } = useApi()

const pesquisa = ref('')
const filtroEstado = ref<string | null>(null)
const modoVisualizacao = ref<'cards' | 'tabela'>('cards')
const expandido = reactive<Record<string, boolean>>({})

const { data: dashboard } = await useAsyncData('admin-dashboard', () => api<any>('/admin/dashboard/'))
const stats = computed(() => dashboard.value?.finance)

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

const listaFiltrada = computed(() => mensalidades.value?.results || mensalidades.value || [])

// --- Agrupamento por estudante ---
interface GrupoEstudante {
  id: string | number
  nome: string
  mensalidades: any[]
  totalPago: number
  totalPendente: number
  totalAtraso: number
  estadoGeral: 'Pago' | 'Pendente' | 'Atraso'
}

const estudantesAgrupados = computed<GrupoEstudante[]>(() => {
  const mapa = new Map<string | number, GrupoEstudante>()

  for (const item of listaFiltrada.value) {
    const chave = item.estudante_id ?? item.nome_estudante
    if (!mapa.has(chave)) {
      mapa.set(chave, {
        id: chave,
        nome: item.nome_estudante,
        mensalidades: [],
        totalPago: 0,
        totalPendente: 0,
        totalAtraso: 0,
        estadoGeral: 'Pago',
      })
    }
    const grupo = mapa.get(chave)!
    grupo.mensalidades.push(item)

    if (item.estado === 'Pago') grupo.totalPago++
    else if (item.estado === 'Atraso') grupo.totalAtraso++
    else grupo.totalPendente++
  }

for (const grupo of mapa.values()) {
  grupo.mensalidades.sort(
    (a, b) => new Date(a.mes_referencia).getTime() - new Date(b.mes_referencia).getTime()
  )
  grupo.estadoGeral = grupo.totalAtraso > 0 ? 'Atraso' : grupo.totalPendente > 0 ? 'Pendente' : 'Pago'
  // todos os grupos começam colapsados
  if (expandido[grupo.id] === undefined) {
    expandido[grupo.id] = false
  }
}

  return Array.from(mapa.values()).sort((a, b) => a.nome.localeCompare(b.nome))
})

const toggleExpandir = (id: string | number) => {
  expandido[id] = !expandido[id]
}

const getStatusBadge = (estado: string) => {
  if (estado === 'Pago') return 'bg-emerald-50 text-emerald-700 border-emerald-200 dark:bg-emerald-900/20 dark:text-emerald-400 dark:border-emerald-800/30'
  if (estado === 'Atraso') return 'bg-rose-50 text-rose-700 border-rose-200 dark:bg-rose-900/20 dark:text-rose-400 dark:border-rose-800/30'
  return 'bg-amber-50 text-amber-700 border-amber-200 dark:bg-amber-900/20 dark:text-amber-400 dark:border-amber-800/30'
}

const formatMoeda = (valor: any) =>
  new Intl.NumberFormat('pt-MZ', { style: 'currency', currency: 'MZN' }).format(Number(valor))

const formatMes = (data: string) => {
  if (!data) return '—'
  return new Date(data).toLocaleDateString('pt-PT', { month: 'long', year: 'numeric' })
}
</script>
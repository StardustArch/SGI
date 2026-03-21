<template>
  <div class="space-y-8 dark:text-white max-w-8xl mx-auto p-4 md:p-8">
    <div class="flex justify-between items-center">
    <div>
      <h1 class="text-3xl font-bold text-gray-800 dark:text-white tracking-tight">Relatórios & Insights</h1>
      <p class="text-stone-500 dark:text-gray-400 mt-1 text-lg">
        {{ descricaoPerfil }}
      </p>
    </div>
    <div class="flex gap-3">
        <button v-if="showExport" @click="exportar('xlsx')" class="px-4 py-2 bg-emerald-500 text-white rounded-xl text-sm font-bold hover:bg-emerald-600 flex items-center gap-2">
          <BootstrapIcon name="file-excel-fill" /> Excel
        </button>
        <button v-if="showExport" @click="exportar('pdf')" class="px-4 py-2 bg-rose-500 text-white rounded-xl text-sm font-bold hover:bg-rose-600 flex items-center gap-2">
          <BootstrapIcon name="file-pdf-fill" /> PDF
        </button>
      </div></div>

    <!-- Cards de sumário financeiro (Financeiro, Gestor, Suporte) -->
    <div v-if="showFinanceiro" class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="stat-card bg-emerald-50 dark:bg-emerald-900/10 border-emerald-100">
        <p class="stat-label text-emerald-600">Receita Arrecadada (Mês)</p>
        <h3 class="stat-value">{{ formatMoeda(financeiroData?.total_arrecadado_mes || 0) }}</h3>
      </div>
      <div class="stat-card bg-amber-50 dark:bg-amber-900/10 border-amber-100">
        <p class="stat-label text-amber-600">Estudantes Pendentes</p>
        <h3 class="stat-value">{{ financeiroData?.total_estudantes_pendentes || 0 }}</h3>
      </div>
      <div class="stat-card bg-rose-50 dark:bg-rose-900/10 border-rose-100">
        <p class="stat-label text-rose-600">Em Atraso</p>
        <h3 class="stat-value text-rose-500">{{ financeiroData?.total_estudantes_atraso || 0 }}</h3>
      </div>
    </div>

    <!-- Gráficos disciplinares (Disciplinar, Gestor, Suporte) -->
    <div v-if="showDisciplinar" class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <div class="bg-white dark:bg-gray-800 rounded-[2rem] p-8 border border-stone-100 dark:border-gray-700 shadow-sm">
        <h3 class="text-lg font-bold mb-6 flex items-center gap-2">
          <BootstrapIcon name="shield-lock-fill" class="text-rose-500" />
          Top 10 Infratores (Mês)
        </h3>
        <div v-if="disciplinarData?.top_infratores?.length" class="space-y-4">
          <div v-for="(item, idx) in disciplinarData.top_infratores.slice(0,5)" :key="idx" class="flex items-center gap-4">
            <span class="text-sm font-bold text-stone-300">#{{ idx+1 }}</span>
            <div class="flex-1">
              <div class="flex justify-between mb-1">
                <span class="text-sm font-bold">{{ item.estudante__nome_completo }}</span>
                <span class="text-xs font-bold text-rose-500">{{ item.total }} sanções</span>
              </div>
              <div class="w-full bg-stone-100 dark:bg-gray-700 h-2 rounded-full overflow-hidden">
                <div class="bg-rose-500 h-full" :style="{ width: (item.total * 8) + '%' }"></div>
              </div>
            </div>
          </div>
        </div>
        <p v-else class="text-stone-400 text-sm">Nenhuma sanção registada este mês.</p>
      </div>

      <div class="bg-white dark:bg-gray-800 rounded-[2rem] p-8 border border-stone-100 dark:border-gray-700 shadow-sm">
        <h3 class="text-lg font-bold mb-6 flex items-center gap-2">
          <BootstrapIcon name="calendar-x-fill" class="text-amber-500" />
          Top 10 Ausências (Estudo)
        </h3>
        <div v-if="disciplinarData?.top_ausentes?.length" class="space-y-4">
          <div v-for="(item, idx) in disciplinarData.top_ausentes.slice(0,5)" :key="idx" class="flex items-center gap-4">
            <span class="text-sm font-bold text-stone-300">#{{ idx+1 }}</span>
            <div class="flex-1">
              <div class="flex justify-between mb-1">
                <span class="text-sm font-bold">{{ item.estudante__nome_completo }}</span>
                <span class="text-xs font-bold text-amber-500">{{ item.total }} faltas</span>
              </div>
              <div class="w-full bg-stone-100 dark:bg-gray-700 h-2 rounded-full overflow-hidden">
                <div class="bg-amber-500 h-full" :style="{ width: (item.total * 5) + '%' }"></div>
              </div>
            </div>
          </div>
        </div>
        <p v-else class="text-stone-400 text-sm">Nenhuma ausência registada este mês.</p>
      </div>
    </div>

    <!-- Resumo de pedidos de saída (Gestor e Suporte) -->
    <div v-if="showPedidos" class="bg-white dark:bg-gray-800 rounded-[2rem] p-8 border border-stone-100 dark:border-gray-700 shadow-sm">
      <h3 class="text-lg font-bold mb-6 flex items-center gap-2">
        <BootstrapIcon name="door-open-fill" class="text-blue-500" />
        Pedidos de Saída (Mês)
      </h3>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="text-center">
          <p class="text-amber-600 text-sm font-bold">Pendentes</p>
          <p class="text-2xl font-bold">{{ pedidosData?.total_pendentes || 0 }}</p>
        </div>
        <div class="text-center">
          <p class="text-emerald-600 text-sm font-bold">Aprovados</p>
          <p class="text-2xl font-bold">{{ pedidosData?.total_aprovados || 0 }}</p>
        </div>
        <div class="text-center">
          <p class="text-rose-600 text-sm font-bold">Rejeitados</p>
          <p class="text-2xl font-bold">{{ pedidosData?.total_rejeitados || 0 }}</p>
        </div>
      </div>
    </div>

    <!-- Sanções por tipo (Disciplinar, Gestor, Suporte) -->
    <div v-if="showDisciplinar && disciplinarData?.sancao_por_tipo?.length" class="bg-white dark:bg-gray-800 rounded-[2rem] p-8 border border-stone-100 dark:border-gray-700 shadow-sm">
      <h3 class="text-lg font-bold mb-6">Sanções por Tipo (Mês)</h3>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div v-for="tipo in disciplinarData.sancao_por_tipo" :key="tipo.tipo_sancao" class="bg-stone-50 dark:bg-gray-700 p-4 rounded-xl text-center">
          <p class="font-bold text-2xl text-rose-500">{{ tipo.total }}</p>
          <p class="text-xs">{{ tipo.tipo_sancao }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

// Aceder ao userData provido pelo layout (sidebar)
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
  if (showFinanceiro.value && showDisciplinar.value && showPedidos.value) return 'completa do internato'
  if (showFinanceiro.value) return 'financeira do internato'
  if (showDisciplinar.value) return 'disciplinar do internato'
  return 'dos dados disponíveis'
})

// Chamadas à API condicionais (só se necessário)
const { api } = useApi()

const financeiroData = ref<any>(null)
const disciplinarData = ref<any>(null)
const pedidosData = ref<any>(null)

async function carregarDados() {
  const promises: Promise<any>[] = []
  if (showFinanceiro.value) promises.push(api('/admin/financeiro/sumario/'))
  if (showDisciplinar.value) promises.push(api('/relatorios/disciplina/top-10/').then(r => ({ top_infratores: r })))
  if (showDisciplinar.value) promises.push(api('/relatorios/assiduidade/top-ausentes/').then(r => ({ top_ausentes: r })))
  if (showDisciplinar.value) promises.push(api('/relatorios/disciplina/por-tipo/').then(r => ({ sancao_por_tipo: r })))
  if (showPedidos.value) promises.push(api('/relatorios/pedidos-saida/sumario/'))

  const results = await Promise.all(promises)
  let idx = 0
  if (showFinanceiro.value) financeiroData.value = results[idx++]
  if (showDisciplinar.value) {
    disciplinarData.value = {
      top_infratores: results[idx++],
      top_ausentes: results[idx++],
      sancao_por_tipo: results[idx++],
    }
  }
  if (showPedidos.value) pedidosData.value = results[idx++]
}

// Executar quando a página for montada
onMounted(() => {
  carregarDados()
})

const formatMoeda = (v: any) => new Intl.NumberFormat('pt-MZ', { style: 'currency', currency: 'MZN' }).format(Number(v))


const tipoRelatorio = computed(() => {
  if (showFinanceiro.value && !showDisciplinar.value && !showPedidos.value) return 'financeiro'
  if (showDisciplinar.value && !showFinanceiro.value && !showPedidos.value) return 'disciplinar'
  if (showPedidos.value && !showFinanceiro.value && !showDisciplinar.value) return 'pedidos'
  if (showFinanceiro.value && showDisciplinar.value && showPedidos.value) return 'completo'  // usar vários tipos
  return null
})

const showExport = computed(() => !!tipoRelatorio.value)

async function exportar(formato: string) {
  if (!tipoRelatorio.value) return
  try {
    const params = new URLSearchParams()
    params.append('tipo', tipoRelatorio.value)
    params.append('formato', formato)
    // adicionar período se necessário
    // params.append('periodo_inicio', ...)
    // params.append('periodo_fim', ...)

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
</script>

<style scoped>
.stat-card {
  @apply p-6 rounded-[2rem] border shadow-sm relative overflow-hidden;
}
.stat-label {
  @apply text-[10px] font-black uppercase tracking-widest mb-1 opacity-70;
}
.stat-value {
  @apply text-3xl font-black text-gray-900 dark:text-white;
}
</style>
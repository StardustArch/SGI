<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 md:py-8">
    
    <!-- Cabeçalho com botão voltar -->
    <div class="flex items-center gap-3 mb-6 md:mb-8">
      <button 
        @click="router.back()" 
        class="p-2 rounded-lg bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 text-slate-500 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800 hover:text-slate-700 dark:hover:text-slate-300 transition shadow-sm"
      >
        <BootstrapIcon name="arrow-left" class="w-5 h-5" />
      </button>
      <h1 class="text-xl md:text-2xl font-bold text-slate-900 dark:text-white">Perfil do Educando</h1>
    </div>

    <!-- Loading -->
    <div v-if="pendingPerfil" class="flex flex-col items-center justify-center py-20 space-y-4">
      <div class="animate-spin h-8 w-8 border-2 border-blue-600 border-t-transparent rounded-full"></div>
      <p class="text-sm text-slate-500 dark:text-slate-400 font-medium">A carregar perfil...</p>
    </div>

    <div v-else class="space-y-6 md:space-y-8">
      
      <!-- Cabeçalho do Estudante -->
      <section class="bg-white dark:bg-slate-900 rounded-xl p-5 md:p-6 border border-slate-200 dark:border-slate-800 shadow-sm">
        <div class="flex flex-col md:flex-row items-center md:items-start gap-5 md:gap-6">
          <div class="h-20 w-20 md:h-24 md:w-24 rounded-full bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 flex items-center justify-center text-2xl md:text-3xl font-bold border border-blue-100 dark:border-blue-800 shrink-0">
            {{ getIniciais(estudante?.nome_completo || '') }}
          </div>
          <div class="text-center md:text-left flex-1 min-w-0">
            <h2 class="text-xl md:text-2xl font-bold text-slate-900 dark:text-white mb-2 break-words">
              {{ estudante?.nome_completo }}
            </h2>
            <div class="flex flex-wrap justify-center md:justify-start gap-2 mb-4">
              <span class="px-2.5 py-0.5 rounded-md bg-slate-100 dark:bg-slate-800 text-xs font-medium border border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-300">
                {{ estudante?.curso }}
              </span>
              <span class="px-2.5 py-0.5 rounded-md bg-slate-100 dark:bg-slate-800 text-xs font-medium border border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-300">
                Quarto {{ estudante?.quarto_numero || 'N/A' }}
              </span>
              <span :class="[
                'px-2.5 py-0.5 rounded-md text-xs font-medium border',
                estudante?.estado === 'Activo' 
                  ? 'bg-emerald-50 text-emerald-700 border-emerald-200 dark:bg-emerald-900/20 dark:text-emerald-400 dark:border-emerald-800/30' 
                  : 'bg-red-50 text-red-700 border-red-200 dark:bg-red-900/20 dark:text-red-400 dark:border-red-800/30'
              ]">
                {{ estudante?.estado }}
              </span>
            </div>
            <div class="text-sm text-slate-500 dark:text-slate-400">
              <span class="block text-xs font-medium text-slate-400 dark:text-slate-500 mb-0.5">Encarregado</span>
              {{ estudante?.encarregado_nome || '—' }}
            </div>
          </div>
        </div>
      </section>

      <!-- Abas -->
      <div class="flex p-1 bg-slate-100 dark:bg-slate-800 rounded-xl overflow-x-auto max-w-full no-scrollbar">
        <button 
          v-for="tab in ['Resumo', 'Financeiro', 'Presenças', 'Disciplina']" 
          :key="tab"
          @click="activeTab = tab"
          :class="[
            'px-4 sm:px-6 py-2.5 rounded-lg text-sm font-medium transition-all whitespace-nowrap',
            activeTab === tab 
              ? 'bg-white dark:bg-slate-900 text-blue-600 dark:text-white shadow-sm' 
              : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
          ]"
        >
          {{ tab }}
        </button>
      </div>

      <!-- Conteúdo das abas -->
      <div class="mt-6">
        
        <!-- Aba Resumo -->
        <div v-if="activeTab === 'Resumo'" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-5">
          <!-- Card Financeiro -->
          <div @click="activeTab = 'Financeiro'" class="group bg-white dark:bg-slate-900 rounded-xl p-5 border border-slate-200 dark:border-slate-800 shadow-sm hover:border-blue-200 dark:hover:border-blue-800 hover:shadow-md transition-all cursor-pointer">
            <div class="flex justify-between items-start mb-4">
              <div class="h-12 w-12 rounded-lg bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 flex items-center justify-center group-hover:scale-110 transition-transform">
                <BootstrapIcon name="cash-coin" class="w-6 h-6" />
              </div>
              <BootstrapIcon name="chevron-right" class="w-5 h-5 text-slate-300 dark:text-slate-600" />
            </div>
            <h3 class="text-xs font-medium text-slate-500 dark:text-slate-400 uppercase tracking-wider mb-1">Situação Financeira</h3>
            <div v-if="dividaTotal > 0">
              <p class="text-2xl font-bold text-amber-600 dark:text-amber-400">{{ dividaTotal }} fatura(s)</p>
              <p class="text-xs text-slate-400 dark:text-slate-500 mt-1">Pendente / Em atraso</p>
            </div>
            <div v-else>
              <p class="text-2xl font-bold text-emerald-600 dark:text-emerald-400">Em Dia</p>
              <p class="text-xs text-slate-400 dark:text-slate-500 mt-1">Nenhum valor pendente</p>
            </div>
            <div :class="['absolute top-0 left-0 w-full h-1 rounded-t-xl', dividaTotal > 0 ? 'bg-amber-500' : 'bg-emerald-500']"></div>
          </div>

          <!-- Card Presenças -->
          <div @click="activeTab = 'Presenças'" class="group bg-white dark:bg-slate-900 rounded-xl p-5 border border-slate-200 dark:border-slate-800 shadow-sm hover:border-blue-200 dark:hover:border-blue-800 hover:shadow-md transition-all cursor-pointer relative">
            <div class="flex justify-between items-start mb-4">
              <div class="h-12 w-12 rounded-lg bg-indigo-50 dark:bg-indigo-900/30 text-indigo-600 dark:text-indigo-400 flex items-center justify-center group-hover:scale-110 transition-transform">
                <BootstrapIcon name="calendar-check" class="w-6 h-6" />
              </div>
              <BootstrapIcon name="chevron-right" class="w-5 h-5 text-slate-300 dark:text-slate-600" />
            </div>
            <h3 class="text-xs font-medium text-slate-500 dark:text-slate-400 uppercase tracking-wider mb-1">Última Presença</h3>
            <div v-if="ultimaPresenca">
              <p :class="['text-2xl font-bold', ultimaPresenca.estado === 'Presente' ? 'text-emerald-600 dark:text-emerald-400' : 'text-rose-600 dark:text-rose-400']">
                {{ ultimaPresenca.estado }}
              </p>
              <p class="text-xs text-slate-400 dark:text-slate-500 mt-1 capitalize">{{ formatDataRecente(ultimaPresenca.data_presenca) }}</p>
            </div>
            <div v-else>
              <p class="text-2xl font-bold text-slate-400 dark:text-slate-500">Sem registos</p>
            </div>
            <div :class="['absolute top-0 left-0 w-full h-1 rounded-t-xl', ultimaPresenca?.estado === 'Presente' ? 'bg-emerald-500' : (ultimaPresenca ? 'bg-rose-500' : 'bg-slate-300')]"></div>
          </div>

          <!-- Card Disciplina -->
          <div @click="activeTab = 'Disciplina'" class="group bg-white dark:bg-slate-900 rounded-xl p-5 border border-slate-200 dark:border-slate-800 shadow-sm hover:border-blue-200 dark:hover:border-blue-800 hover:shadow-md transition-all cursor-pointer relative">
            <div class="flex justify-between items-start mb-4">
              <div class="h-12 w-12 rounded-lg bg-amber-50 dark:bg-amber-900/30 text-amber-600 dark:text-amber-400 flex items-center justify-center group-hover:scale-110 transition-transform">
                <BootstrapIcon name="shield-exclamation" class="w-6 h-6" />
              </div>
              <BootstrapIcon name="chevron-right" class="w-5 h-5 text-slate-300 dark:text-slate-600" />
            </div>
            <h3 class="text-xs font-medium text-slate-500 dark:text-slate-400 uppercase tracking-wider mb-1">Comportamento</h3>
            <div v-if="totalSancoes === 0">
              <p class="text-2xl font-bold text-emerald-600 dark:text-emerald-400">Exemplar</p>
              <p class="text-xs text-slate-400 dark:text-slate-500 mt-1">Nenhuma sanção</p>
            </div>
            <div v-else>
              <p class="text-2xl font-bold text-rose-600 dark:text-rose-400">{{ totalSancoes }} Sanção(s)</p>
              <p class="text-xs text-slate-400 dark:text-slate-500 mt-1">Registada(s)</p>
            </div>
            <div :class="['absolute top-0 left-0 w-full h-1 rounded-t-xl', totalSancoes > 0 ? 'bg-rose-500' : 'bg-emerald-500']"></div>
          </div>
        </div>

        <!-- Aba Financeiro -->
        <div v-else-if="activeTab === 'Financeiro'" class="space-y-4">
          <div v-if="loadingFinanceiro" class="text-center py-10 text-slate-500">Carregando...</div>
          <div v-else-if="mensalidades.length === 0" class="text-center py-10 text-slate-500">Nenhuma mensalidade encontrada.</div>
          <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div v-for="item in mensalidades" :key="item.id" class="bg-white dark:bg-slate-900 p-4 rounded-xl border border-slate-200 dark:border-slate-800 flex justify-between items-center">
              <div>
                <p class="font-semibold text-slate-900 dark:text-white">{{ formatMes(item.mes_referencia) }}</p>
                <p class="text-xs text-slate-500 dark:text-slate-400">{{ item.tipo || 'Mensalidade' }}</p>
              </div>
              <div class="text-right">
                <p :class="item.estado === 'Pago' ? 'text-emerald-600 dark:text-emerald-400' : 'text-amber-600 dark:text-amber-400'">{{ formatMoeda(item.valor_pago) }}</p>
                <span :class="[
                  'text-xs px-2 py-0.5 rounded-md font-medium',
                  item.estado === 'Pago' 
                    ? 'bg-emerald-50 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-300' 
                    : 'bg-amber-50 text-amber-700 dark:bg-amber-900/30 dark:text-amber-300'
                ]">{{ item.estado }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Aba Presenças -->
        <div v-else-if="activeTab === 'Presenças'" class="space-y-4">
          <div v-if="loadingPresencas" class="text-center py-10 text-slate-500">Carregando...</div>
          <div v-else-if="presencas.length === 0" class="text-center py-10 text-slate-500">Nenhum registo de presença.</div>
          <div v-else class="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div v-for="item in presencas" :key="item.id" class="bg-white dark:bg-slate-900 p-3 rounded-lg border border-slate-200 dark:border-slate-800 flex justify-between items-center">
              <span class="text-sm">{{ formatDate(item.data_presenca) }} <span class="text-slate-400">({{ item.periodo || 'Manhã' }})</span></span>
              <span :class="[
                'text-sm font-medium',
                item.estado === 'Presente' ? 'text-emerald-600 dark:text-emerald-400' : 
                (item.estado === 'Ausente' ? 'text-rose-600 dark:text-rose-400' : 'text-amber-600 dark:text-amber-400')
              ]">{{ item.estado }}</span>
            </div>
          </div>
        </div>

        <!-- Aba Disciplina -->
        <div v-else-if="activeTab === 'Disciplina'" class="space-y-4">
          <div v-if="loadingSancoes" class="text-center py-10 text-slate-500">Carregando...</div>
          <div v-else-if="sancoes.length === 0" class="text-center py-10 text-slate-500">Nenhuma sanção registada.</div>
          <div v-else class="space-y-3">
            <div v-for="item in sancoes" :key="item.id" class="bg-white dark:bg-slate-900 p-4 rounded-xl border border-slate-200 dark:border-slate-800">
              <div class="flex flex-wrap justify-between gap-2 mb-2">
                <span class="font-semibold text-slate-900 dark:text-white">{{ formatDate(item.data_ocorrencia) }}</span>
                <span class="text-xs px-2 py-0.5 rounded-md bg-rose-50 text-rose-700 dark:bg-rose-900/30 dark:text-rose-300 font-medium">{{ item.tipo_sancao }}</span>
              </div>
              <p class="text-sm text-slate-600 dark:text-slate-300">{{ item.descricao }}</p>
              <p v-if="item.notificado_encarregado" class="text-xs text-emerald-600 dark:text-emerald-400 mt-2 flex items-center gap-1">
                <span class="inline-block w-1 h-1 rounded-full bg-emerald-500"></span>
                Encarregado notificado
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const { api } = useApi()

const studentId = route.params.id as string
const activeTab = ref('Resumo')

// Dados do perfil (cabeçalho + resumos)
const { data: perfilData, pending: pendingPerfil } = await useAsyncData(
  `guardian-student-${studentId}`,
  async () => {
    const [estudante, finStats, presencasList, sancoesList] = await Promise.all([
      api<any>(`/guardian/students/${studentId}/`),
      api<any>(`/guardian/financial/summary/?estudante=${studentId}`).catch(() => ({ faturas_pendentes: 0, faturas_atraso: 0 })),
      api<any>(`/guardian/attendance/?estudante=${studentId}&page_size=1`).catch(() => ({ results: [] })),
      api<any>(`/guardian/discipline/?estudante=${studentId}&page_size=1`).catch(() => ({ count: 0 }))
    ])
    return { estudante, finStats, ultimaPresenca: presencasList.results?.[0] || null, totalSancoes: sancoesList.count || 0 }
  }
)

const estudante = computed(() => perfilData.value?.estudante)
const dividaTotal = computed(() => (perfilData.value?.finStats?.faturas_pendentes || 0) + (perfilData.value?.finStats?.faturas_atraso || 0))
const ultimaPresenca = computed(() => perfilData.value?.ultimaPresenca)
const totalSancoes = computed(() => perfilData.value?.totalSancoes)

// Dados para as abas (carregados sob demanda)
const mensalidades = ref<any[]>([])
const presencas = ref<any[]>([])
const sancoes = ref<any[]>([])
const loadingFinanceiro = ref(false)
const loadingPresencas = ref(false)
const loadingSancoes = ref(false)

async function carregarFinanceiro() {
  if (mensalidades.value.length > 0) return
  loadingFinanceiro.value = true
  try {
    const res = await api<any>(`/guardian/financial/?estudante=${studentId}`)
    mensalidades.value = res.results || res
  } catch (e) { console.error(e) } 
  finally { loadingFinanceiro.value = false }
}

async function carregarPresencas() {
  if (presencas.value.length > 0) return
  loadingPresencas.value = true
  try {
    const res = await api<any>(`/guardian/attendance/?estudante=${studentId}`)
    presencas.value = res.results || res
  } catch (e) { console.error(e) } 
  finally { loadingPresencas.value = false }
}

async function carregarSancoes() {
  if (sancoes.value.length > 0) return
  loadingSancoes.value = true
  try {
    const res = await api<any>(`/guardian/discipline/?estudante=${studentId}`)
    sancoes.value = res.results || res
  } catch (e) { console.error(e) } 
  finally { loadingSancoes.value = false }
}

watch(activeTab, (tab) => {
  if (tab === 'Financeiro') carregarFinanceiro()
  else if (tab === 'Presenças') carregarPresencas()
  else if (tab === 'Disciplina') carregarSancoes()
}, { immediate: true })

// Helpers
const getIniciais = (nome: string) => {
  const limpo = (nome || '').trim()
  if (!limpo) return '??'
  const partes = limpo.split(/\s+/)
  return ((partes[0]?.[0] || '') + (partes.length > 1 ? partes[partes.length - 1]?.[0] || '' : '')).toUpperCase()
}
const formatMoeda = (v: any) => new Intl.NumberFormat('pt-MZ', { style: 'currency', currency: 'MZN' }).format(Number(v))
const formatMes = (d: string) => new Date(d).toLocaleDateString('pt-PT', { month: 'long', year: 'numeric' })
const formatDate = (d: string) => new Date(d).toLocaleDateString('pt-PT')
const formatDataRecente = (dataStr: string) => {
  if (!dataStr) return ''
  const hoje = new Date().toISOString().split('T')[0]
  return dataStr === hoje ? 'Hoje' : new Date(dataStr).toLocaleDateString('pt-PT', { day: 'numeric', month: 'long' })
}
</script>

<style scoped>
/* Esconder scrollbar em navegadores modernos */
.no-scrollbar::-webkit-scrollbar {
  display: none;
}
.no-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>
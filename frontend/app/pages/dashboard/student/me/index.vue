<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 md:py-8">
    
    <!-- Loading -->
    <div v-if="pending" class="flex flex-col items-center justify-center py-20 space-y-4">
      <div class="animate-spin h-8 w-8 border-2 border-blue-600 border-t-transparent rounded-full"></div>
      <p class="text-sm text-slate-500 dark:text-slate-400 font-medium">A carregar o seu perfil...</p>
    </div>

    <div v-else class="space-y-6 md:space-y-8">
      
      <!-- Cabeçalho do Estudante -->
      <section class="bg-white dark:bg-slate-900 rounded-xl p-5 md:p-6 border border-slate-200 dark:border-slate-800 shadow-sm flex flex-col sm:flex-row items-start sm:items-center gap-4 sm:gap-6">
        <div class="h-16 w-16 sm:h-20 sm:w-20 rounded-full bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 flex items-center justify-center text-xl sm:text-2xl font-bold border border-blue-100 dark:border-blue-800 shrink-0">
          {{ getIniciais(perfil?.nome_completo || '') }}
        </div>

        <div class="flex-grow min-w-0">
          <h2 class="text-lg sm:text-xl font-bold text-slate-900 dark:text-white mb-1 break-words">
            {{ perfil?.nome_completo }}
          </h2>
          <div class="flex flex-wrap items-center gap-2 mb-2 sm:mb-3">
            <span class="px-2.5 py-0.5 rounded-md bg-slate-100 dark:bg-slate-800 text-xs font-medium border border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-300">
              {{ perfil?.curso }}
            </span>
            <span class="px-2.5 py-0.5 rounded-md bg-slate-100 dark:bg-slate-800 text-xs font-medium border border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-300">
              Quarto {{ perfil?.quarto_numero || 'N/A' }}
            </span>
            <span :class="['px-2.5 py-0.5 rounded-md text-xs font-medium border', perfil?.estado === 'Activo' ? 'bg-emerald-50 text-emerald-700 border-emerald-200 dark:bg-emerald-900/20 dark:text-emerald-400 dark:border-emerald-800/30' : 'bg-red-50 text-red-700 border-red-200 dark:bg-red-900/20 dark:text-red-400 dark:border-red-800/30']">
              {{ perfil?.estado }}
            </span>
          </div>
          <p class="text-sm text-slate-500 dark:text-slate-400">
            Encarregado: {{ perfil?.encarregado_nome || '—' }} • Tel: {{ perfil?.encarregado_telefone || '—' }}
          </p>
        </div>
      </section>

      <!-- Abas -->
      <div class="flex p-1 bg-slate-100 dark:bg-slate-800 rounded-xl overflow-x-auto max-w-full no-scrollbar">
        <button 
          v-for="tab in ['Financeiro', 'Presenças', 'Disciplina', 'Saídas']" 
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
        
        <!-- Aba Financeiro -->
        <div v-if="activeTab === 'Financeiro'" class="space-y-5 md:space-y-6">
          <!-- Cards de estatísticas -->
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            <div class="bg-white dark:bg-slate-900 p-5 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm">
              <p class="text-xs font-medium text-slate-500 dark:text-slate-400 mb-1">Total Pago</p>
              <p class="text-2xl font-bold text-emerald-600 dark:text-emerald-400">{{ formatMoeda(finStats.total_pago) }}</p>
            </div>
            <div class="bg-white dark:bg-slate-900 p-5 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm">
              <p class="text-xs font-medium text-slate-500 dark:text-slate-400 mb-1">Pendentes</p>
              <p class="text-2xl font-bold text-amber-600 dark:text-amber-400">{{ finStats.pendentes }}</p>
            </div>
            <div class="bg-white dark:bg-slate-900 p-5 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm">
              <p class="text-xs font-medium text-slate-500 dark:text-slate-400 mb-1">Valor Mensal</p>
              <p class="text-2xl font-bold text-blue-600 dark:text-blue-400">2500,00 MT</p>
            </div>
          </div>

          <!-- Lista de mensalidades -->
          <div v-if="loadingFin" class="text-center py-10 text-slate-500">A carregar mensalidades...</div>
          <div v-else-if="mensalidades.length === 0" class="text-center py-10 text-slate-500">Nenhuma mensalidade encontrada.</div>
          <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div v-for="item in mensalidades" :key="item.id" class="bg-white dark:bg-slate-900 p-4 rounded-xl border border-slate-200 dark:border-slate-800 flex flex-wrap sm:flex-nowrap justify-between items-center gap-2">
              <div class="min-w-0">
                <p class="font-semibold text-slate-900 dark:text-white">{{ formatMes(item.mes_referencia) }}</p>
                <p class="text-xs text-slate-500 dark:text-slate-400">{{ item.tipo || 'Mensalidade' }}</p>
                <p v-if="item.estado === 'Pago'" class="text-xs text-slate-400 mt-0.5">Pago em {{ formatDate(item.data_pagamento_confirmado) }}</p>
              </div>
              <div class="text-right shrink-0">
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
        <div v-else-if="activeTab === 'Presenças'" class="space-y-5">
          <!-- Filtros -->
          <div class="flex flex-wrap gap-2">
            <button 
              v-for="estado in ['Todos', 'Presente', 'Ausente', 'Justificado']" 
              :key="estado" 
              @click="filtroPresenca = estado === 'Todos' ? null : estado" 
              :class="[
                'px-3 sm:px-4 py-2 text-xs sm:text-sm font-medium rounded-lg whitespace-nowrap border transition-colors',
                (filtroPresenca === estado || (estado === 'Todos' && !filtroPresenca)) 
                  ? 'bg-white dark:bg-slate-900 text-blue-600 dark:text-white border-blue-200 dark:border-blue-800 shadow-sm' 
                  : 'bg-transparent border-transparent text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800'
              ]"
            >
              {{ estado }}
            </button>
          </div>

          <div v-if="loadingPres" class="text-center py-10 text-slate-500">A carregar presenças...</div>
          <div v-else-if="presencasFiltradas.length === 0" class="text-center py-10 text-slate-500">Nenhum registo de presença.</div>
          <div v-else class="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div v-for="item in presencasFiltradas" :key="item.id" class="bg-white dark:bg-slate-900 p-3 rounded-lg border border-slate-200 dark:border-slate-800 flex justify-between items-center">
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
        <div v-else-if="activeTab === 'Disciplina'" class="space-y-5">
          <!-- Filtros -->
          <div class="flex flex-wrap gap-2">
            <button 
              v-for="tipo in ['Todos', 'Advertência Verbal', 'Trabalho Comunitário', 'Suspensão de Saída']" 
              :key="tipo" 
              @click="filtroSancao = tipo === 'Todos' ? null : tipo" 
              :class="[
                'px-3 sm:px-4 py-2 text-xs sm:text-sm font-medium rounded-lg whitespace-nowrap border transition-colors',
                (filtroSancao === tipo || (tipo === 'Todos' && !filtroSancao)) 
                  ? 'bg-white dark:bg-slate-900 text-blue-600 dark:text-white border-blue-200 dark:border-blue-800 shadow-sm' 
                  : 'bg-transparent border-transparent text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800'
              ]"
            >
              {{ tipo }}
            </button>
          </div>

          <div v-if="loadingSanc" class="text-center py-10 text-slate-500">A carregar sanções...</div>
          <div v-else-if="sancoesFiltradas.length === 0" class="text-center py-10 text-slate-500">Nenhuma sanção registada.</div>
          <div v-else class="space-y-3">
            <div v-for="item in sancoesFiltradas" :key="item.id" class="bg-white dark:bg-slate-900 p-4 rounded-xl border border-slate-200 dark:border-slate-800">
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

        <!-- Aba Saídas -->
        <div v-else-if="activeTab === 'Saídas'" class="space-y-6">
          <!-- Formulário de criação -->
          <div class="bg-slate-50 dark:bg-slate-800/50 p-5 md:p-6 rounded-xl border border-slate-200 dark:border-slate-700">
            <h3 class="text-base font-semibold text-slate-900 dark:text-white mb-5 border-b border-slate-200 dark:border-slate-700 pb-3">Nova Solicitação de Saída</h3>
            <form @submit.prevent="criarPedido" class="space-y-4">
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <input v-model="novoPedido.data_saida_pretendida" type="date" required class="input" />
                <input v-model="novoPedido.data_retorno_pretendida" type="date" required class="input" />
              </div>
              <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <input v-model="novoPedido.destino" type="text" placeholder="Destino (ex: Casa)" class="input" />
                <input v-model="novoPedido.cidade_destino" type="text" placeholder="Cidade" class="input" />
                <input v-model="novoPedido.meio_transporte" type="text" placeholder="Meio de transporte" class="input" />
              </div>
              <textarea v-model="novoPedido.motivo" rows="2" required placeholder="Motivo da saída..." class="input"></textarea>
              <div class="flex justify-end">
                <button 
                  type="submit" 
                  :disabled="criando" 
                  class="px-6 py-2.5 rounded-lg bg-blue-600 hover:bg-blue-700 text-white font-medium text-sm transition-colors disabled:opacity-60 disabled:cursor-not-allowed min-h-[44px]"
                >
                  <span v-if="criando" class="inline-flex items-center gap-2">
                    <span class="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full"></span>
                    Enviando...
                  </span>
                  <span v-else>Enviar Pedido</span>
                </button>
              </div>
            </form>
            <div v-if="msgSucesso" class="mt-4 p-3 bg-emerald-50 text-emerald-800 dark:bg-emerald-900/20 dark:text-emerald-400 rounded-lg text-sm border border-emerald-200 dark:border-emerald-800/30">{{ msgSucesso }}</div>
            <div v-if="msgErro" class="mt-4 p-3 bg-red-50 text-red-800 dark:bg-red-900/20 dark:text-red-400 rounded-lg text-sm border border-red-200 dark:border-red-800/30">{{ msgErro }}</div>
          </div>

          <!-- Lista de pedidos -->
          <div v-if="loadingSaidas" class="text-center py-10 text-slate-500">A carregar pedidos de saída...</div>
          <div v-else-if="pedidos.length === 0" class="text-center py-10 text-slate-500">Nenhum pedido de saída.</div>
          <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div v-for="item in pedidos" :key="item.id" class="bg-white dark:bg-slate-900 p-4 rounded-xl border border-slate-200 dark:border-slate-800">
              <div class="flex flex-wrap justify-between gap-2 mb-3">
                <span class="font-semibold text-slate-900 dark:text-white text-sm">
                  {{ formatDate(item.data_saida_pretendida) }} → {{ formatDate(item.data_retorno_pretendida) }}
                </span>
                <span :class="getStatusBadge(item.estado)">{{ getStatusLabel(item.estado) }}</span>
              </div>
              <p class="text-sm text-slate-600 dark:text-slate-300 mb-2">{{ item.motivo }}</p>
              <div class="flex flex-wrap gap-x-3 gap-y-1 text-xs text-slate-500 dark:text-slate-400 mb-2">
                <span v-if="item.destino">{{ item.destino }}</span>
                <span v-if="item.cidade_destino">{{ item.cidade_destino }}</span>
                <span v-if="item.meio_transporte">{{ item.meio_transporte }}</span>
              </div>
              <div v-if="item.motivo_rejeicao" class="mt-3 text-xs text-rose-700 dark:text-rose-300 bg-rose-50 dark:bg-rose-900/20 p-2 rounded-md border border-rose-200 dark:border-rose-800/30">
                <strong>Rejeitado:</strong> {{ item.motivo_rejeicao }}
              </div>
              <div v-if="item.observacao_admin" class="mt-3 text-xs text-amber-700 dark:text-amber-300 bg-amber-50 dark:bg-amber-900/20 p-2 rounded-md border border-amber-200 dark:border-amber-800/30">
                <strong>Observação:</strong> {{ item.observacao_admin }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const { api } = useApi()
const route = useRoute()

const activeTab = ref((route.query.tab as string) || 'Financeiro')
const pending = ref(true)

// Dados do perfil
const perfil = ref<any>(null)

// Financeiro
const mensalidades = ref<any[]>([])
const loadingFin = ref(false)
const finStats = reactive({ total_pago: 0, pendentes: 0 })

// Presenças
const presencas = ref<any[]>([])
const loadingPres = ref(false)
const filtroPresenca = ref<string | null>(null)

// Sanções
const sancoes = ref<any[]>([])
const loadingSanc = ref(false)
const filtroSancao = ref<string | null>(null)

// Saídas
const pedidos = ref<any[]>([])
const loadingSaidas = ref(false)
const novoPedido = reactive({
  data_saida_pretendida: '',
  data_retorno_pretendida: '',
  motivo: '',
  destino: '',
  cidade_destino: '',
  meio_transporte: ''
})
const criando = ref(false)
const msgSucesso = ref('')
const msgErro = ref('')

// Computed com filtros
const presencasFiltradas = computed(() => {
  if (!filtroPresenca.value) return presencas.value
  return presencas.value.filter(p => p.estado === filtroPresenca.value)
})

const sancoesFiltradas = computed(() => {
  if (!filtroSancao.value) return sancoes.value
  return sancoes.value.filter(s => s.tipo_sancao === filtroSancao.value)
})

// Carregar tudo
onMounted(async () => {
  try {
    const [perfilRes, finRes, presRes, sancRes, saidasRes] = await Promise.all([
      api('/student/me/'),
      api('/student/financial/'),
      api('/student/attendance/'),
      api('/student/discipline/'),
      api('/student/exits/')
    ])
    perfil.value = perfilRes
    mensalidades.value = finRes.results || finRes
    presencas.value = presRes.results || presRes
    sancoes.value = sancRes.results || sancRes
    pedidos.value = saidasRes.results || saidasRes

    // Calcular stats financeiras
    const pagos = mensalidades.value.filter((m: any) => m.estado === 'Pago')
    finStats.total_pago = pagos.reduce((acc: number, m: any) => acc + Number(m.valor_pago), 0)
    finStats.pendentes = mensalidades.value.filter((m: any) => m.estado !== 'Pago').length
  } catch (e) {
    console.error('Erro ao carregar perfil', e)
  } finally {
    pending.value = false
  }
})

// Criar pedido de saída
async function criarPedido() {
  criando.value = true
  msgSucesso.value = ''
  msgErro.value = ''
  try {
    await api('/student/exits/', { method: 'POST', body: novoPedido })
    msgSucesso.value = 'Pedido enviado com sucesso!'
    // Limpar formulário
    Object.assign(novoPedido, { data_saida_pretendida: '', data_retorno_pretendida: '', motivo: '', destino: '', cidade_destino: '', meio_transporte: '' })
    // Recarregar lista
    const saidasRes = await api('/student/exits/')
    pedidos.value = saidasRes.results || saidasRes
  } catch (e: any) {
    msgErro.value = e.response?._data?.erro || 'Erro ao enviar pedido.'
  } finally {
    criando.value = false
  }
}

// Helpers
const getIniciais = (nome: string) => {
  const partes = (nome || '').trim().split(/\s+/)
  return ((partes[0]?.[0] || '') + (partes.length > 1 ? partes[partes.length - 1]?.[0] || '' : '')).toUpperCase()
}
const formatMoeda = (v: any) => new Intl.NumberFormat('pt-MZ', { style: 'currency', currency: 'MZN' }).format(Number(v))
const formatMes = (d: string) => new Date(d).toLocaleDateString('pt-PT', { month: 'long', year: 'numeric' })
const formatDate = (d: string) => new Date(d).toLocaleDateString('pt-PT')
const getStatusBadge = (e: string) => {
  if (e === 'Autorizado') return 'px-2.5 py-0.5 rounded-md text-xs font-medium bg-emerald-50 text-emerald-700 border border-emerald-200 dark:bg-emerald-900/30 dark:text-emerald-300 dark:border-emerald-800/30'
  if (e === 'Rejeitado') return 'px-2.5 py-0.5 rounded-md text-xs font-medium bg-rose-50 text-rose-700 border border-rose-200 dark:bg-rose-900/30 dark:text-rose-300 dark:border-rose-800/30'
  return 'px-2.5 py-0.5 rounded-md text-xs font-medium bg-amber-50 text-amber-700 border border-amber-200 dark:bg-amber-900/30 dark:text-amber-300 dark:border-amber-800/30'
}
const getStatusLabel = (e: string) => {
  if (e === 'Aguardando_Encarregado') return 'Aguardando Encarregado'
  return e
}
</script>

<style scoped>
.input {
  @apply w-full px-4 py-2.5 bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-lg text-sm text-slate-900 dark:text-white placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors;
}

/* Esconder scrollbar em navegadores modernos */
.no-scrollbar::-webkit-scrollbar {
  display: none;
}
.no-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>
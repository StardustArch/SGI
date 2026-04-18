<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 md:py-8">
    
    <!-- Cabeçalho -->
    <div class="mb-6 md:mb-8">
      <h1 class="text-2xl md:text-3xl font-bold text-slate-900 dark:text-white">Autorizações de Saída</h1>
      <p class="text-sm md:text-base text-slate-500 dark:text-slate-400 mt-1">Gerencie e autorize os pedidos de saída do internato.</p>
    </div>

    <!-- Abas e Filtro -->
    <div class="flex flex-col md:flex-row justify-between items-stretch md:items-center gap-4 mb-6">
      
      <!-- Abas -->
      <div class="flex p-1 bg-slate-100 dark:bg-slate-800 rounded-xl overflow-x-auto w-full md:w-auto">
        <button 
          @click="abaAtiva = 'acao'; page = 1"
          :class="[
            'px-5 sm:px-6 py-2.5 rounded-lg text-sm font-medium transition-all whitespace-nowrap flex items-center gap-2',
            abaAtiva === 'acao' 
              ? 'bg-white dark:bg-slate-900 text-blue-600 dark:text-white shadow-sm' 
              : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
          ]"
        >
          <span v-if="qtdPendentesAcao > 0" class="inline-flex items-center justify-center h-5 min-w-[1.25rem] px-1.5 rounded-full bg-rose-500 text-white text-xs font-bold">
            {{ qtdPendentesAcao }}
          </span>
          <span v-else class="w-2 h-2 rounded-full bg-rose-500"></span>
          Para Aprovar
        </button>
        
        <button 
          @click="abaAtiva = 'historico'; page = 1"
          :class="[
            'px-5 sm:px-6 py-2.5 rounded-lg text-sm font-medium transition-all whitespace-nowrap',
            abaAtiva === 'historico' 
              ? 'bg-white dark:bg-slate-900 text-slate-900 dark:text-white shadow-sm' 
              : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
          ]"
        >
          Histórico Geral
        </button>
      </div>

      <!-- Filtro por Educando -->
      <div class="w-full md:w-64">
        <select 
          v-model="filtroEstudante" 
          @change="page = 1"
          class="w-full appearance-none bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-lg py-2.5 px-3 text-sm text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 cursor-pointer"
        >
          <option :value="null">Todos os Educandos</option>
          <option v-for="filho in educandos" :key="filho.utilizador_id" :value="filho.utilizador_id">
            {{ filho.nome_completo }}
          </option>
        </select>
      </div>
    </div>

    <!-- Conteúdo -->
    <div>
      <div v-if="pending" class="flex flex-col items-center justify-center py-20 space-y-4">
        <div class="animate-spin h-8 w-8 border-2 border-blue-600 border-t-transparent rounded-full"></div>
        <p class="text-sm text-slate-500 dark:text-slate-400 font-medium">A carregar pedidos...</p>
      </div>

      <div v-else-if="pedidosComNome.length === 0" class="flex flex-col items-center justify-center py-16 md:py-24 bg-slate-50/50 dark:bg-slate-800/50 rounded-xl border border-slate-200 dark:border-slate-700 text-center">
        <div class="bg-white dark:bg-slate-900 p-5 rounded-full shadow-sm mb-4">
          <BootstrapIcon v-if="abaAtiva === 'acao'" name="check-circle" class="w-10 h-10 text-emerald-500" />
          <BootstrapIcon v-else name="clock-history" class="w-10 h-10 text-slate-400" />
        </div>
        <h3 class="text-lg font-semibold text-slate-900 dark:text-white">
          {{ abaAtiva === 'acao' ? 'Tudo em dia!' : 'Sem histórico' }}
        </h3>
        <p class="text-sm text-slate-500 dark:text-slate-400 mt-1 max-w-xs mx-auto">
          {{ abaAtiva === 'acao' ? 'Não existem pedidos a aguardar a sua aprovação.' : 'Nenhum pedido de saída foi encontrado.' }}
        </p>
      </div>

      <div v-else class="grid grid-cols-1 lg:grid-cols-2 gap-5 md:gap-6 mb-8">
        
        <div 
          v-for="item in pedidosComNome" 
          :key="item.id"
          class="bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-md transition-shadow flex flex-col overflow-hidden"
        >
          <!-- Barra de status colorida -->
          <div :class="['h-1.5 w-full', getStatusColor(item.estado)]"></div>

          <div class="p-5 md:p-6 flex-1">
            <!-- Cabeçalho do card -->
            <div class="flex flex-wrap justify-between items-start gap-3 mb-5">
               <div class="flex items-center gap-3">
                 <div class="h-12 w-12 rounded-full bg-slate-100 dark:bg-slate-800 flex items-center justify-center font-semibold text-slate-600 dark:text-slate-300 text-base border border-slate-200 dark:border-slate-700">
                    {{ getIniciais(item.estudante_nome) }}
                 </div>
                 <div>
                   <h3 class="font-semibold text-slate-900 dark:text-white">{{ item.estudante_nome }}</h3>
                   <p class="text-xs text-slate-500 dark:text-slate-400">Submetido: {{ formatDate(item.data_submissao) }}</p>
                 </div>
               </div>
               <span :class="['px-2.5 py-0.5 rounded-md text-xs font-medium border', getStatusBadge(item.estado)]">
                 {{ getStatusLabel(item.estado) }}
               </span>
            </div>

            <!-- Datas -->
            <div class="flex gap-4 mb-5">
               <div class="flex-1 bg-slate-50 dark:bg-slate-800/50 rounded-lg p-3 border border-slate-200 dark:border-slate-700 flex flex-col items-center text-center">
                  <span class="text-xs font-medium text-slate-500 dark:text-slate-400 mb-1">Saída</span>
                  <div class="flex items-center gap-1 text-rose-600 dark:text-rose-400">
                     <BootstrapIcon name="box-arrow-right" class="w-4 h-4" />
                     <span class="text-sm font-semibold">{{ formatDateShort(item.data_saida_pretendida) }}</span>
                  </div>
               </div>
               
               <div class="flex-1 bg-slate-50 dark:bg-slate-800/50 rounded-lg p-3 border border-slate-200 dark:border-slate-700 flex flex-col items-center text-center">
                  <span class="text-xs font-medium text-slate-500 dark:text-slate-400 mb-1">Retorno</span>
                  <div class="flex items-center gap-1 text-emerald-600 dark:text-emerald-400">
                     <BootstrapIcon name="box-arrow-in-left" class="w-4 h-4" />
                     <span class="text-sm font-semibold">{{ formatDateShort(item.data_retorno_pretendida) }}</span>
                  </div>
               </div>
            </div>

            <!-- Detalhes -->
            <div class="mb-2">
              <span class="text-xs font-medium text-slate-500 dark:text-slate-400 uppercase tracking-wide">Motivo:</span>
              <p class="text-sm text-slate-700 dark:text-slate-300 italic mt-1">"{{ item.motivo }}"</p>
            </div>
            <div v-if="item.destino || item.cidade_destino || item.meio_transporte" class="grid grid-cols-1 sm:grid-cols-3 gap-2 mt-3 text-xs">
              <div v-if="item.destino"><span class="text-slate-500 dark:text-slate-400">Destino:</span> <span class="text-slate-700 dark:text-slate-300">{{ item.destino }}</span></div>
              <div v-if="item.cidade_destino"><span class="text-slate-500 dark:text-slate-400">Cidade:</span> <span class="text-slate-700 dark:text-slate-300">{{ item.cidade_destino }}</span></div>
              <div v-if="item.meio_transporte"><span class="text-slate-500 dark:text-slate-400">Transporte:</span> <span class="text-slate-700 dark:text-slate-300">{{ item.meio_transporte }}</span></div>
            </div>
            <div v-if="item.motivo_rejeicao" class="mt-4 p-3 bg-rose-50 dark:bg-rose-900/20 rounded-lg text-xs text-rose-700 dark:text-rose-300 border border-rose-200 dark:border-rose-800/30">
              <strong>Motivo da rejeição:</strong> {{ item.motivo_rejeicao }}
            </div>
          </div>

          <!-- Ações (se pendente) -->
          <div v-if="item.estado === 'Aguardando_Encarregado'" class="p-4 md:p-5 bg-slate-50 dark:bg-slate-800/30 border-t border-slate-200 dark:border-slate-700">
             <textarea 
               v-model="motivosRejeicao[item.id]" 
               placeholder="Motivo da rejeição (obrigatório ao rejeitar)" 
               class="w-full text-sm p-3 bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-lg mb-3 focus:outline-none focus:ring-2 focus:ring-rose-500"
               rows="2"
             ></textarea>
             <div class="grid grid-cols-2 gap-3">
               <button 
                 @click="processarAcao(item.id, 'Rejeitado')" 
                 :disabled="loadingId === item.id" 
                 class="px-4 py-2.5 rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300 font-medium text-sm hover:bg-rose-50 dark:hover:bg-rose-900/20 transition-colors disabled:opacity-50"
               >
                 Rejeitar
               </button>
               <button 
                 @click="processarAcao(item.id, 'Autorizado')" 
                 :disabled="loadingId === item.id" 
                 class="px-4 py-2.5 rounded-lg bg-blue-600 hover:bg-blue-700 text-white font-medium text-sm transition-colors disabled:opacity-50 flex justify-center items-center gap-2"
               >
                 <span v-if="loadingId === item.id" class="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full"></span>
                 Autorizar
               </button>
             </div>
          </div>
          <div v-else class="p-4 bg-slate-50 dark:bg-slate-800/30 border-t border-slate-200 dark:border-slate-700 text-center text-xs text-slate-500 dark:text-slate-400">
            Processo finalizado
          </div>
        </div>
      </div>

      <!-- Paginação -->
      <div v-if="pedidosComNome.length > 0" class="flex justify-center items-center gap-4 pb-6">
        <button 
          @click="page--" 
          :disabled="!data?.pedidos?.previous" 
          class="h-10 w-10 rounded-lg border border-slate-200 dark:border-slate-700 flex items-center justify-center text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800 disabled:opacity-40 disabled:cursor-not-allowed transition"
        >
          <BootstrapIcon name="chevron-left" class="w-5 h-5" />
        </button>
        <span class="text-sm font-medium text-slate-600 dark:text-slate-400">Página {{ page }}</span>
        <button 
          @click="page++" 
          :disabled="!data?.pedidos?.next" 
          class="h-10 w-10 rounded-lg border border-slate-200 dark:border-slate-700 flex items-center justify-center text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800 disabled:opacity-40 disabled:cursor-not-allowed transition"
        >
          <BootstrapIcon name="chevron-right" class="w-5 h-5" />
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { useRoute } from 'vue-router'

const { api } = useApi()
const route = useRoute()

const page = ref(1)
const abaAtiva = ref('acao')
const filtroEstudante = ref<number | null>(route.query.student ? Number(route.query.student) : null)
const loadingId = ref<number | null>(null)
const motivosRejeicao = reactive<Record<number, string>>({})

// Buscar educandos
const { data: educandosRaw } = await useAsyncData('guardian-educandos-exits', () => api<any>('/guardian/students/'))

const educandos = computed(() => {
  const raw = educandosRaw.value
  if (!raw) return []
  const list = Array.isArray(raw) ? raw : (raw.results || [])
  return list.filter((item: any) => item && typeof item === 'object' && item.utilizador_id)
})

// Buscar pedidos com filtros
const { data, pending, refresh } = await useAsyncData(
  'guardian-pedidos',
  async () => {
    const params: any = { page: page.value }
    if (filtroEstudante.value) params.estudante = filtroEstudante.value
    if (abaAtiva.value === 'acao') params.estado = 'Aguardando_Encarregado'
    const pedidos = await api<any>('/guardian/exits/', { params })
    return { pedidos }
  },
  { watch: [page, filtroEstudante, abaAtiva] }
)

const pedidosComNome = computed(() => {
  if (!data.value?.pedidos?.results || !educandos.value) return []
  let lista = data.value.pedidos.results
  if (abaAtiva.value === 'historico') {
    lista = lista.filter((p: any) => p.estado !== 'Aguardando_Encarregado')
  }
  const mapaNomes = new Map(educandos.value.map((e: any) => [e.utilizador_id, e.nome_completo]))
  return lista.map((item: any) => ({
    ...item,
    estudante_nome: item.estudante_nome || mapaNomes.get(item.estudante) || 'Desconhecido'
  }))
})

const qtdPendentesAcao = computed(() => 
  abaAtiva.value === 'acao' ? data.value?.pedidos?.count || 0 : 0
)

// Ação de aprovar/rejeitar
const processarAcao = async (id: number, novoEstado: string) => {
  const motivo = motivosRejeicao[id] || ''
  if (novoEstado === 'Rejeitado' && !motivo) {
    alert('Indique o motivo da rejeição.')
    return
  }
  loadingId.value = id
  try {
    const body: any = { estado: novoEstado }
    if (novoEstado === 'Rejeitado') body.motivo_rejeicao = motivo
    await api(`/guardian/exits/${id}/`, { method: 'PATCH', body })
    delete motivosRejeicao[id]
    refresh()
  } catch (e) {
    alert('Erro ao processar.')
  } finally {
    loadingId.value = null
  }
}

// Helpers visuais
const getStatusColor = (estado: string) => {
  const map: Record<string, string> = {
    'Autorizado': 'bg-emerald-500',
    'Rejeitado': 'bg-rose-500',
    'Aguardando_Encarregado': 'bg-amber-500',
  }
  return map[estado] || 'bg-blue-500'
}

const getStatusBadge = (estado: string) => {
  const map: Record<string, string> = {
    'Autorizado': 'bg-emerald-50 text-emerald-700 border-emerald-200 dark:bg-emerald-900/20 dark:text-emerald-400 dark:border-emerald-800/30',
    'Rejeitado': 'bg-rose-50 text-rose-700 border-rose-200 dark:bg-rose-900/20 dark:text-rose-400 dark:border-rose-800/30',
    'Aguardando_Encarregado': 'bg-amber-50 text-amber-700 border-amber-200 dark:bg-amber-900/20 dark:text-amber-400 dark:border-amber-800/30',
  }
  return map[estado] || 'bg-slate-100 text-slate-700 border-slate-200 dark:bg-slate-800 dark:text-slate-300'
}

const getStatusLabel = (estado: string) => {
  return estado === 'Aguardando_Encarregado' ? 'Requer Aprovação' : estado
}

const formatDate = (d: string) => new Date(d).toLocaleDateString('pt-PT')
const formatDateShort = (d: string) => new Date(d).toLocaleDateString('pt-PT', { day: '2-digit', month: 'short' }).toUpperCase()
const getIniciais = (nome: string) => {
  const partes = (nome || '').trim().split(/\s+/)
  return ((partes[0]?.[0] || '') + (partes.length > 1 ? partes[partes.length - 1]?.[0] || '' : '')).toUpperCase()
}
</script>
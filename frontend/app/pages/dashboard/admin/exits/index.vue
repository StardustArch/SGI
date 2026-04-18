<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 md:py-8">
    
    <!-- Cabeçalho -->
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6">
      <div>
        <h1 class="text-2xl md:text-3xl font-bold text-slate-900 dark:text-white">Triagem de Saídas</h1>
        <p class="text-sm md:text-base text-slate-500 dark:text-slate-400 mt-1">Analise e dê o parecer inicial aos pedidos de saída dos internos.</p>
      </div>

      <!-- Filtros -->
      <div class="flex p-1 bg-slate-100 dark:bg-slate-800 rounded-xl">
        <button 
          @click="filtroEstado = 'Pendente'; refresh()"
          :class="[
            'px-4 sm:px-5 py-2 text-sm font-medium rounded-lg transition-all whitespace-nowrap',
            filtroEstado === 'Pendente' 
              ? 'bg-white dark:bg-slate-900 text-blue-600 dark:text-white shadow-sm' 
              : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
          ]"
        >
          Pendentes
        </button>
        <button 
          @click="filtroEstado = ''; refresh()"
          :class="[
            'px-4 sm:px-5 py-2 text-sm font-medium rounded-lg transition-all whitespace-nowrap',
            filtroEstado === '' 
              ? 'bg-white dark:bg-slate-900 text-slate-900 dark:text-white shadow-sm' 
              : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
          ]"
        >
          Todos
        </button>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="pending" class="grid grid-cols-1 md:grid-cols-2 gap-4 md:gap-5">
      <div v-for="i in 4" :key="i" class="h-64 bg-slate-100 dark:bg-slate-800 animate-pulse rounded-xl"></div>
    </div>

    <!-- Empty state -->
    <div v-else-if="pedidos?.length === 0" class="text-center py-16 bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800">
      <BootstrapIcon name="check-circle" class="w-12 h-12 text-emerald-500 dark:text-emerald-400 mx-auto mb-3" />
      <p class="text-slate-500 dark:text-slate-400 font-medium">Não há pedidos pendentes de análise.</p>
    </div>

    <!-- Grid de Pedidos -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4 md:gap-5">
      <div 
        v-for="pedido in pedidos" 
        :key="pedido.id"
        class="bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-md transition-shadow flex flex-col overflow-hidden"
      >
        <!-- Barra de status -->
        <div :class="['h-1.5 w-full', getStatusColor(pedido.estado)]"></div>
        
        <div class="p-5 md:p-6 space-y-4">
          <!-- Cabeçalho do card -->
          <div class="flex flex-wrap justify-between items-start gap-3">
            <div class="flex items-center gap-3">
              <div class="h-12 w-12 rounded-full bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 flex items-center justify-center font-semibold text-base border border-blue-100 dark:border-blue-800 shrink-0">
                {{ pedido.estudante_nome?.charAt(0).toUpperCase() }}
              </div>
              <div>
                <h3 class="font-semibold text-slate-900 dark:text-white">{{ pedido.estudante_nome }}</h3>
                <p class="text-xs text-slate-500 dark:text-slate-400 mt-0.5">Submetido em: {{ formatDate(pedido.data_submissao) }}</p>
              </div>
            </div>
            <span :class="[
              'px-2.5 py-0.5 rounded-md text-xs font-medium border',
              getStatusBadge(pedido.estado)
            ]">
              {{ pedido.estado }}
            </span>
          </div>

          <!-- Informações de destino/transporte -->
          <div v-if="pedido.destino || pedido.cidade_destino || pedido.meio_transporte" class="bg-slate-50 dark:bg-slate-800/50 p-3 rounded-lg border border-slate-200 dark:border-slate-700">
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-2 text-xs">
              <div v-if="pedido.cidade_destino">
                <span class="text-slate-500 dark:text-slate-400 font-medium">Cidade:</span>
                <span class="font-medium ml-1 text-slate-700 dark:text-slate-300">{{ pedido.cidade_destino }}</span>
              </div>
              <div v-if="pedido.destino">
                <span class="text-slate-500 dark:text-slate-400 font-medium">Destino:</span>
                <span class="font-medium ml-1 truncate max-w-[150px] text-slate-700 dark:text-slate-300" :title="pedido.destino">{{ pedido.destino }}</span>
              </div>
              <div v-if="pedido.meio_transporte">
                <span class="text-slate-500 dark:text-slate-400 font-medium">Transporte:</span>
                <span class="font-medium ml-1 text-slate-700 dark:text-slate-300">{{ pedido.meio_transporte }}</span>
              </div>
            </div>
          </div>

          <!-- Datas -->
          <div class="grid grid-cols-2 gap-3">
            <div class="bg-slate-50 dark:bg-slate-800/50 p-3 rounded-lg border border-slate-200 dark:border-slate-700 text-center">
              <p class="text-xs font-medium text-slate-500 dark:text-slate-400 uppercase mb-1">Saída</p>
              <p class="font-semibold text-rose-600 dark:text-rose-400">{{ formatDateShort(pedido.data_saida_pretendida) }}</p>
            </div>
            <div class="bg-slate-50 dark:bg-slate-800/50 p-3 rounded-lg border border-slate-200 dark:border-slate-700 text-center">
              <p class="text-xs font-medium text-slate-500 dark:text-slate-400 uppercase mb-1">Retorno</p>
              <p class="font-semibold text-emerald-600 dark:text-emerald-400">{{ formatDateShort(pedido.data_retorno_pretendida) }}</p>
            </div>
          </div>

          <!-- Motivo -->
          <div class="bg-slate-50 dark:bg-slate-800/30 p-3 rounded-lg border border-slate-200 dark:border-slate-700 italic text-sm text-slate-600 dark:text-slate-300">
            "{{ pedido.motivo }}"
          </div>

          <!-- Ações (apenas para pedidos pendentes) -->
          <div v-if="pedido.estado === 'Pendente'" class="flex flex-col gap-3 pt-2">
            <textarea 
              v-model="observacoes[pedido.id]" 
              placeholder="Motivo da rejeição (obrigatório se rejeitar) ou observação administrativa..."
              class="w-full text-sm p-3 bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
              rows="2"
            ></textarea>
            
            <div class="grid grid-cols-2 gap-3">
              <button 
                @click="decidirPedido(pedido.id, 'Rejeitado')"
                class="py-2.5 rounded-lg border border-slate-300 dark:border-slate-700 font-medium text-sm text-slate-700 dark:text-slate-300 hover:bg-rose-50 dark:hover:bg-rose-900/20 hover:border-rose-200 dark:hover:border-rose-800 transition-colors"
              >
                Rejeitar Pedido
              </button>
              <button 
                @click="decidirPedido(pedido.id, 'Aguardando_Encarregado')"
                class="py-2.5 rounded-lg bg-blue-600 hover:bg-blue-700 text-white font-medium text-sm transition-colors"
              >
                Aprovar (Fase 1)
              </button>
            </div>
            <button 
              @click="decidirPedido(pedido.id, 'Autorizado', true)"
              class="py-2.5 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white font-medium text-sm transition-colors"
            >
              Autorizar (Contacto Telefónico)
            </button>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'

const { api } = useApi()

const filtroEstado = ref('Pendente')
const observacoes = reactive<Record<number, string>>({})

// 1. Carregar Pedidos
const { data: pedidosRaw, pending, refresh } = await useAsyncData(
  'admin-pedidos-saida',
  () => api<any>('/admin/pedidos-saida/', { params: { estado: filtroEstado.value } }),
  { watch: [filtroEstado] }
)

const pedidos = computed(() => {
  const raw = pedidosRaw.value
  if (!raw) return []
  return raw.results ?? raw
})

// 2. Ação de Aprovar/Rejeitar
async function decidirPedido(id: number, novoEstado: string, aprovacaoDireta = false) {
  const obs = observacoes[id] || ""
  
  if (novoEstado === 'Rejeitado' && !obs) {
    alert("Por favor, indique o motivo da rejeição.")
    return
  }
  if (aprovacaoDireta && !obs) {
    alert("Por favor, indique na observação que o encarregado foi contactado.")
    return
  }

  try {
    const body: any = {
      estado: novoEstado,
    }
    
    if (novoEstado === 'Rejeitado') {
      body.motivo_rejeicao = obs
    } else if (novoEstado === 'Aguardando_Encarregado' && obs) {
      body.observacao_admin = obs
    }
    
    await api(`/admin/pedidos-saida/${id}/`, {
      method: 'PATCH',
      body
    })
    delete observacoes[id]
    refresh()
    alert(novoEstado === 'Rejeitado' ? "Pedido rejeitado." : "Pedido aprovado! Agora aguarda autorização do encarregado.")
  } catch (e) {
    alert("Erro ao processar decisão.")
  }
}

// Helpers
const getStatusColor = (e: string) => {
  const map: Record<string, string> = {
    'Autorizado': 'bg-emerald-500',
    'Rejeitado': 'bg-rose-500',
    'Aguardando_Encarregado': 'bg-amber-500',
  }
  return map[e] || 'bg-blue-500'
}

const getStatusBadge = (e: string) => {
  const map: Record<string, string> = {
    'Autorizado': 'bg-emerald-50 text-emerald-700 border-emerald-200 dark:bg-emerald-900/20 dark:text-emerald-400 dark:border-emerald-800/30',
    'Rejeitado': 'bg-rose-50 text-rose-700 border-rose-200 dark:bg-rose-900/20 dark:text-rose-400 dark:border-rose-800/30',
    'Aguardando_Encarregado': 'bg-amber-50 text-amber-700 border-amber-200 dark:bg-amber-900/20 dark:text-amber-400 dark:border-amber-800/30',
  }
  return map[e] || 'bg-slate-100 text-slate-600 border-slate-200 dark:bg-slate-800 dark:text-slate-400'
}

const formatDate = (d: string) => new Date(d).toLocaleString('pt-PT')
const formatDateShort = (d: string) => new Date(d).toLocaleDateString('pt-PT', { day:'2-digit', month:'short' }).toUpperCase()
</script>
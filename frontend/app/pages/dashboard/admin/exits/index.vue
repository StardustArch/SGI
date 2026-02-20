<template>
  <div class="space-y-8 dark:text-white max-w-7xl mx-auto p-4 md:p-8">
    
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
      <div>
        <h1 class="text-3xl font-bold text-gray-800 dark:text-white tracking-tight">Triagem de Saídas</h1>
        <p class="text-stone-500 dark:text-gray-400 mt-1">Analise e dê o parecer inicial aos pedidos de saída dos internos.</p>
      </div>

      <div class="bg-stone-100 dark:bg-gray-800 p-1 rounded-xl flex gap-1">
        <button 
          @click="filtroEstado = 'Pendente'; refresh()"
          :class="['px-4 py-2 text-xs font-bold rounded-lg transition-all', filtroEstado === 'Pendente' ? 'bg-white shadow-sm text-rose-600' : 'text-stone-500']"
        >
          Pendentes
        </button>
        <button 
          @click="filtroEstado = ''; refresh()"
          :class="['px-4 py-2 text-xs font-bold rounded-lg transition-all', filtroEstado === null ? 'bg-white shadow-sm text-gray-800' : 'text-stone-500']"
        >
          Todos
        </button>
      </div>
    </div>

    <div v-if="pending" class="grid grid-cols-1 md:grid-cols-2 gap-6">
       <div v-for="i in 4" :key="i" class="h-64 bg-stone-100 dark:bg-gray-800 animate-pulse rounded-[2rem]"></div>
    </div>

    <div v-else-if="pedidos?.length === 0" class="text-center py-20 bg-stone-50 dark:bg-gray-800/50 rounded-[2rem] border border-dashed border-stone-200">
        <BootstrapIcon name="check2-all" class="text-4xl text-emerald-500 mb-2" />
        <p class="text-stone-500">Não há pedidos pendentes de análise.</p>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div 
        v-for="pedido in pedidos" 
        :key="pedido.id"
        class="bg-white dark:bg-gray-800 rounded-[2rem] border border-stone-100 dark:border-gray-700 shadow-sm hover:shadow-md transition-all flex flex-col overflow-hidden"
      >
        <div :class="['h-1.5 w-full', getStatusColor(pedido.estado)]"></div>
        
        <div class="p-6 md:p-8 space-y-6">
          <div class="flex justify-between items-start">
            <div class="flex items-center gap-3">
              <div class="w-12 h-12 rounded-2xl bg-stone-50 dark:bg-gray-700 flex items-center justify-center font-bold text-rose-500 border border-stone-100">
                {{ pedido.estudante_nome?.charAt(0) }}
              </div>
              <div>
                <h3 class="font-bold text-lg leading-none">{{ pedido.estudante_nome }}</h3>
                <p class="text-xs text-stone-400 mt-1">Submetido em: {{ formatDate(pedido.data_submissao) }}</p>
              </div>
            </div>
            <span :class="['px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-wide border', getStatusBadge(pedido.estado)]">
              {{ pedido.estado }}
            </span>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div class="bg-stone-50 dark:bg-gray-700/50 p-3 rounded-2xl border border-stone-100 text-center">
              <p class="text-[10px] font-bold text-stone-400 uppercase">Saída</p>
              <p class="font-bold text-rose-500">{{ formatDateShort(pedido.data_saida_pretendida) }}</p>
            </div>
            <div class="bg-stone-50 dark:bg-gray-700/50 p-3 rounded-2xl border border-stone-100 text-center">
              <p class="text-[10px] font-bold text-stone-400 uppercase">Retorno</p>
              <p class="font-bold text-emerald-500">{{ formatDateShort(pedido.data_retorno_pretendida) }}</p>
            </div>
          </div>

          <div class="bg-stone-50 dark:bg-gray-700/30 p-4 rounded-2xl border border-stone-100 italic text-sm text-stone-600 dark:text-gray-300">
            "{{ pedido.motivo }}"
          </div>

          <div v-if="pedido.estado === 'Pendente'" class="flex flex-col gap-3">
            <textarea 
              v-model="observacoes[pedido.id]" 
              placeholder="Adicionar observação ou motivo de rejeição..."
              class="w-full text-xs p-3 bg-stone-50 dark:bg-gray-900 border border-stone-100 rounded-xl focus:ring-2 focus:ring-rose-200 outline-none"
            ></textarea>
            
            <div class="grid grid-cols-2 gap-3">
              <button 
                @click="decidirPedido(pedido.id, 'Rejeitado')"
                class="py-3 rounded-xl border border-stone-200 font-bold text-xs hover:bg-rose-50 hover:text-rose-600 transition-colors"
              >
                Rejeitar Pedido
              </button>
              <button 
                @click="decidirPedido(pedido.id, 'Aguardando_Encarregado')"
                class="py-3 rounded-xl bg-gray-900 dark:bg-white text-white dark:text-gray-900 font-bold text-xs shadow-lg hover:opacity-90 transition-all"
              >
                Aprovar (Fase 1)
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const { api } = useApi()

const filtroEstado = ref('Pendente')
const observacoes = reactive<Record<number, string>>({})

// 1. Carregar Pedidos
const { data: pedidos, pending, refresh } = await useAsyncData(
  'admin-pedidos-saida',
  () => api<any[]>('/admin/pedidos-saida/', { params: { estado: filtroEstado.value } }),
  { watch: [filtroEstado] }
)

// 2. Ação de Aprovar/Rejeitar
async function decidirPedido(id: number, novoEstado: string) {
  const obs = observacoes[id] || ""
  
  if (novoEstado === 'Rejeitado' && !obs) {
    alert("Por favor, indique o motivo da rejeição na observação.")
    return
  }

  try {
    await api(`/admin/pedidos-saida/${id}/`, {
      method: 'PATCH',
      body: {
        estado: novoEstado,
        observacao_admin: obs
      }
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
  if (e === 'Autorizado') return 'bg-emerald-500'
  if (e === 'Rejeitado') return 'bg-rose-500'
  if (e === 'Aguardando_Encarregado') return 'bg-amber-400'
  return 'bg-blue-400'
}

const getStatusBadge = (e: string) => {
  if (e === 'Autorizado') return 'bg-emerald-50 text-emerald-700'
  if (e === 'Rejeitado') return 'bg-rose-50 text-rose-700'
  return 'bg-stone-100 text-stone-600'
}

const formatDate = (d: string) => new Date(d).toLocaleString('pt-PT')
const formatDateShort = (d: string) => new Date(d).toLocaleDateString('pt-PT', { day:'2-digit', month:'short' }).toUpperCase()
</script>
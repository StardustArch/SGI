<template>
  <div class="space-y-8 dark:text-white max-w-7xl mx-auto p-4 md:p-8">
    
    <div class="flex flex-col md:flex-row justify-between items-start md:items-end gap-4">
      <div>
        <h1 class="text-3xl font-bold text-gray-800 dark:text-white tracking-tight">Pedidos de Saída</h1>
        <p class="text-stone-500 dark:text-gray-400 mt-1 text-lg">Solicite autorização para sair do internato.</p>
      </div>

      <button 
        @click="showForm = !showForm"
        class="px-6 py-3 rounded-xl bg-gray-900 dark:bg-white text-white dark:text-gray-900 font-bold text-sm hover:opacity-90 shadow-lg shadow-stone-200 dark:shadow-none transition-all flex items-center gap-2"
      >
        <BootstrapIcon :name="showForm ? 'x-lg' : 'plus-lg'" />
        {{ showForm ? 'Cancelar Pedido' : 'Nova Solicitação' }}
      </button>
    </div>

    <div v-show="showForm" class="bg-white dark:bg-gray-800 rounded-[2rem] p-8 border border-stone-100 dark:border-gray-700 shadow-xl relative overflow-hidden transition-all">
      
      <div class="absolute top-0 right-0 w-32 h-32 bg-rose-50 rounded-full -mr-10 -mt-10 dark:bg-gray-700 opacity-50"></div>
      
      <h3 class="text-lg font-bold text-gray-800 dark:text-white mb-6 relative z-10">Preencha os detalhes da saída</h3>

      <div v-if="successMsg" class="mb-6 p-4 rounded-xl bg-emerald-50 text-emerald-700 border border-emerald-100 flex items-center gap-3">
         <BootstrapIcon name="check-circle-fill" class="w-5 h-5" />
         {{ successMsg }}
      </div>
      <div v-if="errorMsg" class="mb-6 p-4 rounded-xl bg-rose-50 text-rose-700 border border-rose-100 flex items-center gap-3">
         <BootstrapIcon name="exclamation-triangle-fill" class="w-5 h-5" />
         {{ errorMsg }}
      </div>

      <form @submit.prevent="handleCreate" class="space-y-6 relative z-10">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="space-y-1">
            <label class="text-xs font-bold text-stone-500 uppercase ml-1">Data de Saída</label>
            <input 
              v-model="newEntry.data_saida_pretendida" 
              type="date" 
              required
              class="w-full bg-stone-50 dark:bg-gray-700 border border-stone-200 dark:border-gray-600 rounded-xl py-3 px-4 focus:outline-none focus:ring-2 focus:ring-rose-200 transition-all font-medium text-gray-700 dark:text-white" 
            />
          </div>
          <div class="space-y-1">
            <label class="text-xs font-bold text-stone-500 uppercase ml-1">Data de Retorno</label>
            <input 
              v-model="newEntry.data_retorno_pretendida" 
              type="date" 
              required
              class="w-full bg-stone-50 dark:bg-gray-700 border border-stone-200 dark:border-gray-600 rounded-xl py-3 px-4 focus:outline-none focus:ring-2 focus:ring-rose-200 transition-all font-medium text-gray-700 dark:text-white" 
            />
          </div>
        </div>
        
        <div class="space-y-1">
          <label class="text-xs font-bold text-stone-500 uppercase ml-1">Motivo / Destino</label>
          <textarea 
            v-model="newEntry.motivo" 
            rows="3" 
            required 
            placeholder="Ex: Visitar a família em Maputo..."
            class="w-full bg-stone-50 dark:bg-gray-700 border border-stone-200 dark:border-gray-600 rounded-xl py-3 px-4 focus:outline-none focus:ring-2 focus:ring-rose-200 transition-all font-medium text-gray-700 dark:text-white resize-none"
          ></textarea>
        </div>

        <div class="flex justify-end pt-2">
           <button 
             type="submit" 
             :disabled="pendingCreate"
             class="px-8 py-3 rounded-xl bg-rose-500 text-white font-bold text-sm hover:bg-rose-600 shadow-lg shadow-rose-200 dark:shadow-none transition-all disabled:opacity-50 flex items-center gap-2"
           >
             <span v-if="pendingCreate" class="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full"></span>
             {{ pendingCreate ? 'A submeter...' : 'Enviar Pedido' }}
           </button>
        </div>
      </form>
    </div>

    <div>
      
      <div v-if="pendingList" class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div v-for="n in 2" :key="n" class="bg-white dark:bg-gray-800 rounded-[2rem] p-6 shadow-sm border border-stone-100 dark:border-gray-700 animate-pulse h-48"></div>
      </div>

      <div v-else-if="pedidos.length === 0" class="flex flex-col items-center justify-center py-20 bg-stone-50/50 dark:bg-gray-800/50 rounded-[2rem] border border-stone-100 dark:border-gray-700 text-center">
        <div class="bg-white p-4 rounded-full shadow-sm mb-4">
          <BootstrapIcon name="send" class="w-10 h-10 text-stone-300" />
        </div>
        <h3 class="text-lg font-bold text-gray-800 dark:text-white">Sem pedidos ativos</h3>
        <p class="text-stone-500 dark:text-gray-400 text-sm mt-1">Utilize o botão "Nova Solicitação" para pedir uma saída.</p>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        
        <div 
          v-for="item in pedidos" 
          :key="item.id"
          class="group bg-white dark:bg-gray-800 rounded-[2rem] p-0 shadow-sm hover:shadow-lg transition-all duration-300 border border-stone-100 dark:border-gray-700 relative overflow-hidden flex flex-col"
        >
          <div :class="['h-2 w-full', getStatusColor(item.estado)]"></div>

          <div class="p-6 md:p-8 flex-1 flex flex-col">
            
            <div class="flex justify-between items-start mb-6">
               <div>
                  <p class="text-[10px] font-bold text-stone-400 uppercase tracking-wider mb-1">Submetido a</p>
                  <p class="text-sm font-bold text-stone-600 dark:text-stone-300">{{ formatDate(item.data_submissao) }}</p>
               </div>
               
               <span :class="['px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-wide border', getStatusBadge(item.estado)]">
                 {{ getEstadoLegivel(item.estado) }}
               </span>
            </div>

            <div class="flex gap-4 mb-6">
               <div class="flex-1 bg-stone-50 dark:bg-gray-700/50 rounded-2xl p-3 border border-stone-100 dark:border-gray-600 flex flex-col items-center text-center">
                  <span class="text-[10px] font-bold text-stone-400 uppercase tracking-wider mb-1">Saída</span>
                  <div class="flex items-center gap-1 text-rose-500">
                     <BootstrapIcon name="box-arrow-right" class="w-4 h-4" />
                     <span class="text-sm font-bold">{{ formatDateShort(item.data_saida_pretendida) }}</span>
                  </div>
               </div>
               
               <div class="flex items-center text-stone-300">
                 <BootstrapIcon name="arrow-right" class="w-5 h-5" />
               </div>

               <div class="flex-1 bg-stone-50 dark:bg-gray-700/50 rounded-2xl p-3 border border-stone-100 dark:border-gray-600 flex flex-col items-center text-center">
                  <span class="text-[10px] font-bold text-stone-400 uppercase tracking-wider mb-1">Retorno</span>
                  <div class="flex items-center gap-1 text-emerald-600">
                     <BootstrapIcon name="box-arrow-in-left" class="w-4 h-4" />
                     <span class="text-sm font-bold">{{ formatDateShort(item.data_retorno_pretendida) }}</span>
                  </div>
               </div>
            </div>

            <div class="mb-4 flex-1">
               <span class="text-[10px] font-bold text-stone-400 uppercase tracking-wider">Motivo</span>
               <p class="text-sm text-stone-600 dark:text-gray-300 mt-1 italic leading-relaxed">"{{ item.motivo }}"</p>
            </div>

            <div v-if="item.observacao_admin" class="mt-4 pt-4 border-t border-stone-100 dark:border-gray-700">
               <span class="text-[10px] font-bold text-rose-400 uppercase tracking-wider flex items-center gap-1">
                 <BootstrapIcon name="info-circle-fill" /> Nota da Direção
               </span>
               <p class="text-xs text-rose-600 dark:text-rose-300 mt-1 font-medium bg-rose-50 dark:bg-rose-900/20 p-2 rounded-lg">
                 {{ item.observacao_admin }}
               </p>
            </div>

          </div>
        </div>

      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'

const { api } = useApi()

// --- Estado UI ---
const showForm = ref(false)
const pendingCreate = ref(false)
const errorMsg = ref<string | null>(null)
const successMsg = ref<string | null>(null)

// --- Form Data ---
const newEntry = reactive({
  data_saida_pretendida: '',
  data_retorno_pretendida: '',
  motivo: ''
})

// --- Carregar Lista ---
// Endpoint ajustado para o do perfil do estudante
const { data: pedidos, pending: pendingList, refresh: refreshPedidos } = await useAsyncData(
  'student-exits',
  () => api<any[]>('/student/exits/'),
  { lazy: true, default: () => [] }
)

// --- Ações ---
async function handleCreate() {
  pendingCreate.value = true
  errorMsg.value = null
  successMsg.value = null

  try {
    await api('/student/exits/', {
      method: 'POST',
      body: newEntry
    })
    
    successMsg.value = "Pedido submetido! Aguarde a aprovação."
    
    // Resetar
    newEntry.data_saida_pretendida = ''
    newEntry.data_retorno_pretendida = ''
    newEntry.motivo = ''
    showForm.value = false // Fecha o form para ver a lista
    
    // Atualizar Lista
    await refreshPedidos()

  } catch (err: any) {
    errorMsg.value = "Erro ao submeter. Verifique as datas (não podem ser no passado)."
  } finally {
    pendingCreate.value = false
  }
}

// --- Helpers de Estilo ---

function getEstadoLegivel(estado: string) {
  if (estado === 'Aprovado_Admin' || estado === 'Autorizado') return 'Aprovado'
  if (estado === 'Aguardando_Encarregado') return 'Pendente (Encarregado)'
  if (estado === 'Rejeitado') return 'Rejeitado'
  return 'Em Análise' // Pendente Admin
}

function getStatusColor(estado: string) {
  if (estado === 'Autorizado' || estado === 'Aprovado_Admin') return 'bg-emerald-500'
  if (estado === 'Rejeitado') return 'bg-rose-500'
  return 'bg-amber-400'
}

function getStatusBadge(estado: string) {
  if (estado === 'Autorizado' || estado === 'Aprovado_Admin') return 'bg-emerald-50 text-emerald-700 border-emerald-100 dark:bg-emerald-900/30 dark:text-emerald-300'
  if (estado === 'Rejeitado') return 'bg-rose-50 text-rose-700 border-rose-100 dark:bg-rose-900/30 dark:text-rose-300'
  return 'bg-amber-50 text-amber-700 border-amber-100 dark:bg-amber-900/30 dark:text-amber-300'
}

// Helpers Data
const formatDate = (d: string) => new Date(d).toLocaleDateString('pt-PT')
const formatDateShort = (d: string) => new Date(d).toLocaleDateString('pt-PT', {day:'2-digit', month:'short'}).toUpperCase()
</script>
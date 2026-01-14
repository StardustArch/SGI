<template>
  <div class="space-y-6 dark:text-white max-w-4xl">
    <h1 class="text-3xl font-bold">Meus Pedidos de Saída</h1>

    <details class="bg-white dark:bg-gray-800 p-4 rounded-lg shadow">
      <summary class="font-medium cursor-pointer text-gray-900 dark:text-white">Submeter Novo Pedido de Saída</summary>
      
      <div v-if="successMsg" class="mt-4 p-3 rounded-md bg-green-100 dark:bg-green-800 text-green-700 dark:text-green-200">
        {{ successMsg }}
      </div>
      <div v-if="errorMsg" class="mt-4 p-3 rounded-md bg-red-100 dark:bg-red-800 text-red-700 dark:text-red-200">
        {{ errorMsg }}
      </div>

      <form @submit.prevent="handleCreate" class="mt-4 space-y-3">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="label">Data de Saída Pretendida</label>
            <input v-model="newEntry.data_saida_pretendida" type="date" class="input" required />
          </div>
          <div>
            <label class="label">Data de Retorno Pretendida</label>
            <input v-model="newEntry.data_retorno_pretendida" type="date" class="input" required />
          </div>
        </div>
        <div>
          <label class="label">Motivo</label>
          <textarea v-model="newEntry.motivo" class="input" rows="3" required placeholder="Ex: Visitar família..."></textarea>
        </div>
        <button type="submit" :disabled="pendingCreate" class="btn-primary">
          {{ pendingCreate ? 'A submeter...' : 'Submeter Pedido' }}
        </button>
      </form>
    </details>

    <div class="overflow-x-auto bg-white dark:bg-gray-800 rounded-lg shadow">
      <table class="w-full">
        <thead class="bg-gray-50 dark:bg-gray-700">
          <tr>
            <th class="table-header">Data Submissão</th>
            <th class="table-header">Saída</th>
            <th class="table-header">Retorno</th>
            <th class="table-header">Estado</th>
            <th class="table-header">Observação (Admin)</th>
          </tr>
        </thead>
        <tbody class="divide-y dark:divide-gray-700">
          <tr v-if="pendingList" class="text-center">
            <td colspan="5" class="table-cell text-gray-500">A carregar histórico...</td>
          </tr>
          <tr v-else-if="pedidos.length === 0">
            <td colspan="5" class="table-cell text-center text-gray-500">Nenhum pedido de saída encontrado.</td>
          </tr>
          <tr v-for="item in pedidos" :key="item.id" class="hover:bg-gray-50 dark:hover:bg-gray-700">
            <td class="table-cell">{{ new Date(item.data_submissao).toLocaleString() }}</td>
            <td class="table-cell">{{ item.data_saida_pretendida }}</td>
            <td class="table-cell">{{ item.data_retorno_pretendida }}</td>
            <td class="table-cell">
              <span :class="getStatusClass(item.estado)">
                {{ getEstadoLegivel(item.estado) }}
              </span>
            </td>
            <td class="table-cell">{{ item.observacao_admin || 'N/A' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const { api } = useApi()

// --- Estado para Criar Novo ---
const pendingCreate = ref(false)
const errorMsg = ref<string | null>(null)
const successMsg = ref<string | null>(null)
const newEntry = ref({
  data_saida_pretendida: '',
  data_retorno_pretendida: '',
  motivo: ''
})

// --- Carregar a Lista de Pedidos ---
const { data: pedidos, pending: pendingList, refresh: refreshPedidos } = await useAsyncData(
  'estudante-pedidos',
  () => api<any[]>('/perfil/pedidos-saida/'),
  { lazy: true, default: () => [] } // Inicia como array vazio
)

// --- Funções ---

async function handleCreate() {
  pendingCreate.value = true
  errorMsg.value = null
  successMsg.value = null

  try {
    // Usar o 'api' (o seu composable)
    await api('/perfil/pedidos-saida/', {
      method: 'POST',
      body: newEntry.value
    })
    
    successMsg.value = "Pedido submetido com sucesso! Será notificado quando for revisto."
    
    // Limpar o formulário
    newEntry.value = { data_saida_pretendida: '', data_retorno_pretendida: '', motivo: '' }
    
    // Recarregar a lista de pedidos na tabela
    await refreshPedidos()

  } catch (err: any) {
    errorMsg.value = "Erro ao submeter o pedido."
  } finally {
    pendingCreate.value = false
  }
}

// --- Funções Helper (Estilo) ---
function getEstadoLegivel(estado: string) {
  if (estado === 'Aprovado_Admin') return 'Aprovado'
  if (estado === 'Rejeitado') return 'Rejeitado'
  return 'Pendente'
}

function getStatusClass(estado: string) {
  if (estado === 'Aprovado_Admin') return 'status-green'
  if (estado === 'Rejeitado') return 'status-red'
  return 'status-yellow'
}
</script>

<style scoped>
.label { @apply block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1; }
.input { @apply w-full px-3 py-2 border rounded-md shadow-sm bg-gray-50 dark:bg-gray-700 dark:text-white dark:border-gray-600; }
.btn-primary { @apply px-4 py-2 font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 disabled:opacity-50; }
.table-header { @apply px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase; }
.table-cell { @apply px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white; }
.status-green { @apply px-2 py-0.5 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800 dark:bg-green-800 dark:text-green-100; }
.status-yellow { @apply px-2 py-0.5 inline-flex text-xs leading-5 font-semibold rounded-full bg-yellow-100 text-yellow-800 dark:bg-yellow-800 dark:text-yellow-100; }
.status-red { @apply px-2 py-0.5 inline-flex text-xs leading-5 font-semibold rounded-full bg-red-100 text-red-800 dark:bg-red-800 dark:text-red-100; }
</style>
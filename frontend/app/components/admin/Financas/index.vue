<template>
  <div class="space-y-6">
    <!-- Secção de Adicionar Nova Mensalidade (como antes) -->
    <details class="bg-white dark:bg-gray-800 p-4 rounded-lg shadow">
      <summary class="font-medium cursor-pointer text-gray-900 dark:text-white">Registar Nova Mensalidade</summary>
      <form @submit.prevent="handleCreate" class="mt-4 space-y-3">
        <div>
          <label class="label">Mês de Referência (ex: 2025-12-01)</label>
          <input v-model="newEntry.mes_referencia" type="date" class="input" required />
        </div>
        <div>
          <label class="label">Estado Inicial</label>
          <select v-model="newEntry.estado" class="input">
            <option v-for="opt in opcoesEstado" :key="opt.value" :value="opt.value">
              {{ opt.label }}
            </option>
          </select>
        </div>
        <button type="submit" :disabled="pendingCreate" class="btn-primary">
          {{ pendingCreate ? 'A criar...' : 'Criar Registo Pendente' }}
        </button>
      </form>
    </details>

    <!-- Tabela do Histórico -->
    <div class="overflow-x-auto bg-white dark:bg-gray-800 rounded-lg shadow">
      <table class="w-full">
        <thead class="bg-gray-50 dark:bg-gray-700">
          <tr>
            <th class="table-header">Mês</th>
            <th class="table-header">Estado</th>
            <th class="table-header">Valor Pago</th>
            <th class="table-header">Método</th>
            <th class="table-header">Data Conf.</th>
            <th class="table-header">Ação</th>
          </tr>
        </thead>
        <tbody class="divide-y dark:divide-gray-700">
          <tr v-if="finances.length === 0">
            <td colspan="6" class="table-cell text-center text-gray-500">Nenhum registo financeiro.</td>
          </tr>
          <tr v-for="item in finances" :key="item.id" class="hover:bg-gray-50 dark:hover:bg-gray-700">
            <td class="table-cell">{{ item.mes_referencia }}</td>
            <td class="table-cell">
              <span :class="item.estado === 'Pago' ? 'status-green' : 'status-yellow'">
                {{ item.estado }}
              </span>
            </td>
            <td class="table-cell">{{ item.valor_pago }}</td>
            <td class="table-cell">{{ item.metodo_pagamento || 'N/A' }}</td>
            <td class="table-cell">{{ item.data_pagamento_confirmado || 'N/A' }}</td>
            <td class="table-cell">
              <!-- BOTÃO DE EDITAR (SUBSTITUI O 'CONFIRMAR') -->
              <button 
                @click="openEditModal(item)"
                class="font-medium text-blue-600 dark:text-blue-400 hover:underline"
              >
                Editar
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- MODAL DE EDIÇÃO -->
    <div v-if="isModalOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-xl w-full max-w-lg transform transition-all">
        <h3 class="text-lg font-medium text-gray-900 dark:text-white">Editar Mensalidade (ID: {{ editingItem.id }})</h3>
        
        <form @submit.prevent="handleUpdate" class="mt-4 space-y-4">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="label">Valor Pago</label>
              <input v-model="editingItem.valor_pago" type="number" step="0.01" class="input" />
            </div>
            <div>
              <label class="label">Data de Confirmação</label>
              <input v-model="editingItem.data_pagamento_confirmado" type="date" class="input" />
            </div>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="label">Método de Pagamento</label>
              <select v-model="editingItem.metodo_pagamento" class="input">
                <option :value="null">N/A</option>
                <option v-for="opt in opcoesMetodo" :key="opt.value" :value="opt.value">
                  {{ opt.label }}
                </option>
              </select>
            </div>
             <div>
              <label class="label">Estado</label>
              <select v-model="editingItem.estado" class="input">
                <option v-for="opt in opcoesEstado" :key="opt.value" :value="opt.value">
                  {{ opt.label }}
                </option>
              </select>
            </div>
          </div>

          <!-- Botões de Ação do Modal -->
          <div class="mt-6 flex justify-end space-x-3">
            <button 
              type="button" 
              @click="closeModal"
              class="px-4 py-2 bg-gray-200 dark:bg-gray-600 text-gray-800 dark:text-gray-200 rounded-md hover:bg-gray-300"
            >
              Cancelar
            </button>
            <button type="submit" :disabled="pendingUpdate" class="btn-primary">
              {{ pendingUpdate ? 'A salvar...' : 'Salvar Alterações' }}
            </button>
          </div>
        </form>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const props = defineProps({
  finances: { type: Array as () => any[], required: true },
  studentId: { type: String, required: true },
  opcoesEstado: { type: Array as () => { value: string, label: string }[], required: true },
  opcoesMetodo: { type: Array as () => { value: string, label: string }[], required: true }
})
const emit = defineEmits(['updateList'])
const { accessToken } = useAuth()

// --- Estado para Criar Novo ---
const pendingCreate = ref(false)
const newEntry = ref({
  mes_referencia: '',
  estado: 'Pendente',
  valor_pago: 0
})

// --- Estado para Edição (Modal) ---
const isModalOpen = ref(false)
const pendingUpdate = ref(false)
// Guarda uma cópia do item que estamos a editar
const editingItem = ref<any>(null)

// Função para CRIAR (como antes)
async function handleCreate() {
  pendingCreate.value = true
  try {
    await $fetch(`/api/v1/estudantes/${props.studentId}/mensalidades/`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${accessToken.value}` },
      body: newEntry.value
    })
    newEntry.value.mes_referencia = ''
    emit('updateList')
  } catch (err) {
    alert("Erro ao criar mensalidade. Já existe uma para este mês?")
  } finally {
    pendingCreate.value = false
  }
}

// --- Funções do Modal de Edição ---

function openEditModal(item: any) {
  // Cria uma cópia profunda (deep copy) para evitar
  // que o 'v-model' edite a tabela directamente
  editingItem.value = JSON.parse(JSON.stringify(item))
  isModalOpen.value = true
}

function closeModal() {
  isModalOpen.value = false
  editingItem.value = null
}

// Função para ATUALIZAR (Editar) - Substitui o 'confirmarPagamento'
async function handleUpdate() {
  if (!editingItem.value) return
  
  pendingUpdate.value = true
  try {
    await $fetch(`/api/v1/mensalidades/${editingItem.value.id}/`, {
      method: 'PATCH',
      headers: { Authorization: `Bearer ${accessToken.value}` },
      // Envia apenas os campos que o nosso Serializer de PATCH permite
      body: {
        estado: editingItem.value.estado,
        valor_pago: editingItem.value.valor_pago,
        data_pagamento_confirmado: editingItem.value.data_pagamento_confirmado,
        metodo_pagamento: editingItem.value.metodo_pagamento
      }
    })
    emit('updateList') // Recarrega a lista
    closeModal()      // Fecha o modal
  } catch (err) {
    alert("Erro ao atualizar pagamento.")
  } finally {
    pendingUpdate.value = false
  }
}
</script>

<style scoped>
.label { @apply block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1; }
.input { @apply w-full px-3 py-2 border rounded-md shadow-sm bg-gray-50 dark:bg-gray-700 dark:text-white dark:border-gray-600 focus:outline-none focus:ring-blue-500 focus:border-blue-500; }
.btn-primary { @apply px-4 py-2 font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 disabled:opacity-50; }
.table-header { @apply px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase; }
.table-cell { @apply px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white; }
.status-green { @apply px-2 py-0.5 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800 dark:bg-green-800 dark:text-green-100; }
.status-yellow { @apply px-2 py-0.5 inline-flex text-xs leading-5 font-semibold rounded-full bg-yellow-100 text-yellow-800 dark:bg-yellow-800 dark:text-yellow-100; }
</style>
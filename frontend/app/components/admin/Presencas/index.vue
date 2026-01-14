<template>
  <div class="space-y-6">
    <div class="overflow-x-auto bg-white dark:bg-gray-800 rounded-lg shadow">
      <table class="w-full">
        <thead class="bg-gray-50 dark:bg-gray-700">
          <tr>
            <th class="table-header">Data</th>
            <th class="table-header">Estado</th>
            <th class="table-header">Ações</th>
          </tr>
        </thead>
        <tbody class="divide-y dark:divide-gray-700">
          <tr v-if="attendance.length === 0">
            <td colspan="3" class="table-cell text-center text-gray-500">Nenhum registo de presença.</td>
          </tr>
          <tr v-for="item in attendance" :key="item.id" class="hover:bg-gray-50 dark:hover:bg-gray-700">
            <td class="table-cell">{{ item.data_presenca }}</td>
            <td class="table-cell">
              <span :class="getStatusClass(item.estado)">
                {{ item.estado }}
              </span>
            </td>
            <td class="table-cell space-x-3">
              <button @click="openEditModal(item)" class="font-medium text-blue-600 dark:text-blue-400 hover:underline">
                Corrigir
              </button>
              <button @click="openDeleteConfirm(item)" class="font-medium text-red-600 dark:text-red-400 hover:underline">
                Apagar
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="isEditModalOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-xl w-full max-w-md">
        <h3 class="text-lg font-medium text-gray-900 dark:text-white">Corrigir Registo de Presença</h3>
        
        <form @submit.prevent="handleUpdate" class="mt-4 space-y-4">
          <div>
            <label class="label">Data: {{ editingItem.data_presenca }}</label>
            <p class="text-sm text-gray-500">A alterar o estado para:</p>
            <select v-model="editingItem.estado" class="input mt-2">
              <option v-for="opt in opcoesEstado" :key="opt.value" :value="opt.value">
                {{ opt.label }}
              </option>
            </select>
          </div>
          <div class="mt-6 flex justify-end space-x-3">
            <button type="button" @click="closeModal" class="px-4 py-2 bg-gray-200 dark:bg-gray-600 rounded-md">
              Cancelar
            </button>
            <button type="submit" :disabled="pendingUpdate" class="btn-primary">
              {{ pendingUpdate ? 'A salvar...' : 'Salvar Correção' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <div v-if="isDeleteModalOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-xl w-full max-w-md">
        <h3 class="text-lg font-medium text-gray-900 dark:text-white">Confirmar Remoção</h3>
        <p class="mt-2 text-sm text-gray-600 dark:text-gray-300">
          Tem a certeza que deseja apagar este registo de presença?
        </p>
        <div class="mt-6 flex justify-end space-x-3">
          <button type="button" @click="closeModal" class="px-4 py-2 bg-gray-200 dark:bg-gray-600 rounded-md">
            Cancelar
          </button>
          <button @click="handleDelete" :disabled="pendingUpdate" class="px-4 py-2 font-medium text-white bg-red-600 rounded-md hover:bg-red-700">
            {{ pendingUpdate ? 'A apagar...' : 'Apagar' }}
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const props = defineProps({
  attendance: { type: Array as () => any[], required: true },
  opcoesEstado: { type: Array as () => { value: string, label: string }[], required: true }
})
const emit = defineEmits(['updateList'])
const { accessToken } = useAuth()

// --- Estado para Edição/Remoção (Modal) ---
const isEditModalOpen = ref(false)
const isDeleteModalOpen = ref(false)
const pendingUpdate = ref(false)
const editingItem = ref<any>(null)

// --- Funções do Modal ---
function closeModal() {
  isEditModalOpen.value = false
  isDeleteModalOpen.value = false
  editingItem.value = null
}

function openEditModal(item: any) {
  editingItem.value = JSON.parse(JSON.stringify(item)) // Copia profunda
  isEditModalOpen.value = true
}

function openDeleteConfirm(item: any) {
  editingItem.value = item
  isDeleteModalOpen.value = true
}

// --- Funções da API (CRUD) ---

// UPDATE (PATCH)
async function handleUpdate() {
  if (!editingItem.value) return
  
  pendingUpdate.value = true
  try {
    await $fetch(`/api/v1/presencas/${editingItem.value.id}/`, {
      method: 'PATCH',
      headers: { Authorization: `Bearer ${accessToken.value}` },
      body: {
        estado: editingItem.value.estado,
      }
    })
    emit('updateList')
    closeModal()
  } catch (err) {
    alert("Erro ao atualizar presença.")
  } finally {
    pendingUpdate.value = false
  }
}

// DELETE
async function handleDelete() {
  if (!editingItem.value) return
  
  pendingUpdate.value = true
  try {
    await $fetch(`/api/v1/presencas/${editingItem.value.id}/`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${accessToken.value}` }
    })
    emit('updateList')
    closeModal()
  } catch (err) {
    alert("Erro ao apagar presença.")
  } finally {
    pendingUpdate.value = false
  }
}

// Helper de Estilo
function getStatusClass(estado: string) {
  if (estado === 'Presente') return 'status-green'
  if (estado === 'Ausente') return 'status-red'
  if (estado === 'Justificado') return 'status-yellow'
  return ''
}
</script>

<style scoped>
/* (Estilos reutilizados) */
.label { @apply block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1; }
.input { @apply w-full px-3 py-2 border rounded-md shadow-sm bg-gray-50 dark:bg-gray-700 dark:text-white dark:border-gray-600; }
.btn-primary { @apply px-4 py-2 font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 disabled:opacity-50; }
.table-header { @apply px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase; }
.table-cell { @apply px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white; }
.status-green { @apply px-2 py-0.5 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800 dark:bg-green-800 dark:text-green-100; }
.status-yellow { @apply px-2 py-0.5 inline-flex text-xs leading-5 font-semibold rounded-full bg-yellow-100 text-yellow-800 dark:bg-yellow-800 dark:text-yellow-100; }
.status-red { @apply px-2 py-0.5 inline-flex text-xs leading-5 font-semibold rounded-full bg-red-100 text-red-800 dark:bg-red-800 dark:text-red-100; }
</style>
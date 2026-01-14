<template>
  <div class="space-y-6">
    <details class="bg-white dark:bg-gray-800 p-4 rounded-lg shadow">
      <summary class="font-medium cursor-pointer text-gray-900 dark:text-white">Registar Nova Sanção</summary>
      <form @submit.prevent="handleCreate" class="mt-4 space-y-3">
        <div>
          <label class="label">Data da Ocorrência</label>
          <input v-model="newEntry.data_ocorrencia" type="date" class="input" required />
        </div>
        <div>
          <label class="label">Tipo de Sanção</label>
          <select v-model="newEntry.tipo_sancao" class="input">
            <option v-for="opt in opcoesTipo" :key="opt.value" :value="opt.value">
              {{ opt.label }}
            </option>
          </select>
        </div>
        <div>
          <label class="label">Descrição</label>
          <textarea v-model="newEntry.descricao" class="input" rows="3" required></textarea>
        </div>
        <button type="submit" :disabled="pendingCreate" class="btn-primary">
          {{ pendingCreate ? 'A registar...' : 'Registar Sanção' }}
        </button>
      </form>
    </details>

    <div class="overflow-x-auto bg-white dark:bg-gray-800 rounded-lg shadow">
      <table class="w-full">
        <thead class="bg-gray-50 dark:bg-gray-700">
          <tr>
            <th class="table-header">Data</th>
            <th class="table-header">Tipo</th>
            <th class="table-header">Descrição</th>
            <th class="table-header">Admin</th>
            <th class="table-header">Ações</th>
          </tr>
        </thead>
        <tbody class="divide-y dark:divide-gray-700">
          <tr v-if="discipline.length === 0">
            <td colspan="5" class="table-cell text-center text-gray-500">Nenhum registo disciplinar.</td>
          </tr>
          <tr v-for="item in discipline" :key="item.id" class="hover:bg-gray-50 dark:hover:bg-gray-700">
            <td class="table-cell">{{ item.data_ocorrencia }}</td>
            <td class="table-cell">{{ item.tipo_sancao }}</td>
            <td class="table-cell max-w-sm truncate" :title="item.descricao">{{ item.descricao }}</td>
            <td class="table-cell">{{ item.admin_id_registo }}</td>
            <td class="table-cell space-x-3">
              <button @click="openEditModal(item)" class="font-medium text-blue-600 dark:text-blue-400 hover:underline">
                Editar
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
      <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-xl w-full max-w-lg">
        <h3 class="text-lg font-medium text-gray-900 dark:text-white">Editar Sanção (ID: {{ editingItem.id }})</h3>
        
        <form @submit.prevent="handleUpdate" class="mt-4 space-y-4">
          <div>
            <label class="label">Data da Ocorrência</label>
            <input v-model="editingItem.data_ocorrencia" type="date" class="input" required />
          </div>
          <div>
            <label class="label">Tipo de Sanção</label>
            <select v-model="editingItem.tipo_sancao" class="input">
              <option v-for="opt in opcoesTipo" :key="opt.value" :value="opt.value">
                {{ opt.label }}
              </option>
            </select>
          </div>
          <div>
            <label class="label">Descrição</label>
            <textarea v-model="editingItem.descricao" class="input" rows="3" required></textarea>
          </div>
          <div class="mt-6 flex justify-end space-x-3">
            <button type="button" @click="closeModal" class="px-4 py-2 bg-gray-200 dark:bg-gray-600 rounded-md">
              Cancelar
            </button>
            <button type="submit" :disabled="pendingUpdate" class="btn-primary">
              {{ pendingUpdate ? 'A salvar...' : 'Salvar Alterações' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <div v-if="isDeleteModalOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-xl w-full max-w-md">
        <h3 class="text-lg font-medium text-gray-900 dark:text-white">Confirmar Remoção</h3>
        <p class="mt-2 text-sm text-gray-600 dark:text-gray-300">
          Tem a certeza que deseja apagar este registo de sanção? Esta ação não pode ser revertida.
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
  discipline: { type: Array as () => any[], required: true },
  studentId: { type: String, required: true },
  opcoesTipo: { type: Array as () => { value: string, label: string }[], required: true }
})
const emit = defineEmits(['updateList'])
const { accessToken } = useAuth()

// --- Estado para Criar Novo ---
const pendingCreate = ref(false)
const newEntry = ref({
  data_ocorrencia: new Date().toISOString().split('T')[0],
  tipo_sancao: props.opcoesTipo[0]?.value || 'Outro',
  descricao: ''
})

// --- Estado para Edição/Remoção (Modal) ---
const isEditModalOpen = ref(false)
const isDeleteModalOpen = ref(false)
const pendingUpdate = ref(false) // Reutilizado para update e delete
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
  editingItem.value = item // Não precisa de cópia, só do ID
  isDeleteModalOpen.value = true
}

// --- Funções da API (CRUD) ---

// CREATE
async function handleCreate() {
  pendingCreate.value = true
  try {
    await $fetch(`/api/v1/estudantes/${props.studentId}/sancoes/`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${accessToken.value}` },
      body: newEntry.value
    })
    newEntry.value.descricao = ''
    emit('updateList')
  } catch (err) {
    alert("Erro ao registar sanção.")
  } finally {
    pendingCreate.value = false
  }
}

// UPDATE (PATCH)
async function handleUpdate() {
  if (!editingItem.value) return
  
  pendingUpdate.value = true
  try {
    await $fetch(`/api/v1/sancoes/${editingItem.value.id}/`, {
      method: 'PATCH',
      headers: { Authorization: `Bearer ${accessToken.value}` },
      body: {
        data_ocorrencia: editingItem.value.data_ocorrencia,
        tipo_sancao: editingItem.value.tipo_sancao,
        descricao: editingItem.value.descricao
      }
    })
    emit('updateList')
    closeModal()
  } catch (err) {
    alert("Erro ao atualizar sanção.")
  } finally {
    pendingUpdate.value = false
  }
}

// DELETE
async function handleDelete() {
  if (!editingItem.value) return
  
  pendingUpdate.value = true
  try {
    await $fetch(`/api/v1/sancoes/${editingItem.value.id}/`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${accessToken.value}` }
    })
    emit('updateList')
    closeModal()
  } catch (err) {
    alert("Erro ao apagar sanção.")
  } finally {
    pendingUpdate.value = false
  }
}
</script>

<style scoped>
/* (Estilos reutilizados) */
.label { @apply block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1; }
.input { @apply w-full px-3 py-2 border rounded-md shadow-sm bg-gray-50 dark:bg-gray-700 dark:text-white dark:border-gray-600; }
.btn-primary { @apply px-4 py-2 font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 disabled:opacity-50; }
.table-header { @apply px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase; }
.table-cell { @apply px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white; }
</style>
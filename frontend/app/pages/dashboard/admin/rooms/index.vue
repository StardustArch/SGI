<template>
  <div class="p-6 space-y-6 dark:text-white">
    <!-- Cabeçalho -->
    <div class="flex justify-between items-center">
      <div>
        <h1 class="text-3xl font-bold">Gestão de Quartos</h1>
        <p class="text-gray-500">Administração de blocos, vagas e ocupação física.</p>
      </div>
      <button @click="openModal()" class="btn-primary flex items-center gap-2">
        <BootstrapIcon name="plus-lg" /> Novo Quarto
      </button>
    </div>

    <!-- Filtros -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4 bg-white dark:bg-gray-800 p-4 rounded-lg shadow-sm">
      <input v-model="filters.search" type="text" placeholder="Pesquisar número ou bloco..." class="input" @input="fetchQuartos" />
      <select v-model="filters.genero" class="input" @change="fetchQuartos">
        <option value="">Todos os Géneros</option>
        <option value="M">Masculino</option>
        <option value="F">Feminino</option>
      </select>
      <select v-model="filters.estado" class="input" @change="fetchQuartos">
        <option value="">Todos os Estados</option>
        <option value="Activo">Activo</option>
        <option value="Manutenção">Manutenção</option>
        <option value="Inactivo">Inactivo</option>
      </select>
    </div>

    <!-- Tabela de quartos -->
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden">
      <table class="w-full text-left border-collapse">
        <thead class="bg-gray-50 dark:bg-gray-700">
          <tr>
            <th class="p-4 font-semibold">Quarto / Bloco</th>
            <th class="p-4 font-semibold">Género</th>
            <th class="p-4 font-semibold">Capacidade</th>
            <th class="p-4 font-semibold">Ocupação</th>
            <th class="p-4 font-semibold">Estado</th>
            <th class="p-4 font-semibold text-right">Acções</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="quarto in quartos" :key="quarto.id" class="border-t dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-750">
            <td class="p-4">
              <span class="font-bold">#{{ quarto.numero }}</span>
              <div class="text-xs text-gray-500">{{ quarto.bloco }}</div>
            </td>
            <td class="p-4">
              <span :class="quarto.genero_permitido === 'M' ? 'text-blue-500' : 'text-pink-500'">
                {{ quarto.genero_permitido === 'M' ? '♂ Masculino' : '♀ Feminino' }}
              </span>
            </td>
            <td class="p-4">{{ quarto.capacidade_maxima }} camas</td>
            <td class="p-4">
              <div class="flex items-center gap-2">
                <div class="w-16 bg-gray-200 rounded-full h-2">
                  <div class="bg-blue-600 h-2 rounded-full" :style="{ width: ocupacaoPercent(quarto) + '%' }"></div>
                </div>
                <span class="text-sm">{{ quarto.ocupacao_atual }}/{{ quarto.capacidade_maxima }}</span>
              </div>
            </td>
            <td class="p-4">
              <span :class="statusClass(quarto.estado)" class="px-2 py-1 rounded-full text-xs font-medium">
                {{ quarto.estado }}
              </span>
            </td>
            <td class="p-4 text-right space-x-2">
              <button @click="openModal(quarto)" class="text-blue-600 hover:text-blue-800">Editar</button>
              <button @click="confirmDelete(quarto)" class="text-red-600 hover:text-red-800">Apagar</button>
            </td>
          </tr>
          <tr v-if="quartos.length === 0 && !loading">
            <td colspan="6" class="p-8 text-center text-gray-500">Nenhum quarto encontrado.</td>
          </tr>
        </tbody>
      </table>
      <div v-if="loading" class="p-8 text-center text-gray-500">Carregando...</div>
    </div>

    <!-- Modal de criação/edição -->
     <ClientOnly>
    <div v-if="showModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div class="bg-white dark:bg-gray-800 rounded-xl p-6 w-full max-w-md shadow-2xl">
        <h2 class="text-xl font-bold mb-4">{{ editingId ? 'Editar Quarto' : 'Novo Quarto' }}</h2>
        <form @submit.prevent="saveQuarto" class="space-y-4">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="label text-xs">Número *</label>
              <input v-model="roomForm.numero" type="text" class="input" required />
            </div>
            <div>
              <label class="label text-xs">Bloco *</label>
              <input v-model="roomForm.bloco" type="text" class="input" required />
            </div>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="label text-xs">Capacidade Máxima *</label>
              <input v-model.number="roomForm.capacidade_maxima" type="number" min="1" class="input" required />
            </div>
            <div>
              <label class="label text-xs">Género *</label>
              <select v-model="roomForm.genero_permitido" class="input" required>
                <option value="M">Masculino</option>
                <option value="F">Feminino</option>
              </select>
            </div>
          </div>
          <div>
            <label class="label text-xs">Estado</label>
            <select v-model="roomForm.estado" class="input">
              <option value="Activo">Activo</option>
              <option value="Manutenção">Em Manutenção</option>
              <option value="Inactivo">Inactivo</option>
            </select>
          </div>
          <div class="flex justify-end gap-3 mt-6">
            <button type="button" @click="closeModal" class="px-4 py-2 text-gray-500">Cancelar</button>
            <button type="submit" class="btn-primary" :disabled="saving">
              {{ saving ? 'A guardar...' : 'Guardar Alterações' }}
            </button>
          </div>
        </form>
      </div>
    </div>
    </ClientOnly>
  </div>
</template>

<script setup lang="ts">
interface Quarto {
  id?: number
  numero: string
  bloco: string
  capacidade_maxima: number
  ocupacao_atual: number
  genero_permitido: 'M' | 'F'
  estado: 'Activo' | 'Manutenção' | 'Inactivo'
}

const { api } = useApi()
const quartos = ref<Quarto[]>([])
const loading = ref(false)
const saving = ref(false)
const showModal = ref(false)
const editingId = ref<number | null>(null)

// Estado dos filtros
const filters = reactive({
  search: '',
  genero: '',
  estado: ''
})

// Formulário do quarto
const roomForm = ref<Quarto>({
  numero: '',
  bloco: '',
  capacidade_maxima: 4,
  ocupacao_atual: 0,
  genero_permitido: 'M',
  estado: 'Activo'
})

// Carregar lista de quartos com filtros
async function fetchQuartos() {
  loading.value = true
  try {
    const params = new URLSearchParams()
    if (filters.genero) params.append('genero_permitido', filters.genero)
    if (filters.estado) params.append('estado', filters.estado)
    if (filters.search) params.append('search', filters.search)
    const response = await api<any>(`/admin/quartos/?${params.toString()}`)
    // Se vier paginado, extrai results; senão, usa como array
    quartos.value = response.results ?? response
  } catch (error) {
    console.error(error)
    alert('Erro ao carregar quartos.')
  } finally {
    loading.value = false
  }
}

// Abrir modal para criar ou editar
function openModal(quarto: Quarto | null = null) {
  if (quarto) {
    editingId.value = quarto.id || null
    roomForm.value = { ...quarto }
  } else {
    editingId.value = null
    roomForm.value = {
      numero: '',
      bloco: '',
      capacidade_maxima: 4,
      ocupacao_atual: 0,
      genero_permitido: 'M',
      estado: 'Activo'
    }
  }
  showModal.value = true
}

function closeModal() {
  showModal.value = false
  editingId.value = null
  // Opcional: resetar formulário para valores padrão
  roomForm.value = {
    numero: '',
    bloco: '',
    capacidade_maxima: 4,
    ocupacao_atual: 0,
    genero_permitido: 'M',
    estado: 'Activo'
  }
}

// Salvar (criar ou atualizar)
async function saveQuarto() {
  saving.value = true
  try {
    const url = editingId.value ? `/admin/quartos/${editingId.value}/` : '/admin/quartos/'
    const method = editingId.value ? 'PATCH' : 'POST'
    // Não enviar ocupacao_atual – o backend já ignora
    const payload = { ...roomForm.value }
    delete payload.ocupacao_atual
    await api(url, { method, body: payload })
    closeModal()
    await fetchQuartos()
    alert(editingId.value ? 'Quarto actualizado com sucesso!' : 'Quarto criado com sucesso!')
  } catch (error: any) {
    const msg = error.response?._data?.erro || 'Erro ao salvar quarto. Verifique se o número já existe.'
    alert(msg)
  } finally {
    saving.value = false
  }
}

// Excluir quarto
async function confirmDelete(quarto: Quarto) {
  if (!confirm(`Deseja apagar o quarto ${quarto.numero}?`)) return
  try {
    await api(`/admin/quartos/${quarto.id}/`, { method: 'DELETE' })
    await fetchQuartos()
    alert('Quarto apagado com sucesso.')
  } catch (error: any) {
    const msg = error.response?._data?.erro || 'Erro ao apagar quarto. Verifique se existem estudantes alocados.'
    alert(msg)
  }
}

// Helper para calcular percentagem de ocupação
function ocupacaoPercent(quarto: Quarto): number {
  return (quarto.ocupacao_atual / quarto.capacidade_maxima) * 100
}

// Classes CSS para estado do quarto
function statusClass(estado: string) {
  return {
    'bg-green-100 text-green-700': estado === 'Activo',
    'bg-orange-100 text-orange-700': estado === 'Manutenção',
    'bg-red-100 text-red-700': estado === 'Inactivo'
  }[estado] || ''
}

onMounted(fetchQuartos)
</script>

<style scoped>
.label {
  @apply block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-1;
}
.input {
  @apply w-full px-4 py-2 border rounded-lg shadow-sm bg-gray-50 dark:bg-gray-700 dark:text-white dark:border-gray-600 focus:ring-2 focus:ring-blue-500 transition-all;
}
.btn-primary {
  @apply px-4 py-2 font-bold text-white bg-blue-600 rounded-lg hover:bg-blue-700 dark:bg-blue-500 shadow-sm disabled:opacity-50 transition-all;
}
</style>
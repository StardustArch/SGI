<template>
  <div class="p-6 space-y-6 dark:text-white">
    <div class="flex justify-between items-center">
      <div>
        <h1 class="text-3xl font-bold">Gestão de Quartos</h1>
        <p class="text-gray-500">Administração de blocos, vagas e ocupação física.</p>
      </div>
      <button @click="openModal()" class="btn-primary">
        + Novo Quarto
      </button>
    </div>

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
      </select>
    </div>

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
                {{ quarto.genero_permitido === 'M' ? '♂ Masc' : '♀ Fem' }}
              </span>
            </td>
            <td class="p-4">{{ quarto.capacidade_maxima }} camas</td>
            <td class="p-4">
              <div class="flex items-center gap-2">
                <div class="w-16 bg-gray-200 rounded-full h-2">
                  <div class="bg-blue-600 h-2 rounded-full" :style="{ width: (quarto.ocupacao_atual / quarto.capacidade_maxima * 100) + '%' }"></div>
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
        </tbody>
      </table>
    </div>

    <div v-if="showModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div class="bg-white dark:bg-gray-800 rounded-xl p-6 w-full max-w-md shadow-2xl">
        <h2 class="text-xl font-bold mb-4">{{ editingId ? 'Editar Quarto' : 'Novo Quarto' }}</h2>
        <form @submit.prevent="saveQuarto" class="space-y-4">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="label text-xs">Número</label>
              <input v-model="roomForm.numero" type="text" class="input" required />
            </div>
            <div>
              <label class="label text-xs">Bloco</label>
              <input v-model="roomForm.bloco" type="text" class="input" required />
            </div>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="label text-xs">Capacidade Max</label>
              <input v-model.number="roomForm.capacidade_maxima" type="number" class="input" required />
            </div>
            <div>
              <label class="label text-xs">Género</label>
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
            <button type="button" @click="showModal = false" class="px-4 py-2 text-gray-500">Cancelar</button>
            <button type="submit" class="btn-primary" :disabled="pending">
              {{ pending ? 'A guardar...' : 'Guardar Alterações' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// 1. Definimos a interface com campos opcionais onde faz sentido (?)
interface Quarto {
  id?: number
  numero: string
  bloco: string
  capacidade_maxima: number
  ocupacao_atual: number // Obrigatório conforme o erro 2322
  genero_permitido: 'M' | 'F'
  estado: 'Activo' | 'Manutenção' | 'Inactivo'
}

const { api } = useApi()
const quartos = ref<Quarto[]>([]) 
const pending = ref(false)
const showModal = ref(false)
const editingId = ref<number | null>(null)

const filters = ref({ search: '', genero: '', estado: '' })

// Função auxiliar para criar um objeto Quarto vazio e válido
const createEmptyRoom = (): Quarto => ({
  numero: '',
  bloco: '',
  capacidade_maxima: 4,
  ocupacao_atual: 0, // Adicionado para satisfazer a interface
  genero_permitido: 'M',
  estado: 'Activo'
})

const roomForm = ref<Quarto>(createEmptyRoom())

async function fetchQuartos() {
  const params = new URLSearchParams()
  if (filters.value.genero) params.append('genero_permitido', filters.value.genero)
  if (filters.value.estado) params.append('estado', filters.value.estado)
  if (filters.value.search) params.append('search', filters.value.search)
  
  // Tipamos o retorno da API
  const data = await api<Quarto[]>(`/admin/quartos/?${params.toString()}`)
  quartos.value = data
}

// Corrigido: Parâmetro tipado e lógica de reset corrigida
function openModal(quarto: Quarto | null = null) {
  if (quarto) {
    editingId.value = quarto.id || null
    roomForm.value = { ...quarto }
  } else {
    editingId.value = null
    roomForm.value = createEmptyRoom() // Usa a função para garantir todos os campos
  }
  showModal.value = true
}

async function saveQuarto() {
  pending.value = true
  try {
    const url = editingId.value ? `/admin/quartos/${editingId.value}/` : '/admin/quartos/'
    const method = editingId.value ? 'PATCH' : 'POST'
    
    await api(url, { method, body: roomForm.value })
    showModal.value = false
    await fetchQuartos()
  } catch (e) {
    alert("Erro ao salvar quarto. Verifique se o número já existe.")
  } finally {
    pending.value = false
  }
}

// Corrigido: Tipagem explícita do parâmetro 'quarto'
async function confirmDelete(quarto: Quarto) {
  if (confirm(`Deseja apagar o quarto ${quarto.numero}?`)) {
    try {
      await api(`/admin/quartos/${quarto.id}/`, { method: 'DELETE' })
      await fetchQuartos()
    } catch (e: any) {
      const msg = e.response?._data?.erro || "Erro ao apagar."
      alert(msg)
    }
  }
}

// Corrigido: Tipagem explícita do parâmetro 's'
const statusClass = (s: string) => ({
  'bg-green-100 text-green-700': s === 'Activo',
  'bg-orange-100 text-orange-700': s === 'Manutenção',
  'bg-red-100 text-red-700': s === 'Inactivo'
})

onMounted(fetchQuartos)
</script>
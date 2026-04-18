<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 md:py-8">
    
    <!-- Cabeçalho -->
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6">
      <div>
        <h1 class="text-2xl md:text-3xl font-bold text-slate-900 dark:text-white">Gestão de Quartos</h1>
        <p class="text-sm md:text-base text-slate-500 dark:text-slate-400 mt-1">Administração de blocos, vagas e ocupação física.</p>
      </div>
      <button @click="openModal()" class="px-5 py-2.5 rounded-lg bg-blue-600 hover:bg-blue-700 text-white font-medium text-sm transition-colors flex items-center gap-2 min-h-[44px]">
        <BootstrapIcon name="plus-lg" class="w-4 h-4" />
        Novo Quarto
      </button>
    </div>

    <!-- Filtros -->
    <div class="bg-white dark:bg-slate-900 rounded-xl p-4 border border-slate-200 dark:border-slate-800 shadow-sm mb-6">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
        <input 
          v-model="filters.search" 
          type="text" 
          placeholder="Pesquisar número ou bloco..." 
          class="input" 
          @input="fetchQuartos" 
        />
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
    </div>

    <!-- Loading -->
    <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div v-for="i in 6" :key="i" class="h-40 bg-slate-100 dark:bg-slate-800 animate-pulse rounded-xl"></div>
    </div>

    <!-- Grid de Cards -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-5">
      
      <div 
        v-for="quarto in quartos" 
        :key="quarto.id" 
        class="bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-md transition-shadow p-5 flex flex-col"
      >
        <!-- Cabeçalho do card -->
        <div class="flex items-start justify-between mb-3">
          <div>
            <div class="flex items-center gap-2">
              <span class="text-lg font-bold text-slate-900 dark:text-white">Bloco {{ quarto.bloco }}</span>
              <span :class="[
                'px-2 py-0.5 rounded-md text-xs font-medium border',
                statusClass(quarto.estado)
              ]">
                {{ quarto.estado }}
              </span>
            </div>
          </div>
          <div :class="[
            'h-8 w-8 rounded-full flex items-center justify-center text-sm font-medium',
            quarto.genero_permitido === 'M' 
              ? 'bg-blue-50 text-blue-600 dark:bg-blue-900/30 dark:text-blue-400' 
              : 'bg-rose-50 text-rose-600 dark:bg-rose-900/30 dark:text-rose-400'
          ]">
            {{ quarto.genero_permitido === 'M' ? '♂' : '♀' }}
          </div>
        </div>

        <!-- Capacidade e Ocupação -->
        <div class="mb-4 flex-1">
          <div class="flex items-center justify-between text-sm mb-1">
            <span class="text-slate-600 dark:text-slate-300">Capacidade</span>
            <span class="font-medium text-slate-900 dark:text-white">{{ quarto.capacidade_maxima }} camas</span>
          </div>
          <div class="flex items-center justify-between text-sm mb-2">
            <span class="text-slate-600 dark:text-slate-300">Ocupação</span>
            <span class="font-medium text-slate-900 dark:text-white">{{ quarto.ocupacao_atual }}/{{ quarto.capacidade_maxima }}</span>
          </div>
          
          <!-- Barra de progresso -->
          <div class="w-full bg-slate-100 dark:bg-slate-800 rounded-full h-2 mb-2">
            <div 
              class="h-2 rounded-full transition-all"
              :class="ocupacaoPercent(quarto) >= 90 ? 'bg-rose-500' : (ocupacaoPercent(quarto) >= 70 ? 'bg-amber-500' : 'bg-emerald-500')"
              :style="{ width: ocupacaoPercent(quarto) + '%' }"
            ></div>
          </div>
          
          <p class="text-xs text-slate-500 dark:text-slate-400">
            <span v-if="quarto.capacidade_maxima - quarto.ocupacao_atual > 0" class="text-emerald-600 dark:text-emerald-400 font-medium">
              {{ quarto.capacidade_maxima - quarto.ocupacao_atual }} vagas disponíveis
            </span>
            <span v-else class="text-rose-600 dark:text-rose-400 font-medium">Lotado</span>
          </p>
        </div>

        <!-- Ações -->
        <div class="flex justify-end gap-2 pt-3 border-t border-slate-100 dark:border-slate-800">
          <button 
            @click="openModal(quarto)" 
            class="px-3 py-1.5 rounded-lg text-sm font-medium text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
          >
            Editar
          </button>
          <button 
            @click="confirmDelete(quarto)" 
            class="px-3 py-1.5 rounded-lg text-sm font-medium text-rose-600 dark:text-rose-400 hover:bg-rose-50 dark:hover:bg-rose-900/20 transition-colors"
          >
            Apagar
          </button>
        </div>
      </div>

    </div>

    <!-- Mensagem quando não há resultados -->
    <div v-if="!loading && quartos.length === 0" class="p-16 text-center bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800">
      <BootstrapIcon name="door-closed" class="w-12 h-12 text-slate-300 dark:text-slate-600 mx-auto mb-3" />
      <p class="text-slate-500 dark:text-slate-400 font-medium">Nenhum quarto encontrado com estes filtros.</p>
    </div>

    <!-- Modal de criação/edição -->
    <ClientOnly>
      <div v-if="showModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4" @click.self="closeModal">
        <div class="bg-white dark:bg-slate-900 rounded-xl p-6 w-full max-w-md shadow-xl border border-slate-200 dark:border-slate-800">
          <h2 class="text-lg font-semibold text-slate-900 dark:text-white mb-5 border-b border-slate-100 dark:border-slate-800 pb-3">
            {{ editingId ? 'Editar Quarto' : 'Novo Quarto' }}
          </h2>
          <form @submit.prevent="saveQuarto" class="space-y-4">
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="label">Número *</label>
                <input v-model="roomForm.numero" type="text" class="input" required />
              </div>
              <div>
                <label class="label">Bloco *</label>
                <input v-model="roomForm.bloco" type="text" class="input" required />
              </div>
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="label">Capacidade Máxima *</label>
                <input v-model.number="roomForm.capacidade_maxima" type="number" min="1" class="input" required />
              </div>
              <div>
                <label class="label">Género *</label>
                <select v-model="roomForm.genero_permitido" class="input" required>
                  <option value="M">Masculino</option>
                  <option value="F">Feminino</option>
                </select>
              </div>
            </div>
            <div>
              <label class="label">Estado</label>
              <select v-model="roomForm.estado" class="input">
                <option value="Activo">Activo</option>
                <option value="Manutenção">Em Manutenção</option>
                <option value="Inactivo">Inactivo</option>
              </select>
            </div>
            <div class="flex justify-end gap-3 mt-6 pt-2 border-t border-slate-100 dark:border-slate-800">
              <button type="button" @click="closeModal" class="px-4 py-2 rounded-lg text-sm font-medium text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors">
                Cancelar
              </button>
              <button type="submit" class="px-4 py-2 rounded-lg bg-blue-600 hover:bg-blue-700 text-white font-medium text-sm transition-colors disabled:opacity-60" :disabled="saving">
                <span v-if="saving" class="inline-flex items-center gap-2">
                  <span class="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full"></span>
                  A guardar...
                </span>
                <span v-else>Guardar</span>
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

const filters = reactive({
  search: '',
  genero: '',
  estado: ''
})

const roomForm = ref<Quarto>({
  numero: '',
  bloco: '',
  capacidade_maxima: 4,
  ocupacao_atual: 0,
  genero_permitido: 'M',
  estado: 'Activo'
})

async function fetchQuartos() {
  loading.value = true
  try {
    const params = new URLSearchParams()
    if (filters.genero) params.append('genero_permitido', filters.genero)
    if (filters.estado) params.append('estado', filters.estado)
    if (filters.search) params.append('search', filters.search)
    const response = await api<any>(`/admin/quartos/?${params.toString()}`)
    quartos.value = response.results ?? response
  } catch (error) {
    console.error(error)
    alert('Erro ao carregar quartos.')
  } finally {
    loading.value = false
  }
}

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
  roomForm.value = {
    numero: '',
    bloco: '',
    capacidade_maxima: 4,
    ocupacao_atual: 0,
    genero_permitido: 'M',
    estado: 'Activo'
  }
}

async function saveQuarto() {
  saving.value = true
  try {
    const url = editingId.value ? `/admin/quartos/${editingId.value}/` : '/admin/quartos/'
    const method = editingId.value ? 'PATCH' : 'POST'
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

function ocupacaoPercent(quarto: Quarto): number {
  return (quarto.ocupacao_atual / quarto.capacidade_maxima) * 100
}

function statusClass(estado: string) {
  return {
    'Activo': 'bg-emerald-50 text-emerald-700 border-emerald-200 dark:bg-emerald-900/20 dark:text-emerald-400 dark:border-emerald-800/30',
    'Manutenção': 'bg-amber-50 text-amber-700 border-amber-200 dark:bg-amber-900/20 dark:text-amber-400 dark:border-amber-800/30',
    'Inactivo': 'bg-slate-100 text-slate-600 border-slate-200 dark:bg-slate-800 dark:text-slate-400 dark:border-slate-700'
  }[estado] || ''
}

onMounted(fetchQuartos)
</script>

<style scoped>
.label {
  @apply block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1;
}
.input {
  @apply w-full px-3 py-2 bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-lg text-sm text-slate-900 dark:text-white placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors;
}
</style>
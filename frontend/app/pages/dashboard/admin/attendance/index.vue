<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 md:py-8">
    
    <!-- Cabeçalho -->
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6">
      <div>
        <h1 class="text-2xl md:text-3xl font-bold text-slate-900 dark:text-white">Chamada de Estudo</h1>
        <p class="text-sm md:text-base text-slate-500 dark:text-slate-400 mt-1">Registe a assiduidade dos internos para o período de estudo.</p>
      </div>

      <div class="flex flex-wrap items-center gap-3">
        <!-- Seletor de Período -->
        <select 
          v-model="periodoSelecionado" 
          class="px-3 py-2 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-lg text-sm font-medium text-slate-700 dark:text-slate-300 focus:outline-none focus:ring-2 focus:ring-blue-500 cursor-pointer"
        >
          <option value="Manhã">🌅 Manhã</option>
          <option value="Tarde">☀️ Tarde</option>
          <option value="Noite">🌙 Noite</option>
        </select>

        <!-- Seletor de Data -->
        <div class="flex items-center gap-2 bg-white dark:bg-slate-900 p-1.5 pl-3 rounded-lg border border-slate-200 dark:border-slate-700 shadow-sm">
          <BootstrapIcon name="calendar-event" class="text-slate-400 w-4 h-4" />
          <input 
            v-model="dataChamada" 
            type="date" 
            class="bg-transparent border-none focus:ring-0 text-sm font-medium text-slate-700 dark:text-slate-300 p-1"
            @change="carregarPresencasExistentes"
          />
        </div>
      </div>
    </div>

    <!-- Filtro por Bloco -->
    <div class="flex items-center gap-3 mb-6">
      <label class="text-sm font-medium text-slate-500 dark:text-slate-400">Filtrar por bloco:</label>
      <select 
        v-model="filtroBloco" 
        class="px-3 py-2 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-lg text-sm text-slate-700 dark:text-slate-300 focus:outline-none focus:ring-2 focus:ring-blue-500 cursor-pointer min-w-[140px]"
        @change="filtrarEstudantes"
      >
        <option value="">Todos os blocos</option>
        <option v-for="bloco in blocosUnicos" :key="bloco" :value="bloco">{{ bloco }}</option>
      </select>
    </div>

    <!-- Cards de Contagem -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
      <div class="bg-emerald-50 dark:bg-emerald-900/20 p-4 rounded-xl border border-emerald-200 dark:border-emerald-800/30 text-center">
        <p class="text-xs font-medium text-emerald-600 dark:text-emerald-400 uppercase tracking-wider mb-1">Presentes</p>
        <h4 class="text-2xl font-bold text-emerald-700 dark:text-emerald-400">{{ contagem.presentes }}</h4>
      </div>
      <div class="bg-rose-50 dark:bg-rose-900/20 p-4 rounded-xl border border-rose-200 dark:border-rose-800/30 text-center">
        <p class="text-xs font-medium text-rose-600 dark:text-rose-400 uppercase tracking-wider mb-1">Ausentes</p>
        <h4 class="text-2xl font-bold text-rose-700 dark:text-rose-400">{{ contagem.ausentes }}</h4>
      </div>
      <div class="bg-amber-50 dark:bg-amber-900/20 p-4 rounded-xl border border-amber-200 dark:border-amber-800/30 text-center">
        <p class="text-xs font-medium text-amber-600 dark:text-amber-400 uppercase tracking-wider mb-1">Justificados</p>
        <h4 class="text-2xl font-bold text-amber-700 dark:text-amber-400">{{ contagem.justificados }}</h4>
      </div>
      <button 
        @click="salvarChamada"
        :disabled="submitting || loadingEstudantes"
        class="bg-blue-600 hover:bg-blue-700 text-white rounded-xl font-medium text-sm transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex flex-col items-center justify-center min-h-[88px]"
      >
        <span v-if="submitting" class="animate-spin h-5 w-5 border-2 border-white border-t-transparent rounded-full mb-1"></span>
        <span v-else class="font-semibold">{{ submitting ? 'A gravar...' : 'Submeter Chamada' }}</span>
      </button>
    </div>

    <!-- Loading -->
    <div v-if="loadingEstudantes" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div v-for="i in 6" :key="i" class="h-20 bg-slate-100 dark:bg-slate-800 animate-pulse rounded-xl"></div>
    </div>

    <!-- Empty state -->
    <div v-else-if="estudantesFiltrados.length === 0" class="text-center py-16 bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800">
      <BootstrapIcon name="emoji-frown" class="w-12 h-12 text-slate-300 dark:text-slate-600 mx-auto mb-3" />
      <p class="text-slate-500 dark:text-slate-400 font-medium">Nenhum estudante ativo encontrado.</p>
    </div>

    <!-- Grid de Estudantes -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div 
        v-for="aluno in estudantesFiltrados" 
        :key="aluno.utilizador_id"
        class="bg-white dark:bg-slate-900 rounded-xl p-4 border border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-md transition-shadow flex items-center justify-between"
      >
        <div class="flex items-center gap-3 min-w-0">
          <div class="h-10 w-10 rounded-full bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 flex items-center justify-center font-semibold text-sm border border-blue-100 dark:border-blue-800 shrink-0">
            {{ aluno.nome_completo.charAt(0).toUpperCase() }}
          </div>
          <div class="min-w-0">
            <h3 class="font-semibold text-slate-900 dark:text-white truncate">{{ aluno.nome_completo }}</h3>
            <p class="text-xs text-slate-500 dark:text-slate-400">
              Quarto {{ aluno.quarto_numero || 'N/A' }} <span v-if="aluno.bloco">({{ aluno.bloco }})</span>
            </p>
          </div>
        </div>

        <div class="flex bg-slate-100 dark:bg-slate-800 p-1 rounded-lg gap-1 shrink-0 ml-2">
          <button 
            @click="aluno.estado = 'Presente'"
            :class="[
              'p-2 rounded-md transition-all',
              aluno.estado === 'Presente' 
                ? 'bg-emerald-500 text-white shadow-sm' 
                : 'text-slate-400 hover:text-emerald-600 dark:hover:text-emerald-400'
            ]"
            title="Presente"
          >
            <BootstrapIcon name="check-lg" class="w-4 h-4" />
          </button>
          <button 
            @click="aluno.estado = 'Ausente'"
            :class="[
              'p-2 rounded-md transition-all',
              aluno.estado === 'Ausente' 
                ? 'bg-rose-500 text-white shadow-sm' 
                : 'text-slate-400 hover:text-rose-600 dark:hover:text-rose-400'
            ]"
            title="Ausente"
          >
            <BootstrapIcon name="x-lg" class="w-4 h-4" />
          </button>
          <button 
            @click="aluno.estado = 'Justificado'"
            :class="[
              'p-2 rounded-md transition-all',
              aluno.estado === 'Justificado' 
                ? 'bg-amber-500 text-white shadow-sm' 
                : 'text-slate-400 hover:text-amber-600 dark:hover:text-amber-400'
            ]"
            title="Justificado"
          >
            <BootstrapIcon name="info-lg" class="w-4 h-4" />
          </button>
            <button 
    @click="navigateTo(`/dashboard/admin/students/${aluno.utilizador_id}/historic?tab=Presenças`)"
    class="p-2 hover:bg-stone-100 rounded-lg text-stone-400 hover:text-blue-500 transition-colors"
    title="Ver histórico de presenças"
  >
    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
  </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'

const { api } = useApi()

const dataChamada = ref(new Date().toISOString().substr(0, 10))
const periodoSelecionado = ref('Manhã')
const filtroBloco = ref('')
const submitting = ref(false)
const loadingEstudantes = ref(false)
const todosEstudantes = ref<any[]>([])
const listaChamada = ref<any[]>([])

const blocosUnicos = computed(() => {
  const blocos = todosEstudantes.value.map(e => e.bloco).filter(Boolean)
  return [...new Set(blocos)].sort()
})

function filtrarEstudantes() {
  if (!filtroBloco.value) {
    listaChamada.value = [...todosEstudantes.value]
  } else {
    listaChamada.value = todosEstudantes.value.filter(e => e.bloco === filtroBloco.value)
  }
  carregarPresencasExistentes()
}

const estudantesFiltrados = computed(() => listaChamada.value)

async function carregarEstudantes() {
  loadingEstudantes.value = true
  try {
    const response = await api<any>('/admin/estudantes/?estado=Activo')
    const estudantes = response.results ?? response
    todosEstudantes.value = estudantes.map((e: any) => ({
      ...e,
      bloco: e.bloco || e.quarto?.bloco || 'Desconhecido',
      estado: 'Presente'
    }))
    listaChamada.value = [...todosEstudantes.value]
  } catch (error) {
    console.error('Erro ao carregar estudantes:', error)
    alert('Não foi possível carregar a lista de alunos.')
  } finally {
    loadingEstudantes.value = false
    carregarPresencasExistentes()
  }
}

async function carregarPresencasExistentes() {
  if (!dataChamada.value || listaChamada.value.length === 0) return
  try {
    const response = await api<any>(`/admin/presencas/?data_presenca=${dataChamada.value}&periodo=${periodoSelecionado.value}`)
    const presencas = response.results ?? response
    if (presencas && presencas.length > 0) {
      const mapa = new Map()
      presencas.forEach((p: any) => mapa.set(p.estudante, p.estado))
      listaChamada.value.forEach(aluno => {
        if (mapa.has(aluno.utilizador_id)) {
          aluno.estado = mapa.get(aluno.utilizador_id)
        } else {
          aluno.estado = 'Presente'
        }
      })
    } else {
      listaChamada.value.forEach(aluno => aluno.estado = 'Presente')
    }
  } catch (error) {
    console.error('Erro ao carregar presenças existentes:', error)
  }
}

const contagem = computed(() => ({
  presentes: listaChamada.value.filter(a => a.estado === 'Presente').length,
  ausentes: listaChamada.value.filter(a => a.estado === 'Ausente').length,
  justificados: listaChamada.value.filter(a => a.estado === 'Justificado').length,
}))

async function salvarChamada() {
  if (!dataChamada.value) {
    alert('Selecione uma data antes de submeter.')
    return
  }

  const total = listaChamada.value.length
  const presentes = contagem.value.presentes
  if (!confirm(`Confirmar registo de presença para ${presentes} de ${total} alunos em ${dataChamada.value} (${periodoSelecionado.value})?`)) return

  submitting.value = true
  const ausentes_ids = listaChamada.value.filter(a => a.estado === 'Ausente').map(a => a.utilizador_id)
  const justificados_ids = listaChamada.value.filter(a => a.estado === 'Justificado').map(a => a.utilizador_id)

  try {
    const payload: any = {
      data_presenca: dataChamada.value,
      periodo: periodoSelecionado.value,
      ausentes_ids,
      justificados_ids
    }
    if (filtroBloco.value) {
      payload.bloco = filtroBloco.value
    }

    await api('/admin/presencas/batch/', {
      method: 'POST',
      body: payload
    })
    alert('Presenças registadas com sucesso!')
  } catch (error: any) {
    const msg = error.response?._data?.erro || 'Erro ao salvar. Verifique se já existe chamada para este dia/período.'
    alert(msg)
  } finally {
    submitting.value = false
  }
}

carregarEstudantes()

watch([dataChamada, periodoSelecionado], () => {
  if (listaChamada.value.length > 0) {
    carregarPresencasExistentes()
  }
})
</script>
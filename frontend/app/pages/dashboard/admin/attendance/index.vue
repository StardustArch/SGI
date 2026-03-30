<template>
  <div class="space-y-8 dark:text-white max-w-7xl mx-auto p-4 md:p-8">
    
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
      <div>
        <h1 class="text-3xl font-bold text-gray-800 dark:text-white tracking-tight">Chamada de Estudo</h1>
        <p class="text-stone-500 dark:text-gray-400 mt-1">Registe a assiduidade dos internos para o período de estudo.</p>
      </div>

      <div class="flex items-center gap-3 bg-white dark:bg-gray-800 p-2 rounded-2xl border border-stone-100 dark:border-gray-700 shadow-sm">
        <BootstrapIcon name="calendar-event" class="ml-2 text-rose-500" />
        <input 
          v-model="dataChamada" 
          type="date" 
          class="bg-transparent border-none focus:ring-0 font-bold text-gray-700 dark:text-white"
          @change="carregarPresencasExistentes"
        />
      </div>
    </div>

    <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
      <div class="bg-emerald-50 dark:bg-emerald-900/20 p-4 rounded-2xl border border-emerald-100 dark:border-emerald-800 text-center">
        <p class="text-[10px] font-bold uppercase text-emerald-600 tracking-wider">Presentes</p>
        <h4 class="text-2xl font-black text-emerald-700 dark:text-emerald-400">{{ contagem.presentes }}</h4>
      </div>
      <div class="bg-rose-50 dark:bg-rose-900/20 p-4 rounded-2xl border border-rose-100 dark:border-rose-800 text-center">
        <p class="text-[10px] font-bold uppercase text-rose-600 tracking-wider">Ausentes</p>
        <h4 class="text-2xl font-black text-rose-700 dark:text-rose-400">{{ contagem.ausentes }}</h4>
      </div>
      <div class="bg-amber-50 dark:bg-amber-900/20 p-4 rounded-2xl border border-amber-100 dark:border-amber-800 text-center">
        <p class="text-[10px] font-bold uppercase text-amber-600 tracking-wider">Justificados</p>
        <h4 class="text-2xl font-black text-amber-700 dark:text-amber-400">{{ contagem.justificados }}</h4>
      </div>
      <button 
        @click="salvarChamada"
        :disabled="submitting || loadingEstudantes"
        class="bg-gray-900 dark:bg-white text-white dark:text-gray-900 rounded-2xl font-bold hover:opacity-90 transition-all flex flex-col items-center justify-center shadow-lg disabled:opacity-50"
      >
        <span v-if="submitting" class="animate-spin h-5 w-5 border-2 border-current border-t-transparent rounded-full mb-1"></span>
        <span v-else>{{ submitting ? 'A gravar...' : 'Submeter Chamada' }}</span>
      </button>
    </div>

    <div v-if="loadingEstudantes" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div v-for="i in 6" :key="i" class="h-24 bg-stone-100 dark:bg-gray-800 animate-pulse rounded-[1.5rem]"></div>
    </div>

    <div v-else-if="listaChamada.length === 0" class="text-center py-20 bg-stone-50 dark:bg-gray-800/50 rounded-[2rem] border-2 border-dashed border-stone-200">
      <BootstrapIcon name="emoji-frown" class="text-4xl text-stone-400 mb-2" />
      <p class="text-stone-500 font-bold">Nenhum estudante ativo encontrado.</p>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div 
        v-for="aluno in listaChamada" 
        :key="aluno.utilizador_id"
        class="group bg-white dark:bg-gray-800 p-4 rounded-[1.5rem] border border-stone-100 dark:border-gray-700 shadow-sm hover:shadow-md transition-all flex items-center justify-between"
      >
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-stone-100 dark:bg-gray-700 flex items-center justify-center font-bold text-stone-500">
            {{ aluno.nome_completo.charAt(0) }}
          </div>
          <div class="min-w-0">
            <h3 class="font-bold text-gray-800 dark:text-white truncate w-32 md:w-40">{{ aluno.nome_completo }}</h3>
            <p class="text-[10px] text-stone-400 font-bold uppercase">Quarto {{ aluno.quarto_numero || 'N/A' }}</p>
          </div>
        </div>

        <div class="flex bg-stone-50 dark:bg-gray-700 p-1 rounded-xl gap-1">
          <button 
            @click="aluno.estado = 'Presente'"
            :class="['p-2 rounded-lg transition-all', aluno.estado === 'Presente' ? 'bg-emerald-500 text-white shadow-sm' : 'text-stone-400']"
            title="Presente"
          >
            <BootstrapIcon name="check-lg" />
          </button>
          <button 
            @click="aluno.estado = 'Ausente'"
            :class="['p-2 rounded-lg transition-all', aluno.estado === 'Ausente' ? 'bg-rose-500 text-white shadow-sm' : 'text-stone-400']"
            title="Ausente"
          >
            <BootstrapIcon name="x-lg" />
          </button>
          <button 
            @click="aluno.estado = 'Justificado'"
            :class="['p-2 rounded-lg transition-all', aluno.estado === 'Justificado' ? 'bg-amber-500 text-white shadow-sm' : 'text-stone-400']"
            title="Justificado"
          >
            <BootstrapIcon name="info-lg" />
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
const submitting = ref(false)
const loadingEstudantes = ref(false)
const listaChamada = ref<any[]>([])

// 1. Carregar todos os alunos ativos (tratando paginação)
async function carregarEstudantes() {
  loadingEstudantes.value = true
  try {
    const response = await api<any>('/admin/estudantes/?estado=Activo')
    // A API pode retornar um objeto paginado ou um array direto
    const estudantes = response.results ?? response
    listaChamada.value = estudantes.map((e: any) => ({
      ...e,
      estado: 'Presente' // estado inicial padrão
    }))
  } catch (error) {
    console.error('Erro ao carregar estudantes:', error)
    alert('Não foi possível carregar a lista de alunos.')
  } finally {
    loadingEstudantes.value = false
  }
}

// 2. Carregar presenças existentes para a data selecionada
async function carregarPresencasExistentes() {
  if (!dataChamada.value) return
  try {
    const response = await api<any>(`/admin/presencas/?data_presenca=${dataChamada.value}`)
    const presencas = response.results ?? response
    if (presencas && presencas.length > 0) {
      // Mapeia os estados existentes para a lista de estudantes
      const mapa = new Map()
      presencas.forEach((p: any) => mapa.set(p.estudante, p.estado))
      listaChamada.value.forEach(aluno => {
        if (mapa.has(aluno.utilizador_id)) {
          aluno.estado = mapa.get(aluno.utilizador_id)
        }
      })
    } else {
      // Se não houver presenças, resetar para "Presente"
      listaChamada.value.forEach(aluno => aluno.estado = 'Presente')
    }
  } catch (error) {
    console.error('Erro ao carregar presenças existentes:', error)
    // Se o endpoint não existir, apenas ignora
  }
}

// 3. Contagem em tempo real
const contagem = computed(() => {
  return {
    presentes: listaChamada.value.filter(a => a.estado === 'Presente').length,
    ausentes: listaChamada.value.filter(a => a.estado === 'Ausente').length,
    justificados: listaChamada.value.filter(a => a.estado === 'Justificado').length,
  }
})

// 4. Salvar a chamada
async function salvarChamada() {
  if (!dataChamada.value) {
    alert('Selecione uma data antes de submeter.')
    return
  }

  const total = listaChamada.value.length
  const presentes = contagem.value.presentes
  if (!confirm(`Confirmar registo de presença para ${presentes} de ${total} alunos em ${dataChamada.value}?`)) return

  submitting.value = true
  const ausentes_ids = listaChamada.value.filter(a => a.estado === 'Ausente').map(a => a.utilizador_id)
  const justificados_ids = listaChamada.value.filter(a => a.estado === 'Justificado').map(a => a.utilizador_id)

  try {
    await api('/admin/presencas/batch/', {
      method: 'POST',
      body: {
        data_presenca: dataChamada.value,
        ausentes_ids,
        justificados_ids
      }
    })
    alert('Presenças registadas com sucesso!')
    // Opcional: recarregar as presenças para confirmar (se o endpoint GET existir)
  } catch (error: any) {
    const msg = error.response?._data?.erro || 'Erro ao salvar. Verifique se já existe chamada para este dia.'
    alert(msg)
  } finally {
    submitting.value = false
  }
}

// Inicializar
carregarEstudantes()

// Quando a data mudar, recarrega as presenças existentes
watch(dataChamada, () => {
  if (listaChamada.value.length > 0) {
    carregarPresencasExistentes()
  }
})
</script>
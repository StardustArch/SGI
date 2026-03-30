<template>
  <div class="space-y-8 dark:text-white max-w-7xl mx-auto p-4 md:p-8">
    
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
      <div>
        <h1 class="text-3xl font-bold text-gray-800 dark:text-white tracking-tight">Gestão Disciplinar</h1>
        <p class="text-stone-500 dark:text-gray-400 mt-1">Registo de ocorrências e sanções do internato.</p>
      </div>

      <button 
        @click="showForm = !showForm"
        :class="['px-6 py-3 rounded-xl font-bold text-sm shadow-lg transition-all flex items-center gap-2', showForm ? 'bg-stone-200 text-stone-700 dark:bg-gray-700 dark:text-white' : 'bg-rose-500 text-white hover:bg-rose-600']"
      >
        <BootstrapIcon :name="showForm ? 'x-lg' : 'exclamation-triangle-fill'" />
        {{ showForm ? 'Cancelar Registo' : 'Registar Ocorrência' }}
      </button>
    </div>

    <div v-show="showForm" class="bg-white dark:bg-gray-800 rounded-[2.5rem] p-8 border border-rose-100 dark:border-rose-900/30 shadow-xl relative overflow-hidden transition-all">
      <div class="absolute top-0 right-0 w-32 h-32 bg-rose-50 dark:bg-rose-900/10 rounded-full -mr-10 -mt-10 opacity-50"></div>
      
      <h3 class="text-lg font-bold mb-6 flex items-center gap-2 relative z-10">
        <BootstrapIcon name="pen-fill" class="text-rose-500" />
        Nova Ocorrência Disciplinar
      </h3>

      <form @submit.prevent="submitSancao" class="space-y-6 relative z-10">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          
          <div class="space-y-1">
            <label class="text-[10px] font-bold text-stone-400 uppercase ml-1">Estudante Infrator</label>
            <select v-model="form.estudante" required class="admin-input appearance-none">
              <option value="" disabled>Selecione o estudante...</option>
              <option v-for="aluno in estudantesLista" :key="aluno.utilizador_id" :value="aluno.utilizador_id">
                {{ aluno.nome_completo }} (Quarto {{ aluno.quarto_numero || 'N/A' }})
              </option>
            </select>
          </div>

          <div class="space-y-1">
            <label class="text-[10px] font-bold text-stone-400 uppercase ml-1">Data da Ocorrência</label>
            <input v-model="form.data_ocorrencia" type="date" required class="admin-input" />
          </div>

          <div class="space-y-1 md:col-span-2">
            <label class="text-[10px] font-bold text-stone-400 uppercase ml-1">Tipo de Sanção</label>
            <div class="flex flex-wrap gap-3 mt-2">
              <label v-for="tipo in tiposSancao" :key="tipo" class="cursor-pointer">
                <input type="radio" v-model="form.tipo_sancao" :value="tipo" class="peer sr-only" required />
                <div class="px-4 py-2 rounded-xl text-sm font-bold border-2 border-stone-100 dark:border-gray-700 text-stone-500 peer-checked:border-rose-500 peer-checked:bg-rose-50 peer-checked:text-rose-600 dark:peer-checked:bg-rose-900/20 transition-all">
                  {{ tipo }}
                </div>
              </label>
            </div>
          </div>

          <div class="space-y-1 md:col-span-2">
            <label class="text-[10px] font-bold text-stone-400 uppercase ml-1">Descrição / Motivo</label>
            <textarea 
              v-model="form.descricao" 
              required 
              rows="3"
              placeholder="Descreva o que aconteceu detalhadamente..." 
              class="admin-input resize-none"
            ></textarea>
          </div>
        </div>

        <div class="flex justify-end pt-4 border-t border-stone-100 dark:border-gray-700">
          <button type="submit" :disabled="saving" class="px-8 py-3 rounded-xl bg-gray-900 dark:bg-white text-white dark:text-gray-900 font-bold shadow-lg hover:opacity-90 transition-all disabled:opacity-50 flex items-center gap-2">
            <span v-if="saving" class="animate-spin h-4 w-4 border-2 border-current border-t-transparent rounded-full"></span>
            {{ saving ? 'A registar...' : 'Salvar no Registo' }}
          </button>
        </div>
      </form>
    </div>

    <div class="bg-white dark:bg-gray-800 rounded-[2rem] border border-stone-100 dark:border-gray-700 overflow-hidden shadow-sm">
      <div class="p-6 border-b border-stone-100 dark:border-gray-700 bg-stone-50 dark:bg-gray-700/50">
        <h3 class="font-bold text-gray-800 dark:text-white uppercase tracking-widest text-xs text-stone-500">Últimas Sanções Aplicadas</h3>
      </div>
      
      <div v-if="pendingList" class="p-8 text-center animate-pulse text-stone-400 font-bold">A carregar registos...</div>
      
      <div v-else-if="sancoesLista.length === 0" class="p-12 text-center">
        <BootstrapIcon name="shield-check" class="text-5xl text-emerald-400 mb-3 mx-auto" />
        <p class="text-stone-500 font-bold">Nenhum registo disciplinar recente.</p>
      </div>

      <div v-else class="divide-y divide-stone-100 dark:divide-gray-700">
        <div v-for="s in sancoesLista" :key="s.id" class="p-6 hover:bg-stone-50/50 dark:hover:bg-gray-700/30 transition-colors flex flex-col md:flex-row gap-6">
          <div class="shrink-0 text-center md:border-r md:pr-6 border-stone-100 dark:border-gray-700 min-w-[100px]">
            <span class="block text-2xl font-black text-rose-500">{{ formatDia(s.data_ocorrencia) }}</span>
            <span class="block text-[10px] font-bold text-stone-400 uppercase">{{ formatMesAno(s.data_ocorrencia) }}</span>
          </div>
          <div class="flex-1 space-y-2">
            <div class="flex flex-wrap items-center justify-between gap-2">
              <h4 class="font-bold text-lg text-gray-800 dark:text-white leading-none">
                {{ nomeEstudanteMap[s.estudante] || `Estudante #${s.estudante}` }}
              </h4>
              <span class="px-3 py-1 bg-rose-50 dark:bg-rose-900/20 text-rose-600 dark:text-rose-400 text-[10px] font-bold uppercase rounded-lg border border-rose-100 dark:border-rose-800/30">
                {{ s.tipo_sancao }}
              </span>
            </div>
            <p class="text-sm text-stone-500 dark:text-gray-400 italic">"{{ s.descricao }}"</p>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'

const { api } = useApi()

const showForm = ref(false)
const saving = ref(false)

const tiposSancao = [
  'Advertência Verbal',
  'Trabalho Comunitário',
  'Suspensão de Saída',
  'Outro'
]

const form = reactive({
  estudante: '',
  tipo_sancao: '',
  data_ocorrencia: new Date().toISOString().substr(0, 10),
  descricao: ''
})

// --- Lista de estudantes (para o select) ---
const { data: estudantesRaw, pending: pendingEstudantes } = await useAsyncData('admin-estudantes-sancoes', 
  () => api<any>('/admin/estudantes/')
)
const estudantesLista = computed(() => {
  const raw = estudantesRaw.value
  if (!raw) return []
  return raw.results ?? raw
})

// Mapeia ID -> nome para usar na listagem
const nomeEstudanteMap = computed(() => {
  const map: Record<number, string> = {}
  estudantesLista.value.forEach((e: any) => {
    map[e.utilizador_id] = e.nome_completo
  })
  return map
})

// --- Lista de sanções (com paginação) ---
const { data: sancoesRaw, pending: pendingList, refresh } = await useAsyncData('admin-sancoes-lista', 
  () => api<any>('/admin/sancoes/')
)
const sancoesLista = computed(() => {
  const raw = sancoesRaw.value
  if (!raw) return []
  return raw.results ?? raw
})

async function submitSancao() {
  if (!form.estudante || !form.tipo_sancao || !form.descricao) {
    alert('Preencha todos os campos obrigatórios.')
    return
  }
  saving.value = true
  try {
    await api('/admin/sancoes/', {
      method: 'POST',
      body: form
    })
    alert('Sanção registada com sucesso!')
    // Limpar formulário
    form.estudante = ''
    form.tipo_sancao = ''
    form.descricao = ''
    showForm.value = false
    // Recarregar a lista
    refresh()
  } catch (error: any) {
    const msg = error.response?._data?.erro || 'Erro ao registar a sanção. Verifique os dados.'
    alert(msg)
  } finally {
    saving.value = false
  }
}

// Helpers
const formatDia = (d: string) => new Date(d).getDate().toString().padStart(2, '0')
const formatMesAno = (d: string) => new Date(d).toLocaleDateString('pt-PT', { month: 'short', year: 'numeric' })
</script>

<style scoped>
.admin-input {
  @apply w-full bg-stone-50 dark:bg-gray-900 border border-stone-200 dark:border-gray-700 rounded-xl py-3 px-4 focus:outline-none focus:ring-2 focus:ring-rose-200 dark:focus:ring-rose-900 transition-all font-medium text-gray-800 dark:text-white;
}
</style>
<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 md:py-8">
    
    <!-- Cabeçalho -->
    <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6">
      <div>
        <h1 class="text-2xl md:text-3xl font-bold text-slate-900 dark:text-white">Gestão Disciplinar</h1>
        <p class="text-sm md:text-base text-slate-500 dark:text-slate-400 mt-1">Registo de ocorrências e sanções do internato.</p>
      </div>

      <button 
        @click="showForm = !showForm"
        :class="[
          'px-5 py-2.5 rounded-lg font-medium text-sm transition-colors flex items-center gap-2 min-h-[44px]',
          showForm 
            ? 'bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700' 
            : 'bg-blue-600 hover:bg-blue-700 text-white'
        ]"
      >
        <BootstrapIcon :name="showForm ? 'x-lg' : 'exclamation-triangle-fill'" class="w-4 h-4" />
        {{ showForm ? 'Cancelar Registo' : 'Registar Ocorrência' }}
      </button>
    </div>

    <!-- Formulário de nova sanção -->
    <div v-show="showForm" class="bg-white dark:bg-slate-900 rounded-xl p-5 md:p-6 border border-slate-200 dark:border-slate-800 shadow-sm mb-6 transition-all">
      <h3 class="text-base font-semibold text-slate-900 dark:text-white flex items-center gap-2 mb-5 border-b border-slate-100 dark:border-slate-800 pb-3">
        <BootstrapIcon name="pen-fill" class="w-5 h-5 text-slate-400" />
        Nova Ocorrência Disciplinar
      </h3>

      <form @submit.prevent="submitSancao" class="space-y-4">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          
          <div>
            <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Estudante Infrator</label>
            <select v-model="form.estudante" required class="input">
              <option value="" disabled>Selecione o estudante...</option>
              <option v-for="aluno in estudantesLista" :key="aluno.utilizador_id" :value="aluno.utilizador_id">
                {{ aluno.nome_completo }} (Quarto {{ aluno.quarto_numero || 'N/A' }})
              </option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Data da Ocorrência</label>
            <input v-model="form.data_ocorrencia" type="date" required class="input" />
          </div>

          <div class="md:col-span-2">
            <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Tipo de Sanção</label>
            <div class="flex flex-wrap gap-2">
              <label v-for="tipo in tiposSancao" :key="tipo" class="cursor-pointer">
                <input type="radio" v-model="form.tipo_sancao" :value="tipo" class="peer sr-only" required />
                <div class="px-4 py-2 rounded-lg text-sm font-medium border border-slate-200 dark:border-slate-700 text-slate-500 dark:text-slate-400 peer-checked:border-blue-500 peer-checked:bg-blue-50 peer-checked:text-blue-600 dark:peer-checked:bg-blue-900/20 dark:peer-checked:text-blue-400 transition-all">
                  {{ tipo }}
                </div>
              </label>
            </div>
          </div>

          <div class="md:col-span-2">
            <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Descrição / Motivo</label>
            <textarea 
              v-model="form.descricao" 
              required 
              rows="3"
              placeholder="Descreva o que aconteceu detalhadamente..." 
              class="input resize-none"
            ></textarea>
          </div>

          <div class="md:col-span-2">
            <label class="flex items-center gap-2 cursor-pointer">
              <input type="checkbox" v-model="form.notificado_encarregado" class="w-4 h-4 rounded border-slate-300 dark:border-slate-700 text-blue-600 focus:ring-blue-500" />
              <span class="text-sm text-slate-700 dark:text-slate-300">Notificar Encarregado sobre esta sanção</span>
            </label>
            <p class="text-xs text-slate-500 dark:text-slate-400 ml-6">Marque se o encarregado já foi informado desta ocorrência.</p>
          </div>
        </div>

        <div class="flex justify-end pt-2 border-t border-slate-100 dark:border-slate-800">
          <button 
            type="submit" 
            :disabled="saving" 
            class="px-5 py-2.5 rounded-lg bg-blue-600 hover:bg-blue-700 text-white font-medium text-sm transition-colors disabled:opacity-60 disabled:cursor-not-allowed flex items-center gap-2 min-h-[44px]"
          >
            <span v-if="saving" class="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full"></span>
            {{ saving ? 'A registar...' : 'Salvar no Registo' }}
          </button>
        </div>
      </form>
    </div>

    <!-- Listagem de sanções -->
    <section class="bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm overflow-hidden">
      <div class="p-5 border-b border-slate-100 dark:border-slate-800 bg-slate-50 dark:bg-slate-800/50">
        <h3 class="font-semibold text-slate-900 dark:text-white uppercase tracking-wider text-xs">Últimas Sanções Aplicadas</h3>
      </div>
      
      <div v-if="pendingList" class="p-8 text-center">
        <div class="animate-spin h-8 w-8 border-2 border-blue-600 border-t-transparent rounded-full mx-auto mb-3"></div>
        <p class="text-slate-500 dark:text-slate-400 text-sm">A carregar registos...</p>
      </div>
      
      <div v-else-if="sancoesLista.length === 0" class="p-12 text-center">
        <BootstrapIcon name="shield-check" class="w-12 h-12 text-emerald-500 dark:text-emerald-400 mb-3 mx-auto" />
        <p class="text-slate-500 dark:text-slate-400 font-medium">Nenhum registo disciplinar recente.</p>
      </div>

      <div v-else class="divide-y divide-slate-100 dark:divide-slate-800">
        <div v-for="s in sancoesLista" :key="s.id" class="p-5 hover:bg-slate-50/50 dark:hover:bg-slate-800/30 transition-colors flex flex-col md:flex-row gap-4">
          <div class="shrink-0 text-center md:border-r md:pr-5 border-slate-100 dark:border-slate-800 min-w-[90px]">
            <span class="block text-2xl font-bold text-rose-600 dark:text-rose-400">{{ formatDia(s.data_ocorrencia) }}</span>
            <span class="block text-xs font-medium text-slate-400 uppercase">{{ formatMesAno(s.data_ocorrencia) }}</span>
          </div>
          <div class="flex-1 space-y-2">
            <div class="flex flex-wrap items-center justify-between gap-2">
              <h4 class="font-semibold text-slate-900 dark:text-white">
                {{ nomeEstudanteMap[s.estudante] || `Estudante #${s.estudante}` }}
              </h4>
              <div class="flex items-center gap-2">
                <span class="px-2.5 py-0.5 rounded-md text-xs font-medium bg-rose-50 dark:bg-rose-900/30 text-rose-700 dark:text-rose-300 border border-rose-200 dark:border-rose-800/30">
                  {{ s.tipo_sancao }}
                </span>
                <span 
                  v-if="s.notificado_encarregado" 
                  class="px-2.5 py-0.5 rounded-md text-xs font-medium bg-emerald-50 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800/30 flex items-center gap-1"
                  title="Encarregado já foi notificado"
                >
                  <BootstrapIcon name="check-circle-fill" class="w-3 h-3" />
                  Notificado
                </span>
                <button 
                  v-else 
                  @click="marcarComoNotificado(s.id)" 
                  :disabled="notificandoId === s.id"
                  class="px-2.5 py-0.5 rounded-md text-xs font-medium bg-amber-50 dark:bg-amber-900/30 text-amber-700 dark:text-amber-300 border border-amber-200 dark:border-amber-800/30 hover:bg-amber-100 dark:hover:bg-amber-800/40 transition-colors flex items-center gap-1"
                  title="Marcar como notificado"
                >
                  <span v-if="notificandoId === s.id" class="animate-spin h-3 w-3 border-2 border-current border-t-transparent rounded-full"></span>
                  <BootstrapIcon v-else name="bell-fill" class="w-3 h-3" />
                  Notificar
                </button>
              </div>
            </div>
            <p class="text-sm text-slate-600 dark:text-slate-300 italic">"{{ s.descricao }}"</p>
          </div>
        </div>
      </div>
    </section>

  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'

const { api } = useApi()

const showForm = ref(false)
const saving = ref(false)
const notificandoId = ref<number | null>(null)

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
  descricao: '',
  notificado_encarregado: false
})

// Lista de estudantes (para o select)
const { data: estudantesRaw } = await useAsyncData('admin-estudantes-sancoes', 
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

// Lista de sanções
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
    form.estudante = ''
    form.tipo_sancao = ''
    form.descricao = ''
    form.notificado_encarregado = false
    showForm.value = false
    refresh()
  } catch (error: any) {
    const msg = error.response?._data?.erro || 'Erro ao registar a sanção. Verifique os dados.'
    alert(msg)
  } finally {
    saving.value = false
  }
}

async function marcarComoNotificado(sancaoId: number) {
  notificandoId.value = sancaoId
  try {
    await api(`/admin/sancoes/${sancaoId}/`, {
      method: 'PATCH',
      body: { notificado_encarregado: true }
    })
    refresh()
  } catch (error: any) {
    const msg = error.response?._data?.erro || 'Erro ao actualizar. Tente novamente.'
    alert(msg)
  } finally {
    notificandoId.value = null
  }
}

// Helpers
const formatDia = (d: string) => new Date(d).getDate().toString().padStart(2, '0')
const formatMesAno = (d: string) => new Date(d).toLocaleDateString('pt-PT', { month: 'short', year: 'numeric' })
</script>

<style scoped>
.input {
  @apply w-full px-4 py-2.5 bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-lg text-sm text-slate-900 dark:text-white placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors;
}
</style>
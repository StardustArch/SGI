<template>
  <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-6 md:py-8">
    
    <!-- Cabeçalho -->
    <div class="flex items-center gap-3 mb-6 md:mb-8">
      <NuxtLink 
        to="/dashboard/admin/students" 
        class="p-2 rounded-lg bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 text-slate-500 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800 hover:text-slate-700 dark:hover:text-slate-300 transition shadow-sm"
      >
        <BootstrapIcon name="arrow-left" class="w-5 h-5" />
      </NuxtLink>
      <h1 class="text-2xl md:text-3xl font-bold text-slate-900 dark:text-white">Ficha do Interno</h1>
    </div>

    <!-- Loading -->
    <div v-if="pending" class="animate-pulse space-y-4">
      <div class="h-40 bg-slate-100 dark:bg-slate-800 rounded-xl"></div>
      <div class="h-96 bg-slate-100 dark:bg-slate-800 rounded-xl"></div>
    </div>

    <!-- Conteúdo -->
    <div v-else class="space-y-5 md:space-y-6">
      
      <!-- Card de Identificação -->
      <section class="bg-white dark:bg-slate-900 rounded-xl p-5 md:p-6 border border-slate-200 dark:border-slate-800 shadow-sm">
        <div class="flex flex-col md:flex-row items-center md:items-start gap-5">
          <div class="h-20 w-20 md:h-24 md:w-24 rounded-full bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 flex items-center justify-center text-2xl md:text-3xl font-bold border border-blue-100 dark:border-blue-800 shrink-0">
            {{ form.nome_completo?.charAt(0)?.toUpperCase() }}
          </div>
          <div class="text-center md:text-left flex-1">
            <h2 class="text-xl md:text-2xl font-bold text-slate-900 dark:text-white break-words">
              {{ form.nome_completo }}
            </h2>
            <p class="text-sm text-slate-500 dark:text-slate-400 mt-1">
              {{ form.email || 'Sem email de login' }}
            </p>
            <div class="flex flex-wrap justify-center md:justify-start gap-2 mt-3">
              <span class="px-2.5 py-0.5 rounded-md bg-slate-100 dark:bg-slate-800 text-xs font-medium border border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-300">
                {{ form.bi || 'Sem BI' }}
              </span>
              <span :class="[
                'px-2.5 py-0.5 rounded-md text-xs font-medium border',
                form.estado === 'Activo' 
                  ? 'bg-emerald-50 text-emerald-700 border-emerald-200 dark:bg-emerald-900/20 dark:text-emerald-400 dark:border-emerald-800/30' 
                  : 'bg-red-50 text-red-700 border-red-200 dark:bg-red-900/20 dark:text-red-400 dark:border-red-800/30'
              ]">
                {{ form.estado }}
              </span>
            </div>
          </div>
        </div>
      </section>

      <!-- Card de Edição -->
      <section class="bg-white dark:bg-slate-900 rounded-xl p-5 md:p-6 border border-slate-200 dark:border-slate-800 shadow-sm">
        <h3 class="text-base font-semibold text-slate-900 dark:text-white flex items-center gap-2 mb-5 border-b border-slate-100 dark:border-slate-800 pb-3">
          <BootstrapIcon name="pencil-square" class="w-5 h-5 text-slate-400" />
          Editar Informações
        </h3>

        <form @submit.prevent="handleUpdate" class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- Nome Completo -->
          <div>
            <label class="label">Nome Completo</label>
            <input v-model="form.nome_completo" type="text" class="input" />
          </div>
          <!-- Curso -->
          <div>
            <label class="label">Curso</label>
            <input v-model="form.curso" type="text" class="input" />
          </div>
          <!-- Quarto (desabilitado) -->
          <div>
            <label class="label">Quarto</label>
            <input v-model="form.quarto_numero" type="text" disabled class="input bg-slate-100 dark:bg-slate-800 cursor-not-allowed" />
          </div>
          <!-- Estado -->
          <div>
            <label class="label">Estado</label>
            <select v-model="form.estado" class="input">
              <option value="Activo">Activo</option>
              <option value="Inactivo">Inactivo</option>
            </select>
          </div>
          <!-- Data Nascimento -->
          <div>
            <label class="label">Data de Nascimento</label>
            <input v-model="form.data_nascimento" type="date" class="input" />
          </div>
          <!-- BI -->
          <div>
            <label class="label">BI</label>
            <input v-model="form.bi" type="text" class="input" />
          </div>
          <!-- NUIT -->
          <div>
            <label class="label">NUIT</label>
            <input v-model="form.nuit" type="text" class="input" />
          </div>
          <!-- Ano Lectivo -->
          <div>
            <label class="label">Ano Lectivo</label>
            <input v-model="form.ano_lectivo" type="text" class="input" />
          </div>
          <!-- Nacionalidade -->
          <div>
            <label class="label">Nacionalidade</label>
            <input v-model="form.nacionalidade" type="text" class="input" />
          </div>
          <!-- Condições de Saúde (full width) -->
          <div class="md:col-span-2">
            <label class="label">Condições de Saúde</label>
            <textarea v-model="form.condicao_saude" rows="2" class="input"></textarea>
          </div>
          <!-- Telefone Pessoal -->
          <div>
            <label class="label">Telefone Pessoal</label>
            <input v-model="form.telefone_pessoal" type="tel" class="input" />
          </div>
          <!-- Email Pessoal -->
          <div>
            <label class="label">Email Pessoal</label>
            <input v-model="form.email_pessoal" type="email" class="input" />
          </div>
          <!-- Morada (full width) -->
          <div class="md:col-span-2">
            <label class="label">Morada</label>
            <textarea v-model="form.morada" rows="2" class="input"></textarea>
          </div>
          <!-- Nome da Mãe -->
          <div>
            <label class="label">Nome da Mãe</label>
            <input v-model="form.nome_mae" type="text" class="input" />
          </div>
          <!-- Nome do Pai -->
          <div>
            <label class="label">Nome do Pai</label>
            <input v-model="form.nome_pai" type="text" class="input" />
          </div>

          <!-- Botão de submissão -->
          <div class="md:col-span-2 flex justify-end pt-2">
            <button 
              type="submit" 
              :disabled="updating" 
              class="px-5 py-2.5 rounded-lg bg-blue-600 hover:bg-blue-700 text-white font-medium text-sm transition-colors disabled:opacity-60 disabled:cursor-not-allowed flex items-center gap-2 min-h-[44px]"
            >
              <span v-if="updating" class="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full"></span>
              {{ updating ? 'A guardar...' : 'Guardar Alterações' }}
            </button>
          </div>
        </form>
      </section>

      <!-- Card do Encarregado -->
      <section v-if="encarregado" class="bg-white dark:bg-slate-900 rounded-xl p-5 md:p-6 border border-slate-200 dark:border-slate-800 shadow-sm">
        <NuxtLink 
          :to="`/dashboard/admin/guardian/${encarregado.id}`" 
          class="flex items-center gap-4 group hover:bg-slate-50 dark:hover:bg-slate-800/50 rounded-lg p-3 -m-3 transition-colors"
        >
          <div class="h-12 w-12 rounded-full bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 flex items-center justify-center font-bold border border-blue-100 dark:border-blue-800">
            {{ encarregado.nome_completo?.charAt(0)?.toUpperCase() }}
          </div>
          <div class="flex-1 min-w-0">
            <p class="font-semibold text-slate-900 dark:text-white group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
              {{ encarregado.nome_completo }}
            </p>
            <p class="text-sm text-slate-500 dark:text-slate-400">
              {{ encarregado.parentesco || 'Contacto' }} • Tel: {{ encarregado.telefone_principal }}
            </p>
            <p class="text-xs text-slate-400 dark:text-slate-500">
              Profissão: {{ encarregado.profissao || 'N/D' }}
            </p>
          </div>
          <BootstrapIcon name="chevron-right" class="w-5 h-5 text-slate-400 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors shrink-0" />
        </NuxtLink>
      </section>

    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, watch } from 'vue'
import { useRoute } from 'vue-router'

const { api } = useApi()
const route = useRoute()
const updating = ref(false)

const form = reactive({
  nome_completo: '',
  curso: '',
  quarto_numero: '',
  estado: '',
  email: '',
  data_nascimento: '',
  bi: '',
  telefone_pessoal: '',
  email_pessoal: '',
  morada: '',
  nome_mae: '',
  nome_pai: '',
  nuit: '',
  ano_lectivo: '',
  nacionalidade: '',
  condicao_saude: ''
})
const encarregado = ref<any>(null)

const { data: aluno, pending } = await useAsyncData('admin-student-detail', 
  () => api<any>(`/admin/estudantes/${route.params.id}/`)
)

watch(aluno, (val) => {
  if (val) {
    form.nome_completo = val.nome_completo
    form.curso = val.curso
    form.quarto_numero = val.quarto_numero
    form.estado = val.estado
    form.email = val.email
    form.data_nascimento = val.data_nascimento || ''
    form.bi = val.bi || ''
    form.telefone_pessoal = val.telefone_pessoal || ''
    form.email_pessoal = val.email_pessoal || ''
    form.morada = val.morada || ''
    form.nome_mae = val.nome_mae || ''
    form.nome_pai = val.nome_pai || ''
    form.nuit = val.nuit || ''
    form.ano_lectivo = val.ano_lectivo || ''
    form.nacionalidade = val.nacionalidade || ''
    form.condicao_saude = val.condicao_saude || ''
    encarregado.value = val.encarregado || null
  }
}, { immediate: true })

async function handleUpdate() {
  updating.value = true
  try {
    await api(`/admin/estudantes/${route.params.id}/`, {
      method: 'PATCH',
      body: {
        nome_completo: form.nome_completo,
        curso: form.curso,
        estado: form.estado,
        data_nascimento: form.data_nascimento,
        bi: form.bi,
        nuit: form.nuit,
        ano_lectivo: form.ano_lectivo,
        nacionalidade: form.nacionalidade,
        condicao_saude: form.condicao_saude,
        telefone_pessoal: form.telefone_pessoal,
        email_pessoal: form.email_pessoal,
        morada: form.morada,
        nome_mae: form.nome_mae,
        nome_pai: form.nome_pai
      }
    })
    alert("Dados do aluno atualizados com sucesso!")
  } catch (e) {
    alert("Erro ao atualizar dados.")
  } finally {
    updating.value = false
  }
}
</script>

<style scoped>
.label {
  @apply block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1;
}

.input {
  @apply w-full px-4 py-2.5 bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-lg text-sm text-slate-900 dark:text-white placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors;
}
</style>
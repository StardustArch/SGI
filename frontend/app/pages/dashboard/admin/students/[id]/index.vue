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

        <!-- Mensagens de erro global -->
        <div v-if="errorMsg" class="mb-4 p-3 rounded-lg bg-red-50 dark:bg-red-900/20 text-red-800 dark:text-red-300 text-sm border border-red-200 dark:border-red-800/30 flex items-start gap-2">
          <BootstrapIcon name="exclamation-triangle-fill" class="w-5 h-5 shrink-0 mt-0.5" />
          <span>{{ errorMsg }}</span>
        </div>
        <div v-if="successMsg" class="mb-4 p-3 rounded-lg bg-emerald-50 dark:bg-emerald-900/20 text-emerald-800 dark:text-emerald-300 text-sm border border-emerald-200 dark:border-emerald-800/30 flex items-start gap-2">
          <BootstrapIcon name="check-circle-fill" class="w-5 h-5 shrink-0 mt-0.5" />
          <span>{{ successMsg }}</span>
        </div>

        <form @submit.prevent="handleUpdate" class="grid grid-cols-1 md:grid-cols-2 gap-4" novalidate>
          <!-- Nome Completo -->
          <div>
            <label class="label">Nome Completo *</label>
            <input 
              v-model="form.nome_completo" 
              type="text" 
              class="input" 
              :class="{ 'border-red-500 focus:ring-red-500': errors.nome_completo }"
              data-field="nome_completo"
              @blur="validateField('nome_completo')"
            />
            <p v-if="errors.nome_completo" class="mt-1 text-xs text-red-600 dark:text-red-400 flex items-center gap-1">
              <BootstrapIcon name="exclamation-circle" class="w-3.5 h-3.5" />
              {{ errors.nome_completo }}
            </p>
          </div>

          <!-- Curso -->
          <div>
            <label class="label">Curso *</label>
            <input 
              v-model="form.curso" 
              type="text" 
              class="input" 
              :class="{ 'border-red-500 focus:ring-red-500': errors.curso }"
              data-field="curso"
              @blur="validateField('curso')"
            />
            <p v-if="errors.curso" class="mt-1 text-xs text-red-600 dark:text-red-400 flex items-center gap-1">
              <BootstrapIcon name="exclamation-circle" class="w-3.5 h-3.5" />
              {{ errors.curso }}
            </p>
          </div>

          <!-- Bloco (ex-Quarto) - apenas leitura -->
          <div>
            <label class="label">Bloco</label>
            <input 
              v-model="form.bloco" 
              type="text" 
              disabled 
              class="input bg-slate-100 dark:bg-slate-800 cursor-not-allowed" 
            />
          </div>

          <!-- Estado -->
          <div>
            <label class="label">Estado *</label>
            <select v-model="form.estado" class="input">
              <option value="Activo">Activo</option>
              <option value="Inactivo">Inactivo</option>
            </select>
          </div>

          <!-- Data Nascimento -->
          <div>
            <label class="label">Data de Nascimento *</label>
            <input 
              v-model="form.data_nascimento" 
              type="date" 
              class="input" 
              :class="{ 'border-red-500 focus:ring-red-500': errors.data_nascimento }"
              data-field="data_nascimento"
              @change="validateField('data_nascimento')"
              @blur="validateField('data_nascimento')"
            />
            <p v-if="errors.data_nascimento" class="mt-1 text-xs text-red-600 dark:text-red-400 flex items-center gap-1">
              <BootstrapIcon name="exclamation-circle" class="w-3.5 h-3.5" />
              {{ errors.data_nascimento }}
            </p>
          </div>

          <!-- BI -->
          <div>
            <label class="label">BI (10 dígitos + 2 letras maiúsculas)</label>
            <input 
              v-model="form.bi" 
              type="text" 
              class="input" 
              :class="{ 'border-red-500 focus:ring-red-500': errors.bi }"
              data-field="bi"
              @blur="validateField('bi')"
              placeholder="1234567890AB"
            />
            <p v-if="errors.bi" class="mt-1 text-xs text-red-600 dark:text-red-400 flex items-center gap-1">
              <BootstrapIcon name="exclamation-circle" class="w-3.5 h-3.5" />
              {{ errors.bi }}
            </p>
          </div>

          <!-- NUIT -->
          <div>
            <label class="label">NUIT (apenas números)</label>
            <input 
              v-model="form.nuit" 
              type="text" 
              class="input" 
              :class="{ 'border-red-500 focus:ring-red-500': errors.nuit }"
              data-field="nuit"
              @blur="validateField('nuit')"
            />
            <p v-if="errors.nuit" class="mt-1 text-xs text-red-600 dark:text-red-400 flex items-center gap-1">
              <BootstrapIcon name="exclamation-circle" class="w-3.5 h-3.5" />
              {{ errors.nuit }}
            </p>
          </div>

          <!-- Ano Lectivo -->
          <div>
            <label class="label">Ano Lectivo *</label>
            <select 
              v-model="form.ano_lectivo" 
              class="input" 
              :class="{ 'border-red-500 focus:ring-red-500': errors.ano_lectivo }"
              data-field="ano_lectivo"
              @change="validateField('ano_lectivo')"
            >
              <option value="2024/2025">2024/2025</option>
              <option value="2025/2026">2025/2026</option>
              <option value="2026/2027">2026/2027</option>
            </select>
            <p v-if="errors.ano_lectivo" class="mt-1 text-xs text-red-600 dark:text-red-400 flex items-center gap-1">
              <BootstrapIcon name="exclamation-circle" class="w-3.5 h-3.5" />
              {{ errors.ano_lectivo }}
            </p>
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
            <label class="label">Telefone Pessoal (ex: 84 123 4567)</label>
            <input 
              v-model="form.telefone_pessoal" 
              type="tel" 
              class="input" 
              :class="{ 'border-red-500 focus:ring-red-500': errors.telefone_pessoal }"
              data-field="telefone_pessoal"
              @blur="validateField('telefone_pessoal')"
              placeholder="84 123 4567"
            />
            <p v-if="errors.telefone_pessoal" class="mt-1 text-xs text-red-600 dark:text-red-400 flex items-center gap-1">
              <BootstrapIcon name="exclamation-circle" class="w-3.5 h-3.5" />
              {{ errors.telefone_pessoal }}
            </p>
          </div>

          <!-- Email Pessoal -->
          <div>
            <label class="label">Email Pessoal (opcional)</label>
            <input 
              v-model="form.email_pessoal" 
              type="email" 
              class="input" 
              :class="{ 'border-red-500 focus:ring-red-500': errors.email_pessoal }"
              data-field="email_pessoal"
              @blur="validateField('email_pessoal')"
            />
            <p v-if="errors.email_pessoal" class="mt-1 text-xs text-red-600 dark:text-red-400 flex items-center gap-1">
              <BootstrapIcon name="exclamation-circle" class="w-3.5 h-3.5" />
              {{ errors.email_pessoal }}
            </p>
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
const errorMsg = ref<string | null>(null)
const successMsg = ref<string | null>(null)

// --- Formulário ---
const form = reactive({
  nome_completo: '',
  curso: '',
  bloco: '',
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

// --- Estado de erros ---
const errors = ref<Record<string, string>>({
  nome_completo: '',
  curso: '',
  data_nascimento: '',
  bi: '',
  telefone_pessoal: '',
  nuit: '',
  email_pessoal: '',
  ano_lectivo: '',
})

// --- Helpers de validação ---
const isValidEmail = (email: string) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
const isOnlyDigits = (str: string) => /^\d+$/.test(str)
const isValidBI = (bi: string) => /^\d{10}[A-Z]{2}$/.test(bi)
const isValidMocambiquePhone = (phone: string) => {
  const digits = phone.replace(/\s/g, '')
  return /^8[2-9]\d{7}$/.test(digits)
}

const calcularIdade = (dataNasc: string) => {
  if (!dataNasc) return 0
  const nasc = new Date(dataNasc)
  const hoje = new Date()
  let idade = hoje.getFullYear() - nasc.getFullYear()
  const m = hoje.getMonth() - nasc.getMonth()
  if (m < 0 || (m === 0 && hoje.getDate() < nasc.getDate())) {
    idade--
  }
  return idade
}

// --- Validação de campo individual ---
const validateField = (field: string) => {
  let msg = ''
  
  switch (field) {
    case 'nome_completo':
      if (!form.nome_completo?.trim()) msg = 'Nome completo é obrigatório.'
      break
    case 'curso':
      if (!form.curso?.trim()) msg = 'Curso é obrigatório.'
      break
    case 'data_nascimento':
      if (form.data_nascimento) {
        const idade = calcularIdade(form.data_nascimento)
        if (idade < 15) msg = 'O estudante deve ter pelo menos 15 anos.'
        else if (idade > 100) msg = 'Data de nascimento inválida (muito antiga).'
      } else {
        msg = 'Data de nascimento é obrigatória.'
      }
      break
    case 'bi':
      if (form.bi && !isValidBI(form.bi)) msg = 'BI inválido. Use 10 dígitos + 2 letras maiúsculas (ex: 1234567890AB).'
      break
    case 'telefone_pessoal':
      if (form.telefone_pessoal && !isValidMocambiquePhone(form.telefone_pessoal)) 
        msg = 'Telefone inválido. Use 9 dígitos começando com 8 (ex: 84 123 4567).'
      break
    case 'nuit':
      if (form.nuit && !isOnlyDigits(form.nuit)) msg = 'NUIT deve conter apenas números.'
      break
    case 'email_pessoal':
      if (form.email_pessoal && !isValidEmail(form.email_pessoal)) msg = 'Email inválido.'
      break
    case 'ano_lectivo':
      if (!form.ano_lectivo) msg = 'Ano lectivo é obrigatório.'
      break
    default:
      break
  }
  
  errors.value[field] = msg
}

// --- Valida todos os campos, retorna true se válido ---
const validateForm = (): boolean => {
  const fields = [
    'nome_completo', 'curso', 'data_nascimento',
    'bi', 'telefone_pessoal', 'nuit', 'email_pessoal', 'ano_lectivo'
  ]
  fields.forEach(f => validateField(f))
  return Object.values(errors.value).every(msg => msg === '')
}

// --- Carregar dados do aluno ---
const { data: aluno, pending } = await useAsyncData('admin-student-detail', 
  () => api<any>(`/admin/estudantes/${route.params.id}/`)
)

watch(aluno, (val) => {
  console.log('Dados do aluno carregados:', val)
  if (val) {
    form.nome_completo = val.nome_completo || ''
    form.curso = val.curso || ''
    form.bloco = val.bloco ||  ''
    form.estado = val.estado || 'Activo'
    form.email = val.email || ''
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

// --- Submissão ---
async function handleUpdate() {
  // Validar formulário
  if (!validateForm()) {
    const firstError = Object.keys(errors.value).find(key => errors.value[key])
    if (firstError) {
      const el = document.querySelector(`[data-field="${firstError}"]`) as HTMLElement
      if (el) el.focus()
    }
    return
  }

  updating.value = true
  errorMsg.value = null
  successMsg.value = null

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
    successMsg.value = "Dados do aluno actualizados com sucesso!"
    // Revalidar após 2 segundos
    setTimeout(() => successMsg.value = null, 4000)
  } catch (e: any) {
    if (e.response?._data?.erro) {
      errorMsg.value = `Erro: ${e.response._data.erro}`
    } else {
      errorMsg.value = "Erro ao actualizar dados. Tente novamente."
    }
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

/* Estilo para campos com erro */
.input.border-red-500 {
  border-color: #ef4444;
}

.input.border-red-500:focus {
  box-shadow: 0 0 0 2px rgba(239, 68, 68, 0.3);
  border-color: #ef4444;
}
</style>
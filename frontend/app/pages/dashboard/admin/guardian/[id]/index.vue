<template>
  <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-6 md:py-8">
    
    <!-- Cabeçalho -->
    <div class="flex items-center gap-3 mb-6 md:mb-8">
      <NuxtLink 
        :to="voltarPara" 
        class="p-2 rounded-lg bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 text-slate-500 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800 hover:text-slate-700 dark:hover:text-slate-300 transition shadow-sm"
      >
        <BootstrapIcon name="arrow-left" class="w-5 h-5" />
      </NuxtLink>
      <h1 class="text-2xl md:text-3xl font-bold text-slate-900 dark:text-white">Ficha do Encarregado</h1>
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
              Perfil de Responsável / Contacto de Emergência
            </p>
            <div class="flex flex-wrap justify-center md:justify-start gap-2 mt-3">
              <span class="px-2.5 py-0.5 rounded-md bg-slate-100 dark:bg-slate-800 text-xs font-medium border border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-300">
                {{ form.telefone_principal || 'Sem telefone' }}
              </span>
              <span v-if="form.email_contacto" class="px-2.5 py-0.5 rounded-md bg-slate-100 dark:bg-slate-800 text-xs font-medium border border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-300">
                {{ form.email_contacto }}
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

        <!-- Mensagens de erro/sucesso -->
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
          <div class="md:col-span-2">
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

          <!-- Telefone Principal -->
          <div>
            <label class="label">Telefone Principal *</label>
            <input 
              v-model="form.telefone_principal" 
              type="tel" 
              class="input" 
              :class="{ 'border-red-500 focus:ring-red-500': errors.telefone_principal }"
              data-field="telefone_principal"
              @blur="validateField('telefone_principal')"
              placeholder="84 123 4567"
            />
            <p v-if="errors.telefone_principal" class="mt-1 text-xs text-red-600 dark:text-red-400 flex items-center gap-1">
              <BootstrapIcon name="exclamation-circle" class="w-3.5 h-3.5" />
              {{ errors.telefone_principal }}
            </p>
          </div>

          <!-- Email de Contacto -->
          <div>
            <label class="label">Email de Contacto</label>
            <input 
              v-model="form.email_contacto" 
              type="email" 
              class="input" 
              :class="{ 'border-red-500 focus:ring-red-500': errors.email_contacto }"
              data-field="email_contacto"
              @blur="validateField('email_contacto')"
              placeholder="exemplo@email.com"
            />
            <p v-if="errors.email_contacto" class="mt-1 text-xs text-red-600 dark:text-red-400 flex items-center gap-1">
              <BootstrapIcon name="exclamation-circle" class="w-3.5 h-3.5" />
              {{ errors.email_contacto }}
            </p>
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

      <!-- Card de Educandos Associados -->
      <section class="bg-white dark:bg-slate-900 rounded-xl p-5 md:p-6 border border-slate-200 dark:border-slate-800 shadow-sm">
        <h3 class="text-base font-semibold text-slate-900 dark:text-white flex items-center gap-2 mb-4">
          <BootstrapIcon name="people" class="w-5 h-5 text-slate-400" />
          Educandos Associados
        </h3>
        <div class="flex flex-wrap gap-2">
          <span 
            v-for="(aluno, idx) in encarregado?.educandos" 
            :key="idx" 
            class="px-3 py-1.5 bg-slate-50 dark:bg-slate-800 rounded-lg text-sm font-medium text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700"
          >
            {{ aluno }}
          </span>
          <span v-if="!encarregado?.educandos?.length" class="text-sm text-slate-400 dark:text-slate-500 italic">
            Nenhum educando associado.
          </span>
        </div>
      </section>

    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, watch, computed } from 'vue'
import { useRoute } from 'vue-router'

const { api } = useApi()
const route = useRoute()
const updating = ref(false)
const errorMsg = ref<string | null>(null)
const successMsg = ref<string | null>(null)

// --- Formulário ---
const form = reactive({
  nome_completo: '',
  telefone_principal: '',
  email_contacto: ''
})

const encarregado = ref<any>(null)

// --- Estado de erros ---
const errors = ref<Record<string, string>>({
  nome_completo: '',
  telefone_principal: '',
  email_contacto: ''
})

// --- Helpers de validação ---
const isValidEmail = (email: string) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
const isValidMocambiquePhone = (phone: string) => {
  const digits = phone.replace(/\s/g, '')
  return /^8[2-9]\d{7}$/.test(digits)
}

// --- Validação de campo individual ---
const validateField = (field: string) => {
  let msg = ''
  
  switch (field) {
    case 'nome_completo':
      if (!form.nome_completo?.trim()) msg = 'Nome completo é obrigatório.'
      break
    case 'telefone_principal':
      if (!form.telefone_principal?.trim()) {
        msg = 'Telefone principal é obrigatório.'
      } else if (!isValidMocambiquePhone(form.telefone_principal)) {
        msg = 'Telefone inválido. Use 9 dígitos começando com 8 (ex: 84 123 4567).'
      }
      break
    case 'email_contacto':
      if (form.email_contacto && !isValidEmail(form.email_contacto)) {
        msg = 'Email inválido.'
      }
      break
    default:
      break
  }
  
  errors.value[field] = msg
}

// --- Valida todos os campos, retorna true se válido ---
const validateForm = (): boolean => {
  const fields = ['nome_completo', 'telefone_principal', 'email_contacto']
  fields.forEach(f => validateField(f))
  return Object.values(errors.value).every(msg => msg === '')
}

// --- Voltar para onde? ---
const voltarPara = computed(() => {
  if (route.query.student) {
    return `/dashboard/admin/students/${route.query.student}`
  }
  return '/dashboard/admin/guardian'
})

// --- Carregar dados do encarregado ---
const { data: encarregadoData, pending } = await useAsyncData('admin-encarregado-detail', 
  () => api<any>(`/admin/encarregados/${route.params.id}/`)
)

watch(encarregadoData, (val) => {
  console.log('Dados do encarregado carregados:', val)
  if (val) {
    form.nome_completo = val.nome_completo || ''
    form.telefone_principal = val.telefone_principal || ''
    form.email_contacto = val.email_contacto || ''
    encarregado.value = val
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
    await api(`/admin/encarregados/${route.params.id}/`, {
      method: 'PATCH',
      body: {
        nome_completo: form.nome_completo,
        telefone_principal: form.telefone_principal,
        email_contacto: form.email_contacto
      }
    })
    successMsg.value = "Dados do encarregado atualizados com sucesso!"
    setTimeout(() => successMsg.value = null, 4000)
  } catch (e: any) {
    if (e.response?._data?.telefone_principal) {
      errorMsg.value = "Este telefone já está em uso."
    } else if (e.response?._data?.erro) {
      errorMsg.value = `Erro: ${e.response._data.erro}`
    } else {
      errorMsg.value = "Erro ao atualizar dados. Tente novamente."
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

/* Estilo para inputs desabilitados */
.input:disabled {
  @apply bg-slate-100 dark:bg-slate-800 cursor-not-allowed opacity-70;
}
</style>
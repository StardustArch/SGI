<template>
  <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-6 md:py-8">
    
    <!-- Cabeçalho -->
    <div class="mb-6 md:mb-8">
      <NuxtLink to="/dashboard/admin/users" class="inline-flex items-center gap-1 text-sm text-slate-500 dark:text-slate-400 hover:text-blue-600 dark:hover:text-blue-400 mb-3 transition-colors">
        <BootstrapIcon name="arrow-left" class="w-4 h-4" />
        Voltar para lista de utilizadores
      </NuxtLink>
      <h1 class="text-2xl md:text-3xl font-bold text-slate-900 dark:text-white">Criar Utilizador Interno</h1>
      <p class="text-sm md:text-base text-slate-500 dark:text-slate-400 mt-1">
        Cria uma conta para Gestor, Financeiro, Disciplinar ou Suporte. Podes atribuir mais de um perfil à mesma pessoa.
      </p>
    </div>

    <!-- Formulário -->
    <form @submit.prevent="submeter" class="bg-white dark:bg-slate-900 rounded-xl p-5 md:p-6 border border-slate-200 dark:border-slate-800 shadow-sm space-y-5">
      
      <!-- Nome Completo -->
      <div>
        <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Nome Completo *</label>
        <input 
          v-model="form.nome_completo" 
          type="text" 
          required 
          class="w-full px-4 py-2.5 bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-lg text-sm text-slate-900 dark:text-white placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors" 
          placeholder="Ex: Maria José Sitoe" 
        />
      </div>

      <!-- Email -->
      <div>
        <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Email *</label>
        <input 
          v-model="form.email" 
          type="email" 
          required 
          class="w-full px-4 py-2.5 bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-lg text-sm text-slate-900 dark:text-white placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors" 
          placeholder="nome@iicb.co.mz" 
        />
      </div>

      <!-- Perfis -->
      <div>
        <label class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Perfis *</label>
        <div class="flex flex-wrap gap-2">
          <label v-for="perfil in perfisDisponiveis" :key="perfil" class="cursor-pointer">
            <input type="checkbox" v-model="form.perfis" :value="perfil" class="peer sr-only" />
            <div class="px-4 py-2 rounded-lg text-sm font-medium border border-slate-200 dark:border-slate-700 text-slate-500 dark:text-slate-400 peer-checked:border-blue-500 peer-checked:bg-blue-50 peer-checked:text-blue-600 dark:peer-checked:bg-blue-900/20 dark:peer-checked:text-blue-400 transition-all">
              {{ perfil }}
            </div>
          </label>
        </div>
        <p v-if="form.perfis.length === 0 && submitted" class="text-xs text-rose-600 dark:text-rose-400 mt-2 flex items-center gap-1">
          <BootstrapIcon name="exclamation-circle" class="w-3.5 h-3.5" />
          Selecciona pelo menos um perfil.
        </p>
      </div>

      <!-- Botão -->
      <div class="flex justify-end pt-2 border-t border-slate-100 dark:border-slate-800">
        <button
          type="submit"
          :disabled="saving"
          class="px-6 py-2.5 rounded-lg bg-blue-600 hover:bg-blue-700 text-white font-medium text-sm transition-colors disabled:opacity-60 disabled:cursor-not-allowed flex items-center gap-2 min-h-[44px]"
        >
          <span v-if="saving" class="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full"></span>
          <BootstrapIcon v-else name="person-plus-fill" class="w-4 h-4" />
          {{ saving ? 'A criar...' : 'Criar Utilizador' }}
        </button>
      </div>
    </form>

    <!-- Mensagem de sucesso -->
    <div v-if="resultado" class="mt-5 bg-emerald-50 dark:bg-emerald-900/20 border border-emerald-200 dark:border-emerald-800/30 rounded-xl p-5">
      <div class="flex items-center gap-3 mb-2">
        <BootstrapIcon name="check-circle-fill" class="w-5 h-5 text-emerald-600 dark:text-emerald-400" />
        <h3 class="font-semibold text-emerald-800 dark:text-emerald-300">Utilizador criado com sucesso</h3>
      </div>
      <div class="text-sm text-emerald-700 dark:text-emerald-400 space-y-1">
        <p><span class="font-medium">Perfis:</span> {{ resultado.perfis.join(', ') }}</p>
        <p class="mt-2 p-3 bg-white dark:bg-slate-800 rounded-lg border border-emerald-200 dark:border-emerald-700/30">
          <span class="font-medium">Senha temporária:</span> 
          <span class="font-mono font-bold text-emerald-800 dark:text-emerald-300">{{ resultado.senha_temporaria }}</span>
        </p>
        <p class="text-xs text-emerald-600 dark:text-emerald-500 mt-2">
          ⚠️ Partilhe esta senha com a pessoa e peça para trocar no primeiro acesso.
        </p>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'

const { api } = useApi()
const router = useRouter()

const perfisDisponiveis = ['Gestor', 'Financeiro', 'Disciplinar', 'Suporte']

const form = reactive({
  nome_completo: '',
  email: '',
  perfis: [] as string[],
})

const saving = ref(false)
const submitted = ref(false)
const resultado = ref<any>(null)

async function submeter() {
  submitted.value = true
  if (form.perfis.length === 0) return

  saving.value = true
  resultado.value = null
  try {
    const data = await api<any>('/admin/utilizadores/criar/', {
      method: 'POST',
      body: { ...form },
    })
    resultado.value = data
    // Limpa o formulário mantendo o sucesso visível
    form.nome_completo = ''
    form.email = ''
    form.perfis = []
    submitted.value = false

    // Opcional: redirecionar após alguns segundos
    setTimeout(() => {
      router.push('/dashboard/admin/users')
    }, 5000)
  } catch (error: any) {
    const msg = error.response?._data?.erro || error.response?._data?.email?.[0] || 'Erro ao criar utilizador.'
    alert(msg)
  } finally {
    saving.value = false
  }
}
</script>
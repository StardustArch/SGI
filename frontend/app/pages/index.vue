<template>
  <div class="min-h-screen flex items-center justify-center bg-slate-50 dark:bg-slate-900 relative overflow-hidden px-4">
    
    <!-- Elemento decorativo de fundo -->
    <div class="absolute top-0 left-1/2 -translate-x-1/2 w-[500px] h-[500px] bg-blue-200/30 dark:bg-blue-900/20 rounded-full blur-[100px] -mt-40 pointer-events-none"></div>
    
    <!-- Card de login -->
    <div class="w-full max-w-md bg-white dark:bg-slate-900 rounded-xl shadow-sm border border-slate-200 dark:border-slate-800 p-6 md:p-8 relative z-10">
      
      <!-- Cabeçalho -->
      <div class="text-center mb-8">
        <div class="inline-flex items-center justify-center w-16 h-16 rounded-full bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 mb-4 shadow-sm">
          <BootstrapIcon name="shield-lock" class="w-8 h-8" />
        </div>
        <h1 class="text-2xl md:text-3xl font-bold text-slate-900 dark:text-white">Bem-vindo(a)</h1>
        <p class="text-sm text-slate-500 dark:text-slate-400 mt-1">Aceda ao Portal SGI</p>
      </div>
      
      <!-- Formulário -->
      <form @submit.prevent="handleLogin" class="space-y-5">
        
        <!-- Mensagem de erro -->
        <div v-if="errorMsg" class="p-3 rounded-lg bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800/30 flex items-start gap-2">
          <BootstrapIcon name="exclamation-triangle-fill" class="w-5 h-5 text-red-600 dark:text-red-400 shrink-0 mt-0.5" />
          <span class="text-sm font-medium text-red-700 dark:text-red-300">{{ errorMsg }}</span>
        </div>

        <!-- Campo Email -->
        <div>
          <label for="login" class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Email, Telefone ou Código de Acesso</label>          <div class="relative">
            <BootstrapIcon name="envelope" class="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 w-5 h-5" />
       <input 
              v-model="email" 
              id="login" 
              type="text" 
              required 
              placeholder="ex@email.com / 84xxxxxxx / IICB-QWPKLW"
              class="w-full pl-10 pr-4 py-2.5 bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-lg text-slate-900 dark:text-white placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
            >
          </div>
        </div>
        
        <!-- Campo Senha -->
        <div>
          <label for="password" class="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Senha</label>
          <div class="relative">
            <BootstrapIcon name="lock" class="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 w-5 h-5" />
            <input 
              v-model="password" 
              id="password" 
              type="password" 
              required 
              placeholder="••••••••"
              class="w-full pl-10 pr-4 py-2.5 bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-lg text-slate-900 dark:text-white placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
            >
          </div>
          <div class="flex justify-end mt-1">
            <NuxtLink to="/auth/forgot-password" class="text-sm font-medium text-blue-600 dark:text-blue-400 hover:underline">
              Esqueceu-se da senha?
            </NuxtLink>
          </div>
        </div>

        <!-- Botão de submit -->
        <button 
          type="submit" 
          :disabled="pending"
          class="w-full py-2.5 px-4 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors disabled:opacity-60 disabled:cursor-not-allowed flex justify-center items-center gap-2 min-h-[44px]"
        >
          <span v-if="pending" class="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full"></span>
          {{ pending ? 'A iniciar sessão...' : 'Entrar na Conta' }}
        </button>
      </form>

      <!-- Rodapé -->
      <div class="mt-6 text-center">
        <p class="text-xs text-slate-400 dark:text-slate-500">
          © 2026 Sistema de Gestão de Internato.
        </p>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: 'login' })

const { api } = useApi()
const { setTokens } = useAuth()
const router = useRouter()

const email = ref('')
const password = ref('')
const errorMsg = ref<string | null>(null)
const pending = ref(false)

async function handleLogin() {
  pending.value = true
  errorMsg.value = null

  try {
    const data = await api<{ access: string; refresh: string }>('/token/', {
      method: 'POST',
      body: { email: email.value, password: password.value },
    })

    setTokens(data.access, data.refresh)

    const newUser = await api<any>('/users/me/')

    let destino = '/dashboard'

    if (newUser.precisa_mudar_senha) {
      if (['Gestor', 'Financeiro', 'Disciplinar', 'Suporte'].includes(newUser.perfil_nome)) {
        destino = '/dashboard/admin/me'
      } else if (newUser.perfil_nome === 'Estudante') {
        destino = '/dashboard/student/me'
      } else if (newUser.perfil_nome === 'Encarregado') {
        destino = '/dashboard/guardian/me'
      }
    } else {
      if (['Gestor', 'Financeiro', 'Disciplinar', 'Suporte'].includes(newUser.perfil_nome)) {
        destino = '/dashboard/admin'
      } else if (newUser.perfil_nome === 'Estudante') {
        destino = '/dashboard/student'
      } else if (newUser.perfil_nome === 'Encarregado') {
        destino = '/dashboard/guardian'
      }
    }

    await router.push(destino)

  } catch (error: any) {
    errorMsg.value = 'Email ou senha incorretos. Tente novamente.'
  } finally {
    if (errorMsg.value) pending.value = false
  }
}
</script>
<template>
  <div class="min-h-screen flex items-center justify-center bg-stone-50 dark:bg-gray-900 relative overflow-hidden px-4">
    
    <div class="absolute top-0 left-1/2 -translate-x-1/2 w-[500px] h-[500px] bg-rose-200/50 dark:bg-rose-900/20 rounded-full blur-[100px] -mt-40 pointer-events-none"></div>
    
    <div class="w-full max-w-md bg-white dark:bg-gray-800 rounded-[2.5rem] shadow-xl border border-stone-100 dark:border-gray-700 p-8 md:p-10 relative z-10">
      
      <div class="text-center mb-10">
        <div class="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-rose-50 dark:bg-gray-700 text-rose-500 mb-4 shadow-sm">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" /></svg>
        </div>
        <h1 class="text-3xl font-bold text-gray-800 dark:text-white tracking-tight">Bem-vindo(a)</h1>
        <p class="text-stone-500 dark:text-gray-400 mt-2">Aceda ao Portal SGI</p>
      </div>
      
      <form @submit.prevent="handleLogin" class="space-y-6">
        
        <div v-if="errorMsg" class="p-4 rounded-xl bg-rose-50 dark:bg-rose-900/30 border border-rose-100 dark:border-rose-800 flex items-center gap-3 animate-pulse">
           <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-rose-600 dark:text-rose-400" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" /></svg>
           <span class="text-sm font-medium text-rose-700 dark:text-rose-300">{{ errorMsg }}</span>
        </div>

        <div class="space-y-1">
          <label for="email" class="text-xs font-bold text-stone-500 uppercase ml-1">Email</label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-stone-400">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207" /></svg>
            </div>
            <input 
              v-model="email" 
              id="email" 
              type="email" 
              required 
              placeholder="seu.email@exemplo.com"
              class="w-full pl-11 pr-4 py-3.5 bg-stone-50 dark:bg-gray-700 border border-stone-200 dark:border-gray-600 rounded-xl text-gray-800 dark:text-white focus:outline-none focus:ring-2 focus:ring-rose-200 dark:focus:ring-rose-900 focus:border-rose-400 transition-all font-medium"
            >
          </div>
        </div>
        
        <div class="space-y-1">
          <label for="password" class="text-xs font-bold text-stone-500 uppercase ml-1">Senha</label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-stone-400">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" /></svg>
            </div>
            <input 
              v-model="password" 
              id="password" 
              type="password" 
              required 
              placeholder="••••••••"
              class="w-full pl-11 pr-4 py-3.5 bg-stone-50 dark:bg-gray-700 border border-stone-200 dark:border-gray-600 rounded-xl text-gray-800 dark:text-white focus:outline-none focus:ring-2 focus:ring-rose-200 dark:focus:ring-rose-900 focus:border-rose-400 transition-all font-medium"
            >
          </div>
          <div class="flex justify-end pt-1">
            <NuxtLink to="/auth/forgot-password" class="text-sm font-medium text-rose-500 hover:text-rose-600 hover:underline">
              Esqueceu-se da senha?
            </NuxtLink>
          </div>
        </div>

        <button 
          type="submit" 
          :disabled="pending"
          class="w-full py-3.5 px-4 bg-gradient-to-r from-rose-500 to-rose-600 text-white font-bold rounded-xl shadow-lg shadow-rose-200 dark:shadow-none hover:shadow-xl hover:from-rose-600 hover:to-rose-700 transform hover:-translate-y-0.5 transition-all disabled:opacity-70 disabled:cursor-not-allowed flex justify-center items-center gap-2"
        >
          <span v-if="pending" class="animate-spin h-5 w-5 border-2 border-white border-t-transparent rounded-full"></span>
          {{ pending ? 'A iniciar sessão...' : 'Entrar na Conta' }}
        </button>
      </form>

      <div class="mt-8 text-center">
        <p class="text-xs text-stone-400">
          © 2026 Sistema de Gestão de Internato.
        </p>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: 'login' }) // Garante que não carrega sidebar/navbar

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
    
    // Pequeno delay visual para dar feedback de sucesso
    setTimeout(async () => {
       await router.push('/dashboard')
    }, 500)
    
  } catch (error: any) {
    errorMsg.value = 'Email ou senha incorretos. Tente novamente.'
  } finally {
    // Não paramos o pending imediatamente se for sucesso para transição suave
    if (errorMsg.value) pending.value = false
  }
}
</script>
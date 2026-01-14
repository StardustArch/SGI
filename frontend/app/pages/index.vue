<template>
  <!-- Fundo que se adapta automaticamente ao tema do sistema -->
  <div class="flex items-center justify-center min-h-screen bg-gray-100 dark:bg-gray-900">
    
    <!-- Caixa de Login -->
    <div class="w-full max-w-md p-8 space-y-6 bg-white rounded-lg shadow-md dark:bg-gray-800">
      
      <h1 class="text-2xl font-bold text-center text-gray-900 dark:text-white">
        Login SGI
      </h1>
      
      <!-- Formulário -->
      <form @submit.prevent="handleLogin" class="space-y-6">
        <!-- Campo de Email -->
        <div>
          <label for="email" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Email</label>
          <input 
            v-model="email" 
            id="email" 
            type="email" 
            required 
            class="w-full px-3 py-2 mt-1 border rounded-md shadow-sm bg-gray-50 dark:bg-gray-700 dark:text-white dark:border-gray-600 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          >
        </div>
        
        <!-- Campo de Senha -->
        <div>
          <label for="password" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Senha</label>
          <input 
            v-model="password" 
            id="password" 
            type="password" 
            required 
            class="w-full px-3 py-2 mt-1 border rounded-md shadow-sm bg-gray-50 dark:bg-gray-700 dark:text-white dark:border-gray-600 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          >
        </div>

        <!-- Mensagem de Erro -->
        <div v-if="errorMsg" class="text-sm text-red-600">
          {{ errorMsg }}
        </div>
        
        <!-- Botão de Submit -->
        <button 
          type="submit" 
          :disabled="pending"
          class="w-full px-4 py-2 font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 dark:bg-blue-500 dark:hover:bg-blue-600 disabled:opacity-50"
        >
          {{ pending ? 'Aguarde...' : 'Entrar' }}
        </button>
      </form>
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
    await router.push('/dashboard')
  } catch (error: any) {
    errorMsg.value = 'Email ou senha inválidos.'
  } finally {
    pending.value = false
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 px-4">
    <div class="max-w-md w-full space-y-8 bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-lg border border-gray-100 dark:border-gray-700">
      
      <div class="text-center">
        <h2 class="text-3xl font-bold text-gray-900 dark:text-white">Recuperar Senha</h2>
        <p class="mt-2 text-sm text-gray-600 dark:text-gray-400">
          Insira o seu email. Enviaremos um link para definir uma nova senha.
        </p>
      </div>

      <form class="mt-8 space-y-6" @submit.prevent="handleRequestReset">
        <div class="rounded-md shadow-sm -space-y-px">
          <div>
            <label for="email-address" class="sr-only">Email</label>
            <input 
              v-model="email" 
              id="email-address" 
              name="email" 
              type="email" 
              required 
              class="appearance-none rounded-xl relative block w-full px-4 py-3 border border-gray-300 dark:border-gray-600 placeholder-gray-500 text-gray-900 dark:text-white dark:bg-gray-700 focus:outline-none focus:ring-rose-500 focus:border-rose-500 sm:text-sm" 
              placeholder="O seu email de registo" 
            />
          </div>
        </div>

        <div v-if="message" :class="['text-sm font-medium text-center p-2 rounded', isError ? 'text-red-600 bg-red-50' : 'text-green-600 bg-green-50']">
          {{ message }}
        </div>

        <div>
          <button 
            type="submit" 
            :disabled="loading"
            class="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-xl text-white bg-rose-600 hover:bg-rose-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-rose-500 disabled:opacity-50 transition-all"
          >
            <span v-if="loading" class="absolute left-0 inset-y-0 flex items-center pl-3">
              <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
            </span>
            {{ loading ? 'A enviar...' : 'Enviar Link de Recuperação' }}
          </button>
        </div>
        
        <div class="text-center">
            <NuxtLink to="/" class="font-medium text-rose-600 hover:text-rose-500 text-sm">
                Voltar ao Login
            </NuxtLink>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
// Nota: Aqui não usamos useApi() porque não estamos autenticados. Usamos $fetch direto.
const email = ref('')
const loading = ref(false)
const message = ref('')
const isError = ref(false)

async function handleRequestReset() {
  loading.value = true
  message.value = ''
  isError.value = false

  try {
    await $fetch('http://127.0.0.1:8000/api/v1/auth/password-reset/', {
      method: 'POST',
      body: { email: email.value }
    })
    message.value = "Se o email existir, enviámos um link para a sua caixa de entrada."
    email.value = '' // Limpar
  } catch (err: any) {
    console.error(err)
    isError.value = true
    message.value = "Erro ao processar pedido. Verifique o email."
  } finally {
    loading.value = false
  }
}
</script>
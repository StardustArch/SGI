<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 px-4">
    <div class="max-w-md w-full space-y-8 bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-lg border border-gray-100 dark:border-gray-700">
      
      <div class="text-center">
        <h2 class="text-3xl font-bold text-gray-900 dark:text-white">Nova Senha</h2>
        <p class="mt-2 text-sm text-gray-600 dark:text-gray-400">
          Defina a sua nova senha de acesso.
        </p>
      </div>

      <div v-if="!tokenValido" class="text-center p-4 bg-red-50 text-red-600 rounded-xl">
          Link inválido ou expirado. Por favor, solicite uma nova recuperação.
          <div class="mt-4">
               <NuxtLink to="/auth/forgot-password" class="text-rose-600 font-bold underline">Pedir novo link</NuxtLink>
          </div>
      </div>

      <form v-else class="mt-8 space-y-6" @submit.prevent="handleResetConfirm">
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Nova Senha</label>
            <input v-model="password" type="password" required class="mt-1 block w-full px-4 py-3 rounded-xl border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white focus:ring-rose-500 focus:border-rose-500" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Confirmar Senha</label>
            <input v-model="confirmPassword" type="password" required class="mt-1 block w-full px-4 py-3 rounded-xl border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white focus:ring-rose-500 focus:border-rose-500" />
          </div>
        </div>

        <div v-if="message" :class="['text-sm font-medium text-center p-2 rounded', isError ? 'text-red-600 bg-red-50' : 'text-green-600 bg-green-50']">
          {{ message }}
        </div>

        <button 
            type="submit" 
            :disabled="loading"
            class="w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-xl text-white bg-rose-600 hover:bg-rose-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-rose-500 disabled:opacity-50 transition-all"
        >
            {{ loading ? 'A alterar...' : 'Alterar Senha' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
const route = useRoute()
const router = useRouter()

const password = ref('')
const confirmPassword = ref('')
const loading = ref(false)
const message = ref('')
const isError = ref(false)

// Capturar Token e UID do URL
const uid = route.query.uid as string
const token = route.query.token as string
const tokenValido = computed(() => !!uid && !!token)

async function handleResetConfirm() {
  if (password.value !== confirmPassword.value) {
      isError.value = true
      message.value = "As senhas não coincidem."
      return
  }

  loading.value = true
  message.value = ''
  isError.value = false

  try {
    await $fetch('http://127.0.0.1:8000/api/v1/auth/password-reset-confirm/', {
      method: 'PATCH',
      body: {
          uidb64: uid,
          token: token,
          password: password.value
      }
    })
    
    message.value = "Senha alterada com sucesso! A redirecionar..."
    
    setTimeout(() => {
        router.push('/')
    }, 2000)

  } catch (err: any) {
    console.error(err)
    isError.value = true
    message.value = "Erro ao alterar senha. O link pode ter expirado."
  } finally {
    loading.value = false
  }
}
</script>
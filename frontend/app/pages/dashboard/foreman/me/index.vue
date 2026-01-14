<!-- Ficheiro: frontend/app/pages/dashboard/foreman/me.vue -->
<template>
  <div class="space-y-6 dark:text-white max-w-4xl">
    <h1 class="text-3xl font-bold">O Meu Perfil (Encarregado)</h1>

    <!-- Ecrã de Carregamento -->
    <div v-if="userPending" class="space-y-4">
      <div class="h-8 bg-gray-200 dark:bg-gray-700 rounded w-1/2 animate-pulse"></div>
    </div>

    <!-- 1. Dados Básicos (Injetados do "Pai") -->
    <div v-if="userData" class="p-6 bg-white dark:bg-gray-800 rounded-lg shadow space-y-4">
      <h2 class="text-xl font-semibold mb-3">Meus Dados</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-x-6 gap-y-3">
        <div class="info-item">
          <span class="label">Nome:</span>
          <span class="value">{{ userData.first_name }} {{ userData.last_name }}</span>
        </div>
        <div class="info-item">
          <span class="label">Email de Login:</span>
          <span class="value">{{ userData.email }}</span>
        </div>
      </div>
    </div>

    <!-- 2. Formulário de Alterar Senha -->
    <div class="p-6 bg-white dark:bg-gray-800 rounded-lg shadow">
      <h2 class="text-xl font-semibold mb-3">Alterar Senha</h2>
      
      <!-- Mensagens de Feedback -->
      <div v-if="successMsg" class="mb-4 p-3 rounded-md bg-green-100 dark:bg-green-800 text-green-700 dark:text-green-200">
        {{ successMsg }}
      </div>
      <div v-if="errorMsg" class="mb-4 p-3 rounded-md bg-red-100 dark:bg-red-800 text-red-700 dark:text-red-200">
        {{ errorMsg }}
      </div>

      <form @submit.prevent="handleChangePassword" class="space-y-4">
        <div>
          <label class="label">Senha Antiga</label>
          <input v-model="formSenha.old_password" type="password" class="input" required />
        </div>
        <div>
          <label class="label">Nova Senha</label>
          <input v-model="formSenha.new_password" type="password" class="input" required />
        </div>
        <div>
          <label class="label">Confirmar Nova Senha</label>
          <input v-model="formSenha.confirm_password" type="password" class="input" required />
        </div>
        <div class="pt-2 flex justify-end">
          <button type="submit" :disabled="pendingSenha" class="btn-primary">
            {{ pendingSenha ? 'A alterar...' : 'Alterar Senha' }}
          </button>
        </div>
      </form>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, reactive, inject, type Ref } from 'vue'

const { api } = useApi()

// "Injecta" os dados fornecidos pelo "Pai" (dashboard.vue)
interface UserData {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  perfil: number;
}
const userData = inject<Ref<UserData | null>>('userData')
const userPending = inject<Ref<boolean>>('pendingData')

// --- LÓGICA DO FORMULÁRIO DE SENHA ---
const pendingSenha = ref(false)
const errorMsg = ref<string | null>(null)
const successMsg = ref<string | null>(null)

const formSenha = reactive({
  old_password: '',
  new_password: '',
  confirm_password: ''
})

async function handleChangePassword() {
  pendingSenha.value = true
  errorMsg.value = null
  successMsg.value = null

  if (formSenha.new_password !== formSenha.confirm_password) {
    errorMsg.value = "As novas senhas não coincidem."
    pendingSenha.value = false
    return
  }

  try {
    await api('/users/change-password/', {
      method: 'PATCH',
      body: {
        old_password: formSenha.old_password,
        new_password: formSenha.new_password
      }
    })
    successMsg.value = "Senha alterada com sucesso!"
    formSenha.old_password = ''
    formSenha.new_password = ''
    formSenha.confirm_password = ''
  } catch (err: any) {
    if (err.response?._data?.old_password) {
      errorMsg.value = err.response._data.old_password[0]
    } else if (err.response?._data?.new_password) {
      errorMsg.value = err.response._data.new_password[0]
    } else {
      errorMsg.value = "Ocorreu um erro ao alterar a senha."
    }
  } finally {
    pendingSenha.value = false
  }
}
</script>

<style scoped>
.label { @apply font-medium text-gray-500 dark:text-gray-400; }
.value { @apply text-gray-900 dark:text-white; }
.info-item { @apply flex flex-col; }
.btn-primary { @apply px-4 py-2 font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 disabled:opacity-50; }
.input { @apply w-full px-3 py-2 border rounded-md shadow-sm bg-gray-50 dark:bg-gray-700 dark:text-white dark:border-gray-600; }
</style>
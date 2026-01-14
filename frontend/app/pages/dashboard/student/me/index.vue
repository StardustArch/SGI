<template>
  <div class="space-y-6 dark:text-white max-w-4xl">
    <h1 class="text-3xl font-bold">O Meu Perfil</h1>

    <div v-if="pending" class="space-y-4">
      <div class="h-8 bg-gray-200 dark:bg-gray-700 rounded w-1/2 animate-pulse"></div>
      <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded w-full animate-pulse"></div>
      <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded w-3/4 animate-pulse"></div>
    </div>

    <div v-if="perfil" class="p-6 bg-white dark:bg-gray-800 rounded-lg shadow space-y-4">
      
      <div>
        <h2 class="text-xl font-semibold mb-3">Meus Dados</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-x-6 gap-y-3">
          <div class="info-item">
            <span class="label">Nome Completo:</span>
            <span class="value">{{ perfil.nome_completo }}</span>
          </div>
          <div class="info-item">
            <span class="label">Email de Login:</span>
            <span class="value">{{ perfil.email }}</span>
          </div>
          <div class="info-item">
            <span class="label">N.º Estudante:</span>
            <span class="value">{{ perfil.num_estudante }}</span>
          </div>
          <div class="info-item">
            <span class="label">Quarto:</span>
            <span class="value">{{ perfil.quarto }}</span>
          </div>
          <div class="info-item">
            <span class="label">Curso:</span>
            <span class="value">{{ perfil.curso }}</span>
          </div>
          <div class="info-item">
            <span class="label">Estado:</span>
            <span :class="perfil.estado === 'Activo' ? 'status-green' : 'status-yellow'">
              {{ perfil.estado }}
            </span>
          </div>
        </div>
      </div>

      <hr class="border-gray-200 dark:border-gray-700" />

      <div>
        <h2 class="text-xl font-semibold mb-3">Meu Encarregado de Educação</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-x-6 gap-y-3">
          <div class="info-item">
            <span class="label">Nome:</span>
            <span class="value">{{ perfil.encarregado_nome }}</span>
          </div>
          <div class="info-item">
            <span class="label">Telefone:</span>
            <span class="value">{{ perfil.encarregado_telefone }}</span>
          </div>
        </div>
      </div>
    </div>
    
    <div v-if="!showPasswordForm">
      <button 
        @click="showPasswordForm = true" 
        class="btn-secondary"
      >
        Alterar Senha
      </button>
    </div>

    <div v-if="showPasswordForm" class="p-6 bg-white dark:bg-gray-800 rounded-lg shadow">
      <h2 class="text-xl font-semibold mb-3">Alterar Senha</h2>
      
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
        <div class="pt-2 flex justify-end space-x-3">
          <button 
            type="button" 
            @click="cancelPasswordChange" 
            class="btn-secondary"
          >
            Cancelar
          </button>
          <button type="submit" :disabled="pendingSenha" class="btn-primary">
            {{ pendingSenha ? 'A alterar...' : 'Alterar Senha' }}
          </button>
        </div>
      </form>
    </div>

  </div>
</template>

<script setup lang="ts">
// Adicionámos 'ref' e 'reactive' (se já não estivessem)
import { ref, reactive } from 'vue'

const { api } = useApi()

// Buscar os dados do perfil (código existente)
const { data: perfil, pending } = await useAsyncData(
  'perfil-estudante',
  () => api<any>('/perfil/detalhes/'),
  { lazy: true }
)

// --- LÓGICA DO FORMULÁRIO DE SENHA ---

// 1. Novo estado para o "toggle"
const showPasswordForm = ref(false)

const pendingSenha = ref(false)
const errorMsg = ref<string | null>(null)
const successMsg = ref<string | null>(null)

const formSenha = reactive({
  old_password: '',
  new_password: '',
  confirm_password: ''
})

// 2. Nova função para o botão "Cancelar"
function cancelPasswordChange() {
  showPasswordForm.value = false
  // Limpar erros e campos
  errorMsg.value = null
  successMsg.value = null
  formSenha.old_password = ''
  formSenha.new_password = ''
  formSenha.confirm_password = ''
}

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
    
    // 3. Limpar o formulário e fechar o "toggle"
    cancelPasswordChange()

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
/* (Estilos existentes) */
.label { @apply font-medium text-gray-500 dark:text-gray-400; }
.value { @apply text-gray-900 dark:text-white; }
.info-item { @apply flex flex-col; }
.status-green { @apply px-2 py-0.5 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800 dark:bg-green-800 dark:text-green-100; }
.status-yellow { @apply px-2 py-0.5 inline-flex text-xs leading-5 font-semibold rounded-full bg-yellow-100 text-yellow-800 dark:bg-yellow-800 dark:text-yellow-100; }
.input { @apply w-full px-3 py-2 border rounded-md shadow-sm bg-gray-50 dark:bg-gray-700 dark:text-white dark:border-gray-600; }

/* (Novos estilos para os botões) */
.btn-primary { @apply px-4 py-2 font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 disabled:opacity-50; }
.btn-secondary { @apply px-4 py-2 font-medium bg-gray-200 dark:bg-gray-600 text-gray-800 dark:text-gray-200 rounded-md hover:bg-gray-300 dark:hover:bg-gray-500; }
</style>
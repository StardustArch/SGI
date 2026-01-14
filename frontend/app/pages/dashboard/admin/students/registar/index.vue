<template>
  <div class="space-y-6 dark:text-white max-w-4xl mx-auto">
    <div>
      <NuxtLink 
        to="/dashboard/admin/estudantes" 
        class="text-blue-600 dark:text-blue-400 hover:underline mb-2 block"
      >
        &larr; Voltar para a lista de estudantes
      </NuxtLink>
      <h1 class="text-3xl font-bold">
        Registar Novo Estudante
      </h1>
    </div>

    <div v-if="successMsg" class="p-4 rounded-md bg-green-100 dark:bg-green-800 text-green-700 dark:text-green-200">
      {{ successMsg }}
    </div>
    <div v-if="errorMsg" class="p-4 rounded-md bg-red-100 dark:bg-red-800 text-red-700 dark:text-red-200">
      {{ errorMsg }}
    </div>

    <form @submit.prevent="handleRegister" class="space-y-8">
      
      <div class="p-6 bg-white dark:bg-gray-800 rounded-lg shadow">
        <h2 class="text-xl font-semibold mb-4">1. Dados do Encarregado</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="label">Nome Completo</label>
            <input v-model="form.encarregado.nome_completo" type="text" class="input" required />
          </div>
          <div>
            <label class="label">Email (para login do Encarregado)</label>
            <input v-model="form.encarregado.email" type="email" class="input" required />
          </div>
          <div>
            <label class="label">Telefone Principal</label>
            <input v-model="form.encarregado.telefone_principal" type="tel" class="input" required />
          </div>
        </div>
      </div>

      <div class="p-6 bg-white dark:bg-gray-800 rounded-lg shadow">
        <h2 class="text-xl font-semibold mb-4">2. Dados do Estudante</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="label">Nome Completo</label>
            <input v-model="form.estudante.nome_completo" type="text" class="input" required />
          </div>
          <div>
            <label class="label">Email (para login do Estudante)</label>
            <input v-model="form.estudante.email" type="email" class="input" required />
          </div>
          <div>
            <label class="label">N.º de Estudante (ID)</label>
            <input v-model="form.estudante.num_estudante" type="text" class="input" required />
          </div>
          <div>
            <label class="label">Quarto</label>
            <input v-model="form.estudante.quarto" type="text" class="input" required />
          </div>
          <div class="md:col-span-2">
            <label class="label">Curso</label>
            <input v-model="form.estudante.curso" type="text" class="input" required />
          </div>
        </div>
      </div>

      <div class="flex justify-end">
        <button type="submit" :disabled="pending" class="btn-primary">
          {{ pending ? 'A registar...' : 'Registar Estudante e Encarregado' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// Usar o api (interceptor)
const { api } = useApi()
const router = useRouter()

// Estado do formulário (com os dois objectos que a API espera)
const form = ref({
  encarregado: {
    nome_completo: '',
    email: '',
    telefone_principal: ''
  },
  estudante: {
    nome_completo: '',
    email: '',
    num_estudante: '',
    quarto: '',
    curso: ''
  }
})

const pending = ref(false)
const errorMsg = ref<string | null>(null)
const successMsg = ref<string | null>(null)

async function handleRegister() {
  pending.value = true
  errorMsg.value = null
  successMsg.value = null

  try {
    // Chamar o endpoint de registo
    const data = await api<any>('/users/admin/registar/', {
      method: 'POST',
      body: form.value
    })

    // Sucesso!
    successMsg.value = "Estudante e Encarregado registados com sucesso! (Senha padrão: mudar1234)"
    
    // Limpar o formulário (opcional)
    form.value.encarregado = { nome_completo: '', email: '', telefone_principal: '' }
    form.value.estudante = { nome_completo: '', email: '', num_estudante: '', quarto: '', curso: '' }

    // Redirecionar para a nova página de detalhes do estudante
    setTimeout(() => {
      router.push(`/dashboard/admin/estudantes/${data.estudante_id}`)
    }, 2000) // Espera 2s para o admin ler a msg de sucesso

  } catch (err: any) {
    // Tratar erros (ex: email duplicado)
    if (err.response?._data?.erro) {
      errorMsg.value = `Erro: ${err.response._data.erro}`
    } else {
      errorMsg.value = "Ocorreu um erro ao registar. Verifique se os emails ou o N.º de Estudante já existem."
    }
  } finally {
    pending.value = false
  }
}
</script>

<style scoped>
/* Estilos de formulário comuns */
.label { @apply block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1; }
.input { @apply w-full px-3 py-2 border rounded-md shadow-sm bg-gray-50 dark:bg-gray-700 dark:text-white dark:border-gray-600 focus:outline-none focus:ring-blue-500 focus:border-blue-500; }
.btn-primary { @apply px-5 py-2 font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 disabled:opacity-50; }
</style>

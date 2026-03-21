<template>
  <div class="space-y-6 dark:text-white max-w-4xl mx-auto pb-10">
    <div>
      <NuxtLink 
        to="/dashboard/admin/students" 
        class="text-blue-600 dark:text-blue-400 hover:underline mb-2 block"
      >
        &larr; Voltar para a lista de estudantes
      </NuxtLink>
      <h1 class="text-3xl font-bold">Registar Novo Estudante</h1>
    </div>

    <div v-if="successMsg" class="p-4 rounded-md bg-green-100 dark:bg-green-800 text-green-700 dark:text-green-200">
      {{ successMsg }}
    </div>
    <div v-if="errorMsg" class="p-4 rounded-md bg-red-100 dark:bg-red-800 text-red-700 dark:text-red-200">
      {{ errorMsg }}
    </div>

    <form @submit.prevent="handleRegister" class="space-y-8">
      
      <div class="p-6 bg-white dark:bg-gray-800 rounded-lg shadow">
        <h2 class="text-xl font-semibold mb-4 border-b pb-2">1. Dados do Encarregado</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="label">Nome Completo</label>
            <input v-model="form.encarregado.nome_completo" type="text" class="input" required />
          </div>
          <div>
            <label class="label">Email (Login)</label>
            <input v-model="form.encarregado.email" type="email" class="input" required />
          </div>
          <div>
            <label class="label">Telefone Principal</label>
            <input v-model="form.encarregado.telefone_principal" type="tel" class="input" required />
          </div>
        </div>
      </div>

      <div class="p-6 bg-white dark:bg-gray-800 rounded-lg shadow">
        <h2 class="text-xl font-semibold mb-4 border-b pb-2">2. Dados do Estudante</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="label">Nome Completo</label>
            <input v-model="form.estudante.nome_completo" type="text" class="input" required />
          </div>
          <div>
            <label class="label">Email (Login)</label>
            <input v-model="form.estudante.email" type="email" class="input" required />
          </div>
          <div>
            <label class="label">N.º de Estudante (ID)</label>
            <input v-model="form.estudante.num_estudante" type="text" class="input" required />
          </div>
          
          <div>
            <label class="label">Género</label>
            <select v-model="form.estudante.genero" class="input" required>
              <option value="">Selecione...</option>
              <option value="M">Masculino</option>
              <option value="F">Feminino</option>
            </select>
          </div>

          <div>
            <label class="label">Alocação de Quarto</label>
<select 
  v-model.number="form.estudante.quarto" 
  class="input" 
  required 
  :disabled="loadingQuartos"
>
  <option value="">{{ loadingQuartos ? 'A carregar...' : 'Selecione um quarto' }}</option>
  <option 
    v-for="q in quartosDisponiveis" 
    :key="q.id" 
    :value="q.id"
  >
    Bloco {{ q.bloco }} - Quarto {{ q.numero }}
  </option>
</select>
            <p v-if="form.estudante.genero" class="text-xs mt-1 text-gray-500">
              Apenas quartos {{ form.estudante.genero === 'M' ? 'Masculinos' : 'Femininos' }} serão aceites.
            </p>
          </div>

          <div>
            <label class="label">Curso</label>
            <input v-model="form.estudante.curso" type="text" class="input" required />
          </div>
        </div>
      </div>

      <div class="flex justify-end">
        <button type="submit" :disabled="pending" class="btn-primary flex items-center gap-2">
          <span v-if="pending" class="animate-spin text-lg">⏳</span>
          {{ pending ? 'A processar registo...' : 'Finalizar Registo' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'

const { api } = useApi()
const router = useRouter()

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
    genero: '', // Novo
quarto: null as number | null, // Alterado para null
    curso: ''
  }
})

const pending = ref(false)
const loadingQuartos = ref(false)
const errorMsg = ref<string | null>(null)
const successMsg = ref<string | null>(null)
const listaQuartos = ref<any[]>([])

// Carregar quartos do backend ao montar o componente
onMounted(async () => {
  loadingQuartos.value = true
  try {
    // Busca os quartos ativos e disponíveis
    listaQuartos.value = await api<any[]>('/admin/quartos/?estado=Activo')
  } catch (err) {
    console.error("Erro ao carregar quartos:", err)
    errorMsg.value = "Não foi possível carregar a lista de quartos. Verifique a conexão."
  } finally {
    loadingQuartos.value = false
  }
})
console.log(listaQuartos.value)

// Filtra quartos no frontend para ajudar o Admin a escolher o género certo
const quartosDisponiveis = computed(() => {
  if (!form.value.estudante.genero) return listaQuartos.value
  return listaQuartos.value.filter(q => q.genero_permitido === form.value.estudante.genero)
})

async function handleRegister() {
  pending.value = true
  errorMsg.value = null
  successMsg.value = null

  try {
    console.log(form.value)
    const data = await api<any>('/users/admin/registar/', {
      method: 'POST',
      body: form.value
    })

    successMsg.value = `Sucesso! Estudante alocado ao quarto e credenciais enviadas por email.`
    
    // Reset do form
    form.value.encarregado = { nome_completo: '', email: '', telefone_principal: '' }
    form.value.estudante = { nome_completo: '', email: '', num_estudante: '', genero: '', quarto: null as number | null, curso: '' }

    setTimeout(() => {
      router.push(`/dashboard/admin/students/${data.estudante_id}`)
    }, 2500)

  } catch (err: any) {
    if (err.response?._data?.erro) {
      errorMsg.value = `Erro de Validação: ${err.response._data.erro}`
    } else {
      errorMsg.value = "Erro ao registar. Verifique os dados e a lotação do quarto."
    }
  } finally {
    pending.value = false
  }
}
</script>

<style scoped>
.label { @apply block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-1; }
.input { @apply w-full px-4 py-2 border rounded-lg shadow-sm bg-gray-50 dark:bg-gray-700 dark:text-white dark:border-gray-600 focus:ring-2 focus:ring-blue-500 transition-all; }
.btn-primary { @apply px-8 py-3 font-bold text-white bg-blue-600 rounded-lg hover:bg-blue-700 dark:bg-blue-500 shadow-lg disabled:opacity-50 transition-all; }
</style>
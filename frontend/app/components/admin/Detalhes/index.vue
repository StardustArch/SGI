<template>
  <form @submit.prevent="handleUpdate" class="p-6 bg-white dark:bg-gray-800 rounded-lg shadow space-y-4 max-w-lg">
    <h3 class="text-lg font-medium leading-6 text-gray-900 dark:text-white">Editar Dados do Estudante</h3>
    
    <!-- Feedback de Sucesso/Erro -->
    <div v-if="successMsg" class="p-3 rounded-md bg-green-100 dark:bg-green-800 text-green-700 dark:text-green-200">
      {{ successMsg }}
    </div>
    <div v-if="errorMsg" class="p-3 rounded-md bg-red-100 dark:bg-red-800 text-red-700 dark:text-red-200">
      {{ errorMsg }}
    </div>

    <div>
      <label class="label">Nome Completo</label>
      <input v-model="form.nome_completo" type="text" class="input" />
    </div>
    <div>
      <label class="label">N.º Estudante</label>
      <input v-model="form.num_estudante" type="text" class="input" />
    </div>
    <div>
      <label class="label">Quarto</label>
      <input v-model="form.quarto" type="text" class="input" />
    </div>
    <div>
      <label class="label">Curso</label>
      <input v-model="form.curso" type="text" class="input" />
    </div>
    <div>
      <label class="label">Estado</label>
      <select v-model="form.estado" class="input">
        <option v-for="opt in opcoesEstado" :key="opt.value" :value="opt.value">
          {{ opt.label }}
        </option>
      </select>
    </div>
    
    <div class="pt-2">
      <button type="submit" :disabled="pending" class="btn-primary">
        {{ pending ? 'A guardar...' : 'Guardar Alterações' }}
      </button>
    </div>
  </form>
</template>

<script setup lang="ts">
const props = defineProps({
  student: { type: Object, required: true },
  opcoesEstado: { type: Array as () => { value: string, label: string }[], required: true }
})

const emit = defineEmits(['studentUpdated'])
const { accessToken } = useAuth()

// Usamos 'ref' para criar uma cópia editável dos dados
// (Nunca editar 'props' directamente)
const form = ref({
  nome_completo: props.student.nome_completo,
  num_estudante: props.student.num_estudante,
  quarto: props.student.quarto,
  curso: props.student.curso,
  estado: props.student.estado,
})

const pending = ref(false)
const errorMsg = ref<string | null>(null)
const successMsg = ref<string | null>(null)

async function handleUpdate() {
  pending.value = true
  errorMsg.value = null
  successMsg.value = null
  console.log(props.student)
  try {
    await $fetch(`/api/v1/estudantes/${props.student.utilizador}/`, {
      method: 'PATCH',
      headers: { Authorization: `Bearer ${accessToken.value}` },
      body: form.value // Envia apenas os dados do formulário
    })
    
    successMsg.value = "Dados atualizados com sucesso!"
    emit('studentUpdated') // Diz ao "pai" ([id].vue) para recarregar os dados

    // Limpa a mensagem de sucesso após 3s
    setTimeout(() => successMsg.value = null, 3000)

  } catch (err: any) {
    errorMsg.value = "Falha ao atualizar. Verifique os campos."
  } finally {
    pending.value = false
  }
}
</script>

<style scoped>
/* Estilos de formulário comuns */
.label { @apply block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1; }
.input { @apply w-full px-3 py-2 border rounded-md shadow-sm bg-gray-50 dark:bg-gray-700 dark:text-white dark:border-gray-600 focus:outline-none focus:ring-blue-500 focus:border-blue-500; }
.btn-primary { @apply px-4 py-2 font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 disabled:opacity-50; }
</style>
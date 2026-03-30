<template>
  <div class="space-y-6 dark:text-white max-w-5xl mx-auto pb-10">
    <div>
      <NuxtLink to="/dashboard/admin/students" class="text-blue-600 dark:text-blue-400 hover:underline mb-2 block">
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

      <!-- Seção: Dados do Estudante -->
      <div class="p-6 bg-white dark:bg-gray-800 rounded-lg shadow">
        <h2 class="text-xl font-semibold mb-4 border-b pb-2">Dados do Estudante</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="label">Nome Completo *</label>
            <input v-model="form.estudante.nome_completo" type="text" class="input" required />
          </div>
          <!-- REMOVIDO: campo de email do estudante -->
          <div>
            <label class="label">Curso *</label>
            <input v-model="form.estudante.curso" type="text" class="input" required />
          </div>
          <div>
            <label class="label">Género *</label>
            <select v-model="form.estudante.genero" class="input" required>
              <option value="">Selecione...</option>
              <option value="M">Masculino</option>
              <option value="F">Feminino</option>
            </select>
          </div>
          <div>
            <label class="label">Data de Nascimento</label>
            <input v-model="form.estudante.data_nascimento" type="date" class="input" />
          </div>
          <div>
            <label class="label">BI/NUIT</label>
            <input v-model="form.estudante.bi" type="text" class="input" />
          </div>
          <div>
            <label class="label">Telefone Pessoal</label>
            <input v-model="form.estudante.telefone_pessoal" type="tel" class="input" />
          </div>
          <div>
            <label class="label">Email Pessoal (opcional)</label>
            <input v-model="form.estudante.email_pessoal" type="email" class="input" />
          </div>
          <div class="md:col-span-2">
            <label class="label">Morada</label>
            <textarea v-model="form.estudante.morada" rows="2" class="input"></textarea>
          </div>
          <div>
            <label class="label">Nome da Mãe</label>
            <input v-model="form.estudante.nome_mae" type="text" class="input" />
          </div>
          <div>
            <label class="label">Nome do Pai</label>
            <input v-model="form.estudante.nome_pai" type="text" class="input" />
          </div>
          <div>
            <label class="label">Quarto *</label>
            <select v-model.number="form.estudante.quarto" class="input" required :disabled="loadingQuartos">
              <option value="">{{ loadingQuartos ? 'A carregar...' : 'Selecione um quarto' }}</option>
              <option v-for="q in quartosDisponiveis" :key="q.id" :value="q.id">
                Bloco {{ q.bloco }} - Quarto {{ q.numero }}
              </option>
            </select>
            <p v-if="form.estudante.genero" class="text-xs mt-1 text-gray-500">
              Apenas quartos {{ form.estudante.genero === 'M' ? 'Masculinos' : 'Femininos' }} disponíveis.
            </p>
          </div>
        </div>
      </div>

      <!-- Seção: Contacto de Emergência (obrigatório) -->
      <div class="p-6 bg-white dark:bg-gray-800 rounded-lg shadow">
        <h2 class="text-xl font-semibold mb-4 border-b pb-2">Contacto de Emergência</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="label">Nome Completo *</label>
            <input v-model="form.encarregado.nome_completo" type="text" class="input" required />
          </div>
          <div>
            <label class="label">Parentesco</label>
            <select v-model="form.encarregado.parentesco" class="input">
              <option value="">Selecione</option>
              <option value="Pai">Pai</option>
              <option value="Mãe">Mãe</option>
              <option value="Tio">Tio/Tia</option>
              <option value="Irmão">Irmão/Irmã</option>
              <option value="Avô">Avô/Avó</option>
              <option value="Outro">Outro</option>
            </select>
          </div>
          <div>
            <label class="label">Telefone Principal *</label>
            <input v-model="form.encarregado.telefone_principal" type="tel" class="input" required />
          </div>
          <div>
            <label class="label">Telefone Alternativo</label>
            <input v-model="form.encarregado.telefone_alternativo" type="tel" class="input" />
          </div>
          <div>
            <label class="label">BI</label>
            <input v-model="form.encarregado.bi" type="text" class="input" />
          </div>
          <div class="md:col-span-2">
            <label class="label">Morada</label>
            <textarea v-model="form.encarregado.morada" rows="2" class="input"></textarea>
          </div>
        </div>

        <div class="mt-4 flex items-center gap-2">
          <input type="checkbox" v-model="criarUsuarioEncarregado" id="criarUsuarioEncarregado" />
          <label for="criarUsuarioEncarregado">Criar acesso ao portal para o encarregado (login com telefone)</label>
        </div>
        <!-- REMOVIDO: campo de email para encarregado, pois login será com telefone -->
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
  estudante: {
    nome_completo: '',
    email: '',
    curso: '',
    genero: '',
    quarto: null as number | null,
    data_nascimento: '',
    bi: '',
    telefone_pessoal: '',
    email_pessoal: '',
    morada: '',
    nome_mae: '',
    nome_pai: ''
  },
  encarregado: {
    nome_completo: '',
    parentesco: '',
    telefone_principal: '',
    telefone_alternativo: '',
    email: '',
    bi: '',
    morada: ''
  }
})

const hasEncarregado = ref(false)
const criarUsuarioEncarregado = ref(false)
const pending = ref(false)
const loadingQuartos = ref(false)
const errorMsg = ref<string | null>(null)
const successMsg = ref<string | null>(null)
const listaQuartos = ref<any[]>([])

onMounted(async () => {
  loadingQuartos.value = true
  try {
    const response = await api<any>('/admin/quartos/?estado=Activo')
    // Se a resposta tem a estrutura paginada (results), extraia; senão, use direto
    listaQuartos.value = response.results ?? response
    console.log('Quartos carregados:', listaQuartos.value) // para debug
  } catch (err) {
    console.error("Erro ao carregar quartos:", err)
    errorMsg.value = "Não foi possível carregar a lista de quartos."
  } finally {
    loadingQuartos.value = false
  }
})

const quartosDisponiveis = computed(() => {
  if (!form.value.estudante.genero) return listaQuartos.value
  return listaQuartos.value.filter(q => q.genero_permitido === form.value.estudante.genero)
})

async function handleRegister() {
  pending.value = true
  errorMsg.value = null
  successMsg.value = null

  // Preparar payload
  const payload: any = {
    estudante: {
      nome_completo: form.value.estudante.nome_completo,
      curso: form.value.estudante.curso,
      genero: form.value.estudante.genero,
      quarto: form.value.estudante.quarto,
      data_nascimento: form.value.estudante.data_nascimento || null,
      bi: form.value.estudante.bi || null,
      telefone_pessoal: form.value.estudante.telefone_pessoal || null,
      email_pessoal: form.value.estudante.email_pessoal || null,
      morada: form.value.estudante.morada || null,
      nome_mae: form.value.estudante.nome_mae || null,
      nome_pai: form.value.estudante.nome_pai || null
    },
    encarregado: {
      nome_completo: form.value.encarregado.nome_completo,
      parentesco: form.value.encarregado.parentesco || null,
      telefone_principal: form.value.encarregado.telefone_principal,
      telefone_alternativo: form.value.encarregado.telefone_alternativo || null,
      bi: form.value.encarregado.bi || null,
      morada: form.value.encarregado.morada || null
    },
    criar_usuario_encarregado: criarUsuarioEncarregado.value
  }

  try {
    const data = await api<any>('/admin/registar/', {
      method: 'POST',
      body: payload
    })

    // Exibir o código de acesso gerado
    successMsg.value = `Sucesso! Estudante registado. Código de acesso: ${data.codigo_acesso} (senha: mudar1234)`
    
    // Reset do formulário
    form.value = {
      estudante: {
        nome_completo: '',
        email: '',
        curso: '',
        genero: '',
        quarto: null,
        data_nascimento: '',
        bi: '',
        telefone_pessoal: '',
        email_pessoal: '',
        morada: '',
        nome_mae: '',
        nome_pai: ''
      },
      encarregado: {
        nome_completo: '',
        parentesco: '',
        telefone_principal: '',
        telefone_alternativo: '',
        email: '',
        bi: '',
        morada: ''
      }
    }
    criarUsuarioEncarregado.value = false

    setTimeout(() => {
      router.push(`/dashboard/admin/students/${data.estudante_id}`)
    }, 3000)
  } catch (err: any) {
    if (err.response?._data?.erro) {
      errorMsg.value = `Erro: ${err.response._data.erro}`
    } else {
      errorMsg.value = "Erro ao registar. Verifique os dados e a lotação do quarto."
    }
  } finally {
    pending.value = false
  }
}
</script>

<style scoped>
.label {
  @apply block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-1;
}

.input {
  @apply w-full px-4 py-2 border rounded-lg shadow-sm bg-gray-50 dark:bg-gray-700 dark:text-white dark:border-gray-600 focus:ring-2 focus:ring-blue-500 transition-all;
}

.btn-primary {
  @apply px-8 py-3 font-bold text-white bg-blue-600 rounded-lg hover:bg-blue-700 dark:bg-blue-500 shadow-lg disabled:opacity-50 transition-all;
}
</style>
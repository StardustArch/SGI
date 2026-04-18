<template>
  <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-6 md:py-8">
    
    <!-- Cabeçalho -->
    <div class="mb-6 md:mb-8">
      <NuxtLink to="/dashboard/admin/students" class="inline-flex items-center gap-1 text-sm text-slate-500 dark:text-slate-400 hover:text-blue-600 dark:hover:text-blue-400 mb-3 transition-colors">
        <BootstrapIcon name="arrow-left" class="w-4 h-4" />
        Voltar para a lista de estudantes
      </NuxtLink>
      <h1 class="text-2xl md:text-3xl font-bold text-slate-900 dark:text-white">Registar Novo Estudante</h1>
      <p class="text-sm md:text-base text-slate-500 dark:text-slate-400 mt-1">Preencha os dados do novo interno e do seu encarregado.</p>
    </div>

    <!-- Mensagens de feedback -->
    <div v-if="successMsg" class="mb-6 p-4 rounded-lg bg-emerald-50 dark:bg-emerald-900/20 text-emerald-800 dark:text-emerald-300 text-sm border border-emerald-200 dark:border-emerald-800/30 flex items-start gap-2">
      <BootstrapIcon name="check-circle-fill" class="w-5 h-5 shrink-0 mt-0.5" />
      <span>{{ successMsg }}</span>
    </div>
    <div v-if="errorMsg" class="mb-6 p-4 rounded-lg bg-red-50 dark:bg-red-900/20 text-red-800 dark:text-red-300 text-sm border border-red-200 dark:border-red-800/30 flex items-start gap-2">
      <BootstrapIcon name="exclamation-triangle-fill" class="w-5 h-5 shrink-0 mt-0.5" />
      <span>{{ errorMsg }}</span>
    </div>

    <form @submit.prevent="handleRegister" class="space-y-6 md:space-y-8">

      <!-- Seção: Dados do Estudante -->
      <section class="bg-white dark:bg-slate-900 rounded-xl p-5 md:p-6 border border-slate-200 dark:border-slate-800 shadow-sm">
        <h2 class="text-base font-semibold text-slate-900 dark:text-white flex items-center gap-2 mb-5 border-b border-slate-100 dark:border-slate-800 pb-3">
          <BootstrapIcon name="person" class="w-5 h-5 text-slate-400" />
          Dados do Estudante
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="label">Nome Completo *</label>
            <input v-model="form.estudante.nome_completo" type="text" class="input" required />
          </div>
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
            <label class="label">BI</label>
            <input v-model="form.estudante.bi" type="text" class="input" />
          </div>
          <div>
            <label class="label">NUIT</label>
            <input v-model="form.estudante.nuit" type="text" class="input" />
          </div>
          <div>
            <label class="label">Telefone Pessoal</label>
            <input v-model="form.estudante.telefone_pessoal" type="tel" class="input" />
          </div>
          <div>
            <label class="label">Ano Lectivo *</label>
            <select v-model="form.estudante.ano_lectivo" class="input" required>
              <option value="2024/2025">2024/2025</option>
              <option value="2025/2026" selected>2025/2026</option>
              <option value="2026/2027">2026/2027</option>
            </select>
          </div>
          <div>
            <label class="label">Nacionalidade</label>
            <input v-model="form.estudante.nacionalidade" type="text" class="input" placeholder="Moçambicana" />
          </div>
          <div class="md:col-span-2">
            <label class="label">Condições de Saúde</label>
            <textarea v-model="form.estudante.condicao_saude" rows="2" class="input" placeholder="Alergias, medicamentos, etc."></textarea>
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
            <p v-if="form.estudante.genero" class="text-xs text-slate-500 dark:text-slate-400 mt-1">
              Apenas quartos {{ form.estudante.genero === 'M' ? 'Masculinos' : 'Femininos' }} disponíveis.
            </p>
          </div>
        </div>
      </section>

      <!-- Seção: Contacto de Emergência -->
      <section class="bg-white dark:bg-slate-900 rounded-xl p-5 md:p-6 border border-slate-200 dark:border-slate-800 shadow-sm">
        <h2 class="text-base font-semibold text-slate-900 dark:text-white flex items-center gap-2 mb-5 border-b border-slate-100 dark:border-slate-800 pb-3">
          <BootstrapIcon name="person-heart" class="w-5 h-5 text-slate-400" />
          Contacto de Emergência
        </h2>
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
            <label class="label">Profissão</label>
            <input v-model="form.encarregado.profissao" type="text" class="input" />
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

        <div class="mt-5 flex items-center gap-2">
          <input 
            type="checkbox" 
            v-model="criarUsuarioEncarregado" 
            id="criarUsuarioEncarregado" 
            class="w-4 h-4 rounded border-slate-300 dark:border-slate-700 text-blue-600 focus:ring-blue-500"
          />
          <label for="criarUsuarioEncarregado" class="text-sm text-slate-700 dark:text-slate-300 cursor-pointer">
            Criar acesso ao portal para o encarregado (login com telefone)
          </label>
        </div>
      </section>

      <!-- Botão de submissão -->
      <div class="flex justify-end">
        <button 
          type="submit" 
          :disabled="pending" 
          class="px-6 py-3 rounded-lg bg-blue-600 hover:bg-blue-700 text-white font-medium text-sm transition-colors disabled:opacity-60 disabled:cursor-not-allowed flex items-center gap-2 min-h-[44px]"
        >
          <span v-if="pending" class="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full"></span>
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
    nome_pai: '',
    nuit: '',
    ano_lectivo: '2025/2026',
    nacionalidade: 'Moçambicana',
    condicao_saude: '',
  },
  encarregado: {
    nome_completo: '',
    parentesco: '',
    telefone_principal: '',
    telefone_alternativo: '',
    email: '',
    bi: '',
    morada: '',
    profissao: ''
  }
})

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
    listaQuartos.value = response.results ?? response
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
      nome_pai: form.value.estudante.nome_pai || null,
      nuit: form.value.estudante.nuit || null,
      ano_lectivo: form.value.estudante.ano_lectivo,
      nacionalidade: form.value.estudante.nacionalidade || 'Moçambicana',
      condicao_saude: form.value.estudante.condicao_saude || null,
    },
    encarregado: {
      nome_completo: form.value.encarregado.nome_completo,
      parentesco: form.value.encarregado.parentesco || null,
      telefone_principal: form.value.encarregado.telefone_principal,
      telefone_alternativo: form.value.encarregado.telefone_alternativo || null,
      bi: form.value.encarregado.bi || null,
      morada: form.value.encarregado.morada || null,
      profissao: form.value.encarregado.profissao || null,
    },
    criar_usuario_encarregado: criarUsuarioEncarregado.value
  }

  try {
    const data = await api<any>('/admin/registar/', {
      method: 'POST',
      body: payload
    })

    successMsg.value = `Sucesso! Estudante registado. Código de acesso: ${data.codigo_acesso} (senha: mudar1234)`
    
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
        nome_pai: '',
        nuit: '',
        ano_lectivo: '2025/2026',
        nacionalidade: 'Moçambicana',
        condicao_saude: '',
      },
      encarregado: {
        nome_completo: '',
        parentesco: '',
        telefone_principal: '',
        telefone_alternativo: '',
        email: '',
        bi: '',
        morada: '',
        profissao: ''
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
  @apply block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1;
}

.input {
  @apply w-full px-4 py-2.5 bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-lg text-sm text-slate-900 dark:text-white placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors;
}
</style>
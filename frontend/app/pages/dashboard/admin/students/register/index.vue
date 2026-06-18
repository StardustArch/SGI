<template>
  <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-6 md:py-8">

    <!-- Cabeçalho -->
    <div class="mb-6 md:mb-8">
      <NuxtLink to="/dashboard/admin/students"
        class="inline-flex items-center gap-1 text-sm text-slate-500 dark:text-slate-400 hover:text-blue-600 dark:hover:text-blue-400 mb-3 transition-colors">
        <BootstrapIcon name="arrow-left" class="w-4 h-4" />
        Voltar para a lista de estudantes
      </NuxtLink>
      <h1 class="text-2xl md:text-3xl font-bold text-slate-900 dark:text-white">Registar Novo Estudante</h1>
      <p class="text-sm md:text-base text-slate-500 dark:text-slate-400 mt-1">Preencha os dados do novo interno e do seu
        encarregado.</p>
    </div>

    <!-- Mensagens de feedback -->
    <div v-if="successMsg"
      class="mb-6 p-4 rounded-lg bg-emerald-50 dark:bg-emerald-900/20 text-emerald-800 dark:text-emerald-300 text-sm border border-emerald-200 dark:border-emerald-800/30 flex items-start gap-2">
      <BootstrapIcon name="check-circle-fill" class="w-5 h-5 shrink-0 mt-0.5" />
      <span>{{ successMsg }}</span>
    </div>
    <div v-if="errorMsg"
      class="mb-6 p-4 rounded-lg bg-red-50 dark:bg-red-900/20 text-red-800 dark:text-red-300 text-sm border border-red-200 dark:border-red-800/30 flex items-start gap-2">
      <BootstrapIcon name="exclamation-triangle-fill" class="w-5 h-5 shrink-0 mt-0.5" />
      <span>{{ errorMsg }}</span>
    </div>

    <form @submit.prevent="handleRegister" class="space-y-6 md:space-y-8" novalidate>

      <!-- Seção: Dados do Estudante -->
      <section
        class="bg-white dark:bg-slate-900 rounded-xl p-5 md:p-6 border border-slate-200 dark:border-slate-800 shadow-sm">
        <h2
          class="text-base font-semibold text-slate-900 dark:text-white flex items-center gap-2 mb-5 border-b border-slate-100 dark:border-slate-800 pb-3">
          <BootstrapIcon name="person" class="w-5 h-5 text-slate-400" />
          Dados do Estudante
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- Nome Completo -->
          <div>
            <label class="label">Nome Completo *</label>
            <input v-model="form.estudante.nome_completo" type="text" class="input"
              :class="{ 'border-red-500 focus:ring-red-500': errors.nome_completo }" data-field="nome_completo"
              @blur="validateField('nome_completo')" />
            <p v-if="errors.nome_completo" class="mt-1 text-xs text-red-600 dark:text-red-400 flex items-center gap-1">
              <BootstrapIcon name="exclamation-circle" class="w-3.5 h-3.5" />
              {{ errors.nome_completo }}
            </p>
          </div>

          <!-- Curso -->
          <div>
            <label class="label">Curso *</label>
            <input v-model="form.estudante.curso" type="text" class="input"
              :class="{ 'border-red-500 focus:ring-red-500': errors.curso }" data-field="curso"
              @blur="validateField('curso')" />
            <p v-if="errors.curso" class="mt-1 text-xs text-red-600 dark:text-red-400 flex items-center gap-1">
              <BootstrapIcon name="exclamation-circle" class="w-3.5 h-3.5" />
              {{ errors.curso }}
            </p>
          </div>

          <!-- Género -->
          <div>
            <label class="label">Género *</label>
            <select v-model="form.estudante.genero" class="input"
              :class="{ 'border-red-500 focus:ring-red-500': errors.genero }" data-field="genero"
              @change="validateField('genero')">
              <option value="">Selecione...</option>
              <option value="M">Masculino</option>
              <option value="F">Feminino</option>
            </select>
            <p v-if="errors.genero" class="mt-1 text-xs text-red-600 dark:text-red-400 flex items-center gap-1">
              <BootstrapIcon name="exclamation-circle" class="w-3.5 h-3.5" />
              {{ errors.genero }}
            </p>
          </div>

          <!-- Data de Nascimento -->
          <div>
            <label class="label">Data de Nascimento</label>
            <input v-model="form.estudante.data_nascimento" type="date" class="input"
              :class="{ 'border-red-500 focus:ring-red-500': errors.data_nascimento }" data-field="data_nascimento"
              @change="validateField('data_nascimento')" @blur="validateField('data_nascimento')" />
            <p v-if="errors.data_nascimento"
              class="mt-1 text-xs text-red-600 dark:text-red-400 flex items-center gap-1">
              <BootstrapIcon name="exclamation-circle" class="w-3.5 h-3.5" />
              {{ errors.data_nascimento }}
            </p>
          </div>

          <!-- BI -->
          <div>
            <label class="label">BI </label>
            <input v-model="form.estudante.bi" type="text" class="input"
              :class="{ 'border-red-500 focus:ring-red-500': errors.bi }" data-field="bi" @blur="validateField('bi')"
              placeholder="1234567890AB" />
            <p v-if="errors.bi" class="mt-1 text-xs text-red-600 dark:text-red-400 flex items-center gap-1">
              <BootstrapIcon name="exclamation-circle" class="w-3.5 h-3.5" />
              {{ errors.bi }}
            </p>
          </div>

          <!-- NUIT -->
          <div>
            <label class="label">NUIT</label>
            <input v-model="form.estudante.nuit" type="text" class="input"
              :class="{ 'border-red-500 focus:ring-red-500': errors.nuit }" data-field="nuit"
              @blur="validateField('nuit')" />
            <p v-if="errors.nuit" class="mt-1 text-xs text-red-600 dark:text-red-400 flex items-center gap-1">
              <BootstrapIcon name="exclamation-circle" class="w-3.5 h-3.5" />
              {{ errors.nuit }}
            </p>
          </div>

          <!-- Telefone Pessoal -->
          <div>
            <label class="label">Telefone Pessoal (ex: 84 123 4567)</label>
            <input v-model="form.estudante.telefone_pessoal" type="tel" class="input"
              :class="{ 'border-red-500 focus:ring-red-500': errors.telefone_pessoal }" data-field="telefone_pessoal"
              @blur="validateField('telefone_pessoal')" placeholder="84 123 4567" />
            <p v-if="errors.telefone_pessoal"
              class="mt-1 text-xs text-red-600 dark:text-red-400 flex items-center gap-1">
              <BootstrapIcon name="exclamation-circle" class="w-3.5 h-3.5" />
              {{ errors.telefone_pessoal }}
            </p>
          </div>

          <!-- Ano Lectivo -->
          <div>
            <label class="label">Ano Lectivo *</label>
            <select v-model="form.estudante.ano_lectivo" class="input"
              :class="{ 'border-red-500 focus:ring-red-500': errors.ano_lectivo }" data-field="ano_lectivo"
              @change="validateField('ano_lectivo')">
              <option value="2024/2025">2024/2025</option>
              <option value="2025/2026" selected>2025/2026</option>
              <option value="2026/2027">2026/2027</option>
            </select>
            <p v-if="errors.ano_lectivo" class="mt-1 text-xs text-red-600 dark:text-red-400 flex items-center gap-1">
              <BootstrapIcon name="exclamation-circle" class="w-3.5 h-3.5" />
              {{ errors.ano_lectivo }}
            </p>
          </div>

          <!-- Nacionalidade -->
          <div>
            <label class="label">Nacionalidade</label>
            <input v-model="form.estudante.nacionalidade" type="text" class="input" placeholder="Moçambicana" />
          </div>

          <!-- Condições de Saúde -->
          <div class="md:col-span-2">
            <label class="label">Condições de Saúde</label>
            <textarea v-model="form.estudante.condicao_saude" rows="2" class="input"
              placeholder="Alergias, medicamentos, etc."></textarea>
          </div>

          <!-- Email Pessoal -->
          <div>
            <label class="label">Email Pessoal (opcional)</label>
            <input v-model="form.estudante.email_pessoal" type="email" class="input"
              :class="{ 'border-red-500 focus:ring-red-500': errors.email_pessoal }" data-field="email_pessoal"
              @blur="validateField('email_pessoal')" />
            <p v-if="errors.email_pessoal" class="mt-1 text-xs text-red-600 dark:text-red-400 flex items-center gap-1">
              <BootstrapIcon name="exclamation-circle" class="w-3.5 h-3.5" />
              {{ errors.email_pessoal }}
            </p>
          </div>

          <!-- Morada -->
          <div class="md:col-span-2">
            <label class="label">Morada</label>
            <textarea v-model="form.estudante.morada" rows="2" class="input"></textarea>
          </div>

          <!-- Nome da Mãe -->
          <div>
            <label class="label">Nome da Mãe</label>
            <input v-model="form.estudante.nome_mae" type="text" class="input" />
          </div>

          <!-- Nome do Pai -->
          <div>
            <label class="label">Nome do Pai</label>
            <input v-model="form.estudante.nome_pai" type="text" class="input" />
          </div>

          <!-- Quarto com autocomplete (pesquisa apenas por bloco) -->
          <div class="md:col-span-2 relative">
            <label class="label">Bloco *</label>

            <!-- Campo de pesquisa -->
            <div class="relative">
              <input ref="quartoInput" v-model="buscaQuarto" type="text" class="input pr-10"
                :class="{ 'border-red-500 focus:ring-red-500': errors.quarto }"
                placeholder="Digite o bloco (ex: A, B1, C)" @input="filtrarQuartos" @focus="mostrarSugestoes = true"
                @blur="fecharSugestoes" autocomplete="off" data-field="quarto" />
              <button v-if="buscaQuarto" @mousedown.prevent="limparQuarto"
                class="absolute right-2 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 dark:hover:text-slate-300"
                type="button">
                <BootstrapIcon name="x-circle-fill" class="w-4 h-4" />
              </button>
            </div>

            <!-- Lista de sugestões -->
            <div v-if="mostrarSugestoes && quartosFiltrados.length > 0"
              class="absolute z-10 mt-1 w-full bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg shadow-lg max-h-60 overflow-y-auto">
              <button v-for="quarto in quartosFiltrados" :key="quarto.id" @mousedown.prevent="selecionarQuarto(quarto)"
                class="w-full text-left px-4 py-2.5 text-sm text-slate-700 dark:text-slate-300 hover:bg-blue-50 dark:hover:bg-blue-900/20 transition-colors flex justify-between items-center"
                :class="{ 'bg-blue-50 dark:bg-blue-900/20': quarto.id === quartoSelecionadoId }">
                <span>
                  <span class="font-medium">Bloco {{ quarto.bloco }}</span>
                  <!-- Substituímos o número do quarto pela lotação -->
                  <span class="text-slate-500 dark:text-slate-400 ml-2">
                    {{ quarto.vagas_disponiveis || 0 }}/{{ quarto.capacidade_maxima }} camas disponíveis
                  </span>
                </span>
                <span
                  class="text-xs px-2 py-0.5 rounded-full bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300">
                  {{ quarto.genero_permitido === 'M' ? 'Masculino' : 'Feminino' }}
                </span>
              </button>
            </div>

            <!-- Mensagem de nenhum resultado -->
            <div v-else-if="mostrarSugestoes && buscaQuarto && quartosFiltrados.length === 0 && !loadingQuartos"
              class="absolute z-10 mt-1 w-full bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg shadow-lg p-3 text-center text-sm text-slate-500 dark:text-slate-400">
              Nenhum bloco encontrado para <strong>"{{ buscaQuarto }}"</strong>
            </div>

            <!-- Erro -->
            <p v-if="errors.quarto" class="mt-1 text-xs text-red-600 dark:text-red-400 flex items-center gap-1">
              <BootstrapIcon name="exclamation-circle" class="w-3.5 h-3.5" />
              {{ errors.quarto }}
            </p>

            <!-- Info de género -->
            <p v-if="form.estudante.genero && !loadingQuartos" class="text-xs text-slate-500 dark:text-slate-400 mt-1">
              Mostrando apenas quartos {{ form.estudante.genero === 'M' ? 'Masculinos' : 'Femininos' }} disponíveis.
            </p>
          </div>
        </div>
      </section>

      <!-- Seção: Contacto de Emergência -->
      <section
        class="bg-white dark:bg-slate-900 rounded-xl p-5 md:p-6 border border-slate-200 dark:border-slate-800 shadow-sm">
        <h2
          class="text-base font-semibold text-slate-900 dark:text-white flex items-center gap-2 mb-5 border-b border-slate-100 dark:border-slate-800 pb-3">
          <BootstrapIcon name="person-heart" class="w-5 h-5 text-slate-400" />
          Contacto de Emergência
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- Nome do Encarregado -->
          <div>
            <label class="label">Nome Completo *</label>
            <input v-model="form.encarregado.nome_completo" type="text" class="input"
              :class="{ 'border-red-500 focus:ring-red-500': errors.encarregado_nome }" data-field="encarregado_nome"
              @blur="validateField('encarregado_nome')" />
            <p v-if="errors.encarregado_nome"
              class="mt-1 text-xs text-red-600 dark:text-red-400 flex items-center gap-1">
              <BootstrapIcon name="exclamation-circle" class="w-3.5 h-3.5" />
              {{ errors.encarregado_nome }}
            </p>
          </div>

          <!-- Parentesco -->
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

          <!-- Profissão -->
          <div>
            <label class="label">Profissão</label>
            <input v-model="form.encarregado.profissao" type="text" class="input" />
          </div>

          <!-- Telefone Principal -->
          <div>
            <label class="label">Telefone Principal * (ex: 84 123 4567)</label>
            <input v-model="form.encarregado.telefone_principal" type="tel" class="input"
              :class="{ 'border-red-500 focus:ring-red-500': errors.telefone_principal }"
              data-field="telefone_principal" @blur="validateField('telefone_principal')" placeholder="84 123 4567" />
            <p v-if="errors.telefone_principal"
              class="mt-1 text-xs text-red-600 dark:text-red-400 flex items-center gap-1">
              <BootstrapIcon name="exclamation-circle" class="w-3.5 h-3.5" />
              {{ errors.telefone_principal }}
            </p>
          </div>

          <!-- Telefone Alternativo -->
          <div>
            <label class="label">Telefone Alternativo</label>
            <input v-model="form.encarregado.telefone_alternativo" type="tel" class="input"
              :class="{ 'border-red-500 focus:ring-red-500': errors.telefone_alternativo }"
              data-field="telefone_alternativo" @blur="validateField('telefone_alternativo')"
              placeholder="85 123 4567" />
            <p v-if="errors.telefone_alternativo"
              class="mt-1 text-xs text-red-600 dark:text-red-400 flex items-center gap-1">
              <BootstrapIcon name="exclamation-circle" class="w-3.5 h-3.5" />
              {{ errors.telefone_alternativo }}
            </p>
          </div>

          <!-- BI do Encarregado -->
          <div>
            <label class="label">BI</label>
            <input v-model="form.encarregado.bi" type="text" class="input"
              :class="{ 'border-red-500 focus:ring-red-500': errors.encarregado_bi }" data-field="encarregado_bi"
              @blur="validateField('encarregado_bi')" placeholder="1234567890AB" />
            <p v-if="errors.encarregado_bi" class="mt-1 text-xs text-red-600 dark:text-red-400 flex items-center gap-1">
              <BootstrapIcon name="exclamation-circle" class="w-3.5 h-3.5" />
              {{ errors.encarregado_bi }}
            </p>
          </div>

          <!-- Morada do Encarregado -->
          <div class="md:col-span-2">
            <label class="label">Morada</label>
            <textarea v-model="form.encarregado.morada" rows="2" class="input"></textarea>
          </div>
        </div>

        <div class="mt-5 flex items-center gap-2">
          <input type="checkbox" v-model="criarUsuarioEncarregado" id="criarUsuarioEncarregado"
            class="w-4 h-4 rounded border-slate-300 dark:border-slate-700 text-blue-600 focus:ring-blue-500" />
          <label for="criarUsuarioEncarregado" class="text-sm text-slate-700 dark:text-slate-300 cursor-pointer">
            Criar acesso ao portal para o encarregado (login com telefone)
          </label>
        </div>
      </section>

      <!-- Botão de submissão -->
      <div class="flex justify-end">
        <button type="submit" :disabled="pending"
          class="px-6 py-3 rounded-lg bg-blue-600 hover:bg-blue-700 text-white font-medium text-sm transition-colors disabled:opacity-60 disabled:cursor-not-allowed flex items-center gap-2 min-h-[44px]">
          <span v-if="pending"
            class="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full"></span>
          {{ pending ? 'A processar registo...' : 'Finalizar Registo' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'

const { api } = useApi()
const router = useRouter()

// --- Estado do formulário ---
const form = ref({
  estudante: {
    nome_completo: '',
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
const filtroBloco = ref('')

// --- Estado de erros ---
const errors = ref<Record<string, string>>({
  nome_completo: '',
  curso: '',
  genero: '',
  quarto: '',
  data_nascimento: '',
  bi: '',
  telefone_pessoal: '',
  nuit: '',
  email_pessoal: '',
  ano_lectivo: '',
  encarregado_nome: '',
  telefone_principal: '',
  telefone_alternativo: '',
  encarregado_bi: '',
})

// --- Helpers de validação ---
const isValidEmail = (email: string) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
const isOnlyDigits = (str: string) => /^\d+$/.test(str)
const isValidBI = (bi: string) => /^\d{10}[A-Z]{1}$/.test(bi) // 10 dígitos + 2 letras maiúsculas
const isValidMocambiquePhone = (phone: string) => {
  const digits = phone.replace(/\s/g, '')
  return /^8[2-9]\d{7}$/.test(digits) // 84, 85, 86, 87, 82, 83...
}

// --- Validação de campo individual ---
const validateField = (field: string) => {
  const e = form.value.estudante
  const enc = form.value.encarregado
  let msg = ''

  switch (field) {
    case 'nome_completo':
      if (!e.nome_completo?.trim()) msg = 'Nome completo é obrigatório.'
      break
    case 'curso':
      if (!e.curso?.trim()) msg = 'Curso é obrigatório.'
      break
    case 'genero':
      if (!e.genero) msg = 'Selecione o género.'
      break
    case 'quarto':
      if (!e.quarto) msg = 'Selecione um quarto.'
      break
    case 'data_nascimento':
      if (e.data_nascimento) {
        const data = new Date(e.data_nascimento)
        const hoje = new Date()
        hoje.setHours(0, 0, 0, 0)
        if (data > hoje) {
          msg = 'Data de nascimento não pode ser futura.'
        } else {
          // Calcular idade
          let idade = hoje.getFullYear() - data.getFullYear()
          const mes = hoje.getMonth() - data.getMonth()
          if (mes < 0 || (mes === 0 && hoje.getDate() < data.getDate())) {
            idade--
          }
          if (idade < 15) {
            msg = 'O estudante deve ter pelo menos 15 anos.'
          }
        }
      }
      break
    case 'bi':
      if (e.bi && !isValidBI(e.bi)) msg = 'BI inválido. Use 10 dígitos + 2 letras maiúsculas (ex: 1234567890AB).'
      break
    case 'telefone_pessoal':
      if (e.telefone_pessoal && !isValidMocambiquePhone(e.telefone_pessoal))
        msg = 'Telefone inválido. Use 9 dígitos começando com 8 (ex: 84 123 4567).'
      break
    case 'nuit':
      if (e.nuit && !isOnlyDigits(e.nuit)) msg = 'NUIT deve conter apenas números.'
      break
    case 'email_pessoal':
      if (e.email_pessoal && !isValidEmail(e.email_pessoal)) msg = 'Email inválido.'
      break
    case 'ano_lectivo':
      if (!e.ano_lectivo) msg = 'Ano lectivo é obrigatório.'
      break
    case 'encarregado_nome':
      if (!enc.nome_completo?.trim()) msg = 'Nome do encarregado é obrigatório.'
      break
    case 'telefone_principal':
      if (!enc.telefone_principal?.trim()) msg = 'Telefone principal é obrigatório.'
      else if (!isValidMocambiquePhone(enc.telefone_principal))
        msg = 'Telefone inválido. Use 9 dígitos começando com 8 (ex: 84 123 4567).'
      break
    case 'telefone_alternativo':
      if (enc.telefone_alternativo && !isValidMocambiquePhone(enc.telefone_alternativo))
        msg = 'Telefone alternativo inválido. Use 9 dígitos começando com 8.'
      break
    case 'encarregado_bi':
      if (enc.bi && !isValidBI(enc.bi)) msg = 'BI inválido. Use 10 dígitos + 2 letras maiúsculas.'
      break
    default:
      break
  }

  errors.value[field] = msg
}

// --- Valida todos os campos, retorna true se válido ---
const validateForm = (): boolean => {
  const fields = [
    'nome_completo', 'curso', 'genero', 'quarto', 'data_nascimento',
    'bi', 'telefone_pessoal', 'nuit', 'email_pessoal', 'ano_lectivo',
    'encarregado_nome', 'telefone_principal', 'telefone_alternativo', 'encarregado_bi'
  ]
  fields.forEach(f => validateField(f))
  return Object.values(errors.value).every(msg => msg === '')
}

// --- Carregar quartos ---
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

// --- Quartos filtrados por bloco e género ---

// --- Se mudar o género, limpar a seleção de quarto se não for compatível ---
watch(() => form.value.estudante.genero, (novo) => {
  if (form.value.estudante.quarto) {
    const quartoSelecionado = listaQuartos.value.find(q => q.id === form.value.estudante.quarto)
    if (quartoSelecionado && quartoSelecionado.genero_permitido !== novo) {
      form.value.estudante.quarto = null
    }
  }
})

// --- Submissão ---
async function handleRegister() {
  if (!validateForm()) {
    // Rola para o primeiro campo com erro
    const firstError = Object.keys(errors.value).find(key => errors.value[key])
    if (firstError) {
      const el = document.querySelector(`[data-field="${firstError}"]`) as HTMLElement
      if (el) el.focus()
    }
    return
  }

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

    // Limpar formulário
    form.value = {
      estudante: {
        nome_completo: '',
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
    filtroBloco.value = ''
    // Limpar erros
    Object.keys(errors.value).forEach(key => errors.value[key] = '')

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
// --- Autocomplete de quarto ---
const buscaQuarto = ref('')
const mostrarSugestoes = ref(false)
const quartoSelecionadoId = ref<number | null>(null)
const quartoInput = ref<HTMLInputElement | null>(null)

// Filtro com base no texto de busca (apenas bloco) e género
const quartosFiltrados = computed(() => {
  let quartos = listaQuartos.value

  // Filtrar por género
  if (form.value.estudante.genero) {
    quartos = quartos.filter(q => q.genero_permitido === form.value.estudante.genero)
  }

  // Filtrar apenas por bloco (removemos a busca por número)
  if (buscaQuarto.value.trim()) {
    const termo = buscaQuarto.value.trim().toLowerCase()
    quartos = quartos.filter(q => q.bloco.toLowerCase().includes(termo))
  }

  // Ordenar por bloco
  return [...quartos].sort((a, b) => a.bloco.localeCompare(b.bloco))
})

// Função para filtrar (disparada a cada input)
const filtrarQuartos = () => {
  mostrarSugestoes.value = true
}

// Selecionar um quarto da lista
const selecionarQuarto = (quarto: any) => {
  // Mostramos o bloco e a lotação no campo (opcional)
  buscaQuarto.value = `Bloco ${quarto.bloco} - ${quarto.vagas_disponiveis || 0}/${quarto.capacidade_maxima} camas`
  form.value.estudante.quarto = quarto.id
  quartoSelecionadoId.value = quarto.id
  mostrarSugestoes.value = false
  validateField('quarto')
}

// Limpar seleção
const limparQuarto = () => {
  buscaQuarto.value = ''
  form.value.estudante.quarto = null
  quartoSelecionadoId.value = null
  mostrarSugestoes.value = true
  quartoInput.value?.focus()
}

// Fechar sugestões ao perder foco
const fecharSugestoes = () => {
  setTimeout(() => {
    mostrarSugestoes.value = false
  }, 200)
}

// Se o género mudar, limpar a seleção se for incompatível
watch(() => form.value.estudante.genero, (novo) => {
  if (quartoSelecionadoId.value) {
    const quarto = listaQuartos.value.find(q => q.id === quartoSelecionadoId.value)
    if (quarto && quarto.genero_permitido !== novo) {
      limparQuarto()
    }
  }
})

// Inicializar o campo de busca com o nome do quarto selecionado (se já existir)
watch(() => form.value.estudante.quarto, (novoId) => {
  if (novoId) {
    const quarto = listaQuartos.value.find(q => q.id === novoId)
    if (quarto) {
      buscaQuarto.value = `Bloco ${quarto.bloco} - ${quarto.vagas_disponiveis || 0}/${quarto.capacidade_maxima} camas`
      quartoSelecionadoId.value = novoId
    }
  } else {
    buscaQuarto.value = ''
    quartoSelecionadoId.value = null
  }
})
</script>

<style scoped>
.label {
  @apply block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1;
}

.input {
  @apply w-full px-4 py-2.5 bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-lg text-sm text-slate-900 dark:text-white placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors;
}

/* Estilo para campos com erro */
.input.border-red-500 {
  border-color: #ef4444;
}

.input.border-red-500:focus {
  box-shadow: 0 0 0 2px rgba(239, 68, 68, 0.3);
  border-color: #ef4444;
}
</style>
<template>
  <div class="space-y-6 dark:text-white">
    <!-- Header e Link de Voltar -->
    <div>
      <NuxtLink to="/dashboard/admin/estudantes" class="text-blue-600 dark:text-blue-400 hover:underline mb-2 block">
        &larr; Voltar para a lista de estudantes
      </NuxtLink>

      <!-- O 'v-if' aqui já lidava com o 'student' ser null -->
      <h1 v-if="student" class="text-3xl font-bold">
        Perfil: {{ student.nome_completo }}
      </h1>
      <div v-else class="h-8 bg-gray-200 dark:bg-gray-700 rounded w-1/2 animate-pulse"></div>
    </div>

    <!-- Navegação das Abas (Tabs) -->
    <div class="border-b border-gray-200 dark:border-gray-700">
      <nav class="flex -mb-px space-x-6" aria-label="Tabs">
        <button v-for="tab in tabs" :key="tab.id" @click="activeTab = tab.id" :class="[
          activeTab === tab.id
            ? 'border-blue-500 text-blue-600 dark:text-blue-400'
            : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 hover:border-gray-300 dark:hover:border-gray-600',
          'whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm'
        ]">
          {{ tab.name }}
        </button>
      </nav>
    </div>

    <!-- Conteúdo das Abas (Componentes) -->
    <div class="mt-6">
      <!-- Aba 1: Detalhes do Estudante (Formulário de Edição) -->
      <div v-show="activeTab === 'detalhes'">

        <AdminDetalhes v-if="student && options" :student="student" :opcoes-estado="options.estudante_estados"
          @student-updated="studentRefresh()" />
      </div>

      <!-- Aba 2: Histórico Financeiro -->
      <div v-show="activeTab === 'financas'">

        <AdminFinancas v-if="finances && options" :finances="finances" :student-id="studentId"
          :opcoes-estado="options.mensalidade_estados" :opcoes-metodo="options.mensalidade_metodos"
          @update-list="financesRefresh()" />
      </div>

      <!-- Aba 3: Histórico Disciplinar -->
      <div v-show="activeTab === 'disciplina'">

        <AdminDisciplina v-if="discipline && options" :discipline="discipline" :student-id="studentId"
          :opcoes-tipo="options.sancao_tipos" @update-list="disciplineRefresh()" />
      </div>

      <!-- Aba 4: Histórico de Presenças -->
      <div v-show="activeTab === 'presencas'">

        <AdminPresencas v-if="attendance && options" :attendance="attendance" :opcoes-estado="options.presenca_estados"
          @update-list="attendanceRefresh()" />
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
// Define o layout padrão (com sidebar)
definePageMeta({
  layout: 'default'
})

// Definição das abas
const tabs = [
  { id: 'detalhes', name: 'Detalhes' },
  { id: 'financas', name: 'Finanças' },
  { id: 'disciplina', name: 'Disciplina' },
  { id: 'presencas', name: 'Presenças' },
]

const activeTab = ref('detalhes') // A aba ativa por padrão

// Hooks de autenticação e rota
const { api } = useApi()
const route = useRoute()
const studentId = route.params.id as string


// --- CORRECÇÃO AQUI ---
// Removemos 'await' e adicionámos 'lazy: true' a TODOS os fetches
// para garantir um comportamento consistente no carregamento e navegação.

// 1. Buscar as Opções (para os dropdowns dos formulários)
const { data: options } = await useAsyncData(
  `opcoes-${studentId}`, // Chave única
  () => api<any>('/opcoes/') // O 'api' já sabe o baseURL e o token
)
const { data: student, refresh: studentRefresh } = await useAsyncData(
  `student-${studentId}-details`, // Chave única
  () => api<any>(`/estudantes/${studentId}/`)
)

// Os dados das abas (lazy: true) carregam em segundo plano
const { data: finances, refresh: financesRefresh } = useAsyncData(
  `student-${studentId}-finances`,
  () => api<any>(`/estudantes/${studentId}/mensalidades/`),
  { lazy: true }
)

const { data: discipline, refresh: disciplineRefresh } = useAsyncData(
  `student-${studentId}-discipline`,
  () => api<any>(`/estudantes/${studentId}/sancoes/`),
  { lazy: true }
)

const { data: attendance, refresh: attendanceRefresh } = useAsyncData(
  `student-${studentId}-attendance`,
  () => api<any>(`/estudantes/${studentId}/presencas/`),
  { lazy: true }
)
</script>
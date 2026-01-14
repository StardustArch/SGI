<template>
  <div class="space-y-6 dark:text-white">
    <h1 class="text-3xl font-bold">Gestão de Estudantes</h1>

    <!-- Barra de Ações: Pesquisa e Botão de Adicionar -->
    <div class="flex flex-col md:flex-row justify-between items-center gap-4">
      <!-- Barra de Pesquisa -->
      <div class="w-full md:w-1/2">
        <input 
          v-model="searchQuery"
          type="text" 
          placeholder="Pesquisar por nome ou nº de estudante..."
          class="w-full px-4 py-2 border rounded-md shadow-sm bg-gray-50 dark:bg-gray-700 dark:text-white dark:border-gray-600 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
        />
      </div>
      
      <!-- Botão de Registar Novo -->
      <NuxtLink 
        to="/dashboard/admin/estudantes/registar" 
        class="w-full md:w-auto px-4 py-2 text-center font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600"
      >
        Registar Novo Estudante
      </NuxtLink>
    </div>

    <!-- Feedback de Carregamento -->
    <div v-if="pending" class="text-center text-gray-500 dark:text-gray-400">
      A carregar lista de estudantes...
    </div>

    <!-- Tabela de Estudantes -->
    <div v-else-if="students" class="overflow-x-auto bg-white dark:bg-gray-800 rounded-lg shadow">
      <table class="w-full min-w-max">
        <thead class="bg-gray-50 dark:bg-gray-700">
          <tr>
            <th class="table-header">Nome Completo</th>
            <th class="table-header">N.º Estudante</th>
            <th class="table-header">Quarto</th>
            <th class="table-header">Curso</th>
            <th class="table-header">Encarregado</th>
            <th class="table-header">Ações</th>
          </tr>
        </thead>
        <tbody class="divide-y dark:divide-gray-700">
          
          <tr v-if="students.length === 0">
            <td colspan="6" class="p-6 text-center text-gray-500 dark:text-gray-400">
              Nenhum estudante encontrado.
            </td>
          </tr>

          <tr v-for="student in students" :key="student.utilizador_id" class="hover:bg-gray-50 dark:hover:bg-gray-700">
            <td class="table-cell font-medium">{{ student.nome_completo }}</td>
            <td class="table-cell">{{ student.num_estudante }}</td>
            <td class="table-cell">{{ student.quarto }}</td>
            <td class="table-cell">{{ student.curso }}</td>
            <td class="table-cell">{{ student.encarregado_nome }}</td>
            <td class="table-cell">
              <!-- Link para a página de detalhes (que criaremos a seguir) -->
              <NuxtLink 
                :to="`/dashboard/admin/estudantes/${student.utilizador_id}`" 
                class="font-medium text-blue-600 dark:text-blue-400 hover:underline"
              >
                Ver Detalhes
              </NuxtLink>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
// Define o tipo de dados que esperamos da API
interface Estudante {
  utilizador_id: number;
  nome_completo: string;
  num_estudante: string;
  quarto: string;
  curso: string;
  encarregado_nome: string;
}

// 2. Obter a função 'api' do composable
const { api } = useApi()
const searchQuery = ref('') // O estado da nossa barra de pesquisa (isto fica)

// 3. O 'accessToken' e 'headers' manuais foram REMOVIDOS
//    (O 'useApi' trata disto agora)

// 4. Substituímos 'useFetch' por 'useAsyncData'
const { data: students, pending, error, refresh } = await useAsyncData<Estudante[]>(
  'student-list', // Chave única para este fetch
  () => api('/estudantes/', { // O 'api' já sabe o baseURL e o token
    // Passamos os query params para a sua função 'api'
    query: {
      search: searchQuery.value 
    }
  }),
  {
    lazy: true, // Não bloqueia a navegação
    // 'watch' vai re-executar este useAsyncData sempre que
    // o 'searchQuery' mudar, o que faz a pesquisa funcionar!
    watch: [searchQuery]
  }
)
</script>
<style scoped>
/* Estilos comuns para a tabela */
.table-header {
  @apply px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider;
}
.table-cell {
  @apply px-6 py-4 whitespace-nowrap text-sm;
}
</style>
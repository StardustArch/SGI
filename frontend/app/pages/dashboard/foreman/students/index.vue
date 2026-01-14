<template>
  <div class="space-y-6 dark:text-white max-w-6xl">
    <h1 class="text-3xl font-bold">Meus Educandos</h1>

    <div v-if="pending" class="dark:text-gray-300">
      A carregar lista de educandos...
    </div>

    <div v-else class="overflow-x-auto bg-white dark:bg-gray-800 rounded-lg shadow">
      <table class="w-full min-w-max">
        <thead class="bg-gray-50 dark:bg-gray-700">
          <tr>
            <th class="table-header">Nome Completo</th>
            <th class="table-header">N.º Estudante</th>
            <th class="table-header">Quarto</th>
            <th class="table-header">Curso</th>
            <th class="table-header">Estado</th>
          </tr>
        </thead>
        <tbody class="divide-y dark:divide-gray-700">
          
          <tr v-if="!educandos || educandos.length === 0">
            <td colspan="5" class="p-6 text-center text-gray-500 dark:text-gray-400">
              Nenhum educando encontrado.
            </td>
          </tr>

          <tr v-for="estudante in educandos" :key="estudante.utilizador_id" class="hover:bg-gray-50 dark:hover:bg-gray-700">
            <td class="table-cell font-medium">{{ estudante.nome_completo }}</td>
            <td class="table-cell">{{ estudante.num_estudante }}</td>
            <td class="table-cell">{{ estudante.quarto }}</td>
            <td class="table-cell">{{ estudante.curso }}</td>
            <td class="table-cell">
              <span :class="estudante.estado === 'Activo' ? 'status-green' : 'status-yellow'">
                {{ estudante.estado }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

  </div>
</template>

<script setup lang="ts">

const { api } = useApi()

// Define o tipo de dados que esperamos da API
interface Educando {
  utilizador_id: number;
  nome_completo: string;
  num_estudante: string;
  quarto: string;
  curso: string;
  estado: string;
  encarregado_nome: string;
}

// 1. Buscar APENAS a lista de educandos
const { data: educandos, pending } = await useAsyncData(
  'encarregado-educandos',
  () => api<Educando[]>('/perfil-encarregado/meus-educandos/'),
  { lazy: true, default: () => [] }
)

// 2. O 'computed' (perfilEducandos) foi removido pois não é mais necessário.
</script>

<style scoped>
/* Estilos comuns para tabelas e status */
.table-header { @apply px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase; }
.table-cell { @apply px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white; }
.status-green { @apply px-2 py-0.5 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800 dark:bg-green-800 dark:text-green-100; }
.status-yellow { @apply px-2 py-0.5 inline-flex text-xs leading-5 font-semibold rounded-full bg-yellow-100 text-yellow-800 dark:bg-yellow-800 dark:text-yellow-100; }
</style>